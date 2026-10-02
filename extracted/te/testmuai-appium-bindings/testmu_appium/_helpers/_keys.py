"""Semantic key name → the platform's own key token, as per-platform data tables.

The generated test.py carries the semantic name ("BACK", "ENTER"); what that name
means to the device is resolved here, so one recording replays on either platform
without a re-export. A platform is activated by filling two rows: its keycode
table below, and its "key_dispatch" adapter row.

The two platforms do not agree on what a key IS. Android has a numeric keycode
space and one call that takes it. iOS has neither: a key is a named hardware
button or a character delivered to the focused element. So a table row holds
whatever its platform dispatches — an int for Android, an _IosKey for iOS — and
only this module ever interprets it.
"""
from typing import Mapping, NamedTuple

from testmu_appium._errors import UnknownKeyEvent, UnsupportedOnPlatform
from testmu_appium._helpers import _adapters

#: Android KeyEvent constants for the key names the recorder emits.
_ANDROID = {
    "HOME": 3,
    "BACK": 4,
    "CALL": 5,
    "ENDCALL": 6,
    "VOLUME_UP": 24,
    "VOLUME_DOWN": 25,
    "POWER": 26,
    "CAMERA": 27,
    "TAB": 61,
    "SPACE": 62,
    "ENTER": 66,
    "DELETE": 67,
    "MENU": 82,
    "SEARCH": 84,
    "MEDIA_PLAY_PAUSE": 85,
    "PAGE_UP": 92,
    "PAGE_DOWN": 93,
    "FORWARD_DEL": 112,
    "MOVE_HOME": 122,
    "MOVE_END": 123,
    "RECENT": 187,
    "BRIGHTNESS_DOWN": 220,
    "BRIGHTNESS_UP": 221,
    "PASTE": 279,
}

#: Legacy/alternate spellings that map onto a canonical name. Kept small and explicit
#: — an alias is a rename, never a new capability. ESCAPE and ESC are the semantic
#: dismiss key, which Android serves with the BACK keycode.
_ALIASES = {
    "APP_SWITCH": "RECENT",
    "RECENT_APPS": "RECENT",
    "GO_BACK": "BACK",
    "BACKSPACE": "DELETE",
    "DEL": "DELETE",
    "RETURN": "ENTER",
    "ESCAPE": "BACK",
    "ESC": "BACK",
}

class _IosKey(NamedTuple):
    """How iOS delivers a key.

    iOS has no keycode space: there is no equivalent of `android.view.KeyEvent`,
    and nothing that takes a number. A key is either a physical button the device
    exposes, or a character handed to whatever currently holds focus. The row
    carries which of the two it is, because the dispatch differs.

    Logged via ``%s``, so the tuple repr is the diagnostic — it escapes the
    control characters that a bare value would print raw into the log line.
    """

    kind: str  # "button" | "text"
    value: str


#: The keys an iOS device can actually be asked for. Deliberately much smaller
#: than the Android column, and the absences are the design rather than an
#: unfinished table:
#:
#: - BACK has no iOS equivalent at all. There is no system back key; going back
#:   is a navigation-bar button or an edge swipe, both of which are ordinary
#:   elements the agent can already see and act on. Aliasing it onto something
#:   would silently do the wrong thing on every screen where the guess is wrong.
#: - MENU / SEARCH / RECENT / POWER / CAMERA are Android hardware or system
#:   affordances with no counterpart.
#: - ESCAPE / PAGE_UP / PAGE_DOWN / MOVE_HOME / MOVE_END exist only on a hardware
#:   keyboard, which a phone under test does not have.
#:
#: A name absent here raises UnknownKeyEvent naming the iOS table, so the caller
#: is told what IS available rather than getting a no-op.
_IOS: dict[str, _IosKey] = {
    "HOME": _IosKey("button", "home"),
    "VOLUME_UP": _IosKey("button", "volumeUp"),
    "VOLUME_DOWN": _IosKey("button", "volumeDown"),
    "ENTER": _IosKey("text", "\n"),
    "TAB": _IosKey("text", "\t"),
    "SPACE": _IosKey("text", " "),
    "DELETE": _IosKey("text", "\b"),
}

