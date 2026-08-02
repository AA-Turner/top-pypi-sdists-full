import logging

from playwright.sync_api import sync_playwright

import agentql

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


if __name__ == "__main__":
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        page = agentql.wrap(browser.new_page())
        page.goto("https://www.agentql.com/blog")

        PROMPT = "Extract the title and content of each blog post"

        response = page.get_data_by_prompt_experimental(PROMPT)
        print(response)
