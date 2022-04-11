# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# import dash_table
import pandas
import dash
from dash import html, dcc, Input, Output, dash_table
import plotly.express as px
import pandas as pd
from PIL import Image
import requests
import dash_bootstrap_components as dbc
from data_extraction import getPlayer, get_gameweek_history
from dash.dependencies import Input, Output, State
import base64
import plotly.graph_objects as go
import psycopg2
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask import Flask
from captain_picks import optimal_captain
import json

server = Flask(__name__)
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
                )

app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.server.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:jedi1999@localhost:5432/data'
db = SQLAlchemy(app.server)

df = pd.read_sql_table('shot_data', con=db.engine)
# radar_data = pd.read_sql_table('radar_data', con=db.engine)

# rdf = pd.DataFrame(radar_data)

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}
"""
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1'}]
                )
"""

# yo = pd.read_csv('/Users/brendanbaker/PycharmProjects/flaskFPL/radar_data_2021-22.csv')
# rdf = pd.DataFrame(yo)

yo = pd.read_sql_table('radar_data', con=db.engine)

rdf = pd.DataFrame(yo)
# print(rdf.info())

test_png = '/Users/brendanbaker/DashFPL/assets/Screenshot 2022-03-04 at 14.38.40.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')
pyLogo = Image.open("/Users/brendanbaker/DashFPL/Screenshot 2022-03-01 at 19.12.20.png")

test_png1 = '/Users/brendanbaker/DashFPL/assets/Screenshot 2022-03-04 at 17.53.34.png'
test1_base64 = base64.b64encode(open(test_png1, 'rb').read()).decode('ascii')

test_png2 = '/Users/brendanbaker/DashFPL/assets/Screenshot 2022-03-07 at 11.11.36.png'
test2_base64 = base64.b64encode(open(test_png2, 'rb').read()).decode('ascii')
nav_item = dbc.NavItem(dbc.NavLink("Fantasy Premier League", href="https://fantasy.premierleague.com/"))

pd.set_option('display.max_columns', 500)
data = ['xG', 'xA', 'npg', 'npxG', 'xGChain', 'xGBuildup', 'xG']
# df = pd.read_csv('/Users/brendanbaker/PycharmProjects/UnderstatAPI/Testing/shot_data.csv')


# engine = create_engine('postgresql://postgres:jedi1999@localhost:5432/data')
# df = pd.read_sql_table('shot_data', con=db.engine)

# df.to_sql('shot_data', engine)

pdff = getPlayer()
# see https://plotly.com/python/px-arguments/ for more options
# df['X'] = df['X'].astype('float64')
# df['Y'] = df['Y'].astype('float64')
# print(0.034000001 * 98)
# print(0.690999985 * 100)
# df['X'] = ((df['X']) * 100)
# df['Y'] = ((df['Y']) * 100)
# print(df.iloc[[5042]])
# df = df.iloc[[1583]]
# del pdf['dreamteam_count'], pdf['special'], pdf['squad_number'], pdf['bps'], pdf['influence'], pdf['creativity'], pdf['threat'], pdf['ict_index'], pdf['influence_rank'], pdf['influence_rank_type'], pdf['creativity_rank']
pdf = pdff[['web_name', 'status', 'total_points', 'goals_scored', 'assists', 'minutes', 'bonus', 'selected_by_percent',
            'now_cost', 'team', 'news', 'id']]
pd.options.mode.chained_assignment = None
pdf["selected_by_percent"] = pd.to_numeric(pdf["selected_by_percent"], downcast="float")

# print(type(pdf['selected_by_percent'][0]))

