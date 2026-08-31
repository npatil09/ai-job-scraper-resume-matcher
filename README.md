# AI Job Scraper & Resume Matcher

An AI-powered job matching application that allows users to upload their resume, extracts relevant skills and profile information, fetches real job listings, and ranks jobs based on how well they match the candidate's skills.

## Features

* Upload resumes in PDF format
* Extract text from uploaded resumes
* Identify candidate skills and profile information
* Fetch real job listings from the Himalayas Jobs API
* Filter jobs for internship opportunities
* Match resume skills against job requirements
* Calculate a match score for each job
* Show matched skills and missing skills
* Rank jobs from highest match score to lowest
* Provide direct links to job applications

## How It Works

1. The user uploads a PDF resume.
2. The application extracts text from the PDF using `pypdf`.
3. Resume information and skills are structured into a candidate profile.
4. The application fetches real internship job listings using the Himalayas Jobs API.
5. Relevant skills are extracted from each job description.
6. The resume profile is compared with the job requirements.
7. Each job receives a match score based on matched and missing skills.
8. Jobs are sorted from the highest match score to the lowest.

## Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn

### Resume Processing

* pypdf

### Job Fetching

* Requests
* Himalayas Jobs API

### Frontend

* HTML
* CSS
* JavaScript

## Project Structure

```text
ai-job-matcher/
│
├── backend/
│   ├── main.py
│   ├── job_fetcher.py
│   └── matcher.py
│
├── services/
│   ├── resume_parser.py
│   └── resume_profile.py
│
├── frontend/
│   └── index.html
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

### 1. Clone the repository

```bash
git clone <>
```

### 2. Navigate to the project folder

```bash
cd ai-job-matcher
```

### 3. Create and activate a virtual environment

```bash
python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI server:

```bash
uvicorn backend.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

## API Endpoints

### GET /

Checks whether the API is running.

Example response:

```json
{
  "message": "AI Job Scraper & Resume Matcher API is running"
}
```

### POST /upload-resume

Uploads a PDF resume and performs job matching.

The endpoint:

* Saves the uploaded resume
* Extracts resume text
* Builds a candidate profile
* Fetches real internship job listings
* Matches the resume against job requirements
* Returns ranked job matches

## Example Output

Each matched job includes:

* Job title
* Company name
* Location
* Employment type
* Application link
* Match score
* Matched skills
* Missing skills
* Match explanation

Example:

```text
Machine Learning Engineer
Company: Example Company

Match: 91%

Matched Skills:
Python, Machine Learning, PyTorch, TensorFlow

Missing Skills:
Data Science
```

## API Documentation

FastAPI automatically provides interactive API documentation.

After starting the server, open:

```text
http://127.0.0.1:8000/docs
```

You can upload a PDF resume and test the API directly from the Swagger UI.

## Important Notes

* Currently, only PDF resumes are supported.
* Job matching is primarily based on detected skills.
* The application fetches real job listings through the Himalayas Jobs API.
* Match scores should be considered an approximate indication of skill alignment rather than a complete evaluation of candidate suitability.
* This project is built as an MVP for the Generative AI Developer Intern Build Sprint.

## Future Improvements

* Add semantic matching using embeddings and LLMs
* Improve skill extraction using NLP
* Support DOCX resumes
* Add job filtering by location and role
* Add user preferences for remote and internship opportunities
* Store job history in a database
* Improve match scoring using weighted skill relevance
* Add personalized resume improvement suggestions

## Author

**Nutan Patil**

M.Sc. Computer Science Student
Interested in Machine Learning, Deep Learning, and Computer Vision
