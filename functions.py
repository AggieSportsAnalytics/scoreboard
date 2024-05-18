from api import live_matches_data
from api import player_statistics_data
from api import shot_map_data
from api import match_odds_data
from fractions import Fraction
from openai import OpenAI
from dotenv import load_dotenv
import os
import logging

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
global homeTeamName
global awayTeamName


def parse_live_match(event_number):
    print("parsing match")
    unparsed_data = live_matches_data()
    match = unparsed_data['events'][event_number]
    filtered_data = {
        'id': unparsed_data['events'][event_number]['id'],
        'home_team_id': match['homeTeam']['id'],
        'away_team_id': match['awayTeam']['id'],
        'home': match['homeTeam']['name'],
        'away': match['awayTeam']['name'],
        (match['homeTeam']['name']): {
            'Score': match['homeScore']['current']
        },
        (match['awayTeam']['name']): {
            'Score': match['awayScore']['current']
        }
    }
    homeTeamName = filtered_data['home']
    awayTeamName = filtered_data['away']
    return filtered_data


def parsed_player_statistics(match_id):
    print("parsing stats")
    unparsed_data = player_statistics_data(match_id)
    home = unparsed_data['home']['players']
    away = unparsed_data['away']['players']

    home_players = {}
    away_players = {}

    for player in home:
        home_players[player['player']['name']] = player['statistics']

    for player in away:
        away_players[player['player']['name']] = player['statistics']

    return {
        'home': home_players,
        'away': away_players
    }


# Manish's section

# helper function to fetch data
def get_player_stats(match_id):
    # Fetch player statistics for the given match
    match_data = player_statistics_data(match_id)
    if 'home' not in match_data or 'away' not in match_data:
        return "No data available for this match."

    # Initialize a dictionary to store the points and assists
    player_stats = {'home': {}, 'away': {}}

    # Process home team players
    for player in match_data['home']['players']:
        name = player['player']['name']
        stats = player['statistics']
        points = stats.get('points', 0)
        assists = stats.get('assists', 0)
        rebounds = stats.get('rebounds', 0)
        turnovers = stats.get('turnovers', 0)
        blocks = stats.get('blocks', 0)
        steals = stats.get('steals', 0)
        personal_fouls = stats.get('personalFouls', 0)
        player_stats['home'][name] = {'points': points,
                                      'assists': assists,
                                      'rebounds': rebounds,
                                      'turnovers': turnovers,
                                      'blocks': blocks,
                                      'steals': steals,
                                      'Personal Fouls': personal_fouls}

    # Process away team players
    for player in match_data['away']['players']:
        name = player['player']['name']
        stats = player['statistics']
        points = stats.get('points', 0)
        assists = stats.get('assists', 0)
        rebounds = stats.get('rebounds', 0)
        turnovers = stats.get('turnovers', 0)
        blocks = stats.get('blocks', 0)
        steals = stats.get('steals', 0)
        personal_fouls = stats.get('personalFouls', 0)
        player_stats['away'][name] = {'points': points,
                                      'assists': assists,
                                      'rebounds': rebounds,
                                      'turnovers': turnovers,
                                      'blocks': blocks,
                                      'steals': steals,
                                      'Personal Fouls': personal_fouls}

    return player_stats

# weighted sum function


def sum_player_stats(player_stats):
    summed_stats = {}
    for player, stats in player_stats.items():
        score = (2.5 * stats.get('points', 0) +
                 2 * stats.get('assists', 0) +
                 1.5 * stats.get('rebounds', 0) -
                 2 * stats.get('turnovers', 0) +
                 1.5 * stats.get('blocks', 0) +
                 2 * stats.get('steals', 0) -
                 2 * stats.get('Personal Fouls', 0))  # Sum all values in the stats dictionary
        summed_stats[player] = score
    return summed_stats

# hot hands


def hot_hands(match_id):
    player_stats = get_player_stats(match_id)
    home_stats = sum_player_stats(player_stats['home'])
    away_stats = sum_player_stats(player_stats['away'])
    hot_hands_home = max(home_stats, key=home_stats.get)
    hot_hands_away = max(away_stats, key=away_stats.get)
    return hot_hands_home, hot_hands_away

