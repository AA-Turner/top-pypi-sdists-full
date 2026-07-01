"""Internal find+heal+act engine used by high-level action wrappers.

Public API to the rest of the package: _ActionSpec dataclass + _run_action.
Public API of the package: the per-verb wrappers in _action_click.py and
_action_type.py — they're the only thing codegen and human test authors see.
"""
import logging
import time
from dataclasses import dataclass
from typing import Any, Callable

_log = logging.getLogger(__name__)

from selenium.common.exceptions import (
    NoSuchElementException, StaleElementReferenceException,
    ElementClickInterceptedException, ElementNotInteractableException, TimeoutException,
    NoSuchWindowException,
)

from testmu_selenium._errors import AutohealExhausted
from testmu_selenium._helpers.find_element import findElement
from testmu_selenium._heal_cascade import _heal_cascade
from testmu_selenium._helpers.smart_wait import SmartWait
from testmu_selenium._step import _current_step


# Relocate cascade for element actions (click/type/search/hover/...). TEXTUAL_QUERY
# is intentionally absent: textual-query autoheal belongs only to the textual_query
# action's _direct_textual_read (the /v1/heal/textual_query value read), not to the
# relocate cascade — the endpoint returns a read value, not a locator.
#
# Tier is DESKTOP_LOCATE only: viewport screenshot + POST to /v2/locate/desktop.
# The unified resolver is viewport-aware, DOM-independent (heals canvas / shadow-DOM /
# iframe targets), and fails honestly when the element is genuinely absent.
# VISION_QUERY (the legacy /v1/heal/vision selector path) and LIST_XPATHS are
# removed from the default cascade — LIST_XPATHS returns a plausible DOM xpath even
# when the real target is gone (false-pass, observed in production), and
# VISION_QUERY is subsumed by DESKTOP_LOCATE's combined vision+locate pass.
# Both tier implementations still exist and can be opted into via an explicit
# tiers= argument (e.g. scroll_into_view keeps VISION_QUERY + LIST_XPATHS).
_DEFAULT_HEAL_TIERS = ('DESKTOP_LOCATE',)

# Default recoverable set — covers the common stale/intercepted/timeout cases
# wrappers can extend or shrink this via their own _ActionSpec.
_DEFAULT_RECOVERABLE = (
    NoSuchElementException, StaleElementReferenceException,
    ElementClickInterceptedException, ElementNotInteractableException,
    TimeoutException,
)


@dataclass(frozen=True)
class _ActionSpec:
    """Describes how to run a single high-level action verb.

    runner: takes (element, ctx_dict) and performs the verb. ctx_dict
            includes 'driver' plus any wrapper-specific kwargs.
    recoverable_exceptions: tuple of exception types that trigger a heal
            attempt. Other exceptions propagate immediately.
    coord_runner: optional fallback dispatched when the heal cascade
            resolves to viewport pixel coordinates (HealResult.coordinates,
            DESKTOP_LOCATE tier) rather than a real CSS/XPath. Signature:
            coord_runner(driver, x, y, ctx) -> Any. Verbs that omit it
            cause _run_action to raise NotImplementedError when a coordinate
            heal fires — preferred over silently propagating a placeholder
            back into findElement (pre-2026-05-01 behaviour).
    """
    runner: Callable[[Any, dict], Any]
    recoverable_exceptions: tuple = _DEFAULT_RECOVERABLE
    coord_runner: Callable[[Any, int, int, dict], Any] | None = None
    op_type: str = "click"


def _heal_stale_window(driver) -> None:
    """Re-point the driver to a surviving window if the current handle is dead.

    A page can open a popup/tab and close it via JS ``window.close()``; Selenium
    then stays bound to the dead handle — it does NOT auto-follow the browser's
    visual focus — and the next command raises ``NoSuchWindowException``.

    Only heal when Selenium reports the current handle as genuinely dead (raises).
    A live popup's current handle can be transiently absent from a ``window_handles``
    snapshot without being dead — that ambiguous signal is NOT enough to steal focus
    away from the tab the test is working on.

    Re-point to the MOST-RECENTLY-OPENED surviving window (``window_handles[-1]``),
    not the first. The newest window is the popup the test just opened and is
    acting on, so the switch lands where focus already is; ``[0]`` (the opener)
    would jump to the wrong tab. For a self-closed single popup the only survivor
    is the opener, so ``[-1]`` == ``[0]`` there.
    """
    try:
        driver.current_window_handle
    except NoSuchWindowException:
        handles = list(driver.window_handles)
        if handles:
            driver.switch_to.window(handles[-1])
            _log.info("    [window] re-pointed to surviving window after dead handle: %s", handles[-1])


