"""Tests for testmu_selenium.clear — high-level clear wrapper.

Strategy: stub _run_action at the wrapper-module path so we can assert the
runtime kwargs/spec the wrapper threads through, without exercising the
full engine again (engine itself is covered in test_action_engine.py).

Groups:
  A — kwarg threading
  B — _clear_runner invokes element.clear()
  C — spec uses default recoverable exceptions
  D — coord_runner is wired on _CLEAR_SPEC
  E — _clear_coord_runner constructs 3 ActionBuilder instances in order
"""
from unittest.mock import MagicMock, call, patch

from selenium.common.exceptions import InvalidElementStateException
from selenium.webdriver.common.keys import Keys

from testmu_selenium import _action_clear as ac
from testmu_selenium._action_clear import (
    clear, _CLEAR_SPEC, _clear_runner, _clear_coord_runner,
)
from testmu_selenium._action_engine import _DEFAULT_RECOVERABLE


PRIMARY = [{"selector": "#email", "isXPath": False}]


# ---------------------------------------------------------------------------
# Group A — kwarg threading
# ---------------------------------------------------------------------------

def test_clear_calls_run_action_with_clear_spec():
    """clear() routes through _run_action, passing _CLEAR_SPEC."""
    driver = MagicMock(name="driver")
    with patch.object(ac, "_run_action", return_value=None) as m_run:
        result = clear(driver, PRIMARY)

    assert result is None
    m_run.assert_called_once()
    args, _kw = m_run.call_args
    assert args[0] is driver
    assert args[1] is _CLEAR_SPEC
    assert args[2] is PRIMARY


def test_clear_threads_description_kwarg():
    driver = MagicMock(name="driver")
    with patch.object(ac, "_run_action", return_value=None) as m_run:
        clear(driver, PRIMARY, description="email field")

    kw = m_run.call_args.kwargs
    assert kw["description"] == "email field"


def test_clear_threads_autoheal_false():
    driver = MagicMock(name="driver")
    with patch.object(ac, "_run_action", return_value=None) as m_run:
        clear(driver, PRIMARY, autoheal=False)

    kw = m_run.call_args.kwargs
    assert kw["autoheal"] is False


def test_clear_threads_tiers_kwarg():
    driver = MagicMock(name="driver")
    custom_tiers = ["LIST_XPATHS"]
    with patch.object(ac, "_run_action", return_value=None) as m_run:
        clear(driver, PRIMARY, tiers=custom_tiers)

    kw = m_run.call_args.kwargs
    assert kw["tiers"] == custom_tiers


# ---------------------------------------------------------------------------
# Group B — _clear_runner invokes element.clear()
# ---------------------------------------------------------------------------

def test_clear_runner_invokes_element_clear():
    """Spec runner calls element.clear() exactly once and returns None."""
    driver = MagicMock(name="driver")
    element = MagicMock(name="element")
    ctx = {"driver": driver, "frame_info": None}

    result = _clear_runner(element, ctx)

    element.clear.assert_called_once()
    assert result is None


# ---------------------------------------------------------------------------
# Group B2 — _clear_runner falls back to keystrokes on InvalidElementState
# ---------------------------------------------------------------------------

def test_clear_runner_falls_back_to_keystrokes_on_invalid_element_state():
    """When native element.clear() raises InvalidElementStateException (a
    masked/readonly input rejects the W3C reset), _clear_runner must NOT
    propagate — it focuses the element and clears via Ctrl+A + Delete
    keystrokes (the same sequence the coord path uses, which the browser
    routes to the focused element without the editability gate)."""
    driver = MagicMock(name="driver")
    element = MagicMock(name="element")
    element.clear.side_effect = InvalidElementStateException("invalid element state")
    ctx = {"driver": driver, "frame_info": None}

    instances = []

    class CapturingAB:
        def __init__(self, _driver):
            self.pointer_action = MagicMock()
            self.key_action = MagicMock()
            self.perform = MagicMock()
            instances.append(self)

    with patch.object(ac, "ActionBuilder", side_effect=CapturingAB):
        result = _clear_runner(element, ctx)  # must not raise

    # native clear was attempted first
    element.clear.assert_called_once()
    # element is focused before keystrokes are sent
    element.click.assert_called_once()
    # two ActionBuilders: select-all (Ctrl+A) then DELETE
    assert len(instances) == 2
    ab_select = instances[0]
    ab_select.key_action.key_down.assert_called_once_with(Keys.CONTROL)
    ab_select.key_action.send_keys.assert_called_once_with('a')
    ab_select.key_action.key_up.assert_called_once_with(Keys.CONTROL)
    ab_delete = instances[1]
    ab_delete.key_action.send_keys.assert_called_once_with(Keys.DELETE)
    assert result is None


