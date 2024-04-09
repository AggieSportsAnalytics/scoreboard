import http.client
import json

conn = http.client.HTTPSConnection("basketapi1.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "5d6150ae55msh12e07a4c465c2f1p11a559jsn49d4aefb0c59",
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

