"""How big the screen is, however this driver will admit to it.

`driver.get_window_size()` is the W3C way and the only one needed on Android. It
is NOT universal on iOS, and the reason is worth stating precisely, because the
obvious diagnosis is wrong: it is not a WebDriverAgent limitation. WDA serves
the screen size perfectly well. What changed is the CLIENT.

    appium-xcuitest-driver 7.x   getWindowRect -> proxies GET /window/size  -> 200
    appium-xcuitest-driver 9.x   getWindowRect -> proxies GET /window/rect  -> 404

WDA never implemented `/window/rect`, so on a 9.x driver the standard call dies
with `Unhandled endpoint` against the SAME agent that answers 7.x. The Appium
server version is identical either way — the driver is versioned separately, so
"same Appium" does not mean "same behaviour here".

Two other routes to the same number survive on 9.x, so nothing is actually lost:

    mobile: deviceScreenInfo -> /wda/screen -> {"screenSize": {...}, "scale": 2}
    the page source's root element, which spans the screen

The routes are tried in the PLATFORM'S OWN order. Android asks the spec route
first — `deviceScreenInfo` is an XCUITest extension UiAutomator2 refuses, so
the standard is both correct and the only cheap route there. iOS asks
`deviceScreenInfo` first: the spec route on a 9.x driver is a GUARANTEED
failed round trip plus a warning at every session start, while /wda/screen
answers on 7.x and 9.x alike; the spec route stays second so a driver that
reinstates the standard is still reachable. The document is last on both —
fetching an entire element tree to read two attributes is paid only when the
cheap routes are gone.

`scale` is the points-to-PIXELS ratio and is deliberately not returned. iOS
coordinates are points end to end: Appium taps in points, the element tree is in
points, and a CSS pixel IS a point. Multiplying by scale here would double every
coordinate on a 2x device.

Which route works is a property of the SESSION, not of the call, so the winner
is remembered: without that every consumer pays up to two failing round trips
before falling back, on every action.
"""

import logging
import xml.etree.ElementTree as ET

from testmu_appium._helpers import _adapters

_log = logging.getLogger("testmu_appium")

#: session id -> name of the reader that answered for it. Keyed by session so a
#: later session on a newer driver is not punished for this one's limits.
_CHOSEN: dict[str, str] = {}


def reset() -> None:
    """Forget what past sessions settled on. Called at session start."""
    _CHOSEN.clear()


def _session_id(driver) -> str:
    return str(getattr(driver, "session_id", "") or "")


def _from_w3c(driver) -> tuple[int, int]:
    """The standard route. Present on Android and on xcuitest-driver 7.x."""
    size = driver.get_window_size()
    return int(size["width"]), int(size["height"])


def _from_screen_info(driver) -> tuple[int, int]:
    """`mobile: deviceScreenInfo`, which reaches WDA's own /wda/screen.

    Returns statusBarSize and scale alongside screenSize; only screenSize is the
    whole screen, and only it is read here.
    """
    info = driver.execute_script("mobile: deviceScreenInfo") or {}
    screen = info.get("screenSize") or {}
    width, height = int(screen.get("width") or 0), int(screen.get("height") or 0)
    if not (width and height):
        raise RuntimeError(f"deviceScreenInfo carried no screenSize: {info!r}")
    return width, height


def _from_page_source(driver) -> tuple[int, int]:
    """Last resort: the document's root spans the screen.

    Only a node with NON-ZERO dimensions counts. A zero-sized first match is a
    real thing a mid-transition capture can produce, and answering (0, 0) here
    poisons every ratio computed against it.
    """
    root = ET.fromstring(driver.page_source)
    for node in root.iter():
        try:
            width = int(float(node.get("width") or 0))
            height = int(float(node.get("height") or 0))
        except (TypeError, ValueError):
            continue
        if width > 0 and height > 0:
            return width, height
    raise RuntimeError(
        "the driver reported no window size and the page source carries no "
        "non-zero sized root; nothing can be measured against this screen")


#: Every route by name; the ORDER they are asked in is the platform row below.
_READER_FNS = {
    "w3c": _from_w3c,
    "screen_info": _from_screen_info,
    "page_source": _from_page_source,
}

# The module docstring carries the full reasoning; in short: the spec route is
# Android's only cheap answer, and iOS 9.x's guaranteed failure.
_adapters.register("screen", {
    "android": {
        "reader_order": lambda: ("w3c", "screen_info", "page_source"),
    },
    "ios": {
        "reader_order": lambda: ("screen_info", "w3c", "page_source"),
    },
})


def _reader_order(platform=None):
    return _adapters.adapter(
        "screen", "reader_order", "screen size reading", platform=platform)()


def window_size(driver, platform=None) -> tuple[int, int]:
    """The screen's (width, height) in the driver's own units.

    Points on iOS, device pixels on Android — the caller's coordinates are in the
    same unit either way, which is the whole reason this returns the driver's
    number rather than converting to one.

    ``platform`` overrides the configured one for THIS read. The first read of
    a run happens when the device session opens — before the consumer has
    called ``configure(platform=...)`` — and resolving from config at that
    moment answers with the default, not the session's platform. A caller that
    knows its platform says so; ``None`` keeps the configured resolution.
    """
    session = _session_id(driver)
    chosen = _CHOSEN.get(session)
    if chosen:
        return _READER_FNS[chosen](driver)

    failures = []
    for name in _reader_order(platform):
        try:
            size = _READER_FNS[name](driver)
        except Exception as exc:  # noqa: BLE001 — an absent route is not fatal
            # The ORIGINAL message rides along, not just the type name. This
            # helper runs inside every capture, so it is often the FIRST place
            # a dying session is observed — and the runner classifies a dead
            # session by message substrings ("invalid session id", "socket
            # hang up"), none of which survive a bare type name. Swallowing
            # them here defeated the auto-reconnect built on those markers.
            failures.append(f"{name}: {type(exc).__name__}: {str(exc)[:160]}")
            continue
        if failures:
            _log.info(
                "[screen] %s answered the screen size for this session after %s",
                name, "; ".join(failures))
        # The winner is remembered so consumers stop paying failing round
        # trips — EXCEPT the document reader: it wins only when both cheap
        # routes failed, and a transient failure would otherwise pin a
        # whole-tree fetch onto every remaining size read of the session.
        # The cheap routes are re-offered on the next call instead.
        if name != "page_source":
            _CHOSEN[session] = name
        return size

    raise RuntimeError(
        "no route to this device's screen size — tried " + "; ".join(failures))
