import streamlit as st
import base64
import re
from analyzer import analyze_job_description
import time
from error_handling import handle_openai_errors
# --- Page config ---
st.set_page_config(
    page_title="Call Your Bluff",
    page_icon="call-your-bluff-logo.png",
    layout="centered"
)

# --- Base64 logo encoder ---
def get_base64_logo(path):
    with open(path, "rb") as img_file:
        b64 = base64.b64encode(img_file.read()).decode()
    return f"data:image/png;base64,{b64}"

logo_base64 = get_base64_logo("call-your-bluff-logo.png")

# --- Inject custom CSS ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Poppins:wght@600;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    body {
        background: linear-gradient(to bottom, #0f0f0f, #1a1a1a);
        color: #f5f5f5;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
        color: #ffffff !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.5);
    }

    .block-container {
        padding-top: 4rem;  /* Slightly more top spacing */
        padding-bottom: 4rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    h3:hover {
        color: #f107a3;
        transform: translateY(-2px);
        transition: all 0.3s ease;
        cursor: help;
    }

    .stTextArea textarea {
        background-color: #ffffff;
        color: #1a1a1a;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        border: 1px solid #ccc;
        border-radius: 6px;
    }

    .center-button {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 3rem auto 3rem auto; /* Top and bottom spacing */
    }

    .stButton>button {
        background-color: #f107a3;
        color: #ffffff;
        border: none;
        padding: 1rem 3.5rem; /* Bigger button */
        border-radius: 14px;
        font-size: 1.25rem; /* Larger text */
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3);
    }

    .stButton>button:hover {
        background-color: #c0007e;
        transform: scale(1.08);
        box-shadow: 0 0 15px rgba(241, 7, 163, 0.6);
    }

    @keyframes pulse {
        0%   { box-shadow: 0 0 0 0 rgba(241, 7, 163, 0.6); }
        70%  { box-shadow: 0 0 0 14px rgba(241, 7, 163, 0); }
        100% { box-shadow: 0 0 0 0 rgba(241, 7, 163, 0); }
    }

    footer {
        visibility: hidden;
    }
</style>


""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown(
    f"""
    <div style='text-align: center; margin-top: 2rem; margin-bottom: 2.5rem;'>
        <img src="{logo_base64}" alt="Call Your Bluff Logo" width="220" style="margin-bottom: 1rem;" />
        <h1 style='margin: 0;'>Call Your Bluff</h1>
        <h4 style='margin-top: 0.5rem;'>We don’t work for HR. We work for you.</h4>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Prompt Header ---
st.markdown("""
    <div title='We’ll analyze the job description for vague, manipulative, or exploitative language.' style='margin-top: 2rem; margin-bottom: 1rem;'>
        <h3>🗑️ Is this job trash? Paste the description and find out.</h3>
    </div>
""", unsafe_allow_html=True)

# --- Text Area ---
st.markdown("""
    <label for='job-desc' title='Paste the entire job listing here.' style='font-weight: 500;'>📄 Paste job description below:</label>
""", unsafe_allow_html=True)

job_description = st.text_area("", key="job-desc", height=250)

# --- Placeholder Panel ---
if job_description.strip() == "":
    st.markdown("""
    <div style="margin-top: 3rem; padding: 1rem; background-color: rgba(255,255,255,0.03); border-radius: 10px;">
        <h4>📊 What you'll see after scanning:</h4>
        <ul style="line-height: 1.8;">
            <li>🚩 <b>Red Flags</b> – shady phrases, vague pay, hidden expectations</li>
            <li>💬 <b>Corporate Speak Translations</b> – what the buzzwords actually mean</li>
            <li>🎯 <b>Trash Meter Score</b> – 0 (total trash) to 100 (golden)</li>
            <li>🙋 <b>Smart Questions to Ask</b> – what to ask *before* they waste your time</li>
        </ul>
        <p style="color: #999; font-size: 0.9rem; margin-top: 1rem;">Paste a job description to get started.</p>
    </div>
    """, unsafe_allow_html=True)

# --- Scan Button ---
import time  # Already at the top? Great! If not, add this.

import time  # Ensure this is already at the top
from error_handling import handle_openai_errors  # ✅ Import your handler

# --- Scan Job Button Styling ---
st.markdown("""
<style>
    .stButton>button {
        background-color: #f107a3;
        color: #ffffff;
        border: none;
        padding: 0.9rem 3rem;
        border-radius: 12px;
        font-size: 1.2rem;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2);
    }

    .stButton>button:hover {
        background-color: #c0007e;
        transform: scale(1.05);
        box-shadow: 0 0 10px rgba(241, 7, 163, 0.5);
    }

    @keyframes pulse {
        0%   { box-shadow: 0 0 0 0 rgba(241, 7, 163, 0.6); }
        70%  { box-shadow: 0 0 0 10px rgba(241, 7, 163, 0); }
        100% { box-shadow: 0 0 0 0 rgba(241, 7, 163, 0); }
    }
