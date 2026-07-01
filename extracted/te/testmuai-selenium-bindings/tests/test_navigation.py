"""Tests for testmu_selenium._helpers.navigation — refresh, go_back, go_forward."""
from __future__ import annotations

from unittest.mock import MagicMock

from testmu_selenium._helpers.navigation import go_back, go_forward, refresh


class TestRefresh:
    def test_refresh_calls_driver_refresh(self):
        driver = MagicMock()
        refresh(driver)
        driver.refresh.assert_called_once()


class TestGoBack:
    def test_go_back_calls_driver_back(self):
        driver = MagicMock()
        go_back(driver)
        driver.back.assert_called_once()


class TestGoForward:
    def test_go_forward_calls_driver_forward(self):
        driver = MagicMock()
        go_forward(driver)
        driver.forward.assert_called_once()
