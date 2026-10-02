"""Semantic key name → platform keycode tables."""
import pytest

from testmu_appium._errors import UnknownKeyEvent, UnsupportedOnPlatform
from testmu_appium._helpers import _keys


#: EVERY row of the Android table, with the value from
#: android.view.KeyEvent. A wrong keycode is invisible in a passing test — the
#: driver dispatches it happily and the app just does something else — so the table
#: is pinned in full rather than sampled.
ANDROID_KEYCODES = {
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

#: Every alias row, with the canonical name it resolves to.
ANDROID_ALIASES = {
    "APP_SWITCH": "RECENT",
    "RECENT_APPS": "RECENT",
    "GO_BACK": "BACK",
    "BACKSPACE": "DELETE",
    "DEL": "DELETE",
    "RETURN": "ENTER",
    "ESCAPE": "BACK",
    "ESC": "BACK",
}


@pytest.mark.parametrize("name,code", sorted(ANDROID_KEYCODES.items()))
def test_android_keycodes(name, code):
    assert _keys.keycode(name, "android") == code


def test_the_pin_covers_the_whole_table():
    """Guards the guard: a keycode added without a pin fails here, not in the field."""
    assert _keys.known_keys("android") == set(ANDROID_KEYCODES)


def test_keycodes_are_unique():
    """Two names sharing a code is almost always a copy-paste in the table."""
    assert len(set(ANDROID_KEYCODES.values())) == len(ANDROID_KEYCODES)


def test_key_names_are_case_insensitive():
    assert _keys.keycode("back", "android") == _keys.keycode("BACK", "android")


@pytest.mark.parametrize("alias,canonical", sorted(ANDROID_ALIASES.items()))
def test_key_name_aliases_resolve(alias, canonical):
    """The generator emits semantic names; a few legacy spellings alias onto them.
    An alias is a RENAME, never a new capability — so each must land on a name the
    table already has."""
    assert canonical in ANDROID_KEYCODES
    assert _keys.keycode(alias, "android") == ANDROID_KEYCODES[canonical]


def test_the_alias_pin_covers_every_alias():
    assert set(_keys._ALIASES) == set(ANDROID_ALIASES)


@pytest.mark.parametrize("alias", sorted(ANDROID_ALIASES))
def test_aliases_are_case_insensitive_too(alias):
    assert _keys.keycode(alias.lower(), "android") == _keys.keycode(alias, "android")


def test_no_alias_shadows_a_real_key_name():
    """An alias that collided with a table row would silently redirect it."""
    assert not (set(ANDROID_ALIASES) & set(ANDROID_KEYCODES))


@pytest.mark.parametrize("name", ["ESCAPE", "ESC"])
def test_escape_replays_as_the_back_keycode(name):
    """Recorded artifacts carry the semantic ESCAPE; Android serves it with BACK."""
    assert _keys.keycode(name, "android") == _keys.keycode("BACK", "android") == 4


@pytest.mark.parametrize("name", ["  BACK  ", "\tenter\n"])
def test_surrounding_whitespace_is_tolerated(name):
    assert _keys.keycode(name, "android") == ANDROID_KEYCODES[name.strip().upper()]


def test_unknown_key_raises_with_the_known_set():
    with pytest.raises(UnknownKeyEvent) as exc:
        _keys.keycode("SIRI", "android")
    assert "SIRI" in str(exc.value)
    assert "BACK" in str(exc.value)


#: EVERY row of the iOS table. Pinned in full for the same reason as Android: a
#: wrong button name or character is dispatched happily and the device just does
#: something else. `kind` is pinned too, because it selects the dispatch.
IOS_KEYS = {
    "HOME": ("button", "home"),
    "VOLUME_UP": ("button", "volumeUp"),
    "VOLUME_DOWN": ("button", "volumeDown"),
    "ENTER": ("text", "\n"),
    "TAB": ("text", "\t"),
    "SPACE": ("text", " "),
    "DELETE": ("text", "\b"),
}


@pytest.mark.parametrize("name,expected", sorted(IOS_KEYS.items()))
def test_ios_keys(name, expected):
    assert _keys.keycode(name, "ios") == _keys._IosKey(*expected)


def test_the_ios_pin_covers_the_whole_table():
    assert _keys.known_keys("ios") == set(IOS_KEYS)


def test_ios_has_no_back_key_and_says_so():
    """BACK is absent BY DESIGN, and the error has to say that clearly.

    iOS has no system back key: going back is a navigation-bar button or an edge
    swipe, both ordinary elements the agent can already see. The failure must name
    the key and list what iOS does have — UnknownKeyEvent — rather than
    UnsupportedOnPlatform, which would read as "iOS keys aren't built yet".
    """
    with pytest.raises(UnknownKeyEvent) as exc:
        _keys.keycode("BACK", "ios")
    assert "BACK" in str(exc.value)
    assert "HOME" in str(exc.value)


def test_ios_aliases_still_resolve():
    """The alias table is platform-neutral, so the ones landing on an iOS row work."""
    assert _keys.keycode("RETURN", "ios") == _keys.keycode("ENTER", "ios")
    assert _keys.keycode("BACKSPACE", "ios") == _keys.keycode("DELETE", "ios")


class _Focus:
    def __init__(self, sink):
        self._sink = sink

    def send_keys(self, text):
        self._sink.append(str(text))


class _SwitchTo:
    def __init__(self, sink):
        self.active_element = _Focus(sink)


class _RecordingDriver:
    def __init__(self):
        self.scripts = []
        self.typed = []
        self.switch_to = _SwitchTo(self.typed)

    def execute_script(self, name, args=None):
        self.scripts.append((name, args))


def test_ios_dispatch_presses_a_hardware_button():
    driver = _RecordingDriver()
    _keys.dispatch(driver, "VOLUME_UP", "ios")
    assert driver.scripts == [("mobile: pressButton", {"name": "volumeUp"})]


def test_ios_dispatch_sends_a_character_through_w3c_actions(monkeypatch):
    """A text key resolves no element, so it rides W3C key actions — the one
    route that reaches BOTH a native field and a focused WKWebView field.
    `switch_to.active_element` raises NoSuchElement for a caret the page
    holds, which lost a web search its ENTER on the field it had just filled."""
    sent = []

    class _Chains:
        def __init__(self, driver):
            pass

        def send_keys(self, value):
            sent.append(value)
            return self

        def perform(self):
            sent.append("performed")

    monkeypatch.setattr(
        "selenium.webdriver.common.action_chains.ActionChains", _Chains)
    driver = _RecordingDriver()
    _keys.dispatch(driver, "ENTER", "ios")
    assert sent == ["\n", "performed"]
    assert driver.scripts == []
    assert driver.typed == [], "the native active element must not be asked"


def test_unknown_platform_raises():
    with pytest.raises(UnsupportedOnPlatform):
        _keys.keycode("BACK", "tizen")


def test_known_keys_lists_the_android_column():
    known = _keys.known_keys("android")
    assert "ENTER" in known and "RECENT" in known
