import json
from pathlib import Path

def summarize(report_json: dict) -> dict:
    # basic summary: we infer pass/fail from success flag, and show assertion clues from stderr
    summary = {
        "passed": 1 if report_json.get("success") else 0,
        "failed": 0 if report_json.get("success") else 1,
        "returncode": report_json.get("returncode"),
    }
    return summary

def save_summary(report_json: dict, path: Path):
    summary = summarize(report_json)
    payload = {"summary": summary, "detail": report_json}
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload
