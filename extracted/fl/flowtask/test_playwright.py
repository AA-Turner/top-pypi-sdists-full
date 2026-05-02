import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        try:
            print("Launching browser...")
            browser = await p.chromium.launch(headless=True)
            print("Browser launched.")
            page = await browser.new_page()
            print("Page created.")
            await browser.close()
            print("Success.")
        except Exception as e:
            print(f"Error: {e}")

asyncio.run(main())
