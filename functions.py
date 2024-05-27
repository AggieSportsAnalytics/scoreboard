from api import live_matches_data, player_statistics_data, shot_map_data, match_odds_data
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
    try:
        unparsed_data = live_matches_data()
        match = unparsed_data['events'][event_number]
        filtered_data = {
            'id': match.get('id'),
            'home_team_id': match['homeTeam'].get('id'),
            'away_team_id': match['awayTeam'].get('id'),
            'home': match['homeTeam'].get('name'),
            'away': match['awayTeam'].get('name'),
            (match['homeTeam'].get('name', 'Home')): {
                'Score': match['homeScore'].get('current')
            },
            (match['awayTeam'].get('name', 'Away')): {
                'Score': match['awayScore'].get('current')
            }
        }
        homeTeamName = filtered_data['home']
        awayTeamName = filtered_data['away']
        return filtered_data
    except KeyError as e:
        logging.error(f"Key error while parsing match data: {e}")
        return {}


def parsed_player_statistics(match_id):
    print("parsing stats")
    try:
        unparsed_data = player_statistics_data(match_id)
        home = unparsed_data['home'].get('players', [])
        away = unparsed_data['away'].get('players', [])

        home_players = {}
        away_players = {}

        for player in home:
            home_players[player['player'].get(
                'name')] = player.get('statistics', {})

        for player in away:
            away_players[player['player'].get(
                'name')] = player.get('statistics', {})

        return {
            'home': home_players,
            'away': away_players
        }
    except KeyError as e:
        logging.error(f"Key error while parsing player statistics: {e}")
        return {'home': {}, 'away': {}}


# Manish's section

# helper function to fetch data
def get_player_stats(match_id):
    try:
        match_data = player_statistics_data(match_id)
        if 'home' not in match_data or 'away' not in match_data:
            return "No data available for this match."

        player_stats = {'home': {}, 'away': {}}

        for player in match_data['home'].get('players', []):
            name = player['player'].get('name')
            stats = player.get('statistics', {})
            player_stats['home'][name] = {
                'points': stats.get('points', 0),
                'assists': stats.get('assists', 0),
                'rebounds': stats.get('rebounds', 0),
                'turnovers': stats.get('turnovers', 0),
                'blocks': stats.get('blocks', 0),
                'steals': stats.get('steals', 0),
                'Personal Fouls': stats.get('personalFouls', 0)
            }

        for player in match_data['away'].get('players', []):
            name = player['player'].get('name')
            stats = player.get('statistics', {})
            player_stats['away'][name] = {
                'points': stats.get('points', 0),
                'assists': stats.get('assists', 0),
                'rebounds': stats.get('rebounds', 0),
                'turnovers': stats.get('turnovers', 0),
                'blocks': stats.get('blocks', 0),
                'steals': stats.get('steals', 0),
                'Personal Fouls': stats.get('personalFouls', 0)
            }

        return player_stats
    except KeyError as e:
        logging.error(f"Key error while fetching player stats: {e}")
        return {'home': {}, 'away': {}}

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
                 2 * stats.get('Personal Fouls', 0))
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
        home_stats, key=lambda x: home_stats[x].get('Personal Fouls', 0))
    max_fouls_away = max(
        away_stats, key=lambda x: away_stats[x].get('Personal Fouls', 0))
    return max_fouls_home, max_fouls_away

# Shot Efficiency Metric


def shot_efficiency(match_id):
    try:
        unparsed_data = player_statistics_data(match_id)
        home_players = unparsed_data['home'].get('players', [])
        away_players = unparsed_data['away'].get('players', [])

        def get_team_efficiency(players):
            total_field_goals_made = sum(
                p['statistics'].get('fieldGoalsMade', 0) for p in players)
            total_field_goal_attempts = sum(
                p['statistics'].get('fieldGoalAttempts', 0) for p in players)
            total_free_throws_made = sum(
                p['statistics'].get('freeThrowsMade', 0) for p in players)
            total_free_throw_attempts = sum(
                p['statistics'].get('freeThrowAttempts', 0) for p in players)

            total_shots_made = total_field_goals_made + total_free_throws_made
            total_shots_attempted = total_field_goal_attempts + total_free_throw_attempts

            shooting_efficiency = (
                total_shots_made / total_shots_attempted) * 100 if total_shots_attempted > 0 else 0
            return shooting_efficiency

        home_shooting_efficiency = get_team_efficiency(home_players)
        away_shooting_efficiency = get_team_efficiency(away_players)

        return home_shooting_efficiency, away_shooting_efficiency
    except KeyError as e:
        logging.error(f"Key error while calculating shot efficiency: {e}")
        return 0, 0

# Controversial fun fact metric with a very cool, basketball-tuned AI agent


def controversial_fact(match_id):
    try:
        match_data = live_matches_data()
        match = next(
            event for event in match_data['events'] if event['id'] == match_id)
        home_team = match['homeTeam'].get('name', 'Home Team')
        away_team = match['awayTeam'].get('name', 'Away Team')

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who knows a lot about basketball."},
                {"role": "user", "content": f"Give me a controversial fun fact about either the {home_team} or {away_team}. Make it 20 words long, edgy and funny, and from recent events."},
            ]
        )

        return response.choices[0].message.content
    except KeyError as e:
        logging.error(f"Key error while fetching controversial fact: {e}")
        return "Unable to fetch controversial fact."


# Shot Map
def shot_map(match_id, team_id):
    try:
        unparsed_data = shot_map_data(match_id, team_id)
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
    except (KeyError, ValueError) as e:
        logging.error(f"Failed to get shot map data: {e}")
        return {
            'made': {'x': [], 'y': []},
            'missed': {'x': [], 'y': []}
        }


def match_odds(match_id):
    try:
        unparsed_data = match_odds_data(match_id)
        if not unparsed_data:
            return 0, 0

        market = unparsed_data.get('markets', [{}])[0]
        choices = market.get('choices', [{}])

        if len(choices) < 2:
            logging.error(
                f"Insufficient choices data for match ID: {match_id}")
            return 0, 0

        home_team_win_percentage = 1 / \
            (float(Fraction(choices[0].get('fractionalValue', '1/1'))) + 1)
        away_team_win_percentage = 1 / \
            (float(Fraction(choices[1].get('fractionalValue', '1/1'))) + 1)

        gap = 1 - (home_team_win_percentage + away_team_win_percentage)
        home_team_win_percentage += gap / 2
        away_team_win_percentage += gap / 2

        return home_team_win_percentage * 100, away_team_win_percentage * 100
    except KeyError as e:
        logging.error(f"Key error while fetching match odds: {e}")
        return 0, 0
    except Exception as e:
        logging.error(f"Unexpected error while fetching match odds: {e}")
        return 0, 0
