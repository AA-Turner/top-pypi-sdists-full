import asyncio
import json
import logging

from playwright.async_api import async_playwright

import agentql
from agentql.tools.async_api import paginate

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


async def main():
    async with async_playwright() as playwright, await playwright.chromium.launch(headless=False) as browser:
        page = await agentql.wrap_async(browser.new_page())
        await page.goto("https://news.ycombinator.com/")

        QUERY = """
        {
            posts[] {
                title
            }
        }
        """
        paginated_data = await paginate(page, QUERY, 3)

        with open("./hackernews_paginated_data.json", "w") as f:
            json.dump(paginated_data, f, indent=4)
        log.debug("Paginated data has been saved to hackernews_paginated_data.json")


if __name__ == "__main__":
    asyncio.run(main())
