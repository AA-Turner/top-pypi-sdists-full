"""Tests for testmu_selenium.type — high-level type wrapper.

Strategy mirrors test_action_click: stub _run_action at the wrapper-module
path and assert kwarg threading + runner positional ordering.
"""
from unittest.mock import MagicMock, patch

import pytest

from testmu_selenium import _action_type as at
from testmu_selenium._action_type import (
    type as type_fn, _TYPE_SPEC, _type_runner, _type_coord_runner,
)
from testmu_selenium._action_engine import _DEFAULT_RECOVERABLE


PRIMARY = [{"selector": "input[name=email]", "isXPath": False}]


def test_type_calls_run_action_with_type_spec():
    driver = MagicMock(name="driver")
    with patch.object(at, "_run_action", return_value=None) as m_run:
        type_fn(driver, PRIMARY, "user@example.com")

    m_run.assert_called_once()
    args, _kw = m_run.call_args
    assert args[0] is driver
    assert args[1] is _TYPE_SPEC
    assert args[2] is PRIMARY


def test_type_threads_value_strategy_timeout():
    driver = MagicMock(name="driver")
    with patch.object(at, "_run_action", return_value=None) as m_run:
        type_fn(driver, PRIMARY, "hello", strategy="ac_js_se", timeout=42)

    kw = m_run.call_args.kwargs
    assert kw["value"] == "hello"
    assert kw["strategy"] == "ac_js_se"
    assert kw["timeout"] == 42


def test_type_threads_coords_multiple_inputs_manual_tag():
    driver = MagicMock(name="driver")
    with patch.object(at, "_run_action", return_value=None) as m_run:
        type_fn(
            driver, PRIMARY, "v",
            coords=(120, 240),
            multiple_inputs=True,
            manual_interaction_tag="date-tag",
        )

    kw = m_run.call_args.kwargs
    assert kw["coords"] == (120, 240)
    assert kw["multiple_inputs"] is True
    assert kw["manual_interaction_tag"] == "date-tag"


def test_type_threads_tiers_autoheal_max_attempts():
    driver = MagicMock(name="driver")
    with patch.object(at, "_run_action", return_value=None) as m_run:
        type_fn(
            driver, PRIMARY, "v",
            tiers=["LIST_XPATHS"],
            autoheal=False,
            max_attempts=2,
        )

    kw = m_run.call_args.kwargs
    assert kw["tiers"] == ["LIST_XPATHS"]
    assert kw["autoheal"] is False
    assert kw["max_attempts"] == 2


def test_type_runner_invokes_input_value_with_full_arg_order():
    """Spec runner calls element.input_value with the V2-parity positional order
    (driver, value, order, timeout, coords, multiple_inputs, manual_interaction_tag)."""
    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    el.input_value = MagicMock(return_value=None)

    ctx = {
        "driver": driver,
        "frame_info": None,
        "value": "v",
        "strategy": "se_js_ac",
        "timeout": 7,
        "coords": (1, 2),
        "multiple_inputs": True,
        "manual_interaction_tag": "tag",
    }
    _type_runner(el, ctx)

    el.input_value.assert_called_once_with(
        driver, "v", "se_js_ac", 7, (1, 2), True, "tag",
    )


def test_type_spec_uses_default_recoverable():
    """_TYPE_SPEC must inherit the engine's _DEFAULT_RECOVERABLE so additions
    to the default set automatically propagate to type."""
    assert _TYPE_SPEC.recoverable_exceptions is _DEFAULT_RECOVERABLE


def test_type_runner_defaults_when_ctx_missing_optional_keys():
    """Defaults match input_value() signature defaults."""
    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    el.input_value = MagicMock(return_value=None)

    _type_runner(el, {"driver": driver, "frame_info": None, "value": "v"})

    el.input_value.assert_called_once_with(driver, "v", "se_js_ac", 10, None, False, "")


# ---------------------------------------------------------------------------
# COORDINATE-tier dispatch (mirrors CLICK's coord_runner)
#
# Pre-0.1.4: TYPE crashed with NotImplementedError
# ("spec has no coord_runner") whenever the heal cascade fell back to the
# COORDINATE tier — _TYPE_SPEC was missing coord_runner. Same class of issue
# the CLICK fix in 0.1.3 closed.
# ---------------------------------------------------------------------------

def test_type_spec_has_coord_runner():
    """_TYPE_SPEC must wire coord_runner. Without it, COORDINATE-tier heal
    raises NotImplementedError instead of typing into the resolved element."""
    assert _TYPE_SPEC.coord_runner is _type_coord_runner


