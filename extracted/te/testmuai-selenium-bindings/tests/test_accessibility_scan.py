"""accessibility_scan fires the grid hook on cloud, no-ops locally and never fails the test."""
from unittest.mock import MagicMock, patch

import testmu_selenium
from testmu_selenium._helpers.accessibility import accessibility_scan


def test_cloud_sends_the_hook_and_returns_the_reply():
    driver = MagicMock()
    driver.execute_script.return_value = "Lambda accessibility scan completed"
    with patch("testmu_selenium._config.run_target", "cloud"):
        reply = accessibility_scan(driver)
    driver.execute_script.assert_called_once_with("lambda-accessibility-scan")
    assert reply == "Lambda accessibility scan completed"


def test_local_run_is_a_no_op():
    driver = MagicMock()
    with patch("testmu_selenium._config.run_target", "local"):
        assert accessibility_scan(driver) is None
    driver.execute_script.assert_not_called()


def test_failed_hook_is_logged_not_raised():
    driver = MagicMock()
    driver.execute_script.side_effect = Exception("lambda is not defined")
    with patch("testmu_selenium._config.run_target", "cloud"):
        assert accessibility_scan(driver) is None


def test_exported():
    assert "accessibility_scan" in testmu_selenium.__all__
    assert testmu_selenium.accessibility_scan is accessibility_scan
