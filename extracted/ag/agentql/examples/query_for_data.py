import logging

from playwright.sync_api import sync_playwright

import agentql

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


if __name__ == "__main__":
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        page = agentql.wrap(browser.new_page())
        page.goto("https://apply.workable.com/pony-dot-ai/j/95797D31AA/")

        QUERY = """
        {
            required_programming_skills (just the skill name)[]
            base_salary_min (without the dollar sign, use _ as separator)
            base_salary_max (with dollar sign)
        }
        """

        response = page.query_data(QUERY)
        print(f"Base salary min: {response['base_salary_min']}")
        print(f"Base salary max: {response['base_salary_max']}")

        for skill in response.get("required_programming_skills", []):
            print(f"Required programming skill: {skill}")
