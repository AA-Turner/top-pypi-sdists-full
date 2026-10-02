"""scroll_until — bounded scroll-search for an element that is not on screen yet.

Each iteration re-runs the find against the RECORDED strategies (the target may have
just been rendered, so a cached handle would be meaningless) and checks visibility
before scrolling again.

Visibility is a threshold, not mere presence: on Android a row can exist in the tree
while sitting under the app bar or below the fold, and stopping there leaves the target
unclickable. The element counts as reached when the requested fraction of its box lies
inside the viewport.

WHAT THE VIEWPORT IS depends on the scope. A screen-scoped search checks against the
screen. A CONTAINER-scoped one checks against the container clipped to the screen: the
scrolling happens inside that container, so a row that is on screen but outside it —
a sticky header, a neighbouring pane, the very row the container was recorded to
disambiguate from — does not count as reached.

This verb never degrades to a blind tap: it runs when the target's position is
unknown, so recorded coordinates carry no information about where it is now.

A recorded CONDITION shifts the stop test from geometry to vision. When a
natural-language condition is supplied, each pass asks the model whether it holds
on screen (check_until_condition) rather than finding a recorded selector and
measuring its visible fraction. The target may then carry no recorded selector at
all — the condition is the whole handle. Selectors and condition are each
optional, but a call carrying neither has nothing to search for and is refused.
"""
import logging
import time

from testmu_appium import _action_web, _config
from testmu_appium._helpers import _screen
from testmu_appium._errors import ElementNotFound
from testmu_appium._heal import (
    CACHE_ABSENT, HEAL_SOURCE, HealNoMatch, WebHealHit, autoheal_web, cache_key,
    invalidate_cache, read_cache, write_cache,
)
from testmu_appium._helpers._strategy import compile_selector, order_by_score
from testmu_appium._helpers.foreground import foreground_app
from testmu_appium._helpers.gesture import scroll_area, scroll_element, scroll_travel
from testmu_appium._helpers.band import (
    BAND_NUDGE_MAX_GESTURES,
    BAND_TOLERANCE_PX,
    in_band,
    nudge_toward_band,
)
from testmu_appium._helpers.condition import check_until_condition
from testmu_appium._helpers.movement import (
    MOVE_SETTLE_S as _MOVE_SETTLE_S,
    container_box as _container_box,
    container_signature as _container_signature,
    gesture_moved as _gesture_moved,
    perceive as _perceive,
)
from testmu_appium._action_scroll import (
    _container_under_centre, _element_area, _screen_area,
)
from testmu_appium._step import mark_autohealed

_log = logging.getLogger("testmu_appium")

#: How many gestures ONE scroll_until op spends. A search longer than this is
#: recorded as several scroll_until ops in a row rather than one giant op or a pile
#: of raw scrolls: each op scrolls up to this many times, and a chunk that spends
#: its budget with the list still moving hands off to the next op (see
#: `_scroll_until_condition`). The movement probe (`_container_signature`, scoped to
#: the scrolled container) still ends a chunk early at the true bottom, so a wrong or
#: absent target is not chased past the end of the list.
DEFAULT_MAX_SCROLLS = 30
DEFAULT_VISIBILITY_THRESHOLD = 0.9
_SCROLL_PERCENT = 0.7

# The movement probe (`_container_signature`/`_gesture_moved`) and the settle it
# reads after live in `_helpers.movement`, shared with the edge scroll — whose
# gesture cannot answer "is there more?" itself and stops on movement the same
# way this verb's search loop does.


class _WebHealDeadline:
    """Start-budget shared by web scroll perception, HTTP retries and re-read.

    The HTTP retry call is wall-clock bounded; synchronous device/debug commands
    already in flight cannot be cancelled and finish at their transport timeout.
    """

    def __init__(self):
        milliseconds = int(_config.get("heal_timeout_ms", 60000) or 0)
        if milliseconds <= 0:
            milliseconds = 60000
        self.expires_at = time.monotonic() + milliseconds / 1000.0

    def remaining_s(self):
        return max(0.0, self.expires_at - time.monotonic())


