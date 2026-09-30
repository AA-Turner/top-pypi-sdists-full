"""Ship the interacted element's rect so the run UI can annotate the screenshot.

The instance view draws a marker over the element a step acted on. It gets that
rect from the ``lambda-element-bounds`` hook, emitted just before the verb runs
("Incorrect Screenshot displayed while re-authoring the test").

The rect is in **main-page** coordinates. ``element.rect`` is relative to the
element's own document, so an element inside an iframe would be annotated at the
wrong place on a top-level screenshot — the JS below walks the frame chain and
adds each owner's offset, mirroring V2's ``_MAIN_PAGE_RECT_JS``.

Best-effort throughout: this is reporting, and a marker that fails to draw must
never fail the step that was otherwise fine.
"""
import json
import logging

_log = logging.getLogger(__name__)

# Element bbox in top-level (main page) coords — walks up the frame chain.
# Read-only and same-origin; a cross-origin hop throws on frameElement and the
# loop stops, leaving the rect correct for as far as it could see.
_MAIN_PAGE_RECT_JS = """
var el = arguments[0];
var r = el.getBoundingClientRect();
var x = r.left, y = r.top, w = r.width, h = r.height;
var win = el.ownerDocument.defaultView;
while (win && win !== win.top) {
    var fe = null;
    try { fe = win.frameElement; } catch (e) { break; }
    if (!fe) break;
    var fr = fe.getBoundingClientRect();
    x += fr.left; y += fr.top;
    win = win.parent;
}
return {'x': x, 'y': y, 'width': w, 'height': h};
"""


def _emit_bounds(driver, rect: dict) -> None:
    """Ship one ``lambda-element-bounds`` event. No-op off the cloud run target."""
    from testmu_selenium import _config
    if _config.run_target != "cloud":
        return
    try:
        from testmu_selenium._step import _current_step
        step = _current_step.get()
        instruction_id = getattr(step, "instruction_id", None) if step else None
        args = {
            "x": rect.get("x", 0),
            "y": rect.get("y", 0),
            "width": rect.get("width", 0),
            "height": rect.get("height", 0),
        }
        if instruction_id:
            args["instructionId"] = instruction_id
        driver.execute_script("lambda-element-bounds=" + json.dumps(args))
    except Exception as e:  # noqa: BLE001 — reporting must never fail a step
        _log.debug("[bounds] emit skipped: %s", e)


def send_element_bounds(driver, element) -> None:
    """Report the element's main-page rect before the verb runs.

    Falls back to ``element.rect`` when the frame-walk fails: a rect in the
    element's own coordinate space still annotates correctly for the common
    top-level case, and is strictly better than no marker at all.
    """
    if driver is None or element is None:
        return
    try:
        rect = driver.execute_script(_MAIN_PAGE_RECT_JS, element)
    except Exception as e:  # noqa: BLE001
        _log.debug("[bounds] main-page rect failed, falling back to element.rect: %s", e)
        try:
            rect = element.rect
        except Exception:  # noqa: BLE001
            return
    if rect:
        _emit_bounds(driver, rect)


def send_point_bounds(driver, x, y) -> None:
    """Report a coordinate click as a zero-size point rect (X-marker annotation).

    The coordinate tier has no DOM element to measure — it healed to a pixel —
    so the annotation is a point rather than a box.
    """
    if driver is None:
        return
    try:
        _emit_bounds(driver, {"x": int(x), "y": int(y), "width": 0, "height": 0})
    except Exception as e:  # noqa: BLE001
        _log.debug("[bounds] point emit skipped: %s", e)
