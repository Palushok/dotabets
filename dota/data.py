import pandas as pd


def json_to_dataframe(data):
    data_dict = {}
    idx = 0
    for match in data:
        location = match['location']
        date = match['date']
        teams = []
        teams = match['teams']
        team_0 = teams[0]['team']
        country_0 = teams[0]['county']
        team_1 = teams[1]['team']
        country_1 = teams[1]['county']
        for game in match['maps']:
            picks_0 = game['picks'][0]
            picks_1 = game['picks'][1]
            bans_0 = game['bans'][0]
            bans_1 = game['bans'][1]
            winner = game['winner']
            data_dict[idx] = {
                'location': location,
                'team_0': team_0,
                'team_1': team_1,
                'country_0': country_0,
                'country_1': country_1,
                'picks_0': picks_0,
                'bans_0': bans_0,
                'picks_1': picks_1,
                'bans_1': bans_1,
                'winner': winner
            }
            idx += 1

    df = pd.DataFrame.from_dict(data_dict, orient='index')
    return df
