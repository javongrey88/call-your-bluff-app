import openai
import streamlit as st

def handle_openai_errors(e):
    if isinstance(e, openai.error.APIConnectionError):
        st.error("🔌 Connection error. Please check your internet and try again.")
    elif isinstance(e, openai.error.Timeout):
        st.error("⏳ The request timed out. Try again in a few seconds.")
    elif isinstance(e, openai.error.RateLimitError):
        st.error("🚫 Too many requests. You’ve hit the limit. Try again shortly.")
    elif isinstance(e, openai.error.AuthenticationError):
        st.error("🔐 Authentication failed. Check your API key.")
    elif isinstance(e, openai.error.APIError):
        st.error("🚨 OpenAI API returned an error. Please try again.")
    elif isinstance(e, openai.error.InvalidRequestError):
        st.error("❗Invalid request. Check the format of your prompt or data.")
    else:
        st.error(f"⚠️ Unexpected error: {str(e)}")
