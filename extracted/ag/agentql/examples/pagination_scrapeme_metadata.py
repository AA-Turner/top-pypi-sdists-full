import logging

from playwright.sync_api import sync_playwright

import agentql

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

if __name__ == "__main__":
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        page = agentql.wrap(browser.new_page())
        page.goto("https://scrapeme.live/shop/page/2/")

        log.debug("Navigating to next page...")
        pagination_info = page.get_pagination_info()

        # attempt to navigate to next page
        if pagination_info.has_next_page:
            pagination_info.navigate_to_next_page()

        page.wait_for_timeout(1000)
