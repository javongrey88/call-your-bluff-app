import streamlit as st

# Page config
st.set_page_config(page_title="Call Your Bluff", page_icon="🕵️", layout="centered")

# Title and subtitle
st.title("🕵️ Call Your Bluff")
st.subheader("Is this job trash? Paste the description and find out.")

# Input: Job Description
job_description = st.text_area("Paste the job description below:", height=250)

# Button
if st.button("Scan the Job"):
    if job_description.strip() == "":
        st.warning("Please paste a job description first.")
    else:
        st.info("🔍 Scanning job description...")
        # Placeholder for analysis results
        st.write("🚩 **Red Flags:** [Results here]")
        st.write("💬 **Corporate Speak Translated:** [Results here]")
        st.write("🎯 **Trash Meter:** [Score here]")
        st.write("🙋 **Questions to Ask the Employer:** [Suggestions here]")
