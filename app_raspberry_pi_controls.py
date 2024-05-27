import streamlit as st
import time
import RPi.GPIO as GPIO
from gpiozero import MCP3008
from functions import parse_live_match, parsed_player_statistics, draymond, shot_efficiency, controversial_fact, bum, hot_hands, shot_map, match_odds
import matplotlib.pyplot as plt
import pandas as pd
import logging
import matplotlib.image as mpimg
from api import live_matches_data

# GPIO and Potentiometer setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
buttonPin = 37
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
pot = MCP3008(0)

# Initialize session state variables
if 'displaying_stats' not in st.session_state:
    st.session_state.displaying_stats = False
if 'selected_event' not in st.session_state:
    st.session_state.selected_event = None
if 'num_games' not in st.session_state:
    st.session_state.num_games = 0

# Functions to handle hardware control states


def handle_hardware_controls():
    pot_value = pot.value
    new_game_index = int(pot_value * (st.session_state.num_games - 1))

    if new_game_index != st.session_state.selected_event:
        st.session_state.selected_event = new_game_index
        st.experimental_rerun()

    button_state = GPIO.input(buttonPin)
    if button_state == GPIO.LOW:
        if st.session_state.displaying_stats:
            st.session_state.displaying_stats = False
            st.session_state.selected_event = None
        else:
            st.session_state.displaying_stats = True
        st.experimental_rerun()

# Function to display shot map


def display_shot_map(match_id, home_team_id, away_team_id, fig, ax):
    try:
        shot_map_home = shot_map(match_id, home_team_id)
        shot_map_away = shot_map(match_id, away_team_id)
        ax.scatter(shot_map_home['made']['x'], shot_map_home['made']['y'],
                   color='black', marker='x', label='Made Shot', alpha=0.5)
        ax.scatter(shot_map_home['missed']['x'], shot_map_home['missed']['y'],
                   color='green', marker='o', label='Missed Shot', alpha=0.5)
        fig.suptitle('Home Team Shot Map')
        ax.scatter(shot_map_away['made']['x'], shot_map_away['made']['y'],
                   color='black', marker='x', label='Made Shot', alpha=0.5)
        ax.scatter(shot_map_away['missed']['x'], shot_map_away['missed']['y'],
                   color='green', marker='o', label='Missed Shot', alpha=0.5)
        fig.suptitle('Away Team Shot Map')
    except Exception as e:
        logging.error(f"Error displaying shot map: {e}")
    return fig

# Function to display player statistics


def display_player_statistics(match_id):
    player_statistics = parsed_player_statistics(match_id)
    return [pd.DataFrame(player_statistics['home']).T, pd.DataFrame(player_statistics['away']).T]


def display_image(image_path):
    img = mpimg.imread(image_path)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(img)
    ax.axis('off')
    fig.suptitle("Shot Chart", fontsize=16)
    return fig

# Functions to display various match statistics


def display_draymond(match_id):
    dray = draymond(match_id)
    return f"Home Team: {dray[0]}", f"Away Team: {dray[1]}"


def generate_fact(match_id):
    fact = controversial_fact(match_id)
    return fact


def display_shot_efficiency(match_id):
    eff = shot_efficiency(match_id)
    return f"Home Team: {str(round(eff[0], 2))}%", f"Away Team: {str(round(eff[1], 2))}%"


def display_hot_hands(match_id):
    hot = hot_hands(match_id)
    return f"Home Team: {hot[0]}", f"Away Team: {hot[1]}"


def display_bum(match_id):
    bum_stat = bum(match_id)
    return f"Home Team: {bum_stat[0]}", f"Away Team: {bum_stat[1]}"


def display_match_odds(match_id):
    mo = match_odds(match_id)
    return f"Home Team: {str(round(mo[0], 2))}%", f"Away Team: {str(round(mo[1], 2))}%"


