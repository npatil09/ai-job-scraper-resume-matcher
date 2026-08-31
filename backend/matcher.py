def calculate_match(resume_profile, job):
    """
    Calculate a job match using resume skills and evidence
    from the resume's project and experience text.
    """

    resume_skills = {
        skill.lower().strip()
        for skill in resume_profile.get("skills", [])
    }

    evidence_text = (
        resume_profile.get("projects", "") + " " +
        resume_profile.get("experience", "")
    ).lower()

    job_skills = {
        skill.lower().strip()
        for skill in job.get("skills", [])
        if skill
    }

    if not job_skills:
        return {
            "score": None,
            "matched_skills": [],
            "missing_skills": [],
            "reason": "Unable to evaluate this job because no relevant skills were detected."
        }

    # Skills that are more meaningful indicators of technical fit
    strong_skills = {
        "python",
        "pytorch",
        "tensorflow",
        "scikit-learn",
        "fastapi",
        "django",
        "rag",
        "qdrant",
        "computer vision",
        "deep learning",
        "machine learning",
        "llm",
        "nlp",
        "generative ai",
        "prompt engineering",
        "opencv",
        "mediapipe",
        "sql"
    }

    matched = []
    missing = []

    for skill in job_skills:

        # Directly listed on the resume
        if skill in resume_skills:
            matched.append(skill)
            continue

        # Evidence from projects/experience
        if skill in evidence_text:
            matched.append(skill)
            continue

        missing.append(skill)

    # Give slightly more importance to strong technical skills
    total_weight = 0
    matched_weight = 0

    for skill in job_skills:
        weight = 2 if skill in strong_skills else 1
        total_weight += weight

        if skill in matched:
            matched_weight += weight

    if total_weight == 0:
        score = 0
    else:
        score = round((matched_weight / total_weight) * 100)

    return {
        "score": score,
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "reason": generate_reason(
            score,
            matched,
            missing
        )
    }


def generate_reason(score, matched, missing):

    if score is None:
        return (
            "Unable to evaluate this job because "
            "no relevant skills were detected."
        )

    if score >= 80:
        level = "Strong match"
    elif score >= 60:
        level = "Good match"
    elif score >= 40:
        level = "Partial match"
    else:
        level = "Limited match"

    reason = (
        f"{level}. Your profile matches "
        f"{len(matched)} relevant skill(s)."
    )

    if missing:
        reason += (
            f" Missing or unverified skills: "
            f"{', '.join(sorted(missing))}."
        )

    return reason