def _find_first(driver, selectors, platform):
    for selector in order_by_score(selectors):
        by, value = compile_selector(selector, platform)
        try:
            matches = driver.find_elements(by, value)
        except Exception:  # noqa: BLE001 — a strategy that errors mid-scroll is a miss
            continue
        if len(matches) == 1:
            return matches[0]
    return None


def _nudge_into_band(driver, selectors, container, viewport, platform):
    """Reposition an on-screen target into the band with a bounded sized nudge.

    Phase two of the selector search: the search brought the target on screen but out
    of band, so at most ``BAND_NUDGE_MAX_GESTURES`` sized gestures aim its centre into
    the band, re-reading the centre between each and stopping when a gesture moves it no
    further. This is the same deterministic nudge the adapter runs at authoring —
    ``nudge_toward_band`` is the one landing both call — so an element ends in the same
    relative position on either side. The gesture is sized as a container-proportional
    percent, carrying the same content travel as the authoring pixel path and recording
    no device distance; with no scrollable container it scrolls the screen instead. A
    clipped box has no reliable centre, so a coarse gesture reveals the clipped side
    first and the loop re-measures once it is whole. Returns the element once its centre
    is in band, else ``None`` — the caller then returns the element it already found,
    best effort.
    """
    _, vy, _, vh = viewport
    top, bottom = vy, vy + vh
    box = _container_box(container)
    span = max((box[3] - box[1]) if box is not None else vh, 1)
    prev_cy = None
    for attempt in range(BAND_NUDGE_MAX_GESTURES + 1):
        element = _find_first(driver, selectors, platform)
        if element is None:
            return None                   # scrolled off during the nudge
        try:
            rect = element.rect
        except Exception:  # noqa: BLE001 — an element that will not report a box
            return None
        el_top, height = int(rect["y"]), int(rect["height"])
        if height <= 0 or el_top + height <= top or el_top >= bottom:
            return None                   # entirely off screen after a gesture
        cy = el_top + height / 2
        clipped = el_top <= top or el_top + height >= bottom
        if not clipped and in_band(cy, top, bottom):
            return element                # placed
        if prev_cy is not None and abs(cy - prev_cy) <= BAND_TOLERANCE_PX:
            return None                   # the last gesture moved it no further
        if attempt == BAND_NUDGE_MAX_GESTURES:
            return None                   # budget spent, checked, still not placed
        if clipped:
            # The centre is unreliable, so a sized aim is meaningless: reveal the
            # clipped side with a coarse gesture and re-measure once it is whole.
            direction, percent = ("up" if el_top <= top else "down"), _SCROLL_PERCENT
        else:
            direction, distance = nudge_toward_band(cy, top, bottom)
            percent = min(1.0, distance / (scroll_travel() * span))
        prev_cy = cy
        if container is not None:
            scroll_element(driver, container, direction, percent)
        else:
            left, s_top, width, s_height = _screen_area(driver)
            scroll_area(driver, left, s_top, width, s_height, direction, percent)
        time.sleep(_MOVE_SETTLE_S)
    return None


def _visible_fraction(element, viewport) -> float:
    """The fraction of the element's box that lies inside the viewport."""
    try:
        rect = element.rect
    except Exception:  # noqa: BLE001
        return 0.0
    x, y = int(rect["x"]), int(rect["y"])
    w, h = int(rect["width"]), int(rect["height"])
    if w <= 0 or h <= 0:
        return 0.0
    vx, vy, vw, vh = viewport
    overlap_w = max(0, min(x + w, vx + vw) - max(x, vx))
    overlap_h = max(0, min(y + h, vy + vh) - max(y, vy))
    return (overlap_w * overlap_h) / float(w * h)


def _viewport(driver):
    """The full screen. Distinct from the gesture area, which is inset to stay clear
    of system gestures — an element sitting inside that inset band is still visible."""
    size = _screen.window_size(driver)
    return 0, 0, size[0], size[1]


