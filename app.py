import streamlit as st
from functions import parse_live_match
from functions import parsed_player_statistics
from functions import draymond
from functions import shot_efficiency
from functions import controversial_fact
from functions import bum
from functions import hot_hands
from functions import shot_map
from functions import match_odds
import matplotlib.pyplot as plt
import pandas as pd
import time
import logging
from api import live_matches_data

# layout="wide"
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
    return f"{homeTeamName}: {dray[0]} | {awayTeamName}: {dray[1]}"


def generate_fact(match_id):
    fact = controversial_fact(match_id)
    return fact


nl = '\n'


def display_shot_efficiency(match_id):
    eff = shot_efficiency(match_id)
    print(eff)
    return f"{homeTeamName}: {eff[0]}% | {awayTeamName}: {eff[1]}%"


def display_hot_hands(match_id):
    hot = hot_hands(match_id)
    return f"{homeTeamName}: {hot[0]} | {awayTeamName}: {hot[1]}"


def display_bum(match_id):
    bum_stat = bum(match_id)
    return f"{homeTeamName}: {bum_stat[0]} | {awayTeamName}: {bum_stat[1]}"


def display_match_odds(match_id):
    mo = match_odds(match_id)
    return f"{homeTeamName}: {str(round(mo[0], 2))}% | {awayTeamName}: {str(round(mo[1], 2))}%"


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
    placeholder_hot_hands = st.empty()
    placeholder_bum = st.empty()
    placeholder_shot_efficiency = st.empty()
    placeholder_match_odds = st.empty()
    placeholder_fact = st.empty()

    global homeTeamName
    global awayTeamName

    fact_match = parse_live_match(0)
    fact_match_id = fact_match.pop('id')
    homeTeamName = fact_match['home']
    awayTeamName = fact_match['away']
    print(homeTeamName)
    print(awayTeamName)
    fact = generate_fact(fact_match_id)
    print("fact generated")
    print(fact)

    # max one minute so that it doesn't accidentally run in the background
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
        placeholder_shot_efficiency.empty()
        placeholder_hot_hands.empty()
        placeholder_bum.empty()
        placeholder_fact.empty()
        placeholder_match_odds.empty()

        if switch == -1:  # next needs to be initialized to a base value
            next = display_player_statistics(
                match_id)
            switch = 0
        elif switch == 0:
            switch += 1
            # general
            stat_title.title("Game Statistics")
            placeholder_home_player_statistics.table(next[0])
            placeholder_away_player_statistics.table(next[1])
            next = display_shot_map(match_id, home_team_id,
                                    away_team_id, fig, ax)
            # placeholder_away_player_statistics.title("1")
            time.sleep(2)
        elif switch == 1:
            switch += 1
            # shotmap
            stat_title.title("Player Shotmap")
            placeholder_shot_map.pyplot(next)
            next = display_draymond(
                match_id)
            # placeholder_shot_map.title("2")
            time.sleep(2)
        elif switch == 2:
            switch += 1
            # draymond
            stat_title.title("Draymond/Foul")
            placeholder_draymond.title(next)
            st.image('./images/peter.png')
            next = display_hot_hands(
                match_id)
            time.sleep(2)
        elif switch == 3:
            switch += 1
            # hot hands
            stat_title.title("Hot Hands")
            placeholder_hot_hands.title(next)
            next = display_bum(
                match_id)
            time.sleep(2)
        elif switch == 4:
            switch += 1
            # bum
            stat_title.title("Bum")
            placeholder_bum.title(next)
            next = display_shot_efficiency(
                match_id)
            time.sleep(2)
        elif switch == 5:
            switch += 1
            # shot efficiency
            stat_title.title("Shot Efficiency")
            placeholder_shot_efficiency.title(next)
            next = display_match_odds(
                match_id)
            time.sleep(2)
        elif switch == 6:
            switch += 1
            # match odds
            stat_title.title("Match Odds")
            placeholder_match_odds.title(next)
            next = fact
            time.sleep(2)
        elif switch == 7:
            switch += 1
            # fun fact
            stat_title.title("Fun Fact")
            placeholder_fact.title(next)
            next = 1
            time.sleep(2)
        elif switch == 8:
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
