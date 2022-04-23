import asyncio
from understat import Understat
import aiohttp
import pandas as pd
import ssl
import certifi
from sqlalchemy import create_engine

# List of teams in the Prem, List of players for club in Prem, list of all shot of a player on prem for 2021.
pd.set_option('display.max_columns', 500)
shot_list = []
shot_list2 = []
season = 2021

engine = create_engine('postgresql://postgres:jedi1999@localhost:5432/data')


async def main():
    epl = []
    test = []
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)
    async with aiohttp.ClientSession(connector=conn) as session:
        understat = Understat(session)

        # Get teams in league for current season
        league_teams = await understat.get_teams('epl', season)
        # Clean league team data, returns list of teams
        teams_lst = team_cleaning(league_teams)

        for j in range(len(teams_lst)):
            epl_players = await understat.get_team_players(teams_lst[j], season)
            epl += epl_players
        id_list = list_of_IDs(epl)

        for i in range(len(id_list)):
            cfc_player_Sh = await understat.get_player_shots(id_list[i], {'season': str(season)})
            test += cfc_player_Sh

        print('Stage 2')

        data = pd.DataFrame(test)
        data_prep = format_shot_data(data, teams_lst)
        # print(data_prep.info())
        data_prep.to_sql('shot_data', engine, if_exists='replace', index=False)


def format_shot_data(df, team_lst):
    # print(df)
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
    # print(df.head())
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

    # df['xG90'] = df['xG90'].astype('float64')
    # df['xG90'] = df['xG90'].round(2)
    # print(df.head())
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
    # players.to_csv('/Users/brendanbaker/PycharmProjects/flaskFPL/radar_data_2021-22.csv', index=False)
    players.to_sql('radar_data', engine, if_exists='replace', index=False)
    id_list = players['id']
    # print(id_list)
    return id_list


loop = asyncio.get_event_loop()
loop.run_until_complete(main())


