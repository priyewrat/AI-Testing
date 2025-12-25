import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="AI Test Report", layout="centered")
st.title("AI Agent Test Report")

path = Path(__file__).resolve().parent.parent / "reports" / "latest_report.json"

if not path.exists():
    st.warning("No report found. Run the agent first.")
else:
    detail = json.loads(path.read_text(encoding="utf-8"))
    st.subheader("Summary")
    st.write(f"Success: {'✅' if detail.get('success') else '❌'}")
    st.write(f"Return code: {detail.get('returncode')}")
    st.subheader("Actions")
    for i, a in enumerate(detail.get("actions", []), 1):
        st.write(f"{i}. {a['action']} {a.get('target','')} {a.get('value','')}")
    st.subheader("Logs")
    st.text_area("stdout", detail.get("stdout", ""), height=200)
    st.text_area("stderr", detail.get("stderr", ""), height=200)
