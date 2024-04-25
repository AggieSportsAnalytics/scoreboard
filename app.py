import streamlit as st
from functions import parse_live_match
from functions import parsed_player_statistics
import pandas as pd
import time


match = parse_live_match(0) # get the match initially to write the team names
homeTeam = match['home']
awayTeam = match['away']
st.title(homeTeam + ' vs. ' + awayTeam)
placeholder = st.empty() # create a placeholder to keep track of the live data
st.title(homeTeam)
placeholder_home_player_statistics = st.empty()
st.title(awayTeam)
placeholder_away_player_statistics = st.empty()

for seconds in range(30): # max one minute so that it doesn't accidentally run in the background
    match = parse_live_match(0)
    print("bomboclaat")
    match_id = match.pop('id') # pop the id from match so it is not displayed
    home_team = match.pop('home')
    away_team = match.pop('away')
    placeholder.table(match)

    player_statistics = parsed_player_statistics(match_id)

    placeholder_home_player_statistics.table(pd.DataFrame(player_statistics['home']).T) # pandas and .T is to transpose the data 
    placeholder_away_player_statistics.table(pd.DataFrame(player_statistics['away']).T)

    time.sleep(2) # update data every two
