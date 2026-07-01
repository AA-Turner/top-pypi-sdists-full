"""Drag helpers for Playwright.

``click_drag``  — raw coordinate click-and-drag (unchanged).

``drag_drop``   — polymorphic V2-parity element-pair drag with a V3-gated heal
path. Async Playwright port of the selenium reference
``testmu_selenium._action_drag_drop`` (spec §10.1):

- Locator/handle PAIR (neither endpoint is a selector list) → a real pointer
  gesture computed from each element's rect centre; heal is never engaged and
  the heal kwargs are ignored. This is the shape codegen emits today.
- Selector-list endpoints (possibly empty) → heal path: per-endpoint sequential
  resolution — ``page.locator(...)`` wait, then DESKTOP_LOCATE for the failed
  endpoint (source ``drop_aware=False``, target ``drop_aware=True``) →
  ``resolve_coordinate`` → verified-xpath element, or a coordinate endpoint on
  resolver bail. Gesture matrix: both elements → element gesture; any coordinate
  endpoint → coordinate pointer gesture (element endpoints convert via rect
  centre, clamped to the viewport).

Attempt loop mirrors the selenium reference per-endpoint: fresh heal coordinates
are stashed and consumed on the NEXT attempt without re-entering locate. On
exhaustion, recorded ``fallback_coordinates`` dispatch one final stored-pair
coordinate gesture; without them ``AutohealExhausted`` is raised. Stored coords
are never consulted before exhaustion.

The (0.1, 0.1) drop-zone nudge before release is deliberate (V2 parity) — some
frameworks need a pointer-move while hovering the drop zone to register that a
draggable is over it and activate the drop.

Divergences from the sync selenium reference (documented for review):

1. ``get_v3_desktop_locate_target`` (the PW DESKTOP_LOCATE client) returns
   ``None`` on miss / non-200 / transport / invalid-PNG / empty-intent and never
   raises — unlike selenium's ``Heal.desktop_locate`` which raises
   ``HealTierMiss``. PW therefore has no ``HealTierMiss``; the None is converted
   at the endpoint boundary into the private ``_LocateMiss`` marker which routes
   to the same exhaustion path (selenium reaches it via ``HealTierMiss``). The
   selenium "infra-exception → tier-miss conversion" is intrinsic here because
   the PW client already collapses every failure to None.
2. Heal is gated on ``kane_version == 'v3'`` (mirroring ``_heal_patch.py``); the
   selenium binding is V3-only so it has no such gate. A successful selector
   drag still works in v4 — only the DESKTOP_LOCATE fallback is V3-gated.
3. Playwright has no ActionChains ``move_to_element``; both gestures run on
   ``page.mouse`` and element endpoints convert to centres via
   ``locator.bounding_box()``.
"""
import asyncio
import logging

from testmu import _configure
from testmu._errors import AutohealExhausted
from testmu._heal_cascade import get_v3_desktop_locate_target
from testmu._helpers._coordinate_resolver import resolve_coordinate

_log = logging.getLogger("testmu")

# Recoverable lookup/gesture failures — Playwright's auto-wait timeout plus the
# stdlib alias (mirrors _action_engine._DEFAULT_RECOVERABLE / _heal_patch).
try:
    from playwright.async_api import TimeoutError as _PWTimeoutError
    _RECOVERABLE: tuple = (_PWTimeoutError, TimeoutError)
except ImportError:  # playwright absent (unit tests) — stdlib alias only.
    _RECOVERABLE = (TimeoutError,)

# V2-parity constants (selenium _action_drag_drop parity). Hardcoded — V2 does
# not parameterize these.
_DROP_ZONE_NUDGE_X = 0.1
_DROP_ZONE_NUDGE_Y = 0.1
_COORD_GESTURE_PAUSE = 0.1
# Intermediate mousemove steps for the drag travel. HTML5 drag-and-drop needs
# interim pointermove events to register the drag; matches click_drag's default.
_DRAG_STEPS = 20
# Cap the heal-derived-xpath re-lookup so a stale derived selector fails fast to
# the same round's coordinates instead of burning the full action timeout.
_DERIVED_LOOKUP_CAP_MS = 5000


