import streamlit as st
import os
import pandas as pd
import numpy as np
import time
import requests
backend_url = os.getenv("AZURE_FUNCTION_URL")
backend_key = os.getenv("AZURE_FUNCTION_KEY")


def submit_search(search_value):
    st.session_state["results"] = []
    requests
    


if 'results' not in st.session_state:
    st.session_state['results'] = []

st.title('OpenAI Document Search')

selected = st.text_input("", "Search...")
button_clicked = st.button("OK")

if button_clicked: # Make button a condition.
    st.write(f"Search submitted with: {selected}")