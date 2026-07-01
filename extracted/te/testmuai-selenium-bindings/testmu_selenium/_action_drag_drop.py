"""drag_drop wrapper — polymorphic V2-parity element-pair drag + heal path.

WebElement pair → byte-identical legacy gesture (V2-parity ActionChains chain
with the 0.1 drop-zone nudge); heal kwargs are ignored on this shape and Heal
is never constructed. Codegen DragDropNode emission hits this path unchanged.

Selector-list endpoints (possibly empty) → heal path (spec §10.1): per-endpoint
sequential resolution — findElement ladder, then DESKTOP_LOCATE for the failed
endpoint (source drop_aware=False, target drop_aware=True) → resolve_coordinate
→ verified-xpath element, or coordinate endpoint on resolver bail. Gesture:
both elements → legacy chain; any coordinate endpoint → V2 ActionBuilder
pointer gesture (element endpoints convert via rect center, clamped).

Attempt loop mirrors _run_action's semantics per-endpoint: engine recoverable
set, fresh heal coords stashed and consumed on the NEXT attempt without
re-entering locate. On exhaustion (HealTierMiss or max_attempts), recorded
fallback_coordinates dispatch one final stored-pair coordinate gesture (its own
failure propagates); without them AutohealExhausted is raised. Stored coords
are never consulted before exhaustion (spec §6 contract).

Ported from the V2 Selenium drag implementation.
The (0.1, 0.1) move_by_offset before release is deliberate — some frameworks
need to register an event that a draggable is hovering over the drop zone to
activate it for the drop.
"""
import logging
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder

from testmu_selenium._action_engine import _DEFAULT_RECOVERABLE
from testmu_selenium._errors import AutohealExhausted, HealTierMiss
from testmu_selenium._heal import Heal
from testmu_selenium._heal_cascade import _synthesize_current_action
from testmu_selenium._helpers._coordinate_resolver import resolve_coordinate
from testmu_selenium._helpers.find_element import findElement

_log = logging.getLogger(__name__)

# V2-parity drop-zone activation jiggle. Hardcoded — V2 does not parameterize.
_DROP_ZONE_NUDGE_X = 0.1
_DROP_ZONE_NUDGE_Y = 0.1

# V2-parity inter-step settle pause in the coordinate pointer gesture.
_COORD_GESTURE_PAUSE = 0.1


def drag_drop(driver, source, target, *,
              source_description='', target_description='',
              fallback_coordinates=None,
              autoheal=True, max_attempts=3, retry_delay=0.5):
    """Drag source onto target with V2-parity gesture; heal selector endpoints.

    Args:
        driver: Selenium WebDriver.
        source: Already-resolved WebElement, or selector list (possibly empty)
            of {'selector', 'isXPath'} dicts.
        target: Same shapes as source.
        source_description: Heal intent for the source endpoint.
        target_description: Heal intent for the target endpoint.
        fallback_coordinates: Recorded authoring-time ((sx, sy), (ex, ey))
            viewport-CSS pair — last resort on heal exhaustion only; never
            short-circuits a fresh resolve.
        autoheal: False → endpoint lookup errors propagate, no locate calls.
        max_attempts: Attempt-loop budget for the heal path.
        retry_delay: Sleep between heal-path attempts.

    WebElement pair → legacy gesture; heal kwargs ignored on this shape.
    """
    if not isinstance(source, list) and not isinstance(target, list):
        _element_gesture(driver, source, target)
        return
    return _drag_drop_heal(
        driver, source, target,
        source_description=source_description,
        target_description=target_description,
        fallback_coordinates=fallback_coordinates,
        autoheal=autoheal, max_attempts=max_attempts, retry_delay=retry_delay,
    )


# ---------------------------------------------------------------------------
# Gestures
# ---------------------------------------------------------------------------

def _element_gesture(driver, source_element, target_element):
    """V2-parity element-pair chain with drop-zone activation jiggle."""
    ActionChains(driver) \
        .move_to_element(source_element) \
        .click_and_hold(source_element) \
        .move_to_element(target_element) \
        .move_by_offset(_DROP_ZONE_NUDGE_X, _DROP_ZONE_NUDGE_Y) \
        .release() \
        .perform()


def _coordinate_gesture(driver, src_xy, tgt_xy):
    """V2 coordinate pointer drag: press at src, settle, move to tgt, release."""
    ab = ActionBuilder(driver)
    ab.pointer_action.move_to_location(src_xy[0], src_xy[1])
    ab.pointer_action.pointer_down()
    ab.pointer_action.pause(_COORD_GESTURE_PAUSE)
    ab.pointer_action.move_to_location(tgt_xy[0], tgt_xy[1])
    ab.pointer_action.pause(_COORD_GESTURE_PAUSE)
    ab.pointer_action.pointer_up()
    ab.perform()
    return True


def _element_viewport_center(driver, element):
    """Element endpoint → viewport-CSS rect center, clamped to the viewport."""
    cx, cy, vw, vh = driver.execute_script(
        "var r = arguments[0].getBoundingClientRect();"
        "return [r.x + r.width / 2, r.y + r.height / 2,"
        " window.innerWidth, window.innerHeight];",
        element,
    )
    return (
        max(0, min(int(cx), int(vw) - 1)),
        max(0, min(int(cy), int(vh) - 1)),
    )


