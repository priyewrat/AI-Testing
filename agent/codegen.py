from typing import List, Dict

HEADER = """from playwright.sync_api import sync_playwright

def run_generated():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
"""

FOOTER = """
        context.close()
        browser.close()

if __name__ == "__main__":
    run_generated()
"""

def to_python(actions: List[Dict]) -> str:
    lines = [HEADER]
    for a in actions:
        if a["action"] == "goto":
            lines.append(f"        page.goto('{a['target']}')\n")
        elif a["action"] == "fill":
            lines.append(f"        page.fill('{a['target']}', '{a['value']}')\n")
        elif a["action"] == "click":
            lines.append(f"        page.click('{a['target']}')\n")
        elif a["action"] == "assert_text":
            lines.append(f"        actual = page.inner_text('{a['target']}')\n")
            # Case-insensitive exact match
            lines.append(
                f"        assert actual.strip().lower() == '{a['value'].lower()}', "
                f"f\"Expected exact text '{a['value']}', got '{{actual}}'\"\n"
            )
        elif a["action"] == "assert_contains":
            lines.append(f"        actual = page.inner_text('{a['target']}')\n")
            # Case-insensitive containment check
            lines.append(
                f"        assert '{a['value'].lower()}' in actual.lower(), "
                f"f\"Expected to contain '{a['value']}', got '{{actual}}'\"\n"
            )
        else:
            lines.append(f"        # Unsupported action: {a}\n")
    lines.append(FOOTER)
    return "".join(lines)
