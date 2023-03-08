import os

import dash
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
from dash import Input, Output, html, State, MATCH, dcc, ctx
import requests

from dash.exceptions import PreventUpdate

try:
    # Attempt dev env load
    load_dotenv("../dev.env")
except:
    pass

API_URL = os.getenv("API_URL", "")
API_KEY = os.getenv("API_KEY", "")

app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY], use_pages=True)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    # "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "marginLeft": "18rem",
    "marginRight": "2rem",
    "padding": "2rem 1rem",
}


app.layout = html.Div(
    [
        dcc.Store(id="store", storage_type="session"),
        html.Div(
            [
                html.H2("Sidebar", className="display-4"),
                html.Hr(),
                dbc.Nav(
                    [
                        dbc.NavLink(f"{page['name']}", href=page["relative_path"])
                        for page in dash.page_registry.values()
                    ],
                    vertical=True,
                    pills=True,
                ),
            ],
            style=SIDEBAR_STYLE,
        ),
        html.Div(dash.page_container, style=CONTENT_STYLE),
    ],
)
app.config.suppress_callback_exceptions = True


if __name__ == "__main__":
    app.run_server(port=8888)
