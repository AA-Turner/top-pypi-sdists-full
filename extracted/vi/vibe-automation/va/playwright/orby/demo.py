"""
Minimal Browser Agent Implementation

This script demonstrates a simple browser automation agent that can perform
web tasks using Playwright and a custom agent model.
"""

import asyncio
from playwright.async_api import async_playwright

from .subtask_agent import perform_task


async def main():
    async with async_playwright() as p:
        # Launch browser and navigate to Google
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://www.google.com")
        await perform_task(page, "Perform google search for 'how to make a cake'")


if __name__ == "__main__":
    asyncio.run(main())
