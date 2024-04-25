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

    # Shot efficiency metric printed to terminal
    efficiency = shot_efficiency(home_players, away_players)
    print("Home Team Shooting Efficiency:", efficiency["home"], "%")
    print("Away Team Shooting Efficiency:", efficiency["away"], "%")

    return {
        'home': home_players,
        'away': away_players
    }

# Shot Efficiency Metric
def shot_efficiency(home_players, away_players):
    def get_team_efficiency(players):
        total_field_goals_made = 0
        total_field_goal_attempts = 0
        total_free_throws_made = 0
        total_free_throw_attempts = 0

        for player_stats in players.values():
            total_field_goals_made += player_stats['fieldGoalsMade']
            total_field_goal_attempts += player_stats['fieldGoalAttempts']
            total_free_throws_made += player_stats['freeThrowsMade']
            total_free_throw_attempts += player_stats['freeThrowAttempts']

        total_shots_made = total_field_goals_made + total_free_throws_made
        total_shots_attempted = total_field_goal_attempts + total_free_throw_attempts

        if total_shots_attempted > 0:
            shooting_efficiency = (total_shots_made / total_shots_attempted) * 100
        else:
            shooting_efficiency = 0

        return shooting_efficiency

    home_shooting_efficiency = get_team_efficiency(home_players)
    away_shooting_efficiency = get_team_efficiency(away_players)

    return {
        "home": home_shooting_efficiency,
        "away": away_shooting_efficiency
    }

# Controversial fun fact metric