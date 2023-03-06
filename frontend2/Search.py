import streamlit as st
import os
import pandas as pd
import numpy as np
import time
import requests
from utils import load_css

backend_url = os.getenv("AZURE_FUNCTION_URL")
backend_key = os.getenv("AZURE_FUNCTION_KEY")



def submit_search(search_value):
    st.session_state["results"] = []
    requests

def download_file(blob_path):
    print(f"Downloading {blob_path}")
    return

if 'results' not in st.session_state:
    st.session_state["results"] = [
        {"title": "Sample Document Title", "summary": "Summary of doc", "blobPath": ""},
        {"title": "2nd Sample Document Title", "summary": "2nd Summary of doc", "blobPath":""}
    ]


st.title('OpenAI Document Search')
selected = st.text_input("", "Search...")
button_clicked = st.button("OK")

if button_clicked: # Make button a condition.
    st.write(f"Search submitted with: {selected}")

st.write("RESULTS")

for result in st.session_state["results"]:
    with st.container():
        st.write(result["title"])
        col1, col2, col3 = st.columns([1,3,1])
        col1.write("Doc Thumbnail")
        col2.write(result["summary"])
        with col3:
            st.button("Download", key=result["title"], on_click=download_file, args=(result["blobPath"]))


