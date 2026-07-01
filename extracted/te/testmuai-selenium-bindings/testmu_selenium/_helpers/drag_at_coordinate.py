"""drag_at_coordinate helper — V2-parity canvas-coordinate drag.

Driver-level helper, not _run_action-wrapped — no element to heal.
Anchors gesture on /html/body and converts absolute viewport coordinates to
viewport-centered offsets, then runs an integer 5px / 0.01s step loop.

Selenium 4.x's PointerActions.move_by truncates both axes via int(x), int(y).
A naive float step (delta/steps) therefore drops the fractional part on every
iteration and the cumulative drag undershoots the target — e.g. (352, 239)
becomes 71 × (4, 3) = (284, 213), ~60-70px short; a minor axis whose per-step
delta is < 1px (e.g. dy 0.833) truncates to 0 and collapses entirely. Use the
integer ±5 step + remainder loop, identical to _legacy_element_drag.

Ported from the V2 Selenium canvas-branch drag implementation.
"""
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from testmu_selenium._errors import TestmuConfigError

_DRAG_STEP_PX = 5
_DRAG_STEP_PAUSE = 0.01


def drag_at_coordinate(driver, start_x, start_y, end_x, end_y):
    """Canvas-coordinate drag anchored on /html/body with viewport-centered offsets.

    Args:
        driver: Selenium WebDriver.
        start_x, start_y: Absolute viewport coordinates of the drag start.
        end_x, end_y: Absolute viewport coordinates of the drag end.

    Raises:
        TestmuConfigError: When the page does not respond to viewport size
            queries (e.g., mid-navigation or blocking dialog).
    """
    html = driver.find_element(By.XPATH, "/html/body")
    vw = driver.execute_script("return window.innerWidth")
    vh = driver.execute_script("return window.innerHeight")

    if vw is None or vh is None:
        raise TestmuConfigError(
            "drag_at_coordinate: viewport width/height unavailable — "
            "page may be mid-navigation or have a blocking dialog."
        )

    sx = start_x - vw / 2
    sy = start_y - vh / 2
    ex = end_x - vw / 2
    ey = end_y - vh / 2

    # Integer ±5 step + remainder loop so the steps sum EXACTLY to the requested
    # displacement. move_by_offset int()-truncates each axis toward zero, so any
    # fractional per-step delta is silently dropped — a float step (delta/steps)
    # undershoots and a sub-pixel minor axis collapses to 0. The vw/2 anchor
    # terms cancel in (ex - sx) == (end_x - start_x), so the displacement is
    # viewport-independent. Mirrors _legacy_element_drag.
    remaining_x = int(ex - sx)
    remaining_y = int(ey - sy)

    chain = ActionChains(driver) \
        .move_to_element_with_offset(html, sx, sy) \
        .click_and_hold()
    while remaining_x != 0 or remaining_y != 0:
        if abs(remaining_x) >= _DRAG_STEP_PX:
            step_x = _DRAG_STEP_PX if remaining_x > 0 else -_DRAG_STEP_PX
        else:
            step_x = remaining_x

        if abs(remaining_y) >= _DRAG_STEP_PX:
            step_y = _DRAG_STEP_PX if remaining_y > 0 else -_DRAG_STEP_PX
        else:
            step_y = remaining_y

        chain.move_by_offset(step_x, step_y).pause(_DRAG_STEP_PAUSE)
        remaining_x -= step_x
        remaining_y -= step_y

    chain.release().perform()
