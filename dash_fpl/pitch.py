import asyncio
from understat import Understat
import aiohttp
from mplsoccer.pitch import VerticalPitch, Pitch
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

# List of teams in the Prem, List of players for club in Prem, list of all shot of a player on prem for 2021.
pd.set_option('display.max_columns', 500)
shot_list = []
shot_list2 = []
epl = []
test = []
season = 2021
"""
conn = sqlite3.connect('shots2021.db')


async def main(shot_list, epl, test):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)

        # Get teams in league for current season
        league_teams = await understat.get_teams('epl', season)
        # Clean league team data, returns list of teams
        teams_lst = team_cleaning(league_teams)

        player_shots = await understat.get_player_shots(619)

        for j in range(len(teams_lst)):
            epl_players = await understat.get_team_players(teams_lst[j], season)
            epl += epl_players

        id_list = list_of_IDs(epl)

        for i in range(len(id_list)):
            cfc_player_Sh = await understat.get_player_shots(id_list[i], {'season': season})
            test += cfc_player_Sh


        player_xg = await understat.get_player_stats(619)
        shot_list += player_shots

        df = pd.DataFrame(test)
        df = format_data(df)

        df.to_sql(name='shots2021', con=conn, if_exists='replace', index=False)
        conn.commit()
        # df.to_csv('/Users/brendanbaker/PycharmProjects/UnderstatAPI/Testing/shot_data.csv')


def format_data(df):
    df['X'] = df['X'].astype('float64')
    df['Y'] = df['Y'].astype('float64')
    df['X'] = (df['X']) * 98
    df['Y'] = (df['Y']) * 120
    return df


def team_cleaning(data):
    df_teams = pd.DataFrame(data)
    df_teams = df_teams['title']
    teams_lst = df_teams.values.tolist()
    teams_lst.sort()
    return teams_lst


def list_of_IDs(players):
    players = pd.DataFrame(players)
    id_list = players['id']
    return id_list


#loop = asyncio.get_event_loop()
loop.run_until_complete(main(shot_list, epl, test))

shots = pd.DataFrame(shot_list)

shots['xG'] = shots['xG'].astype('float64')
shots['X'] = shots['X'].astype('float64')
shots['Y'] = shots['Y'].astype('float64')
# Original X and Y
shots['X'] = (shots['X']) * 100
shots['Y'] = (shots['Y']) * 100
goals = shots[shots['result'] == 'Goal']
goals_y = goals[goals['Y'] < 45]
goals_2020 = goals_y[goals_y['season'] == '2015']
# print(type(goals_2020))
# print(goals_2020)

# Main code
pitch = Pitch(  # pitch extends slightly below halfway line
    half=False,  # half of a pitch
    goal_alpha=0.4,
    pitch_type='opta',
    pitch_color='grey',
    tight_layout=True,
    line_color='white',
    linewidth=2.5,
    axis=True)
# stripe_color='#c2d59d',
# stripe=True)  # The measurements for Stats Perform are 105x68

# fig, ax = pitch.draw(figsize=(12, 10))
fig, ax = pitch.draw(figsize=(11, 17))
sc1 = pitch.scatter(0.690999985*100, 0.034000001*100, ax=ax)"""

pitch = Pitch(  # pitch extends slightly below halfway line
    half=False,  # half of a pitch
    goal_alpha=0.4,
    pitch_type='opta',
    pitch_color='#8d9db6',
    tight_layout=True,
    line_color='white',
    linewidth=2.5,
    axis=True)
# #b0aac0
#   8d9db6
# stripe_color='#c2d59d',
# stripe=True)  # The measurements for Stats Perform are 105x68

# fig, ax = pitch.draw(figsize=(12, 10))
fig, ax = pitch.draw(figsize=(11, 17))
# sc1 = pitch.scatter(0.690999985*100, 0.034000001*100, ax=ax)

# SC1

plt.savefig('fooshots.png', bbox_inches='tight', pad_inches=0)
plt.show()
