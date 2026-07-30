"""Tests for testmu_selenium._action_search — high-level search wrapper.

Strategy mirrors test_action_type: stub _run_action at the wrapper-module
path and assert kwarg threading + runner positional ordering.
SEARCH = TYPE value into element + press Enter.
"""
from unittest.mock import MagicMock, patch

import pytest

from testmu_selenium import _action_search as asearch
from testmu_selenium._action_search import (
    search, _SEARCH_SPEC, _search_runner, _search_coord_runner,
)
from testmu_selenium._action_engine import _DEFAULT_RECOVERABLE


PRIMARY = [{"selector": "input[name=q]", "isXPath": False}]


# ---------------------------------------------------------------------------
# Group A — kwarg threading
# ---------------------------------------------------------------------------

def test_search_calls_run_action_with_search_spec():
    driver = MagicMock(name="driver")
    with patch.object(asearch, "_run_action", return_value=None) as m_run:
        search(driver, PRIMARY, "audi q7")

    m_run.assert_called_once()
    args, _kw = m_run.call_args
    assert args[0] is driver
    assert args[1] is _SEARCH_SPEC
    assert args[2] is PRIMARY


def test_search_threads_value_strategy_timeout():
    driver = MagicMock(name="driver")
    with patch.object(asearch, "_run_action", return_value=None) as m_run:
        search(driver, PRIMARY, "tesla", strategy="ac_js_se", timeout=42)

    kw = m_run.call_args.kwargs
    assert kw["value"] == "tesla"
    assert kw["strategy"] == "ac_js_se"
    assert kw["timeout"] == 42


def test_search_threads_description_tiers_autoheal():
    driver = MagicMock(name="driver")
    with patch.object(asearch, "_run_action", return_value=None) as m_run:
        search(
            driver, PRIMARY, "v",
            description="search box",
            tiers=["LIST_XPATHS"],
            autoheal=False,
        )

    kw = m_run.call_args.kwargs
    assert kw["description"] == "search box"
    assert kw["tiers"] == ["LIST_XPATHS"]
    assert kw["autoheal"] is False


def test_search_threads_max_attempts_retry_delay():
    driver = MagicMock(name="driver")
    with patch.object(asearch, "_run_action", return_value=None) as m_run:
        search(driver, PRIMARY, "v", max_attempts=2, retry_delay=1.5)

    kw = m_run.call_args.kwargs
    assert kw["max_attempts"] == 2
    assert kw["retry_delay"] == 1.5


def test_search_default_kwargs_forwarded():
    driver = MagicMock(name="driver")
    with patch.object(asearch, "_run_action", return_value=None) as m_run:
        search(driver, PRIMARY, "default test")

    kw = m_run.call_args.kwargs
    assert kw["strategy"] == "se_js_ac"
    assert kw["timeout"] == 10
    assert kw["autoheal"] is True
    assert kw["max_attempts"] == 4
    assert kw["retry_delay"] == 0.5


# ---------------------------------------------------------------------------
# Group B — runner unit tests
# ---------------------------------------------------------------------------

def test_search_runner_calls_input_value_then_enter():
    """_search_runner must call element.input_value with fixed None/False/'' args
    then send Keys.ENTER via ActionChains."""
    from selenium.webdriver.common.keys import Keys

    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    el.input_value = MagicMock(return_value=None)

    ctx = {
        "driver": driver,
        "frame_info": None,
        "value": "bmw x5",
        "strategy": "se_js_ac",
        "timeout": 7,
    }

    with patch("testmu_selenium._action_search.ActionChains") as m_ac_cls:
        chain = MagicMock(name="chain")
        chain.send_keys.return_value = chain
        m_ac_cls.return_value = chain

        result = _search_runner(el, ctx)

    assert result is True
    el.input_value.assert_called_once_with(driver, "bmw x5", "se_js_ac", 7, None, False, '')
    m_ac_cls.assert_called_once_with(driver)
    chain.send_keys.assert_called_once_with(Keys.ENTER)
    chain.perform.assert_called_once()


def test_search_runner_defaults_when_ctx_missing_optional_keys():
    """strategy/timeout must default to 'se_js_ac'/10 when absent from ctx."""
    from selenium.webdriver.common.keys import Keys

    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    el.input_value = MagicMock(return_value=None)

    with patch("testmu_selenium._action_search.ActionChains") as m_ac_cls:
        chain = MagicMock()
        chain.send_keys.return_value = chain
        m_ac_cls.return_value = chain

        _search_runner(el, {"driver": driver, "frame_info": None, "value": "v"})

    el.input_value.assert_called_once_with(driver, "v", "se_js_ac", 10, None, False, '')


# ---------------------------------------------------------------------------
# Group C — spec recoverable
# ---------------------------------------------------------------------------

