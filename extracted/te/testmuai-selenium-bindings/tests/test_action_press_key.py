"""Tests for testmu_selenium.press_key — high-level targeted key-press wrapper.

Strategy: stub _run_action at the wrapper-module path so we can assert the
runtime kwargs/spec the wrapper threads through, without exercising the
full engine again (engine itself is covered in test_action_engine.py).

Groups:
  A — kwarg threading (selector, description, key, autoheal, tiers, search_root)
  B — _press_key_runner invokes element.send_keys(key from ctx)
  C — spec uses default recoverable exceptions; has coord_runner wired
  D — coord_runner bridges a DESKTOP_LOCATE-healed pixel to the element:
      move_to_location(x,y) + click to focus, then send the key via ActionBuilder
"""
import pytest
from unittest.mock import MagicMock, patch, call

from testmu_selenium import _action_press_key as pk
from testmu_selenium._action_press_key import (
    press_key, _PRESS_KEY_SPEC, _press_key_runner, _press_key_coord_runner,
)
from testmu_selenium._action_engine import _DEFAULT_RECOVERABLE


PRIMARY = [{"selector": "#search-box", "isXPath": False}]


# ---------------------------------------------------------------------------
# Group A — kwarg threading
# ---------------------------------------------------------------------------

def test_press_key_calls_run_action_with_spec():
    """press_key() routes through _run_action, passing the spec + selector."""
    driver = MagicMock(name="driver")
    with patch.object(pk, "_run_action", return_value=None) as m_run:
        result = press_key(driver, PRIMARY, "Enter")

    assert result is None
    m_run.assert_called_once()
    args, _kw = m_run.call_args
    assert args[0] is driver
    assert args[1] is _PRESS_KEY_SPEC
    assert args[2] is PRIMARY


def test_press_key_threads_key_as_runner_kwarg():
    """key must reach the runner via runner_kwargs (engine forwards to ctx)."""
    driver = MagicMock(name="driver")
    with patch.object(pk, "_run_action", return_value=None) as m_run:
        press_key(driver, PRIMARY, "Tab")

    kw = m_run.call_args.kwargs
    assert kw["key"] == "Tab"


def test_press_key_threads_description_kwarg():
    driver = MagicMock(name="driver")
    with patch.object(pk, "_run_action", return_value=None) as m_run:
        press_key(driver, PRIMARY, "Enter", description="submit form")

    kw = m_run.call_args.kwargs
    assert kw["description"] == "submit form"


def test_press_key_threads_autoheal_false():
    driver = MagicMock(name="driver")
    with patch.object(pk, "_run_action", return_value=None) as m_run:
        press_key(driver, PRIMARY, "Escape", autoheal=False)

    kw = m_run.call_args.kwargs
    assert kw["autoheal"] is False


def test_press_key_threads_tiers_kwarg():
    driver = MagicMock(name="driver")
    custom_tiers = ["LIST_XPATHS"]
    with patch.object(pk, "_run_action", return_value=None) as m_run:
        press_key(driver, PRIMARY, "Enter", tiers=custom_tiers)

    kw = m_run.call_args.kwargs
    assert kw["tiers"] == custom_tiers


def test_press_key_default_tiers_is_none():
    """Default tiers=None defers to the engine's _DEFAULT_HEAL_TIERS.
    press_key has no reason to override; passing None lets the engine choose."""
    driver = MagicMock(name="driver")
    with patch.object(pk, "_run_action", return_value=None) as m_run:
        press_key(driver, PRIMARY, "Enter")  # no tiers passed

    kw = m_run.call_args.kwargs
    assert kw["tiers"] is None


def test_press_key_threads_search_root():
    driver = MagicMock(name="driver")
    root = MagicMock(name="shadow_root")
    with patch.object(pk, "_run_action", return_value=None) as m_run:
        press_key(driver, PRIMARY, "Enter", search_root=root)

    kw = m_run.call_args.kwargs
    assert kw["search_root"] is root


def test_press_key_threads_max_attempts_and_retry_delay():
    driver = MagicMock(name="driver")
    with patch.object(pk, "_run_action", return_value=None) as m_run:
        press_key(driver, PRIMARY, "Enter", max_attempts=2, retry_delay=0.1)

    kw = m_run.call_args.kwargs
    assert kw["max_attempts"] == 2
    assert kw["retry_delay"] == 0.1


def test_press_key_threads_fallback_coordinates():
    driver = MagicMock(name="driver")
    with patch.object(pk, "_run_action", return_value=None) as m_run:
        press_key(driver, PRIMARY, "Enter", fallback_coordinates=(50, 100))

    kw = m_run.call_args.kwargs
    assert kw["fallback_coordinates"] == (50, 100)


# ---------------------------------------------------------------------------
# Group B — _press_key_runner invokes element.send_keys(key)
# ---------------------------------------------------------------------------

