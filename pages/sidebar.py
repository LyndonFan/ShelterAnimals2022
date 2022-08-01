# Code is based on similar work by bilative on github
# see their original work here:
# https://github.com/bilative/Summer-Community-App-Challenge-DASH

import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    << << << < HEAD
    "width": "18rem",
    == == == =
    "width": "16rem",
    >>>>>> > 5a77d4a942fe0273b95ed62816d44c356a166a9e
    "padding": "2rem 1rem",
    "background-color": "#111111",
    "color": "#C8C8C8"
}


CONTENT_STYLE = {
    "margin-left": "16.5rem",
    "margin-right": "0.5rem",
    "padding": "1rem 0.5rem",
    "bacground-color": "black"
}


pageList = ['home', 'board']


sidebar = html.Div(
    [
        html.H3("Shelter Animal Outcomes", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home",
                            href="/home", id="home-link"),
                dbc.NavLink("Board",
                            href="/board", id="board-link"),
            ],
            vertical=True,
            pills=True,
        )
    ],
    style=SIDEBAR_STYLE,
)