def test_type_coord_runner_real_click_then_sends_keys():
    """coord_runner must perform a REAL pointer click at the resolved viewport
    coordinates (ActionBuilder.pointer_action.move_to_location + click), then
    deliver the value via ActionBuilder.key_action — NOT elementFromPoint().focus().

    A pure <canvas> has no focusable DOM node: el.focus() is a no-op and the
    canvas' own click handler never fires, so its internal focus/active state is
    never set and keystrokes are silently dropped. A real pointer click fires the
    handler, exactly as the V2 visual-fallback path and _clear_coord_runner do."""
    driver = MagicMock(name="driver")
    instances = []

    class CapturingAB:
        def __init__(self, _driver):
            self.pointer_action = MagicMock()
            self.key_action = MagicMock()
            self.perform = MagicMock()
            instances.append(self)

    with patch.object(at, "ActionBuilder", side_effect=CapturingAB):
        out = _type_coord_runner(
            driver, 388, 202,
            {"driver": driver, "frame_info": None, "value": "audi q7"},
        )

    assert out is True
    # No JS focus shim — the canvas-broken path must be gone.
    driver.execute_script.assert_not_called()
    # First builder: real pointer click at the coords.
    assert len(instances) >= 2, "expected a click builder and a key builder"
    click_ab = instances[0]
    click_ab.pointer_action.move_to_location.assert_called_once_with(388, 202)
    click_ab.pointer_action.click.assert_called_once()
    # A later builder delivers the value via the keyboard input source.
    assert any(
        ab.key_action.send_keys.call_args is not None
        and ab.key_action.send_keys.call_args.args == ("audi q7",)
        for ab in instances
    ), "value must be typed via ActionBuilder.key_action.send_keys"
    # Every builder is performed.
    for ab in instances:
        ab.perform.assert_called_once()


def test_type_coord_runner_coerces_int_value_to_string():
    """A numeric variable reaching the coord-tier fallback must be coerced to a
    string before key_action.send_keys — send_keys iterates chars and an int
    would crash on a real driver."""
    driver = MagicMock(name="driver")
    instances = []

    class CapturingAB:
        def __init__(self, _driver):
            self.pointer_action = MagicMock()
            self.key_action = MagicMock()
            self.perform = MagicMock()
            instances.append(self)

    with patch.object(at, "ActionBuilder", side_effect=CapturingAB):
        _type_coord_runner(
            driver, 10, 20,
            {"driver": driver, "frame_info": None, "value": 123},
        )

    assert any(
        ab.key_action.send_keys.call_args is not None
        and ab.key_action.send_keys.call_args.args == ("123",)
        for ab in instances
    ), "int value must be coerced to '123' before send_keys"


def test_type_coord_runner_coerces_bool_value_to_python_str():
    """bool must reach send_keys as Python's str(True) == 'True' — the format
    every sibling binding emits (playwright-python _coerce_text, csharp
    ActionEngine, java VarStore all produce 'True'/'False')."""
    driver = MagicMock(name="driver")
    instances = []

    class CapturingAB:
        def __init__(self, _driver):
            self.pointer_action = MagicMock()
            self.key_action = MagicMock()
            self.perform = MagicMock()
            instances.append(self)

    with patch.object(at, "ActionBuilder", side_effect=CapturingAB):
        _type_coord_runner(
            driver, 10, 20,
            {"driver": driver, "frame_info": None, "value": True},
        )

    assert any(
        ab.key_action.send_keys.call_args is not None
        and ab.key_action.send_keys.call_args.args == ("True",)
        for ab in instances
    ), "bool must be coerced to 'True' before send_keys"


@pytest.mark.parametrize("structural", [{"a": 1}, [1, 2]])
def test_type_coord_runner_rejects_structural_value(structural):
    """The coord fallback must enforce the SAME structural-value guard as
    input_value. Without it, send_keys silently iterates a dict (typing its
    KEY NAMES) or a list, so an un-stringified API variable produced garbage
    input on the coord tier while failing loudly on the selector tier."""
    driver = MagicMock(name="driver")

    class CapturingAB:
        def __init__(self, _driver):
            self.pointer_action = MagicMock()
            self.key_action = MagicMock()
            self.perform = MagicMock()

    with patch.object(at, "ActionBuilder", side_effect=CapturingAB):
        with pytest.raises(TypeError, match="structural"):
            _type_coord_runner(
                driver, 10, 20,
                {"driver": driver, "frame_info": None, "value": structural},
            )


def test_type_coord_runner_still_clicks_with_empty_value():
    """Empty value still performs the real click (focus primitive) and a no-op
    keyboard send — preserves TYPE-with-empty-value as a focus primitive."""
    driver = MagicMock(name="driver")
    instances = []

    class CapturingAB:
        def __init__(self, _driver):
            self.pointer_action = MagicMock()
            self.key_action = MagicMock()
            self.perform = MagicMock()
            instances.append(self)

    with patch.object(at, "ActionBuilder", side_effect=CapturingAB):
        _type_coord_runner(
            driver, 100, 50,
            {"driver": driver, "frame_info": None, "value": ""},
        )

    instances[0].pointer_action.move_to_location.assert_called_once_with(100, 50)
    instances[0].pointer_action.click.assert_called_once()
    assert any(
        ab.key_action.send_keys.call_args is not None
        and ab.key_action.send_keys.call_args.args == ("",)
        for ab in instances
    )
