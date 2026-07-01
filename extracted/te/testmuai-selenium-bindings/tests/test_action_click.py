"""Tests for testmu_selenium.click — high-level click wrapper.

Strategy: stub _run_action at the wrapper-module path so we can assert the
runtime kwargs/spec the wrapper threads through, without exercising the
full engine again (engine itself is covered in test_action_engine.py).
"""
from unittest.mock import MagicMock, patch

from testmu_selenium import _action_click as ac
from testmu_selenium._action_click import (
    click, _CLICK_SPEC, _click_runner, _click_coord_runner,
)
from testmu_selenium._action_engine import _DEFAULT_RECOVERABLE


PRIMARY = [{"selector": "#login", "isXPath": False}]


def test_click_calls_run_action_with_click_spec():
    """click() routes through _run_action, passing _CLICK_SPEC."""
    driver = MagicMock(name="driver")
    with patch.object(ac, "_run_action", return_value=True) as m_run:
        result = click(driver, PRIMARY)

    assert result is True
    m_run.assert_called_once()
    args, _kw = m_run.call_args
    # positional: driver, spec, selector
    assert args[0] is driver
    assert args[1] is _CLICK_SPEC
    assert args[2] is PRIMARY


def test_click_threads_strategy_kwarg():
    driver = MagicMock(name="driver")
    with patch.object(ac, "_run_action", return_value=True) as m_run:
        click(driver, PRIMARY, strategy="js_se_ac")

    kw = m_run.call_args.kwargs
    assert kw["strategy"] == "js_se_ac"


def test_click_threads_modifiers_kwarg():
    driver = MagicMock(name="driver")
    with patch.object(ac, "_run_action", return_value=True) as m_run:
        click(driver, PRIMARY, modifiers=["Shift"])

    kw = m_run.call_args.kwargs
    assert kw["modifiers"] == ["Shift"]


def test_click_threads_autoheal_false():
    driver = MagicMock(name="driver")
    with patch.object(ac, "_run_action", return_value=True) as m_run:
        click(driver, PRIMARY, autoheal=False)

    kw = m_run.call_args.kwargs
    assert kw["autoheal"] is False


def test_click_threads_tiers_kwarg():
    driver = MagicMock(name="driver")
    custom_tiers = ["LIST_XPATHS"]
    with patch.object(ac, "_run_action", return_value=True) as m_run:
        click(driver, PRIMARY, tiers=custom_tiers)

    kw = m_run.call_args.kwargs
    assert kw["tiers"] == custom_tiers


def test_click_runner_invokes_clickElement_with_strategy_and_modifiers():
    """Spec runner calls element.clickElement(driver, strategy, modifiers)."""
    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    el.clickElement = MagicMock(return_value=True)

    ctx = {"driver": driver, "frame_info": None, "strategy": "ac_js_se", "modifiers": ["Control"]}
    out = _click_runner(el, ctx)

    assert out is True
    el.clickElement.assert_called_once_with(driver, "ac_js_se", ["Control"], None)


def test_click_spec_uses_default_recoverable():
    """_CLICK_SPEC must inherit the engine's _DEFAULT_RECOVERABLE so additions
    to the default set automatically propagate to click."""
    assert _CLICK_SPEC.recoverable_exceptions is _DEFAULT_RECOVERABLE


def test_click_runner_defaults_strategy_when_missing():
    """When ctx doesn't carry strategy/modifiers, runner uses defaults."""
    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    el.clickElement = MagicMock(return_value=True)

    _click_runner(el, {"driver": driver, "frame_info": None})

    el.clickElement.assert_called_once_with(driver, "se_js_ac", None, None)


# ---------------------------------------------------------------------------
# COORDINATE-tier dispatch
# ---------------------------------------------------------------------------

def test_click_spec_has_coord_runner():
    """_CLICK_SPEC must wire the coord_runner so the engine never falls back
    to feeding a synthetic 'coord:x,y' placeholder into findElement when the
    heal cascade resolves to viewport pixel coordinates."""
    assert _CLICK_SPEC.coord_runner is _click_coord_runner


def test_click_coord_runner_real_pointer_click():
    """coord_runner must REAL-click at the resolved viewport coords (ActionBuilder
    pointer move_to_location + click) — not elementFromPoint(x,y).click() (JS).

    The coord tier is only reached when heal returns coordinates, i.e. a
    canvas/no-DOM visual target. A JS el.click() synthesizes a MouseEvent with
    clientX/clientY = 0, so a canvas onclick that reads e.clientX grounds to the
    wrong spot; a real pointer click carries the true coords."""
    driver = MagicMock(name="driver")
    instances = []

    class CapturingAB:
        def __init__(self, _driver):
            self.pointer_action = MagicMock()
            self.key_action = MagicMock()
            self.perform = MagicMock()
            instances.append(self)

    with patch.object(ac, "ActionBuilder", side_effect=CapturingAB):
        out = _click_coord_runner(driver, 388, 202, {"driver": driver, "frame_info": None})

    assert out is True
    driver.execute_script.assert_not_called()
    assert len(instances) == 1
    instances[0].pointer_action.move_to_location.assert_called_once_with(388, 202)
    instances[0].pointer_action.click.assert_called_once()
    instances[0].perform.assert_called_once()


