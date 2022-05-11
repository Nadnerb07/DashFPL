import requests
import json
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)


# https://fantasy.premierleague.com/api/dream-team/8/ ----> highest scoring

# TODO
def multiply_by_2(dataframe):
    captain = dataframe.loc[dataframe['multiplier'] == 2]
    return captain


# TODO
def multiply_by_3(dataframe):
    captain = dataframe.loc[dataframe['multiplier'] == 3]
    # print(type(captain), captain)
    return captain


# TESTED
def dataframe_col_to_list(dataframe):
    captain_names = dataframe['element'].tolist()
    return captain_names


# TESTED
def total_points_multiplier(dataframe):
    return dataframe.total_points * dataframe.multiplier


# TESTED
def points_multiplier(dataframe):
    return dataframe.points * 2


# TESTED
def captain_points_difference(dataframe):
    return dataframe['Points'] - dataframe['Optimal Points']


# TESTED
def get_GW_captain_picks(manager_id, gameweek, df):
    while 1:
        r = requests.get(f"https://fantasy.premierleague.com/api/entry/{manager_id}/event/{gameweek}/picks/")
        if r.status_code == 404:
            gameweek = 1  # reset gameweek to 1
            return df, gameweek
        else:
            data = (json.loads(r.text))
            dataset = pd.DataFrame.from_dict(data['picks'])
            if dataset['multiplier'].eq(2).any():
                cpt = multiply_by_2(dataset)
            elif dataset['multiplier'].eq(3).any():
                cpt = multiply_by_3(dataset)
            df = pd.concat([df, cpt])
        gameweek += 1


# TESTED
def match_captain_pick_to_score(captains, captain_points, gameweek):
    for i in captains:

        r5 = requests.get(f"https://fantasy.premierleague.com/api/element-summary/{i}/")
        test = (json.loads(r5.text))
        try:
            elements_df = pd.DataFrame(test['history'])
        except KeyError:
            return captain_points, gameweek
        elements_df = elements_df[['total_points', 'round']]
        aggregation_functions = {'total_points': 'sum', 'round': 'sum'}
        df_new = elements_df.groupby(elements_df['round']).aggregate(aggregation_functions)

        captain_points.append(df_new.at[gameweek, 'total_points'])
        gameweek += 1
        if gameweek == len(captains) + 1:
            gameweek = 1
            return captain_points, gameweek


# TODO
def get_GW_optimal_captains(topPlayerDf, gameweek):
    while 1:
        top_player_request = requests.get(f"https://fantasy.premierleague.com/api/dream-team/{gameweek}/")
        if top_player_request.status_code == 404:
            # print(gameweek, "404")
            return topPlayerDf
        else:
            tp_data = (json.loads(top_player_request.text))
            temp_dataset = pd.DataFrame(tp_data['top_player'], index=[gameweek])
            topPlayerDf = pd.concat([topPlayerDf, temp_dataset])
            gameweek += 1


# TODO
def getGenericPlayerData():
    requestGenericPlayerData = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
    genericPLayerData = requestGenericPlayerData.json()
    playerElementsTemp = pd.DataFrame(genericPLayerData['elements'])
    playerElements = playerElementsTemp[['id', 'web_name']]
    return playerElements


# TODO
# List to series to col
def captain_points_to_col(captain_points):
    return pd.Series(captain_points)


# TODO
def dataframe_col_rename(dataframe):
    dataframe = dataframe.rename(
        columns={'element': 'Captain', 'total_points': 'Points', 'id': 'Optimal Pick', 'points': 'Optimal Points'})
    return dataframe


# TODO
# Test input a variable, expect a dataframe
def optimal_captain(manager_id):
    captain_points = []
    playerElements = getGenericPlayerData()
    gameweek = 1
    df = pd.DataFrame()
    optimalCaptainDf = pd.DataFrame()
    df, gameweek = get_GW_captain_picks(manager_id, gameweek, df)
    df.index = np.arange(0, len(df))

    # Check data format here
    captain_list = dataframe_col_to_list(df)

    captain_points, gameweek = match_captain_pick_to_score(captain_list, captain_points, gameweek)
    df['total_points'] = captain_points_to_col(captain_points)
    df.index = np.arange(1, len(df) + 1)

    optimalCaptainDf = get_GW_optimal_captains(optimalCaptainDf, gameweek)

    optimalCaptainDf.index.name = 'Gameweek'
    df = df.join(optimalCaptainDf)
    # Test Here
    df['total_points'] = total_points_multiplier(df)
    # Test Here
    df['points'] = points_multiplier(df)
    df = df.drop(columns=['position', 'is_captain', 'is_vice_captain', 'multiplier'])
    df['id'] = df['id'].map(playerElements.set_index('id')['web_name'])
    df['element'] = df['element'].map(playerElements.set_index('id')['web_name'])
    df = dataframe_col_rename(df)
    df['Difference'] = captain_points_difference(df)
    df.index.name = 'Gameweek'

    return df

# optimal_captain(8931)
# optimal_captain(6518279)
