def cv_to_text(cv:dict) -> str:
    """Flatten a CV dictionary into one block of text for keyword matching."""
    parts = [cv.get("headline", ""), cv.get("summary", "")]
    parts.extend(cv.get("skills", []))
    parts.extend(cv.get("certifications", []))
    for job in cv.get("experience", []):
        parts.append(job.get("title", ""))
        parts.append(job.get("company", ""))
        parts.extend(job.get("bullets", []))
    return "\n".join(filter(None, parts))