def _run_action(
    driver,
    spec: _ActionSpec,
    primary_selector,
    *,
    description: str = '',
    tiers=None,
    autoheal: bool = True,
    max_attempts: int = 4,
    retry_delay: float = 0.5,
    search_root=None,
    fallback_coordinates: "tuple[int, int] | None" = None,
    **runner_kwargs,
):
    """Find element → invoke spec.runner. On recoverable exception with
    autoheal=True, run heal cascade and retry up to max_attempts.

    Returns spec.runner's return value on success.
    Raises spec's recoverable exception on final attempt failure.
    Raises AutohealExhausted from heal_cascade if all tiers miss.
    Non-recoverable exceptions propagate immediately.
    """
    if tiers is None:
        tiers = list(_DEFAULT_HEAL_TIERS)
    _log.info("    [AutoHeal] autoheal=%s", autoheal)
    selector = primary_selector
    frame_info = None
    first_exc = None
    pending_coord_fallback = None
    # Re-point to a surviving window before any driver interaction: a self-closed
    # popup/tab leaves the session on a dead handle, and SmartWait (JS) / findElement
    # below would otherwise raise NoSuchWindowException (not in _DEFAULT_RECOVERABLE).
    _heal_stale_window(driver)
    SmartWait(driver).smart_wait(is_vision=False)
    for attempt in range(max_attempts):
        # Logged before findElement's own "Finding element..." trace; ordering
        # differs from V2 (which prints the find line first) but carries the same info.
        _log.info("    is_retry: %s", attempt > 0)
        try:
            el = findElement(driver, selector, description=description, allow_autoheal=False,
                             search_root=search_root)
            ctx = {'driver': driver, 'frame_info': frame_info, **runner_kwargs}
            return spec.runner(el, ctx)
        except spec.recoverable_exceptions as exc:
            if first_exc is None:
                first_exc = exc
            if not autoheal:
                raise
            # A previous heal round produced both a derived xpath and fresh
            # coordinates; the xpath attempt just failed. Fall back to the same
            # round's coordinates instead of re-entering the cascade — one
            # /v2/locate/desktop call serves both attempts (spec §3.3).
            if pending_coord_fallback is not None and spec.coord_runner is not None:
                x, y = pending_coord_fallback
                _log.info(
                    "    [AutoHeal] derived-xpath attempt failed (%s); coordinate fallback %s",
                    type(exc).__name__, pending_coord_fallback,
                )
                ctx = {'driver': driver, 'frame_info': frame_info, **runner_kwargs}
                return spec.coord_runner(driver, x, y, ctx)
            if attempt == max_attempts - 1:
                raise exc from first_exc
            _log.info(
                "    [retry] attempt %d/%d after %s: %s",
                attempt + 1, max_attempts, type(exc).__name__, exc,
            )
            _active_step = _current_step.get(None)
            if _active_step is not None:
                _active_step.auto_heal = True
            try:
                heal_result = _heal_cascade(
                    description=description,
                    current_selector=selector,
                    current_frame_info=frame_info,
                    tiers=tiers,
                    exception=exc,
                    driver=driver,
                    op_type=spec.op_type,
                )
            except AutohealExhausted as heal_exc:
                # Codegen-marked op: the resolver found nothing fresh ([0,0]);
                # recorded authoring-time coordinates are the true last resort
                # (spec §3.4).
                if fallback_coordinates is not None and spec.coord_runner is not None:
                    x, y = fallback_coordinates
                    _log.info(
                        "    [AutoHeal] cascade exhausted (%s); recorded fallback_coordinates %s",
                        type(heal_exc).__name__, fallback_coordinates,
                    )
                    ctx = {'driver': driver, 'frame_info': frame_info, **runner_kwargs}
                    return spec.coord_runner(driver, x, y, ctx)
                raise
            # Coordinates-only path: the resolver derived no xpath (shadow DOM /
            # iframe / verify failure). Dispatch via coord_runner instead of
            # re-entering findElement — a synthetic 'coord:x,y' placeholder fed
            # back into findElement crashes Chrome with InvalidSelectorException.
            if heal_result.coordinates is not None and not heal_result.selectors:
                _log.info(
                    "    [AutoHeal] relocated via %s -> coordinates %s",
                    heal_result.tier_used, heal_result.coordinates,
                )
                if spec.coord_runner is None:
                    raise NotImplementedError(
                        f"heal cascade resolved to coordinates {heal_result.coordinates} "
                        f"via tier {heal_result.tier_used!r}, but spec has no coord_runner. "
                        f"Either provide one on _ActionSpec or drop coordinate-resolving tiers."
                    )
                ctx = {'driver': driver, 'frame_info': heal_result.frame_info, **runner_kwargs}
                x, y = heal_result.coordinates
                return spec.coord_runner(driver, x, y, ctx)
            # Derived-xpath path: act through the standard runner; keep this
            # round's fresh coordinates as the fallback for the NEXT failure.
            # Also resets the stash each heal round — fresh coords supersede stale.
            pending_coord_fallback = (
                heal_result.coordinates
                if (heal_result.selectors and heal_result.coordinates is not None)
                else None
            )
            # Belt+suspenders: synthetic 'coord:x,y' placeholders must never
            # appear in HealResult.selectors. Pre-fix the old COORDINATE tier
            # produced them and Chrome rejected the next findElement with
            # InvalidSelectorException. Surface future regressions here
            # rather than in a cluster log.
            for s in heal_result.selectors or []:
                sel = s.get("selector") if isinstance(s, dict) else None
                if isinstance(sel, str) and sel.startswith("coord:"):
                    raise ValueError(
                        f"HealResult.selectors contains synthetic 'coord:' placeholder: {s}. "
                        f"Coordinate tiers must use HealResult.coordinates instead."
                    )
            selector = heal_result.selectors
            frame_info = heal_result.frame_info
            _log.info(
                "    [AutoHeal] relocated via %s -> %s",
                heal_result.tier_used,
                [s.get("selector") for s in heal_result.selectors],
            )
            time.sleep(retry_delay)
