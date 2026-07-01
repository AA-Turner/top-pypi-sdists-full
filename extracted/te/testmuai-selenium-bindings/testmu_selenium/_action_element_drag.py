"""element_drag wrapper — V2-parity element-relative drag with integer step loop.

WebElement form is byte-identical legacy (codegen ElementDragNode emission
unchanged): no _run_action wrap, heal lives upstream in FindElementNode's emit.

Selector-list form (spec §10.2) routes through _run_action with op_type
'click_drag' (default tier DESKTOP_LOCATE): the runner replays the legacy
gesture on the found element; the coord_runner turns a healed viewport (x, y)
into a drag_at_coordinate gesture from (x, y) to (x+dx, y+dy), end point
clamped to the viewport.

Ported from the V2 Selenium drag implementation (non-canvas branch).
The 5px step + 0.01s pause is required for sliders,
scrubbers, and signature-pad-like UIs that fire oninput on motion samples.

Selenium 4.x's PointerActions.move_by truncates both axes via int(x), int(y).
A naive float step (dx/steps) therefore drops the fractional part on every
iteration and the cumulative drag undershoots the target — e.g. (-352, -239)
becomes 71 × (-4, -3) = (-284, -213), 60-70px short of the drop zone. Use
integer ±5 step + remainder per V2.
"""
from selenium.webdriver.common.action_chains import ActionChains

from testmu_selenium._action_engine import _ActionSpec, _run_action
from testmu_selenium._helpers.drag_at_coordinate import drag_at_coordinate

# V2-parity step granularity and inter-step pause. Hardcoded.
_DRAG_STEP_PX = 5
_DRAG_STEP_PAUSE = 0.01


def element_drag(driver, source, dx, dy, *, description='', tiers=None,
                 autoheal=True, max_attempts=4, retry_delay=0.5,
                 search_root=None, fallback_coordinates=None):
    """Element-relative drag with integer 5px step + remainder loop.

    Args:
        driver: Selenium WebDriver.
        source: Already-resolved WebElement (byte-identical legacy gesture,
            heal kwargs ignored), or selector list of {'selector', 'isXPath'}
            dicts routed through the find+heal+act engine.
        dx: X-axis delta in pixels.
        dy: Y-axis delta in pixels.
        description / tiers / autoheal / max_attempts / retry_delay /
        search_root / fallback_coordinates: engine kwargs, selector form only
        (same semantics as click/hover — see _run_action).
    """
    if not isinstance(source, list):
        _legacy_element_drag(driver, source, dx, dy)
        return
    return _run_action(
        driver, _DRAG_SPEC, source,
        description=description, tiers=tiers, autoheal=autoheal,
        max_attempts=max_attempts, retry_delay=retry_delay,
        search_root=search_root,
        fallback_coordinates=fallback_coordinates,
        dx=dx, dy=dy,
    )


def _legacy_element_drag(driver, element, dx, dy):
    """V2-parity gesture on an already-resolved source WebElement."""
    dx = int(dx)
    dy = int(dy)

    actions = ActionChains(driver)
    actions.click_and_hold(element)

    remaining_x = dx
    remaining_y = dy

    while remaining_x != 0 or remaining_y != 0:
        if abs(remaining_x) >= _DRAG_STEP_PX:
            step_x = _DRAG_STEP_PX if remaining_x > 0 else -_DRAG_STEP_PX
        else:
            step_x = remaining_x

        if abs(remaining_y) >= _DRAG_STEP_PX:
            step_y = _DRAG_STEP_PX if remaining_y > 0 else -_DRAG_STEP_PX
        else:
            step_y = remaining_y

        actions.move_by_offset(step_x, step_y)
        actions.pause(_DRAG_STEP_PAUSE)

        remaining_x -= step_x
        remaining_y -= step_y

    actions.release()
    actions.perform()


def _element_drag_runner(element, ctx):
    _legacy_element_drag(ctx['driver'], element, ctx['dx'], ctx['dy'])
    return True


# Coordinate-tier fallback: the heal resolved the drag SOURCE to a viewport
# point but derived no xpath. Drag from the healed point by the requested
# offset; the end point is clamped to the viewport so a stale offset never
# throws the pointer out of bounds.
def _element_drag_coord_runner(driver, x, y, ctx):
    vw, vh = driver.execute_script(
        "return [window.innerWidth, window.innerHeight]")
    end_x = max(0, min(int(x) + int(ctx['dx']), int(vw) - 1))
    end_y = max(0, min(int(y) + int(ctx['dy']), int(vh) - 1))
    drag_at_coordinate(driver, x, y, end_x, end_y)
    return True


# Recoverable set inherits the engine default — see _DEFAULT_RECOVERABLE
# in _action_engine. op_type 'click_drag' selects the drag tagify branch in
# the heal payload (V2 parity).
_DRAG_SPEC = _ActionSpec(runner=_element_drag_runner,
                         coord_runner=_element_drag_coord_runner,
                         op_type='click_drag')
