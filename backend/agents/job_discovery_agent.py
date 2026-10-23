
from services.job_sources import get_sample_jobs


def discover_jobs(keyword=None, location=None, job_type=None):
    """
    Discover sample jobs using optional filters.

    This version does not require an AI API call.
    """
    jobs = get_sample_jobs()
    results = []

    for job in jobs:
        if keyword:
            searchable_text = (
                job["title"] + " "
                + job["description"] + " "
                + " ".join(job["required_skills"])
            ).lower()

            if keyword.lower() not in searchable_text:
                continue

        if location:
            if location.lower() not in job["location"].lower():
                continue

        if job_type:
            if job_type.lower() != job["job_type"].lower():
                continue

        results.append(job)

    return results
