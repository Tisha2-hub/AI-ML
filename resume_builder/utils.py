import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import re

# ⚠️ For security: Move your API key to a .env file in production!
genai.configure(api_key="AIzaSyA0bnQ8gX9OZiW_oWVoMzHRq1-TUvB7r-4")


def generate_summary(name, education, experience, skills):
    prompt = f"""
Generate a 4–5 line resume summary for the following candidate.

Name: {name}
Education: {education}
Experience: {experience}
Skills: {", ".join(skills)}

The summary should be professional, formal, and ATS-friendly. Do not include extra titles.
"""
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except ResourceExhausted:
        return f"{name} is a skilled professional with experience in {', '.join(skills)}. They have demonstrated impact across academic and industry projects and are seeking to contribute to data-driven innovation through strong analytical and collaborative skills."
    except Exception as e:
        return f"Error generating summary: {e}"


def calculate_ats_score(resume_text, job_description):
    resume_words = set(re.findall(r"\b\w+\b", resume_text.lower()))
    jd_keywords = set(re.findall(r"\b\w+\b", job_description.lower()))

    matched = resume_words & jd_keywords
    score = round(len(matched) / len(jd_keywords) * 100) if jd_keywords else 0

    missing = sorted(jd_keywords - resume_words)
    return score, sorted(matched), missing


def generate_ats_feedback(resume_text, job_description):
    prompt = f"""
You are an ATS (Applicant Tracking System) and resume evaluator.

Compare the resume and job description below. Return in this format:
1. ATS Match Score (out of 100)
2. Top Matched Keywords (5–10)
3. Missing but Important Keywords (5–10)
4. Resume Improvement Tips (2–3 short lines)

Resume:
{resume_text}

Job Description:
{job_description}
"""

    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Could not generate ATS feedback: {e}"