def _intersect(first, second):
    """The overlap of two (x, y, width, height) boxes, zero-sized when they are
    disjoint — which `_visible_fraction` then reads as "not visible at all"."""
    fx, fy, fw, fh = first
    sx, sy, sw, sh = second
    x, y = max(fx, sx), max(fy, sy)
    right, bottom = min(fx + fw, sx + sw), min(fy + fh, sy + sh)
    return x, y, max(0, right - x), max(0, bottom - y)


def _gesture_target(driver, container_selectors, platform):
    """What to scroll, and the rectangle to judge visibility against.

    Returns ``(container_or_None, viewport)``. The gesture is aimed at the
    container when there is one and at the screen rectangle otherwise; visibility
    is measured against ``viewport``.

    A recorded container is honoured and its clipped box becomes the viewport, so
    a row on screen but outside it does not count as reached. With no recorded
    container the search is screen-scoped: the viewport is the whole screen, but
    the gesture still aims at the scrollable a thumb at the centre would move
    (R4) rather than the inset rectangle — on a sticky-header layout the rectangle
    gestures the header, moves nothing, and reads as end-of-content. A recorded
    container that is not on screen degrades to that same screen search rather than
    raising (R5): reaching the container is a separate outer loop's job.
    """
    screen = _viewport(driver)
    if container_selectors:
        container = _find_first(driver, container_selectors, platform)
        if container is not None:
            return container, _intersect(_element_area(container), screen)
        _log.info("    [scroll_until] recorded container not on screen; "
                  "falling back to the screen's own scrollable")
    return _container_under_centre(driver), screen


def _scroll_toward(driver, container, direction):
    """One gesture toward ``direction``.

    Aims at the container when there is one, at the inset screen rectangle
    otherwise. Returns the gesture's own canScrollMore, which the search loops no
    longer trust — they compare the container's rows before and after
    (`_container_signature`) to tell a gesture that moved content from one at the
    end, because canScrollMore
    is a false negative on some lists. Kept only so callers outside the search
    loops still get the raw signal.
    """
    if container is not None:
        return scroll_element(driver, container, direction, _SCROLL_PERCENT)
    left, top, width, height = _screen_area(driver)
    return scroll_area(driver, left, top, width, height, direction, _SCROLL_PERCENT)


def _scroll_healed_descriptor(driver, descriptor, deadline=None):
    if deadline is not None and deadline.remaining_s() <= 0:
        return None
    channel = _action_web.visible_channel(foreground_app(driver))
    if channel is None:
        return None
    try:
        surface = _action_web.open_unplaced_surface(channel)
    except Exception as e:  # noqa: BLE001
        _log.info("    [AutoHeal] web page could not be re-read (%s)", e)
        return None
    element = _action_web.resolve_descriptor(surface.all_elements, descriptor)
    if element is None:
        return None
    try:
        if deadline is not None and deadline.remaining_s() <= 0:
            return None
        verdict = _action_web.scroll_descriptor(channel, descriptor)
    except Exception as e:  # noqa: BLE001 — caller retries with fresh perception
        _log.info("    [AutoHeal] healed web scroll failed (%s)", e)
        return None
    return verdict if verdict != "missing" else None


def _fresh_unplaced_surface(driver):
    channel = _action_web.visible_channel(foreground_app(driver))
    if channel is None:
        return None, None
    return channel, _action_web.open_unplaced_surface(channel)


