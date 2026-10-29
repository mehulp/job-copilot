def fit_score(
    jd_words: set[str], cv_words: set[str]
) -> tuple[int, set[str], set[str]]:
    """Compare JD keywords with CV keywords.

    Returns (score, matched, missing). The score is the percentage of
    JD keywords that also appear in the CV.
    """
    matched = jd_words & cv_words
    missing = jd_words - cv_words
    score = round(100 * len(matched) / len(jd_words)) if jd_words else 0
    return score, matched, missing



def format_report(
    score: int,
    matched: set[str],
    missing: set[str],
    max_items: int = 40,
) -> str:
    """Build the text report, showing at most max_items words per list."""
    lines = [f"Fit score: {score}%"]
    for title, words in (("Matched", matched), ("Missing", missing)):
        shown = sorted(words)[:max_items]
        extra = len(words) - len(shown)
        text = ", ".join(shown)
        if extra > 0:
            text += f" ... (+{extra} more)"
        lines.append(f"{title} ({len(words)}): {text}")
    return "\n".join(lines)