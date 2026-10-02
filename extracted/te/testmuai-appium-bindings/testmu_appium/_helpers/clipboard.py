"""OS clipboard driver verbs.

Each verb resolves its platform's adapter from the "clipboard" registry. Writing
is one W3C endpoint both platforms serve, so android and ios share those rows.
Pasting is not symmetric: Android has a PASTE key event and iOS has nothing
equivalent, so the ios row simply has no "paste" entry and that verb alone raises.

iOS caveat worth knowing before relying on this: the pasteboard is read and written
through WebDriverAgent, and iOS only grants pasteboard access to the foreground
app. A value written here reaches the app under test in the ordinary case, but a
system prompt or an app switch between the write and the paste can lose it.
"""
import logging

from testmu_appium._helpers import _adapters
from testmu_appium._helpers.keyevent import keyevent
from testmu_appium._vars import var

_log = logging.getLogger("testmu_appium")

#: Platforms whose driver serves the W3C set/get pasteboard endpoints.
_WRITES_CLIPBOARD = frozenset({"android", "ios"})

def _android_set_text(driver, text: str) -> None:
    driver.set_clipboard_text(text)


def _android_paste(driver, description: str) -> None:
    keyevent(driver, "PASTE", description=description)


def _android_clear(driver) -> None:
    driver.set_clipboard_text("")


#: `set_clipboard_text` is the W3C endpoint, served identically by both drivers, so
#: iOS reuses those rows outright. There is deliberately no ios "paste": no paste
#: key exists, and cmd+V only reaches an app with a hardware keyboard attached. The
#: iOS way is to long-press the field and tap "Paste" — ordinary elements the agent
#: already sees — so refusing sends the caller down a path that works.
_adapters.register("clipboard", {
    "android": {
        "set_text": _android_set_text,
        "paste": _android_paste,
        "clear": _android_clear,
    },
    "ios": {
        "set_text": _android_set_text,
        "clear": _android_clear,
    },
})


def set_clipboard(driver, text, *, description: str = "") -> None:
    """Replace the plain-text clipboard with ``text``.

    Resolution happens here so a value produced by an earlier generated step is
    read at replay time rather than frozen into the exported test.
    """
    write = _adapters.adapter("clipboard", "set_text", "set_clipboard")
    write(driver, str(var(text)))
    suffix = f" — {description}" if description else ""
    _log.info("set_clipboard: wrote plain text%s", suffix)


def paste_clipboard(driver, *, description: str = "") -> None:
    """Paste at the focused editable control without reading clipboard content."""
    paste = _adapters.adapter("clipboard", "paste", "paste_clipboard")
    paste(driver, description)
    suffix = f" — {description}" if description else ""
    _log.info("paste_clipboard%s", suffix)


def clear_clipboard(driver, *, description: str = "") -> None:
    """Clear the plain-text clipboard."""
    clear = _adapters.adapter("clipboard", "clear", "clear_clipboard")
    clear(driver)
    suffix = f" — {description}" if description else ""
    _log.info("clear_clipboard%s", suffix)