# ---------------------------------------------------------------------------
# Heal path
# ---------------------------------------------------------------------------

def _resolve_endpoint(driver, selector_or_element, description, *,
                      is_target, autoheal, stashed_coords):
    """Resolve one drag endpoint → ((element, coords), fresh_heal_coords).

    Exactly one of element/coords is non-None. fresh_heal_coords is set only
    when a locate call fired this round — the caller stashes it so the next
    attempt reuses the coordinates WITHOUT re-entering locate.
    Raises HealTierMiss when the locate misses (exhaustion path) and the
    lookup error when autoheal is False.
    """
    if stashed_coords is not None:
        return (None, stashed_coords), None
    if not isinstance(selector_or_element, list):
        # Already-resolved WebElement endpoint (mixed shape) — passthrough.
        return (selector_or_element, None), None
    try:
        el = findElement(driver, selector_or_element, description=description,
                         allow_autoheal=False)
        return (el, None), None
    except _DEFAULT_RECOVERABLE as lookup_exc:
        if not autoheal:
            raise
        endpoint = "target" if is_target else "source"
        _log.info("    [AutoHeal] drag %s endpoint lookup failed (%s); DESKTOP_LOCATE",
                  endpoint, type(lookup_exc).__name__)
        current_action = _synthesize_current_action(
            description, selector_or_element, op_type="drag_drop")
        healer = Heal(current_action, driver)
        try:
            vx, vy = healer.desktop_locate(drop_aware=is_target)
        except HealTierMiss as miss:
            # Chain the lookup error so the exhaustion path can surface the
            # original Selenium failure as AutohealExhausted.original.
            raise miss from lookup_exc
        except Exception as e:
            # Heal-infrastructure failure (transport error after retries,
            # malformed JSON, screenshot/driver failure) — convert to a tier
            # miss like the engine cascade does, so exhaustion still consults
            # fallback_coordinates instead of leaking the raw exception.
            raise HealTierMiss("DESKTOP_LOCATE", str(e)) from e
        resolved = resolve_coordinate(driver, vx, vy)
        if resolved is not None:
            try:
                el = findElement(driver,
                                 [{"selector": resolved.xpath, "isXPath": True}],
                                 description=description, allow_autoheal=False)
                return (el, None), (vx, vy)
            except _DEFAULT_RECOVERABLE:
                # Derived xpath unfindable — the same round's coordinates
                # carry the gesture (one locate serves both, spec §3.3).
                pass
        return (None, (vx, vy)), (vx, vy)


def _drag_drop_heal(driver, source, target, *, source_description,
                    target_description, fallback_coordinates, autoheal,
                    max_attempts, retry_delay):
    first_exc = None
    # Per-endpoint fresh-coords stash: [source, target]. Consumed (cleared) by
    # _resolve_endpoint on the attempt after the heal round that filled it.
    stash: list[tuple[int, int] | None] = [None, None]
    for attempt in range(max_attempts):
        _log.info("    is_retry: %s", attempt > 0)
        try:
            (src_el, src_xy), stash[0] = _resolve_endpoint(
                driver, source, source_description,
                is_target=False, autoheal=autoheal, stashed_coords=stash[0])
            (tgt_el, tgt_xy), stash[1] = _resolve_endpoint(
                driver, target, target_description,
                is_target=True, autoheal=autoheal, stashed_coords=stash[1])
        except HealTierMiss as miss:
            original = first_exc or miss.__cause__ or miss
            return _exhaust(driver, fallback_coordinates, original, miss)
        try:
            if src_el is not None and tgt_el is not None:
                _element_gesture(driver, src_el, tgt_el)
                return True
            src_xy = src_xy if src_xy is not None else _element_viewport_center(driver, src_el)
            tgt_xy = tgt_xy if tgt_xy is not None else _element_viewport_center(driver, tgt_el)
            _log.info("    [AutoHeal] drag coordinate gesture %s -> %s", src_xy, tgt_xy)
            return _coordinate_gesture(driver, src_xy, tgt_xy)
        except _DEFAULT_RECOVERABLE as exc:
            if first_exc is None:
                first_exc = exc
            if not autoheal:
                raise
            if attempt == max_attempts - 1:
                return _exhaust(driver, fallback_coordinates, first_exc, None)
            _log.info(
                "    [retry] attempt %d/%d after %s: %s",
                attempt + 1, max_attempts, type(exc).__name__, exc,
            )
            time.sleep(retry_delay)


def _exhaust(driver, fallback_coordinates, original, last_miss):
    """Exhaustion: stored-pair gesture when marked, else AutohealExhausted.

    The stored pair is dispatched exactly once and its own failure propagates
    — true last resort, never retried (spec §10.1).
    """
    if fallback_coordinates is not None:
        src_xy, tgt_xy = fallback_coordinates
        _log.info(
            "    [AutoHeal] drag heal exhausted; recorded fallback_coordinates %s -> %s",
            src_xy, tgt_xy,
        )
        return _coordinate_gesture(driver, src_xy, tgt_xy)
    raise AutohealExhausted(original=original, last_miss=last_miss)
