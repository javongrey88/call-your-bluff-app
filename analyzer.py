import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_job_description(job_text):
    prompt = f"""
You are a job listing truth detector. A user has submitted the following job description. Analyze it and return:

🚩 Red Flags - suspicious or vague language  
💬 Corporate Speak Translations - explain what typical buzzwords really mean  
🎯 Trash Meter Score - give a rating from 0 (pure garbage) to 100 (excellent) with a short summary  
🙋 Questions the user should ask in the interview

Job Description:
\"\"\"
{job_text}
\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful career advisor and corporate lingo translator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=800
    )

    return response.choices[0].message.content
