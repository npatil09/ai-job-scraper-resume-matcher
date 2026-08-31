import requests


HIMALAYAS_SEARCH_API = "https://himalayas.app/jobs/api/search"


def fetch_jobs(query="machine learning", limit=20):
    """
    Fetch real remote internship jobs from Himalayas.

    Himalayas provides a public JSON API that does not
    require authentication.
    """

    params = {
        "q": query,
        "employment_type": "Intern",
        "sort": "recent",
        "page": 1,
    }

    response = requests.get(
        HIMALAYAS_SEARCH_API,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    jobs = []

    for job in data.get("jobs", [])[:limit]:
        jobs.append({
            "title": job.get("title", ""),
            "company": job.get("companyName", ""),
            "description": job.get("description", ""),
            "employment_type": job.get("employmentType", ""),
            "location": job.get("locationRestrictions", []),
            "application_link": job.get("applicationLink", ""),
            "published": job.get("pubDate", ""),
            "min_salary": job.get("minSalary"),
            "max_salary": job.get("maxSalary"),
            "currency": job.get("currency", ""),
        })

    return jobs


if __name__ == "__main__":
    jobs = fetch_jobs("machine learning")

    print(f"Found {len(jobs)} jobs")

    for job in jobs:
        print("\n-----------------------------")
        print("Title:", job["title"])
        print("Company:", job["company"])
        print("Type:", job["employment_type"])
        print("Location:", job["location"])
        print("Apply:", job["application_link"])