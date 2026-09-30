"""checkbox/radio clicks skip the element_to_be_clickable wait.

Custom-styled checkboxes and radios are routinely sized 0x0 or moved off-screen
behind a styled label, so `element_to_be_clickable` never reports them
clickable. The Selenium tier then burns the FULL timeout before the JS tier
rescues the click, making every such step slow and flaky.

They are directly clickable when enabled, so click them straight away and keep
the wait for everything else.

Port of V2.
"""
from unittest.mock import MagicMock, patch

import pytest
from selenium.common.exceptions import WebDriverException

from testmu_selenium._helpers.click import _is_checkbox_or_radio, _selenium_click


def _element(tag="input", el_type="checkbox", enabled=True):
    el = MagicMock(name="element")
    el.tag_name = tag
    el.get_attribute.return_value = el_type
    el.is_enabled.return_value = enabled
    return el


# ---------------------------------------------------------------------------
# _is_checkbox_or_radio
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("el_type", ["checkbox", "radio", "CHECKBOX", "Radio"])
def test_detects_checkbox_and_radio_case_insensitively(el_type):
    assert _is_checkbox_or_radio(_element(el_type=el_type)) is True


@pytest.mark.parametrize("tag,el_type", [
    ("input", "text"), ("input", "submit"), ("button", "checkbox"),
    ("div", None), ("INPUT", "password"),
])
def test_rejects_everything_else(tag, el_type):
    assert _is_checkbox_or_radio(_element(tag=tag, el_type=el_type)) is False


def test_missing_tag_or_type_is_not_a_checkbox():
    el = MagicMock(name="element")
    el.tag_name = None
    assert _is_checkbox_or_radio(el) is False
    el2 = _element(el_type=None)
    assert _is_checkbox_or_radio(el2) is False


def test_stale_element_falls_through_rather_than_raising():
    # A detached element must take the normal wait path, not abort the click.
    el = MagicMock(name="element")
    type(el).tag_name = property(lambda self: (_ for _ in ()).throw(WebDriverException("stale")))
    assert _is_checkbox_or_radio(el) is False


# ---------------------------------------------------------------------------
# _selenium_click routing
# ---------------------------------------------------------------------------

def test_enabled_checkbox_clicks_directly_without_the_wait():
    el, driver = _element(), MagicMock(name="driver")
    with patch("testmu_selenium._helpers.click.WebDriverWait") as m_wait:
        assert _selenium_click(el, driver) is True
    m_wait.assert_not_called()
    el.click.assert_called_once_with()


def test_enabled_radio_clicks_directly_without_the_wait():
    el, driver = _element(el_type="radio"), MagicMock(name="driver")
    with patch("testmu_selenium._helpers.click.WebDriverWait") as m_wait:
        _selenium_click(el, driver)
    m_wait.assert_not_called()
    el.click.assert_called_once_with()


def test_disabled_checkbox_still_uses_the_wait():
    # A disabled input is genuinely not clickable — let the wait report that
    # rather than firing a click that silently does nothing.
    el, driver = _element(enabled=False), MagicMock(name="driver")
    with patch("testmu_selenium._helpers.click.WebDriverWait") as m_wait:
        _selenium_click(el, driver)
    m_wait.assert_called_once()


def test_ordinary_element_still_uses_the_wait():
    el, driver = _element(tag="button", el_type=None), MagicMock(name="driver")
    with patch("testmu_selenium._helpers.click.WebDriverWait") as m_wait:
        _selenium_click(el, driver)
    m_wait.assert_called_once()
    el.click.assert_not_called()  # the wait's .until(...) returns the clickable element


def test_driverless_path_is_unchanged():
    el = _element()
    with patch("testmu_selenium._helpers.click.WebDriverWait") as m_wait:
        _selenium_click(el, None)
    m_wait.assert_not_called()
    el.click.assert_called_once_with()
