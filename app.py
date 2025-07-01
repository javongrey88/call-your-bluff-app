import streamlit as st
from analyzer import analyze_job_description

# Page config
st.set_page_config(page_title="Call Your Bluff", page_icon="🕵️", layout="centered")

# Title and subtitle
st.title("🕵️ Call Your Bluff")
st.subheader("Is this job trash? Paste the description and find out.")

# Input: Job Description
job_description = st.text_area("Paste the job description below:", height=250)

# Scan Button
if st.button("Scan the Job"):
    if job_description.strip() == "":
        st.warning("Please paste a job description first.")
    else:
        with st.spinner("🔍 Scanning job description..."):
            try:
                result = analyze_job_description(job_description)
                st.markdown(result)
            except Exception as e:
                st.error(f"❌ Error: {e}")
