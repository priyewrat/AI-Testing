# Minimal orchestration: parse -> codegen -> write -> execute -> report
from pathlib import Path
from .parser import parse_instruction
from .codegen import to_python
from .executor import write_script, run_script, record_run_report

ARTIFACTS_DIR = Path(__file__).resolve().parent.parent
TEST_PATH = ARTIFACTS_DIR / "tests" / "generated_test.py"
REPORT_PATH = ARTIFACTS_DIR / "reports" / "latest_report.json"

def run_pipeline(nl_instruction: str) -> dict:
    actions = parse_instruction(nl_instruction)
    code = to_python(actions)
    write_script(code, TEST_PATH)
    exec_result = run_script(TEST_PATH)
    report = record_run_report(actions, exec_result, REPORT_PATH)
    return report
