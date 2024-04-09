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

conn.request("GET", "/api/basketball/matches/live", headers=headers)

res = conn.getresponse()
data = json.loads(res.read().decode())

if len(data['events']) != 0:
    first_game = data['events'][0]


    home_team = first_game['homeTeam']['name']
    home_score = first_game['homeScore']['current']
    away_team = first_game['awayTeam']['name']
    away_score = first_game['awayScore']['current']

    print("Home Team:", home_team)
    print("Home Score:", home_score)
    print("Away Team:", away_team)
    print("Away Score:", away_score)
else:
    print("No Games Currently")
print(data)

