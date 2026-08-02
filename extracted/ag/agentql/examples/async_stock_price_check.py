import asyncio
import json
import logging

from playwright.async_api import async_playwright

import agentql
from agentql import BaseAgentQLError

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

stocks = [
    "Tesla stock price",
    "Apple stock price",
    "Google stock price",
    "Amazon stock price",
]

QUERY_1 = """
{
    search_box
    search_btn
}
"""

QUERY_2 = """
{
    stock_price
}
"""


async def query_url(stock):
    try:
        async with async_playwright() as playwright, await playwright.chromium.launch(headless=False) as browser:
            page = await agentql.wrap_async(browser.new_page())
            await page.goto("https://www.google.com")
            response = await page.query_elements(QUERY_1)

            await response.search_box.type(stock)
            await response.search_btn.click()

            data = await page.query_data(QUERY_2)
            result = {
                "stock": stock,
                "price": data["stock_price"],
            }
            return result
    except BaseAgentQLError as e:
        return {"error": str(e)}


async def main():
    tasks = [query_url(stock) for stock in stocks]
    data_list = await asyncio.gather(*tasks)

    log.debug(json.dumps(data_list, indent=4))


if __name__ == "__main__":
    asyncio.run(main())
