from streamlit.components.v1 import html
import streamlit as st
from utils import load_css
from pathlib import Path

st.title('Document QnA')
css_path = Path(__file__).parent.joinpath("styles.css").absolute()
load_css(css_path)

inner_text = """
<div class="chatbox">
    <div class="bot">
        <div class="bubble">
        <p>This is a bot response</p>
        </div>
    </div>
    <div class="user">
        <div class="bubble">
        <p>This is an input. with a very long input sdfiojqpefn;lk asndklp jfkljek d c askpjfeu asjfooe slsadfkjlep djasdpfpoe jasdlf;j</p>
        </div>
    </div>
</div>
"""

st.markdown(inner_text, unsafe_allow_html=True)
chat_input = st.text_input("", "Document Question")
if "chat_input" not in st.session_state:
    st.session_state["chat_input"] = ""

button_clicked = st.button("Submit")
if button_clicked or (st.session_state["chat_input"] != chat_input):
    st.session_state["chat_input"] = chat_input
    # Display search results for user_query
