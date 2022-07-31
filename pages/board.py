import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime, timedelta
import os
import sys

import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

CWD = os.path.dirname(os.path.abspath(__file__))

original_df = pd.read_csv(os.path.join(CWD, '../data/clean_data.csv'),
                          parse_dates=['date_of_birth', 'datetime'])
original_df = original_df.sort_values(by='datetime', ascending=False)

# dash.register_page(__name__)

layout = html.Div([
    html.H1('Shelter Animal Outcomes'),
    html.Div([
        html.Div(children=[
            html.H4(len(original_df)),
            html.P('distinct records')
        ],
            style={
            "display": "inline-block",
            "width": "25%"
        }),
        html.Div(children=[
            html.H4(len(original_df.animal_id.unique())),
            html.P('distinct animals')
        ], style={
            "display": "inline-block",
            "width": "25%"
        }),
        dcc.RadioItems(
            id='choose_unique_animals',
            options=[
                'All Visits', 'Distinct Animals (Most Recent)', 'Distinct Animals (Oldest)'],
            value='All Visits',
            inline=True,
            style={
                "display": "inline-block",
                "width": "25%"
            },
        ),
        dcc.Checklist(
            id='choose_animal_type',
            options=original_df.animal_type.unique(),
            value=original_df.animal_type.unique(),
            style={
                "display": "inline-block",
                "width": "25%"
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
    dcc.Graph(id='outcome_type_graph'),
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


@ callback(
    Output('event_count_graph', 'figure'),
    Input('choose_unique_animals', 'value')
)
def get_event_count_graph(row_option):  # dummy argument
    temp = df('All Visits')
    temp['Month'] = temp.datetime.apply(
        lambda t: t.replace(day=1, hour=0, minute=0, second=0))
    has_error = True
    while has_error:
        try:
            fig = px.line(temp['Month'].value_counts().sort_index())
            has_error = False
        except ValueError:
            continue
    fig.update_layout(
        title='Number of Visits per Month',
        xaxis_title='Month',
        yaxis_title='Number of Visits'
    )
    return fig


@ callback(
    Output('num_visits_graph', 'figure'),
    Input('choose_unique_animals', 'value')
)
def get_num_visits_graph(row_option):  # dummy argument
    temp = df('All Visits')
    fig = px.bar(temp.animal_id.value_counts().value_counts(),
                 text_auto='.2s')
    fig.update_layout(
        title='Distribution of Number of Visits per Animal',
        xaxis_title='Number of Visits',
        yaxis_title='Number of Animals',
        hovermode='x',
    )
    return fig


@ callback(
    Output('outcome_type_graph', 'figure'),
    Input('choose_unique_animals', 'value')
)
def get_outcome_type_graph(row_option):  # dummy argument
    temp = df('All Visits')
    temp['Month'] = temp.datetime.apply(
        lambda t: t.replace(day=1, hour=0, minute=0, second=0))
    temp['Visit'] = 1
    has_error = True
    while has_error:
        try:
            fig = px.area(
                temp, x='Month', y='Visit', color='outcome_type', line_group='outcome_subtype'
            )
            has_error = False
        except ValueError:
            continue
    fig.update_layout(
        title='Outcome Types per Visits per Month',
        xaxis_title='Month',
        yaxis_title='Number of Visits'
    )
    return fig


@ callback(
    Output('animal_type_graph', 'figure'),
    Input('choose_unique_animals', 'value')
)
def get_animal_type_graph(row_option):
    has_error = True
    while has_error:
        try:
            fig = px.histogram(
                df(row_option), x='animal_type', category_orders=dict(
                    animal_type=['Dog', 'Cat', 'Bird', 'Livestock', 'Other']),
                text_auto='.2s',
            )
            has_error = False
        except ValueError as e:
            continue
    if row_option == 'All Visits':
        fig.update_layout(title='Number of Visits by Animal Type')
    else:
        fig.update_layout(title='Number of Animals by Animal Type')
    fig.update_layout(
        xaxis_title='Animal Type', yaxis_title='Count',
        hovermode='x',
    )
    return fig


@ callback(
    Output('sex_type_graph', 'figure'),
    Input('choose_unique_animals', 'value')
)
def get_sex_type_graph(row_option):
    temp = df(row_option).groupby(
        ['sex_upon_outcome', 'sex', 'neutered']).count().reset_index()
    temp['Count'] = temp['name']
    fig = px.sunburst(temp, path=['sex', 'sex_upon_outcome'], values='Count')
    if row_option == 'All Visits':
        fig.update_layout(
            title='Distribution of Visits by Sex and Neuter Status')
    else:
        fig.update_layout(
            title='Distribution of Animals by Sex and Neuter Status')
    return fig
