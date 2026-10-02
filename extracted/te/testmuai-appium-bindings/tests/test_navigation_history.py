"""Surface-aware native and mobile-web history navigation."""
import pytest

from testmu_appium import _action_web, _config
from testmu_appium._errors import UnsupportedOnPlatform, WebSurfaceUnavailable
from testmu_appium._helpers import _web
from testmu_appium._helpers.navigation_history import go_back, go_forward


class _Driver:
    current_package = "com.android.chrome"

    def __init__(self):
        self.pressed = []

    def press_keycode(self, code):
        self.pressed.append(code)


class _Channel(_web.Channel):
    """A recording wire UNDER the real Channel: the verb goes through the
    genuine ``navigate_history``, and the assertions keep pinning the exact
    CDP calls it makes."""

    def __init__(self, current=1, entries=None):
        self.current = current
        self.entries = entries or [{"id": 10}, {"id": 20}, {"id": 30}]
        self.calls = []

    def call(self, method, params=None):
        self.calls.append((method, params))
        if method == "Page.getNavigationHistory":
            return {"currentIndex": self.current, "entries": self.entries}
        return {}


@pytest.fixture(autouse=True)
def _android(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")


def _use(monkeypatch, channel):
    seen = []

    def visible(package):
        seen.append(package)
        return channel

    monkeypatch.setattr(_action_web, "visible_channel", visible)
    return seen


def test_native_go_back_presses_device_back_without_opening_web(monkeypatch):
    monkeypatch.setattr(
        _action_web,
        "visible_channel",
        lambda package: pytest.fail("native BACK must not open a web channel"),
    )
    driver = _Driver()

    go_back(driver, surface="native")

    assert driver.pressed == [4]


def test_native_go_forward_is_explicitly_unsupported(monkeypatch):
    monkeypatch.setattr(
        _action_web,
        "visible_channel",
        lambda package: pytest.fail("native forward must not open a web channel"),
    )
    driver = _Driver()

    with pytest.raises(UnsupportedOnPlatform) as exc:
        go_forward(driver, surface="native")

    assert "native surface" in str(exc.value)
    assert driver.pressed == []


@pytest.mark.parametrize("verb,target_id", [
    (go_back, 10),
    (go_forward, 30),
])
def test_web_navigation_moves_to_adjacent_cdp_history_entry(
        monkeypatch, verb, target_id):
    channel = _Channel()
    seen = _use(monkeypatch, channel)
    driver = _Driver()

    verb(driver, surface="web")

    assert seen == ["com.android.chrome"]
    assert channel.calls == [
        ("Page.getNavigationHistory", None),
        ("Page.navigateToHistoryEntry", {"entryId": target_id}),
    ]
    assert driver.pressed == []


@pytest.mark.parametrize("verb,current", [
    (go_back, 0),
    (go_forward, 2),
])
def test_web_history_boundary_is_a_successful_no_op(monkeypatch, verb, current):
    channel = _Channel(current=current)
    _use(monkeypatch, channel)
    driver = _Driver()

    verb(driver, surface="web")

    assert channel.calls == [("Page.getNavigationHistory", None)]
    assert driver.pressed == []


@pytest.mark.parametrize("verb", [go_back, go_forward])
def test_missing_web_channel_fails_closed_without_native_fallback(
        monkeypatch, verb):
    monkeypatch.setattr(_action_web, "visible_channel", lambda package: None)
    driver = _Driver()

    with pytest.raises(WebSurfaceUnavailable) as exc:
        verb(driver, surface="web")

    assert "visible debuggable mobile web surface" in str(exc.value)
    assert driver.pressed == []


@pytest.mark.parametrize("verb", [go_back, go_forward])
def test_unknown_surface_is_rejected_before_any_action(monkeypatch, verb):
    monkeypatch.setattr(
        _action_web,
        "visible_channel",
        lambda package: pytest.fail("invalid surface must not open a web channel"),
    )
    driver = _Driver()

    with pytest.raises(ValueError) as exc:
        verb(driver, surface="hybrid")

    assert "hybrid" in str(exc.value)
    assert driver.pressed == []
