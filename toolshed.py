
import streamlit as st
import pandas as pd
import io
import xlsxwriter
from datetime import date
from PIL import Image

# ========================
# ✅ Page Setup & Styling
# ========================
st.set_page_config(page_title="ONE TEAM Continuous Improvement Toolshed", layout="wide")

# ✅ Inject ONE TEAM Styles
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
        }
        .stButton > button {
            background-color: #2DBE9C;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5em 1em;
        }
        h1, h2 {
            color: #F37C2A;
        }
    </style>
""", unsafe_allow_html=True)

# ✅ Load tool data
@st.cache_data
def load_data():
    try:
        return pd.read_csv("Data/Tools_description.csv")
    except FileNotFoundError:
        return pd.read_csv("Tools_description.csv")

tool_data = load_data()
tool_data = tool_data.rename(columns={
    "Unnamed: 3": "More Info",
    "Unnamed: 4": "Video1",
    "Unnamed: 5": "Video2",
    "Unnamed: 6": "Video3"
})

# ========================
# ✅ Sidebar: Logo + Inputs
# ========================
with st.sidebar:
    logo = Image.open("resources/oneteam.png")
    st.image(logo, width=180)
    st.markdown("### John Lewis Distribution")
    st.markdown("#### ONE TEAM Project Hub")
    st.markdown("---")

    st.markdown("### Project Details")
    st.session_state['project_name'] = st.text_input("Project Name")
    st.session_state['project_owner'] = st.text_input("Project Owner")

    st.markdown("### Select Tools for PDCA Phases")
    plan_tool = st.selectbox("Plan Tools:", tool_data['Tool'].dropna().unique())
    do_tool = st.selectbox("Do Tools:", tool_data['Tool'].dropna().unique())
    check_tool = st.selectbox("Check Tools:", tool_data['Tool'].dropna().unique())
    act_tool = st.selectbox("Act Tools:", tool_data['Tool'].dropna().unique())

# ========================
# ✅ Main Page Header
# ========================
st.image("resources/oneteam.png", width=200)
st.markdown("## One Team Continuous Improvement Toolshed")
st.markdown("---")
st.markdown("Select tools from each PDCA phase in the sidebar. They will appear in the corresponding toolbox below:")

# ========================
# ✅ Display Selected Tools
# ========================
def show_toolbox(phase, tool_name, bg_color):
    st.markdown(
        f"<div style='background-color:{bg_color};padding:10px 15px;border-radius:5px;'>"
        f"<h3 style='color:white;margin:0;'>{phase} Toolbox</h3></div>",
        unsafe_allow_html=True
    )
    if tool_name:
        tool_row = tool_data[tool_data['Tool'] == tool_name]
        if not tool_row.empty:
            st.markdown(f"**{tool_name}**")
            st.write(tool_row['Description'].values[0])
        else:
            st.write("Tool not found.")
    else:
        st.write("No tools selected")

show_toolbox("Plan", plan_tool, "#F4C542")
show_toolbox("Do", do_tool, "#2DBE9C")
show_toolbox("Check", check_tool, "#2A75F3")
show_toolbox("Act", act_tool, "#F3413D")