# bomba bum


def bum(match_id):
    player_stats = get_player_stats(match_id)
    home_stats = sum_player_stats(player_stats['home'])
    away_stats = sum_player_stats(player_stats['away'])
    bum_home = min(home_stats, key=home_stats.get)
    bum_away = min(away_stats, key=away_stats.get)
    return bum_home, bum_away

# draymond


def draymond(match_id):
    player_stats = get_player_stats(match_id)
    home_stats = player_stats['home']
    away_stats = player_stats['away']
    max_fouls_home = max(
        home_stats, key=lambda x: home_stats[x]['Personal Fouls'])
    max_fouls_away = max(
        away_stats, key=lambda x: away_stats[x]['Personal Fouls'])
    return max_fouls_home, max_fouls_away

# Shot Efficiency Metric


def shot_efficiency(match_id):
    unparsed_data = player_statistics_data(match_id)
    home_players = unparsed_data['home']['players']
    away_players = unparsed_data['away']['players']

    def get_team_efficiency(players):
        total_field_goals_made = sum(
            p['statistics']['fieldGoalsMade'] for p in players)
        total_field_goal_attempts = sum(
            p['statistics']['fieldGoalAttempts'] for p in players)
        total_free_throws_made = sum(
            p['statistics']['freeThrowsMade'] for p in players)
        total_free_throw_attempts = sum(
            p['statistics']['freeThrowAttempts'] for p in players)

        total_shots_made = total_field_goals_made + total_free_throws_made
        total_shots_attempted = total_field_goal_attempts + total_free_throw_attempts

        shooting_efficiency = (
            total_shots_made / total_shots_attempted) * 100 if total_shots_attempted > 0 else 0
        return shooting_efficiency

    home_shooting_efficiency = get_team_efficiency(home_players)
    away_shooting_efficiency = get_team_efficiency(away_players)

    return home_shooting_efficiency, away_shooting_efficiency

# Controversial fun fact metric with a very cool, basketball-tuned AI agent
# Only needs to be called once per game, otherwise it will be expensive


def controversial_fact(match_id):
    match_data = live_matches_data()
    match = next(
        event for event in match_data['events'] if event['id'] == match_id)
    home_team = match['homeTeam']['name']
    away_team = match['awayTeam']['name']

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who knows a lot about basketball."},
            {"role": "user", "content": f"Give me a controversial fun fact about either the {home_team} or {away_team}. Make it around 50 words long, edgy and funny, and from recent events."},
        ]
    )

    return response.choices[0].message.content


# Shot Map
def shot_map(match_id, team_id):
    try:
        unparsed_data = shot_map_data(match_id, team_id)
    except ValueError as e:
        logging.error(f"Failed to get shot map data: {e}")
        return {
            'made': {'x': [], 'y': []},
            'missed': {'x': [], 'y': []}
        }

    x_made = []
    y_made = []
    x_missed = []
    y_missed = []
    for x in unparsed_data.get('shotmap', []):
        if x.get('made') == True:
            x_made.append(x.get('x'))
            y_made.append(x.get('y'))
        else:
            x_missed.append(x.get('x'))
            y_missed.append(x.get('y'))

    return {
        'made': {'x': x_made, 'y': y_made},
        'missed': {'x': x_missed, 'y': y_missed}
    }


def match_odds(match_id):
    unparsed_data = match_odds_data(match_id)
    home_team_win_percentage = 1 / \
        (float(Fraction(unparsed_data['markets'][0]
         ['choices'][0]['fractionalValue'])) + 1)
    away_team_win_percentage = 1 / \
        (float(Fraction(unparsed_data['markets'][0]
         ['choices'][1]['fractionalValue'])) + 1)
    # odds themselves are a bit skewed to favor the house, meaning the win percentages dont add up to 100%
    gap = 1 - (home_team_win_percentage + away_team_win_percentage)
    home_team_win_percentage += gap/2
    away_team_win_percentage += gap/2
    # print("Home Team Win Percentage:", home_team_win_percentage*100, "%")
    # print("Away Team Win Percentage:", away_team_win_percentage*100, "%")
    # now they should add up to 100%
    return home_team_win_percentage*100, away_team_win_percentage*100
