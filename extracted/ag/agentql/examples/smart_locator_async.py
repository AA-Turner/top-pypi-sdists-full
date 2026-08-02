import asyncio

from playwright.async_api import async_playwright

import agentql


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await agentql.wrap_async(browser.new_page())
        await page.goto("https://www.google.com/")

        search_box = await page.get_by_prompt("Search input field")  # type: ignore
        search_btn = await page.get_by_prompt("Search button which initiaties the search")  # type: ignore

        if search_box is None or search_btn is None:
            print("Element not found")
            return

        await search_box.type("Tiny Fish")
        await search_btn.click(force=True)

        await page.wait_for_timeout(5000)


if __name__ == "__main__":
    asyncio.run(main())