async def click_drag(page, x1, y1, x2, y2, steps=20):
    """Perform click-and-drag from start to end coordinates with intermediate steps."""
    _log.info("    [click_drag] (%d, %d) → (%d, %d) over %d steps", x1, y1, x2, y2, steps)
    await page.mouse.move(x1, y1)
    await page.mouse.down()
    await page.mouse.move(x2, y2, steps=steps)
    await page.mouse.up()
    _log.info("    [click_drag] completed")


class _LocateMiss(Exception):
    """Internal control-flow marker: DESKTOP_LOCATE missed for an endpoint.

    PW's get_v3_desktop_locate_target returns None on miss/transport/infra/empty
    intent (it never raises, unlike selenium's Heal.desktop_locate which raises
    HealTierMiss). We convert that None into this marker at the endpoint boundary
    so _drag_drop_heal routes to the same exhaustion path selenium reaches via
    HealTierMiss — fallback_coordinates if recorded, else AutohealExhausted.
    """

    def __init__(self, original):
        self.original = original
        super().__init__("DESKTOP_LOCATE miss")


async def drag_drop(page, source, target, *,
                    source_description='', target_description='',
                    fallback_coordinates=None,
                    autoheal=True, max_attempts=3, retry_delay=0.5):
    """Drag source onto target with a V2-parity gesture; heal selector endpoints.

    Args:
        page: Playwright Page.
        source: Already-resolved Locator/ElementHandle, or a selector list
            (possibly empty) of ``{'selector', 'isXPath'}`` dicts.
        target: Same shapes as source.
        source_description: Heal intent for the source endpoint.
        target_description: Heal intent for the target endpoint.
        fallback_coordinates: Recorded authoring-time ``((sx, sy), (ex, ey))``
            viewport-CSS pair — last resort on heal exhaustion only; never
            short-circuits a fresh resolve.
        autoheal: False → endpoint lookup errors propagate, no locate calls.
        max_attempts: Attempt-loop budget for the heal path.
        retry_delay: Sleep between heal-path attempts.

    Locator/handle pair → element gesture; heal kwargs ignored on this shape.
    """
    if not isinstance(source, list) and not isinstance(target, list):
        await _element_pair_gesture(page, source, target)
        return
    return await _drag_drop_heal(
        page, source, target,
        source_description=source_description,
        target_description=target_description,
        fallback_coordinates=fallback_coordinates,
        autoheal=autoheal, max_attempts=max_attempts, retry_delay=retry_delay,
    )


async def element_drag(page, source, dx, dy, *,
                       description='', fallback_coordinates=None,
                       autoheal=True, max_attempts=4, retry_delay=0.5):
    """Heal-capable relative element drag (V3-gated heal path).

    Args:
        page: Playwright Page.
        source: Already-resolved Locator/ElementHandle, or a selector list
            of {'selector', 'isXPath'} dicts.
        dx: X-axis delta in pixels (signed).
        dy: Y-axis delta in pixels (signed).
        description: Heal intent for the source endpoint (selector-list form
            only; ignored for Locator/ElementHandle source).
        fallback_coordinates: Recorded authoring-time (x, y) source point —
            last resort on heal exhaustion only; drags (x,y)->(x+dx,y+dy)
            clamped to the viewport. A SINGLE tuple (contrast drag_drop's pair).
        autoheal: False → lookup errors propagate, no DESKTOP_LOCATE calls.
        max_attempts: Attempt-loop budget for the heal path.
        retry_delay: Sleep between heal-path attempts.

    Locator/ElementHandle source → coordinate gesture from element centre to
    centre+(dx,dy); heal kwargs ignored on this shape.
    Selector-list source (possibly empty) → heal path; V3-gated
    DESKTOP_LOCATE on lookup miss. Heal is never engaged for non-v3
    kane_version or when autoheal=False. On exhaustion: fallback_coordinates
    dispatches a single clamped coordinate gesture, else AutohealExhausted.
    """
    if not isinstance(source, list):
        cx, cy = await _element_center(page, source)
        _log.info("    [element_drag] element centre (%s, %s) dx=%s dy=%s",
                  cx, cy, dx, dy)
        return await _coordinate_gesture(page, (cx, cy), (cx + dx, cy + dy))
    return await _element_drag_heal(
        page, source, dx, dy,
        description=description,
        fallback_coordinates=fallback_coordinates,
        autoheal=autoheal, max_attempts=max_attempts, retry_delay=retry_delay,
    )


