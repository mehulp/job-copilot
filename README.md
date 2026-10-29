# Job Search Copilot

A command-line tool that matches a CV against job descriptions, keeps stories for
interviews, and tracks applications. Built in Python as a hands-on project while
learning AI-assisted engineering.

## What it does

- Scores how well a CV matches a job description, and lists matched and missing keywords
- Stores CV data and interview stories as JSON
- Tracks applications in a local SQLite database
- Week 2 and 3 add LLM calls, retrieval and an agent (see the roadmap)

## Quick start

```bash
git clone https://github.com/mehulp/job-copilot.git
cd job-copilot
python3 -m venv .venv
source .venv/bin/activate

python3 -m copilot score --jd data/sample/jd.txt --cv data/sample/cv.json --top 4
```

Example output:

```text
Fit score: 14%
Matched (24): aws, building, cloud, design ... (+20 more)
Missing (147): accountable, apis, applications, architects ... (+143 more)
```

## Commands

| Command | What it does |
| --- | --- |
| `score --jd FILE [--cv FILE] [--top N]` | Score a CV against a job description |
| `stories [--file FILE] [--theme T]` | List stories |
| `add`, `list`, `status` | Track applications in SQLite |

## Project layout

- `copilot/` the package: keywords, scoring, storage, models, database and CLI
- `data/sample/` invented sample data. Real data stays out of the repo

## Roadmap

- [x] Week 1: keyword scoring, JSON data, CLI, SQLite tracker
- [ ] Week 2: LLM summaries, structured extraction, embeddings, retrieval
- [ ] Week 3: an agent that tailors bullets, tool use, evaluations

## Privacy

The repo contains only sample data. Personal data and API keys are kept out with `.gitignore`.