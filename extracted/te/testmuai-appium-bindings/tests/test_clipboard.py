"""Android plain-text clipboard driver verbs."""
import pytest

from testmu_appium import _config, _vars
from testmu_appium._errors import UnsupportedOnPlatform
from testmu_appium._helpers.clipboard import (
    clear_clipboard,
    paste_clipboard,
    set_clipboard,
)


class _Driver:
    def __init__(self):
        self.clipboard_writes = []
        self.pressed = []

    def set_clipboard_text(self, text):
        self.clipboard_writes.append(text)

    def press_keycode(self, code):
        self.pressed.append(code)


@pytest.fixture(autouse=True)
def _android_and_clear_vars(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    yield
    _vars.clear_state()


def test_set_clipboard_resolves_runtime_variable_as_plain_text():
    _vars.set_var("copied", 12345)
    driver = _Driver()

    set_clipboard(driver, "{{copied}}")

    assert driver.clipboard_writes == ["12345"]
    assert driver.pressed == []


def test_paste_clipboard_uses_android_paste_key_without_reading_clipboard():
    driver = _Driver()

    paste_clipboard(driver)

    assert driver.pressed == [279]
    assert driver.clipboard_writes == []


def test_clear_clipboard_replaces_content_with_empty_text():
    driver = _Driver()

    clear_clipboard(driver)

    assert driver.clipboard_writes == [""]


@pytest.mark.parametrize("verb,args,written", [
    (set_clipboard, ("text",), "text"),
    (clear_clipboard, (), ""),
])
def test_writing_the_clipboard_works_on_ios(monkeypatch, verb, args, written):
    """Writing is one W3C endpoint both platforms serve."""
    monkeypatch.setitem(_config._config, "platform", "ios")
    driver = _Driver()

    verb(driver, *args)

    assert driver.clipboard_writes == [written]


def test_pasting_is_refused_on_ios(monkeypatch):
    """Pasting is NOT symmetric with writing, which is why the two are gated apart.

    iOS has no paste key, and cmd+V only reaches an app with a hardware keyboard
    attached. The iOS way is to long-press the field and tap "Paste" — ordinary
    elements the agent can already see — so refusing here sends it down a path
    that works instead of silently doing nothing.
    """
    monkeypatch.setitem(_config._config, "platform", "ios")
    driver = _Driver()

    with pytest.raises(UnsupportedOnPlatform) as exc:
        paste_clipboard(driver)

    assert "ios" in str(exc.value)
    assert driver.pressed == []


@pytest.mark.parametrize("verb,args", [
    (set_clipboard, ("text",)),
    (paste_clipboard, ()),
    (clear_clipboard, ()),
])
def test_clipboard_verbs_fail_loudly_on_an_unshipped_platform(monkeypatch, verb, args):
    monkeypatch.setitem(_config._config, "platform", "tizen")
    driver = _Driver()

    with pytest.raises(UnsupportedOnPlatform) as exc:
        verb(driver, *args)

    assert "tizen" in str(exc.value)
    assert driver.clipboard_writes == []
    assert driver.pressed == []