</style>
""", unsafe_allow_html=True)

# --- Perfectly Centered Button in Its Own Row ---
st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)  # vertical spacing
col1, col2, col3 = st.columns([1, 1, 1])  # truly even spacing
with col2:
    scan_clicked = st.button("Scan Job", key="scan")

# --- Scan Logic ---
if scan_clicked:
    if job_description.strip() == "":
        st.warning("Please paste a job description first.")
    else:
        # --- Progress Bar Simulation ---
        progress_bar = st.progress(0, text="🔍 Scanning for red flags...")
        for percent in range(1, 101):
            time.sleep(0.008)
            progress_bar.progress(percent, text=f"🔍 Scanning... {percent}%")

        try:
            result = analyze_job_description(job_description)

            # --- Extract Score ---
            score_match = re.search(r"Trash Meter Score:\s*(\d+)/100", result)
            score = int(score_match.group(1)) if score_match else None

            # --- Display Score Bubble ---
            if score is not None:
                if score >= 90:
                    color = "#4CAF50"
                    emoji = "🎉"
                    st.balloons()
                elif score >= 50:
                    color = "#FF9800"
                    emoji = "🎯"
                else:
                    color = "#F44336"
                    emoji = "💀"

                st.markdown(f"""
                <div style="text-align:center; margin: 2rem 0;">
                    <div style="display:inline-block; background-color:{color}; color:white; padding: 1.2rem 2rem; border-radius: 100px; font-size: 2rem; font-weight: bold; box-shadow: 0 0 20px rgba(0,0,0,0.3);" title="Score based on clarity, pay transparency, and job stability">
                        {emoji} {score}/100
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # --- Display Analysis ---
            st.markdown(result, unsafe_allow_html=True)

        except Exception as e:
            handle_openai_errors(e)



st.markdown("""
    <hr style="margin-top: 3rem; border: 0.5px solid #ccc;" />
    <style>
        .social-icons a {
            margin: 0 8px;
            display: inline-block;
            transition: transform 0.2s ease, box-shadow 0.3s ease;
        }

        .social-icons img {
            width: 26px;
            height: 26px;
            filter: invert(100%) brightness(120%);
        }

        .social-icons a:hover img {
            transform: scale(1.2);
            filter: drop-shadow(0 0 6px #f107a3);
        }
    </style>

    <div style="text-align: center; font-size: 12px; color: #ddd;">
        <div class="social-icons" style="margin-bottom: 0.7rem;">
            <a href="https://x.com/CYB_app" target="_blank">
                <img src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/x.svg" alt="X">
            </a>
            <a href="https://instagram.com/cyb_app" target="_blank">
                <img src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/instagram.svg" alt="Instagram">
            </a>
            <a href="https://tiktok.com/@call_your_bluff_app_01" target="_blank">
                <img src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/tiktok.svg" alt="TikTok">
            </a>
        </div>
        <p>
            📮 Have feedback about this tool? <a href="mailto:team.callyourbluff@gmail.com" style="color: #fff;">Email our team</a><br>
            Built with 🔍, 😤, and a little machine learning.<br>
            <b style="color: #f107a3;">We don’t work for HR. We work for you.</b><br>
            © 2025 Call Your Bluff
        </p>
    </div>
""", unsafe_allow_html=True)


