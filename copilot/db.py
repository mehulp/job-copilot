import json
import sqlite3
from datetime import date
from typing import Optional

from copilot.models import STATUSES, Application, Job

SCHEMA = """
CREATE TABLE IF NOT EXISTS applications (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    company     TEXT NOT NULL,
    title       TEXT NOT NULL,
    location    TEXT NOT NULL DEFAULT '',
    url         TEXT NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT '',
    status      TEXT NOT NULL DEFAULT 'to apply',
    applied_on  TEXT,
    cv_version  TEXT NOT NULL DEFAULT '',
    notes       TEXT NOT NULL DEFAULT '[]'
)
"""


class ApplicationNotFound(Exception):
    """Raised when an application number does not exist."""


def connect(path: str = "data/copilot.db") -> sqlite3.Connection:
    """Open (and if needed create) the database."""
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute(SCHEMA)
    return conn


def add_application(conn: sqlite3.Connection, app: Application) -> int:
    """Save an application and return its new id."""
    job = app.job
    with conn:
        cursor = conn.execute(
            "INSERT INTO applications "
            "(company, title, location, url, description, status, "
            "applied_on, cv_version, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                job.company,
                job.title,
                job.location,
                job.url,
                job.description,
                app.status,
                app.applied_on.isoformat() if app.applied_on else None,
                app.cv_version,
                json.dumps(app.notes),
            ),
        )
    return cursor.lastrowid


def _to_application(row: sqlite3.Row) -> Application:
    """Turn one database row back into an Application object."""
    job = Job(
        company=row["company"],
        title=row["title"],
        location=row["location"],
        description=row["description"],
        url=row["url"],
    )
    applied_on = date.fromisoformat(row["applied_on"]) if row["applied_on"] else None
    return Application(
        job=job,
        status=row["status"],
        applied_on=applied_on,
        cv_version=row["cv_version"],
        notes=json.loads(row["notes"]),
        id=row["id"],
    )


def list_applications(
    conn: sqlite3.Connection, status: Optional[str] = None
) -> list[Application]:
    """Return all applications, or only those with the given status."""
    if status is None:
        rows = conn.execute("SELECT * FROM applications ORDER BY id").fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM applications WHERE status = ? ORDER BY id", (status,)
        ).fetchall()
    return [_to_application(row) for row in rows]


def update_status(conn: sqlite3.Connection, app_id: int, status: str) -> None:
    """Change the status of one application."""
    if status not in STATUSES:
        raise ValueError(f"Unknown status '{status}'.")
    with conn:
        cursor = conn.execute(
            "UPDATE applications SET status = ? WHERE id = ?", (status, app_id)
        )
    if cursor.rowcount == 0:
        raise ApplicationNotFound(f"No application with number {app_id}.")