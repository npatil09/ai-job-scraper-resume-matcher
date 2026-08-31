from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from services.resume_parser import extract_resume_text
from services.resume_profile import build_resume_profile

from .job_fetcher import fetch_jobs
from .matcher import calculate_match

import os


app = FastAPI(title="AI Job Scraper & Resume Matcher")


# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Folders
RESUME_FOLDER = "data/resume"
os.makedirs(RESUME_FOLDER, exist_ok=True)


# Skills that the matcher can detect
POSSIBLE_SKILLS = [
    "python",
    "machine learning",
    "deep learning",
    "computer vision",
    "pytorch",
    "tensorflow",
    "scikit-learn",
    "sql",
    "django",
    "fastapi",
    "rag",
    "llm",
    "nlp",
    "generative ai",
    "prompt engineering",
    "qdrant",
    "opencv",
    "mediapipe",
    "data science",
    "artificial intelligence",
]


def extract_job_skills(description):
    """
    Find known skills mentioned in the job description.
    """

    description = description.lower()

    skills = []

    for skill in POSSIBLE_SKILLS:
        if skill in description:
            skills.append(skill)

    return skills


# -----------------------------
# FRONTEND
# -----------------------------

@app.get("/")
def home():
    return FileResponse("frontend/index.html")


# -----------------------------
# RESUME UPLOAD
# -----------------------------

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF resumes are supported."
        }

    file_path = os.path.join(
        RESUME_FOLDER,
        file.filename
    )

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    # Step 1: Extract resume text
    resume_text = extract_resume_text(file_path)

    # Step 2: Build structured resume profile
    profile = build_resume_profile(resume_text)

    # Step 3: Fetch jobs
    jobs = fetch_jobs(
        "machine learning",
        limit=20
    )

    matched_jobs = []

    # Step 4: Match resume against jobs
    for job in jobs:

        job_skills = extract_job_skills(
            job.get("description", "")
        )

        job_for_matching = {
            "title": job.get("title", ""),
            "company": job.get("company", ""),
            "description": job.get("description", ""),
            "skills": job_skills,
        }

        match = calculate_match(
            profile,
            job_for_matching
        )

        matched_jobs.append({
            "title": job.get("title", ""),
            "company": job.get("company", ""),
            "location": job.get("location", []),
            "employment_type": job.get(
                "employment_type",
                ""
            ),
            "application_link": job.get(
                "application_link",
                ""
            ),
            "published": job.get(
                "published",
                ""
            ),
            "match": match,
        })

    # Step 5: Highest match first
    matched_jobs.sort(
        key=lambda x: (
            x["match"]["score"]
            if x["match"]["score"] is not None
            else -1
        ),
        reverse=True,
    )

    return {
        "filename": file.filename,
        "profile": profile,
        "jobs_found": len(matched_jobs),
        "matched_jobs": matched_jobs,
        "text": resume_text,
    }