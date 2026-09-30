"""Coordinate clicking that penetrates iframe boundaries on Firefox.

``ActionBuilder.move_to_location`` addresses the **top-level viewport**. Chrome
resolves that to whatever is painted at the point, including content inside an
iframe; geckodriver does not — the click lands on the iframe element itself, so
a coordinate or canvas click inside an iframe silently misses. That is the
Amdocs report, "Discrepancy at validation stage for Canvas elements".

The fix walks the iframe chain with ``document.elementFromPoint``, switching
into each frame and rebasing the coordinate, then clicks at the correct depth
with a real (trusted) pointer action. Works on every browser, but only Firefox
needs it, so the drill is gated — Chrome keeps its single-action fast path.

Port of V2 ``_click_at_viewport_with_iframe_drill``.
"""
import logging

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder

_log = logging.getLogger(__name__)

# Depth guard. A page cannot legitimately nest this deep, so a higher count means
# elementFromPoint is cycling — bail rather than spin.
_MAX_IFRAME_DEPTH = 100

# Returns the iframe painted at (x, y) plus its viewport rect, else null. The
# rect is what rebases the coordinate for the next level down.
_IFRAME_AT_POINT_JS = """
var x = arguments[0], y = arguments[1];
var el = document.elementFromPoint(x, y);
if (el && el.tagName === 'IFRAME') {
    var r = el.getBoundingClientRect();
    return {element: el, x: r.x, y: r.y, w: r.width, h: r.height};
}
return null;
"""


def _is_firefox(driver) -> bool:
    try:
        return (driver.capabilities.get("browserName") or "").lower() == "firefox"
    except Exception:  # noqa: BLE001 — a capability probe must never fail a click
        return False


def _click_at_viewport_with_iframe_drill(driver, x, y, max_depth: int = _MAX_IFRAME_DEPTH) -> None:
    """Drill into nested iframes, then click at the rebased coordinate.

    Always returns to the default content, including on failure — leaving the
    driver parked inside a frame would break every subsequent step, which is a
    far worse outcome than the click itself missing.
    """
    try:
        driver.switch_to.default_content()
    except Exception as e:  # noqa: BLE001
        _log.info("    [iframe-drill] could not switch to default content: %s", e)

    rel_x, rel_y = x, y
    try:
        for depth in range(max_depth):
            iframe_at_point = driver.execute_script(_IFRAME_AT_POINT_JS, rel_x, rel_y)
            if iframe_at_point is None:
                break
            _log.info(
                "    [iframe-drill] depth %d: iframe at (%s, %s) %sx%s",
                depth, iframe_at_point["x"], iframe_at_point["y"],
                iframe_at_point["w"], iframe_at_point["h"],
            )
            driver.switch_to.frame(iframe_at_point["element"])
            # The child document's origin is the iframe's top-left, so the
            # coordinate rebases by exactly that offset at each level.
            rel_x = int(rel_x - iframe_at_point["x"])
            rel_y = int(rel_y - iframe_at_point["y"])
    except Exception as e:  # noqa: BLE001 — a drill failure still gets a click attempt
        _log.info("    [iframe-drill] drill-down failed, clicking at current depth: %s", e)

    try:
        _log.info("    [iframe-drill] clicking at (%s, %s)", rel_x, rel_y)
        actions = ActionBuilder(driver)
        actions.pointer_action.move_to_location(rel_x, rel_y)
        actions.pointer_action.click()
        actions.perform()
    finally:
        try:
            driver.switch_to.default_content()
        except Exception as e:  # noqa: BLE001 — teardown must not mask the click result
            _log.info("    [iframe-drill] could not switch back to default content: %s", e)


def click_at_coordinates(driver, x, y) -> None:
    """Click at viewport coordinates, drilling into iframes on Firefox."""
    if _is_firefox(driver):
        _log.info("    [iframe-drill] firefox — drilling iframes for the coordinate click")
        _click_at_viewport_with_iframe_drill(driver, x, y)
        return
    actions = ActionBuilder(driver)
    actions.pointer_action.move_to_location(x, y)
    actions.pointer_action.click()
    actions.perform()
