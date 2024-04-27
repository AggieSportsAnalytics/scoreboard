import streamlit as st
from functions import parse_live_match
from functions import parsed_player_statistics
from functions import shot_map
import matplotlib.pyplot as plt
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

placeholder_shot_map = st.empty()
court_img = plt.imread('./images/shot_chart.webp')
fig, ax = plt.subplots()
ax.imshow(court_img, extent=[-250, 250, -47.5, 422.5])
ax.axis('off')

for seconds in range(30): # max one minute so that it doesn't accidentally run in the background
    match = parse_live_match(0)
    match_id = match.pop('id') # pop the id from match so it is not displayed
    home_team_id = match.pop('home_team_id')
    away_team_id = match.pop('away_team_id')
    home_team = match.pop('home')
    away_team = match.pop('away')


    placeholder.table(match)

    player_statistics = parsed_player_statistics(match_id)

    placeholder_home_player_statistics.table(pd.DataFrame(player_statistics['home']).T) # pandas and .T is to transpose the data 
    placeholder_away_player_statistics.table(pd.DataFrame(player_statistics['away']).T)

    shot_map_home = shot_map(match_id, home_team_id)
    shot_map_away = shot_map(match_id, away_team_id)

    ax.scatter(shot_map_home['made']['x'], shot_map_home['made']['y'], color='black', marker='x', label='Made Shot', alpha=0.5)
    ax.scatter(shot_map_home['missed']['x'], shot_map_home['missed']['y'], color='green', marker='o', label='Missed Shot', alpha=0.5)

    fig.suptitle(home_team + ' Shot Map')
    placeholder_shot_map.pyplot(fig)

    time.sleep(2) # update data every two
