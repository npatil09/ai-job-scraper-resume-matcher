from matcher import calculate_match
from job_fetcher import fetch_jobs


resume_profile = {
    "skills": [
        "Python",
        "C++",
        "SQL",
        "PyTorch",
        "TensorFlow",
        "scikit-learn",
        "NumPy",
        "Pandas",
        "OpenCV",
        "MediaPipe",
        "FastAPI",
        "Django",
        "RAG",
        "Qdrant",
        "sentence-transformers",
        "Machine Learning",
        "Computer Vision",
        "Federated Learning",
        "Differential Privacy"
    ],

    "projects": """
    ClaimTrace - RAG-Based Claim Verification Engine

    Built a RAG pipeline from scratch using FastAPI,
    ingestion, embedding, retrieval and answer synthesis.

    The system retrieves both supporting and opposing evidence
    for a claim and flags contradictions across the corpus.

    Embeddings use sentence-transformers MiniLM and Qdrant
    as the vector store.

    The system also uses LLM-based answer synthesis,
    confidence scoring and prompt engineering.

    Federated Learning with Differential Privacy

    Implemented FedAvg from scratch using NumPy and
    scikit-learn.

    Ran experiments examining privacy-accuracy tradeoffs
    across different privacy budgets.
    """,

    "experience": """
    Full Stack Developer Intern

    Built and maintained Django backend services
    and worked with MySQL.

    Connected frontend components to Django endpoints
    and worked with API-based backend services.
    """
}


def main():

    print("Fetching real jobs from Himalayas...")

    jobs = fetch_jobs("machine learning", limit=20)

    results = []

    for job in jobs:

        # Convert the job into the format expected by matcher
        job_for_matching = {
            "title": job["title"],
            "company": job["company"],
            "description": job["description"],
            "skills": []
        }

        # Skills we can currently detect from job descriptions
        possible_skills = [
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
            "artificial intelligence"
        ]

        description = job["description"].lower()

        for skill in possible_skills:
            if skill in description:
                job_for_matching["skills"].append(skill)

        result = calculate_match(
            resume_profile,
            job_for_matching
        )

        results.append({
            "job": job,
            "match": result
        })

    # Highest matches first.
    # Jobs that cannot be evaluated are placed at the bottom.
    results.sort(
        key=lambda x: (
            x["match"]["score"]
            if x["match"]["score"] is not None
            else -1
        ),
        reverse=True
    )

    print(f"\nFound {len(results)} jobs\n")

    for index, item in enumerate(results, start=1):

        job = item["job"]
        match = item["match"]

        print("=" * 60)
        print(f"{index}. {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")

        if match["score"] is None:
            print("Match: Unable to evaluate")
        else:
            print(f"Match: {match['score']}%")

        print("Matched:", match["matched_skills"])
        print("Missing:", match["missing_skills"])
        print("Reason:", match["reason"])
        print("Apply:", job["application_link"])
        print()


if __name__ == "__main__":
    main()