def run_app(event_number):
    stat_title = st.empty()
    placeholder_home_player_statistics = st.empty()
    placeholder_away_player_statistics = st.empty()
    placeholder_shot_map = st.empty()
    court_img = plt.imread('./images/shot_chart.webp')
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.imshow(court_img, extent=[-250, 250, -47.5, 422.5])
    ax.axis('off')

    switch = -1
    next = 0

    placeholder_draymond = st.empty()
    placeholder_draymond_2 = st.empty()
    placeholder_hot_hands = st.empty()
    placeholder_hot_hands_2 = st.empty()
    placeholder_bum = st.empty()
    placeholder_bum_2 = st.empty()
    placeholder_shot_efficiency = st.empty()
    placeholder_shot_efficiency_2 = st.empty()
    placeholder_match_odds = st.empty()
    placeholder_match_odds_2 = st.empty()
    placeholder_fact = st.empty()

    global homeTeamName
    global awayTeamName

    fact_match = parse_live_match(0)
    fact_match_id = fact_match.pop('id')
    homeTeamName = fact_match['home']
    awayTeamName = fact_match['away']
    fact = generate_fact(fact_match_id)

    image_map = {
        -1: "./images/shotmap.png",
        0: "./images/shotmap.png",
        1: "./images/foul.png",
        2: "./images/hot_hands.png",
        3: "./images/bum.png",
        4: "./images/shot_efficiency.png",
        5: "./images/match_odds.png",
        6: "./images/fun_fact.png"
    }

    if st.button("Back", key=f"back_button_{event_number}"):
        st.session_state.displaying_stats = False
        st.session_state.selected_event = None
        st.experimental_rerun()

    for seconds in range(30):
        if not st.session_state.displaying_stats:
            break

        match = parse_live_match(0)
        match_id = match.pop('id')
        home_team_id = match.pop('home_team_id')
        away_team_id = match.pop('away_team_id')
        home_team = match.pop('home')
        away_team = match.pop('away')

        stat_title.empty()
        placeholder_away_player_statistics.empty()
        placeholder_home_player_statistics.empty()
        placeholder_shot_map.empty()
        placeholder_draymond.empty()
        placeholder_draymond_2.empty()
        placeholder_shot_efficiency.empty()
        placeholder_shot_efficiency_2.empty()
        placeholder_hot_hands.empty()
        placeholder_hot_hands_2.empty()
        placeholder_bum.empty()
        placeholder_bum_2.empty()
        placeholder_fact.empty()
        placeholder_match_odds.empty()
        placeholder_match_odds_2.empty()

        if switch == -1:
            next = display_shot_map(
                match_id, home_team_id, away_team_id, fig, ax)
            switch = 0
        elif switch == 0:
            placeholder_shot_map.pyplot(next)
            next = display_draymond(match_id)
            time.sleep(2)
            switch += 1
        elif switch == 1:
            stat_title.image(image_map[switch])
            placeholder_draymond.markdown(
                f"<div><h1>{next[0]}</h1></div>", unsafe_allow_html=True)
            placeholder_draymond_2.markdown(
                f"<div><h1>{next[1]}</h1></div>", unsafe_allow_html=True)
            next = display_hot_hands(match_id)
            time.sleep(2)
            switch += 1
        elif switch == 2:
            stat_title.image(image_map[switch])
            placeholder_hot_hands.markdown(
                f"<div><h1>{next[0]}</h1></div>", unsafe_allow_html=True)
            placeholder_hot_hands_2.markdown(
                f"<div><h1>{next[1]}</h1></div>", unsafe_allow_html=True)
            next = display_bum(match_id)
            time.sleep(2)
            switch += 1
        elif switch == 3:
            stat_title.image(image_map[switch])
            placeholder_bum.markdown(
                f"<div><h1>{next[0]}</h1></div>", unsafe_allow_html=True)
            placeholder_bum_2.markdown(
                f"<div><h1>{next[1]}</h1></div>", unsafe_allow_html=True)
            next = display_shot_efficiency(match_id)
            time.sleep(2)
            switch += 1
        elif switch == 4:
            stat_title.image(image_map[switch])
            placeholder_shot_efficiency.markdown(
                f"<div><h1>{next[0]}</h1></div>", unsafe_allow_html=True)
            placeholder_shot_efficiency_2.markdown(
                f"<div><h1>{next[1]}</h1></div>", unsafe_allow_html=True)
            next = display_match_odds(match_id)
            time.sleep(2)
            switch += 1
        elif switch == 5:
            stat_title.image(image_map[switch])
            placeholder_match_odds.markdown(
                f"<div><h1>{next[0]}</h1></div>", unsafe_allow_html=True)
            placeholder_match_odds_2.markdown(
                f"<div><h1>{next[1]}</h1></div>", unsafe_allow_html=True)
            next = fact
            time.sleep(2)
            switch += 1
        elif switch == 6:
            stat_title.image(image_map[switch])
            placeholder_fact.title(next)
            next = 1
            time.sleep(2)
            switch += 1
        elif switch == 7:
            switch = -1


# Main app logic
data = live_matches_data()
placeholders = []
buttons = []

if len(data['events']) == 0:
    st.title("No Games Currently")
else:
    st.session_state.num_games = len(data['events'])
    if not st.session_state.displaying_stats:
        for index, game in enumerate(data['events']):
            home_team = game['homeTeam']['name']
            away_team = game['awayTeam']['name']
            emp = st.empty()
            placeholders.append(emp)
            game_name, game_score, game_start = emp.columns([6, 4, 1])
            game_name.markdown(f"##### {home_team} vs. {away_team}")
            game_score.markdown(
                f"##### {game['homeScore']['current']} - {game['awayScore']['current']}")
            game_start = game_start.empty()
            buttons.append(game_start)
            if game_start.button("Run", key=f"run_button_{index}"):
                st.session_state.displaying_stats = True
                st.session_state.selected_event = index
                for button in buttons:
                    button.empty()
                for placeholder in placeholders:
                    placeholder.empty()
                run_app(index)
                break
    else:
        run_app(st.session_state.selected_event)

# Continuously check for hardware input
while True:
    handle_hardware_controls()
    time.sleep(0.1)
