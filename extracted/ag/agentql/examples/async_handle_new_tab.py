import asyncio
import logging

from playwright.async_api import async_playwright

import agentql

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


async def main():
    async with async_playwright() as playwright, await playwright.chromium.launch(headless=False) as browser:
        page = await agentql.wrap_async(browser.new_page())
        await page.goto("https://playwright.dev/docs/api/class-browserserver")

        QUERY = """
        {
            promise_link
        }
        """

        log.debug("Analyzing...")

        response = await page.query_elements(QUERY)

        await page.screenshot(path="screenshot.png")

        # Explicitly wait for the new tab to open. The following code will wait for tab to open before proceeding.
        async with page.context.expect_page() as new_page:
            await response.promise_link.click()

        # Point to the new tab
        page = await new_page.value  # type: ignore

        await page.screenshot(path="new_tab_screenshot.png")


if __name__ == "__main__":
    asyncio.run(main())
