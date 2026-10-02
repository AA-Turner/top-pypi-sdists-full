"""Foreground-app identity, resolved through the platform adapter registries.

The foreground app is what binds a WebView debug socket to its owner. Every
module that needs it resolves through this one registry row: the android row
reads Appium's ``current_package`` endpoint, the ios row reads the bundle id out
of ``mobile: activeAppInfo``, both swallow a failed read to an empty identity,
and a platform without a row raises ``UnsupportedOnPlatform`` before any driver
read happens.
"""
import logging

from testmu_appium._helpers import _adapters

_log = logging.getLogger("testmu_appium")


def _android_foreground_app(driver) -> str:
    """The Android foreground package; empty when the driver cannot report one."""
    try:
        return str(driver.current_package or "")
    except Exception as e:  # noqa: BLE001 — the package read is best-effort
        _log.debug("[foreground] current package unavailable: %s", e)
        return ""


def _ios_foreground_app(driver) -> str:
    """The iOS foreground bundle id; empty when the driver cannot report one.

    There is no `current_package` counterpart — the bundle id comes from
    `mobile: activeAppInfo`, which reports the app actually in front rather than
    the one the session launched. They differ the moment a test leaves the app
    under test, which is exactly when a WebView socket needs binding to its owner.
    """
    try:
        info = driver.execute_script("mobile: activeAppInfo", {}) or {}
    except Exception as e:  # noqa: BLE001 — the identity read is best-effort
        _log.debug("[foreground] active app info unavailable: %s", e)
        return ""
    # The same read carries the pid, which is what target ownership on the one
    # shared iwdp endpoint filters by — stash it while it is in hand rather than
    # paying a second driver round-trip later.
    from testmu_appium._helpers import _web_ios  # noqa: PLC0415
    _web_ios.note_foreground(int(info.get("pid") or 0))
    return str(info.get("bundleId") or "")


_adapters.register("foreground_app", {
    "android": {"identify": _android_foreground_app},
    "ios": {"identify": _ios_foreground_app},
})


def foreground_app(driver) -> str:
    """The identity of the app in the foreground, in the platform's own vocabulary."""
    identify = _adapters.adapter("foreground_app", "identify", "foreground app identity")
    return identify(driver)
