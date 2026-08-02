import asyncio
import logging

from playwright.async_api import async_playwright

import agentql

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


async def main():
    async with async_playwright() as playwright, await playwright.chromium.launch(headless=False) as browser:
        page = await agentql.wrap_async(browser.new_page())
        await page.goto("https://apply.workable.com/pony-dot-ai/j/95797D31AA/")

        QUERY = """
        {
            required_programming_skills (just the skill name)[]
            base_salary_min (without the dollar sign, use _ as separator)
            base_salary_max (with dollar sign)
        }
        """

        await page.query_data(QUERY)
        print(f"Query: {page.get_last_query()}")
        print(f"Response: {page.get_last_response()}")
        print(f"Accessibility tree: {page.get_last_accessibility_tree()}")


if __name__ == "__main__":
    asyncio.run(main())
