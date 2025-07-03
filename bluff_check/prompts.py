def valuation_prompt(resume, job_title, location, level):
    return f"""
Act as a professional resume and job market analyst.

Analyze the resume below and perform the following:

1. Estimate a realistic market salary range in USD for 2024.
2. Score the resume from 1 to 10 based on competitiveness in the applicant pool.
3. List 3 strengths and 3 weaknesses in the resume.
4. Explain how formatting, keyword usage, and clarity affect its performance in applicant tracking systems.

Factors: Job Title: {job_title} | Location: {location} | Experience Level: {level}

Resume:
\"\"\"
{resume}
\"\"\"
"""
