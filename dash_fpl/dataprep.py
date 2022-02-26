# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import pandas
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from PIL import Image

pyLogo = Image.open("/Users/brendanbaker/DashFPL/Screenshot 2022-02-25 at 22.09.49.png")
app = Dash(__name__)
pd.set_option('display.max_columns', 500)
df = pd.read_csv('/Users/brendanbaker/PycharmProjects/UnderstatAPI/Testing/shot_data.csv')
# print(df)
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
# df['X'] = df['X'].astype('float64')
# df['Y'] = df['Y'].astype('float64')
# print(0.034000001 * 98)
# print(0.690999985 * 100)
df['X'] = ((df['X']) * 100)
df['Y'] = ((df['Y']) * 100)
# print(df.iloc[[5042]])
# df = df.iloc[[1583]]
available_players = df['player'].unique()
help = df['result'].unique()
"""
fig = px.scatter(df, x="X", y="Y", hover_name="player", hover_data=["result", "situation", 'player_assisted'])
#fig = px.scatter(x=0.034000001 * 100, y=0.007212541 * 100)
fig.update_layout(template="plotly_white", width=1070, height=711,
                  xaxis_showgrid=False, yaxis_showgrid=False)
fig.update_xaxes(
    visible=True,
    range=[0, 100]
)

fig.update_yaxes(
    visible=True,
    range=[0, 100]
)
fig.add_layout_image(
    source=pyLogo,
    xref="paper",
    yref="paper",
    x=0,
    y=1,
    xanchor="left",
    yanchor="top",
    layer="below",
    sizing="stretch",
    sizex=1.0,
    sizey=1.0
)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])
"""
all = df['result'].unique()
options = [{'label': x, 'value': x} for x in all]
options.append({'label': 'Select All', 'value': "all"})
# print(all)
app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                df['player'].unique(),
                'Hakim Ziyech',
                id='player',
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='choice',
                #options=[{'label': x, 'value': x} for x in all] + [{'label': 'Select all', 'value': 'all_values'}],
                options=[{'label': 'Select all', 'value': 'all_values'}] + [{'label': x, 'value': x} for x in all],
                value='all_values',
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
    ]),

    dcc.Graph(id='shot-map')
])


@app.callback(
    Output('shot-map', 'figure'),
    Input('player', 'value'),
    Input('choice', 'value'))
def update_graph(player, choice):
    dff = df[df['player'] == player]
    # Data frame with all the players data including shot data
    if choice == 'all_values':
        dff = df[df['player'] == player]
        print(dff)

    else:
        dff = dff[dff['result'] == choice]

    fig = px.scatter(dff, x="X", y="Y", color='result', size='xG', size_max=25, hover_name="player", hover_data=[
        "result", "situation", 'player_assisted'])

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.update_layout(template="plotly_white", width=1070, height=711,
                      xaxis_showgrid=False, yaxis_showgrid=False)
    fig.update_xaxes(
        visible=True,
        range=[0, 100]
    )

    fig.update_yaxes(
        visible=True,
        range=[0, 100]
    )
    fig.add_layout_image(
        source=pyLogo,
        xref="paper",
        yref="paper",
        x=0,
        y=1,
        xanchor="left",
        yanchor="top",
        layer="below",
        sizing="stretch",
        sizex=1.0,
        sizey=1.0
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