#: platform → key name → the token that platform dispatches. Android's token is
#: its numeric keycode; iOS's is an _IosKey. Nothing outside this module reads
#: the token except to log it, which is what lets the two shapes coexist.
#: Mapping, not dict, because dict's value type is invariant: the Android column
#: is dict[str, int] and the iOS one dict[str, _IosKey], and neither is a
#: dict[str, int | _IosKey]. Reading is all this module does with them.
_TABLES: Mapping[str, Mapping[str, "int | _IosKey"]] = {
    "android": _ANDROID,
    "ios": _IOS,
}


def _table(platform: str) -> Mapping[str, "int | _IosKey"]:
    platform = (platform or "").lower()
    if platform not in _TABLES:
        raise UnsupportedOnPlatform(f"key events for platform {platform!r}", platform)
    table = _TABLES[platform]
    if not table:
        raise UnsupportedOnPlatform(f"{platform} key table not shipped", platform)
    return table


def known_keys(platform: str) -> set:
    """The key names this binding can resolve for the given platform."""
    return set(_table(platform))


def keycode(name: str | int, platform: str) -> "int | _IosKey":
    """Resolve a key name, or an Android numeric code, to a dispatch token.

    Named for Android's keycode because that is what it returns there and what
    every caller predating iOS expects. On iOS the token is an _IosKey — the
    platform has no code space to return.
    """
    table = _table(platform)
    # Recorded Android key events may carry raw codes, including codes without
    # a semantic alias. Leave interpretation of those codes to Android/Appium.
    if (platform or "").lower() == "android":
        if type(name) is int and name >= 0:
            return name
        if isinstance(name, str):
            numeric = name.strip()
            if numeric.isascii() and numeric.isdigit():
                return int(numeric)
    canonical = str(name or "").strip().upper()
    canonical = _ALIASES.get(canonical, canonical)
    if canonical not in table:
        raise UnknownKeyEvent(str(name), platform, table)
    return table[canonical]


def _android_dispatch(driver, code: int) -> None:
    driver.press_keycode(code)


def _ios_dispatch(driver, key: _IosKey) -> None:
    """Press a hardware button, or hand a character to whatever holds focus.

    Both are driver-level: this verb resolves no selector and finds no element,
    so the text form goes through the session's own key entry rather than an
    element's send_keys, which would need a focus target the caller never gave us.
    """
    if key.kind == "button":
        driver.execute_script("mobile: pressButton", {"name": key.value})
        return
    # `mobile: keys` is not served by every WebDriverAgent build — the one this
    # was verified against answers "Unhandled endpoint". W3C key actions carry
    # no element, so they go wherever the OS is directing keystrokes — which is
    # also the ONLY route that reaches a focused WKWebView field: XCUITest only
    # knows native focus, so `switch_to.active_element` raises NoSuchElement for
    # a caret the page holds, and a search that typed its text web-safe then
    # lost its ENTER here, on the very field it had just filled.
    from selenium.webdriver.common.action_chains import ActionChains  # noqa: PLC0415

    ActionChains(driver).send_keys(key.value).perform()


_adapters.register("key_dispatch", {
    "android": {"press": _android_dispatch},
    "ios": {"press": _ios_dispatch},
})


def dispatch(driver, name: str | int, platform: str) -> "int | _IosKey":
    """Resolve and execute a semantic key through the platform adapter seam.

    Returns the token that was dispatched, for the caller's log line only — an
    int on Android, an _IosKey on iOS.
    """
    code = keycode(name, platform)
    press = _adapters.adapter("key_dispatch", "press", "key event dispatch", platform=platform)
    press(driver, code)
    return code