# ---------------------------------------------------------------------------
# Group C — default recoverable
# ---------------------------------------------------------------------------

def test_clear_spec_uses_default_recoverable():
    """_CLEAR_SPEC must inherit the engine's _DEFAULT_RECOVERABLE."""
    assert _CLEAR_SPEC.recoverable_exceptions is _DEFAULT_RECOVERABLE


# ---------------------------------------------------------------------------
# Group D — coord_runner wired
# ---------------------------------------------------------------------------

def test_clear_spec_has_coord_runner():
    """_CLEAR_SPEC must wire the coord_runner so the engine dispatches
    via _clear_coord_runner when the heal cascade resolves to coordinates."""
    assert _CLEAR_SPEC.coord_runner is _clear_coord_runner


# ---------------------------------------------------------------------------
# Group E — _clear_coord_runner constructs 3 ActionBuilder instances in order
# ---------------------------------------------------------------------------

def test_clear_coord_runner_constructs_three_action_builders():
    """_clear_coord_runner must create exactly 3 separate ActionBuilder
    instances and call perform() on each one."""
    driver = MagicMock(name="driver")
    ctx = {"driver": driver, "frame_info": None}

    mock_ab = MagicMock(name="ActionBuilderInstance")
    with patch.object(ac, "ActionBuilder", return_value=mock_ab) as mock_cls:
        _clear_coord_runner(driver, 100, 200, ctx)

    assert mock_cls.call_count == 3
    # Each instance must have had perform() called exactly once
    assert mock_ab.perform.call_count == 3


def test_clear_coord_runner_perform_called_in_order():
    """Each ActionBuilder.perform() is called before the next builder is
    created — order: ab1.perform, ab2.perform, ab3.perform."""
    driver = MagicMock(name="driver")
    ctx = {"driver": driver, "frame_info": None}

    call_log = []

    class TrackingAB:
        def __init__(self, _driver):
            self.pointer_action = MagicMock()
            self.key_action = MagicMock()
            self._id = len(call_log)

        def perform(self):
            call_log.append(self._id)

    with patch.object(ac, "ActionBuilder", side_effect=TrackingAB):
        _clear_coord_runner(driver, 50, 75, ctx)

    assert call_log == [0, 1, 2], f"perform() order wrong: {call_log}"


def test_clear_coord_runner_ctrl_a_then_delete_sequence():
    """ab2 sends Ctrl+A; ab3 sends DELETE — verifies the key sequence."""
    driver = MagicMock(name="driver")
    ctx = {"driver": driver, "frame_info": None}

    instances = []

    class CapturingAB:
        def __init__(self, _driver):
            self.pointer_action = MagicMock()
            self.key_action = MagicMock()
            self.perform = MagicMock()
            instances.append(self)

    with patch.object(ac, "ActionBuilder", side_effect=CapturingAB):
        result = _clear_coord_runner(driver, 10, 20, ctx)

    assert len(instances) == 3

    # ab1: move_to_location(x, y) + click
    ab1 = instances[0]
    ab1.pointer_action.move_to_location.assert_called_once_with(10, 20)
    ab1.pointer_action.click.assert_called_once()

    # ab2: key_down(CONTROL) + send_keys('a') + key_up(CONTROL)
    ab2 = instances[1]
    ab2.key_action.key_down.assert_called_once_with(Keys.CONTROL)
    ab2.key_action.send_keys.assert_called_once_with('a')
    ab2.key_action.key_up.assert_called_once_with(Keys.CONTROL)

    # ab3: send_keys(DELETE)
    ab3 = instances[2]
    ab3.key_action.send_keys.assert_called_once_with(Keys.DELETE)

    assert result is True
