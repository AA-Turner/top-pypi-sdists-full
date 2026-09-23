"""THE ONE definition of "this element is ready to be acted on".

Every browser action that asks *is this element there and usable?* asks it here.
That is the whole point of the module: the package used to carry two answers that
disagreed, and the disagreement was invisible until an agent hit it.

  * ``actions.get_element`` did ``query_selector`` + ``bounding_box()`` with no
    visibility check at all, so a ``visibility:hidden`` input was reported
    ``found=True`` with a full bounding box — present and, by implication,
    usable;
  * ``humanize._target_box`` waited for Playwright ``state="visible"``, so the
    very same element made ``type_text`` wait out its whole timeout.

An agent that probes a field, is told it is there, and then cannot type into it
has been told something untrue by its own tools. So there is ONE definition and
it is the honest one: **usable means an element a person could actually aim at**
— attached, visible, and at least one pixel in each direction. Anything weaker
promises something the input path will refuse.

The verdict distinguishes ABSENT from PRESENT-BUT-NOT-USABLE, because those need
different remedies: a wrong selector versus a field the page has not revealed
yet.

Playwright lives behind the ``browser`` extra and is never imported here; a
timeout is classified by exception NAME, exactly as ``actions._failure_type``
does.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)

#: How long ``get_element`` waits for a match to become visible. A probe is not
#: an action: it answers quickly and honestly rather than sitting on the page's
#: full action timeout. (Never 0 — Playwright reads 0 as "no timeout at all".)
PROBE_TIMEOUT_MS = 1_000

#: Measuring is not waiting. ``timeout_ms`` is what the caller will WAIT for the
#: element to appear; scrolling it into view and reading its box happen after
#: that and get their own small allowance on top. Splitting the caller's budget
#: between the two instead would mean an element that appears late — but inside
#: the budget — is reported unusable anyway, because nothing is left to measure
#: it with: the probe failing exactly the case it exists to catch.
MEASURE_ALLOWANCE_SECONDS = 2.0

#: How long the "is it in the DOM at all" fallback may take. It runs only after
#: the probe above already timed out, so it gets a small slice, never
#: Playwright's 30-second page default on top of a budget already spent.
PRESENCE_CHECK_SECONDS = 2.0

#: The minimum box a pointer can be aimed at. Below this there is nothing to
#: click, hover or type into, whatever the DOM says.
MIN_TARGET_PX = 1.0

#: Every verdict word this module can return. A reason is never free text.
READINESS_REASONS = frozenset({"ready", "absent", "not_visible", "zero_size", "probe_failed"})


@dataclass(frozen=True)
class ElementReadiness:
    """What the ONE definition says about one selector on one page."""

    #: The selector matches something in the DOM.
    present: bool
    #: A person could aim at it: attached, visible, and big enough. This is the
    #: bar every input action applies, so it is the bar every probe reports.
    usable: bool
    #: The aim-able box, present only when ``usable``.
    box: dict[str, float] | None
    #: One word from ``READINESS_REASONS`` saying which of the two it is and why.
    reason: str

    @property
    def found(self) -> bool:
        """The word the action results use. Deliberately the same thing as
        ``usable`` — "found" must never mean "there but you cannot touch it"."""
        return self.usable


def _is_timeout(exc: BaseException) -> bool:
    return type(exc).__name__ == "TimeoutError"


async def _is_present(page: Any, selector: str) -> bool:
    """Is it in the DOM at all — bounded, because this runs AFTER a timeout.

    ``query_selector`` takes no timeout argument, so it inherits Playwright's
    30-second page default. On a page that is already too busy to answer, that
    default is spent on top of the probe that just timed out.
    """
    try:
        async with asyncio.timeout(PRESENCE_CHECK_SECONDS):
            return await page.query_selector(selector) is not None
    except Exception:  # pragma: no cover - a dead or wedged page is not "present"
        return False


async def element_readiness(page: Any, selector: str, *, timeout_ms: int) -> ElementReadiness:
    """The one readiness verdict. Never raises on an ordinary miss or timeout."""
    try:
        # 🚨 ONE BUDGET FOR THE WHOLE PROBE. Each step below carries its own
        # timeout, so three of them could cost 3x what the caller asked for —
        # and ``bounding_box()`` takes NO timeout argument at all, so it falls
        # back to Playwright's 30-second page default. On the signed-in
        # production `/staff` page that was enough for a `get_element` asking
        # for a ONE-SECOND probe to run 55.4 s and be killed by the worker's
        # command ceiling (observed 2026-09-21, run a7890d21). A probe may
        # never cost more than the timeout it was given.
        async with asyncio.timeout(max(timeout_ms, 1) / 1000 + MEASURE_ALLOWANCE_SECONDS):
            # Resolving the locator is inside the try on purpose: a page object
            # that cannot be probed at all must produce the ``probe_failed``
            # VERDICT, not an exception. A readiness probe that raises would
            # turn every action that consults it into an error on pages it
            # simply could not examine.
            #
            locator = page.locator(selector).first
            await locator.wait_for(state="visible", timeout=timeout_ms)
            await locator.scroll_into_view_if_needed(timeout=timeout_ms)
            box = await locator.bounding_box()
    except Exception as exc:
        if not _is_timeout(exc):
            logger.warning(
                "readiness probe for %r failed with %s", selector, type(exc).__name__
            )
            return ElementReadiness(
                present=False, usable=False, box=None, reason="probe_failed"
            )
        present = await _is_present(page, selector)
        return ElementReadiness(
            present=present,
            usable=False,
            box=None,
            reason="not_visible" if present else "absent",
        )
    if not box or box["width"] < MIN_TARGET_PX or box["height"] < MIN_TARGET_PX:
        return ElementReadiness(present=True, usable=False, box=None, reason="zero_size")
    return ElementReadiness(
        present=True,
        usable=True,
        box={str(k): float(v) for k, v in box.items()},
        reason="ready",
    )
