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
    html.H1('This is the home page')
])
