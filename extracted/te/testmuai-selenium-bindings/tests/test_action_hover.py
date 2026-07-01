"""Tests for testmu_selenium.hover — high-level hover wrapper.

Strategy: stub _run_action at the wrapper-module path so we can assert the
runtime kwargs/spec the wrapper threads through, without exercising the
full engine again (engine itself is covered in test_action_engine.py).
"""
from unittest.mock import MagicMock, patch, call

from testmu_selenium import _action_hover as ah
from testmu_selenium._action_hover import (
    hover, _HOVER_SPEC, _hover_runner, _hover_coord_runner,
)
from testmu_selenium._action_engine import _DEFAULT_RECOVERABLE


PRIMARY = [{"selector": "#nav-item", "isXPath": False}]


# ---------------------------------------------------------------------------
# Group A — kwarg threading via patched _run_action
# ---------------------------------------------------------------------------

def test_hover_calls_run_action_with_hover_spec():
    """hover() routes through _run_action, passing _HOVER_SPEC."""
    driver = MagicMock(name="driver")
    with patch.object(ah, "_run_action", return_value=True) as m_run:
        result = hover(driver, PRIMARY)

    assert result is True
    m_run.assert_called_once()
    args, _kw = m_run.call_args
    assert args[0] is driver
    assert args[1] is _HOVER_SPEC
    assert args[2] is PRIMARY


def test_hover_threads_autoheal_false():
    driver = MagicMock(name="driver")
    with patch.object(ah, "_run_action", return_value=True) as m_run:
        hover(driver, PRIMARY, autoheal=False)

    kw = m_run.call_args.kwargs
    assert kw["autoheal"] is False


def test_hover_threads_tiers_kwarg():
    driver = MagicMock(name="driver")
    custom_tiers = ["LIST_XPATHS", "TEXTUAL_QUERY"]
    with patch.object(ah, "_run_action", return_value=True) as m_run:
        hover(driver, PRIMARY, tiers=custom_tiers)

    kw = m_run.call_args.kwargs
    assert kw["tiers"] == custom_tiers


def test_hover_threads_retry_params():
    driver = MagicMock(name="driver")
    with patch.object(ah, "_run_action", return_value=True) as m_run:
        hover(driver, PRIMARY, max_attempts=7, retry_delay=1.5)

    kw = m_run.call_args.kwargs
    assert kw["max_attempts"] == 7
    assert kw["retry_delay"] == 1.5


# ---------------------------------------------------------------------------
# Group B — _hover_runner invokes ActionChains.move_to_element(...).perform()
# ---------------------------------------------------------------------------

def test_hover_runner_invokes_action_chains_move_to_element():
    """_hover_runner must call ActionChains(driver).move_to_element(el).perform()."""
    driver = MagicMock(name="driver")
    element = MagicMock(name="element")

    chain_instance = MagicMock(name="chain")
    chain_instance.move_to_element.return_value = chain_instance

    with patch.object(ah, "ActionChains", return_value=chain_instance) as m_ac:
        out = _hover_runner(element, {"driver": driver, "frame_info": None})

    assert out is True
    m_ac.assert_called_once_with(driver)
    chain_instance.move_to_element.assert_called_once_with(element)
    chain_instance.perform.assert_called_once()


# ---------------------------------------------------------------------------
# Group C — _HOVER_SPEC inherits _DEFAULT_RECOVERABLE
# ---------------------------------------------------------------------------

def test_hover_spec_uses_default_recoverable():
    """_HOVER_SPEC must inherit the engine's _DEFAULT_RECOVERABLE so additions
    to the default set automatically propagate to hover."""
    assert _HOVER_SPEC.recoverable_exceptions is _DEFAULT_RECOVERABLE


# ---------------------------------------------------------------------------
# Group D — _HOVER_SPEC wires coord_runner
# ---------------------------------------------------------------------------

def test_hover_spec_has_coord_runner():
    """_HOVER_SPEC must wire the coord_runner so the engine dispatches
    ActionBuilder pixel-coords when the heal cascade resolves to coordinates."""
    assert _HOVER_SPEC.coord_runner is _hover_coord_runner


# ---------------------------------------------------------------------------
# Group E — _hover_coord_runner uses ActionBuilder.move_to_location + perform
# ---------------------------------------------------------------------------

def test_hover_coord_runner_constructs_action_builder_and_moves():
    """_hover_coord_runner must build an ActionBuilder, call
    pointer_action.move_to_location(x, y), then perform()."""
    driver = MagicMock(name="driver")

    ab_instance = MagicMock(name="ab")
    with patch.object(ah, "ActionBuilder", return_value=ab_instance) as m_ab:
        out = _hover_coord_runner(driver, 320, 240, {"driver": driver, "frame_info": None})

    assert out is True
    m_ab.assert_called_once_with(driver)
    ab_instance.pointer_action.move_to_location.assert_called_once_with(320, 240)
    ab_instance.perform.assert_called_once()


def test_hover_coord_runner_passes_correct_coordinates():
    """Coordinates passed to _hover_coord_runner flow through to move_to_location."""
    driver = MagicMock(name="driver")

    ab_instance = MagicMock(name="ab")
    with patch.object(ah, "ActionBuilder", return_value=ab_instance):
        _hover_coord_runner(driver, 42, 99, {"driver": driver, "frame_info": None})

    ab_instance.pointer_action.move_to_location.assert_called_once_with(42, 99)
