"""Tests for testmu_selenium._helpers.tabs."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock, call, PropertyMock

from selenium.common.exceptions import NoSuchWindowException

from testmu_selenium._helpers.tabs import new_tab, switch_tab, close_tab


def _make_driver(handles=None, title="Page"):
    """Return a MagicMock driver with window_handles and title set."""
    driver = MagicMock()
    driver.window_handles = handles if handles is not None else ["h0", "h1"]
    driver.title = title
    return driver


# ---------------------------------------------------------------------------
# new_tab
# ---------------------------------------------------------------------------


def test_new_tab_opens_window_and_switches():
    driver = _make_driver(handles=["h0", "h1"])
    new_tab(driver)
    driver.execute_script.assert_called_once_with("window.open()")
    driver.switch_to.window.assert_called_once_with("h1")


def test_new_tab_navigates_when_url_provided():
    driver = _make_driver(handles=["h0", "h1"])
    new_tab(driver, url="https://example.com")
    driver.execute_script.assert_called_once_with("window.open()")
    driver.switch_to.window.assert_called_once_with("h1")
    driver.get.assert_called_once_with("https://example.com")


def test_new_tab_navigates_google_when_url_none():
    driver = _make_driver(handles=["h0", "h1"])
    new_tab(driver, url=None)
    driver.get.assert_called_once_with("https://www.google.com")


# ---------------------------------------------------------------------------
# switch_tab
# ---------------------------------------------------------------------------


def test_switch_tab_by_index():
    driver = _make_driver(handles=["h0", "h1", "h2"])
    switch_tab(driver, index=2)
    driver.switch_to.window.assert_called_once_with("h2")


def test_switch_tab_by_title_searches_handles():
    driver = _make_driver(handles=["h0", "h1", "h2"])
    # title changes as we iterate — mock side effects
    titles = {"h0": "Home", "h1": "About", "h2": "Contact"}

    def switch_side_effect(handle):
        driver.title = titles[handle]

    driver.switch_to.window.side_effect = switch_side_effect
    driver.title = "Home"

    switch_tab(driver, title="About")

    # should have switched to h1 and stopped
    assert driver.switch_to.window.call_args_list == [call("h0"), call("h1")]


def test_switch_tab_with_index_and_title_validates_title_after_switch():
    driver = _make_driver(handles=["h0", "h1", "h2"])
    titles = {"h0": "Home", "h1": "About", "h2": "Contact"}

    def switch_side_effect(handle):
        driver.title = titles[handle]

    driver.switch_to.window.side_effect = switch_side_effect
    # First switch to index=0 → "Home", then search for "About"
    driver.title = "Home"

    switch_tab(driver, index=0, title="About")

    # switched to h0 first (by index), then searched and found h1
    calls = driver.switch_to.window.call_args_list
    assert calls[0] == call("h0")
    assert call("h1") in calls


def test_switch_tab_raises_on_neither_arg():
    driver = _make_driver()
    with pytest.raises(ValueError, match="switch_tab requires index or title"):
        switch_tab(driver)


def test_switch_tab_title_not_found_raises():
    driver = _make_driver(handles=["h0", "h1"])
    titles = {"h0": "Home", "h1": "About"}

    def switch_side_effect(handle):
        driver.title = titles[handle]

    driver.switch_to.window.side_effect = switch_side_effect
    driver.title = "Home"

    with pytest.raises(NoSuchWindowException):
        switch_tab(driver, title="Missing")


# ---------------------------------------------------------------------------
# close_tab
# ---------------------------------------------------------------------------


def test_close_tab_current_when_no_args():
    driver = _make_driver(handles=["h0", "h1"])
    close_tab(driver)
    driver.close.assert_called_once()
    driver.switch_to.window.assert_called_once_with("h1")


def test_close_tab_by_index_then_switches_to_last():
    driver = _make_driver(handles=["h0", "h1", "h2"])
    close_tab(driver, index=1)
    driver.switch_to.window.assert_any_call("h1")
    driver.close.assert_called_once()
    # final switch is to handles[-1] = "h2"
    assert driver.switch_to.window.call_args_list[-1] == call("h2")


def test_close_tab_by_title():
    driver = _make_driver(handles=["h0", "h1", "h2"])
    titles = {"h0": "Home", "h1": "Target", "h2": "Other"}

    def switch_side_effect(handle):
        driver.title = titles[handle]

    driver.switch_to.window.side_effect = switch_side_effect
    driver.title = "Home"

    close_tab(driver, title="Target")

    # Should have found and switched to h1, closed, then switched to last
    switch_calls = driver.switch_to.window.call_args_list
    assert call("h1") in switch_calls
    driver.close.assert_called_once()
    assert switch_calls[-1] == call("h2")


def test_close_tab_with_index_and_title():
    driver = _make_driver(handles=["h0", "h1", "h2"])
    titles = {"h0": "Home", "h1": "About", "h2": "Target"}

    def switch_side_effect(handle):
        driver.title = titles[handle]

    driver.switch_to.window.side_effect = switch_side_effect
    driver.title = "Home"

    # index=0 → "Home", but title="Target" → should search and find h2
    close_tab(driver, index=0, title="Target")

    switch_calls = driver.switch_to.window.call_args_list
    assert call("h2") in switch_calls
    driver.close.assert_called_once()
    assert switch_calls[-1] == call("h2")
