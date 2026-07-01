"""Tests for testmu_selenium._helpers.url — driver-level URL/title helpers."""
from unittest.mock import MagicMock

from testmu_selenium._helpers.url import get_url, get_title


def test_get_url_returns_driver_current_url():
    driver = MagicMock()
    driver.current_url = "https://example.com/page"
    assert get_url(driver) == "https://example.com/page"


def test_get_title_returns_driver_title():
    driver = MagicMock()
    driver.title = "Example Domain"
    assert get_title(driver) == "Example Domain"
