"""
import asyncio
from understat import Understat
import aiohttp
from mplsoccer.pitch import VerticalPitch, Pitch
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
# List of teams in the Prem, List of players for club in Prem, list of all shot of a player on prem for 2021.
pd.set_option('display.max_columns', 500)
shot_list = []
shot_list2 = []
epl = []
import ssl
import certifi
season = 2021

# conn = sqlite3.connect('shots2021.db')
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:jedi1999@localhost:5432/data')


async def main(shot_list, epl):
    test = []
    rd_data = []
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)
    async with aiohttp.ClientSession(connector=conn) as session:
        understat = Understat(session)

        # Get teams in league for current season
        league_teams = await understat.get_teams('epl', season, ssl=False)
        # Clean league team data, returns list of teams
        teams_lst = team_cleaning(league_teams)
        #print(teams_lst)
        # player_shots = await understat.get_player_shots(619)

        for j in range(len(teams_lst)):
            epl_players = await understat.get_team_players(teams_lst[j], season)
            epl += epl_players
        #print('Stage 1')
        #print(epl)
        id_list = list_of_IDs(epl)

        for i in range(len(id_list)):
            cfc_player_Sh = await understat.get_player_shots(id_list[i], {'season': str(season)})
            test += cfc_player_Sh

            # print(cfc_player_Sh)
        #print('Stage 2')
        # minutes = total minutes / 90
        # xG90 = xG / minutes

        # player_xg = await understat.get_player_stats(619)

        # shot_list += player_shots
        data = pd.DataFrame(test)
        df_rd_data = pd.DataFrame(rd_data)
        data_prep = format_shot_data(data, teams_lst)
        #print(data_prep.info())
        # data_prep.to_sql(name='test', con=conn, if_exists='replace', index=False)
        # test = format_data(test)
        # df = pd.DataFrame(data)
        # print(df)
        # print('Done')
        # data_prep.to_csv('/Users/brendanbaker/PycharmProjects/flaskFPL/shot_data_2021-22.csv', index=False)

        data_prep.to_sql('shot_data', engine, if_exists='replace', index=False)


def format_shot_data(df, team_lst):
    df['X'] = df['X'].astype('float64')
    df['Y'] = df['Y'].astype('float64')
    df['minute'] = df['minute'].astype('int64')
    df['result'] = df['result'].astype(str)
    df['xG'] = df['xG'].astype('float64')
    df['player'] = df['player'].astype('unicode')
    df['h_goals'] = df['h_goals'].astype('int64')
    df['a_goals'] = df['a_goals'].astype('int64')
    df['date'] = pd.to_datetime(df['date'])
    df['player_id'] = df['player_id'].astype('int64')
    # place ~ for inverted value between df and df
    df = df[df['a_team'].isin(team_lst)]
    df = df[df['h_team'].isin(team_lst)]
    df['X'] = (df['X']) * 98
    df['Y'] = (df['Y']) * 120

    return df


def format_player_data(df):
    df['player_name'] = df['player_name'].astype('unicode')
    df['id'] = df['id'].astype('int64')
    df['games'] = df['games'].astype('int64')
    df['time'] = df['time'].astype('int64')
    df['goals'] = df['goals'].astype('int64')
    df['xG'] = df['xG'].astype('float64')
    df['assist'] = df['assist'].astype('int64')
    df['xA'] = df['xA'].astype('float64')
    df['shots'] = df['shots'].astype('int64')
    df['key_passes'] = df['key_passes'].astype('int64')
    df['yellow_cards'] = df['yellow_cards'].astype('int64')
    df['red_cards'] = df['red_cards'].astype('int64')
    df['npg'] = df['npg'].astype('int64')
    df['npxG'] = df['npxG'].astype('float64')
    df['xGChain'] = df['xGChain'].astype('float64')
    df['xGBuildup'] = df['xGBuildup'].astype('float64')

    return df


"""
9740
10293
10327
"""


def team_cleaning(data):
    df_teams = pd.DataFrame(data)
    df_teams = df_teams['title']
    teams_lst = df_teams.values.tolist()
    teams_lst.sort()
    return teams_lst


def list_of_IDs(players):
    players = pd.DataFrame(players)
    #players.to_csv('/Users/brendanbaker/PycharmProjects/flaskFPL/radar_data_2021-22.csv', index=False)
    players.to_sql('radar_data', engine, if_exists='replace', index=False)
    id_list = players['id']
    #print(id_list)
    return id_list


loop = asyncio.get_event_loop()
loop.run_until_complete(main(shot_list, epl))

shots = pd.DataFrame(shot_list)
"""
import asyncio
from understat import Understat
import aiohttp
from mplsoccer.pitch import VerticalPitch, Pitch
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import psycopg2
# List of teams in the Prem, List of players for club in Prem, list of all shot of a player on prem for 2021.
pd.set_option('display.max_columns', 500)
shot_list = []
shot_list2 = []
epl = []

season = 2021
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:jedi1999@localhost:5432/data')

