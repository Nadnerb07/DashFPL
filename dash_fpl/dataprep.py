# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import pandas
import dash
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from PIL import Image
import dash_bootstrap_components as dbc

# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# app = Dash(__name__)
pyLogo = Image.open("/Users/brendanbaker/DashFPL/Screenshot 2022-02-25 at 22.09.49.png")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
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
"""app.layout = dbc.Container(
    dbc.Alert("Hello Bootstrap!", color="success"),
    className="p-5",
)"""
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
        ], style={'width': '20%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='choice',
                # options=[{'label': x, 'value': x} for x in all] + [{'label': 'Select all', 'value': 'all_values'}],
                options=[{'label': 'Select all', 'value': 'all_values'}] + [{'label': x, 'value': x} for x in all],
                value='all_values',
            )
        ], style={'width': '20%', 'display': 'inline-block'}),
    ]),

    dcc.Graph(id='shot-map')
])
"""
all = df['result'].unique()
options = [{'label': x, 'value': x} for x in all]
options.append({'label': 'Select All', 'value': "all"})

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("FPL Dashboard",
                        # text centered, text blue, mb-4 padding underneath title
                        className='text-center text-primary, mb-4'),
                width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(df['player'].unique(),
                         'Hakim Ziyech',
                         id='player',
                         style={'width': '60%'},
                         ),

            dcc.Dropdown(id='choice', multi=False, value='all_values',
                         options=[{'label': 'Select all', 'value': 'all_values'}] + [{'label': x, 'value': x} for x in
                                                                                     all],
                         style={'width': '50%'}
                         ),

            dcc.Graph(id='shot-map', figure={}, config={'displaylogo': False, 'displayModeBar':False}),
            # https://www.youtube.com/watch?v=0mfIK8zxUds --> Justify, turn off offset and watch out for size
            # Order in which the features appear left-to-right, offset from left, size how many columns taken-up
        ], width={'size': 6, 'offset': 1, 'order': 1})
    ], className="g-1"),  # Gutter 1 gap between pitch and radar
], fluid=True)


@app.callback(
    Output('shot-map', 'figure'),
    Input('player', 'value'),
    Input('choice', 'value'))
def update_graph(player, choice):
    dff = df[df['player'] == player]
    # Data frame with all the players data including shot data
    if choice == 'all_values':
        dff = df[df['player'] == player]
        # print(dff)

    else:
        dff = dff[dff['result'] == choice]

    fig = px.scatter(dff, x="X", y="Y", color='result', size='xG', size_max=25, hover_name="player", hover_data=[
        "result", "situation", 'player_assisted'])

    fig.update_layout(margin={'l': 0, 'b': 0, 't': 25, 'r': 0}, hovermode='closest')

    #fig.update_layout(template="simple_white", width=1070, height=711,
                      #xaxis_showgrid=False, yaxis_showgrid=False)
    fig.update_xaxes(
        visible=False,
        range=[0, 100]
    )

    fig.update_yaxes(
        visible=False,
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

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
