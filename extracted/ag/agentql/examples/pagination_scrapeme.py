import json
import logging

from playwright.sync_api import sync_playwright

import agentql
from agentql.tools.sync_api import paginate

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

if __name__ == "__main__":
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        page = agentql.wrap(browser.new_page())
        page.goto("https://scrapeme.live/shop/")

        QUERY = """
        {
            items[] {
                title
            }
        }
        """
        paginated_data = paginate(page, QUERY, 3)

        with open("./scrapeme_paginated_data.json", "w") as f:
            json.dump(paginated_data, f, indent=4)
        log.debug("Paginated data has been saved to scrapeme_paginated_data.json")
