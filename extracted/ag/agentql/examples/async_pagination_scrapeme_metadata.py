import asyncio
import logging

from playwright.async_api import async_playwright

import agentql

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


async def main():
    async with async_playwright() as playwright, await playwright.chromium.launch(headless=False) as browser:
        page = await agentql.wrap_async(browser.new_page())
        await page.goto("https://scrapeme.live/shop/page/2/")

        log.debug("Navigating to next page...")
        pagination_info = await page.get_pagination_info()

        # attempt to navigate to next page
        if pagination_info.has_next_page:
            await pagination_info.navigate_to_next_page()

        await page.wait_for_timeout(1000)


if __name__ == "__main__":
    asyncio.run(main())
