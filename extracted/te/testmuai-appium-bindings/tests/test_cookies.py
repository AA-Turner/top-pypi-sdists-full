"""Mobile-web cookie verbs over the visible CDP channel."""
import pytest

from testmu_appium import _action_web, _vars
from testmu_appium._helpers import _web
from testmu_appium._errors import WebSurfaceUnavailable
from testmu_appium._helpers.cookies import (
    clear_cookies,
    delete_cookies,
    set_cookies,
)


class _Driver:
    current_package = "com.android.chrome"


class _Channel(_web.Channel):
    """A recording wire UNDER the real Channel: the cookie verbs go through the
    genuine get/set/delete/clear methods, and these assertions keep pinning the
    exact CDP payloads those methods emit."""

    def __init__(self, *, cookies=None, url="https://example.test/cart"):
        self.cookies = list(cookies or [])
        self.url = url
        self.calls = []
        self.evaluations = []

    def evaluate(self, expression):
        self.evaluations.append(expression)
        return self.url

    def call(self, method, params=None):
        self.calls.append((method, params))
        if method == "Storage.getCookies":
            return {"cookies": self.cookies}
        return {}


@pytest.fixture(autouse=True)
def _clear_vars():
    yield
    _vars.clear_state()


def _use(monkeypatch, channel):
    seen = []

    def visible(package):
        seen.append(package)
        return channel

    monkeypatch.setattr(_action_web, "visible_channel", visible)
    return seen


def test_set_cookies_scopes_unscoped_cookie_to_runtime_url(monkeypatch):
    channel = _Channel()
    seen = _use(monkeypatch, channel)

    set_cookies(_Driver(), [{"name": "session", "value": "abc"}])

    assert seen == ["com.android.chrome"]
    assert channel.evaluations == ["location.href"]
    assert channel.calls == [(
        "Network.setCookies",
        {"cookies": [{
            "name": "session",
            "value": "abc",
            "url": "https://example.test/cart",
        }]},
    )]


@pytest.mark.parametrize("scope", [
    {"url": "https://api.example.test/"},
    {"domain": ".example.test"},
    {"path": "/checkout"},
])
def test_set_cookies_preserves_any_explicit_scope_without_reading_url(
        monkeypatch, scope):
    channel = _Channel()
    _use(monkeypatch, channel)
    cookie = {"name": "session", "value": "abc", **scope}

    set_cookies(_Driver(), [cookie])

    assert channel.evaluations == []
    assert channel.calls == [(
        "Network.setCookies",
        {"cookies": [cookie]},
    )]


def test_set_cookies_resolves_value_at_replay_time(monkeypatch):
    channel = _Channel()
    _use(monkeypatch, channel)
    _vars.set_var("token", 12345)

    set_cookies(
        _Driver(),
        [{"name": "token", "value": "{{token}}", "secure": True}],
    )

    sent = channel.calls[0][1]["cookies"][0]
    assert sent["value"] == "12345"
    assert sent["secure"] is True


def test_set_cookies_does_not_mutate_the_recorded_cookie(monkeypatch):
    channel = _Channel()
    _use(monkeypatch, channel)
    cookie = {"name": "session", "value": "{{token}}"}

    set_cookies(_Driver(), [cookie])

    assert cookie == {"name": "session", "value": "{{token}}"}


def test_delete_cookies_deletes_every_matching_domain_and_path(monkeypatch):
    channel = _Channel(cookies=[
        {"name": "session", "domain": "a.example", "path": "/"},
        {
            "name": "session",
            "domain": "b.example",
            "path": "/cart",
            "partitionKey": {"topLevelSite": "https://shop.example"},
        },
        {"name": "keep", "domain": "a.example", "path": "/"},
    ])
    _use(monkeypatch, channel)

    delete_cookies(_Driver(), ["session"])

    assert channel.calls == [
        ("Storage.getCookies", None),
        ("Network.deleteCookies", {
            "name": "session", "domain": "a.example", "path": "/",
        }),
        ("Network.deleteCookies", {
            "name": "session",
            "domain": "b.example",
            "path": "/cart",
            "partitionKey": {"topLevelSite": "https://shop.example"},
        }),
    ]


def test_clear_cookies_uses_browser_cookie_command(monkeypatch):
    channel = _Channel()
    _use(monkeypatch, channel)

    clear_cookies(_Driver())

    assert channel.calls == [("Network.clearBrowserCookies", None)]


@pytest.mark.parametrize("verb,args", [
    (set_cookies, ([{"name": "a", "value": "b"}],)),
    (delete_cookies, (["a"],)),
    (clear_cookies, ()),
])
def test_cookie_verbs_fail_when_no_visible_web_channel(
        monkeypatch, verb, args):
    monkeypatch.setattr(_action_web, "visible_channel", lambda package: None)

    with pytest.raises(WebSurfaceUnavailable) as exc:
        verb(_Driver(), *args)

    assert "visible debuggable mobile web surface" in str(exc.value)
    assert "com.android.chrome" in str(exc.value)


def test_set_cookies_rejects_fields_outside_the_cdp_contract(monkeypatch):
    channel = _Channel()
    _use(monkeypatch, channel)

    with pytest.raises(ValueError) as exc:
        set_cookies(_Driver(), [{
            "name": "a", "value": "b", "unexpected": "ignored?",
        }])

    assert "unexpected" in str(exc.value)
    assert channel.calls == []
