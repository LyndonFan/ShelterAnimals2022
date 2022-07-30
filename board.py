from isodate import parse_date
import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime, timedelta
import os
import sys

from dash import Dash, dcc, html, Input, Output

CWD = os.path.dirname(os.path.abspath(__file__))

original_df = pd.read_csv(os.path.join(CWD, 'clean_data.csv'),
                          parse_dates=['date_of_birth', 'datetime'])
original_df = original_df.sort_values(by='datetime', ascending=False)

app = Dash(__name__)
app.layout = html.Div([
    html.H1('Shelter Animal Outcomes'),
    html.Div([
        html.Div(children=[
            html.H4(len(original_df)),
            html.P('distinct records')
        ],
            style={
            "display": "inline-block",
            "width": "20%"
        }),
        html.Div(children=[
            html.H4(len(original_df.animal_id.unique())),
            html.P('distinct animals')
        ], style={
            "display": "inline-block",
            "width": "20%"
        }),
        dcc.RadioItems(
            id='choose_unique_animals',
            options=[
                'All Visits', 'Distinct Animals (Most Recent)', 'Distinct Animals (Oldest)'],
            value='All Visits',
            inline=True,
            style={
                "display": "inline-block",
                "width": "20%"
            },
        )
    ], style={
        "display": "inline-block",
        "margin-left": "20px",
        "verticalAlign": "top",
        "width": "100%",
    },),
    html.Div(
        children=[
            dcc.Graph(
                id='animal_type_graph', style={
                    "display": "inline-block",
                    "width": "50%"
                }),
            dcc.Graph(
                id='sex_type_graph', style={
                    "display": "inline-block",
                    "width": "50%"
                }),
        ]
    ),
    # html.Div(
    #     children=[
    #         dcc.Graph(
    #             id='neutered_type_graph', style={
    #                 "display": "inline-block",
    #                 "width": "50%"
    #             }),
    #         dcc.Graph(),
    #     ]
    # ),
    dcc.Graph(id='outcome_type_graph'),
    html.Div(
        children=[
            dcc.Graph(
                id='event_count_graph', style={
                    "display": "inline-block",
                    "width": "50%"
                }),
            dcc.Graph(
                id='num_visits_graph', style={
                    "display": "inline-block",
                    "width": "50%"
                }
            ),
        ]
    ),
])


def df(row_option='All Visits'):
    assert row_option in [
        'All Visits', 'Distinct Animals (Most Recent)', 'Distinct Animals (Oldest)'], \
        f'{row_option} is not "All Visits", "Distinct Animals (Most Recent)", or "Distinct Animals (Oldest)"'
    if row_option == 'All Visits':
        return original_df.copy()
    if 'Most Recent' in row_option:
        return original_df.drop_duplicates(subset='datetime', keep='first')
    return original_df.drop_duplicates(subset='datetime', keep='last')


@ app.callback(
    Output('animal_type_graph', 'figure'),
    Input('choose_unique_animals', 'value')
)
def get_animal_type_graph(row_option):
    # vcs = df(row_option).animal_type.fillna('N/A').value_counts().reset_index()
    # vcs[['Animal Type', 'Count']] = vcs[['index', 'animal_type']]
    # vcs = pd.concat([vcs[vcs.animal_type != 'Other'],
    #                 vcs[vcs.animal_type == 'Other']], ignore_index=True)
    # return px.bar(vcs, x='Animal Type', y='Count')
    return px.histogram(df(row_option), x='animal_type', category_orders=dict(animal_type=['Dog', 'Cat', 'Bird', 'Livestock', 'Other']))


@ app.callback(
    Output('sex_type_graph', 'figure'),
    Input('choose_unique_animals', 'value')
)
def get_sex_type_graph(row_option):
    # vcs = df(row_option).sex.fillna('N/A').value_counts().reset_index()
    # vcs[['Sex', 'Count']] = vcs[['index', 'sex']]
    # vcs = vcs.loc[[0] + list(range(len(vcs)-1, 0, -1))]
    # return px.pie(vcs, names='Sex', values='Count')
    temp = df(row_option).groupby(
        ['sex_upon_outcome', 'sex', 'neutered']).count().reset_index()
    temp['Count'] = temp['name']
    return px.sunburst(temp, path=['sex', 'sex_upon_outcome'], values='Count')


@ app.callback(
    Output('outcome_type_graph', 'figure'),
    Input('choose_unique_animals', 'value')
)
def get_outcome_type_graph(row_option):  # dummy argument
    temp = df(row_option)
    temp['Month'] = temp.datetime.apply(
        lambda t: t.replace(day=1, hour=0, minute=0, second=0))
    print(temp['Month'].value_counts())
    return px.line(temp['Month'].value_counts().sort_index())


@ app.callback(
    Output('event_count_graph', 'figure'),
    Input('choose_unique_animals', 'value')
)
def get_event_count_graph(row_option):  # dummy argument
    temp = df('All Visits')
    temp['Month'] = temp.datetime.apply(
        lambda t: t.replace(day=1, hour=0, minute=0, second=0))
    return px.line(temp['Month'].value_counts().sort_index())


@ app.callback(
    Output('num_visits_graph', 'figure'),
    Input('choose_unique_animals', 'value')
)
def get_num_visits_graph(row_option):  # dummy argument
    temp = df('All Visits')
    return px.bar(temp.animal_id.value_counts().value_counts(), log_y=True)


if __name__ == '__main__':
    app.run_server(debug=True)
