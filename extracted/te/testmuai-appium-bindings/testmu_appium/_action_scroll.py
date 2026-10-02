"""scroll — screen-level and element-scoped scrolling.

Four recorded kinds:
- "times"   → N screen-heights in the given direction
- "percent" → a fraction of the scrollable area
- "pixels"  → an absolute distance, covered by as many gestures as it takes
- "edge"    → scroll to the top or bottom, ended by the movement probe (a gesture
  that moved nothing), bounded by a scroll budget

Scope is decided by the presence of selectors: with them the gesture runs inside the
element's rectangle, without them it runs over the screen (inset from the edges, which
otherwise trigger system gestures like back-swipe and the notification shade).

The scroll verbs deliberately have NO coordinate fallback. A recorded ratio identifies
a point, and a blind tap is never a substitute for a scroll.
"""
import logging
import time

from testmu_appium._action_engine import (
    _ActionSpec, _basis_is_complete, _coordinates_from_basis, _run_action, run_driver,
)
from testmu_appium._errors import CoordinateFallbackUnavailable
from testmu_appium._helpers import _screen
from testmu_appium._helpers.gesture import (
    drag_scroll, scroll_area, scroll_element, scroll_travel, scrollable_containers,
)
from testmu_appium._helpers.movement import (
    MOVE_SETTLE_S as _MOVE_SETTLE_S,
    box_signature as _box_signature,
    container_signature as _container_signature,
    gesture_moved as _gesture_moved,
    perceive as _perceive,
)

_log = logging.getLogger("testmu_appium")

SCROLL_KINDS = ("times", "percent", "pixels", "edge")
DIRECTIONS = ("up", "down", "left", "right")

#: Fraction of the screen kept clear of the gesture on each axis. The outer band is
#: owned by system gestures.
_SCREEN_INSET_X = 0.1
_SCREEN_INSET_Y = 0.15

#: How far one "time" travels, as a fraction of the gesture area. Appium insets
#: the gesture inside that area, so the content moves about three quarters of the
#: fraction asked for. The element path takes the shorter stride: a container is
#: smaller than the screen it sits in, so the same fraction of it leaves less of
#: the previous view behind for the next look at the screen to overlap with.
_ONE_SCREEN_PERCENT = 0.8
_ONE_ELEMENT_PERCENT = 0.6

#: Running to an end wants distance rather than overlap.
_EDGE_PERCENT = 0.8

#: Upper bound on the gestures an "edge" scroll will issue before giving up, so a
#: list that always reports "more to scroll" cannot spin forever.
_EDGE_MAX_GESTURES = 30

#: Consecutive failed movement reads after which an edge scroll stops probing and
#: falls back to the gesture's own answer. Two in a row means the tree is not
#: readable for this op (a webview-less mock, a screen with no rows), not a
#: transient miss; paying a settle and a read per gesture for None every time
#: would slow the loop without ever concluding anything.
_PROBE_DEAD_READS = 2

#: Share of the screen one drag from a recorded point may travel per gesture. The
#: drag has no container to measure against, and a control nothing could name
#: is usually a small one (a drum), where a screen-sized fling spins past the row
#: a loop is hunting for. Measured on the V16App looping drum (row ~150px on a
#: 2856px screen): a quarter screen moved three rows per gesture, 15% one to
#: two, which is the step an until loop can stop on; the loop covers distance.
_POINT_DRAG_MAX_SHARE = 0.15

#: Slowest finger speed a point drag travels at, px per ms. Below it the content
#: tracks the finger and stops where it stops; faster reads as a fling, whose
#: momentum carries a drum several rows past the finger.
_POINT_DRAG_PX_PER_MS = 0.4

#: Upper bound on the gestures one pixel scroll will issue, so a distance far
#: past the end of the content cannot spin forever.
_PIXELS_MAX_GESTURES = 30

