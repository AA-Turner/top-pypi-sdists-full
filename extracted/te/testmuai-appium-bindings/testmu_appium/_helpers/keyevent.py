"""DRIVER-mode keyevent verb — press a semantic device key.

No selector, no find, no heal: the only work here is resolving the semantic key
name to the live platform's numeric keycode and dispatching it to the driver.
"""
import logging

from testmu_appium import _config
from testmu_appium._helpers import _keys

_log = logging.getLogger("testmu_appium")


def keyevent(driver, key: str | int, *, description: str = "") -> None:
    """Press a named device key, or a numeric keycode on Android.

    Resolution and platform gating both live in ``_helpers._keys.keycode`` — this
    verb only dispatches the resolved code. ``UnknownKeyEvent`` /
    ``UnsupportedOnPlatform`` raised by ``keycode()`` propagate unchanged, since
    there is nothing to retry or heal for a key event.

    Args:
        driver: Live Appium webdriver session.
        key: Case-insensitive semantic name (e.g. "BACK", "ENTER"). Android
            also accepts nonnegative integers or decimal strings (e.g. 4, "4").
            Numeric codes are passed directly to Appium; iOS requires names.
        description: Optional human-readable label for the INFO log line.

    Raises:
        UnknownKeyEvent: `key` has no keycode row for the configured platform.
        UnsupportedOnPlatform: the platform's keycode table isn't shipped.
    """
    token = _keys.dispatch(driver, key, _config.platform())
    suffix = f" — {description}" if description else ""
    # %s, not %d: only Android's token is a number. iOS resolves to a button name
    # or a character, whose tuple repr keeps control characters escaped here.
    _log.info("keyevent: %s (%s)%s", key, token, suffix)
