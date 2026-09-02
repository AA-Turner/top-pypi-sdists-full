"""AI-callable browser automation surface.

This module provides the **pure** browser-control primitives that any AI tool
runtime (matrx-ai, MCP server, plain async functions) can build on top of.
Everything here:

    * Owns its own Playwright lifecycle (no host dependency).
    * Returns plain dicts and dataclasses (no matrx-ai or matrx-connect imports).
    * Is JSON-serialisable — every value can flow through an MCP transport.
    * Is async-first.

The shape mirrors the 9 server-side browser tools that matrx-ai already exposes
(`browser_navigate` / `_click` / `_type_text` / `_select_option` / `_screenshot`
/ `_wait_for` / `_get_element` / `_scroll` / `_close`) plus a handful of
extractors that the AI loop tends to need when scraping fails:

    * navigate → open or reuse a session, return final URL + title + (optional) text
    * click   → CSS click; optional wait_after_ms
    * fill    → set value of an <input>/<textarea>
    * type    → type into a focused field, optional press-enter-and-wait
    * select_option → set a <select> by value or label
    * screenshot → PNG bytes (full page, viewport, or element)
    * wait_for → wait for selector or visible text
    * get_element → query an element's attrs, text, html
    * get_html → page.content()  (post-recipe, post-JS)
    * get_text → body innerText, capped
    * query_selectors → bulk pull text/attrs across many selectors at once
    * eval_js → page.evaluate() — locked-down by default; enable with allow_eval_js
    * scroll → page or element scroll
    * close → release a session

Everything else (scraping, crawling, recipes) is composed on top of this.
"""

from __future__ import annotations

from matrx_scraper.ai_browser.session import (
    BrowserSession,
    BrowserSessionManager,
    get_browser_session_manager,
)
from matrx_scraper.ai_browser.client import (
    RemoteBrowserClient,
    BrowserClientError,
)
from matrx_scraper.ai_browser.actions import (
    NavigateResult,
    ClickResult,
    FillResult,
    TypeResult,
    SelectOptionResult,
    ScreenshotResult,
    WaitForResult,
    GetElementResult,
    QuerySelectorsResult,
    EvalJsResult,
    ScrollResult,
    GetHtmlResult,
    GetTextResult,
    navigate,
    click,
    fill,
    type_text,
    select_option,
    screenshot,
    wait_for,
    get_element,
    query_selectors,
    eval_js,
    scroll,
    get_html,
    get_text,
    close as close_session,
)

__all__ = [
    # session
    "BrowserSession",
    "BrowserSessionManager",
    "get_browser_session_manager",
    # remote client (HTTP) — hosts that don't run Playwright themselves
    "RemoteBrowserClient",
    "BrowserClientError",
    # action results
    "NavigateResult",
    "ClickResult",
    "FillResult",
    "TypeResult",
    "SelectOptionResult",
    "ScreenshotResult",
    "WaitForResult",
    "GetElementResult",
    "QuerySelectorsResult",
    "EvalJsResult",
    "ScrollResult",
    "GetHtmlResult",
    "GetTextResult",
    # actions
    "navigate",
    "click",
    "fill",
    "type_text",
    "select_option",
    "screenshot",
    "wait_for",
    "get_element",
    "query_selectors",
    "eval_js",
    "scroll",
    "get_html",
    "get_text",
    "close_session",
]
