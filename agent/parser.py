import re
from typing import List, Dict

# A simple rule-based parser to map natural language into action steps.
# Supports: goto/open, fill type-in, click, assert text/contains

def parse_instruction(nl: str) -> List[Dict]:
    text = nl.strip().lower()

    actions = []

    # URL or route detection
    # Patterns: "open the login page", "go to /login", "navigate to http://..."
    url_match = re.search(r"(http[s]?://[^\s,]+|/(login|form|home|dashboard))", text)
    if "open" in text or "go to" in text or "navigate" in text:
        if url_match:
            url = url_match.group(1)
            actions.append({"action": "goto", "target": url})
        else:
            # default to login route if mentioned
            if "login" in text:
                actions.append({"action": "goto", "target": "http://127.0.0.1:5000/login"})
            else:
                actions.append({"action": "goto", "target": "http://127.0.0.1:5000/"})

    # Fill username
    user_match = re.search(r"(username|user name)\s+(is|=)?\s*([a-z0-9_]+)", text)
    if not user_match:
        user_match = re.search(r"enter username\s+([a-z0-9_]+)", text)
    if user_match:
        value = user_match.group(3) if user_match.lastindex and user_match.lastindex >= 3 else user_match.group(user_match.lastindex)
        actions.append({"action": "fill", "target": "#username", "value": value})

    # Fill password
    pass_match = re.search(r"(password|pass word)\s+(is|=)?\s*([^\s,]+)", text)
    if not pass_match:
        pass_match = re.search(r"enter password\s+([^\s,]+)", text)
    if pass_match:
        value = pass_match.group(3) if pass_match.lastindex and pass_match.lastindex >= 3 else pass_match.group(pass_match.lastindex)
        actions.append({"action": "fill", "target": "#password", "value": value})

    # Generic fill pattern: "type <value> into #selector" or "fill <field> with <value>"
    generic_fills = re.findall(r"type\s+\"([^\"]+)\"\s+into\s+(#[a-z0-9_-]+)", text)
    for val, sel in generic_fills:
        actions.append({"action": "fill", "target": sel, "value": val})

    # Click actions
    if "click login" in text or "click submit" in text or "press login" in text:
        actions.append({"action": "click", "target": "#submit"})
    # Fallback if "click" mentioned without target: click first button
    if "click" in text and not any(a for a in actions if a["action"] == "click"):
        actions.append({"action": "click", "target": "button[type='submit']"})

    # Assertions: "verify welcome message contains ...", "check text of #welcome includes ..."
    contains_match = re.search(r"verify.*(contains|include[s]?)\s+([^\n,]+)", text)
    if contains_match:
        phrase = contains_match.group(2).strip()
        actions.append({"action": "assert_contains", "target": "#welcome", "value": phrase})

    # Specific target assertion: "verify #welcome contains Hello"
    targeted_assert = re.findall(r"verify\s+(#[a-z0-9_-]+)\s+(contains|equals)\s+\"([^\"]+)\"", text)
    for sel, kind, phrase in targeted_assert:
        if kind == "equals":
            actions.append({"action": "assert_text", "target": sel, "value": phrase})
        else:
            actions.append({"action": "assert_contains", "target": sel, "value": phrase})

    # Default: if login context detected, assert welcome exists
    if ("login" in text) and not any(a for a in actions if a["action"].startswith("assert")):
        actions.append({"action": "assert_contains", "target": "#welcome", "value": "welcome"})

    return actions
