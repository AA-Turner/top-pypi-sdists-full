"""Find → act → heal loop for Playwright verbs.

Behavioural parity with testmu_selenium._action_engine._run_action, adapted
to async Playwright and to the 2-tier cascade (COORDINATE → VISION_QUERY).

Public entry point: _run_verb(page, locator, verb_spec, *args, ...). Callers
are:
  - VisionLocator methods (empty-selector vision-agent ops; locator=None)
  - The Locator monkey-patch (locator-method timeout; locator=<original>)

Flow per attempt:
  1. If locator is not None: try ``await verb_spec.runner(locator, *args, **kwargs)``.
     Success → return. Recoverable failure → fall to step 2.
  2. Run the heal cascade (verb-specific tiers if overridden).
  3. Cascade returned selector_xpath (preferred, even when coordinates are also
     set) → rebuild locator = ``page.locator(xpath)``, retry; coordinates stay
     stashed as the in-round fallback.
  4. Cascade returned coordinates only → dispatch ``verb_spec.coord_runner(page, x, y, *args, **kwargs)``.
     No coord_runner → NotImplementedError (caller's verb spec is broken).

Repeat up to ``max_attempts``. Final attempt re-raises the first recoverable
exception; full-cascade-miss propagates AutohealExhausted.
"""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Callable, Optional

from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from testmu._errors import AutohealExhausted
from testmu._heal_cascade import HealResult, _heal_cascade

_log = logging.getLogger("testmu.action_engine")

# Default recoverable set — Playwright's timeout class plus the stdlib alias
# (some Playwright internals raise the latter on cancelled awaits).
_DEFAULT_RECOVERABLE: tuple = (PlaywrightTimeoutError, TimeoutError)


@dataclass(frozen=True)
class _VerbSpec:
    """Per-verb behaviour for the find→act→heal loop.

    ``runner``: async callable that performs the verb on a Locator.
        Signature: ``async (locator, *args, **kwargs) -> Any``.

    ``coord_runner``: optional async callable for COORDINATE-tier hits.
        Signature: ``async (page, x: int, y: int, *args, **kwargs) -> Any``.
        Verbs that can't be performed by pixel coords (e.g. scroll_into_view)
        leave this None and override ``tiers`` to exclude COORDINATE.

    ``recoverable_exceptions``: exception types that trigger heal. Defaults
        to (PlaywrightTimeoutError, TimeoutError). Other exceptions propagate
        immediately without entering the cascade.

    ``tiers``: per-verb cascade override (e.g. scroll_into_view uses
        ('VISION_QUERY',) — no COORDINATE). None = use cascade defaults.
    """
    runner: Callable
    coord_runner: Optional[Callable] = None
    recoverable_exceptions: tuple = _DEFAULT_RECOVERABLE
    tiers: Optional[tuple[str, ...]] = None


def _coerce_to_page(page):
    """Return a Playwright Page for *page*, recovering it from a frame/shadow
    scope when codegen hands one in where a Page is required.

    The engine operates on the viewport — screenshots, ``page.mouse`` and the
    dead-page guard ``page.is_closed()`` — so it needs the owning Page. Codegen
    can pass a scope instead: e.g. ``_resolve_ranked_locator(frame_N, ...)``
    exhausting to ``testmu.locator(frame_N, ...)`` for a nested shadow/iframe
    element. ``frame_N`` is a Locator (shadow) or FrameLocator (iframe); both
    belong to the same top-level Page. Without this, the guard raised
    ``'Locator' object has no attribute 'is_closed'``.

    Recovery uses public Playwright accessors:
      - Page is the only one of the three exposing ``is_closed`` → use as-is.
      - ``Locator.page`` → owning Page.
      - ``FrameLocator.owner`` (a Locator) → ``.page``.
    If nothing resolves, return the original so the caller's error surfaces
    unchanged rather than being masked.
    """
    if hasattr(page, "is_closed"):
        return page
    recovered = getattr(page, "page", None)
    if recovered is None:
        recovered = getattr(getattr(page, "owner", None), "page", None)
    if recovered is not None and hasattr(recovered, "is_closed"):
        return recovered
    return page


def _engine_selector(selector: str) -> str:
    """Pin the correct Playwright engine for a heal-derived selector.

    ``page.locator()`` defaults to the CSS engine and only auto-detects xpath for
    selectors starting with ``//`` or ``..``. Heal can yield an absolute xpath
    (``/html[1]/...``) or a union xpath (``(//a|//b)[1]``) that would otherwise be
    parsed as CSS and raise ``Unexpected token "/" while parsing css selector``.

    - Already engine-pinned (``xpath=`` / ``css=``) → returned unchanged.
    - xpath-shaped (starts with ``/`` or ``(``; a CSS selector never does) →
      prefixed with the ``xpath=`` engine. ``//`` / ``..`` would auto-detect, but
      prefixing them is equally valid and keeps the rule simple.
    - anything else (``#id``, ``.cls``, ``[attr]``, ``div > span`` …) → returned
      unchanged so genuine CSS heal selectors keep working.
    """
    if selector.startswith(("xpath=", "css=")):
        return selector
    if selector.startswith(("/", "(")):
        return f"xpath={selector}"
    return selector


