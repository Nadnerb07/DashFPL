import requests
import json
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

# https://fantasy.premierleague.com/api/dream-team/8/ ----> highest scoring

gameweek = 1
dataset = pd.DataFrame
# final = pd.DataFrame
eq = []
data = []
df = pd.DataFrame()
theList = []
#cpt = pd.DataFrame()
while 1:
    r = requests.get(f"https://fantasy.premierleague.com/api/entry/6518279/event/{gameweek}/picks/")
    if r.status_code == 404:
        #print(gameweek, "404")
        break
    else:
        data = (json.loads(r.text))
        # print(data)
        dataset = pd.DataFrame.from_dict(data['picks'])
        cpt = dataset.loc[dataset['multiplier'] == 2]
        #print(type(cpt))
        #df = df.append(cpt, ignore_index=False)
        df = pd.concat([df, cpt])
        gameweek += 1
#new_hr_2 = hr_df.join(cand_df)
df.index = np.arange(0, len(df))
df.index.name = 'Gameweek'
#print(df)

col_one_list = df['element'].tolist()
e = []
gw = 0
for i in col_one_list:

    #print(type(i), i, gw)
    r5 = requests.get(f"https://fantasy.premierleague.com/api/element-summary/{i}/")
    #json = r5.json()
    test = (json.loads(r5.text))
    # print(json.keys())
    elements_df = pd.DataFrame(test['history'])
    # print(elements_df.head())
    e.append(elements_df.at[gw, 'total_points'])
    gw += 1
    if gw == len(col_one_list) - 1:
        break

df['total_points'] = pd.Series(e)
df.index = np.arange(1, len(df)+1)
#print(df)


gameweek = 1

# top_player = requests.get(f"https://fantasy.premierleague.com/api/dream-team/{gameweek}/")
# json = top_player.json()
# print(json)
# tp_list = []

temp_dataset = pd.DataFrame
tpdf = pd.DataFrame()

while 1:
    top_player_request = requests.get(f"https://fantasy.premierleague.com/api/dream-team/{gameweek}/")
    if top_player_request.status_code == 404:
        #print(gameweek, "404")
        break
    else:
        tp_data = (json.loads(top_player_request.text))
        #data = (json.loads(top_player_request.text))
        # print(data)
        temp_dataset = pd.DataFrame(tp_data['top_player'], index=[gameweek])
        # cpt = dataset.loc[dataset['multiplier'] == 2]
        # print(type(cpt))
        tpdf = pd.concat([tpdf, temp_dataset])

        #print(df)
        gameweek += 1
#df.index = np.arange(0, len(df))
tpdf.index.name = 'Gameweek'
#print(tpdf)
df = df.join(tpdf)
print(df)