#: Upper bound on the gestures one percent scroll will issue. A percent over 100%
#: of the area cannot land in one gesture, so it is delivered as repeated full
#: gestures plus a remainder; the cap stops a huge percent from spinning forever.
_PERCENT_MAX_GESTURES = 30


def _validate(kind: str, direction: str) -> None:
    if kind not in SCROLL_KINDS:
        raise ValueError(f"unknown scroll kind {kind!r}; expected one of {list(SCROLL_KINDS)}")
    if direction not in DIRECTIONS:
        raise ValueError(
            f"unknown scroll direction {direction!r}; expected one of {list(DIRECTIONS)}"
        )


def _screen_area(driver):
    size = _screen.window_size(driver)
    width, height = size[0], size[1]
    inset_x, inset_y = int(width * _SCREEN_INSET_X), int(height * _SCREEN_INSET_Y)
    return inset_x, inset_y, width - 2 * inset_x, height - 2 * inset_y


def _element_area(element):
    rect = element.rect
    return int(rect["x"]), int(rect["y"]), int(rect["width"]), int(rect["height"])


def _perform(scroll_once, extent, kind, direction, value, step_percent,
             probe=None, max_step_percent=None, travel_share=None) -> bool:
    """Run one scroll kind. Returns whether content remains in that direction.

    ``scroll_once(percent)`` issues a single gesture and answers whether anything
    could still be scrolled; what that gesture is aimed at is the caller's to
    decide. ``extent`` is the (width, height) the gesture covers, which is what a
    pixel distance is measured against. ``step_percent`` is how far one "time"
    travels. ``probe`` is a zero-argument movement read (the current signature of
    the scrolled surface, or None for an unreadable one); only the "edge" kind
    consumes it — see there.

    ``max_step_percent`` and ``travel_share`` describe a ``scroll_once`` that is
    a plain drag rather than a platform scroll: the drag truncates any one
    gesture to ``max_step_percent`` of the extent and travels exactly its
    percent of the extent (``travel_share=1.0``, where a platform gesture
    travels ``scroll_travel()`` of it). The pixels accounting budgets by these
    facts — otherwise one truncated drag is booked as the whole ask and the
    rest of the distance is never attempted.

    That per-gesture answer is passed on rather than swallowed. It is the only
    thing separating a container at its end from one with more to give, and a
    caller looping until something appears has no other exit: without it every
    retry after the end still pays for a gesture, a tree read and a model call
    that cannot change anything. It is NOT a success flag — a scroll that
    arrives at the end did its job.
    """
    width, height = extent

    if kind == "times":
        more = True
        for gesture in range(max(1, int(value or 1))):
            more = bool(scroll_once(step_percent))
            if not more:
                # scrollGesture answers whether content remains in that
                # direction. Gesturing at a container already at its end moves
                # nothing and reports the same "ok" as a scroll that worked.
                _log.info("[scroll] reached the end after %d gesture(s)", gesture + 1)
                break
        return more

    if kind == "percent":
        # A recorded percent may be 0..1 or 0..100; anything above 1 is read as the
        # latter, which is how the recorder writes whole percentages.
        fraction = float(value or 0)
        if fraction > 1:
            fraction /= 100.0
        # One gesture cannot drag more than a full extent, so a request over 100%
        # is delivered as repeated full gestures plus a final remainder. A percent
        # at or under 100% is a single gesture, exactly as before.
        remaining = fraction
        more = True
        for _ in range(_PERCENT_MAX_GESTURES):
            if remaining <= 0:
                break
            step = min(1.0, remaining)
            more = bool(scroll_once(step))
            if not more:
                _log.info("[scroll] reached the end before covering the asked percent")
                break
            remaining -= step
        return more

    if kind == "pixels":
        span = height if direction in ("up", "down") else width
        stride = (scroll_travel() if travel_share is None else travel_share) * max(span, 1)
        cap = 1.0 if max_step_percent is None else max_step_percent
        remaining = abs(float(value or 0))
        more = True
        for _ in range(_PIXELS_MAX_GESTURES):
            if remaining < 1:
                break
            percent = min(cap, remaining / stride)
            more = bool(scroll_once(percent))
            if not more:
                _log.info("[scroll] reached the end before covering the asked distance")
                break
            remaining -= percent * stride
        else:
            _log.warning("[scroll] pixel scroll hit its %d-gesture budget with "
                         "%dpx left to cover", _PIXELS_MAX_GESTURES, round(remaining))
        return more

    # edge — keep scrolling until a gesture demonstrably moves nothing. The
    # movement probe is the judge because the gesture's own answer cannot be:
    # iOS has no scroll verb that reports "more to scroll" (its adapter answers
    # True unconditionally, so this loop used to burn its whole budget swiping
    # at a page that had already ended), and Android's `scrollGesture` lies both
    # ways (a Compose LazyColumn claims "cannot scroll" while still scrolling; a
    # gesture landed on a sticky header claims the end of a list it never
    # touched). Two conclusive reads with no movement between them mean the end
    # — no later gesture can do better. A gesture's "no more" claim is honoured
    # only while the probe cannot rule (no probe, or a failed read on either
    # side): with conclusive reads showing movement, the claim is refuted by the
    # gesture's own effect and the next pass decides.
    prev_sig = probe() if probe is not None else None
    dead_reads = 1 if probe is not None and prev_sig is None else 0
    for gesture in range(_EDGE_MAX_GESTURES):
        more = scroll_once(_EDGE_PERCENT)
        cur_sig = None
        if probe is not None and dead_reads < _PROBE_DEAD_READS:
            time.sleep(_MOVE_SETTLE_S)
            cur_sig = probe()
            dead_reads = dead_reads + 1 if cur_sig is None else 0
        if prev_sig is not None and cur_sig is not None:
            if not _gesture_moved(prev_sig, cur_sig):
                _log.info("[scroll] edge reached the end after %d gesture(s)",
                          gesture + 1)
                return False
        elif not more:
            return False
        prev_sig = cur_sig
    _log.warning("[scroll] edge scroll hit its %d-gesture budget", _EDGE_MAX_GESTURES)
    return True


