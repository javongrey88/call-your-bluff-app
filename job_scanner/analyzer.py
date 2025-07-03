import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_job_description(job_text):
    prompt = f"""
You are a job listing truth detector. A user has submitted the following job description. Return your response in **Markdown** using clear **emojis** and **bold section headers**.

Analyze the listing and return:

🚩 **Red Flags** – suspicious, vague, or toxic phrases  
💬 **Corporate Speak Translations** – decode fluffy buzzwords  
🎯 **Trash Meter Score** – from 0 (pure garbage) to 100 (excellent), with 1-line summary  
🙋 **Smart Questions to Ask** – what to ask during interview to uncover hidden issues

Only return the analysis — no disclaimers or extra fluff.

---
Job Description:
\"\"\"
{job_text}
\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a blunt but helpful career advisor and corporate translator. Format in Markdown with emojis and short sections."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=800
    )

    return response.choices[0].message.content
