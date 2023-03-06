import dash
from dash import html

dash.register_page(__name__, path="/qna", title="DocumentQnA", name="QnA")


def layout(document_id=None, **other_unknown_query_strings):
    return html.Div(
        children=[
            html.H1(children="This is our Archive page"),
            html.Div(
                children=f"""
	        This is report: {document_id}.
	    """
            ),
        ]
    )