final_pdf = pdf.sort_values(by=['selected_by_percent'], ascending=False)
all = df['result'].unique()
options = [{'label': x, 'value': x} for x in all]
options.append({'label': 'Select All', 'value': "all"})
# print(df.dtypes)
"""app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("FPL Dashboard",
                        # text centered, text blue, mb-4 padding underneath title
                        className='text-center text-primary mb-4'),
                width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Dropdown(df['player'].unique(), id='player', ),
                width={'size': 2, "offset": 1, 'order': 0}
                ),

        dbc.Col(dcc.Dropdown(id='choice', value='all_values',
                             options=[{'label': 'Select all', 'value': 'all_values'}] + [{'label': x, 'value': x} for x
                                                                                         in all]),
                width={'size': 2, "offset": 1, 'order': 1}
                ),
        dbc.Col(dcc.Dropdown(final_pdf['web_name'].unique(), id='player1', value='Ziyech'),
                width={'size': 2, "offset": 0, 'order': 2}
                ),
        dbc.Col(dcc.Dropdown(final_pdf['web_name'].unique(), id='player2', value='Ronaldo'),
                width={'size': 2, "offset": 1, 'order': 2}
                ),

    ]),
    dbc.Row([

        dbc.Col(dcc.Graph(id='shot-map', figure={}, config={'displaylogo': False, 'displayModeBar': False}),
                width=6, lg={'size': 5, "offset": 1, 'order': 'first'}
                ),
        dbc.Col(dcc.Graph(id='lc', figure={}, config={'displaylogo': False, 'displayModeBar': False}),
                width=6, lg={'size': 6, "offset": 0, 'order': 'second'}),

    ]),

    dbc.Row([
        dbc.Col(html.H1("Statistic Table",
                        # text centered, text blue, mb-4 padding underneath title
                        className='text-center text-primary mb-4'),
                width=12)
    ]),
    # https://www.youtube.com/watch?v=0mfIK8zxUds --> Justify, turn off offset and watch out for size
    # Order in which the features appear left-to-right, offset from left, size how many columns taken-up

    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                final_pdf.to_dict('records'),
                [{"name": i, "id": i} for i in final_pdf.columns],
                filter_action='native',
                page_size=5,
                style_table={'overflowX': 'auto', 'height': '250px'},
                fill_width=False,
                style_data={'whiteSpace': 'normal', 'height': 'auto', 'font_size': 15},
                style_cell={
                    # 'height': 'auto',
                    # all three widths are needed
                    # 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                    # 'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                    'whiteSpace': 'normal'
                },
                style_cell_conditional=[
                    {'if': {'column_id': 'news'},
                     'width': '300px'},
                    {'if': {'column_id': 'web_name'},
                     'width': '150px'}],
            ),
        ], width={'size': 10, "offset": 1, 'order': 0}),
    ])
], fluid=True)
"""
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("LinkedIn", href='https://www.linkedin.com/in/brendan-b-249996191/'),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Github", href='https://github.com/Nadnerb07'),
    ],
    nav=True,
    in_navbar=True,
    label="Important Links",
)
DropdownApp = dbc.Container([
    dbc.Row([
        dbc.Col(dcc.Dropdown(df['player'].unique(), id='player', ),
                width={'size': 4, "offset": 1, 'order': 0}
                ),

        dbc.Col(dcc.Dropdown(id='choice', value='all_values',
                             options=[{'label': 'Select all', 'value': 'all_values'}] + [{'label': x, 'value': x} for x
                                                                                         in all]),
                width={'size': 4, "offset": 1, 'order': 1}
                ),
    ]),
    dbc.Row([

        dbc.Col(dcc.Graph(id='shot-map', figure={}, config={'displaylogo': False, 'displayModeBar': False}),
                width=10, lg={'size': 10, "offset": 1, 'order': 'first'}, style={'paper_bgcolor': 'rgb(0,0,0,0)'},
                ),
    ]),
])

DropdownApp1 = dbc.Container([
    dbc.Row([
        dbc.Col(dcc.Dropdown(final_pdf['web_name'].unique(), id='player1', value='Ziyech'),
                width={'size': 4, "offset": 0, 'order': 2}
                ),
        dbc.Col(dcc.Dropdown(final_pdf['web_name'].unique(), id='player2', value='Ronaldo'),
                width={'size': 4, "offset": 1, 'order': 2}
                ),
    ]),
    dbc.Row([

        dbc.Col(dcc.Graph(id='lc', figure={}, config={'displaylogo': False, 'displayModeBar': False}),
                width=12, lg={'size': 12, "offset": 0, 'order': 'second'}),
    ]),
])