def _scrollables(driver):
    """The scrollable containers on screen, or none when they cannot be read.

    Best-effort by construction: resolving a container improves the gesture and
    must never become a new way for a scroll to fail. A platform with no such
    lookup declared raises out of the registry and lands here as "none", which
    is the same answer as a screen that has none.
    """
    try:
        return scrollable_containers(driver)
    except Exception as e:  # noqa: BLE001 — see above
        _log.debug("[scroll] scrollable lookup unavailable (%s)", e)
        return []


def _container_under_centre(driver):
    """The scrollable a thumb at the screen centre would move, or None."""
    try:
        size = driver.get_window_size()
        centre = int(size["width"]) // 2, int(size["height"]) // 2
    except Exception as e:  # noqa: BLE001 — no window, no centre to aim at
        _log.debug("[scroll] window size unavailable (%s)", e)
        return None
    return _container_under_point(driver, centre)


def _container_under_point(driver, point):
    """The scrollable a thumb at ``point`` would move, or None.

    Innermost wins, measured by area: a nested container's bounds sit inside the
    one enclosing it, so the smallest box containing the point is the deepest.
    That is the same answer the device's own hit-testing gives for a touch there,
    which is what keeps authoring and replay describing the same gesture.
    """
    cx, cy = point
    best = None
    for element in _scrollables(driver):
        try:
            rect = element.rect
            x, y = int(rect["x"]), int(rect["y"])
            width, height = int(rect["width"]), int(rect["height"])
        except Exception:  # noqa: BLE001 — a stale node describes no box
            continue
        if not (x <= cx <= x + width and y <= cy <= y + height):
            continue
        area = width * height
        if best is None or area < best[0]:
            best = (area, element)
    return best[1] if best else None


