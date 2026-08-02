import logging

from playwright.sync_api import sync_playwright

import agentql

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


if __name__ == "__main__":
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        page = agentql.wrap(browser.new_page())
        page.goto("https://www.google.com")

        QUERY = """
        {
            search_box
            search_btn
            about_link
        }
        """

        log.debug("Analyzing...")

        response = page.query_elements(QUERY)

        log.debug("Inputting text...")
        response.search_box.fill("tinyfish")

        log.debug('Clicking "Search" button...')
        response.search_btn.click(force=True)

        page.wait_for_page_ready_state()
