
import streamlit as st
import pandas as pd
import io
import xlsxwriter
from datetime import date
from PIL import Image

# Set wide layout with custom page title
st.set_page_config(page_title="PDCA Toolshed – ONE TEAM", layout="wide")

# ✅ Custom styling for ONE TEAM theme
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            background-color: #FDFDFD;
        }
        .sidebar .sidebar-content {
            background-color: #D6EEE7;
        }
        .stButton > button {
            background-color: #2DBE9C;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5em 1em;
        }
        h1, h2, h3 {
            color: #F37C2A;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ Load tool data
@st.cache_data
def load_data():
    try:
        return pd.read_csv("Data/Tools_description.csv")
    except FileNotFoundError:
        return pd.read_csv("Tools_description.csv")

tool_data = load_data()

# ✅ Fix column names
tool_data = tool_data.rename(columns={
    "Unnamed: 3": "More Info",
    "Unnamed: 4": "Video1",
    "Unnamed: 5": "Video2",
    "Unnamed: 6": "Video3"
})

# ✅ Sidebar: Logo, Project Details & PDCA Selection
with st.sidebar:
    logo = Image.open("resources/oneteam.png")
    st.image(logo, width=180)
    st.markdown("### John Lewis Distribution")
    st.markdown("#### ONE TEAM Project Hub")
    st.markdown("---")

    # Store Project Name & Owner in session state
    if "project_name" not in st.session_state:
        st.session_state["project_name"] = ""

    if "project_owner" not in st.session_state:
        st.session_state["project_owner"] = ""

    st.session_state["project_name"] = st.text_input("Project Name", st.session_state["project_name"])
    st.session_state["project_owner"] = st.text_input("Project Owner", st.session_state["project_owner"])

# ✅ Main Header
st.image("resources/oneteam.png", width=200)
st.markdown("## ONE TEAM PDCA Toolshed")

# (Continue your app logic here)
