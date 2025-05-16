import os
import json
from glob import glob
from datetime import datetime

ROOT = "scorecard-reports"
OUTPUT_MD = "README.md"

def get_latest_report_path(repo_dir):
    files = sorted(glob(os.path.join(repo_dir, "*.json")), reverse=True)
    return files[0] if files else None

def parse_scorecard(file_path):
    with open(file_path) as f:
        data = json.load(f)
    score = data.get("score", "N/A")
    checks = data.get("checks", [])
    important_check_names = [
        "Branch-Protection", "Token-Permissions", "Signed-Releases"
    ]
    important_checks = [
        c for c in checks if c["name"] in important_check_names
    ]
    checks_summary = ", ".join(
        f'{c["name"]} {"✅" if c["score"] > 5 else "❌"}' for c in important_checks
    )
    return score, checks_summary

def generate_dashboard():
    lines = []
    lines.append("# OpenSSF Scorecard Dashboard\n")
    lines.append("This dashboard is auto-generated based on the latest reports.\n")
    lines.append("## Summary\n")
    lines.append("| Repo | Date | Score | Critical Checks |")
    lines.append("|------|------|-------|-----------------|")

    index = []

    for repo_path in sorted(os.listdir(ROOT)):
        full_path = os.path.join(ROOT, repo_path)
        latest_report = get_latest_report_path(full_path)
        if not latest_report:
            continue

        repo_name = repo_path.replace("_", "/")
        date = os.path.basename(latest_report).split("-report.json")[0]
        score, summary = parse_scorecard(latest_report)

        lines.append(f"| [{repo_name}](https://github.com/{repo_name}) | {date} | {score} | {summary} |")
        index.append(f"- [{repo_name} latest report](./{latest_report})")

    lines.append("\n## Index\n")
    lines.extend(index)

    with open(OUTPUT_MD, "w") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    generate_dashboard()
