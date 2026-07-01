"""Tests for testmu_selenium._helpers.wait — timing/condition wait helpers."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from testmu_selenium._helpers.wait import wait, wait_for_load, wait_until


class TestWait:
    def test_wait_sleeps_for_milliseconds_converted_to_seconds(self):
        with patch("testmu_selenium._helpers.wait.time.sleep") as mock_sleep:
            wait(MagicMock(), milliseconds=2000)
        mock_sleep.assert_called_once_with(2.0)

    def test_wait_no_op_when_milliseconds_none(self):
        with patch("testmu_selenium._helpers.wait.time.sleep") as mock_sleep:
            wait(MagicMock())
        mock_sleep.assert_not_called()

    def test_wait_fractional_milliseconds(self):
        with patch("testmu_selenium._helpers.wait.time.sleep") as mock_sleep:
            wait(MagicMock(), milliseconds=500)
        mock_sleep.assert_called_once_with(0.5)


class TestWaitUntil:
    """Pins wait_until to a fixed sleep on purpose. Codegen emits a static sleep
    for WaitUntilNode and never calls this helper with a pollable condition;
    real polling is a code-gen-layer follow-up, not a binding gap."""

    def test_wait_until_sleeps_for_timeout_seconds(self):
        with patch("testmu_selenium._helpers.wait.time.sleep") as mock_sleep:
            wait_until(MagicMock(), query="some condition", timeout=5000)
        mock_sleep.assert_called_once_with(5.0)

    def test_wait_until_default_timeout_is_30000ms(self):
        with patch("testmu_selenium._helpers.wait.time.sleep") as mock_sleep:
            wait_until(MagicMock(), query="some condition")
        mock_sleep.assert_called_once_with(30.0)


class TestWaitForLoad:
    def _make_driver(self, ready_states):
        """Build a mock driver returning successive readyState values."""
        driver = MagicMock()
        states = iter(ready_states)
        last = ready_states[-1]

        def _exec_script(script, *args):
            nonlocal last
            try:
                last = next(states)
            except StopIteration:
                pass
            return last

        driver.execute_script.side_effect = _exec_script
        return driver

    def test_wait_for_load_polls_until_complete(self):
        driver = self._make_driver(['loading', 'loading', 'complete'])
        wait_for_load(driver, state='load')
        assert driver.execute_script.call_count >= 3

    def test_wait_for_load_networkidle_treated_as_load(self):
        # Selenium has no native network-idle wait, so 'networkidle' intentionally
        # behaves like 'load' (polls readyState until 'complete').
        driver = self._make_driver(['loading', 'complete'])
        wait_for_load(driver, state='networkidle')
        assert driver.execute_script.call_count >= 2

    def test_wait_for_load_domcontentloaded_stops_at_interactive_or_complete(self):
        driver = self._make_driver(['loading', 'interactive'])
        wait_for_load(driver, state='domcontentloaded')
        # Stopped polling once readyState != 'loading'
        assert driver.execute_script.call_count >= 2

    def test_wait_for_load_default_state_is_load(self):
        import inspect
        sig = inspect.signature(wait_for_load)
        assert sig.parameters['state'].default == 'load'

    def test_wait_for_load_load_state_completes_immediately_when_already_complete(self):
        driver = self._make_driver(['complete'])
        wait_for_load(driver, state='load')
        assert driver.execute_script.call_count >= 1

    def test_wait_for_load_domcontentloaded_does_not_stop_at_loading(self):
        # Ensure that 'loading' keeps the loop going; only 'interactive'/'complete' exits
        driver = self._make_driver(['loading', 'loading', 'complete'])
        wait_for_load(driver, state='domcontentloaded')
        assert driver.execute_script.call_count >= 3
