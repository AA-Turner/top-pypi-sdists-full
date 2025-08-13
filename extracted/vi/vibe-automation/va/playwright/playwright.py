import logging
import os
from contextlib import asynccontextmanager

from playwright.async_api import (
    async_playwright,
    BrowserContext,
    Page as PlaywrightPage,
)

from .page import Page as VibePage

logger = logging.getLogger(__name__)


class WrappedContext:
    """Browser context wrapper that automatically wraps pages with VibePage functionality."""

    def __init__(
        self,
        playwright_context: BrowserContext,
        playwright_pages: list[PlaywrightPage] = None,
    ):
        """Initialize WrappedContext with native Playwright objects."""
        self._playwright_context = playwright_context
        self._pages = []
        if playwright_pages:
            for page in playwright_pages:
                self._pages.append(VibePage(page))

    @property
    def pages(self):
        return self._pages

    async def _wait_for_login_tasks(self):
        """Wait for any background login tasks to complete before closing"""
        for page in self._pages:
            await page._wait_for_login_task()

    def __getattr__(self, name):
        # Forward attribute lookups to the underlying Playwright context
        attr = getattr(self._playwright_context, name)

        # Special handling for methods that return pages
        if name == "new_page":
            # Replace with our own implementation that wraps the page
            async def wrapped_new_page(*args, **kwargs):
                playwright_page = await self._playwright_context.new_page(
                    *args, **kwargs
                )
                vibe_page = VibePage(playwright_page)
                self._pages.append(vibe_page)
                return vibe_page

            return wrapped_new_page

        return attr


@asynccontextmanager
async def get_browser_context(
    headless: bool | None = None, slow_mo: float | None = None
):
    """Async version of get_browser for use in async contexts."""
    wrapped_context = None
    browser = None

    try:
        wrapped_context, browser = await create_browser_context_async(headless, slow_mo)
        yield wrapped_context
    finally:
        # Wait for any background login tasks before closing
        if wrapped_context:
            await wrapped_context._wait_for_login_tasks()

        if browser:
            await browser.close()


async def create_browser_context_async(
    headless: bool | None = None, slow_mo: float | None = None
):
    """Create a browser context using native Playwright."""
    logger.info("Creating native Playwright browser context...")

    playwright = await async_playwright().start()

    connection_url = os.environ.get("CONNECTION_URL")
    if connection_url:
        # Connect to existing browser instance via CDP
        logger.info(f"Connecting to existing browser via CDP: {connection_url}")
        browser = await playwright.chromium.connect_over_cdp(connection_url)
        # Get the default context from the connected browser
        contexts = browser.contexts
        if contexts:
            context = contexts[0]
        else:
            context = await browser.new_context()
    else:
        # Launch a new browser instance
        logger.info("Launching new browser instance")
        browser = await playwright.chromium.launch(
            headless=headless,
            slow_mo=slow_mo,
            # scale ratio is set to 1 to ensure coordinates are calculated correctly
            args=["--force-device-scale-factor=1"],
        )
        context = await browser.new_context()

    # Set default timeout
    context.set_default_timeout(3000)

    # Get existing pages and wrap them
    pages = context.pages
    wrapped_context = WrappedContext(context, pages)

    logger.info("Native Playwright browser context created successfully")
    return wrapped_context, browser
