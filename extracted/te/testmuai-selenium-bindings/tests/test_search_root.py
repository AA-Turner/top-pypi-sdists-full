"""Tests for the search_root parameter — shadow-DOM element resolution.

When search_root is provided, findElement must resolve selectors against that
WebElement (a shadow-root child) instead of the driver. When None, lookups run
against the driver — the exact pre-existing behaviour. Only the element LOOKUP
uses search_root; the action still runs on driver.

When search_root is a ShadowRoot, XPath candidates are skipped upfront because
ShadowRoot.find_element rejects By.XPATH with InvalidArgumentException and XPath
cannot pierce shadow boundaries. Only CSS candidates run.
"""
import pytest
from unittest.mock import MagicMock, patch

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.shadowroot import ShadowRoot

from testmu_selenium import _action_click as ac
from testmu_selenium._action_click import click
from testmu_selenium._helpers.find_element import findElement


PRIMARY = [{"selector": "#login", "isXPath": False}]


# ---------------------------------------------------------------------------
# findElement: search_root routing
# ---------------------------------------------------------------------------

def test_find_element_uses_search_root_when_provided():
    """search_root.find_element resolves the selector; driver.find_element is NOT used."""
    driver = MagicMock(name="driver")
    sentinel = MagicMock(name="resolved-element")
    root = MagicMock(name="shadow-root-child")
    root.find_element.return_value = sentinel

    result = findElement(driver, PRIMARY, search_root=root)

    assert result is sentinel
    root.find_element.assert_called_once_with(by=By.CSS_SELECTOR, value="#login")
    driver.find_element.assert_not_called()


def test_find_element_falls_back_to_driver_when_search_root_none():
    """search_root=None preserves pre-existing behaviour: driver does the lookup."""
    driver = MagicMock(name="driver")
    sentinel = MagicMock(name="resolved-element")
    driver.find_element.return_value = sentinel

    result = findElement(driver, PRIMARY, search_root=None)

    assert result is sentinel
    driver.find_element.assert_called_once_with(by=By.CSS_SELECTOR, value="#login")


def test_find_element_default_search_root_is_none():
    """Omitting search_root entirely is identical to passing None (driver lookup)."""
    driver = MagicMock(name="driver")
    sentinel = MagicMock(name="resolved-element")
    driver.find_element.return_value = sentinel

    result = findElement(driver, PRIMARY)

    assert result is sentinel
    driver.find_element.assert_called_once()


# ---------------------------------------------------------------------------
# Wrapper threading: search_root flows from the public wrapper into _run_action
# ---------------------------------------------------------------------------

def test_click_threads_search_root_kwarg():
    """click() must forward search_root to _run_action so the engine can pierce
    shadow DOM. Guards against a silently dropped pass-through."""
    driver = MagicMock(name="driver")
    root = MagicMock(name="shadow-root-child")
    with patch.object(ac, "_run_action", return_value=True) as m_run:
        click(driver, PRIMARY, search_root=root)

    assert m_run.call_args.kwargs["search_root"] is root


def test_click_default_search_root_is_none():
    """Without a caller-supplied search_root, the wrapper threads None (no-op)."""
    driver = MagicMock(name="driver")
    with patch.object(ac, "_run_action", return_value=True) as m_run:
        click(driver, PRIMARY)

    assert m_run.call_args.kwargs["search_root"] is None


# ---------------------------------------------------------------------------
# ShadowRoot root: CSS-only lookups (shadow-piercing contract)
# ---------------------------------------------------------------------------

def test_find_element_shadow_root_css_only_hit():
    """ShadowRoot + CSS selector: element returned, XPATH never passed to root."""
    driver = MagicMock(name="driver")
    sentinel = MagicMock(name="resolved-element")
    root = MagicMock(spec=ShadowRoot, name="shadow-root")
    root.find_element.return_value = sentinel

    result = findElement(driver, [{"selector": "#target", "isXPath": False}], search_root=root)

    assert result is sentinel
    root.find_element.assert_called_once_with(by=By.CSS_SELECTOR, value="#target")
    driver.find_element.assert_not_called()
    # Confirm By.XPATH was never passed to the shadow root
    for call in root.find_element.call_args_list:
        assert call.kwargs.get("by") != By.XPATH


def test_find_element_shadow_root_skips_xpath_uses_css():
    """ShadowRoot + [xpath, css] list: xpath skipped, root.find_element called ONCE with CSS."""
    driver = MagicMock(name="driver")
    sentinel = MagicMock(name="resolved-element")
    root = MagicMock(spec=ShadowRoot, name="shadow-root")
    root.find_element.return_value = sentinel

    selectors = [
        {"selector": "//div[@id='target']", "isXPath": True},
        {"selector": "#target", "isXPath": False},
    ]
    result = findElement(driver, selectors, search_root=root)

    assert result is sentinel
    # ONCE — xpath candidate was silently skipped before any driver round-trip
    root.find_element.assert_called_once_with(by=By.CSS_SELECTOR, value="#target")
    driver.find_element.assert_not_called()


def test_find_element_shadow_root_only_xpath_raises():
    """ShadowRoot + only-xpath selectors: NoSuchElementException with descriptive message."""
    driver = MagicMock(name="driver")
    root = MagicMock(spec=ShadowRoot, name="shadow-root")

    selectors = [{"selector": "//div[@id='x']", "isXPath": True}]
    with pytest.raises(NoSuchElementException) as exc_info:
        findElement(driver, selectors, search_root=root)

    # Root must never be called — all candidates skipped
    root.find_element.assert_not_called()
    driver.find_element.assert_not_called()
    # Message must mention the skip reason so callers can diagnose
    msg = str(exc_info.value)
    assert "xpath" in msg.lower()
    assert "shadowroot" in msg.lower()


def test_find_element_shadow_root_mixed_list_css_failure_wins():
    """ShadowRoot + [xpath, css] where the CSS candidate genuinely fails:
    the real CSS NoSuchElementException (last_exception) is raised, NOT the
    synthetic skip-mention message — real failures are more informative."""
    driver = MagicMock(name="driver")
    root = MagicMock(spec=ShadowRoot, name="shadow-root")
    css_exc = NoSuchElementException("no such element: #target")
    root.find_element.side_effect = css_exc

    selectors = [
        {"selector": "//div[@id='target']", "isXPath": True},
        {"selector": "#target", "isXPath": False},
    ]
    with pytest.raises(NoSuchElementException) as exc_info:
        findElement(driver, selectors, search_root=root)

    # The genuine CSS failure surfaces — not the synthetic skip message
    assert exc_info.value is css_exc
    root.find_element.assert_called_once_with(by=By.CSS_SELECTOR, value="#target")


def test_find_element_webelem_xpath_unchanged():
    """Plain WebElement root with xpath: behavior byte-identical to pre-ShadowRoot code."""
    driver = MagicMock(name="driver")
    sentinel = MagicMock(name="resolved-element")
    root = MagicMock(name="web-element")  # NOT spec=ShadowRoot — plain mock
    root.find_element.return_value = sentinel

    result = findElement(
        driver,
        [{"selector": "//div[@id='x']", "isXPath": True}],
        search_root=root,
    )

    assert result is sentinel
    root.find_element.assert_called_once_with(by=By.XPATH, value="//div[@id='x']")
    driver.find_element.assert_not_called()
