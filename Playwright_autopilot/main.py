# main.py

import os
from playwright.sync_api import sync_playwright, TimeoutError

SEARCH_QUERY = "Playwright cheat sheet for python"

def save_to_file(data):
    os.makedirs("data", exist_ok=True)
    with open("data/results.txt", "w", encoding="utf-8") as f:
        f.write(data)
    print("📁 Results saved")

# 🔹 Self-healing selector function
def find_search_box(page):
    selectors = [
        ("ID", "#ask-input"),
        ("XPATH", 'xpath=//*[@id="ask-input"]'),
        ("ROLE", "role=textbox"),
        ("TEXTAREA", "textarea")
    ]

    for name, selector in selectors:
        try:
            print(f"🔍 Trying selector [{name}] → {selector}")
            element = page.wait_for_selector(selector, timeout=5000)
            print(f"✅ Found using [{name}]")
            return selector
        except TimeoutError:
            print(f"❌ Failed [{name}]")

    raise Exception("🚨 Search box not found using any selector!")

def run():
    print(f"🔍 Auto Searching: {SEARCH_QUERY}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.perplexity.ai")

        # 🔥 Self-healing selector usage
        search_selector = find_search_box(page)

        page.fill(search_selector, SEARCH_QUERY)
        page.keyboard.press("Enter")

        # Wait for response
        page.wait_for_timeout(8000)

        # Extract results
        results = page.locator("div.prose").all_inner_texts()
        final_text = "\n\n".join(results)

        save_to_file(final_text)

        browser.close()

if __name__ == "__main__":
    run()