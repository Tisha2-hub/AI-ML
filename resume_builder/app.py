import streamlit as st
from resume_template import create_pdf
from utils import generate_summary, calculate_ats_score, generate_ats_feedback
from analytics import increment_download_count, get_download_count

st.set_page_config(page_title="AI Resume Builder", layout="centered")
st.title("📄 AI Resume Builder – Gemini + ATS Analyzer")

# Session flags
if "resume_ready" not in st.session_state:
    st.session_state.resume_ready = False
if "download_clicked" not in st.session_state:
    st.session_state.download_clicked = False

# Resume Form
with st.form("resume_form"):
    st.subheader("👤 Personal Information")
    name = st.text_input("Full Name")
    title = st.text_input("Your Title (e.g., Data Analyst / Data Scientist)")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    linkedin = st.text_input("LinkedIn URL")
    github = st.text_input("GitHub URL")

    st.subheader("📝 Resume Content")
    education = st.text_area("Education")
    skills = st.text_area("Skills")
    experience = st.text_area("Experience")
    projects = st.text_area("Projects")
    certifications = st.text_area("Certifications")
    strengths = st.text_area("Strengths")
    languages = st.text_input("Languages")

    submitted = st.form_submit_button("✅ Generate Resume")

# Resume Generation
if submitted:
    st.info("Generating professional summary using Gemini...")
    summary = generate_summary(name, education, experience, skills.split(","))
    st.success("Summary generated!")

    data = {
        "name": name,
        "title": title,
        "phone": phone,
        "email": email,
        "linkedin": linkedin,
        "github": github,
        "education": education,
        "skills": skills,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
        "strengths": strengths,
        "languages": languages,
        "summary": summary
    }

    st.session_state.resume_data = data
    output_path = create_pdf(data)
    st.session_state.resume_ready = True
    st.session_state.resume_path = output_path

# Resume Download
if st.session_state.resume_ready:
    with open(st.session_state.resume_path, "rb") as f:
        if st.download_button("📥 Download Your Resume", data=f, file_name="My_Resume.pdf", mime="application/pdf"):
            st.session_state.download_clicked = True
            increment_download_count()  # Count the download

# ATS Analyzer
if st.session_state.download_clicked:
    st.subheader("📊 ATS Score Analyzer")
    job_description = st.text_area("📌 Paste the Job Description to compare against your resume")

    if job_description and "resume_data" in st.session_state:
        data = st.session_state.resume_data
        resume_text = "\n".join([
            data["summary"], data["education"], data["skills"],
            data["experience"], data["projects"],
            data["certifications"], data["strengths"], data["languages"]
        ])

        score, matched_keywords, missing_keywords = calculate_ats_score(resume_text, job_description)

        st.metric("✅ ATS Match Score", f"{score}%")
        st.progress(score / 100)

        if score >= 80:
            st.success("🎯 Excellent ATS match! Your resume is highly aligned with the job.")
        elif score >= 50:
            st.warning("⚠️ Fair match. Consider adding more relevant keywords from the job description.")
        else:
            st.error("❌ Low match. Add more role-specific skills and experiences.")

        if matched_keywords:
            st.markdown("**✔️ Matched Keywords:**")
            st.write(", ".join(matched_keywords))

        if missing_keywords:
            st.markdown("**⚠️ Missing Keywords:**")
            st.write(", ".join(missing_keywords))

        st.markdown("---")
        st.subheader("🤖 Gemini ATS Feedback")
        feedback = generate_ats_feedback(resume_text, job_description)
        st.markdown(feedback)

# ✅ Show Resume Download Analytics
st.markdown("---")
st.subheader("📈 Resume Download Analytics")
st.metric("Total Resumes Downloaded", get_download_count())
