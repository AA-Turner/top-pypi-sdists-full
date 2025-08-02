import asyncio
import logging
import os
from contextlib import asynccontextmanager, contextmanager

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


def get_browser(headless: bool | None = None, slow_mo: float | None = None):
    """Get browser - use get_browser_sync for sync contexts or get_browser_async for async contexts"""
    # For backward compatibility, try to detect if we're in async context
    import asyncio

    try:
        asyncio.get_running_loop()
        # We're in an async context, but this function is sync
        # We'll return the sync version and let the user handle async properly
        return get_browser_sync(headless, slow_mo)
    except RuntimeError:
        # No event loop, use sync version
        return get_browser_sync(headless, slow_mo)


@contextmanager
def get_browser_sync(headless: bool | None = None, slow_mo: float | None = None):
    """Recommended way to get a Playwright browser instance in Vibe Automation Framework.

    There are three running modes:
    1. during local development, we can get a local browser instance
    2. in managed execution environment, the browser instance are provided by Orby. This is
       activated via the presence of CONNECTION_URL.
    Returns a wrapped browser that automatically wraps pages with VibePage functionality
    when new_page() is called, eliminating the need for manual wrap() calls.
    """
    try:
        wrapped_context, browser = asyncio.run(
            create_browser_context_async(headless, slow_mo)
        )
        yield wrapped_context
    finally:
        # Wait for any background login tasks before closing
        asyncio.run(wrapped_context._wait_for_login_tasks())
        asyncio.run(browser.close())


@asynccontextmanager
async def get_browser_context(
    headless: bool | None = None, slow_mo: float | None = None
):
    """Async version of get_browser for use in async contexts."""

    try:
        wrapped_context, browser = await create_browser_context_async(headless, slow_mo)
        yield wrapped_context
    finally:
        # Wait for any background login tasks before closing
        await wrapped_context._wait_for_login_tasks()
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
