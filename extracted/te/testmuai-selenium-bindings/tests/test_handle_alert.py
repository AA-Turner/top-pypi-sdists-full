"""Tests for testmu_selenium._helpers.dialog.handle_alert."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from selenium.common.exceptions import NoAlertPresentException

from testmu_selenium._helpers.dialog import handle_alert


def _driver_with_alert():
    driver = MagicMock()
    alert = MagicMock()
    driver.switch_to.alert = alert
    return driver, alert


class TestHandleAlertAccept:
    def test_accept_no_value_calls_accept_only(self):
        driver, alert = _driver_with_alert()
        handle_alert(driver, action="accept")
        alert.accept.assert_called_once()
        alert.send_keys.assert_not_called()
        alert.dismiss.assert_not_called()

    def test_accept_with_value_sends_keys_then_accepts(self):
        driver, alert = _driver_with_alert()
        handle_alert(driver, action="accept", value="hello")
        alert.send_keys.assert_called_once_with("hello")
        alert.accept.assert_called_once()
        alert.dismiss.assert_not_called()


class TestHandleAlertDismiss:
    def test_dismiss_calls_dismiss_only(self):
        driver, alert = _driver_with_alert()
        handle_alert(driver, action="dismiss")
        alert.dismiss.assert_called_once()
        alert.accept.assert_not_called()
        alert.send_keys.assert_not_called()

    def test_dismiss_ignores_value(self):
        """Dismiss should never type into the prompt even if value is supplied."""
        driver, alert = _driver_with_alert()
        handle_alert(driver, action="dismiss", value="ignored")
        alert.send_keys.assert_not_called()
        alert.dismiss.assert_called_once()


class TestHandleAlertRetry:
    def test_retries_on_no_alert_present(self):
        """A dialog opening a tick after the trigger should still be handled."""
        driver = MagicMock()
        alert = MagicMock()
        # First switch raises NoAlertPresent, second succeeds.
        type(driver.switch_to).alert = property(MagicMock(side_effect=[
            NoAlertPresentException(),
            alert,
        ]))
        handle_alert(driver, action="accept", max_attempts=2, retry_delay=0.0)
        alert.accept.assert_called_once()

    def test_propagates_after_max_attempts(self):
        driver = MagicMock()
        type(driver.switch_to).alert = property(MagicMock(side_effect=NoAlertPresentException()))
        with pytest.raises(NoAlertPresentException):
            handle_alert(driver, action="accept", max_attempts=2, retry_delay=0.0)
