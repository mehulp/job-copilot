from pathlib import Path


def load_text(path: str) -> str:
    """Read a text file and return its contents as one string."""
    return Path(path).read_text(encoding="utf-8")