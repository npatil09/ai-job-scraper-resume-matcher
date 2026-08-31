from matcher import calculate_match
from jobs import JOBS


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


for job in JOBS:

    result = calculate_match(resume_profile, job)

    print("\n-----------------------------")
    print(job["title"])
    print(job["company"])
    print(f"Match: {result['score']}%")
    print("Matched:", result["matched_skills"])
    print("Missing:", result["missing_skills"])
    print("Reason:", result["reason"])