"""Refresh the visible mobile-web page without changing Appium context."""
import logging

from testmu_appium import _action_web
from testmu_appium._errors import WebSurfaceUnavailable
from testmu_appium._helpers.foreground import foreground_app

_log = logging.getLogger("testmu_appium")


def refresh(driver, *, surface: str, description: str = "") -> None:
    """Reload the visible debuggable page through CDP.

    There is deliberately no ``driver.refresh()`` fallback: Appium remains in
    ``NATIVE_APP``, where that call has browser-context-dependent behavior.
    """
    if surface != "web":
        raise ValueError("refresh requires surface='web'")
    package = foreground_app(driver)
    channel = _action_web.visible_channel(package)
    if channel is None:
        raise WebSurfaceUnavailable("refresh", package)
    channel.call("Page.reload")
    _log.info("refresh")