# conn = sqlite3.connect('shots2021.db')
#import websockets
import ssl
import certifi


async def main(shot_list, epl):
    test = []
    rd_data = []
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)
    async with aiohttp.ClientSession(connector=conn) as session:
        understat = Understat(session)

        # Get teams in league for current season
        league_teams = await understat.get_teams('epl', season)
        # Clean league team data, returns list of teams
        teams_lst = team_cleaning(league_teams)
        #print(teams_lst)
        # player_shots = await understat.get_player_shots(619)

        for j in range(len(teams_lst)):
            epl_players = await understat.get_team_players(teams_lst[j], season)
            epl += epl_players
        #print('Stage 1')
        #print(epl)
        id_list = list_of_IDs(epl)

        for i in range(len(id_list)):
            cfc_player_Sh = await understat.get_player_shots(id_list[i], {'season': str(season)})
            test += cfc_player_Sh

            # print(cfc_player_Sh)
        print('Stage 2')
        # minutes = total minutes / 90
        # xG90 = xG / minutes

        # player_xg = await understat.get_player_stats(619)

        # shot_list += player_shots
        data = pd.DataFrame(test)
        df_rd_data = pd.DataFrame(rd_data)
        data_prep = format_shot_data(data, teams_lst)
        #print(data_prep.info())
        # data_prep.to_sql(name='test', con=conn, if_exists='replace', index=False)
        # test = format_data(test)
        # df = pd.DataFrame(data)
        # print(df)
        # print('Done')
        #data_prep.to_csv('/Users/brendanbaker/PycharmProjects/flaskFPL/shot_data_2021-22.csv', index=False)
        data_prep.to_sql('shot_data', engine, if_exists='replace', index=False)

def format_shot_data(df, team_lst):
    #print(df)
    df['X'] = df['X'].astype('float64')
    df['Y'] = df['Y'].astype('float64')
    df['minute'] = df['minute'].astype('int64')
    df['result'] = df['result'].astype(str)
    df['xG'] = df['xG'].astype('float64').round(2)
    df['player'] = df['player'].astype('unicode')
    df['h_goals'] = df['h_goals'].astype('int64')
    df['a_goals'] = df['a_goals'].astype('int64')
    df['date'] = pd.to_datetime(df['date'])
    df['player_id'] = df['player_id'].astype('int64')
    # place ~ for inverted value between df and df
    df = df[df['a_team'].isin(team_lst)]
    df = df[df['h_team'].isin(team_lst)]
    df['X'] = (df['X']) * 100
    df['Y'] = (df['Y']) * 100
    df.fillna("N/A", inplace=True)
    return df


def format_player_data(df):
    #print(df.head())
    df['player_name'] = df['player_name'].astype('unicode')
    df['id'] = df['id'].astype('int64')
    df['games'] = df['games'].astype('int64')
    df['time'] = df['time'].astype('int64')
    df['goals'] = df['goals'].astype('int64')
    df['xG'] = df['xG'].astype('float64').round(2)
    df['assists'] = df['assists'].astype('int64')
    df['xA'] = df['xA'].astype('float64').round(2)
    df['shots'] = df['shots'].astype('int64')
    df['key_passes'] = df['key_passes'].astype('int64')
    df['yellow_cards'] = df['yellow_cards'].astype('int64')
    df['red_cards'] = df['red_cards'].astype('int64')
    df['npg'] = df['npg'].astype('int64')
    df['npxG'] = df['npxG'].astype('float64').round(2)
    df['xGChain'] = df['xGChain'].astype('float64').round(2)
    df['xGBuildup'] = df['xGBuildup'].astype('float64').round(2)

    # Radar Plot Data
    df['xG90'] = (df['xG'] / (df['time'] / 90)).round(2)
    df['xA90'] = (df['xA'] / (df['time'] / 90)).round(2)
    df['xGBuildup90'] = (df['xGBuildup'] / (df['time'] / 90)).round(2)
    df['xGChain90'] = (df['xGChain'] / (df['time'] / 90)).round(2)
    df['G90'] = (df['goals'] / (df['time'] / 90)).round(2)
    df['A90'] = (df['assists'] / (df['time'] / 90)).round(2)



    #df['xG90'] = df['xG90'].astype('float64')
    #df['xG90'] = df['xG90'].round(2)
    #print(df.head())
    return df


"""
9740
10293
10327
"""


def team_cleaning(data):
    df_teams = pd.DataFrame(data)
    df_teams = df_teams['title']
    teams_lst = df_teams.values.tolist()
    teams_lst.sort()
    return teams_lst


def list_of_IDs(players):
    players = pd.DataFrame(players)
    players = format_player_data(players)
    #players.to_csv('/Users/brendanbaker/PycharmProjects/flaskFPL/radar_data_2021-22.csv', index=False)
    players.to_sql('radar_data', engine, if_exists='replace', index=False)
    id_list = players['id']
    #print(id_list)
    return id_list


loop = asyncio.get_event_loop()
loop.run_until_complete(main(shot_list, epl))

shots = pd.DataFrame(shot_list)