def test_runner_sends_key_to_element():
    """Runner reads key from ctx and calls element.send_keys(key)."""
    element = MagicMock(name="element")
    ctx = {"driver": MagicMock(), "frame_info": None, "key": ""}  # Keys.RETURN

    result = _press_key_runner(element, ctx)

    element.send_keys.assert_called_once_with("")
    assert result is None


def test_runner_sends_arbitrary_key_string():
    """Runner works for any key string, not just special Keys constants."""
    element = MagicMock(name="element")
    ctx = {"driver": MagicMock(), "frame_info": None, "key": "a"}

    _press_key_runner(element, ctx)

    element.send_keys.assert_called_once_with("a")


# ---------------------------------------------------------------------------
# Group C — spec shape
# ---------------------------------------------------------------------------

def test_spec_uses_default_recoverable():
    assert _PRESS_KEY_SPEC.recoverable_exceptions is _DEFAULT_RECOVERABLE


def test_spec_has_coord_runner():
    """DESKTOP_LOCATE is a usable tier for press_key; the spec wires the
    coord_runner so the engine can dispatch to it when heal resolves coordinates."""
    assert _PRESS_KEY_SPEC.coord_runner is _press_key_coord_runner


# ---------------------------------------------------------------------------
# Group D — coord_runner: move+click to focus, then send key via ActionBuilder
# ---------------------------------------------------------------------------

def test_coord_runner_moves_and_clicks_then_sends_key():
    """coord_runner must first focus the element at (x, y) via a real pointer
    click (not elementFromPoint — mirrors _type_coord_runner and _clear_coord_runner),
    then deliver the key via the keyboard input source."""
    driver = MagicMock(name="driver")
    ctx = {"driver": driver, "frame_info": None, "key": ""}

    result = _press_key_coord_runner(driver, 100, 200, ctx)

    # Two ActionBuilder.perform() calls expected: one for pointer click, one for key
    assert driver.mock_calls, "driver must be used (ActionBuilder calls)"
    # Return is truthy (mirrors _type_coord_runner / _clear_coord_runner convention)
    assert result is True


def test_coord_runner_uses_move_to_location():
    """Verify the coord_runner builds the pointer action with the exact (x, y)
    from the heal result — it must not clip or offset the coordinates."""
    from selenium.webdriver.common.actions.action_builder import ActionBuilder

    driver = MagicMock(name="driver")
    ctx = {"driver": driver, "frame_info": None, "key": "Tab"}

    with patch(
        "testmu_selenium._action_press_key.ActionBuilder"
    ) as MockAB:
        mock_ab1 = MagicMock(name="ab1")
        mock_ab2 = MagicMock(name="ab2")
        MockAB.side_effect = [mock_ab1, mock_ab2]

        _press_key_coord_runner(driver, 42, 77, ctx)

    # First builder: pointer move + click
    mock_ab1.pointer_action.move_to_location.assert_called_once_with(42, 77)
    mock_ab1.pointer_action.click.assert_called_once()
    mock_ab1.perform.assert_called_once()

    # Second builder: key send
    mock_ab2.key_action.send_keys.assert_called_once_with("Tab")
    mock_ab2.perform.assert_called_once()


def test_coord_runner_key_is_taken_from_ctx():
    """The coord_runner reads key from ctx, not a closure — whatever key the
    engine forwards must be the one delivered to the keyboard source."""
    from selenium.webdriver.common.actions.action_builder import ActionBuilder

    driver = MagicMock(name="driver")
    ctx = {"driver": driver, "frame_info": None, "key": ""}  # Keys.SPACE

    with patch(
        "testmu_selenium._action_press_key.ActionBuilder"
    ) as MockAB:
        mock_ab1 = MagicMock(name="ab1")
        mock_ab2 = MagicMock(name="ab2")
        MockAB.side_effect = [mock_ab1, mock_ab2]

        _press_key_coord_runner(driver, 0, 0, ctx)

    mock_ab2.key_action.send_keys.assert_called_once_with("")


# ---------------------------------------------------------------------------
# Regression: global (no-selector) path is NOT broken
# (Kept as a documentation/contract test — press_key always has a selector per
# the spec, but the binding function accepts any selector, including the empty
# list that means "selectorless" in the codegen convention.  The wrapper must
# NOT add selectorless special-casing — it delegates to _run_action verbatim.)
# ---------------------------------------------------------------------------

def test_nonempty_selector_routes_through_run_action():
    """A standard selector takes the find+heal path unchanged."""
    driver = MagicMock(name="driver")
    with patch.object(pk, "_run_action", return_value=None) as m_run:
        press_key(driver, PRIMARY, "Enter")

    m_run.assert_called_once()
    args, _ = m_run.call_args
    assert args[2] is PRIMARY


def test_press_key_exported_from_package():
    """testmu_selenium.press_key must be importable at the package level."""
    import testmu_selenium
    assert callable(testmu_selenium.press_key)
