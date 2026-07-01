"""Test findElement (V3 Selenium binding element-location helper)."""
import pytest
from unittest.mock import MagicMock
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from testmu_selenium._helpers.find_element import findElement


@pytest.fixture
def mock_driver():
    return MagicMock()


class TestFindElementSelectorList:
    def test_first_selector_matches(self, mock_driver):
        el = MagicMock()
        mock_driver.find_element.return_value = el
        selectors = [{"selector": ".btn", "isXPath": False}]
        assert findElement(mock_driver, selectors) is el

    def test_falls_through_to_second_selector_on_first_miss(self, mock_driver):
        el = MagicMock()
        mock_driver.find_element.side_effect = [NoSuchElementException(), el]
        selectors = [
            {"selector": ".missing", "isXPath": False},
            {"selector": ".btn", "isXPath": False},
        ]
        assert findElement(mock_driver, selectors) is el
        assert mock_driver.find_element.call_count == 2

    def test_all_miss_raises_last_exception(self, mock_driver):
        # No description -> no autoheal print path; raises last exception directly.
        last_exc = NoSuchElementException("second-miss")
        mock_driver.find_element.side_effect = [
            NoSuchElementException("first-miss"),
            last_exc,
        ]
        selectors = [
            {"selector": ".a", "isXPath": False},
            {"selector": ".b", "isXPath": False},
        ]
        with pytest.raises(NoSuchElementException) as exc_info:
            findElement(mock_driver, selectors)
        assert exc_info.value is last_exc

    def test_empty_selector_list_raises_no_such_element(self, mock_driver):
        """Empty selector list must raise NoSuchElementException, not bare Exception.

        Vision-agent sourced ops (CLEAR / CLICK / TYPE / etc. without a bound
        selector) arrive at the verb wrapper with an empty selector list.
        _run_action's _DEFAULT_RECOVERABLE catches NoSuchElementException to
        trigger the heal cascade — a bare Exception escapes that net, and the
        wrapper fails before description/coordinate heal can resolve the field.
        """
        with pytest.raises(NoSuchElementException) as exc_info:
            findElement(mock_driver, [])
        assert "Element not found with selectors" in str(exc_info.value)

    def test_xpath_selector_uses_by_xpath(self, mock_driver):
        el = MagicMock()
        mock_driver.find_element.return_value = el
        selectors = [{"selector": "//div", "isXPath": True}]
        findElement(mock_driver, selectors)
        call = mock_driver.find_element.call_args
        args, kwargs = call
        assert kwargs.get("by") == By.XPATH or (args and args[0] == By.XPATH)
        assert kwargs.get("value") == "//div" or (len(args) > 1 and args[1] == "//div")

    def test_css_selector_uses_by_css(self, mock_driver):
        el = MagicMock()
        mock_driver.find_element.return_value = el
        selectors = [{"selector": ".btn", "isXPath": False}]
        findElement(mock_driver, selectors)
        call = mock_driver.find_element.call_args
        args, kwargs = call
        assert kwargs.get("by") == By.CSS_SELECTOR or (args and args[0] == By.CSS_SELECTOR)

    def test_isxpath_defaults_to_false_when_missing(self, mock_driver):
        el = MagicMock()
        mock_driver.find_element.return_value = el
        # No isXPath key present -> defaults to CSS_SELECTOR.
        selectors = [{"selector": ".btn"}]
        findElement(mock_driver, selectors)
        call = mock_driver.find_element.call_args
        args, kwargs = call
        assert kwargs.get("by") == By.CSS_SELECTOR or (args and args[0] == By.CSS_SELECTOR)

    def test_stops_at_first_match_no_extra_calls(self, mock_driver):
        el = MagicMock()
        mock_driver.find_element.return_value = el
        selectors = [
            {"selector": ".first", "isXPath": False},
            {"selector": ".second", "isXPath": False},
        ]
        findElement(mock_driver, selectors)
        assert mock_driver.find_element.call_count == 1


class TestFindElementAutoheal:
    def test_allow_autoheal_false_suppresses_print(self, mock_driver, capsys):
        mock_driver.find_element.side_effect = NoSuchElementException("nope")
        selectors = [{"selector": ".a", "isXPath": False}]
        with pytest.raises(NoSuchElementException):
            findElement(
                mock_driver,
                selectors,
                description="login button",
                allow_autoheal=False,
            )
        captured = capsys.readouterr()
        assert "autoheal" not in captured.out.lower()

    def test_no_description_no_autoheal_print(self, mock_driver, capsys):
        mock_driver.find_element.side_effect = NoSuchElementException("nope")
        selectors = [{"selector": ".a", "isXPath": False}]
        with pytest.raises(NoSuchElementException):
            findElement(mock_driver, selectors)
        captured = capsys.readouterr()
        assert "autoheal" not in captured.out.lower()

    def test_autoheal_not_invoked_on_success(self, mock_driver, capsys):
        el = MagicMock()
        mock_driver.find_element.return_value = el
        selectors = [{"selector": ".btn", "isXPath": False}]
        findElement(mock_driver, selectors, description="login")
        captured = capsys.readouterr()
        assert "autoheal" not in captured.out.lower()


class TestFindElementTraces:
    def test_logs_finding_and_found_locator(self, mock_driver, caplog):
        el = MagicMock()
        mock_driver.find_element.return_value = el
        with caplog.at_level("INFO"):
            findElement(mock_driver, [{"selector": ".btn", "isXPath": False}])
        assert "Finding element..." in caplog.text
        assert "Element found using locator: .btn" in caplog.text

    def test_logs_the_matching_locator_not_the_first(self, mock_driver, caplog):
        el = MagicMock()
        mock_driver.find_element.side_effect = [NoSuchElementException(), el]
        selectors = [
            {"selector": ".missing", "isXPath": False},
            {"selector": ".btn", "isXPath": False},
        ]
        with caplog.at_level("INFO"):
            findElement(mock_driver, selectors)
        assert "Element found using locator: .btn" in caplog.text
        assert "Element found using locator: .missing" not in caplog.text
