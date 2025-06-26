# app.py
import streamlit as st
from utils.file_handler import extract_text_from_file
from utils.fitment_evaluator import evaluate_fitment
from utils.improvement_suggester import suggest_improvements
import os
from dotenv import load_dotenv
from utils.improvement_suggester import suggest_improvements

load_dotenv(dotenv_path=".env")  # <-- explicitly point to the file in root

os.environ["TOKENIZERS_PARALLELISM"] = "false"
load_dotenv()  # Automatically loads .env from root

st.title("📄 Resume Fitment & Improvement Analyzer")

st.markdown("Upload your **Resume** and **Job Description** to check match and get suggestions.")

resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=['pdf', 'docx'])
jd_file = st.file_uploader("Upload Job Description (PDF/DOCX/TXT)", type=['pdf', 'docx', 'txt'])
jd_text_input = st.text_area("OR Paste Job Description")

use_genai = st.checkbox("🔮 Use GenAI for Suggestions", value=True)

if st.button("Evaluate Fitment") and (resume_file and (jd_file or jd_text_input)):
    resume_text = extract_text_from_file(resume_file)
    jd_text = extract_text_from_file(jd_file) if jd_file else jd_text_input

    st.subheader("✅ Fitment Score")
    score, common_skills = evaluate_fitment(resume_text, jd_text)
    st.metric("Match %", f"{score:.2f}%")
    st.text("Matched Keywords or Skills:")
    st.write(common_skills)

    if use_genai:
        st.subheader("🧠 Resume Improvement Suggestions")
        suggestions = suggest_improvements(resume_text, jd_text)
        st.write(suggestions)
