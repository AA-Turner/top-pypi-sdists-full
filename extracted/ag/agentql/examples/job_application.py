import logging

from playwright.sync_api import sync_playwright

import agentql

log = logging.getLogger(__name__)

URL = "https://jobs.ashbyhq.com/ramp/a7b5b128-c024-433a-b5d7-4e7b7ed7a49d/application"

QUERY = """
{
    name_input
    email_input
    resume_upload_btn
    phone_input
    cover_letter_upload_btn
    linkedin_input
    website_input
    authorized_work_in_us {
        yes_btn
        no_btn
    }
    country_of_residence {
        other_btn
        canada_btn
        us_btn
    }
    what_ways_entrepreneurial_input
    examples_exceptional_performance_input
    submit_btn
}
"""

if __name__ == "__main__":
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        page = agentql.wrap(browser.new_page())
        page.goto(URL)
        log.debug("Analyzing...")
        response = page.query_elements(QUERY)
        response.name_input.type("Tiny Fish")
        response.email_input.type("tinyfish@tinyfish.io")
        response.authorized_work_in_us.yes_btn.click()
        page.wait_for_timeout(10000)
