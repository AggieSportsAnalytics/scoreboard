from api import live_matches_data
from api import player_statistics_data


def parse_live_match(event_number):
    print("parsing match")
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
    print("parsing stats")
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
    max_fouls_home = max(home_stats, key=lambda x: home_stats[x]['Personal Fouls'])
    max_fouls_away = max(away_stats, key=lambda x: away_stats[x]['Personal Fouls'])
    return max_fouls_home, max_fouls_away