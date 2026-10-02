"""click — tap an element, optionally with a long-press or multi-click modifier."""
from testmu_appium._action_engine import _ActionSpec, _run_action
from testmu_appium._helpers.gesture import (
    apply_click_modifier, apply_click_modifier_at, click_target, tap,
)
from testmu_appium._timing import action_phase as _action_phase, count as _timing_count


def _runner(element, ctx):
    _timing_count("click_commands")
    with _action_phase("click"):
        element = click_target(ctx["driver"], element)
        if apply_click_modifier(ctx["driver"], element, ctx.get("click_modifier")):
            return True
        element.click()
    return True


def _coord_runner(driver, x, y, ctx):
    """Run a click at a point while preserving its recorded modifier."""
    _timing_count("click_commands")
    with _action_phase("click"):
        if apply_click_modifier_at(driver, x, y, ctx.get("click_modifier")):
            return True
        tap(driver, x, y)
    return True


_CLICK_SPEC = _ActionSpec(
    runner=_runner, target_mode="element", op_type="click",
    coord_runner=_coord_runner, vision_runner=_coord_runner,
)


def click(driver, *, selectors, description: str = "",
          fallback_coordinates: dict | None = None, click_modifier: dict | None = None,
          surface: str = "native", frame_path: str = "", grounded_by: str = ""):
    """Tap the element the recorded selectors identify.

    click_modifier: the recorded gesture dict, in either producer's spelling —
    {"gesture": "long_press", "duration_ms": ms} / {"gesture": "multi_click",
    "count"|"frequency": n, "gap_ms": ms} from the mobile recorder, or the legacy web
    {"kind": ..., "duration": <seconds>, "gap": <seconds>}. Its `{{var}}` tokens
    resolve at execution time.

    surface / frame_path: which reader found this element. "native" is the
    accessibility tree, "web" the DOM of a page read over the device's debug
    channel; both act through Appium. frame_path names the frame a web element was
    recorded in, and separates matches that are the same selector in two frames.

    fallback_coordinates: the recorded coordinate basis
    ({"x_ratio", "y_ratio", "orientation", "window"}). Used only after an
    authoritative heal miss, and only when the live orientation matches.
    """
    return _run_action(
        driver, _CLICK_SPEC, selectors,
        description=description,
        fallback_coordinates=fallback_coordinates,
        surface=surface,
        frame_path=frame_path,
        grounded_by=grounded_by,
        click_modifier=click_modifier,
    )
