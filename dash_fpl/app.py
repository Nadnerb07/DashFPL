
import dash
from dash import html, dcc, dash_table
import plotly.express as px
import pandas as pd
from PIL import Image
import requests
import dash_bootstrap_components as dbc
from data_extraction import getPlayer, get_gameweek_history
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from captain_picks import optimal_captain

pd.options.mode.chained_assignment = None
pd.options.display.float_format = "{:,.2f}".format
pd.set_option('display.max_columns', 500)
server = Flask(__name__)
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
                )

app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.server.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:jedi1999@localhost:5432/data'
db = SQLAlchemy(app.server)

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
    'backgroundColor': '#00ff85',  # 00ff85
    'color': 'black',
    'padding': '6px'
}

radarData = pd.read_sql_table('radar_data', con=db.engine)
df = pd.read_sql_table('shot_data', con=db.engine)
rdf = pd.DataFrame(radarData)

"""
Images from assets folder for cards and visualisations
"""
pitch = Image.open("/Users/brendanbaker/DashFPL/assets/Screenshot 2022-03-01 at 19.12.20.png")
gameweekLineChartImage = Image.open('/Users/brendanbaker/DashFPL/assets/Screenshot 2022-03-04 at 17.53.34.png')
shotMapImage = Image.open("/Users/brendanbaker/DashFPL/assets/Screenshot 2022-03-04 at 14.38.40.png")
radarImage = Image.open('/Users/brendanbaker/DashFPL/assets/Screenshot 2022-03-07 at 11.11.36.png')
bubbleChartImage = Image.open('/Users/brendanbaker/DashFPL/assets/Screenshot 2022-04-20 at 17.06.33.png')


nav_item = dbc.NavItem(dbc.NavLink("Fantasy Premier League", href="https://fantasy.premierleague.com/"))

data = ['xG90', 'xA90', 'A90', 'xGBuildup90', 'G90', 'xG90']

pdff = getPlayer()

pdf = pdff[['web_name', 'status', 'total_points', 'goals_scored', 'assists', 'minutes', 'bonus', 'selected_by_percent',
            'now_cost', 'team', 'news', 'id', 'element_type']]
pdf['element_type'] = pdf['element_type'].astype(str)

# Function
pdf.loc[pdf['element_type'] == '1', 'element_type'] = 'Goalkeeper'
pdf.loc[pdf['element_type'] == '2', 'element_type'] = 'Defender'
pdf.loc[pdf['element_type'] == '3', 'element_type'] = 'Midfielder'
pdf.loc[pdf['element_type'] == '4', 'element_type'] = 'Forward'

pdf["selected_by_percent"] = pd.to_numeric(pdf["selected_by_percent"], downcast="float")

final_pdf = pdf.sort_values(by=['selected_by_percent'], ascending=False)
test_pdf = final_pdf


all = df['result'].unique()
options = [{'label': x, 'value': x} for x in all]
options = [{'label': x, 'value': x} for x in all]
options.append({'label': 'Select All', 'value': "all"})

