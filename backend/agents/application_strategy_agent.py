
import re


def is_entry_level_job(job):
    """Check whether a job appears suitable for freshers or beginners."""
    title = job.get("title", "").lower()
    description = job.get("description", "").lower()

    # Explicit eligibility statements take priority over weak seniority clues.
    entry_phrases = [
        "freshers eligible",
        "freshers are eligible",
        "entry level",
        "entry-level",
        "for freshers",
        "0-1 years",
        "0 to 1 year",
        "no experience required",
    ]

    text = f"{title} {description}"

    if any(phrase in text for phrase in entry_phrases):
        return True

    title_entry_terms = [
        "intern",
        "internship",
        "trainee",
        "junior",
        "graduate",
        "fresher",
    ]

    return any(term in title for term in title_entry_terms)


def is_senior_job(job):
    """Detect clear senior-level signals from the job title."""
    title = job.get("title", "").lower()

    senior_patterns = [
        r"\bsenior\b",
        r"\blead\b",
        r"\bprincipal\b",
        r"\bstaff engineer\b",
        r"\bmanager\b",
        r"\bdirector\b",
        r"\bhead of\b",
        r"\bsde\s*[23]\b",
    ]

    return any(re.search(pattern, title) for pattern in senior_patterns)


def generate_application_strategy(candidate_profile, matched_jobs):
    """
    Create application priorities using the existing profile
    and job-matching results.
    """
    candidate_skills = {
        skill.strip().lower()
        for skill in candidate_profile.get("skills", [])
        if isinstance(skill, str)
    }

    strategies = []

    for job in matched_jobs:
        match_score = float(job.get("match_percentage", 0))
        title = job.get("title", "Unknown title")
        company = job.get("company", "Unknown company")

        matched_skills = job.get("matched_skills", [])
        missing_skills = job.get("missing_skills", [])

        entry_level = is_entry_level_job(job)
        senior_level = is_senior_job(job)

        if senior_level and not entry_level:
            priority = "Low"
            reason = (
                "The job title suggests a senior-level position. "
                "Verify its experience requirements before applying."
            )

        elif match_score >= 80:
            priority = "High"
            reason = (
                "Strong estimated resume match. "
                "Review the job requirements and eligibility first."
            )

        elif match_score >= 65:
            priority = "Medium"
            reason = (
                "Reasonable estimated match. Review the skill gaps "
                "and confirm the required experience."
            )

        else:
            priority = "Low"
            reason = (
                "The estimated match is relatively low. "
                "Check the required skills before investing time."
            )

        if entry_level and not senior_level and match_score >= 65:
            reason += " The listing also appears to mention an entry-level opportunity."

        if missing_skills:
            next_action = (
                "Review the missing skills: "
                + ", ".join(missing_skills)
                + ". Apply only if you meet the essential requirements."
            )
        else:
            next_action = (
                "Verify the eligibility criteria and prepare a tailored application."
            )

        strategies.append({
            "job_id": job.get("job_id", ""),
            "title": title,
            "company": company,
            "location": job.get("location", "Not specified"),
            "match_percentage": match_score,
            "priority": priority,
            "reason": reason,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "entry_level_signal": entry_level,
            "recommended_next_action": next_action,
            "apply_link": job.get("apply_link", ""),
            "source": job.get("source", "Unknown"),
            "skill_source": job.get("skill_source", "Unknown"),
        })

    priority_order = {"High": 0, "Medium": 1, "Low": 2}

    strategies.sort(
        key=lambda item: (
            priority_order[item["priority"]],
            -item["match_percentage"],
        )
    )

    for index, strategy in enumerate(strategies, start=1):
        strategy["strategy_rank"] = index

    return strategies
