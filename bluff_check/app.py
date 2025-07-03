import streamlit as st
import openai
import os
from prompts import valuation_prompt
from dotenv import load_dotenv

# Load OpenAI key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Bluff Check", page_icon="🃏")

st.markdown("<h1 style='text-align: center;'>🃏 Bluff Check</h1>", unsafe_allow_html=True)
st.markdown("**Find out how much your resume is really worth.**")

# Form UI
with st.form("resume_form"):
    resume_text = st.text_area("Paste your resume text here:", height=300)
    job_title = st.text_input("Target Job Title")
    location = st.text_input("Location (City, State)")
    level = st.selectbox("Experience Level", ["Junior", "Mid-level", "Senior", "Executive"])
    submitted = st.form_submit_button("Analyze Resume")

# Run GPT analysis
if submitted and resume_text and job_title and location:
    with st.spinner("Analyzing your resume..."):

        prompt = valuation_prompt(resume_text, job_title, location, level)

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            result = response['choices'][0]['message']['content']
            st.success("✅ Analysis complete!")
            st.markdown(result)

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
else:
    if submitted:
        st.warning("Please fill in all fields.")
