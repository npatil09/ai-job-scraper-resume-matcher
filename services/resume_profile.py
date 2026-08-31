import re


SKILLS = [
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
    "Deep Learning",
    "Computer Vision",
    "Federated Learning",
    "Differential Privacy",
]


SECTION_HEADINGS = [
    "RESEARCH INTEREST",
    "EDUCATION",
    "RESEARCH-RELEVANT PROJECTS",
    "EXPERIENCE",
    "SKILLS",
]


def clean_text(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)

    return text.strip()


def extract_skills(text: str) -> list[str]:
    found_skills = []

    text_lower = text.lower()

    for skill in SKILLS:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills


def extract_sections(text: str) -> dict:
    """
    Extract sections based on the known resume headings.
    """

    # Normalize spacing while preserving line structure
    text = clean_text(text)

    # Find every section heading
    matches = []

    for heading in SECTION_HEADINGS:
        pattern = rf"(?m)^{re.escape(heading)}\s*$"

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            matches.append(
                (match.start(), match.end(), heading)
            )

    # Sort headings according to their position in the resume
    matches.sort(key=lambda x: x[0])

    sections = {}

    for index, (start, end, heading) in enumerate(matches):

        if index + 1 < len(matches):
            next_start = matches[index + 1][0]
            content = text[end:next_start]
        else:
            content = text[end:]

        sections[heading] = clean_text(content)

    return sections


def build_resume_profile(text: str) -> dict:

    sections = extract_sections(text)

    return {
        "skills": extract_skills(text),

        "research_interest": sections.get(
            "RESEARCH INTEREST",
            ""
        ),

        "education": sections.get(
            "EDUCATION",
            ""
        ),

        "projects": sections.get(
            "RESEARCH-RELEVANT PROJECTS",
            ""
        ),

        "experience": sections.get(
            "EXPERIENCE",
            ""
        ),

        "skills_section": sections.get(
            "SKILLS",
            ""
        ),
    }