# ---------------------------------------------------------------------------
# Gestures
# ---------------------------------------------------------------------------

def _build_locator(page, selector_list):
    """First selector in the list → a Playwright Locator (xpath= prefix for
    xpath selectors; raw CSS otherwise — same convention as _default_heal)."""
    sel = selector_list[0]
    raw = sel.get("selector", "")
    if sel.get("isXPath"):
        return page.locator(f"xpath={raw}")
    return page.locator(raw)


def _lookup_timeout_ms() -> int:
    return _configure.get("default_action_timeout_ms") or 10000


async def _viewport(page):
    dims = await page.evaluate("() => [window.innerWidth, window.innerHeight]")
    return int(dims[0]), int(dims[1])


async def _element_center(page, locator):
    """Element endpoint → viewport-CSS rect centre, clamped to the viewport."""
    box = await locator.bounding_box()
    if not box:
        # No box → not rendered/attached; treat as a recoverable miss so the
        # attempt loop can retry (or fall through to exhaustion).
        raise TimeoutError("element has no bounding box (not visible/attached)")
    cx = box["x"] + box["width"] / 2
    cy = box["y"] + box["height"] / 2
    vw, vh = await _viewport(page)
    return (
        max(0, min(int(cx), vw - 1)),
        max(0, min(int(cy), vh - 1)),
    )


async def _element_gesture(page, src_xy, tgt_xy):
    """V2-parity element drag: press at source, travel to the drop zone, then a
    (0.1, 0.1) nudge at the drop zone to activate the droppable before release."""
    sx, sy = src_xy
    tx, ty = tgt_xy
    await page.mouse.move(sx, sy)
    await page.mouse.down()
    await page.mouse.move(tx, ty, steps=_DRAG_STEPS)
    await page.mouse.move(tx + _DROP_ZONE_NUDGE_X, ty + _DROP_ZONE_NUDGE_Y)
    await page.mouse.up()
    return True


async def _coordinate_gesture(page, src_xy, tgt_xy):
    """V2 coordinate pointer drag: press at src, settle, travel to tgt, settle, release."""
    sx, sy = src_xy
    tx, ty = tgt_xy
    await page.mouse.move(sx, sy)
    await page.mouse.down()
    await asyncio.sleep(_COORD_GESTURE_PAUSE)
    await page.mouse.move(tx, ty, steps=_DRAG_STEPS)
    await asyncio.sleep(_COORD_GESTURE_PAUSE)
    await page.mouse.up()
    return True


async def _element_pair_gesture(page, source, target):
    """Both endpoints are elements → V2 element gesture. Centres are computed
    first so a stale endpoint fails BEFORE any mouse press is issued."""
    src_c = await _element_center(page, source)
    tgt_c = await _element_center(page, target)
    return await _element_gesture(page, src_c, tgt_c)


# ---------------------------------------------------------------------------
# Heal path
# ---------------------------------------------------------------------------

