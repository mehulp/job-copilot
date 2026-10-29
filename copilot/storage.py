import json
from typing import Any

class DataFileError(Exception):
    """Raised when there is an error reading or writing a data file."""
    pass

def load_json(file_path: str) -> Any:
    """Read a JSON file and return the Python data inside it."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as err:
        raise DataFileError(f"{file_path} is not valid JSON (line {err.lineno}, column {err.colno}): {err.msg}") from err

def save_json(data: Any, file_path: str) -> None:
    """Save a Python object as a JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")  # Add a newline at the end of the file for better readability

