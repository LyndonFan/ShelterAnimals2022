from matplotlib import use
import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime, timedelta
import os
import sys

import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

from app import app
from pages import home, board
from pages.sidebar import CONTENT_STYLE, sidebar


CWD = os.path.dirname(os.path.abspath(__file__))


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
app.config.suppress_callback_exceptions = True


content = html.Div(dash.page_container, id="page-content", style=CONTENT_STYLE)

app.layout = dbc.Container([
    dcc.Location(id="url"),
    sidebar, content
])


@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/index"]:
        return home
    elif pathname == "/board":
        return board
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"This page is not available..."),
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=True)
