import os
import json

import requests

import dash
from dash import html, State, Input, Output, dcc
from dash.exceptions import PreventUpdate

import dash_bootstrap_components as dbc

dash.register_page(
    __name__, path_template="/qna/<document_id>", title="DocumentQnA", name="QnA"
)

API_URL = os.getenv("API_URL", "")
API_KEY = os.getenv("API_KEY", "")

bubble_styles = {
    "padding": "10px",
    "borderRadius": "10px",
    "margin": "10px",
    "maxWidth": "55%",
    "width": "fit-content",
}


def format_bot_response(text: str):
    return dbc.Row(
        [
            html.Div(
                [text],
                style={"backgroundColor": "white", "color": "black", **bubble_styles},
                class_name="bot",
            )
        ],
        justify="start",
    )


def format_user_input(text: str):
    return dbc.Row(
        [
            html.Div(
                [text],
                style={"backgroundColor": "blue", **bubble_styles},
                class_name="user",
            )
        ],
        justify="end",
    )


def layout(document_id=None):
    return html.Div(
        children=[
            dcc.Location(id="url"),
            html.Div("QnA", style={"textAlign": "center", "fontSize": "30px"}),
            html.Div(
                id="document-info", style={"textAlign": "center", "fontSize": "30px"}
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [],
                                style={
                                    "minHeight": "75vh",
                                    "width": "100%",
                                    "backgroundColor": "gray",
                                    "borderRadius": "10px",
                                    "padding": "10px",
                                },
                                id="chatbox",
                            ),
                        ],
                        xs=10,
                    ),
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Input(
                                                id="chatInput",
                                                placeholder="Type something...",
                                                type="text",
                                            ),
                                        ],
                                        md=9,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Button(
                                                "Submit",
                                                id="submitChatButton",
                                                color="primary",
                                                className="me-1",
                                            ),
                                        ],
                                        md=1,
                                    ),
                                ],
                                justify="center",
                            )
                        ],
                        xs=10,
                        style={"marginTop": "10px"},
                    ),
                ],
                justify="center",
            ),
        ],
        style={"margin": "auto"},
    )


@dash.callback(
    Output("chatbox", "children"),
    [Input("submitChatButton", "n_clicks"), Input("url", "pathname")],
    [
        State("chatInput", "value"),
        State("chatbox", "children"),
    ],
)
def submit_chat(n_clicks, pathname, value, current_children):
    if n_clicks is None or pathname is None:
        raise PreventUpdate

    user_inputs = []
    bot_inputs = []
    for child in current_children:
        div = child["props"]["children"][0]
        if div["props"]["className"] == "user":
            user_inputs.append(div["props"]["children"][0])
        else:
            bot_inputs.append(div["props"]["children"][0])

    document_id = int(pathname.split("/")[-1])
    data = json.dumps(
        {
            "doc_id": document_id,
            "new_input": value,
            "user_inputs": user_inputs,
            "bot_outputs": bot_inputs,
        }
    )

    res = requests.post(API_URL + "qna", data=data)
    print(res.content)

    res = res.json()
    print(res)

    children = []
    for user_input, bot_output in zip(res["user_inputs"], res["bot_outputs"]):
        children += [format_user_input(user_input), format_bot_response(bot_output)]

    return children


@dash.callback(
    Output("document-info", "children"),
    Input("url", "pathname"),
)
def display_document_info(pathname):
    if pathname is None:
        raise PreventUpdate
    document_id = pathname.split("/")[-1]
    return html.Div(
        [
            html.H1("Document Info"),
            html.H2(f"Document ID: {document_id}"),
        ]
    )