DropdownApp2 = dbc.Container([
    dbc.Row([
        dbc.Col(dcc.Dropdown(rdf['player_name'].unique(), id='firstPlayer', value='Bukayo Saka'),
                width={'size': 4, "offset": 0, 'order': 2}
                ),
        dbc.Col(dcc.Dropdown(rdf['player_name'].unique(), id='secondPlayer', value='Reece James'),
                width={'size': 4, "offset": 1, 'order': 2}
                ),
    ]),
    dbc.Row([

        dbc.Col(dcc.Graph(id='radar', figure={}, config={'displaylogo': False, 'displayModeBar': False}),
                width=12, lg={'size': 12, "offset": 0, 'order': 'second'}),
    ]),
])
cardOne = dbc.Card(
    [
        dbc.CardImg(src='data:assets/png;base64,{}'.format(test_base64), style={'height': '100%', 'width': '100%'},
                    top=True),
        dbc.CardBody(
            [
                html.H4("League Shot Map", className="card-title"),
                html.P(
                    "An interactive shot map capable of visualising every players shot outcome in the league, "
                    "use widgets to filter and hover over a shot to view further dimensions.",
                    className="card-text",
                ),
                dbc.Button("Open App", id="open", color='warning'),  # style={'margin': 'auto', 'width': '100%'}),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Player's Shot Outcome"),
                        dbc.ModalBody(DropdownApp),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close", className="ml-auto")
                        ),
                    ],
                    id="modal",
                    size="lg",
                    style={'color': 'plotly_dark'},
                ),
            ]
        ),
    ],
    style={"width": "100%", 'height': '100%'},
)

cardTwo = dbc.Card(
    [
        dbc.CardImg(src='data:assets/png;base64,{}'.format(test1_base64),
                    # style={'height': '100%', 'width': '100%', "opacity": 0.35},
                    top=True),

        dbc.CardImgOverlay(
            dbc.CardBody(
                [
                    html.H4("Gameweek performance", className="card-title"),
                    html.P(
                        "A interactive line-chart showcasing game-week timeseries data in correlation with total points",
                        className="card-text",
                    ),
                    dbc.Button("Open App", id="opentwo", color='warning'),
                    # style={'margin': 'auto', 'width': '100%'}),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Player Gameweek Performance"),
                            dbc.ModalBody(DropdownApp1),
                            dbc.ModalFooter(
                                dbc.Button("Close", id="closetwo", className="ml-auto")
                            ),
                        ],
                        id="modaltwo",
                        size="lg",
                        style={'color': 'plotly_dark'},
                    ),
                ]
            ),
        ),
    ],
    # style={"width": "22rem", 'height': '15rem'},
)

cardThree = dbc.Card(
    [
        dbc.CardImg(src='data:assets/png;base64,{}'.format(test2_base64), style={'height': '100%', 'width': '100%'},
                    top=True),

        dbc.CardBody(
            [
                html.H4("Radar Analysis", className="card-title"),
                html.P(
                    "Radar Chart allowing player comparison across multiple variables including xG, xA, npxG, "
                    "xGChain, xGBuildup, npg. Pick any player in the league and begin exploring.",
                    className="card-text",
                ),
                dbc.Button("Open App", id="open3", color='warning'),  # style={'margin': 'auto', 'width': '100%'}),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Player Gameweek Performance"),
                        dbc.ModalBody(DropdownApp2),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close3", className="ml-auto")
                        ),
                    ],
                    id="modal3",
                    size="lg",
                    style={'color': 'plotly_dark'},
                ),
            ]
        ),

    ],
    style={"width": "100%", 'height': '100%'},
)
"""Body"""
# rows
col1 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(cardOne), xs=12, sm=12, md=6, lg=3)
            ],
            style={'margin': 'auto', 'width': '80vw'}
        ),
    ]
)

col2 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(cardTwo))
            ],
            style={'margin': 'auto', 'width': '80vw'}
        ),
    ]
)

