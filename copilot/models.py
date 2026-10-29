from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from copilot.keywords import extract_keywords

STATUSES = ("to apply", "applied", "interviewing", "offer", "rejected", "withdrawn")


@dataclass
class Job:
    company: str
    title: str
    location: str = ""
    description: str = field(default="", repr=False)
    url: str = ""

    def keywords(self) -> set[str]:
        """Return the meaningful words in this job's description."""
        return extract_keywords(self.description)


@dataclass
class Application:
    job: Job
    status: str = "to apply"
    applied_on: Optional[date] = None
    cv_version: str = ""
    notes: list[str] = field(default_factory=list)
    id: Optional[int] = None

    def mark_applied(self, cv_version: str) -> None:
        """Record that the application was sent today."""
        self.status = "applied"
        self.applied_on = date.today()
        self.cv_version = cv_version

    def set_status(self, status: str) -> None:
        """Change the status, refusing values we do not know."""
        if status not in STATUSES:
            raise ValueError(
                f"Unknown status '{status}'. Choose from: {', '.join(STATUSES)}"
            )
        self.status = status

    def days_since_applied(self) -> Optional[int]:
        """Days since the application was sent, or None if it was not sent."""
        if self.applied_on is None:
            return None
        return (date.today() - self.applied_on).days