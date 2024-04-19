import http.client
import json
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('RAPIDAPI_KEY')

conn = http.client.HTTPSConnection("basketapi1.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': api_key,
    'X-RapidAPI-Host': "basketapi1.p.rapidapi.com"
}


def live_matches_data():
    conn.request("GET", "/api/basketball/matches/live", headers=headers)

    res = conn.getresponse()
    data = json.loads(res.read().decode())
    return data

def player_statistics_data(match_id):
    conn.request("GET", "/api/basketball/match/" + str(match_id) + "/lineups", headers=headers)

    res = conn.getresponse()
    data = json.loads(res.read().decode())
    return data


# if len(data['events']) != 0:
#     first_game = data['events'][0]

#     home_team = first_game['homeTeam']['name']
#     home_score = first_game['homeScore']['current']
#     away_team = first_game['awayTeam']['name']
#     away_score = first_game['awayScore']['current']

#     print("Home Team:", home_team)
#     print("Home Score:", home_score)
#     print("Away Team:", away_team)
#     print("Away Score:", away_score)
# else:
#     print("No Games Currently")
# print(data)