def _heal_web_scroll(driver, selectors, description, frame_path):
    deadline = _WebHealDeadline()
    key = ("web", "scroll", frame_path or "", *cache_key(selectors))
    cached = read_cache(key)
    if cached is None:
        raise ElementNotFound(
            description or "scroll_until target", ["css"],
            "autoheal previously reported no matching web element",
        )
    if cached is not CACHE_ABSENT:
        verdict = _scroll_healed_descriptor(driver, cached, deadline)
        if verdict is not None:
            mark_autohealed(HEAL_SOURCE)
            return verdict
        invalidate_cache(key)

    if deadline.remaining_s() <= 0:
        raise ElementNotFound(
            description or "scroll_until target", ["css"],
            "action deadline was exhausted before web autoheal recapture",
        )
    try:
        channel, surface = _fresh_unplaced_surface(driver)
    except Exception as e:  # noqa: BLE001
        raise ElementNotFound(
            description or "scroll_until target", ["css"],
            f"the web page could not be read for autoheal: {e}",
        ) from e
    if channel is None or surface is None:
        raise ElementNotFound(
            description or "scroll_until target", ["css"],
            "no debug channel reached the page on screen for autoheal",
        )
    last_reason = ""
    for attempt in range(2):
        if deadline.remaining_s() <= 0:
            raise ElementNotFound(
                description or "scroll_until target", ["css"],
                "action deadline was exhausted during web autoheal",
            )
        outcome = autoheal_web(
            driver, surface, description, "scroll",
            budget_s=deadline.remaining_s(), allow_inert=True
        )
        if isinstance(outcome, WebHealHit):
            # The HTTP round trip can outlive a tab switch or WebView teardown.
            # Reacquire the page currently visible before resolving or scrolling.
            verdict = _scroll_healed_descriptor(
                driver, outcome.descriptor, deadline
            )
            if verdict is not None:
                write_cache(key, outcome.descriptor)
                mark_autohealed(outcome.source)
                return verdict
            last_reason = (
                f"web descriptor for dom_index {outcome.dom_index} did not "
                "strictly resolve before scrolling"
            )
            if attempt == 0:
                if deadline.remaining_s() <= 0:
                    break
                try:
                    channel, surface = _fresh_unplaced_surface(driver)
                except Exception:
                    break
                if channel is None or surface is None:
                    break
                continue
        elif isinstance(outcome, HealNoMatch):
            write_cache(key, None)
            raise ElementNotFound(
                description or "scroll_until target", ["css"], outcome.reason
            )
        else:
            cause = (
                getattr(outcome, "cause", None)
                or getattr(outcome, "detail", None)
                or getattr(outcome, "reason", "")
            )
            raise ElementNotFound(
                description or "scroll_until target", ["css"],
                f"heal could not be consulted: {cause}",
            )
        break
    raise ElementNotFound(
        description or "scroll_until target", ["css"],
        f"heal answered but its web descriptor did not resolve: {last_reason}",
    )


def _scroll_web_into_view(driver, selectors, description: str, frame_path: str = ""):
    """Scroll a DOM element into view over the debug channel.

    The page places its own elements, so there is no gesture loop here: one call
    moves the element and reports whether it landed in the viewport. Nothing is
    returned, because a web target has no native element handle to hand back.
    """
    if _action_web.css_of(selectors) is None:
        raise ValueError(
            "a web-surface scroll_until needs a css strategy; the recorded "
            f"strategies were {[s.get('strategy') for s in selectors]}"
        )
    channel = _action_web.visible_channel(foreground_app(driver))
    if channel is None:
        raise ElementNotFound(
            description or "scroll_until target", ["css"],
            "no debug channel reached the page on screen",
        )
    css = _action_web.css_of(selectors)
    verdict = None
    target = css
    if frame_path:
        try:
            surface = _action_web.open_unplaced_surface(channel)
        except Exception as e:  # noqa: BLE001
            raise ElementNotFound(
                description or "scroll_until target", ["css"],
                f"the nested web page could not be read: {e}",
            ) from e
        candidates = [
            e for e in surface.all_elements
            if e.get("path", "") == frame_path
        ]
        element = _action_web.locate(candidates, selectors, frame_path)
        if element is not None and element.get("dom_path"):
            descriptor = _action_web.descriptor_for(element)
            verdict = _action_web.scroll_descriptor(channel, descriptor)
            target = element.get("css") or element.get("label", "")
    if verdict is None:
        # The top-document fast path stays one round trip. Nested targets take
        # the descriptor path above because querySelector cannot cross a boundary.
        verdict = (
            "missing" if frame_path
            else _action_web.scroll_into_view(channel, css)
        )
    if verdict is None:
        raise ElementNotFound(
            description or "scroll_until target", ["css"],
            f"the page failed while scrolling {target} into view",
        )
    if verdict == "missing":
        if not (description or "").strip():
            raise ElementNotFound(
                "scroll_until target", ["css"],
                f"{target} names nothing in the page and no description was "
                "supplied for autoheal",
            )
        verdict = _heal_web_scroll(
            driver, selectors, description, frame_path
        )
        target = description
    _log.info("    [scroll_until] %s scrolled into view (%s)", target, verdict)
    return None


