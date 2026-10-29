import re

GRAMMAR_WORDS = {
    "the", "and", "for", "with", "you", "our", "your", "are", "will",
    "this", "that", "from", "have", "has", "who", "can", "all", "into",
}

FILLER_WORDS = {
    "also", "enough", "same", "take", "type", "used", "what", "where",
    "why", "real", "part", "about", "across", "both", "its", "through",
    "three", "new", "time", "work", "working", "including", "based",
    "strong", "level", "years", "ability", "clear", "clearly", "closely",
    "many", "role", "looking", "join", "meet", "own", "full",
}

STOPWORDS = GRAMMAR_WORDS | FILLER_WORDS

WORD_PATTERN = r"[a-z][a-z0-9+#]*"
MIN_LENGTH = 3


def extract_keywords(text: str) -> set[str]:
    """Return the set of meaningful lowercase words found in text."""
    words = re.findall(WORD_PATTERN, text.lower())
    return {w for w in words if w not in STOPWORDS and len(w) >= MIN_LENGTH}