col3 = html.Div(
    [
        dbc.Row(dbc.Col(html.Div(cardThree)),
                style={'margin': 'auto', 'width': '80vw'}
                ),
    ]
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(dbc.NavbarBrand("Fantasy Premier League Visualisations", className="ml-2")),
                    ],
                    align="center",
                    # no_gutters=True,

                ),
                # href="https://plot.ly",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [nav_item,
                     dropdown,
                     ], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    # className="mb-4",
)
#####################################################################################

"""Layout"""

"""app.layout = html.Div([
    dbc.Row(dbc.Col(navbar, width=12)),
    dbc.Row([
        dbc.Col(col1, width={'size': 3, "offset": 0, 'order': 0}),
        dbc.Col(col2, width={'size': 3, "offset": 0, 'order': 1}),
    ])

])
width = {'offset': 0}
"""
# html.div
"""viz_layout = html.Div([
    # dbc.Row(dbc.Col(navbar, width=12)),
    dbc.Row([
        dbc.Col(col1, xs=12, sm=12, md=6, lg=3),
        dbc.Col(col3, xs=12, sm=12, md=6, lg=3),
        dbc.Col(
            [
                dbc.Row(
                    dbc.Col(cardTwo)),

                # dbc.Row(
                # dbc.Col(cardThree))
            ], width={'size': 3, "offset": 0, 'order': 0}),
        # dbc.Col(col3, width={'size': 3, "offset": 0, 'order': 0}, style={'border': '1px solid'})
    ], )

], )"""

viz_layout = html.Div([
    # dbc.Row(dbc.Col(navbar, width=12)),
    dbc.Row([dbc.Col(cardOne, xs={'size': 12, "offset": 0}, sm={'size': 12, "offset": 0}, md={'size': 6, "offset": 1},
                     lg={'size': 3, "offset": 1}),
             dbc.Col(cardThree, xs=12, sm=12, md=6, lg=3),
             dbc.Col(cardTwo, xs=12, sm=12, md=6, lg=3)]),

], )

"""app_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Visualisations", tab_id="tab-visualisation", labelClassName="text-success font-weight-bold",
                        activeLabelClassName="text-danger"),
            ],
            id="tabs",
            active_tab="tab-visualisations",
        ),
    ], className="mt-3"
)
"""
app_tabs = html.Div([
    dcc.Tabs(id='tabs', value='tab-visualisations', children=[
        dcc.Tab(label='Visualisations', value='tab-visualisations', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Optimal Captaincy', value='tab-2', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),

])

app.layout = html.Div([
    dbc.Row(dbc.Col(navbar, width=12)),
    # html.Hr(),
    dbc.Row(dbc.Col(app_tabs, width=12)),
    html.Div(id='content', children=[])

])


def captain_layout_function(captain_df):
    captain_layout = html.Div([
        dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    captain_df.to_dict('records'),
                    [{"name": i, "id": i} for i in captain_df.columns],
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable="single",
                    filter_action='native',
                    page_size=6,
                    style_table={'overflowX': 'auto', 'height': '250px'},
                    fill_width=False,
                    style_data={'whiteSpace': 'normal', 'height': 'auto', 'font_size': 15},
                    style_cell={
                        # 'height': 'auto',
                        # all three widths are needed
                        # 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                        # 'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                        'whiteSpace': 'normal'
                    },
                    style_data_conditional=[
                        {
                            'if': {
                                'filter_query': '{Points} >= {Optimal Points}',
                                'column_id': 'Difference'
                            },
                            'color': 'chartreuse',
                            'fontWeight': 'bold'
                        },
                        {
                            'if': {
                                'filter_query': '{Difference} <= -10 && {Difference} >= -20',
                                'column_id': 'Difference'
                            },
                            'color': 'orange',
                            'fontWeight': 'bold'
                        },
                        {
                            'if': {
                                'filter_query': '{Difference} <= -1 && {Difference} > -10',
                                'column_id': 'Difference'
                            },
                            'color': 'forestgreen',
                            'fontWeight': 'bold'
                        },
                        {
                            'if': {
                                'filter_query': '{Difference} < -20',
                                'column_id': 'Difference'
                            },
                            'color': 'red',
                            'fontWeight': 'bold'
                        },

                    ],

                ),
            ], width={'size': 10, "offset": 1, 'order': 0}),
        ])
    ])
    return captain_layout


