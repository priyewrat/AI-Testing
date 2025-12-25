from playwright.sync_api import sync_playwright

def run_generated():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto('http://127.0.0.1:5000/login')
        page.fill('#username', 'test_user')
        page.fill('#password', 'secret')
        page.click('#submit')
        actual = page.inner_text('#welcome')
        assert 'welcome' in actual.lower(), f"Expected to contain 'welcome', got '{actual}'"

        context.close()
        browser.close()

if __name__ == "__main__":
    run_generated()