async def _resolve_endpoint(page, selector_or_element, description, *,
                            is_target, autoheal, stashed_coords):
    """Resolve one drag endpoint → ``((locator, coords), fresh_heal_coords)``.

    Exactly one of locator/coords is non-None. fresh_heal_coords is set only when
    a locate call fired this round — the caller stashes it so the next attempt
    reuses the coordinates WITHOUT re-entering locate.
    Raises _LocateMiss when the locate misses (exhaustion path) and the original
    lookup error when autoheal is False or kane_version != 'v3'.
    """
    if stashed_coords is not None:
        return (None, stashed_coords), None
    if not isinstance(selector_or_element, list):
        # Already-resolved endpoint (pair/mixed shape) — passthrough.
        return (selector_or_element, None), None
    try:
        if not selector_or_element:
            raise TimeoutError("empty selector list")
        locator = _build_locator(page, selector_or_element)
        await locator.wait_for(state="visible", timeout=_lookup_timeout_ms())
        return (locator, None), None
    except _RECOVERABLE as lookup_exc:
        # Heal is V3-only; in v4 (or with autoheal off) the lookup error
        # propagates without any DESKTOP_LOCATE call (mirrors _heal_patch gate).
        if not autoheal or _configure.get("kane_version") != "v3":
            raise
        endpoint = "target" if is_target else "source"
        _log.info(
            "    [drag_drop] %s endpoint lookup failed (%s); DESKTOP_LOCATE drop_aware=%s",
            endpoint, type(lookup_exc).__name__, is_target,
        )
        coords = await get_v3_desktop_locate_target(
            page, description, method_name="drag_drop", drop_aware=is_target,
        )
        if coords is None:
            # PW locate never raises; None == miss/transport/infra/empty-intent.
            raise _LocateMiss(lookup_exc) from lookup_exc
        vx, vy = coords
        resolved = await resolve_coordinate(page, vx, vy)
        if resolved is not None:
            try:
                derived = page.locator(f"xpath={resolved.xpath}")
                await derived.wait_for(
                    state="visible",
                    timeout=min(_lookup_timeout_ms(), _DERIVED_LOOKUP_CAP_MS),
                )
                return (derived, None), (vx, vy)
            except _RECOVERABLE:
                # Derived xpath unfindable — the same round's coordinates carry
                # the gesture (one locate serves both).
                pass
        return (None, (vx, vy)), (vx, vy)


async def _drag_drop_heal(page, source, target, *, source_description,
                          target_description, fallback_coordinates, autoheal,
                          max_attempts, retry_delay):
    first_exc = None
    # Per-endpoint fresh-coords stash: [source, target]. Consumed (cleared) by
    # _resolve_endpoint on the attempt after the heal round that filled it.
    stash: list[tuple[int, int] | None] = [None, None]
    for attempt in range(max_attempts):
        _log.info("    [drag_drop] is_retry: %s", attempt > 0)
        try:
            (src_loc, src_xy), stash[0] = await _resolve_endpoint(
                page, source, source_description,
                is_target=False, autoheal=autoheal, stashed_coords=stash[0])
            (tgt_loc, tgt_xy), stash[1] = await _resolve_endpoint(
                page, target, target_description,
                is_target=True, autoheal=autoheal, stashed_coords=stash[1])
        except _LocateMiss as miss:
            return await _exhaust(page, fallback_coordinates,
                                  first_exc or miss.original)
        try:
            if src_loc is not None and tgt_loc is not None:
                return await _element_pair_gesture(page, src_loc, tgt_loc)
            src_xy = src_xy if src_xy is not None else await _element_center(page, src_loc)
            tgt_xy = tgt_xy if tgt_xy is not None else await _element_center(page, tgt_loc)
            _log.info("    [drag_drop] coordinate gesture %s -> %s", src_xy, tgt_xy)
            return await _coordinate_gesture(page, src_xy, tgt_xy)
        except _RECOVERABLE as exc:
            if first_exc is None:
                first_exc = exc
            if not autoheal:
                raise
            if attempt == max_attempts - 1:
                return await _exhaust(page, fallback_coordinates, first_exc)
            _log.info(
                "    [drag_drop] retry %d/%d after %s: %s",
                attempt + 1, max_attempts, type(exc).__name__, exc,
            )
            await asyncio.sleep(retry_delay)


async def _exhaust(page, fallback_coordinates, original):
    """Exhaustion: stored-pair gesture when marked, else AutohealExhausted.

    The stored pair is dispatched exactly once and its own failure propagates —
    true last resort, never retried.
    """
    if fallback_coordinates is not None:
        src_xy, tgt_xy = fallback_coordinates
        _log.info(
            "    [drag_drop] heal exhausted; recorded fallback_coordinates %s -> %s",
            src_xy, tgt_xy,
        )
        return await _coordinate_gesture(page, src_xy, tgt_xy)
    raise AutohealExhausted("drag_drop heal cascade exhausted") from original


# ---------------------------------------------------------------------------
# element_drag heal path
# ---------------------------------------------------------------------------

