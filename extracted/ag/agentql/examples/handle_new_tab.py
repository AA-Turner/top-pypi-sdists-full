import logging

from playwright.sync_api import sync_playwright

import agentql

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


if __name__ == "__main__":
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        page = agentql.wrap(browser.new_page())
        page.goto(
            "https://playwright.dev/docs/api/class-browserserver",
        )

        QUERY = """
        {
            promise_link
        }
        """

        log.debug("Analyzing...")

        response = page.query_elements(QUERY)

        # In some rare cases, we may need to explicitly wait for the new tab to open. The following code will wait for tab to open before proceeding.
        with page.context.expect_page() as new_page:
            response.promise_link.click()

        # The new tab is now open and we can interact with it.
        page = agentql.wrap(new_page.value)
        page.wait_for_page_ready_state()

        page.screenshot(path="new_tab_screenshot.png")
