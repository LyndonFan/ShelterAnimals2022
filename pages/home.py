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


layout = html.Div([
    html.H1('Shelter Animal Outcomes'),
    html.Hr(),
    html.Div([
        html.P('This is a crude dashboard for the '),
        html.A('Austin Animal Center Shelter Outcomes dataset',
               href='https://www.kaggle.com/datasets/aaronschlegel/austin-animal-center-shelter-outcomes-and?select=aac_shelter_cat_outcome_eng.csv'),
        html.P('. Its features are limited but hopefully there will be more pages!')
    ]),
])
