"""Recipe action runtime.

Executes a `CrawlRecipe` action list against a Playwright `Page` object.

Screenshot capture lives in ``matrx_scraper.browser_pool.capture_screenshots``
(shared by ``fetch_with_capture`` and callers that own their own navigation).
This module only runs recipe actions.

This module is optional and accepts the Playwright page structurally, so merely
importing it does not pull Playwright into non-browser crawls.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from matrx_scraper.recipes import RecipeAction

logger = logging.getLogger(__name__)


async def execute_directives(page: Any, actions: list[RecipeAction]) -> list[str]:
    """Run a recipe action list against a Playwright page.

    Returns a list of one-line "result strings" per action (success or
    short error) so the caller can surface what happened to the user.
    """
    results: list[str] = []
    for a in actions:
        try:
            r = await _run_one(page, a)
            results.append(r)
        except Exception as exc:
            msg = f"{a.type} failed: {type(exc).__name__}: {exc}"
            logger.info("recipe action %s on page %s — %s", a.type, getattr(page, "url", "?"), msg)
            results.append(msg)
    return results


async def _run_one(page: Any, a: RecipeAction) -> str:
    if a.type == "click" and a.selector:
        try:
            await page.locator(a.selector).first.click(timeout=a.timeout_ms or 5000)
            return f"click ok: {a.selector}"
        except Exception:
            return f"click skipped (no match): {a.selector}"
    if a.type == "wait_for" and a.selector:
        await page.wait_for_selector(a.selector, timeout=a.timeout_ms or 10_000)
        return f"wait_for ok: {a.selector}"
    if a.type == "scroll_to_bottom":
        steps = a.steps or 6
        delay = a.delay_ms or 250
        for _ in range(steps):
            await page.evaluate("window.scrollBy(0, window.innerHeight)")
            await asyncio.sleep(delay / 1000.0)
        return f"scroll_to_bottom ok: {steps} steps"
    if a.type == "scroll_by" and a.px:
        await page.evaluate(f"window.scrollBy(0, {int(a.px)})")
        return f"scroll_by ok: {a.px}px"
    if a.type == "remove" and a.selector:
        # Best-effort — set display:none on every match.
        await page.evaluate(
            "(s) => document.querySelectorAll(s).forEach(el => el.style.display = 'none')",
            a.selector,
        )
        return f"remove ok: {a.selector}"
    if a.type == "set_value" and a.selector:
        await page.locator(a.selector).first.fill(a.value or "")
        return f"set_value ok: {a.selector}"
    if a.type == "press" and a.key:
        await page.keyboard.press(a.key)
        return f"press ok: {a.key}"
    if a.type == "evaluate" and a.script:
        await page.evaluate(a.script)
        return "evaluate ok"
    if a.type == "sleep" and a.ms:
        await asyncio.sleep(a.ms / 1000.0)
        return f"sleep ok: {a.ms}ms"
    return f"skip (unknown or incomplete action): {a.type}"


__all__ = ["execute_directives"]
