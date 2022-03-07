import requests, json
from pprint import pprint
import pandas as pd

# base url for all FPL API endpoints

base_url = 'https://fantasy.premierleague.com/api/'
# get data from bootstrap-static endpoint
pd.set_option('display.max_columns', 500)


# show the top level fields
# pprint(r, indent=2, depth=1, compact=True)

# get player data from 'elements' field
# show data for first player
# players = pd.json_normalize(r['elements'])

def getPlayer():
    base_url = 'https://fantasy.premierleague.com/api/'
    r = requests.get(base_url + 'bootstrap-static/').json()
    players = pd.json_normalize(r['elements'])
    return players


def gameweekHistory(element_id):
    url = f'https://fantasy.premierleague.com/api/element-summary/{element_id}/'
    r = requests.get(url)
    json = r.json()
    print(json.keys())
    json_history_df = pd.DataFrame(json['history'])
    print(json_history_df.head())


# gameweekHistory(200)


def get_gameweek_history(player_id):
    '''get all gameweek info for a given player_id'''

    # send GET request to
    # https://fantasy.premierleague.com/api/element-summary/{PID}/
    r = requests.get(
        base_url + 'element-summary/' + str(player_id) + '/'
    ).json()

    # extract 'history' data from response into dataframe
    # print(r)
    df = pd.json_normalize(r['history'])
    # print(df.head())
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


"""def apitest():
    link = "https://understat.com/player/5232"
    r = requests.get(link).json()
    print(r)


apitest()"""
print(get_gameweek_history(200))