def _movement_probe(driver, *, container=None, box=None):
    """A zero-argument read of what the scrolled surface currently shows.

    Scoped to the container when the gesture is aimed at one, and to the given
    box — the inset screen rectangle the gesture covers, which excludes the
    status bar — when it is not. Each read is one perception pass; a read that
    fails answers None, which the edge loop treats as inconclusive.
    """
    def read():
        perception = _perceive(driver, screenshot=False)
        if container is not None:
            return _container_signature(perception, container)
        return _box_signature(perception, box)
    return read


def _recorded_point(driver, basis):
    """The recorded coordinate basis scaled onto the live window, or None.

    None when there is no basis, it is incomplete, or it was recorded in the
    other orientation — the screen scroll then aims the way it always has.
    """
    if not basis or not _basis_is_complete(basis):
        return None
    try:
        return _coordinates_from_basis(driver, basis)
    except CoordinateFallbackUnavailable as e:
        _log.info("[scroll] recorded point not replayable here (%s); aiming at the centre", e)
        return None


def _drag_runner(driver, point, ctx):
    """Scroll from the recorded point when nothing under it is a container.

    The device reported no scrollable at the point, yet the recording says a
    scroll happened there: a control the tree does not flag (a NumberPicker on
    some builds), or a custom surface. A finger that lands ON it still moves it,
    so the gesture is a drag whose touch-down is the point itself, travelling the
    asked share of the screen up to `_POINT_DRAG_MAX_SHARE` per gesture. The drag
    has no "more to scroll" answer; the movement probe judges an edge scroll, as
    it does on iOS.
    """
    direction = ctx["direction"]
    left, top, width, height = _screen_area(driver)
    span = height if direction in ("up", "down") else width

    # The recorded point is scaled on the FULL window while every endpoint
    # below clamps into the inset rectangle. The start clamps the same way:
    # a point outside the inset (the status-bar strip) would otherwise put
    # the clamped end on the far side of the start, and the drag would travel
    # against the asked direction.
    point = (min(max(point[0], left), left + width),
             min(max(point[1], top), top + height))

    def once(percent):
        distance = max(1, int(min(percent, _POINT_DRAG_MAX_SHARE) * span))
        x, y = point
        if direction == "down":
            end = (x, max(top, y - distance))
        elif direction == "up":
            end = (x, min(top + height, y + distance))
        elif direction == "right":
            end = (max(left, x - distance), y)
        else:
            end = (min(left + width, x + distance), y)
        drag_scroll(driver, point, end, move_ms=int(distance / _POINT_DRAG_PX_PER_MS))
        return True

    return _perform(
        once, (width, height), ctx["kind"], direction, ctx.get("value"),
        _ONE_SCREEN_PERCENT,
        probe=_movement_probe(driver, box=(left, top, left + width, top + height)),
        max_step_percent=_POINT_DRAG_MAX_SHARE, travel_share=1.0,
    )


def _element_runner(element, ctx, step_percent=None):
    """Scroll one element. ``step_percent`` overrides how far one "time" travels,
    for a caller whose request was not "scroll this container" (see
    ``_driver_runner``); the element stride is the default."""
    driver, direction = ctx["driver"], ctx["direction"]
    _left, _top, width, height = _element_area(element)
    return _perform(
        lambda percent: scroll_element(driver, element, direction, percent),
        (width, height), ctx["kind"], direction, ctx.get("value"),
        step_percent if step_percent is not None else _ONE_ELEMENT_PERCENT,
        probe=_movement_probe(driver, container=element),
    )


def _screen_percent_as_pixels(driver, direction: str, value) -> float:
    """A screen-level percent as the pixel distance it names on the full screen.

    A recorded percent may be 0..1 or 0..100; anything above 1 is read as the
    latter. Vertical directions measure against the screen height, horizontal
    ones against the width.
    """
    fraction = float(value or 0)
    if fraction > 1:
        fraction /= 100.0
    width, height = _screen.window_size(driver)
    span = height if direction in ("up", "down") else width
    return fraction * span


