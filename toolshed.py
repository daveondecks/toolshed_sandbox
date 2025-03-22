import streamlit as st
import pandas as pd
import io
from PIL import Image
# Set wide layout
st.set_page_config(page_title="PDCA Toolshed", layout="wide")

# === ONE TEAM color palette styles ===
st.markdown("""
    <style>
        h1, h2, h3 {
            color: #1E4C48;
        }

        .stButton > button {
            border: none;
            border-radius: 8px;
            padding: 0.6em 1.4em;
            font-weight: bold;
            font-size: 16px;
        }

        div[data-testid="stHorizontalBlock"] > div:nth-child(1) button { background-color: #F37C2A; color: white; }
        div[data-testid="stHorizontalBlock"] > div:nth-child(2) button { background-color: #2DBE9C; color: white; }
        div[data-testid="stHorizontalBlock"] > div:nth-child(3) button { background-color: #A5D8D0; color: #1E4C48; }
        div[data-testid="stHorizontalBlock"] > div:nth-child(4) button { background-color: #1E4C48; color: white; }
    </style>
""", unsafe_allow_html=True)


# Display ONE TEAM logo at top of sidebar
with st.sidebar:
    logo = Image.open("resources/oneteam.png")
    st.image(logo, use_container_width=True)

import xlsxwriter
from datetime import date


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

# ✅ Sidebar: Project Details & PDCA Selection
st.sidebar.title("Project Details")

# ✅ Store Project Name & Owner in session state
if "project_name" not in st.session_state:
    st.session_state["project_name"] = ""

if "project_owner" not in st.session_state:
    st.session_state["project_owner"] = ""

# ✅ Save inputs to session state (NO DUPLICATE `text_input`)
st.session_state["project_name"] = st.sidebar.text_input("Project Name", value=st.session_state["project_name"])
st.session_state["project_owner"] = st.sidebar.text_input("Project Owner", value=st.session_state["project_owner"])
# ✅ Store created date
if "created_date" not in st.session_state:
    st.session_state["created_date"] = date.today().strftime("%d-%m-%Y")
created_date = st.session_state["created_date"]

st.sidebar.markdown("---")  # separator line
st.sidebar.header("Select Tools for PDCA Phases")

# ✅ Ensure session state is initialized properly
if "selected_tools" not in st.session_state:
    st.session_state.selected_tools = {
        "Plan": [],
        "Do": [],
        "Check": [],
        "Act": []
    }

# ✅ Unified PDCA Selection (Used in Both Toolshed & Project Plan Tabs)
for phase in ["Plan", "Do", "Check", "Act"]:
    selected_temp = st.sidebar.multiselect(
        f"{phase} Tools:",
        options=tool_data[tool_data['PDCA Category'] == phase]['Tool Name'].tolist(),
        default=st.session_state.selected_tools.get(phase, [])
    )

    # ✅ Update session state if selection changes
    if selected_temp != st.session_state.selected_tools[phase]:
        st.session_state.selected_tools[phase] = selected_temp

# ✅ Define PDCA colors (matching your screenshot)
pdca_colors = {
    "Plan": "#FFD700",  # Gold Yellow
    "Do": "#32CD32",    # Green
    "Check": "#1E90FF", # Blue
    "Act": "#FF4500"    # Red
}

# ✅ Main Tabs
st.title("🧰 One Team Continuous Improvement Toolshed")
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🛠️ Toolshed", "📖 Tool Dictionary", "📹 Video Library", "🗂 Project Plan", 
    "📂 Repository", "📊 Analytics", "💬 Discussion", "📝 Feedback"
])

