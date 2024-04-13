from api import live_matches_data

def parse_live_matches():
    unparsed_data = live_matches_data()
    first_game = unparsed_data['events'][0]
    filtered_data = { (first_game['homeTeam']['name']): { 'Score': first_game['homeScore']['current']},
                      (first_game['awayTeam']['name']): {  'Score': first_game['awayScore']['current']} }
    return filtered_data