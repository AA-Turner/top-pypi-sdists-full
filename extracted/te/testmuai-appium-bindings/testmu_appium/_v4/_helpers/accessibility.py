"""DRIVER-mode accessibility_scan verb — trigger the LambdaTest a11y scan.

The scan itself is LambdaTest infrastructure: the hook marks the moment in the
session and the platform's scanner does the work (parity with the legacy V2
exported runtime, auteur models/appium_uiActions.py::execute_accessibility_scan).
Locally there is no scanner, so the verb records a log line and returns — the
recorded test keeps replaying instead of failing on an infra-only feature.
"""
import logging

from testmu_appium import _config

_log = logging.getLogger("testmu_appium")


def accessibility_scan(driver, *, description: str = "") -> None:
    """Run a LambdaTest accessibility scan on the current screen.

    Args:
        driver: Live Appium webdriver session.
        description: Optional human-readable label for the INFO log line.
    """
    suffix = f" — {description}" if description else ""
    if _config.run_target != "cloud":
        _log.info("accessibility_scan: no-op outside LambdaTest cloud%s", suffix)
        return
    driver.execute_script("lambda-accessibility-scan")
    _log.info("accessibility_scan: triggered%s", suffix)
