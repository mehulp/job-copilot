import argparse
import sys
from contextlib import closing
from typing import Optional

from copilot import db
from copilot.cvdata import cv_to_text
from copilot.keywords import extract_keywords
from copilot.models import STATUSES, Application, Job
from copilot.scoring import fit_score, format_report
from copilot.storage import DataFileError, load_json
from copilot.textio import load_text

DB_PATH = "data/copilot.db"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="copilot",
        description="Job Search Copilot: match your CV to job descriptions.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    score = subparsers.add_parser(
        "score", help="score your CV against a job description"
    )
    score.add_argument(
        "--jd", required=True, help="path to the job description (text file)"
    )
    score.add_argument(
        "--cv", default="data/cv.json", help="path to your CV (JSON file)"
    )
    score.add_argument(
        "--top", type=int, default=40, help="words to show per list"
    )

    stories = subparsers.add_parser("stories", help="list your stories")
    stories.add_argument(
        "--file", default="data/stories.json", help="path to your stories (JSON file)"
    )
    stories.add_argument("--theme", help="only show stories with this theme")

    add = subparsers.add_parser("add", help="record a new application")
    add.add_argument("--company", required=True)
    add.add_argument("--title", required=True)
    add.add_argument("--location", default="")
    add.add_argument("--url", default="")
    add.add_argument("--jd", help="path to the job description (text file)")

    listing = subparsers.add_parser("list", help="list your applications")
    listing.add_argument("--status", choices=STATUSES, help="only show this status")

    status = subparsers.add_parser("status", help="change an application's status")
    status.add_argument("id", type=int, help="application number")
    status.add_argument("new_status", choices=STATUSES)

    return parser


def cmd_score(args: argparse.Namespace) -> int:
    jd = extract_keywords(load_text(args.jd))
    cv = extract_keywords(cv_to_text(load_json(args.cv)))
    score, matched, missing = fit_score(jd, cv)
    print(format_report(score, matched, missing, max_items=args.top))
    return 0


def cmd_stories(args: argparse.Namespace) -> int:
    for story in load_json(args.file):
        if args.theme and args.theme not in story["themes"]:
            continue
        print(f"{story['id']}: {story['title']}")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    description = load_text(args.jd) if args.jd else ""
    job = Job(
        company=args.company,
        title=args.title,
        location=args.location,
        url=args.url,
        description=description,
    )
    with closing(db.connect(DB_PATH)) as conn:
        app_id = db.add_application(conn, Application(job=job))
    print(f"Saved application {app_id}: {job.company}, {job.title}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    with closing(db.connect(DB_PATH)) as conn:
        apps = db.list_applications(conn, status=args.status)
    if not apps:
        print("No applications yet.")
        return 0
    for app in apps:
        print(f"{app.id:>3}  {app.status:<13}  {app.job.company:<22}  {app.job.title}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    with closing(db.connect(DB_PATH)) as conn:
        db.update_status(conn, args.id, args.new_status)
    print(f"Application {args.id} is now '{args.new_status}'.")
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    commands = {
        "score": cmd_score,
        "stories": cmd_stories,
        "add": cmd_add,
        "list": cmd_list,
        "status": cmd_status,
    }
    try:
        return commands[args.command](args)
    except FileNotFoundError as err:
        print(f"Error: file not found: {err.filename}", file=sys.stderr)
    except DataFileError as err:
        print(f"Error: {err}", file=sys.stderr)
    except db.ApplicationNotFound as err:
        print(f"Error: {err}", file=sys.stderr)
    return 1