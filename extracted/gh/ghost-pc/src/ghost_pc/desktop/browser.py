"""Browser automation via Chrome DevTools Protocol (CDP).

Connects to Chrome's CDP endpoint for deep browser control without
pixel clicking. Falls back gracefully when CDP isn't available.

Requires Chrome/Edge launched with --remote-debugging-port=9222.
Uses Playwright for CDP communication.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

# Chrome CDP default endpoint
_CDP_URL = "http://localhost:9222"

# Lazy-loaded browser context
_browser = None
_playwright = None


async def _get_browser():
    """Lazy-connect to Chrome CDP endpoint."""
    global _browser, _playwright

    if _browser and _browser.is_connected():
        return _browser

    try:
        from playwright.async_api import async_playwright

        _playwright = await async_playwright().start()
        _browser = await _playwright.chromium.connect_over_cdp(_CDP_URL)
        logger.info("Connected to Chrome CDP at %s", _CDP_URL)
        return _browser
    except Exception as e:
        logger.debug("CDP connection failed: %s", e)
        _browser = None
        return None


async def _get_page():
    """Get the active page from the CDP-connected browser."""
    browser = await _get_browser()
    if not browser:
        return None

    contexts = browser.contexts
    if not contexts:
        return None

    pages = contexts[0].pages
    if not pages:
        return None

    return pages[0]


async def browser_navigate(url: str) -> dict[str, Any]:
    """Navigate the active tab to a URL.

    Args:
        url: The URL to navigate to.
    """
    page = await _get_page()
    if not page:
        return {
            "status": "error",
            "error": "No CDP connection. Launch Chrome with --remote-debugging-port=9222",
        }

    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=15000)
        return {"status": "ok", "url": page.url, "title": await page.title()}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def browser_get_page_text() -> dict[str, Any]:
    """Get the text content of the active page."""
    page = await _get_page()
    if not page:
        return {"status": "error", "error": "No CDP connection"}

    try:
        text = await page.evaluate("document.body.innerText")
        return {"status": "ok", "text": str(text)[:5000]}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def browser_fill_form(selector: str, value: str) -> dict[str, Any]:
    """Fill a form field by CSS selector.

    Args:
        selector: CSS selector for the input element.
        value: Value to fill in.
    """
    page = await _get_page()
    if not page:
        return {"status": "error", "error": "No CDP connection"}

    try:
        await page.fill(selector, value, timeout=5000)
        return {"status": "ok", "selector": selector, "value": value}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def browser_click_element(selector: str) -> dict[str, Any]:
    """Click an element by CSS selector.

    Args:
        selector: CSS selector for the element to click.
    """
    page = await _get_page()
    if not page:
        return {"status": "error", "error": "No CDP connection"}

    try:
        await page.click(selector, timeout=5000)
        return {"status": "ok", "selector": selector}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def browser_get_tabs() -> dict[str, Any]:
    """List all open browser tabs."""
    browser = await _get_browser()
    if not browser:
        return {"status": "error", "error": "No CDP connection"}

    try:
        tabs: list[dict[str, str | int]] = []
        for ctx in browser.contexts:
            for i, page in enumerate(ctx.pages):
                tabs.append(
                    {
                        "index": i,
                        "url": page.url,
                        "title": await page.title(),
                    }
                )
        return {"status": "ok", "tabs": tabs, "count": len(tabs)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def browser_switch_tab(index: int) -> dict[str, Any]:
    """Switch to a browser tab by index.

    Args:
        index: Tab index (0-based).
    """
    browser = await _get_browser()
    if not browser:
        return {"status": "error", "error": "No CDP connection"}

    try:
        pages = browser.contexts[0].pages
        if index < 0 or index >= len(pages):
            return {
                "status": "error",
                "error": f"Tab index {index} out of range (0-{len(pages) - 1})",
            }

        page = pages[index]
        await page.bring_to_front()
        return {"status": "ok", "index": index, "url": page.url}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def browser_execute_js(code: str) -> dict[str, Any]:
    """Execute JavaScript in the active page context.

    Args:
        code: JavaScript code to execute.
    """
    page = await _get_page()
    if not page:
        return {"status": "error", "error": "No CDP connection"}

    try:
        result = await page.evaluate(code)
        return {"status": "ok", "result": str(result)[:3000]}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def close_browser_connection() -> None:
    """Clean up the CDP connection."""
    global _browser, _playwright

    if _browser:
        try:
            await _browser.close()
        except Exception:
            pass
        _browser = None

    if _playwright:
        try:
            await _playwright.stop()
        except Exception:
            pass
        _playwright = None
