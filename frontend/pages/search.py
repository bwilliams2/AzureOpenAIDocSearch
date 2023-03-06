import os

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, html, State
from dash.exceptions import PreventUpdate

import requests

API_URL = os.getenv("API_URL", "")
API_KEY = os.getenv("API_KEY", "")

dash.register_page(__name__, path="/", title="Search", name="Search")

text_input = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Input(
                            id="input", placeholder="Type something...", type="text"
                        ),
                    ],
                    md=7,
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            "Submit",
                            id="submitButton",
                            color="primary",
                            className="me-1",
                        ),
                    ],
                    md=1,
                ),
            ],
            justify="center",
        )
    ]
)

RESULTS_STYLE = {
    "backgroundColor": "rgba(100,100,100,0.5)",
    "minHeight": "80vh",
    "minWidth": "80%",
    "overflowY": "scroll",
    "margin": "8px",
    "padding": "10px",
    "borderRadius": "10px",
}

results = html.Div([html.Div(id="results-container")], style=RESULTS_STYLE)


def layout(document_id=None, **other_unknown_query_strings):
    return html.Div(
        children=[
            html.H1(children="Document Search"),
            text_input,
            results,
        ]
    )


def result_card(res):
    layout = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col([html.P("Image")], xs=2),
                    dbc.Col(
                        [
                            html.H6(res["title"], style={"fontWeight": "bold"}),
                            html.Div("Summary", style={"textDecoration": "underline"}),
                            html.Div(res["summary"]),
                            html.Div(f"Authors: {', '.join(res['authors'])}"),
                            html.Div(
                                f"Keywords: {', '.join(res['keywords'])}",
                                style={"fontStyle": "italic"},
                            ),
                        ]
                    ),
                ]
            )
        ],
        style={"margin": "10px"},
    )
    return layout


@dash.callback(
    Output("store", "data"),
    Input("submitButton", "n_clicks"),
    [State("input", "value"), State("store", "data")],
)
def submit_results(n_clicks, value, data):
    print("new results")
    if data is None:
        data = {}

    if "last_search" not in data:
        data["last_search"] = value
    elif data["last_search"] == value:
        return data

    res = []
    res = requests.get(
        API_URL + "search",
        params={"content": value, "skip": 0, "limit": 15, "apiKey": API_KEY},
    )
    res = res.json()
    data["results"] = res
    print("new results posted")
    return data


@dash.callback(
    Output("results-container", "children"),
    Input("store", "modified_timestamp"),
    State("store", "data"),
)
def create_results(ts, data):
    print("got new results")
    if ts is None:
        print("ts is None")
        raise PreventUpdate
    if data is None:
        data = {}

    if "results" not in data or not isinstance(data["results"], list):
        data["results"] = []

    results = []
    print("Creating results")
    for result in data["results"]:
        results.append(result_card(result))
    return results
