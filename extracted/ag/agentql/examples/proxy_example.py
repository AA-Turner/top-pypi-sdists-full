import logging

from playwright.sync_api import ProxySettings, sync_playwright

import agentql

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

proxy = {
    "server": "https://someproxy.com:8010",
    "username": "user",
    "password": "password",
}
QUERY = """
{
    public_ip_address
}
"""

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, proxy=ProxySettings(**proxy))
    page = agentql.wrap(browser.new_page())
    page.goto("https://www.google.com/search?q=whats+my+ip+google")

    response = page.query_data(QUERY)
    log.debug(response)
    browser.close()
