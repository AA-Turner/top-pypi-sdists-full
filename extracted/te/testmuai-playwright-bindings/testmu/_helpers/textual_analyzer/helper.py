"""testmu.textual_analyzer — the public helper exported test code calls.

Replaces the old raw ``page.evaluate(wrapped_js, [page.locator(L).element_handle()...])``.
Per recorded locator: STRICT visibility check (small timeout). If ALL are visible,
resolve handles and run the recorded wrapped_js (the fast happy path). If ANY is
not visible, AUTOHEAL — regenerate the whole extraction (heal.run_heal) and recover
the value. If heal misses, FAIL the step (no vision fallback).
"""
from __future__ import annotations

import logging

from testmu._helpers.textual_analyzer.heal import run_heal

_log = logging.getLogger("testmu")

# Strict "visible with eyes" gate — a recorded locator must be actually visible
# within this window or we heal. Small so we don't wait the default 30s per locator.
_VISIBLE_TIMEOUT_MS = 1500


class TextualAnalyzerHealFailed(Exception):
    """Raised when a recorded locator is not visible and heal could not
    regenerate a usable extraction. The step fails (no vision fallback)."""


async def _stale_and_handles(page, locators: list[str]):
    """Return (stale_locators, handles). A locator is stale if it isn't visible
    within the timeout (strict isVisible) or can't be resolved to a handle."""
    stale: list[str] = []
    handles = []
    for loc in locators:
        target = page.locator(loc).first
        try:
            await target.wait_for(state="visible", timeout=_VISIBLE_TIMEOUT_MS)
            handle = await target.element_handle()
            if handle is None:
                stale.append(loc)
            else:
                handles.append(handle)
        except Exception:  # noqa: BLE001 — timeout / detached / strict-mode
            stale.append(loc)
    return stale, handles


async def textual_analyzer(
    page,
    *,
    wrapped_js: str,
    locators: list[str],
    query: str,
    expected_value: str | None = None,
    needs_unit_conversion: bool = False,
    operator: str = "contains",
    transforms: list[str] | None = None,
    condition: str | None = None,
    code_js: str | None = None,
):
    """Execute a recorded textual_visual extraction, healing on locator drift.

    Returns the extracted value (string, transforms applied downstream as today).
    """
    transforms = transforms or []
    stale, handles = await _stale_and_handles(page, locators)

    # Happy path — every recorded locator visible.
    if not stale and len(handles) == len(locators):
        return await page.evaluate(wrapped_js, handles)

    # Drift — regenerate the whole extraction.
    _log.info("[textual_analyzer] %d/%d locators not visible -> heal (query=%r)",
              len(stale), len(locators), query[:60])
    outcome = await run_heal(
        page, query, expected_value, needs_unit_conversion, condition, code_js,
    )
    if outcome is None:
        raise TextualAnalyzerHealFailed(
            f"textual_analyzer could not heal extraction for query={query!r}; "
            f"stale locators: {stale}"
        )

    _log.info("[textual_analyzer] healed locator drift -> %r", outcome.value)
    return outcome.value