def _driver_runner(driver, ctx):
    # A screen scroll has no selectors, but the screen still has one thing a
    # thumb at its centre would move. Address that, because the inset rectangle
    # is not it: on a layout with a sticky header the rectangle's leading edge
    # lands ABOVE the scrollable, so the gesture is delivered to the header,
    # moves nothing, and the driver truthfully answers "no more content" —
    # indistinguishable from a real end of list.
    direction = ctx["direction"]
    point = _recorded_point(driver, ctx.get("fallback_coordinates"))
    if point is not None:
        # A recorded point aims the gesture where the author scrolled: the
        # innermost container under it, or — when the device flags nothing
        # scrollable there — a drag from the point itself. The recorded percent
        # is kept; a drum wants a small clamped stride, not a screen-percent fling.
        container = _container_under_point(driver, point)
        if container is None:
            _log.info("[scroll] no scrollable under the recorded point %s; dragging from it", point)
            return _drag_runner(driver, point, ctx)
    else:
        if ctx["kind"] == "percent":
            # A screen-level percent is a share of the SCREEN, so it travels as
            # that many pixels through the pixel path, which measures each gesture
            # against the box it drags and its real travel. The box is unchanged.
            ctx = {
                **ctx,
                "kind": "pixels",
                "value": _screen_percent_as_pixels(driver, direction, ctx.get("value")),
            }
        container = _container_under_centre(driver)
    if container is not None:
        # The request was "scroll the screen"; the container is only how it was
        # carried out, so the gesture keeps the screen's reach. A stride is a
        # fraction OF THE BOX being dragged, so covering the same ground inside a
        # smaller box takes a larger fraction — and a gesture cannot drag a
        # container past its own span, so a short list clamps at all of it.
        _left, _top, screen_w, screen_h = _screen_area(driver)
        _l, _t, box_w, box_h = _element_area(container)
        vertical = direction in ("up", "down")
        reach = _ONE_SCREEN_PERCENT * (screen_h if vertical else screen_w)
        span = max(box_h if vertical else box_w, 1)
        return _element_runner(container, ctx, min(1.0, reach / span))

    left, top, width, height = _screen_area(driver)
    return _perform(
        lambda percent: scroll_area(driver, left, top, width, height, direction, percent),
        (width, height), ctx["kind"], direction, ctx.get("value"),
        _ONE_SCREEN_PERCENT,
        probe=_movement_probe(driver, box=(left, top, left + width, top + height)),
    )


_ELEMENT_SCROLL_SPEC = _ActionSpec(
    runner=_element_runner, target_mode="element", op_type="scroll"
)
_SCREEN_SCROLL_SPEC = _ActionSpec(
    runner=_driver_runner, target_mode="driver", op_type=""
)


def scroll(driver, *, selectors=None, kind: str = "times", direction: str = "down",
           value=None, description: str = "", fallback_coordinates: dict | None = None):
    """Scroll the screen, or the element the selectors identify when given.

    A selector-less call may still carry ``fallback_coordinates`` — the recorded
    basis of the control the author scrolled, for a control nothing could name
    (a NumberPicker with no id or text). The screen scroll then aims at the
    container under that point rather than under the screen centre, and drags
    from the point itself when the device reports no container there.
    """
    _validate(kind, direction)
    if selectors:
        return _run_action(
            driver, _ELEMENT_SCROLL_SPEC, selectors,
            description=description,
            fallback_coordinates=fallback_coordinates,
            kind=kind, direction=direction, value=value,
        )
    return run_driver(
        driver, _SCREEN_SCROLL_SPEC, kind=kind, direction=direction, value=value,
        fallback_coordinates=fallback_coordinates,
    )
