import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from Resume_parser import extract_text, clean_text
from Skill_extractor import load_skill_dictionary, extract_skills, flatten_skills
from Job_matcher import load_job_roles, rank_roles, check_role_skills
from Roadmap_generator import build_roadmap

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "5"))


def build_report(file_name, skills_by_category, ranked, target, roadmap):
    """Put the analysis into a plain text report the user can download."""
    lines = []
    lines.append("AI RESUME ANALYSIS REPORT")
    lines.append("=" * 40)
    lines.append(f"Resume: {file_name}")
    lines.append("")

    lines.append("SKILLS FOUND")
    if skills_by_category:
        for category, skills in skills_by_category.items():
            lines.append(f"- {category}: {', '.join(skills)}")
    else:
        lines.append("- None of the skills in our list were found.")
    lines.append("")

    lines.append("TOP 3 RECOMMENDED ROLES")
    for number, result in enumerate(ranked[:3], start=1):
        lines.append(f"{number}. {result['role']} - {round(result['score'])}%")
    lines.append("")

    lines.append(f"TARGET ROLE: {target['role']} ({round(target['score'])}% match)")
    lines.append(f"Skills found:   {', '.join(target['matched']) or 'None'}")
    lines.append(f"Skills missing: {', '.join(target['missing']) or 'None'}")
    lines.append("")

    lines.append("LEARNING ROADMAP")
    for step in roadmap:
        lines.append(f"- {step}")
    lines.append("")

    lines.append("Note: match scores are estimates to guide learning. They are not hiring")
    lines.append("decisions, and a missing keyword does not always mean a missing ability.")
    return "\n".join(lines)


#  page setup
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")
st.title("📄 AI Resume Analyzer & Job Recommendation System")
st.caption("Upload your resume, see which job roles fit it best, and get a simple plan to close your skill gaps.")
st.info(" Your resume is read in memory and is not stored.")

#load data
skill_list = load_skill_dictionary()
roles = load_job_roles()

known_skills = [item["skill"] for item in skill_list]
problems = check_role_skills(roles, known_skills)
if problems:
    st.warning("These role skills are not in Data/Skill_dictionary.csv, so they can never be matched: "
               + "; ".join(problems))

#upload
uploaded = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded is None:
    st.write("Upload a resume above to get started.")
    st.stop()

st.write(f"Uploaded file: **{uploaded.name}**")

if uploaded.size > MAX_FILE_SIZE_MB * 1024 * 1024:
    st.error(f"This file is larger than {MAX_FILE_SIZE_MB} MB. Please upload a smaller one.")
    st.stop()

#analyse
try:
    raw_text = extract_text(uploaded)
except Exception:
    st.error("Sorry, this file could not be read. Please try another PDF or DOCX.")
    st.stop()

if not raw_text.strip():
    st.error("No text was found in this file. If it is a scanned image, "
             "please upload a text-based PDF or a DOCX instead.")
    st.stop()

cleaned_text = clean_text(raw_text)
skills_by_category = extract_skills(cleaned_text, skill_list)
resume_skills = flatten_skills(skills_by_category)
ranked = rank_roles(resume_skills, roles)

#  1. skills
st.header("1. Skills found in your resume")
st.metric("Skills detected", len(resume_skills))

if skills_by_category:
    for category, skills in skills_by_category.items():
        st.markdown(f"**{category}:** {', '.join(skills)}")
else:
    st.warning("None of the skills in our list were found. Check that the resume has a skills section, "
               "or add more skills to Data/Skill_dictionary.csv.")

#  2. roles
st.header("2. Recommended job roles")

top_rows = []
for result in ranked[:3]:
    total = len(result["matched"]) + len(result["missing"])
    top_rows.append({
        "Job role": result["role"],
        "Match score": f"{round(result['score'])}%",
        "Skills matched": f"{len(result['matched'])} of {total}",
    })
st.table(pd.DataFrame(top_rows, index=range(1, len(top_rows) + 1)))

st.subheader("Match score for every role")
chart_data = pd.DataFrame(
    {"Match score (%)": [round(result["score"]) for result in ranked]},
    index=[result["role"] for result in ranked],
)
st.bar_chart(chart_data)

# 3. skill gap
st.header("3. Skill gap and learning roadmap")

role_names = [result["role"] for result in ranked]      # best match comes first
chosen_name = st.selectbox("Choose a target role", role_names)
target = next(result for result in ranked if result["role"] == chosen_name)

st.metric(f"Match score for {target['role']}", f"{round(target['score'])}%")

left, right = st.columns(2)
with left:
    st.subheader("✅ Skills you already have")
    st.write(", ".join(target["matched"]) if target["matched"] else "None of the required skills were found.")
with right:
    st.subheader("⚠️ Missing or weak skills")
    st.write(", ".join(target["missing"]) if target["missing"] else "You have all the required skills.")

st.subheader("🗺️ Suggested learning roadmap")
roadmap = build_roadmap(target["missing"])
for step in roadmap:
    st.markdown(f"- {step}")

# 4. report
st.header("4. Download your report")
report_text = build_report(uploaded.name, skills_by_category, ranked, target, roadmap)
st.download_button("Download analysis report (.txt)", data=report_text,
                   file_name="resume_analysis_report.txt", mime="text/plain")

st.caption("A missing keyword does not always mean a missing ability - the tool only checks the "
           "words written in the resume.")
