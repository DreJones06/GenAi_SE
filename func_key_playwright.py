from playwright.async_api import async_playwright 
import asyncio

async def playwright_func():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        pages = await browser.new_page()
#navigation
        await pages.goto("https://www.google.com/")
        # will it autofill the search box?
        await pages.fill("textarea[name='q']", "socialeagle ai")
        await pages.press("textarea[name='q']", "Enter")
 
        await pages.wait_for_timeout(5000)
        await browser.close()

if __name__ == "__main__":    
    asyncio.run(playwright_func())
