# engine/playwright_engine.py

from playwright.async_api import async_playwright
from config.settings import WAIT_TIME

async def run_search(query):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://www.perplexity.ai")
        await page.wait_for_selector("#ask-input")

        await page.fill("#ask-input", query)
        await page.keyboard.press("Enter")

        await page.wait_for_timeout(WAIT_TIME)

        results = await page.locator("div.prose").all_inner_texts()

        await browser.close()

        return "\n\n".join(results)