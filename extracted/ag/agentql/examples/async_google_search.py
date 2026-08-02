import asyncio
import logging

from playwright.async_api import async_playwright

import agentql

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


async def main():
    async with async_playwright() as playwright, await playwright.chromium.launch(headless=False) as browser:
        page = await agentql.wrap_async(browser.new_page())
        await page.goto("https://www.google.com")

        QUERY = """
        {
            search_box
            search_btn
            about_link
        }
        """

        log.debug("Analyzing...")

        response = await page.query_elements(QUERY)

        log.debug("Inputting text...")
        await response.search_box.type("Tinyfish")

        log.debug('Clicking "Search" button...')
        await response.search_btn.click()

        await page.wait_for_timeout(10000)


if __name__ == "__main__":
    asyncio.run(main())
