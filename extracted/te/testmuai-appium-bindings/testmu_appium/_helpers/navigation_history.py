"""Surface-aware BACK/FORWARD navigation for native and mobile-web screens."""
import logging

from testmu_appium import _action_web, _config
from testmu_appium._errors import UnsupportedOnPlatform, WebSurfaceUnavailable
from testmu_appium._helpers.foreground import foreground_app
from testmu_appium._helpers.keyevent import keyevent

_log = logging.getLogger("testmu_appium")
_SURFACES = frozenset({"native", "web"})


def _web_channel(driver, feature: str):
    package = foreground_app(driver)
    channel = _action_web.visible_channel(package)
    if channel is None:
        raise WebSurfaceUnavailable(feature, package)
    return channel


def _surface(value: str) -> str:
    normalized = str(value or "").strip().lower()
    if normalized not in _SURFACES:
        raise ValueError(
            f"unknown navigation surface {value!r}; expected one of {sorted(_SURFACES)}"
        )
    return normalized


def _navigate_web_history(driver, delta: int, feature: str) -> bool:
    """Move through the visible page's history, in the channel's own dialect.

    The CHANNEL owns how history is walked — Chrome asks where it stands first
    and can report a boundary; WebKit's protocol cannot ask, so its channel
    attempts the move and reports it attempted. The verb only decides direction.
    """
    channel = _web_channel(driver, feature)
    return channel.navigate_history(delta)


def go_back(driver, *, surface: str, description: str = "") -> None:
    """Go back on the explicitly recorded surface.

    Native BACK is a device key. Web BACK is CDP history navigation and never
    falls back to the device key when the page channel is unavailable.
    """
    resolved_surface = _surface(surface)
    suffix = f" — {description}" if description else ""
    if resolved_surface == "native":
        keyevent(driver, "BACK", description=description)
        _log.info("go_back: native%s", suffix)
        return
    moved = _navigate_web_history(driver, -1, "go_back")
    _log.info("go_back: web%s%s", "" if moved else " (history boundary)", suffix)


def go_forward(driver, *, surface: str, description: str = "") -> None:
    """Go forward on the explicitly recorded surface.

    Android has no native forward navigation primitive. It raises rather than
    guessing at ``driver.forward()``, whose meaning is browser-context specific.
    """
    resolved_surface = _surface(surface)
    suffix = f" — {description}" if description else ""
    if resolved_surface == "native":
        raise UnsupportedOnPlatform(
            "go_forward on a native surface", _config.platform()
        )
    moved = _navigate_web_history(driver, 1, "go_forward")
    _log.info("go_forward: web%s%s", "" if moved else " (history boundary)", suffix)