async def _resolve_source(page, selector_or_element, description, *,
                          autoheal, stashed_coords):
    """Resolve the element_drag source endpoint → ``((locator, coords), fresh_heal_coords)``.

    Mirrors _resolve_endpoint for the single-source (drop_aware=False) case.
    Exactly one of locator/coords is non-None. fresh_heal_coords is set only
    when a locate call fired this round — the caller stashes it so the next
    attempt reuses coordinates WITHOUT re-entering locate.
    Raises _LocateMiss when locate misses, or the original lookup error when
    autoheal is False or kane_version != 'v3'.
    """
    if stashed_coords is not None:
        return (None, stashed_coords), None
    if not isinstance(selector_or_element, list):
        # Already-resolved endpoint (passed through from a mixed-shape caller).
        return (selector_or_element, None), None
    try:
        if not selector_or_element:
            raise TimeoutError("empty selector list")
        locator = _build_locator(page, selector_or_element)
        await locator.wait_for(state="visible", timeout=_lookup_timeout_ms())
        return (locator, None), None
    except _RECOVERABLE as lookup_exc:
        if not autoheal or _configure.get("kane_version") != "v3":
            raise
        _log.info(
            "    [element_drag] source lookup failed (%s); DESKTOP_LOCATE drop_aware=False",
            type(lookup_exc).__name__,
        )
        coords = await get_v3_desktop_locate_target(
            page, description, method_name="element_drag", drop_aware=False,
        )
        if coords is None:
            raise _LocateMiss(lookup_exc) from lookup_exc
        vx, vy = coords
        resolved = await resolve_coordinate(page, vx, vy)
        if resolved is not None:
            try:
                derived = page.locator(f"xpath={resolved.xpath}")
                await derived.wait_for(
                    state="visible",
                    timeout=min(_lookup_timeout_ms(), _DERIVED_LOOKUP_CAP_MS),
                )
                return (derived, None), (vx, vy)
            except _RECOVERABLE:
                # Derived xpath unfindable — same round's coordinates carry the
                # gesture.
                pass
        return (None, (vx, vy)), (vx, vy)


async def _element_drag_heal(page, source, dx, dy, *, description,
                              fallback_coordinates, autoheal, max_attempts, retry_delay):
    first_exc = None
    stash = None  # stashed heal coords (vx, vy) from the previous attempt
    for attempt in range(max_attempts):
        _log.info("    [element_drag] is_retry: %s", attempt > 0)
        try:
            (origin_loc, origin_xy), fresh = await _resolve_source(
                page, source, description,
                autoheal=autoheal, stashed_coords=stash,
            )
        except _LocateMiss as miss:
            return await _element_drag_exhaust(
                page, dx, dy, fallback_coordinates, first_exc or miss.original,
            )
        stash = fresh
        try:
            if origin_xy is not None:
                ox, oy = origin_xy
            else:
                ox, oy = await _element_center(page, origin_loc)
            vw, vh = await _viewport(page)
            ex = max(0, min(int(ox + dx), vw - 1))
            ey = max(0, min(int(oy + dy), vh - 1))
            _log.info("    [element_drag] origin (%s, %s) → end (%s, %s)", ox, oy, ex, ey)
            return await _coordinate_gesture(page, (ox, oy), (ex, ey))
        except _RECOVERABLE as exc:
            if first_exc is None:
                first_exc = exc
            if not autoheal:
                raise
            if attempt == max_attempts - 1:
                return await _element_drag_exhaust(
                    page, dx, dy, fallback_coordinates, first_exc,
                )
            _log.info(
                "    [element_drag] retry %d/%d after %s: %s",
                attempt + 1, max_attempts, type(exc).__name__, exc,
            )
            await asyncio.sleep(retry_delay)


async def _element_drag_exhaust(page, dx, dy, fallback_coordinates, original):
    """Exhaustion for element_drag.

    fallback_coordinates is a single (x, y) source point (NOT a stored pair —
    contrast drag_drop's _exhaust). End point (x+dx, y+dy) is clamped to the
    viewport.
    """
    if fallback_coordinates is not None:
        fx, fy = fallback_coordinates
        vw, vh = await _viewport(page)
        ex = max(0, min(int(fx + dx), vw - 1))
        ey = max(0, min(int(fy + dy), vh - 1))
        _log.info(
            "    [element_drag] heal exhausted; recorded fallback_coordinates"
            " (%s, %s) → end (%s, %s)", fx, fy, ex, ey,
        )
        return await _coordinate_gesture(page, (fx, fy), (ex, ey))
    raise AutohealExhausted("element_drag heal cascade exhausted") from original
