import streamlit as st
from functions import parse_live_match, parsed_player_statistics, draymond, shot_efficiency, controversial_fact, bum, hot_hands, shot_map, match_odds
import matplotlib.pyplot as plt
import pandas as pd
import time
import logging
from api import live_matches_data

# Set layout to wide
st.set_page_config(layout="wide")


def display_shot_map(match_id, home_team_id, away_team_id, fig, ax):
    try:
        shot_map_home = shot_map(match_id, home_team_id)
        shot_map_away = shot_map(match_id, away_team_id)

        ax.scatter(shot_map_home['made']['x'], shot_map_home['made']['y'],
                   color='black', marker='x', label='Made Shot', alpha=0.5)
        ax.scatter(shot_map_home['missed']['x'], shot_map_home['missed']['y'],
                   color='green', marker='o', label='Missed Shot', alpha=0.5)

        fig.suptitle(home_team + ' Shot Map')

        ax.scatter(shot_map_away['made']['x'], shot_map_away['made']['y'],
                   color='black', marker='x', label='Made Shot', alpha=0.5)
        ax.scatter(shot_map_away['missed']['x'], shot_map_away['missed']['y'],
                   color='green', marker='o', label='Missed Shot', alpha=0.5)

        fig.suptitle(away_team + ' Shot Map')
    except Exception as e:
        logging.error(f"Error displaying shot map: {e}")
    return fig


def display_player_statistics(match_id):
    player_statistics = parsed_player_statistics(match_id)
    return [pd.DataFrame(player_statistics['home']).T, pd.DataFrame(player_statistics['away']).T]


fact_match = parse_live_match(0)
fact_match_id = fact_match.pop('id')
homeTeamName = fact_match['home']
awayTeamName = fact_match['away']


def display_draymond(match_id):
    dray = draymond(match_id)
    return f"{homeTeamName}: {dray[0]}", f"{awayTeamName}: {dray[1]}"


def generate_fact(match_id):
    fact = controversial_fact(match_id)
    return fact


def display_shot_efficiency(match_id):
    eff = shot_efficiency(match_id)
    return f"{homeTeamName}: {str(round(eff[0], 2))}%", f"{awayTeamName}: {str(round(eff[1], 2))}%"


def display_hot_hands(match_id):
    hot = hot_hands(match_id)
    return f"{homeTeamName}: {hot[0]}", f"{awayTeamName}: {hot[1]}"


def display_bum(match_id):
    bum_stat = bum(match_id)
    return f"{homeTeamName}: {bum_stat[0]}", f"{awayTeamName}: {bum_stat[1]}"


def display_match_odds(match_id):
    mo = match_odds(match_id)
    return f"{homeTeamName}: {str(round(mo[0], 2))}%", f"{awayTeamName}: {str(round(mo[1], 2))}%"


def run_app(event_number):
    stat_title = st.empty()
    placeholder_home_player_statistics = st.empty()
    placeholder_away_player_statistics = st.empty()
    placeholder_shot_map = st.empty()
    court_img = plt.imread('./images/shot_chart.webp')
    fig, ax = plt.subplots()
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
        -1: "./images/text.png",
        0: "./images/text.png",
        1: "./images/text.png",
        2: "./images/text.png",
        3: "./images/text.png",
        4: "./images/text.png",
        5: "./images/text.png",
        6: "./images/text.png"
    }

    for seconds in range(30):
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

        if switch == -1:  # General Statistics
            next = display_shot_map(
                match_id, home_team_id, away_team_id, fig, ax)
            switch = 0
        elif switch == 0:  # Player Shotmap
            stat_title.image(image_map[switch])
            placeholder_shot_map.pyplot(next)
            next = display_draymond(match_id)
            time.sleep(2)
            switch += 1
        elif switch == 1:  # Draymond/Foul
            stat_title.image(image_map[switch])
            placeholder_draymond.title(next[0])
            placeholder_draymond_2.title(next[1])
            next = display_hot_hands(match_id)
            time.sleep(2)
            switch += 1
        elif switch == 2:  # Hot Hands
            stat_title.image(image_map[switch])
            placeholder_hot_hands.title(next[0])
            placeholder_hot_hands_2.title(next[1])
            next = display_bum(match_id)
            time.sleep(2)
            switch += 1
        elif switch == 3:  # Bum
            stat_title.image(image_map[switch])
            placeholder_bum.title(next[0])
            placeholder_bum_2.title(next[1])
            next = display_shot_efficiency(match_id)
            time.sleep(2)
            switch += 1
        elif switch == 4:  # Shot Efficiency
            stat_title.image(image_map[switch])
            placeholder_shot_efficiency.title(next[0])
            placeholder_shot_efficiency_2.title(next[1])
            next = display_match_odds(match_id)
            time.sleep(2)
            switch += 1
        elif switch == 5:  # Match Odds
            stat_title.image(image_map[switch])
            placeholder_match_odds.title(next[0])
            placeholder_match_odds_2.title(next[1])
            next = fact
            time.sleep(2)
            switch += 1
        elif switch == 6:  # Fun Fact
            stat_title.image(image_map[switch])
            placeholder_fact.title(next)
            next = 1
            time.sleep(2)
            switch += 1
        elif switch == 7:
            switch = -1


data = live_matches_data()
placeholders = []
buttons = []

if len(data['events']) == 0:
    st.title("No Games Currently")
else:
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
        if game_start.button("Run", key=index):
            for button in buttons:
                button.empty()
            for placeholder in placeholders:
                placeholder.empty()
            run_app(index)
            break
