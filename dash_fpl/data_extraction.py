import requests

import pandas as pd

base_url = 'https://fantasy.premierleague.com/api/'
pd.set_option('display.max_columns', 500)


def getPlayer():
    base_url = 'https://fantasy.premierleague.com/api/'
    r = requests.get(base_url + 'bootstrap-static/').json()
    players = pd.json_normalize(r['elements'])
    return players


def get_gameweek_history(player_id):
    '''get all gameweek info for a given player_id'''

    # https://fantasy.premierleague.com/api/element-summary/{PID}/
    r = requests.get(
        base_url + 'element-summary/' + str(player_id) + '/'
    ).json()

    # extract 'history' data from response into dataframe
    df = pd.json_normalize(r['history'])
    df = df[[
        'round',
        'total_points',
        'minutes',
        'goals_scored',
        'assists',
        'clean_sheets',
        'saves',
        'bonus',
        'value',
        'element'
    ]]
    return df
