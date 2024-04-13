from api import live_matches_data
from api import player_statistics_data


def parse_live_match(event_number):
    unparsed_data = live_matches_data()
    match = unparsed_data['events'][event_number]
    filtered_data = { 
                        'id': unparsed_data['events'][event_number]['id'],
                        'home': match['homeTeam']['name'],
                        'away': match['awayTeam']['name'],
                        (match['homeTeam']['name']): { 
                            'Score': match['homeScore']['current']
                            },
                        (match['awayTeam']['name']): {  
                            'Score': match['awayScore']['current']
                            } 
                    }
    return filtered_data

def parsed_player_statistics(match_id):
    unparsed_data = player_statistics_data(match_id)
    home = unparsed_data['home']['players']
    away = unparsed_data['away']['players']

    home_players = { }
    away_players = { }

    for player in home:
        home_players[player['player']['name']] = player['statistics']

    for player in away:
        away_players[player['player']['name']] = player['statistics']

    return {
        'home': home_players,
        'away': away_players
    }