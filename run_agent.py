import sys
from agent.graph import run_pipeline

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_agent.py \"<natural language test>\"")
        sys.exit(1)
    nl = sys.argv[1]
    report = run_pipeline(nl)
    print("Success:", report["success"])
    print("Report written to reports/latest_report.json")

if __name__ == "__main__":
    main()
