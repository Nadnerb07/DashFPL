import pandas as pd
import plotly.express as px

yo = pd.read_csv('/Users/brendanbaker/PycharmProjects/flaskFPL/radar_data_2021-22.csv')

rdf = pd.DataFrame(yo)

# id,player_name,games,time,goals,xG,assists,xA,shots,key_passes,yellow_cards,red_cards,position,team_title,npg,npxG,xGChain,xGBuildup
import plotly.graph_objects as go

player1 = 'Bukayo Saka'
player2 = 'Reece James'

pd.set_option('display.max_columns', 500)
data = ['xG', 'xA', 'npg', 'npxG', 'xGChain', 'xGBuildup', 'xG']

"""
fig = go.Figure(data=go.Scatterpolar(
        r=df1_for_plot['score'],
        theta=df1_for_plot.index,
        fill='toself',
        #marker_color='yellow',
        #opacity=0.7,
        hoverinfo="text",
        name=player1,
        text=[df1_for_plot.index[i] + ' = ' + str(df1_for_plot['score'][i]) for i in range(len(df1_for_plot))]
    ))
"""

"""
    fig.update_layout(
        autosize=False,
        width=800,
        height=800,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        bgcolor="rgba(0,0,0,0)",
    )
"""


def tab_1_function(player1, player2):
    # scatterpolar
    df1_for_plot = pd.DataFrame(rdf[rdf['player_name'] == player1][data].iloc[0])
    df2_for_plot = pd.DataFrame(rdf[rdf['player_name'] == player2][data].iloc[0])
    print(df1_for_plot)
    df1_for_plot.columns = ['score']
    df2_for_plot.columns = ['score']
    print(df1_for_plot)
    list_scores = [df1_for_plot.index[i] + ' = ' + str(df1_for_plot['score'][i]) for i in
                   range(len(df1_for_plot))]
    text_scores_1 = player1
    for i in list_scores:
        text_scores_1 += '<br>' + i

    list_scores = [df2_for_plot.index[i] + ' = ' + str(df2_for_plot['score'][i]) for i in
                   range(len(df2_for_plot))]
    text_scores_2 = player2
    for i in list_scores:
        text_scores_2 += '<br>' + i
    print(text_scores_1[0])
    fig = go.Figure(data=go.Scatterpolar(
        r=df1_for_plot['score'],
        theta=df1_for_plot.index,
        fill='toself',
        # marker_color='yellow',
        # opacity=0.7,
        hoverinfo="text",
        name=(player1 + ' ' + str(rdf[rdf['player_name'] == player1]['time'].iloc[0]) + 'mp'),
        text=[df1_for_plot.index[i] + ' = ' + str(df1_for_plot['score'][i]) for i in range(len(df1_for_plot))]
    ))

    fig.add_trace(go.Scatterpolar(
        r=df2_for_plot['score'],
        theta=df2_for_plot.index,
        fill='toself',
        # marker_color='mediumvioletred',
        hoverinfo="text",
        # opacity=1,
        name=(player2 + ' ' + str(rdf[rdf['player_name'] == player2]['time'].iloc[0]) + 'mp'),
        text=[df2_for_plot.index[i] + ' = ' + str(df2_for_plot['score'][i]) for i in range(len(df2_for_plot))]
    ))

    fig.update_layout(
        polar=dict(
            #hole=0.1,
            bgcolor="grey",
            radialaxis=dict(
                visible=True,
                #type='linear',
                #autotypenumbers='strict',
                #autorange=False,
                #range=[30, 100],
                #angle=90,
                showline=False,
                showticklabels=False, ticks='',
                gridcolor='yellow'),
                ),
        width=800,
        height=800,
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)',

    )

    fig.show()


tab_1_function(player1, player2)
