"""Tests for clickElement click_modifier dispatch (gesture routing + collapse)."""
import inspect
from unittest.mock import MagicMock, patch

from testmu_selenium._helpers import gesture
from testmu_selenium._helpers.click import clickElement, add_clickElement_to_webelement


def test_right_click_modifier_routes_to_dispatch_gesture_with_held_keys():
    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    with patch.object(gesture, "dispatch_gesture", return_value=True) as m:
        out = clickElement(el, driver, "se_js_ac",
                           modifiers=["Control"], click_modifier={"kind": "right_click"})
    assert out is True
    m.assert_called_once_with(el, driver, {"kind": "right_click"}, ["Control"])


def test_long_press_modifier_routes_to_dispatch_gesture():
    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    with patch.object(gesture, "dispatch_gesture", return_value=True) as m:
        clickElement(el, driver, "se_js_ac",
                     click_modifier={"kind": "long_press", "duration": 2.0})
    m.assert_called_once_with(el, driver, {"kind": "long_press", "duration": 2.0}, None)


def test_frequency_one_collapses_to_plain_cascade():
    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    with patch.object(gesture, "dispatch_gesture", return_value=True) as m_disp, \
         patch("testmu_selenium._helpers.click._selenium_click", return_value=True) as m_se:
        out = clickElement(el, driver, "se_js_ac",
                           click_modifier={"kind": "multi_click", "frequency": 1})
    assert out is True
    m_disp.assert_not_called()        # collapsed -> no gesture
    m_se.assert_called_once()         # fell through to plain cascade


def test_click_modifier_takes_precedence_over_modifiers():
    # right_click + Control must run the GESTURE (which holds Control internally),
    # NOT the plain _modifier_click path.
    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    with patch.object(gesture, "dispatch_gesture", return_value=True) as m_disp, \
         patch("testmu_selenium._helpers.click._modifier_click", return_value=True) as m_mod:
        clickElement(el, driver, "se_js_ac",
                     modifiers=["Control"], click_modifier={"kind": "right_click"})
    m_disp.assert_called_once()
    m_mod.assert_not_called()


def test_monkeypatch_closure_accepts_click_modifier():
    from selenium.webdriver.remote.webelement import WebElement
    if hasattr(WebElement, "clickElement"):
        delattr(WebElement, "clickElement")
    add_clickElement_to_webelement()
    params = inspect.signature(WebElement.clickElement).parameters
    assert "click_modifier" in params


def test_templated_gesture_resolved_before_validation():
    """Export-path data-driven gesture (Task 25): the {{var}} carrier is resolved
    BEFORE validate_click_modifier sees the dict, and the RESOLVED dict is what
    reaches dispatch_gesture. The lazy import binds the patched names at call
    time, so patch.object on the gesture module takes effect."""
    driver = MagicMock(name="driver")
    el = MagicMock(name="element")
    raw = {"kind": "multi_click", "frequency": 2,
           "variables": {"frequency": "{{MultiCount}}"}}
    resolved = {"kind": "multi_click", "frequency": 5}
    with patch.object(gesture, "resolve_click_modifier_variables",
                      return_value=resolved) as m_resolve, \
         patch.object(gesture, "validate_click_modifier",
                      return_value=resolved) as m_validate, \
         patch.object(gesture, "dispatch_gesture", return_value=True) as m_disp:
        clickElement(el, driver, "se_js_ac", click_modifier=raw)
    m_resolve.assert_called_once_with(raw)
    m_validate.assert_called_once_with(resolved)
    m_disp.assert_called_once_with(el, driver, resolved, None)
