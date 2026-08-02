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

        response = await page.query_data(QUERY)
        print(f"Base salary min: {response['base_salary_min']}")
        print(f"Base salary max: {response['base_salary_max']}")

        for skill in response.get("required_programming_skills", []):
            print(f"Required programming skill: {skill}")


if __name__ == "__main__":
    asyncio.run(main())