ShotMapDropdownApp = dbc.Container([
    dbc.Row([
        dbc.Col(dcc.Dropdown(df['player'].unique(), id='player', value='Mason Mount'),
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

LineChartDropdownApp = dbc.Container([
    dbc.Row([
        dbc.Col(dcc.Dropdown(final_pdf['web_name'].unique(), id='player1', value='Ziyech', clearable=False),
                width={'size': 4, "offset": 0, 'order': 2}
                ),
        dbc.Col(dcc.Dropdown(final_pdf['web_name'].unique(), id='player2', value='Ronaldo', clearable=False),
                width={'size': 4, "offset": 1, 'order': 2}
                ),
    ]),
    dbc.Row([

        dbc.Col(dcc.Graph(id='lc', figure={}, config={'displaylogo': False, 'displayModeBar': True}),
                width=12, lg={'size': 12, "offset": 0, 'order': 'second'}),
    ]),
])

RadarChartDropdownApp = dbc.Container([
    dbc.Row([
        dbc.Col(dcc.Dropdown(rdf['player_name'].unique(), id='firstPlayer', value='Bukayo Saka', clearable=False),
                width={'size': 4, "offset": 0, 'order': 2}
                ),
        dbc.Col(dcc.Dropdown(rdf['player_name'].unique(), id='secondPlayer', value='Reece James', clearable=False),
                width={'size': 4, "offset": 1, 'order': 2}
                ),
    ]),
    dbc.Row([

        dbc.Col(dcc.Graph(id='radar', figure={}, config={'displaylogo': False, 'displayModeBar': False}),
                width=12, lg={'size': 12, "offset": 0, 'order': 'second'}),
    ]),
])

ShotMapCard = dbc.Card(
    [
        dbc.CardImg(src=shotMapImage, style={'height': '100%', 'width': '100%'},
                    top=True),
        dbc.CardBody(
            [
                html.H4("League Shot Map", className="card-title"),
                html.P(
                    "An interactive shot map capable of visualising every players shot outcome in the league, "
                    "use widgets to filter and hover over a shot to view further dimensions.",
                    className="card-text",
                ),
                dbc.Button("Open App", id="open", color='warning'),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Player's Shot Outcome"),
                        dbc.ModalBody(ShotMapDropdownApp),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close", className="ml-auto", color='danger')
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

LineChartCard = dbc.Card(
    [
        dbc.CardImg(src=gameweekLineChartImage,
                    # style={'height': '100%', 'width': '100%', "opacity": 0.35},
                    top=True,
                    style={'height': '100%', 'width': '100%', "opacity": 0.5}
                    ),

        dbc.CardImgOverlay(
            dbc.CardBody(
                [
                    html.H4("Gameweek performance", className="card-title"),
                    html.P(
                        "A interactive line-chart showcasing game-week timeseries data in correlation with total "
                        "points.",
                        className="card-text",
                    ),
                    dbc.Button("Open App", id="opentwo", color='warning'),
                    # style={'margin': 'auto', 'width': '100%'}),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Player Gameweek Performance"),
                            dbc.ModalBody('Note - Gaps represent a player has not participate in a given gameweek.'),
                            dbc.ModalBody(LineChartDropdownApp),
                            dbc.ModalFooter(
                                dbc.Button("Close", id="closetwo", className="ml-auto", color='danger')
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
    style={"width": "100%", 'height': '100%'},
)

RadarChartCard = dbc.Card(
    [
        dbc.CardImg(src=radarImage, style={'height': '100%', 'width': '100%'},
                    top=True),

        dbc.CardBody(
            [
                html.H4("Radar Analysis", className="card-title"),
                html.P(
                    "Radar Chart allowing player comparison across multiple variables including xG90, xA90, G90, "
                    "A90 and "
                    "xGBuildup90.",
                    className="card-text",
                ),
                dbc.Button("Open App", id="open3", color='warning'),  # style={'margin': 'auto', 'width': '100%'}),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Radar Chart Comparison"),
                        dbc.ModalBody(RadarChartDropdownApp),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close3", className="ml-auto", color='danger')
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

bubbleChartLayout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.RangeSlider(0, 80, 5, count=1, value=[20, 40], id='year-slider',
                    )
])

BubbleChartCard = dbc.Card(
    [
        dbc.CardImg(src=bubbleChartImage, style={'height': '100%', 'width': '100%'},
                    top=True),
        dbc.CardBody(
            [
                html.H4("Points vs % Selected", className="card-title"),
                html.P(
                    "Explore season points vs Ownership Percentage using the range slider to find hidden value in players, "
                    "in addition to effective ownership.",
                    className="card-text",
                ),
                dbc.Button("Open App", id="open4", color='warning'),  # style={'margin': 'auto', 'width': '100%'}),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Points vs Ownership %"),
                        dbc.ModalBody(bubbleChartLayout),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close4", className="ml-auto", color='danger')
                        ),
                    ],
                    id="modal4",
                    size="lg",
                    style={'color': 'plotly_dark'},
                ),
            ]
        ),
    ],
    style={"width": "100%", 'height': '100%'},
)


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Offical FPL", href="https://fantasy.premierleague.com/")),
    ],
    brand="Fantasy Premier League Visualisations",
    brand_href="#",
    color="#38003c",  # 38003c
    dark=True,
)

visualisationsLayout = html.Div([

    dbc.Row([
        dbc.Col(ShotMapCard, xs={'size': 12, "offset": 0}, sm={'size': 12, "offset": 0}, md={'size': 5, "offset": 1},
                lg={'size': 3, "offset": 1}),

        dbc.Col(RadarChartCard, xs=12, sm=12, md=5, lg=3),
        dbc.Col(
            [
                dbc.Row(
                    LineChartCard,
                ),
                dbc.Row(className='mb-4'),
                dbc.Row(
                    BubbleChartCard,
                )
            ],
            xs={'size': 12, "offset": 0}, sm={'size': 12, "offset": 0}, md={'size': 4, "offset": 0},
            lg={'size': 4, "offset": 0},
        )
    ]
    )

]),

applicationTabs = html.Div([
    dcc.Tabs(id='tabs', value='tab-visualisations', children=[
        dcc.Tab(label='Visualisations', value='tab-visualisations', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Optimal Captaincy', value='tab-2', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),

])

app.layout = html.Div([
    dbc.Row(dbc.Col(navbar, xs=12, sm=12, md=12, lg=12, xl=12, xxl=12)),
    dbc.Row(dbc.Col(applicationTabs, width=12)),
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


optimalCaptainTabComponents = html.Div(
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

invalidTeamIDAlert = html.Div(
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


@app.callback([Output("output", "children"), Output("the_alert", "children")],
              [Input("loading-button", "n_clicks")], [State("input", "value")])
def output_text(n_clicks, value):
    if n_clicks:
        id = value
        manager_id = requests.get(f"https://fantasy.premierleague.com/api/entry/{id}/")
        if manager_id.status_code == 404:
            return invalidTeamIDAlert, dash.no_update
        else:
            temp_df = optimal_captain(value).reset_index()
            return captain_layout_function(temp_df), dash.no_update
    return dash.no_update


@app.callback(
    Output("content", "children"),
    [Input("tabs", "value")]
)
def switch_tab(tab_chosen):
    if tab_chosen == "tab-visualisations":
        return visualisationsLayout
    if tab_chosen == 'tab-2':
        return optimalCaptainTabComponents
    return html.P("This shouldn't be displayed for now...")


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
    fig3 = go.Figure()
    df1 = final_pdf[final_pdf['web_name'] == player1]
    df2 = final_pdf[final_pdf['web_name'] == player2]
    # print(dff)
    id_1 = df1['id'].iloc[0]
    id_2 = df2['id'].iloc[0]
    int_id_1 = int(id_1)
    int_id_2 = int(id_2)

    gwdf1 = get_gameweek_history(int_id_1)
    gwdf2 = get_gameweek_history(int_id_2)

    elements_df1 = gwdf1[['total_points', 'round', 'minutes']]
    elements_df2 = gwdf2[['total_points', 'round', 'minutes']]

    aggregation_functions = {'total_points': 'sum', 'round': 'sum', 'minutes': 'sum'}
    df_player1 = elements_df1.groupby(elements_df1['round']).aggregate(aggregation_functions)
    df_player2 = elements_df2.groupby(elements_df2['round']).aggregate(aggregation_functions)

    df_player1 = df_player1.drop(columns=['round'])
    df_player2 = df_player2.drop(columns=['round'])

    df_player1.loc[df_player1['minutes'] == 0, 'total_points'] = None
    df_player2.loc[df_player2['minutes'] == 0, 'total_points'] = None

    fig3.add_trace(go.Scatter(x=df_player1['total_points'].index, y=df_player1['total_points'],
                              mode='lines',
                              name=player1))
    fig3.add_trace(go.Scatter(x=df_player2['total_points'].index, y=df_player2['total_points'],
                              mode='lines',
                              name=player2))
    fig3.update_traces(
        hovertemplate="<br>".join([
            "Gameweek: %{x}",
            "Points: %{y}",
        ])
    )

    fig3.update_layout(
        title="Gameweek Player Data",
        xaxis_title="Gameweek",
        yaxis_title="Points",
        legend_title="Player",

    )

    return fig3


@app.callback(
    Output('shot-map', 'figure'),
    Input('player', 'value'),
    Input('choice', 'value'))
def update_graph(player, choice):
    dff = df[df['player'] == player]

    if choice == 'all_values':
        dff = df[df['player'] == player]

    else:
        dff = dff[dff['result'] == choice]

    dff = dff.rename(
        columns={'player': 'Player', 'result': 'Result', 'situation': 'Situation',
                 'player_assisted': 'Player Assisted'})

    try:

        fig1 = px.scatter(dff, x="X", y="Y", color='Result', size_max=25, hover_name="Player",
                          hover_data={"Result": True, "Situation": True, "Player Assisted": True, 'X': False,
                                      'Y': False}
                          , size='xG')
    except ValueError:
        fig1 = px.scatter(dff, x="X", y="Y", color='Result', size_max=25, hover_name="Player",
                          hover_data={"Result": True, "Situation": True, "Player Assisted": True, 'X': False,
                                      'Y': False}
                          , size='xG')

    fig1.update_layout(margin={'l': 0, 'b': 0, 't': 0, 'r': 0}, hovermode='closest')

    fig1.update_xaxes(
        visible=False,
        range=[0, 100]
    )

    fig1.update_yaxes(
        visible=False,
        range=[0, 100]
    )

    fig1.update_layout(
        hoverlabel=dict(
            # bgcolor="white",
            font_size=11,
            font_family="Arial"
        )
    )

    fig1.add_layout_image(
        source=pitch,
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

    fig1.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    ))
    return fig1


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
    Output("modal4", "is_open"),
    [Input("open4", "n_clicks"), Input("close4", "n_clicks")],
    [State("modal4", "is_open")],
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
    df1_for_plot = pd.DataFrame(rdf[rdf['player_name'] == firstPlayer][data].iloc[0])
    df2_for_plot = pd.DataFrame(rdf[rdf['player_name'] == secondPayer][data].iloc[0])

    df1_for_plot.columns = ['score']
    df2_for_plot.columns = ['score']

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

    fig = go.Figure(data=go.Scatterpolar(
        r=df1_for_plot['score'],
        theta=df1_for_plot.index,
        fill='toself',
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


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    temp = test_pdf[
        (test_pdf['selected_by_percent'] >= selected_year[0]) & (test_pdf['selected_by_percent'] <= selected_year[1])]

    temp['now_cost'] = temp['now_cost'].astype('float64')
    temp['now_cost'] = temp['now_cost'] / 10

    temp = temp.rename(
        columns={'web_name': 'Player', 'selected_by_percent': 'Ownership Percentage', 'total_points': 'Total Points',
                 'element_type': 'Position',
                 'now_cost': 'Cost'})
    try:
        fig = px.scatter(temp, x="Ownership Percentage", y="Total Points",
                         size="Cost", hover_name="Player",
                         size_max=35, color='Position', text="Player")
    except ValueError:
        fig = px.scatter(temp, x="Ownership Percentage", y="Total Points",
                         size="Cost", hover_name="Player",
                         size_max=35, color='Position', text="Player")

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