# === Toolshed Tab ===
with tab1:
    st.subheader("Toolshed")
    st.write("Select tools from each PDCA phase in the sidebar. They will appear in the corresponding toolbox below:")

    # ✅ Retrieve selected tools from session state
    selected_tools = st.session_state.selected_tools

    # ✅ Create PDCA toolboxes with colors
    toolbox_cols = st.columns(4)
    for idx, phase in enumerate(["Plan", "Do", "Check", "Act"]):
        with toolbox_cols[idx]:
            tools = selected_tools[phase]
            box_color = pdca_colors[phase]  

            # ✅ Render PDCA-colored Toolbox Header
            st.markdown(f"""
            <div style="
                background-color: {box_color}; 
                padding: 15px; 
                border-radius: 10px; 
                text-align: center; 
                color: white; 
                font-weight: bold;">
                {phase} Toolbox
            </div>
            """, unsafe_allow_html=True)

            # ✅ Display selected tools
            if not tools:
                st.markdown(f"""
                <div style="
                    background-color: #F1F1F1; 
                    padding: 10px; 
                    border-radius: 5px;
                    text-align: center;
                    margin-top: 5px;
                    color: black;">
                    No tools selected
                </div>
                """, unsafe_allow_html=True)
            else:
                toolbox_html = f"""
                <div style="
                    background-color: white;
                    border: 2px solid {box_color};
                    border-radius: 10px;
                    padding: 10px;
                    margin-top: 5px;
                ">
                <ul style="list-style-type: none; padding: 0;">
                """
                for tool in tools:
                    toolbox_html += f'<li style="padding: 5px; border-bottom: 1px solid {box_color};">✅ {tool}</li>'
                toolbox_html += "</ul></div>"

                st.markdown(toolbox_html, unsafe_allow_html=True)

# === Tool Dictionary Tab ===
with tab2:
    st.subheader("Tool Dictionary")
    
    # Search box
    query = st.text_input("🔍 Search tools:", "")

    # ✅ Case-insensitive filtering
    if query:
        mask = tool_data['Tool Name'].str.contains(query, case=False, na=False) | tool_data['Description'].str.contains(query, case=False, na=False)
        filtered_data = tool_data[mask].copy()
    else:
        filtered_data = tool_data.copy()

    # ✅ Convert 'Tool Name' into clickable links
    if 'More Info' in filtered_data.columns:
        filtered_data['Tool Name'] = filtered_data.apply(
            lambda row: f"<a href='{row['More Info']}' target='_blank'>{row['Tool Name']}</a>" 
                        if pd.notna(row['More Info']) and str(row['More Info']).strip() != "" 
                        else row['Tool Name'],
            axis=1
        )

    # ✅ Display table with same width as the search box
    dict_display = filtered_data[['PDCA Category', 'Tool Name', 'Description']].copy()
    dict_display.rename(columns={'PDCA Category': 'Phase'}, inplace=True)

    if dict_display.empty:
        st.warning("⚠️ No tools found. Try a different search term.")
    else:
        st.container()  # Wrap table inside a container
        st.dataframe(dict_display, use_container_width=True)

# === Video Library Tab ===
with tab3:
    st.subheader("🎥 Video Library - Work in Progress 🚧")
    
    # Work in Progress message with an icon
    st.markdown(
        """
        🚀 **Coming Soon!** This is where you will be able to **upload a short video of your project**.  
        
        🎯 **What to Include in Your Video:**
        - 🎬 A brief **introduction to your project**  
        - 🛠️ The **PDCA tools** you used  
        - 📊 **How successful it was** and **what you learned**  
        - 💡 **Tips for others** who may want to try similar tools  

        🔍 You will also be able to **search videos by PDCA category and keyword**.  

        🏗️ **Just watch this space!** 🎥
        """,
        unsafe_allow_html=True
    )
    # === Project Plan Tab ===
