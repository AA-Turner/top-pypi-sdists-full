import pytest
import pytest_asyncio
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

import agentql
from agentql.ext.playwright._driver_constants import AGENTQL_PAGE_INSTANCE_KEY


@pytest_asyncio.fixture
async def playwright_page_async():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        yield page
        await browser.close()


@pytest.fixture
def playwright_page_sync():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        yield page
        browser.close()


@pytest.mark.asyncio
async def test_page_ref_is_set_async(playwright_page_async):
    assert not hasattr(playwright_page_async, AGENTQL_PAGE_INSTANCE_KEY)
    agentql_page = await agentql.wrap_async(playwright_page_async)
    assert getattr(playwright_page_async, AGENTQL_PAGE_INSTANCE_KEY) is agentql_page


def test_page_ref_is_set_sync(playwright_page_sync):
    assert not hasattr(playwright_page_sync, AGENTQL_PAGE_INSTANCE_KEY)
    agentql_page = agentql.wrap(playwright_page_sync)
    assert getattr(playwright_page_sync, AGENTQL_PAGE_INSTANCE_KEY) is agentql_page


@pytest.mark.asyncio
async def test_no_new_wrapper_playwright_page_async(playwright_page_async):
    """Make sure same agentql page is returned if we pass same Playwright page."""
    agentql_page1 = await agentql.wrap_async(playwright_page_async)
    agentql_page2 = await agentql.wrap_async(playwright_page_async)
    assert agentql_page1 is agentql_page2


def test_no_new_wrapper_playwright_page_sync(playwright_page_sync):
    """Make sure same agentql page is returned if we pass same playwright page."""
    agentql_page1 = agentql.wrap(playwright_page_sync)
    agentql_page2 = agentql.wrap(playwright_page_sync)
    assert agentql_page1 is agentql_page2


@pytest.mark.asyncio
async def test_no_new_wrapper_agentql_page_async(playwright_page_async):
    """Make sure same agentql page is returned if we pass same agentql page."""
    agentql_page1 = await agentql.wrap_async(playwright_page_async)
    agentql_page2 = await agentql.wrap_async(agentql_page1)
    assert agentql_page1 is agentql_page2


def test_no_new_wrapper_agentql_page_sync(playwright_page_sync):
    """Make sure same agentql page is returned if we pass same agentql page."""
    agentql_page1 = agentql.wrap(playwright_page_sync)
    agentql_page2 = agentql.wrap(agentql_page1)
    assert agentql_page1 is agentql_page2
