"""Mobile-web refresh through the visible CDP channel."""
import pytest

from testmu_appium import _action_web
from testmu_appium._errors import WebSurfaceUnavailable
from testmu_appium._helpers.refresh import refresh


class _Driver:
    current_package = "com.android.chrome"

    def refresh(self):
        pytest.fail("refresh must not fall back to the native Appium context")


class _Channel:
    def __init__(self, error=None):
        self.calls = []
        self.error = error

    def call(self, method, params=None):
        self.calls.append((method, params))
        if self.error is not None:
            raise self.error
        return {}


def _use(monkeypatch, channel):
    seen = []

    def visible(package):
        seen.append(package)
        return channel

    monkeypatch.setattr(_action_web, "visible_channel", visible)
    return seen


def test_refresh_reloads_the_visible_page_without_native_fallback(monkeypatch):
    channel = _Channel()
    seen = _use(monkeypatch, channel)

    refresh(_Driver(), surface="web")

    assert seen == ["com.android.chrome"]
    assert channel.calls == [("Page.reload", None)]


def test_refresh_fails_closed_without_a_visible_channel(monkeypatch):
    monkeypatch.setattr(_action_web, "visible_channel", lambda package: None)

    with pytest.raises(WebSurfaceUnavailable) as exc:
        refresh(_Driver(), surface="web")

    assert "visible debuggable mobile web surface" in str(exc.value)
    assert "com.android.chrome" in str(exc.value)


def test_refresh_propagates_cdp_errors_without_native_fallback(monkeypatch):
    _use(monkeypatch, _Channel(RuntimeError("Page.reload failed")))

    with pytest.raises(RuntimeError, match="Page.reload failed"):
        refresh(_Driver(), surface="web")


@pytest.mark.parametrize("surface", ["native", "hybrid", "WEB", "", None])
def test_refresh_rejects_every_non_web_surface_before_channel_lookup(
        monkeypatch, surface):
    monkeypatch.setattr(
        _action_web,
        "visible_channel",
        lambda package: pytest.fail("invalid surface must not open CDP"),
    )

    with pytest.raises(ValueError, match="surface='web'"):
        refresh(_Driver(), surface=surface)