with tab4:
    st.subheader("Project Plan")

    # ✅ Retrieve project details from session state
    project_name = st.session_state["project_name"]
    project_owner = st.session_state["project_owner"]
    created_date = st.session_state.get("created_date", date.today().strftime("%d-%m-%Y"))

    # ✅ Display Project Details
    st.markdown(f"**Project Name:** {project_name} &nbsp;&nbsp; **Owner:** {project_owner} &nbsp;&nbsp; **Created:** {created_date}", unsafe_allow_html=True)
    st.write("")  # Empty line for spacing

    # ✅ Introductory text for the project plan table
    st.write("The table below outlines the selected tools as tasks in your PDCA project plan.")

    # ✅ Add missing tool descriptions
    all_tasks = []
    for phase in ["Plan", "Do", "Check", "Act"]:
        for tool in st.session_state.selected_tools[phase]:
            desc = tool_data.loc[tool_data["Tool Name"] == tool, "Description"].values
            desc_text = desc[0] if len(desc) > 0 else ""
            all_tasks.append({"PDCA Phase": phase, "Task Name": tool, "Description": desc_text})

    project_plan_df = pd.DataFrame(all_tasks)

    # ✅ Display project plan table
    st.dataframe(project_plan_df, use_container_width=True)

    # ✅ Download buttons
    st.markdown("**Download Project Plan:**")
    dcol1, dcol2, dcol3, dcol4 = st.columns(4)

    # ✅ CSV Download
    csv_data = project_plan_df.to_csv(index=False, encoding='utf-8-sig')
    dcol1.download_button("Download CSV", data=csv_data, file_name="Project_Plan.csv", mime="text/csv")
    # ✅ TXT Download
    text_data = project_plan_df.to_csv(index=False, sep='\t')
    dcol3.download_button("Download TXT", data=text_data, file_name="Project_Plan.txt", mime="text/plain")

    # ✅ Excel Download using `xlsxwriter`
try:
    excel_output = io.BytesIO()
    with pd.ExcelWriter(excel_output, engine='xlsxwriter') as writer:
        project_plan_df.to_excel(writer, index=False, sheet_name="Project Plan")
        excel_data = excel_output.getvalue()
    dcol2.download_button("Download Excel", data=excel_data, file_name="Project_Plan.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
except Exception as e:
        dcol2.write("⚠️ Excel export not available")
    
try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

if FPDF is not None:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ✅ Title Section
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Project Plan - {st.session_state.get('project_name', 'Untitled')}", ln=1, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Owner: {st.session_state.get('project_owner', 'N/A')}    Created: {st.session_state.get('created_date', 'N/A')}", ln=1, align='C')
    pdf.ln(10)

    # ✅ Write tasks to PDF
    if not project_plan_df.empty:
        for _, row in project_plan_df.iterrows():
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 8, f"{row['PDCA Phase']} Phase", ln=1)
            pdf.set_font("Arial", '', 12)

            # ✅ Handle encoding issues
            task_name = row['Task Name'] if row['Task Name'] else "Unnamed Task"
            description = row['Description'] if row['Description'] else "No Description Available"

            def clean_text(text):
                return ''.join(c for c in text if ord(c) < 128)  # Keep only ASCII characters

            task_name = clean_text(task_name)
            description = clean_text(description)

            pdf.cell(0, 6, f"{task_name} - {description}", ln=1)
            pdf.cell(0, 6, "Start Date: ______    Completion Date: ______", ln=1)
            pdf.ln(4)

    else:
        pdf.set_font("Arial", 'I', 12)
        pdf.cell(0, 10, "No tasks selected for this project plan.", ln=1, align='C')

    # ✅ Generate PDF Download Button
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    dcol4.download_button("Download PDF", data=pdf_bytes, file_name="Project_Plan.pdf", mime="application/pdf")

else:
    dcol4.write("⚠️ PDF export not available (FPDF not installed)")

    import streamlit as st
from PIL import Image

# === Repository ===
with tab5:
    # Tab 5: Repository
    st.title("📂 CI Repository (Coming Soon)")
    st.write("Upload and share useful CI files and presentations with other users.")
    st.info("This feature is a work in progress and will be available soon!")

# === Analytics ===
with tab6:
# Tab 6: Analytics
    st.title("📊 Analytics (Coming Soon)")
    st.write("Track tool usage, analyze effectiveness, and get recommendations based on ML models.")
    st.info("Future updates will include graphs and AI-driven recommendations!")


# === Discussion ===
with tab7:
# Tab 7: Discussions
    st.title("💬 CI Discussions")
    st.write("A searchable forum for discussing CI tools, sharing tips, successes, and learning from failures.")
    st.text_input("Search discussions...")
    st.info("Start a new discussion or browse existing conversations.")

# === Feedback ===
with tab8:
# Tab 8: Feedback
    st.title("📝 Toolshed Feedback")
    st.write("Share your thoughts on the Toolshed app! What do you like? What can be improved?")
    st.text_area("Your feedback here...")
    st.button("Submit Feedback")