async def _run_verb(
    page,
    locator,
    verb_spec: _VerbSpec,
    *args,
    description: str,
    verb_name: str,
    autoheal: bool = True,
    max_attempts: int = 4,
    retry_delay: float = 0.5,
    fallback_coordinates: "Optional[tuple[int, int]]" = None,
    **kwargs,
) -> Any:
    """Execute ``verb_spec`` on ``locator`` (or via heal if locator is None),
    retrying with heal cascade on recoverable failures.

    Sets the heal-patch re-entry guard for its duration so verb runners can
    safely call ``await locator.click(...)`` without re-triggering the
    monkey-patched wrapper that called us in the first place.

    Args:
        page: Playwright Page (needed for cascade + coord_runner).
        locator: Playwright Locator or None. None means "no prior locator,
            go straight to heal" (VisionLocator entry).
        verb_spec: The verb's runner + coord_runner + tiers configuration.
        description: Human-readable element intent (forwarded to cascade).
        verb_name: Method name forwarded as operation_type in heal payload.
        autoheal: When False, raise immediately on recoverable failure
            instead of running the cascade.
        max_attempts: Maximum total attempts (including the first try).
        retry_delay: Sleep between attempts on selector-tier rebuild.
        fallback_coordinates: Authoring-time coordinates persisted by codegen
            for selectorless ops (spec §3.4). Consumed ONLY when the cascade
            exhausts (AutohealExhausted) — dispatches coord_runner at the
            recorded coords as the true last resort. Never forwarded to
            runner or coord_runner.
        *args, **kwargs: Forwarded verbatim to runner and coord_runner.

    Returns: runner's return value (or coord_runner's, on COORDINATE hit).
    Raises: AutohealExhausted (cascade miss); the first recoverable
        exception (loop exhausted while keeping recovering selectors).
    """
    first_exc: Optional[Exception] = None

    # Set the re-entry guard for the heal patch so verb runners' calls into
    # Locator methods bypass the wrapper. Reset on exit (even on raise).
    from testmu._heal_patch import _in_engine
    _token = _in_engine.set(True)
    try:
        return await _run_verb_inner(
            page, locator, verb_spec, *args,
            description=description, verb_name=verb_name,
            autoheal=autoheal, max_attempts=max_attempts,
            retry_delay=retry_delay, first_exc=first_exc,
            fallback_coordinates=fallback_coordinates, **kwargs,
        )
    finally:
        _in_engine.reset(_token)


