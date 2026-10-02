"""Mobile-web cookie management without leaving Appium's native context.

The visible page is reached through the same debug side channel used by hybrid
element actions, and the CHANNEL owns the wire vocabulary — Chrome answers in
Network/Storage methods, WebKit in its own (with an httpOnly write limit its
protocol imposes). The Appium driver remains in ``NATIVE_APP`` throughout.
"""
import logging

from testmu_appium import _action_web
from testmu_appium._errors import WebSurfaceUnavailable
from testmu_appium._helpers.foreground import foreground_app
from testmu_appium._vars import var

_log = logging.getLogger("testmu_appium")

_COOKIE_FIELDS = frozenset({
    "name", "value", "url", "domain", "path", "secure", "httpOnly",
    "sameSite", "expires", "priority", "sameParty", "sourceScheme",
    "sourcePort", "partitionKey",
})


def _visible_channel(driver, feature: str):
    package = foreground_app(driver)
    channel = _action_web.visible_channel(package)
    if channel is None:
        raise WebSurfaceUnavailable(feature, package)
    return channel


def _cookie_param(cookie: dict, current_url: str) -> dict:
    if not isinstance(cookie, dict):
        raise TypeError(f"cookie must be a dict, got {type(cookie).__name__}")
    unknown = set(cookie) - _COOKIE_FIELDS
    if unknown:
        raise ValueError(f"unsupported cookie fields: {sorted(unknown)}")

    result = {key: value for key, value in cookie.items() if key in _COOKIE_FIELDS}
    if not str(result.get("name") or ""):
        raise ValueError("cookie name must not be empty")
    result["name"] = str(result["name"])
    result["value"] = str(var(result.get("value", "")))

    # A URL is a runtime property of the visible page, not authoring metadata.
    # A caller that supplied any explicit scoping field owns that scope.
    if not any(key in result for key in ("url", "domain", "path")):
        if not current_url:
            raise RuntimeError("visible mobile web page did not report location.href")
        result["url"] = current_url
    return result


def set_cookies(driver, cookies: list, *, description: str = "") -> None:
    """Set cookies on the visible mobile-web page through CDP.

    Cookie values resolve ``{{variable}}`` templates at replay time. Cookies
    without ``url``, ``domain`` or ``path`` are scoped to the visible page's
    current URL at replay time.
    """
    channel = _visible_channel(driver, "set_cookies")
    current_url = ""
    if any(
        isinstance(cookie, dict)
        and not any(key in cookie for key in ("url", "domain", "path"))
        for cookie in cookies
    ):
        current_url = str(channel.evaluate("location.href") or "")
    params = [_cookie_param(cookie, current_url) for cookie in cookies]
    channel.set_cookies(params)
    suffix = f" — {description}" if description else ""
    _log.info("set_cookies: set %d cookie(s)%s", len(params), suffix)


def delete_cookies(driver, names: list[str], *, description: str = "") -> None:
    """Delete every cookie with one of ``names`` across the current context."""
    channel = _visible_channel(driver, "delete_cookies")
    wanted = {str(name) for name in names}
    deleted = 0
    for cookie in channel.get_cookies():
        if cookie.get("name") not in wanted:
            continue
        channel.delete_cookie(cookie)
        deleted += 1
    suffix = f" — {description}" if description else ""
    _log.info("delete_cookies: deleted %d cookie(s)%s", deleted, suffix)


def clear_cookies(driver, *, description: str = "") -> None:
    """Clear all browser cookies visible to the current CDP context."""
    channel = _visible_channel(driver, "clear_cookies")
    channel.clear_cookies()
    suffix = f" — {description}" if description else ""
    _log.info("clear_cookies%s", suffix)