def test_click_coord_runner_does_not_consult_strategy_or_modifiers():
    """Coord-tier is the visual-location fallback after every selector tier
    missed; click strategy/modifiers from the original call site are not
    forwarded — only the pointer click at the resolved coords matters."""
    driver = MagicMock(name="driver")
    instances = []

    class CapturingAB:
        def __init__(self, _driver):
            self.pointer_action = MagicMock()
            self.key_action = MagicMock()
            self.perform = MagicMock()
            instances.append(self)

    with patch.object(ac, "ActionBuilder", side_effect=CapturingAB):
        _click_coord_runner(driver, 100, 50, {
            "driver": driver, "frame_info": None,
            "strategy": "ac_js_se", "modifiers": ["Shift", "Control"],
        })

    instances[0].pointer_action.move_to_location.assert_called_once_with(100, 50)
    instances[0].pointer_action.click.assert_called_once()


# ---------------------------------------------------------------------------
# click_modifier (V3 gestures) threading
# ---------------------------------------------------------------------------

def test_click_threads_click_modifier_kwarg():
    driver = MagicMock(name="driver")
    cm = {"kind": "right_click"}
    with patch.object(ac, "_run_action", return_value=True) as m_run:
        click(driver, PRIMARY, click_modifier=cm)
    assert m_run.call_args.kwargs["click_modifier"] == cm


def test_click_runner_forwards_click_modifier_to_clickElement():
    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    el.clickElement = MagicMock(return_value=True)
    ctx = {"driver": driver, "frame_info": None, "strategy": "ac_js_se",
           "modifiers": ["Control"], "click_modifier": {"kind": "right_click"}}
    _click_runner(el, ctx)
    el.clickElement.assert_called_once_with(
        driver, "ac_js_se", ["Control"], {"kind": "right_click"}
    )


def test_coord_runner_dispatches_gesture_when_click_modifier_present():
    driver = MagicMock(name="driver")
    with patch.object(ac, "do_gesture_at_coordinate", return_value=True) as m:
        out = _click_coord_runner(driver, 120, 240, {
            "driver": driver, "frame_info": None,
            "click_modifier": {"kind": "right_click"},
        })
    assert out is True
    # held-keys-coord (Task 32): the coord runner threads ctx['modifiers'] (None here)
    m.assert_called_once_with(driver, 120, 240, {"kind": "right_click"}, None)


def test_coord_runner_plain_click_when_no_click_modifier():
    """No click_modifier -> existing plain pointer click (no gesture dispatch)."""
    driver = MagicMock(name="driver")
    instances = []

    class CapturingAB:
        def __init__(self, _driver):
            self.pointer_action = MagicMock()
            self.key_action = MagicMock()
            self.perform = MagicMock()
            instances.append(self)

    with patch.object(ac, "ActionBuilder", side_effect=CapturingAB), \
         patch.object(ac, "do_gesture_at_coordinate") as m_gest:
        out = _click_coord_runner(driver, 10, 20, {"driver": driver, "frame_info": None})
    assert out is True
    m_gest.assert_not_called()
    instances[0].pointer_action.move_to_location.assert_called_once_with(10, 20)
    instances[0].pointer_action.click.assert_called_once()


def test_coord_runner_resolves_template_before_validation():
    """Export-path data-driven coord gesture (Task 25):
    resolve_click_modifier_variables runs BEFORE validate_click_modifier in
    _click_coord_runner, and the resolved dict reaches do_gesture_at_coordinate."""
    driver = MagicMock(name="driver")
    raw = {"kind": "multi_click", "frequency": 2,
           "variables": {"frequency": "{{MultiCount}}"}}
    resolved = {"kind": "multi_click", "frequency": 5}
    with patch.object(ac, "resolve_click_modifier_variables",
                      return_value=resolved) as m_resolve, \
         patch.object(ac, "validate_click_modifier",
                      return_value=resolved) as m_validate, \
         patch.object(ac, "do_gesture_at_coordinate", return_value=True) as m_gest:
        out = _click_coord_runner(driver, 120, 240, {
            "driver": driver, "frame_info": None, "click_modifier": raw,
        })
    assert out is True
    m_resolve.assert_called_once_with(raw)
    m_validate.assert_called_once_with(resolved)
    # held-keys-coord (Task 32): trailing modifiers arg (None — no ctx['modifiers'])
    m_gest.assert_called_once_with(driver, 120, 240, resolved, None)
