import asyncio
import json
import logging
import os

import aiofiles
from playwright.async_api import async_playwright

import agentql

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

URL = "https://www.yelp.com/"
FILE_PATH = "user_session_yelp.json"

YELP_EMAIL = ""
YELP_PASSWORD = ""

QUERY_1 = """
{
    header {
        sign_in_btn
    }
}
"""

QUERY_2 = """
{
    email_box
    password_box
    log_in_btn
}
"""

QUERY_3 = """
{
    header {
        search_box
        search_btn
    }
}
"""


async def get_user_session_state():
    async with async_playwright() as playwright, await playwright.chromium.launch(headless=False) as browser:
        page = await agentql.wrap_async(browser.new_page())
        await page.goto(URL)

        log.debug("Signing in to Yelp...")
        response = await page.query_elements(QUERY_1)
        await response.header.sign_in_btn.click()

        response = await page.query_elements(QUERY_2)
        await response.email_box.type(YELP_EMAIL)
        await response.password_box.type(YELP_PASSWORD)
        await response.log_in_btn.click()

        await page.wait_for_page_ready_state()

        # Save the user session state to a variable
        user_session = await page.context.storage_state()

        # Save the user session state to a file
        async with aiofiles.open(FILE_PATH, "w", encoding="utf-8") as f:
            await f.write(json.dumps(user_session))

        return user_session


async def main():
    # Load the user session state from variable
    user_session = await get_user_session_state()

    # Load the user session state from file
    if os.path.exists(FILE_PATH):
        async with aiofiles.open(FILE_PATH, encoding="utf-8") as file:
            content = await file.read()
            user_session = json.loads(content)

    # Start a new session with the user session state
    async with async_playwright() as playwright, await playwright.chromium.launch(headless=False) as browser:
        page = await agentql.wrap_async(browser.new_page(storage_state=user_session))
        await page.goto(URL)

        response = await page.query_elements(QUERY_3)
        await response.header.search_box.type("Best restaurants in Palo Alto")
        await response.header.search_btn.click()

        # Sleep to see the result
        await page.wait_for_timeout(10000)


if __name__ == "__main__":
    asyncio.run(main())
