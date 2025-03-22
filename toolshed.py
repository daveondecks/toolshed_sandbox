
import streamlit as st
from fpdf import FPDF
import pandas as pd
import os

# Load tool data
tool_data = pd.read_csv("Tools_description.csv")

# PDCA color codes
phase_colors = {
    "Plan": (243, 124, 42),
    "Do": (45, 190, 156),
    "Check": (165, 216, 208),
    "Act": (30, 76, 72)
}

class OneTeamPDF(FPDF):
    def header(self):
        try:
            self.image("resources/oneteam.png", 10, 8, 40)
        except:
            pass
        self.set_font("Arial", "B", 16)
        self.set_text_color(30, 76, 72)
        self.cell(0, 10, "ONE TEAM PDCA Project Report", ln=True, align="C")
        self.ln(10)

    def section_title(self, title):
        self.set_fill_color(*phase_colors["Plan"])
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True, fill=True)
        self.set_text_color(0, 0, 0)

    def section_body(self, text, height=10):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, height, text if text else "_" * 100)

    def tool_table(self, tools_df):
        self.set_font("Arial", "B", 11)
        self.set_fill_color(220, 220, 220)
        self.cell(60, 10, "Tool", border=1, fill=True)
        self.cell(100, 10, "Description", border=1, fill=True)
        self.cell(30, 10, "Phase", border=1, ln=True, fill=True)

        self.set_font("Arial", "", 10)
        for _, row in tools_df.iterrows():
            phase = row["PDCA Category"]
            color = phase_colors.get(phase, (200, 200, 200))
            self.set_fill_color(*color)
            self.cell(60, 10, row["Tool Name"], border=1)
            self.cell(100, 10, row["Tool Description"], border=1)
            self.cell(30, 10, phase, border=1, ln=True, fill=True)

def generate_pdf_report(selected_tools_dict):
    pdf = OneTeamPDF()
    pdf.add_page()

    pdf.section_title("Project Name")
    pdf.section_body(st.session_state.get("project_name", ""))

    pdf.section_title("Project Owner")
    pdf.section_body(st.session_state.get("project_owner", ""))

    pdf.set_font("Arial", "", 11)
    pdf.cell(50, 10, f"Start Date: {st.session_state.get('start_date', '')}", ln=False)
    pdf.cell(80, 10, f"End Date: {st.session_state.get('end_date', '')}", ln=True)

    pdf.section_title("Project Objective")
    pdf.section_body(st.session_state.get("project_objective", ""), height=8)

    pdf.section_title("Milestones")
    pdf.section_body(st.session_state.get("project_milestones", ""), height=8)

    pdf.section_title("Estimated Cost / Projected Savings")
    pdf.section_body(st.session_state.get("project_cost_savings", ""), height=8)

    pdf.section_title("Selected Tools & PDCA Phase")
    rows = []
    for phase, selected_tools in selected_tools_dict.items():
        for tool in selected_tools:
            match = tool_data[(tool_data["Tool Name"] == tool) & (tool_data["PDCA Category"] == phase)]
            if not match.empty:
                rows.append(match.iloc[0])
    if rows:
        pdf.tool_table(pd.DataFrame(rows))

    pdf.section_title("Next Steps / Action Plan")
    pdf.section_body(st.session_state.get("next_steps", ""), height=8)

    path = "generated_oneteam_report.pdf"
    pdf.output(path)
    return path

# Streamlit UI
st.title("📄 Generate ONE TEAM Project Report")

st.text_input("Project Name", key="project_name")
st.text_input("Project Owner", key="project_owner")
st.date_input("Start Date", key="start_date")
st.date_input("End Date", key="end_date")
st.text_area("Project Objective", key="project_objective")
st.text_area("Milestones", key="project_milestones")
st.text_area("Estimated Cost / Projected Savings", key="project_cost_savings")
st.text_area("Next Steps / Action Plan", key="next_steps")

if "selected_tools" not in st.session_state:
    st.session_state.selected_tools = {
        "Plan": [],
        "Do": [],
        "Check": [],
        "Act": []
    }

if st.button("📄 Generate Report"):
    pdf_path = generate_pdf_report(st.session_state.selected_tools)
    st.success("✅ Report generated!")
    with open(pdf_path, "rb") as f:
        st.download_button("⬇️ Download Report", f, file_name="ONE_TEAM_Report.pdf")
