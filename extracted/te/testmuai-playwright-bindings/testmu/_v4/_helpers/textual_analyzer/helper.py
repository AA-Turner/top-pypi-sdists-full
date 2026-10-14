"""testmu.textual_analyzer — the public helper exported test code calls.

Replaces the old raw ``page.evaluate(wrapped_js, [page.locator(L).element_handle()...])``.
Per recorded locator: STRICT visibility check (small timeout). If ALL are visible,
resolve handles and run the recorded wrapped_js (the fast happy path). If ANY is
not visible, AUTOHEAL — regenerate the whole extraction (heal.run_heal) and recover
the value. If heal misses, FAIL the step (no vision fallback).
"""
from __future__ import annotations

import asyncio
import logging
import os
import time

from testmu_helper.evaluation import _compare, apply_transforms

from testmu._v4._helpers.textual_analyzer.heal import run_heal

_log = logging.getLogger("testmu")

# Strict "visible with eyes" gate — a recorded locator must be actually visible
# within this window or we heal. Small so we don't wait the default 30s per locator.
_VISIBLE_TIMEOUT_MS = 1500

# A read whose answer differs from the one recorded is read again until it
# matches or the budget runs out: the page may not have caught up yet (a
# counter still updating, a run still in progress). After the budget the last
# answer is returned unchanged, so a real difference still fails downstream.
# The budget is the one the replay runner sets for this read (derived from what
# authoring observed), else TESTMU_READ_SETTLE_MS, else 15 s; never above 30 s.


def _env_settle_ms(default: int = 15_000) -> int:
    """TESTMU_READ_SETTLE_MS as an int; the default when unset or not a number."""
    try:
        return int(os.environ.get("TESTMU_READ_SETTLE_MS", ""))
    except ValueError:
        return default


_SETTLE_DEFAULT_MS = _env_settle_ms()
_SETTLE_CAP_MS = 30_000
_SETTLE_INTERVAL_S = 1.0
_settle_budget_override: int | None = None
# Operators the assertion evaluator judges (testmu_helper.evaluation._compare);
# any other operator always evaluates false there, so re-reading cannot help.
_JUDGED_OPERATORS = frozenset({
    "equals", "not_equals", "contains", "not_contains", "gt", "gte", "lt", "lte",
    "matches", "not_matches", "has_key", "true", "false",
})


def set_read_settle_budget(budget_ms: int | None) -> None:
    """Budget for the next reads' re-read loop; None restores the default."""
    global _settle_budget_override
    _settle_budget_override = None if budget_ms is None else int(budget_ms)


def _settle_budget_ms() -> int:
    budget = _settle_budget_override if _settle_budget_override is not None else _SETTLE_DEFAULT_MS
    return max(0, min(int(budget), _SETTLE_CAP_MS))


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
        value = await page.evaluate(wrapped_js, handles)
        return await _settle(page, value, wrapped_js, locators, expected_value, operator,
                             transforms, query)

    # Drift — regenerate the whole extraction.
    _log.info("[textual_analyzer] %d/%d locators not visible -> heal (query=%r)",
              len(stale), len(locators), query[:60])
    outcome = await run_heal(
        page, query, expected_value, needs_unit_conversion, condition, code_js,
    )
    if outcome is None:
        if condition:
            # This read feeds a condition (a while / if-else producer). Its
            # element is gone and nothing on the page can replace it, so the
            # condition is not met here: read false and let the caller take
            # the else branch / exit the loop. Failing the step would abort a
            # test whose recorded page simply differs from the current one.
            _log.info(
                "[textual_analyzer] heal missed for condition evidence -> 'false' (query=%r)",
                query[:60],
            )
            return "false"
        raise TextualAnalyzerHealFailed(
            f"textual_analyzer could not heal extraction for query={query!r}; "
            f"stale locators: {stale}"
        )

    _log.info("[textual_analyzer] healed locator drift -> %r", outcome.value)
    if outcome.wrapped_js and outcome.locators:
        return await _settle(page, outcome.value, outcome.wrapped_js, outcome.locators,
                             expected_value, operator, transforms, query)
    return outcome.value


def _matches(value, expected: str, operator: str, transforms: list[str]) -> bool | None:
    """Whether ``value`` passes the recorded check, judged exactly as the
    assertion evaluator judges it (recorded transforms on both sides, then
    ``_compare``); None for an operator the evaluator does not judge."""
    if operator not in _JUDGED_OPERATORS:
        return None
    actual = apply_transforms("" if value is None else str(value), transforms, None)
    wanted = apply_transforms(str(expected), transforms, None)
    return _compare(actual, wanted, operator)


async def _settle(page, value, wrapped_js, locators, expected_value, operator, transforms, query):
    """Re-read until the recorded expected answer holds, within the budget."""
    budget_ms = _settle_budget_ms()
    if expected_value in (None, "") or budget_ms <= 0:
        return value
    operator = operator or "contains"
    transforms = transforms or []
    if _matches(value, expected_value, operator, transforms) is not False:
        return value
    started = time.monotonic()
    deadline = started + budget_ms / 1000
    reads = 1
    while time.monotonic() < deadline:
        await asyncio.sleep(_SETTLE_INTERVAL_S)
        stale, handles = await _stale_and_handles(page, locators)
        if stale or len(handles) != len(locators):
            continue
        try:
            value = await page.evaluate(wrapped_js, handles)
        except Exception as e:  # noqa: BLE001 — a re-read that throws keeps the last answer
            _log.debug("[textual_analyzer] re-read failed: %s", e)
            continue
        reads += 1
        if _matches(value, expected_value, operator, transforms):
            _log.info("[textual_analyzer] answer settled after %d reads / %.1fs -> %r (query=%r)",
                      reads, time.monotonic() - started, value, query[:60])
            return value
    _log.info("[textual_analyzer] answer did not settle in %.0fs (%d reads) -> %r (query=%r)",
              budget_ms / 1000, reads, value, query[:60])
    return value