def _scroll_until_condition(driver, condition, description, direction,
                            container_selectors, max_scrolls, platform):
    """Scroll until a natural-language condition holds on screen, judged by vision.

    The stop test is `check_until_condition` — a model looking at a fresh
    screenshot — not a recorded selector (D8). The target may carry no recorded
    ref at all: the condition is the whole handle. The gesture aims at the
    scrollable under the centre or a recorded container (R4/R5).

    Returns None on success. It ALSO returns None when the budget runs out with the
    list still scrolling: that is one chunk of a search recorded as several
    scroll_until ops, and the next op continues the travel. It raises only when the
    list reaches its true end (nothing moves) without the condition ever holding —
    the target is genuinely not there.
    """
    container, _ = _gesture_target(driver, container_selectors, platform)

    # ONE capture per gesture serves both jobs: its screenshot answers the vision
    # condition, and its rows — scoped to the scrolled container — are the movement
    # /end signal. So the tree is read once per gesture, not twice, and content
    # outside the container (a ticking clock, a neighbouring pane) cannot read as
    # movement. Each capture is also the fresh post-gesture screen, so a target the
    # terminal gesture just revealed is caught before we conclude the end (R6) —
    # without a second condition call.
    prev_sig = None
    reached_end = False
    for attempt in range(max_scrolls + 1):
        perception = _perceive(driver, screenshot=True)
        if perception is not None and check_until_condition(
                driver, condition, perception=perception):
            _log.info("    [scroll_until] condition met after %d scroll(s)", attempt)
            return None
        cur_sig = _container_signature(perception, container)
        if attempt > 0 and not _gesture_moved(prev_sig, cur_sig):
            _log.info("    [scroll_until] reached the end of the scrollable area")
            reached_end = True
            break
        if attempt == max_scrolls:
            break
        _scroll_toward(driver, container, direction)
        time.sleep(_MOVE_SETTLE_S)
        prev_sig = cur_sig

    if not reached_end:
        # Budget spent with the list still moving: this op is one chunk of a longer
        # search recorded as several scroll_until ops. It did its share of the
        # travel; the NEXT op carries on from here. Returning rather than raising is
        # what lets the chain advance — a genuinely-absent target is still caught by
        # whichever chunk reaches the true end.
        _log.info("    [scroll_until] budget of %d spent, list still scrolling; "
                  "chunk complete, a chained op continues", max_scrolls)
        return None

    raise ElementNotFound(
        description or condition, ["vision"],
        f"the condition never held before the end of the list: {condition}",
    )


