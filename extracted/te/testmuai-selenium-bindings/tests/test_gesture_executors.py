"""Tests for element-path gesture executors (ActionChains patterns) + dispatch."""
from unittest.mock import MagicMock, patch

from selenium.webdriver.common.keys import Keys

from testmu_selenium._helpers import gesture
from testmu_selenium._helpers.gesture import (
    do_long_press, do_multi_click, do_right_click, dispatch_gesture,
)


def _chainable():
    """A chainable ActionChains mock: every builder method returns the same mock."""
    chain = MagicMock(name="chain")
    for m in ("click_and_hold", "pause", "release", "double_click",
              "click", "context_click", "key_down", "key_up"):
        getattr(chain, m).return_value = chain
    return chain


def test_long_press_holds_with_buffer():
    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    chain = _chainable()
    with patch.object(gesture, "ActionChains", return_value=chain) as m_ac:
        assert do_long_press(el, driver, 2.0) is True
    m_ac.assert_called_once_with(driver)
    chain.click_and_hold.assert_called_once_with(el)
    chain.pause.assert_called_once_with(2.1)   # 2.0 + 0.1 buffer
    chain.release.assert_called_once_with(el)
    chain.perform.assert_called_once()


def test_multi_click_two_uses_double_click():
    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    chain = _chainable()
    with patch.object(gesture, "ActionChains", return_value=chain) as m_ac:
        assert do_multi_click(el, driver, 2, 0.1) is True
    m_ac.assert_called_once_with(driver)
    chain.double_click.assert_called_once_with(el)
    chain.perform.assert_called_once()


def test_multi_click_five_loops_with_gap():
    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    chain = _chainable()
    with patch.object(gesture, "ActionChains", return_value=chain) as m_ac, \
         patch.object(gesture.time, "sleep") as m_sleep:
        assert do_multi_click(el, driver, 5, 0.1) is True
    assert m_ac.call_count == 5
    assert chain.click.call_count == 5
    assert chain.perform.call_count == 5
    chain.double_click.assert_not_called()
    assert m_sleep.call_count == 4            # gap between, not after last
    m_sleep.assert_called_with(0.1)


def test_right_click_holds_modifiers():
    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    chain = _chainable()
    with patch.object(gesture, "ActionChains", return_value=chain):
        assert do_right_click(el, driver, ["Control"]) is True
    chain.key_down.assert_called_once_with(Keys.CONTROL)
    chain.context_click.assert_called_once_with(el)
    chain.key_up.assert_called_once_with(Keys.CONTROL)
    chain.perform.assert_called_once()


def test_right_click_without_modifiers_no_key_hold():
    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    chain = _chainable()
    with patch.object(gesture, "ActionChains", return_value=chain):
        assert do_right_click(el, driver, None) is True
    chain.key_down.assert_not_called()
    chain.context_click.assert_called_once_with(el)
    chain.perform.assert_called_once()


def test_dispatch_routes_right_click_with_modifiers():
    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    with patch.object(gesture, "do_right_click", return_value=True) as m:
        dispatch_gesture(el, driver, {"kind": "right_click"}, ["Control"])
    m.assert_called_once_with(el, driver, ["Control"])


def test_dispatch_routes_long_press():
    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    with patch.object(gesture, "do_long_press", return_value=True) as m:
        dispatch_gesture(el, driver, {"kind": "long_press", "duration": 2.0}, None)
    m.assert_called_once_with(el, driver, 2.0, None)


def test_dispatch_routes_multi_click_with_gap_default():
    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    with patch.object(gesture, "do_multi_click", return_value=True) as m:
        dispatch_gesture(el, driver, {"kind": "multi_click", "frequency": 5}, None)
    m.assert_called_once_with(el, driver, 5, 0.1, None)
