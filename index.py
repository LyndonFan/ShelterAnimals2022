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

app.config.suppress_callback_exceptions = True


app.config.suppress_callback_exceptions = True
content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = dbc.Container([
    dcc.Location(id="url"),
    sidebar, content
])


@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def render_page_content(pathname):


<< << << < HEAD
    if pathname in ["/", "/home"]:
        return home.layout
    elif pathname == "/board":
        return board.layout
    return dbc.Container(
== == == =
    if pathname in ["/", "/index"]:
        return home
    elif pathname == "/board":
        return board
    return dbc.Jumbotron(
>>>>>> > 5a77d4a942fe0273b95ed62816d44c356a166a9e
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"This page is not available..."),
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=True)
