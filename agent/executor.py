import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

def write_script(code: str, path: Path):
    path.write_text(code, encoding="utf-8")

def run_script(path: Path):
    try:
        result = subprocess.run([sys.executable, str(path)], capture_output=True, text=True, timeout=60)
        success = result.returncode == 0
        return {
            "success": success,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired as e:
        return {"success": False, "stdout": "", "stderr": f"Timeout: {e}", "returncode": -1}

def record_run_report(actions, exec_result, report_path: Path):
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "actions": actions,
        "success": exec_result["success"],
        "stdout": exec_result["stdout"],
        "stderr": exec_result["stderr"],
        "returncode": exec_result["returncode"],
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