app.config.suppress_callback_exceptions = True

inputs = html.Div(
    children=[
        dbc.Row(
            className='mb-5',
        ),
        dbc.Row(
            dbc.Col(
                html.H1("Optimal Captaincy History", className='text-center text-primary, mb-3'),
                width={"size": 6, "offset": 3},
            )
        ),
        dbc.Row(
            dbc.Col(
                html.H2("Enter Team ID below", className='text-center text-primary, mb-4'),
                width={"size": 6, "offset": 3},
            )
        ),
        dbc.Row([
            dbc.Col([
                dbc.Input(id="input", placeholder="Enter Team ID", type="text", className="text-center mb-4"),
                html.Br(),
            ], width={"size": 4, "offset": 4}),

            dbc.Col(dbc.Button(id="loading-button", n_clicks=0, color='success', children=["Enter"]),
                    width={'size': 1, 'offset': 0}),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Spinner(html.Div(id='output', children=[]), fullscreen=True,
                            spinner_style={"width": "10rem", "height": "10rem"}),

            ]),
        ]),
        dbc.Row([
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(id="the_alert", children=[]),
            ], width={"size": 4, "offset": 4}, className="d-grid gap-2", )
        ]),
    ])

alert = html.Div(
    [
        dbc.Row([
            dbc.Col([
                dbc.Alert(
                    [
                        html.H4('Error - Invalid Team ID', className="alert-heading"),
                        html.Hr(),
                        "Please enter a valid team ID, a guide on how to find your team ID can be found ",
                        html.A("Here", href="https://fpl.team/find-id", className="alert-link"),
                    ],
                    color="danger", dismissable=True, duration=4500,
                ),
            ], width={"size": 6, "offset": 3}, className="d-grid gap-2"),
        ]),
    ]
)

dbc.Alert(
    [
        html.H4('Error - Invalid Team ID', className="alert-heading"),
        html.Hr(),
        "Please enter a valid team ID, a guide on how to find your team ID can be found ",
        html.A("Here", href="https://fpl.team/find-id", className="alert-link"),
    ],
    color="danger",
),


@app.callback([Output("output", "children"), Output("the_alert", "children")],
              [Input("loading-button", "n_clicks")], [State("input", "value")])
def output_text(n_clicks, value):
    if n_clicks:
        id = value
        manager_id = requests.get(f"https://fantasy.premierleague.com/api/entry/{id}/")
        if manager_id.status_code == 404:
            return alert, dash.no_update
        else:
            manager_id.json()
            data = (json.loads(manager_id.text))
            print(value)
            temp_df = optimal_captain(value).reset_index()
            # data = temp_df.to_dict('records')
            # columns = [{"name": i, "id": i, } for i in (temp_df.columns)]
            return captain_layout_function(temp_df), dash.no_update
    return dash.no_update


@app.callback(
    Output("content", "children"),
    [Input("tabs", "value")]
)
def switch_tab(tab_chosen):
    if tab_chosen == "tab-visualisations":
        return viz_layout
    if tab_chosen == 'tab-2':
        return inputs
    return html.P("This shouldn't be displayed for now...")


