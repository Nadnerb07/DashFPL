import requests
import json
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
# https://fantasy.premierleague.com/api/dream-team/8/ ----> highest scoring
a = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
at = a.json()
# print(at)
#print(at.keys())
test1 = pd.DataFrame(at['elements'])
test1 = test1[['id', 'web_name']]
#print(type(test1))
#print(test1)
#m = dict(zip(test.id, test.web_name))
#print(m)
#exit()
gameweek = 1
dataset = pd.DataFrame
# final = pd.DataFrame
eq = []
data = []
df = pd.DataFrame()
theList = []
# cpt = pd.DataFrame()
while 1:
    r = requests.get(f"https://fantasy.premierleague.com/api/entry/6518279/event/{gameweek}/picks/")
    if r.status_code == 404:
        # print(gameweek, "404")
        break
    else:
        data = (json.loads(r.text))
        # print(data)
        dataset = pd.DataFrame.from_dict(data['picks'])
        cpt = dataset.loc[dataset['multiplier'] == 2]
        # print(type(cpt))
        # df = df.append(cpt, ignore_index=False)
        df = pd.concat([df, cpt])
        gameweek += 1
# new_hr_2 = hr_df.join(cand_df)
#print(df)
df.index = np.arange(0, len(df))
df.index.name = 'Gameweek'
# print(df)

col_one_list = df['element'].tolist()
e = []
gw = 1
# -- > Gameweek captain picks, gameweek in length


# Change gw variable to 1 start was 0 before
# Here we're trying to get the total_points for each gameweek
for i in col_one_list:

    # print(type(i), i, gw)
    r5 = requests.get(f"https://fantasy.premierleague.com/api/element-summary/{i}/")
    # json = r5.json()
    test = (json.loads(r5.text))
    #print(test)
    # print(json.keys())
    elements_df = pd.DataFrame(test['history'])
    elements_df = elements_df[['total_points', 'round']]
    aggregation_functions = {'total_points': 'sum', 'round': 'sum'}
    df_new = elements_df.groupby(elements_df['round']).aggregate(aggregation_functions)
    #print(elements_df)
    #print(df_new)
    #exit()
    #TODO add function that merges the total points
    e.append(df_new.at[gw, 'total_points'])
    #print(e)
    gw += 1
    if gw == len(col_one_list):
        break
#print(gw)

#print(e)
#exit()
df['total_points'] = pd.Series(e)
df.index = np.arange(1, len(df) + 1)
# print(df)

gameweek = 1

# top_player = requests.get(f"https://fantasy.premierleague.com/api/dream-team/{gameweek}/")
# json = top_player.json()
# print(json)
# tp_list = []

temp_dataset = pd.DataFrame
tpdf = pd.DataFrame()

# Best Player each Week
while 1:
    top_player_request = requests.get(f"https://fantasy.premierleague.com/api/dream-team/{gameweek}/")
    if top_player_request.status_code == 404:
        # print(gameweek, "404")
        break
    else:
        tp_data = (json.loads(top_player_request.text))
        # data = (json.loads(top_player_request.text))
        # print(data)
        temp_dataset = pd.DataFrame(tp_data['top_player'], index=[gameweek])
        # cpt = dataset.loc[dataset['multiplier'] == 2]
        # print(type(cpt))
        tpdf = pd.concat([tpdf, temp_dataset])

        # print(df)
        gameweek += 1
# df.index = np.arange(0, len(df))
tpdf.index.name = 'Gameweek'
# print(tpdf)
df = df.join(tpdf)
#m = dict(zip(test.id, test.web_name))
# df['id'] = df['id'].map(m('id')['web_name'])
#print(type(df))
#print(type(test1))
#df['total_points'] = df['total_points'].astype('int64')
df = df.drop(columns=['position', 'is_captain', 'is_vice_captain'])
df['id'] = df['id'].map(test1.set_index('id')['web_name'])
df['element'] = df['element'].map(test1.set_index('id')['web_name'])
# if the names match or the points are the same == optimal
# difference == 0, or green tick whatever
df.index.name = 'Gameweek'
print(df)
