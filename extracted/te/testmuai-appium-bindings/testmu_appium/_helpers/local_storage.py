"""Origin-scoped mobile-web localStorage verbs over the visible CDP page."""
import logging

from testmu_appium import _action_web
from testmu_appium._errors import WebSurfaceUnavailable
from testmu_appium._helpers.foreground import foreground_app
from testmu_appium._vars import var

_log = logging.getLogger("testmu_appium")

_SET_ITEMS = """function(items) {
    for (const [key, value] of Object.entries(items)) {
        this.localStorage.setItem(key, value);
    }
}"""

_DELETE_KEYS = """function(keys) {
    for (const key of keys) {
        this.localStorage.removeItem(key);
    }
}"""

_CLEAR = """function() {
    this.localStorage.clear();
}"""


def _visible_channel(driver, feature: str):
    package = foreground_app(driver)
    channel = _action_web.visible_channel(package)
    if channel is None:
        raise WebSurfaceUnavailable(feature, package)
    return channel


def _items(value) -> dict[str, str]:
    if not isinstance(value, dict) or not value:
        raise ValueError("items must be a non-empty dict")
    if any(not isinstance(key, str) or not key for key in value):
        raise ValueError("localStorage keys must be non-empty strings")
    # Resolve against the replay-time store without changing the recorded map.
    # Web Storage is string-only, so preserve setItem's string-value contract.
    return {key: str(var(item)) for key, item in value.items()}


def _keys(value) -> list[str]:
    if (
        not isinstance(value, list)
        or not value
        or any(not isinstance(key, str) or not key for key in value)
    ):
        raise ValueError("keys must be a non-empty list of non-empty strings")
    return list(value)


def set_local_storage(
    driver, items: dict, *, description: str = ""
) -> None:
    """Set entries in localStorage for the currently visible page's origin."""
    resolved = _items(items)
    channel = _visible_channel(driver, "set_local_storage")
    channel.call_function(_SET_ITEMS, (resolved,))
    # Values can be credentials or API output. Only their count is safe to log.
    _log.info("set_local_storage: set %d item(s)", len(resolved))


def delete_local_storage(
    driver, keys: list[str], *, description: str = ""
) -> None:
    """Remove keys from localStorage for the currently visible page's origin."""
    copied = _keys(keys)
    channel = _visible_channel(driver, "delete_local_storage")
    channel.call_function(_DELETE_KEYS, (copied,))
    _log.info("delete_local_storage: removed %d key(s)", len(copied))


def clear_local_storage(driver, *, description: str = "") -> None:
    """Clear localStorage for the currently visible page's origin."""
    channel = _visible_channel(driver, "clear_local_storage")
    channel.call_function(_CLEAR)
    _log.info("clear_local_storage")