# remove fuild
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output('lc', 'figure'),
    Input('player1', 'value'),
    Input('player2', 'value'),
)
def lineChart(player1, player2):
    df1 = final_pdf[final_pdf['web_name'] == player1]
    df2 = final_pdf[final_pdf['web_name'] == player2]
    # print(dff)
    id_1 = df1['id'].iloc[0]
    id_2 = df2['id'].iloc[0]
    int_id_1 = int(id_1)
    int_id_2 = int(id_2)

    gwdf1 = get_gameweek_history(int_id_1)
    gwdf2 = get_gameweek_history(int_id_2)

    gwdf1.loc[gwdf1['minutes'] == 0, 'total_points'] = None
    gwdf2.loc[gwdf2['minutes'] == 0, 'total_points'] = None

    fig = px.line(gwdf1, x='round', y='total_points', title="Gameweek Payer Data", hover_data=['minutes'])
    fig.update_traces(line_color='blue')
    fig.update_traces(connectgaps=False)

    fig2 = px.line(gwdf2, x='round', y='total_points', title="Gameweek Payer Data", hover_data=['minutes'])
    fig.update_traces(connectgaps=False)
    fig2.update_traces(line_color='orange')
    fig3 = go.Figure(data=fig.data + fig2.data)

    fig3.update_layout(
        title="Gameweek Payer Data",
        xaxis_title="Gameweek",
        yaxis_title="Points",
        legend_title="Player",

        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )

    return fig3


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

    fig = px.scatter(dff, x="X", y="Y", color='result', size_max=25, hover_name="player",
                     hover_data={"result": True, "situation": True, 'player_assisted': True, 'X': False, 'Y': False}
                     , size='xG')

    fig.update_layout(margin={'l': 0, 'b': 0, 't': 0, 'r': 0}, hovermode='closest')

    # fig.update_layout(template="simple_white", width=1070, height=711,
    # xaxis_showgrid=False, yaxis_showgrid=False)
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
        sizey=1.0,
    )

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        # bgcolor='rgb(0,0,0,0)',
    ))
    return fig


@app.callback(
    Output("modaltwo", "is_open"),
    [Input("opentwo", "n_clicks"), Input("closetwo", "n_clicks")],
    [State("modaltwo", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("modal3", "is_open"),
    [Input("open3", "n_clicks"), Input("close3", "n_clicks")],
    [State("modal3", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output('radar', 'figure'),
    Input('firstPlayer', 'value'),
    Input('secondPlayer', 'value'))
def radar_function(firstPlayer, secondPayer):
    # scatterpolar
    df1_for_plot = pd.DataFrame(rdf[rdf['player_name'] == firstPlayer][data].iloc[0])
    df2_for_plot = pd.DataFrame(rdf[rdf['player_name'] == secondPayer][data].iloc[0])
    # print(df1_for_plot)
    df1_for_plot.columns = ['score']
    df2_for_plot.columns = ['score']
    # print(df1_for_plot)
    list_scores = [df1_for_plot.index[i] + ' = ' + str(df1_for_plot['score'][i]) for i in
                   range(len(df1_for_plot))]
    text_scores_1 = firstPlayer
    for i in list_scores:
        text_scores_1 += '<br>' + i

    list_scores = [df2_for_plot.index[i] + ' = ' + str(df2_for_plot['score'][i]) for i in
                   range(len(df2_for_plot))]
    text_scores_2 = secondPayer
    for i in list_scores:
        text_scores_2 += '<br>' + i
    # print(text_scores_1[0])
    fig = go.Figure(data=go.Scatterpolar(
        r=df1_for_plot['score'],
        theta=df1_for_plot.index,
        fill='toself',
        # marker_color='yellow',
        # opacity=0.7,
        hoverinfo="text",
        name=(firstPlayer + ' ' + str(rdf[rdf['player_name'] == firstPlayer]['time'].iloc[0]) + 'mp'),
        text=[df1_for_plot.index[i] + ' = ' + str(df1_for_plot['score'][i]) for i in range(len(df1_for_plot))]
    ))

    fig.add_trace(go.Scatterpolar(
        r=df2_for_plot['score'],
        theta=df2_for_plot.index,
        fill='toself',
        # marker_color='mediumvioletred',
        hoverinfo="text",
        # opacity=1,
        name=(secondPayer + ' ' + str(rdf[rdf['player_name'] == secondPayer]['time'].iloc[0]) + 'mp'),
        text=[df2_for_plot.index[i] + ' = ' + str(df2_for_plot['score'][i]) for i in range(len(df2_for_plot))]
    ))

    fig.update_layout(
        polar=dict(
            # hole=0.1,
            bgcolor="grey",
            radialaxis=dict(
                visible=True,
                # type='linear',
                # autotypenumbers='strict',
                # autorange=False,
                # range=[30, 100],
                # angle=90,
                showline=False,
                showticklabels=False, ticks='',
                gridcolor='yellow'),
        ),
        # width=750,
        # height=750,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',

    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
