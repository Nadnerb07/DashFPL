import requests
import json
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)


# https://fantasy.premierleague.com/api/dream-team/8/ ----> highest scoring

def optimal_captain(manager_id):
    print(manager_id, 'inside ID')
    a = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
    at = a.json()
    test1 = pd.DataFrame(at['elements'])
    test1 = test1[['id', 'web_name']]
    # print('a', a)
    gameweek = 1
    dataset = pd.DataFrame

    data = []
    df = pd.DataFrame()

    while 1:
        r = requests.get(f"https://fantasy.premierleague.com/api/entry/{manager_id}/event/{gameweek}/picks/")
        # print(r, 'while')
        if r.status_code == 404:
            # print(r.json())
            # print(gameweek, "404")
            # print('HereLast', gameweek)
            break
        else:
            data = (json.loads(r.text))
            dataset = pd.DataFrame.from_dict(data['picks'])
            if dataset['multiplier'].eq(2).any():
                cpt = dataset.loc[dataset['multiplier'] == 2]
            elif dataset['multiplier'].eq(3).any():
                cpt = dataset.loc[dataset['multiplier'] == 3]

            df = pd.concat([df, cpt])
        gameweek += 1
    df.index = np.arange(0, len(df))
    # df.index.name = 'Gameweek'

    col_one_list = df['element'].tolist()
    print(col_one_list)
    e = []
    gw = 1
    # print('HereLO')
    # Merge the double gameweeks, i is list of user captains get score for each week
    for i in col_one_list:

        r5 = requests.get(f"https://fantasy.premierleague.com/api/element-summary/{i}/")
        test = (json.loads(r5.text))
        elements_df = pd.DataFrame(test['history'])
        elements_df = elements_df[['total_points', 'round']]
        # print(elements_df.tail())
        aggregation_functions = {'total_points': 'sum', 'round': 'sum'}
        df_new = elements_df.groupby(elements_df['round']).aggregate(aggregation_functions)
        # print(df_new.at[gw, 'total_points'])
        # print(df_new, gw)
        # print(gw, i)
        # print(df_new)
        try:
            e.append(df_new.at[gw, 'total_points'])
            # print(e)
        except KeyError:
            continue
        gw += 1
        if gw == len(col_one_list) + 1:
            break
    print(e)
    df['total_points'] = pd.Series(e)
    df.index = np.arange(1, len(df) + 1)

    gameweek = 1

    temp_dataset = pd.DataFrame
    tpdf = pd.DataFrame()

    # Best Player each Week
    print('HereLast')
    while 1:
        top_player_request = requests.get(f"https://fantasy.premierleague.com/api/dream-team/{gameweek}/")
        if top_player_request.status_code == 404:
            # print(gameweek, "404")
            break
        else:
            tp_data = (json.loads(top_player_request.text))
            temp_dataset = pd.DataFrame(tp_data['top_player'], index=[gameweek])
            tpdf = pd.concat([tpdf, temp_dataset])

            gameweek += 1

    tpdf.index.name = 'Gameweek'
    df = df.join(tpdf)
    df['total_points'] = df.total_points * df.multiplier
    df['points'] = df.points * 2
    df = df.drop(columns=['position', 'is_captain', 'is_vice_captain', 'multiplier'])
    df['id'] = df['id'].map(test1.set_index('id')['web_name'])
    df['element'] = df['element'].map(test1.set_index('id')['web_name'])
    df = df.rename(
        columns={'element': 'Captain', 'total_points': 'Points', 'id': 'Optimal Pick', 'points': 'Optimal Points'})
    df['Difference'] = df['Points'] - df['Optimal Points']
    df.index.name = 'Gameweek'

    # print(df)
    return df

# optimal_captain(8931)
# optimal_captain(6518279)