def scroll_until(driver, *, selectors=None, description: str = "", direction: str = "down",
                 condition: str = "", container_selectors=None,
                 max_scrolls: int = DEFAULT_MAX_SCROLLS,
                 visibility_threshold: float = DEFAULT_VISIBILITY_THRESHOLD,
                 fallback_coordinates: dict | None = None,
                 surface: str = "native", frame_path: str = ""):
    """Scroll until the target is reached, or the budget runs out.

    With a `condition` the stop test is vision (see `_scroll_until_condition`) and
    `selectors` may be omitted. Without one it is the recorded selector's visible
    fraction. A call carrying neither is refused — there is nothing to search for.

    fallback_coordinates is accepted for call-shape uniformity with the other element
    verbs and deliberately ignored: this verb runs when the target's position is
    unknown, so a recorded point carries no information about where it is.

    `surface="web"` scrolls through the page instead, which is one call rather than
    a gesture loop because the DOM already knows where its elements are.
    `frame_path` keeps nested targets in their recorded frame; healed targets retain
    both frame and shadow identity privately.
    """
    if not selectors and not condition:
        raise ValueError(
            "scroll_until needs a recorded selector or a vision condition; it runs "
            "when the target's position is unknown and has nothing else to search for"
        )

    if surface == "web":
        return _scroll_web_into_view(
            driver, selectors, description, frame_path
        )

    platform = _config.platform()

    if condition:
        return _scroll_until_condition(
            driver, condition, description, direction, container_selectors,
            max_scrolls, platform,
        )

    container, viewport = _gesture_target(driver, container_selectors, platform)

    def _placed():
        """The target when it is found AND inside the band, and separately whatever
        was found at all. A clipped box — bounds coincident with a viewport edge —
        has an unreliable centre and counts as not placed. ``visibility_threshold``
        is kept in the signature for generated callers; the native stop test is the
        band, and the fraction is the web branch's.
        """
        element = _find_first(driver, selectors, platform)
        if element is None:
            return None, None
        try:
            rect = element.rect
        except Exception:  # noqa: BLE001 — an element that will not report a box
            return None, element
        height = int(rect["height"])
        vx, vy, vw, vh = viewport
        top, bottom = vy, vy + vh
        el_top = int(rect["y"])
        el_bottom = el_top + height
        if height <= 0 or el_bottom <= top or el_top >= bottom:
            # Entirely off screen — a real tree omits it, so it is not reached.
            return None, None
        if el_top <= top or el_bottom >= bottom:
            # Clipped at an edge: on screen but the centre is unreliable, so it
            # is found yet not placed.
            return None, element
        if in_band(el_top + height / 2, top, bottom):
            return element, element
        return None, element

    # Runs max_scrolls + 1 times so the LAST scroll is followed by a check; every
    # exit path has already checked the element in its final position. The end is
    # found by whether a gesture moved the rows INSIDE THE CONTAINER (scoped so a
    # ticking clock or a neighbouring pane cannot read as movement), not by the
    # gesture's own canScrollMore, which lies on some lists. _placed() runs on each
    # fresh post-gesture screen, so a target the terminal gesture revealed is caught
    # before we conclude the end (R6).
    seen = None
    prev_sig = None
    for attempt in range(max_scrolls + 1):
        placed, seen = _placed()
        if placed is not None:
            _log.info("    [scroll_until] target in band after %d scroll(s)", attempt)
            return placed
        if seen is not None:
            # On screen but out of band: hand off to the deterministic nudge, which
            # aims the centre into the band with sized gestures — the same landing as
            # authoring — rather than another coarse search step (N2). Its bounded
            # budget lands the target, or leaves it for the best-effort return below.
            nudged = _nudge_into_band(driver, selectors, container, viewport, platform)
            if nudged is not None:
                _log.info("    [scroll_until] target nudged into band after %d scroll(s)",
                          attempt)
                return nudged
            break
        cur_sig = _container_signature(_perceive(driver, screenshot=False), container)
        if attempt > 0 and not _gesture_moved(prev_sig, cur_sig):
            _log.info("    [scroll_until] reached the end of the scrollable area")
            break
        if attempt == max_scrolls:
            break
        _scroll_toward(driver, container, direction)
        time.sleep(_MOVE_SETTLE_S)
        prev_sig = cur_sig

    if seen is not None:
        # Best effort: found at its final position but not placed in the band — a
        # structurally-unreachable element. Returning it keeps replay from
        # hard-failing where authoring proceeded; a target that scrolled away is
        # not `seen` at the end and still raises.
        _log.info("    [scroll_until] target found but not placed after %d scroll(s); "
                  "returning best effort", max_scrolls)
        return seen
    raise ElementNotFound(
        description or "scroll_until target",
        [s.get("strategy") for s in selectors],
        f"not found after {max_scrolls} scroll(s)",
    )
