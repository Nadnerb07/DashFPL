# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash_table
import pandas
import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from PIL import Image
import dash_bootstrap_components as dbc
from data_extraction import getPlayer, get_gameweek_history

pyLogo = Image.open("/Users/brendanbaker/DashFPL/Screenshot 2022-03-01 at 19.12.20.png")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
pd.set_option('display.max_columns', 500)




df = pd.read_csv('/Users/brendanbaker/PycharmProjects/UnderstatAPI/Testing/shot_data.csv')
pdff = getPlayer()
# see https://plotly.com/python/px-arguments/ for more options
# df['X'] = df['X'].astype('float64')
# df['Y'] = df['Y'].astype('float64')
# print(0.034000001 * 98)
# print(0.690999985 * 100)
df['X'] = ((df['X']) * 100)
df['Y'] = ((df['Y']) * 100)
# print(df.iloc[[5042]])
# df = df.iloc[[1583]]
# del pdf['dreamteam_count'], pdf['special'], pdf['squad_number'], pdf['bps'], pdf['influence'], pdf['creativity'], pdf['threat'], pdf['ict_index'], pdf['influence_rank'], pdf['influence_rank_type'], pdf['creativity_rank']
pdf = pdff[['web_name', 'status', 'total_points', 'goals_scored', 'assists', 'minutes', 'bonus', 'selected_by_percent',
            'now_cost', 'team', 'news', 'id']]

pdf["selected_by_percent"] = pd.to_numeric(pdf["selected_by_percent"], downcast="float")

print(type(pdf['selected_by_percent'][0]))

final_pdf = pdf.sort_values(by=['selected_by_percent'], ascending=False)
all = df['result'].unique()
options = [{'label': x, 'value': x} for x in all]
options.append({'label': 'Select All', 'value': "all"})
app.layout = dbc.Container([
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

@app.callback(
    Output('lc', 'figure'),
    Input('player1', 'value'),
    Input('player2', 'value'),
)
def lineChart(player1, player2):
    df1 = final_pdf[final_pdf['web_name'] == player1]
    df2 = final_pdf[final_pdf['web_name'] == player2]
    #print(dff)
    id_1 = df1['id'].iloc[0]
    id_2 = df2['id'].iloc[0]
    int_id_1 = int(id_1)
    int_id_2 = int(id_2)

    gwdf1 = get_gameweek_history(int_id_1)
    gwdf2 = get_gameweek_history(int_id_2)

    gwdf1.loc[gwdf1['minutes'] == 0, 'total_points'] = None
    gwdf2.loc[gwdf2['minutes'] == 0, 'total_points'] = None

    fig = px.line(gwdf1, x='round', y='total_points', title="Gameweek Payer Data", hover_data=['minutes'])
    fig.update_traces(connectgaps=False)

    return fig


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

    fig.update_layout(margin={'l': 0, 'b': 0, 't': 20, 'r': 0}, hovermode='closest',)

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
    ))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
