"""DRIVER-mode navigate verb — app switch, BACK, or a deeplink.

Three routes, dispatched on the *resolved* url value: "app://<id>" activates an
app, the literal "back" issues the BACK key event, and anything else is treated
as a deeplink URL.
"""
import logging

from testmu_appium import _config
from testmu_appium._helpers import _adapters
from testmu_appium._helpers.keyevent import keyevent
from testmu_appium._vars import var

_log = logging.getLogger("testmu_appium")

_APP_SCHEME = "app://"

#: platform → the key "mobile: deepLink" names the target app with. The whole of
#: the platform difference for this route.
def _deeplink(app_key: str):
    """A deeplink opener naming the target app the way this platform does.

    Both platforms serve the same "mobile: deepLink" script and disagree only on
    the payload key — Android's "package", iOS's "bundleId". That is the entire
    platform difference for this route, so it is a closure over a key name rather
    than two implementations. An explicit ``package`` (the recorded deeplink's
    target) overrides the configured app_id fallback.

    With NEITHER, the key is left out rather than sent empty. The app is optional
    on both drivers — absent means "let the OS resolve the url's scheme to
    whatever app registered it" — but only Android reads an empty string as
    absent (its driver appends the package under a truthiness check). iOS
    forwards the value verbatim to WebDriverAgent, which asks the system for an
    app named "" and is told there is no such app, so every deeplink failed
    there with an error naming an empty bundle id.
    """
    def open_deeplink(driver, url: str, package: str = "") -> None:
        params = {"url": url}
        target = package or _config.get("app_id") or ""
        if target:
            params[app_key] = target
        driver.execute_script("mobile: deepLink", params)
    return open_deeplink


_adapters.register("deeplink", {
    "android": {"open": _deeplink("package")},
    "ios": {"open": _deeplink("bundleId")},
})


def navigate(driver, url: str, *, package: str = "", description: str = "") -> None:
    """Route a navigate verb to an app switch, BACK, or a deeplink.

    Dispatch is on the resolved url value, so {{var}} templates are substituted
    first — the routing decision itself depends on the resolved content.

    Deeplinks resolve through the "deeplink" adapter registry. Both platforms
    serve the Appium "mobile: deepLink" script and disagree only on what the
    target app is called in the payload — Android's "package", iOS's "bundleId" —
    so each row differs by a key name rather than a code path.

    "back" is Android-only, and not because the route is unfinished: iOS has no
    system back key at all. Going back there is a navigation-bar button or an edge
    swipe, both ordinary elements the agent already sees, so the key lookup
    refuses and names what iOS does have.

    Args:
        driver: Live Appium webdriver session.
        url: "app://<app_id>", the literal "back" (case-insensitive), or a
            deeplink URL. May contain {{var}} templates.
        package: Optional explicit Android package for a deeplink; defaults to
            the configured app_id. Ignored for the "app://" and "back" routes.
        description: Optional human-readable label for the INFO log line.

    Raises:
        ValueError: "app://" scheme with no app id and no configured fallback.
        UnknownKeyEvent: "back" requested on a platform with no back key.
        UnsupportedOnPlatform: deeplink navigation on an unshipped platform.
    """
    resolved = str(var(url))
    suffix = f" — {description}" if description else ""

    if resolved.lower().startswith(_APP_SCHEME):
        app_id = resolved[len(_APP_SCHEME):].strip("/") or _config.get("app_id") or ""
        if not app_id:
            raise ValueError(
                "navigate('app://') needs an app id; none in the url and no "
                "app_id configured"
            )
        driver.activate_app(app_id)
        _log.info("navigate: activated app %s%s", app_id, suffix)
        return

    if resolved.strip().lower() == "back":
        keyevent(driver, "BACK", description=description)
        return

    open_deeplink = _adapters.adapter("deeplink", "open", "deeplink navigation")
    open_deeplink(driver, resolved, str(var(package)) if package else "")
    _log.info("navigate: deeplink %s%s", resolved, suffix)