async def _run_verb_inner(
    page,
    locator,
    verb_spec: _VerbSpec,
    *args,
    description: str,
    verb_name: str,
    autoheal: bool,
    max_attempts: int,
    retry_delay: float,
    first_exc: Optional[Exception],
    fallback_coordinates: "Optional[tuple[int, int]]" = None,
    **kwargs,
) -> Any:
    """Body of _run_verb. Extracted so the re-entry guard wraps the whole
    cascade lifecycle without indenting everything one more level."""

    # Defensive: a caller may hand us a frame/shadow scope (Locator/FrameLocator)
    # where a Page is required — e.g. _resolve_ranked_locator(frame_N, ...)
    # exhausting to testmu.locator(frame_N, ...) for a nested shadow/iframe op.
    # Recover the owning Page so the viewport guard/cascade/coord_runner work
    # instead of crashing on page.is_closed(). See _coerce_to_page.
    page = _coerce_to_page(page)

    # Stash for a heal round that returned both selector_xpath AND coordinates.
    # Set when the xpath path is taken so the next recoverable failure can fall
    # back to the same round's coordinates without a second cascade call (spec §3.3).
    pending_coord_fallback: Optional[tuple[int, int]] = None

    # Pre-action guard: if the page died (e.g. a popup that self-closed), re-point to
    # the most-recently-opened surviving page and null the stale locator so the cascade
    # re-discovers the element on the live page. Mirrors the Selenium dead-window heal
    # (switch to the last/most-recent surviving window, not the first).
    if page.is_closed():
        ctx_pages = page.context.pages
        if not ctx_pages:
            raise RuntimeError(
                f"all pages are closed; cannot perform {verb_name!r} on {description!r}"
            )
        page = ctx_pages[-1]
        await page.bring_to_front()
        locator = None  # locator was bound to the dead page — force cascade re-discovery

    for attempt in range(max_attempts):
        # Step 1 — try the verb on the current locator (skip if VisionLocator entry).
        if locator is not None:
            try:
                return await verb_spec.runner(locator, *args, **kwargs)
            except verb_spec.recoverable_exceptions as exc:
                if first_exc is None:
                    first_exc = exc
                if not autoheal:
                    raise
                # A previous heal round produced both a derived xpath and fresh
                # coordinates; the xpath attempt just failed. Fall back to the
                # same round's coordinates instead of re-entering the cascade —
                # one /v2/locate/desktop call serves both attempts (spec §3.3).
                # Checked BEFORE the final-attempt raise (selenium parity): the
                # stash must fire even when this was the last allowed attempt.
                if pending_coord_fallback is not None and verb_spec.coord_runner is not None:
                    x, y = pending_coord_fallback
                    _log.info(
                        "[engine] derived-xpath attempt failed (%s); coordinate fallback (%d, %d) for %s",
                        type(exc).__name__, x, y, verb_name,
                    )
                    return await verb_spec.coord_runner(page, x, y, *args, **kwargs)
                if attempt == max_attempts - 1:
                    # Last allowed attempt — propagate without entering cascade
                    # again. Mirrors Selenium _run_action's final-attempt branch.
                    raise

        elif not autoheal:
            # locator is None AND autoheal is off — there's literally nothing
            # to do. The caller asked for heal-disabled lookup of a bare
            # description; we have to surface that.
            raise AutohealExhausted(
                f"no locator and autoheal disabled for {description!r} ({verb_name})"
            )

        # Step 2 — heal cascade.
        # Wrap in try/except to honour fallback_coordinates on exhaustion (spec §3.4).
        try:
            heal: HealResult = await _heal_cascade(
                page=page,
                description=description,
                verb_name=verb_name,
                current_selector=None,
                tiers=verb_spec.tiers,
                last_exception=first_exc,
            )
        except AutohealExhausted as heal_exc:
            # Codegen-marked op: the API found nothing ([0,0]);
            # recorded authoring-time coordinates are the true last resort.
            if fallback_coordinates is not None and verb_spec.coord_runner is not None:
                x, y = fallback_coordinates
                _log.info(
                    "[engine] cascade exhausted (%s); recorded fallback_coordinates (%d, %d) for %s",
                    type(heal_exc).__name__, x, y, verb_name,
                )
                return await verb_spec.coord_runner(page, x, y, *args, **kwargs)
            raise

        # Step 3 — dispatch based on what the cascade returned.
        # Selector-first: when both fields are populated, take the xpath path
        # and keep coordinates as the in-round fallback (spec §3.3).
        if heal.selector_xpath is not None:
            # Pin the right Playwright engine for the heal-derived selector. A
            # heal xpath is usually absolute ('/html[1]/...') which page.locator()
            # would parse as CSS ("Unexpected token \"/\""); CSS selectors pass
            # through to Playwright's default engine. See _engine_selector.
            locator = page.locator(_engine_selector(heal.selector_xpath))
            # Stash fresh coordinates for the fallback; reset stash each heal round
            # (fresh coordinates supersede stale ones).
            pending_coord_fallback = heal.coordinates  # may be None — that's fine
            _log.info(
                "[engine] heal via %s → selector %r, retrying %s",
                heal.tier_used, heal.selector_xpath, verb_name,
            )
            if retry_delay > 0:
                await asyncio.sleep(retry_delay)
            continue  # retry the verb on the new locator

        elif heal.coordinates is not None:
            # Coordinates-only (resolver returned None — shadow DOM / iframe /
            # verify failure): dispatch via coord_runner immediately.
            # Reset stash since this heal round produced no xpath.
            pending_coord_fallback = None
            if verb_spec.coord_runner is None:
                raise NotImplementedError(
                    f"heal cascade resolved to coordinates {heal.coordinates} "
                    f"via tier {heal.tier_used!r}, but verb {verb_name!r} has "
                    f"no coord_runner. Either provide one on the _VerbSpec or "
                    f"drop COORDINATE from this verb's tiers."
                )
            x, y = heal.coordinates
            _log.info(
                "[engine] heal via %s → coord_runner at (%d, %d) for %s",
                heal.tier_used, x, y, verb_name,
            )
            return await verb_spec.coord_runner(page, x, y, *args, **kwargs)

        else:
            # HealResult should never reach here (a hit must set at least one
            # of selector_xpath/coordinates), but surface the invariant violation.
            raise AutohealExhausted(
                f"heal tier={heal.tier_used} returned no selector or coordinates "
                f"for {description!r} ({verb_name})"
            )

    # Loop completed without success. If we have a recoverable exception
    # stashed, re-raise it; otherwise it was a VisionLocator entry that
    # exhausted (which means the cascade kept returning selectors that
    # also timed out).
    if first_exc is not None:
        raise first_exc
    raise AutohealExhausted(
        f"max_attempts={max_attempts} exhausted for {description!r} ({verb_name})"
    )
