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
from api import live_matches_data
import matplotlib.pyplot as plt
import pandas as pd
import time

st.set_page_config(layout="wide")


def display_shot_map(match_id, home_team_id, away_team_id, fig, ax):
    shot_map_home = shot_map(match_id, home_team_id)
    shot_map_away = shot_map(match_id, away_team_id)

    ax.scatter(shot_map_home['made']['x'], shot_map_home['made']['y'],
               color='black', marker='x', label='Made Shot', alpha=0.5)
    ax.scatter(shot_map_home['missed']['x'], shot_map_home['missed']
               ['y'], color='green', marker='o', label='Missed Shot', alpha=0.5)

    fig.suptitle(' Shot Map')

    ax.scatter(shot_map_away['made']['x'], shot_map_away['made']['y'],
               color='black', marker='x', label='Made Shot', alpha=0.5)
    ax.scatter(shot_map_away['missed']['x'], shot_map_away['missed']
               ['y'], color='green', marker='o', label='Missed Shot', alpha=0.5)

    fig.suptitle(' Shot Map')
    return fig


def display_player_statistics(match_id, home_placeholder, away_placeholder):
    player_statistics = parsed_player_statistics(match_id)

    return [pd.DataFrame(player_statistics['home']).T, pd.DataFrame(player_statistics['away']).T]


def display_draymond(match_id):
    dray = draymond(match_id)
    return dray


def display_controversial_fact(match_id):
    fact = controversial_fact(match_id)
    return fact


# match = parse_live_match(0) # get the match initially to write the team names
# homeTeam = match['home']
# awayTeam = match['away']
# st.title(homeTeam + ' vs. ' + awayTeam)
# placeholder = st.empty() # create a placeholder to keep track of the live data
# st.title(homeTeam)



def display_shot_efficiency(match_id):
    eff = shot_efficiency(match_id)
    return eff


def display_hot_hands(match_id):
    hot = hot_hands(match_id)
    return hot


def display_bum(match_id):
    bum_stat = bum(match_id)
    return bum_stat


def display_match_odds(match_id):
    match_odds = match_odds(match_id)
    return match_odds


# max one minute so that it doesn't accidentally run in the background

def run_app(event_number):
    placeholder_home_player_statistics = st.empty()
    # st.title(awayTeam)
    placeholder_away_player_statistics = st.empty()

    # FACT (openai is expensive lol and its kinda slow rn)
    # initial_match_id = match.pop('id')
    # fact = controversial_fact(initial_match_id)
    # print("Fact: ", fact)

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
    stat_title = st.empty()
    for seconds in range(30):
        match = parse_live_match(event_number)
        match_id = match.pop('id')  # pop the id from match so it is not displayed
        home_team_id = match.pop('home_team_id')
        away_team_id = match.pop('away_team_id')
        home_team = match.pop('home')
        away_team = match.pop('away')

        # print out the stats except for fact + map
        # bum_stat = bum(match_id)
        # hot_hands_stat = hot_hands(match_id)
        # draymond_stat = draymond(match_id)
        # match_odds_stat = match_odds(match_id)
        # shot_efficiency_stat = shot_efficiency(match_id)
        # print("bum: ", bum_stat)
        # print("hot hands: ", hot_hands_stat)
        # print("draymond: ", draymond_stat)
        # print("match odds: ", match_odds_stat)
        # print("shot efficiency: ", shot_efficiency_stat)

        # placeholder.table(match)
        # match_odds_data = match_odds(match_id)

        # Next is declared after the placeholder is updated otherwise there is a large pause between stats
        # due to the api calling time, so im calling it afterwards instead

        # TODO: Create more "display" functions for the other stats

        placeholder_away_player_statistics.empty()
        placeholder_home_player_statistics.empty()
        placeholder_shot_map.empty()
        placeholder_draymond.empty()
        placeholder_shot_efficiency.empty()
        placeholder_hot_hands.empty()
        placeholder_bum.empty()
        placeholder_match_odds.empty()
        stat_title.empty()
        if switch == -1:  # next needs to be initialized to a base value
            next = display_player_statistics(
                match_id, placeholder_home_player_statistics, placeholder_away_player_statistics)
            switch = 0
        elif switch == 0:
            switch += 1
            # general
            stat_title.title("general")
            placeholder_home_player_statistics.table(next[0])
            placeholder_away_player_statistics.table(next[1])
            next = display_shot_map(match_id, home_team_id,
                                    away_team_id, fig, ax)
            # placeholder_away_player_statistics.title("1")
            time.sleep(2)
        elif switch == 1:
            switch += 1
            # shotmap
            stat_title.title("shotmap")
            placeholder_shot_map.pyplot(next)
            next = display_draymond(
                match_id)
            # placeholder_shot_map.title("2")
            time.sleep(2)
        elif switch == 2:
            switch += 1
            # draymond
            stat_title.title("draymond")
            placeholder_draymond.title(next)
            next = display_hot_hands(
                match_id)
            time.sleep(2)
        elif switch == 3:
            switch += 1
            # hot hands
            stat_title.title("hot hands")
            placeholder_hot_hands.title(next)
            next = display_bum(
                match_id)
            time.sleep(2)
        elif switch == 4:
            switch += 1
            # bum
            stat_title.title("bum")
            placeholder_bum.title(next)
            next = display_shot_efficiency(
                match_id)
            time.sleep(2)
        elif switch == 4:
            switch += 1
            # shot efficiency
            stat_title.title("shot efficiency")
            placeholder_shot_efficiency.title(next)
            next = display_match_odds(
                match_id)
            time.sleep(2)
        elif switch == 5:
            switch += 1
            # match odds
            stat_title.title("match odds")
            placeholder_match_odds.title(next)
            next = 1
            time.sleep(2)
        elif switch == 6:
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
        game_score.markdown(f"##### {game['homeScore']['current']} - {game['awayScore']['current']}")
        game_start = game_start.empty()
        buttons.append(game_start)
        if game_start.button("Run", key = index):
            for button in buttons:
                button.empty()
            for placeholder in placeholders:
                placeholder.empty()
            run_app(index)

            break