def test_search_spec_uses_default_recoverable():
    """_SEARCH_SPEC must inherit engine's _DEFAULT_RECOVERABLE."""
    assert _SEARCH_SPEC.recoverable_exceptions is _DEFAULT_RECOVERABLE


# ---------------------------------------------------------------------------
# Group D — spec coord_runner wired
# ---------------------------------------------------------------------------

def test_search_spec_has_coord_runner():
    """_SEARCH_SPEC must wire coord_runner to _search_coord_runner."""
    assert _SEARCH_SPEC.coord_runner is _search_coord_runner


# ---------------------------------------------------------------------------
# Group E — coord_runner unit tests
# ---------------------------------------------------------------------------

def test_search_coord_runner_real_click_then_value_and_enter():
    """coord_runner must REAL-click at the resolved coords (ActionBuilder pointer
    move + click) — not elementFromPoint().focus() — then send value + ENTER via
    the keyboard input source. A pure <canvas> isn't focusable; only a real click
    fires its handler so keystrokes land (same reasoning as _type_coord_runner)."""
    from selenium.webdriver.common.keys import Keys

    driver = MagicMock(name="driver")
    instances = []

    class CapturingAB:
        def __init__(self, _driver):
            self.pointer_action = MagicMock()
            self.key_action = MagicMock()
            self.perform = MagicMock()
            instances.append(self)

    with patch.object(asearch, "ActionBuilder", side_effect=CapturingAB):
        out = _search_coord_runner(
            driver, 388, 202,
            {"driver": driver, "frame_info": None, "value": "audi q7"},
        )

    assert out is True
    driver.execute_script.assert_not_called()
    instances[0].pointer_action.move_to_location.assert_called_once_with(388, 202)
    instances[0].pointer_action.click.assert_called_once()
    # value then ENTER delivered via key_action.send_keys (in order).
    sent = [
        c.args[0]
        for ab in instances
        for c in ab.key_action.send_keys.call_args_list
    ]
    assert sent == ["audi q7", Keys.ENTER]


def test_search_coord_runner_sends_enter_even_for_empty_value():
    """Enter must be sent even when value is empty string."""
    from selenium.webdriver.common.keys import Keys

    driver = MagicMock(name="driver")
    instances = []

    class CapturingAB:
        def __init__(self, _driver):
            self.pointer_action = MagicMock()
            self.key_action = MagicMock()
            self.perform = MagicMock()
            instances.append(self)

    with patch.object(asearch, "ActionBuilder", side_effect=CapturingAB):
        _search_coord_runner(
            driver, 100, 50,
            {"driver": driver, "frame_info": None, "value": ""},
        )

    sent = [
        c.args[0]
        for ab in instances
        for c in ab.key_action.send_keys.call_args_list
    ]
    assert sent == ["", Keys.ENTER]


# ---------------------------------------------------------------------------
# Group F — coord_runner value normalization
#
# _search_runner delivers the value through input_value(), which coerces
# scalars and rejects structural values. _search_coord_runner bypasses
# input_value entirely, so the same normalization has to be applied here or
# SEARCH behaves differently depending on which heal tier resolved it.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "value,expected",
    [(123, "123"), (3.5, "3.5"), (True, "True"), (False, "False")],
)
def test_search_coord_runner_coerces_scalar_value(value, expected):
    """A numeric/bool variable reaching the coord tier must be stringified
    before send_keys — bools use Python's str(True) == 'True', matching every
    sibling binding."""
    from selenium.webdriver.common.keys import Keys

    driver = MagicMock(name="driver")
    instances = []

    class CapturingAB:
        def __init__(self, _driver):
            self.pointer_action = MagicMock()
            self.key_action = MagicMock()
            self.perform = MagicMock()
            instances.append(self)

    with patch.object(asearch, "ActionBuilder", side_effect=CapturingAB):
        _search_coord_runner(
            driver, 10, 20,
            {"driver": driver, "frame_info": None, "value": value},
        )

    sent = [
        c.args[0]
        for ab in instances
        for c in ab.key_action.send_keys.call_args_list
    ]
    assert sent == [expected, Keys.ENTER]


@pytest.mark.parametrize("structural", [{"a": 1}, [1, 2]])
def test_search_coord_runner_rejects_structural_value(structural):
    """Same structural-value guard as input_value: a dict handed to send_keys
    would be iterated as its key names rather than failing loudly."""
    driver = MagicMock(name="driver")

    class CapturingAB:
        def __init__(self, _driver):
            self.pointer_action = MagicMock()
            self.key_action = MagicMock()
            self.perform = MagicMock()

    with patch.object(asearch, "ActionBuilder", side_effect=CapturingAB):
        with pytest.raises(TypeError, match="structural"):
            _search_coord_runner(
                driver, 10, 20,
                {"driver": driver, "frame_info": None, "value": structural},
            )
