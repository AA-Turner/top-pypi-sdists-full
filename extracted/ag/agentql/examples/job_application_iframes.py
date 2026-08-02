import logging

from playwright.sync_api import sync_playwright

import agentql

log = logging.getLogger(__name__)

URL = "https://www.alarm.com/about/open-positions.aspx"

QUERY = """
{
    first_name_input
}
"""

if __name__ == "__main__":
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        page = agentql.wrap(browser.new_page())
        page.goto(URL)
        log.debug("Open the first open position")
        the_first_open_position = page.get_by_prompt("the first open position title")
        if not the_first_open_position:
            log.error("No open positions found")
            exit(1)

        the_first_open_position.click()
        page.wait_for_page_ready_state()
        log.debug("Analyzing...")
        response = page.query_elements(QUERY)
        response.first_name_input.type("Tiny Fish")
        page.wait_for_page_ready_state()
        page.wait_for_timeout(10000)
