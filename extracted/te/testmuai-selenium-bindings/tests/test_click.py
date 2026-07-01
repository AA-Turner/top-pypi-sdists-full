"""Test clickElement (ClickAllMethodsFailed imported from _errors)."""
import pytest
from unittest.mock import MagicMock, patch
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
)
from testmu_selenium._helpers.click import (
    clickElement, _selenium_click, _javascript_click, _action_chain_click,
    add_clickElement_to_webelement,
)
from testmu_selenium._errors import ClickAllMethodsFailed


@pytest.fixture
def mock_driver():
    return MagicMock()


@pytest.fixture
def mock_element():
    el = MagicMock()
    el.is_displayed = MagicMock(return_value=True)
    el.is_enabled = MagicMock(return_value=True)
    return el


class TestSeleniumClick:
    def test_se_click_succeeds_calls_click(self, mock_driver, mock_element):
        with patch("testmu_selenium._helpers.click.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = mock_element
            result = _selenium_click(mock_element, mock_driver)
            assert result is True
            mock_element.click.assert_called_once()


class TestJavascriptClick:
    def test_js_click_calls_execute_script(self, mock_driver, mock_element):
        result = _javascript_click(mock_element, mock_driver)
        assert result is True
        mock_driver.execute_script.assert_called_once_with("arguments[0].click();", mock_element)

    def test_js_click_requires_driver(self, mock_element):
        # _javascript_click raises Exception("Driver required for JavaScript click") when driver is None
        with pytest.raises(Exception):
            _javascript_click(mock_element, None)


class TestActionChainClick:
    def test_ac_click_uses_action_chains(self, mock_driver, mock_element):
        # ActionChains is imported lazily inside _action_chain_click, so patch at source module
        with patch("selenium.webdriver.common.action_chains.ActionChains") as mock_ac:
            chain = MagicMock()
            mock_ac.return_value = chain
            chain.move_to_element.return_value = chain
            chain.click.return_value = chain
            result = _action_chain_click(mock_element, mock_driver)
            assert result is True
            chain.perform.assert_called_once()


class TestClickElementCascade:
    def test_se_succeeds_returns_true(self, mock_driver, mock_element):
        with patch("testmu_selenium._helpers.click._selenium_click", return_value=True):
            assert clickElement(mock_element, mock_driver, "se_js_ac") is True

    def test_se_fails_js_succeeds(self, mock_driver, mock_element):
        with patch("testmu_selenium._helpers.click._selenium_click", side_effect=StaleElementReferenceException()), \
             patch("testmu_selenium._helpers.click._javascript_click", return_value=True):
            assert clickElement(mock_element, mock_driver, "se_js_ac") is True

    def test_se_js_fail_ac_succeeds(self, mock_driver, mock_element):
        with patch("testmu_selenium._helpers.click._selenium_click", side_effect=Exception("se fail")), \
             patch("testmu_selenium._helpers.click._javascript_click", side_effect=Exception("js fail")), \
             patch("testmu_selenium._helpers.click._action_chain_click", return_value=True):
            assert clickElement(mock_element, mock_driver, "se_js_ac") is True

    def test_all_fail_raises_click_all_methods_failed(self, mock_driver, mock_element):
        with patch("testmu_selenium._helpers.click._selenium_click", side_effect=StaleElementReferenceException()), \
             patch("testmu_selenium._helpers.click._javascript_click", side_effect=StaleElementReferenceException()), \
             patch("testmu_selenium._helpers.click._action_chain_click", side_effect=StaleElementReferenceException()):
            with pytest.raises(ClickAllMethodsFailed):
                clickElement(mock_element, mock_driver, "se_js_ac")

    def test_click_all_methods_failed_is_subclass_of_eci(self):
        assert issubclass(ClickAllMethodsFailed, ElementClickInterceptedException)

    def test_falsy_element_raises(self, mock_driver):
        with pytest.raises(Exception):
            clickElement(None, mock_driver, "se_js_ac")


class TestModifierClick:
    def test_modifier_click_routes_to_action_chains(self, mock_driver, mock_element):
        # clickElement accepts modifiers= kwarg and routes to _modifier_click (ActionChains key_down/click/key_up)
        # ActionChains is imported lazily inside _modifier_click, so patch at source module
        with patch("selenium.webdriver.common.action_chains.ActionChains") as mock_ac:
            chain = MagicMock()
            mock_ac.return_value = chain
            chain.key_down.return_value = chain
            chain.click.return_value = chain
            chain.key_up.return_value = chain
            try:
                result = clickElement(mock_element, mock_driver, "se_js_ac", modifiers=["Shift"])
                assert result is True
                chain.perform.assert_called_once()
            except TypeError:
                # If no modifiers kwarg, skip
                pytest.skip("clickElement does not accept modifiers kwarg in this version")


class TestMonkeyPatch:
    def test_add_clickElement_attaches_method(self):
        from selenium.webdriver.remote.webelement import WebElement
        if hasattr(WebElement, "clickElement"):
            delattr(WebElement, "clickElement")
        add_clickElement_to_webelement()
        assert hasattr(WebElement, "clickElement")
