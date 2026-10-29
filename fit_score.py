from copilot.cvdata import cv_to_text
from copilot.keywords import extract_keywords
from copilot.scoring import fit_score, format_report
from copilot.storage import load_json_file
from copilot.textio import load_text


def main():
    jd = extract_keywords(load_text("data/jd.txt"))
    cv = extract_keywords(cv_to_text(load_json_file("data/cv.json")))
    score, matched, missing = fit_score(jd, cv)
    print(format_report(score, matched, missing))


if __name__ == "__main__":
    main()