"""Android Chrome tabs over the browser DevTools endpoint."""
from __future__ import annotations

import json
from urllib.parse import unquote

import pytest

import testmu_appium
from testmu_appium import _config
from testmu_appium import _action_web
from testmu_appium._errors import UnsupportedOnPlatform, WebSurfaceUnavailable
from testmu_appium._helpers import _tabs_android as tabs
from testmu_appium._helpers import _web
from testmu_appium._helpers.cookies import set_cookies
from testmu_appium._helpers.local_storage import set_local_storage
from testmu_appium._helpers.navigation_history import go_back, go_forward
from testmu_appium._helpers.refresh import refresh
from testmu_appium._vars import set_var


class _Driver:
    current_package = "com.android.chrome"
    session_id = "appium-session-1"


class _Backend:
    def __init__(self):
        self.targets = [
            {
                "id": "A",
                "url": "https://one.test/path?token=secret#fragment",
                "title": "One",
                "visible": True,
            },
            {
                "id": "B",
                "url": "https://two.test/",
                "title": "Two",
                "visible": False,
            },
        ]
        self.calls = []
        self.http_mutations = []
        self.target_transport = True
        self.close_target = True
        self.next_id = 1
        self.json_ids = {}
        self.json_available = True
        self.create_return_id = None
        self.discovery_extras = []

    def target(self, target_id):
        return next(
            (target for target in self.targets if target["id"] == target_id),
            None,
        )

    def activate(self, target_id):
        target = self.target(target_id)
        if target is None:
            raise RuntimeError("stale target")
        for candidate in self.targets:
            candidate["visible"] = candidate is target

    def close(self, target_id):
        target = self.target(target_id)
        if target is None:
            raise RuntimeError("stale target")
        self.targets.remove(target)

    def create(self, url):
        target_id = f"N{self.next_id}"
        self.next_id += 1
        self.targets.append(
            {"id": target_id, "url": url, "title": "", "visible": False}
        )
        self.activate(target_id)
        return target_id

    def channel(self):
        backend = self

        class _Channel(_web.Channel):
            # The real Channel over a scripted wire, so the cookie/history
            # verbs run their genuine channel methods down into `call`.
            def __init__(self, ws_url, websocket_module=None, timeout=3.0):
                self.ws_url = ws_url
                self.timeout = timeout

            def call(self, method, params=None):
                params = params or {}
                backend.calls.append((self.ws_url, method, dict(params)))
                if method == "Target.getTargets":
                    if not backend.target_transport:
                        raise RuntimeError("-32601 Method not found")
                    return {
                        "targetInfos": [
                            {
                                "targetId": target["id"],
                                "type": "tab",
                                "url": target["url"],
                                "title": target["title"],
                            }
                            for target in backend.targets
                        ]
                    }
                if method == "Target.createTarget":
                    created = backend.create(params["url"])
                    return {"targetId": backend.create_return_id or created}
                if method == "Target.activateTarget":
                    backend.activate(params["targetId"])
                    return {}
                if method == "Target.closeTarget":
                    if not backend.close_target:
                        raise RuntimeError("-32601 Method not found")
                    backend.close(params["targetId"])
                    return {"success": True}
                if method == "Page.getNavigationHistory":
                    return {
                        "currentIndex": 1,
                        "entries": [{"id": 10}, {"id": 11}, {"id": 12}],
                    }
                if method in {
                    "Network.setCookies",
                    "Page.reload",
                    "Page.navigateToHistoryEntry",
                }:
                    return {}
                raise AssertionError(method)

            def is_visible(self):
                target_id = self.ws_url.rsplit("/", 1)[-1]
                target = backend.target(target_id)
                if target is None:
                    raise RuntimeError("stale page websocket")
                return target["visible"]

            def call_function(self, function_declaration, arguments=()):
                backend.calls.append(
                    (
                        self.ws_url,
                        "Runtime.callFunctionOn",
                        {"arguments": arguments},
                    )
                )
                return None

        return _Channel

    def evaluate(self, browser_ws, target_id, expression, timeout=3.0):
        assert browser_ws == "ws://browser"
        assert expression == "document.visibilityState"
        target = self.target(target_id)
        if target is None:
            raise RuntimeError("stale Target-domain target")
        return "visible" if target["visible"] else "hidden"

    def discover(self, browser_ws, timeout=3.0):
        assert browser_ws == "ws://browser"
        return [
            {
                "targetId": target["id"],
                "type": "page",
                "url": target["url"],
                "title": target["title"],
            }
            for target in self.targets
        ] + list(self.discovery_extras)

    def read_json(self, port, path, timeout=8.0):
        assert port == 9222
        if path == "/json/version":
            return {
                "Android-Package": "com.android.chrome",
                "webSocketDebuggerUrl": "ws://browser",
            }
        if path == "/json":
            if not self.json_available:
                raise RuntimeError("/json unavailable")
            return [
                {
                    "id": self.json_ids.get(target["id"], target["id"]),
                    "type": "page",
                    "url": target["url"],
                    "title": target["title"],
                    "webSocketDebuggerUrl": f"ws://page/{target['id']}",
                }
                for target in self.targets
            ]
        raise AssertionError(path)

    def mutate_http(self, port, path, method="GET", timeout=8.0):
        assert port == 9222
        self.http_mutations.append((method, path))
        if path.startswith("/json/new?"):
            return {"id": self.create(unquote(path.partition("?")[2]))}
        if path.startswith("/json/activate/"):
            self.activate(unquote(path.rsplit("/", 1)[-1]))
            return "Target activated"
        if path.startswith("/json/close/"):
            self.close(unquote(path.rsplit("/", 1)[-1]))
            return "Target is closing"
        raise AssertionError(path)


@pytest.fixture
def backend(monkeypatch):
    backend = _Backend()
    monkeypatch.setattr(_config, "run_target", "local")
    monkeypatch.setitem(_config._config, "platform", "android")
    monkeypatch.setitem(_config._config, "udid", "device-1")
    monkeypatch.setattr(_web, "reachable", lambda: True)
    monkeypatch.setattr(
        _web,
        "sockets",
        lambda: [_web.Socket("chrome_devtools_remote", None, "browser")],
    )
    monkeypatch.setattr(_web, "forward", lambda socket: 9222)
    monkeypatch.setattr(_web, "Channel", backend.channel())
    monkeypatch.setattr(tabs, "_read_json", backend.read_json)
    monkeypatch.setattr(tabs, "_mutate_http", backend.mutate_http)
    monkeypatch.setattr(tabs, "_discover_target_infos", backend.discover)
    monkeypatch.setattr(tabs, "_evaluate_in_target", backend.evaluate)
    return backend


@pytest.fixture
def provider():
    return tabs.AndroidChromeTabProvider()


def test_inventory_is_stable_and_never_exposes_target_ids(provider, backend):
    first = provider.get_tabs(_Driver())
    backend.targets.reverse()
    backend.targets.append(
        {
            "id": "C",
            "url": "https://three.test/",
            "title": "Three",
            "visible": False,
        }
    )
    second = provider.get_tabs(_Driver())

    assert [tab["title"] for tab in first] == ["One", "Two"]
    assert [tab["title"] for tab in second] == ["One", "Two", "Three"]
    assert all(set(tab) == {"index", "url", "title", "active", "identifier"}
               for tab in second)
    assert "A" not in repr(second) and "B" not in repr(second)
    assert first[0]["identifier"] == "https://one.test/path"
    assert "secret" not in first[0]["identifier"]


def test_target_inventory_ignores_mismatched_json_id_namespace(
    provider, backend
):
    backend.targets[0]["id"] = "FA35BROWSER"
    backend.targets[1]["id"] = "FB36BROWSER"
    backend.json_ids = {
        "FA35BROWSER": "261",
        "FB36BROWSER": "259",
    }

    inventory = provider.get_tabs(_Driver())

    assert [tab["title"] for tab in inventory] == ["One", "Two"]
    assert [tab["active"] for tab in inventory] == [True, False]
    assert "FA35BROWSER" not in repr(inventory)
    assert "261" not in repr(inventory)


def test_target_transport_inventory_does_not_require_json_pages(
    provider, backend
):
    backend.json_available = False

    inventory = provider.get_tabs(_Driver())

    assert [tab["title"] for tab in inventory] == ["One", "Two"]
    assert _web.remembered_target() == ""


def test_json_correlation_filters_discovered_page_proxies(provider, backend):
    backend.discovery_extras = [
        {
            "targetId": "PAGE-PROXY",
            "type": "page",
            "url": "chrome-native://newtab/",
            "title": "New Tab",
        },
        {
            "targetId": "TAB-PROXY",
            "type": "tab",
            "url": "",
            "title": "",
        },
    ]

    inventory = provider.get_tabs(_Driver())

    assert [tab["title"] for tab in inventory] == ["One", "Two"]
    assert "PROXY" not in repr(inventory)


def test_exact_correlated_pages_use_direct_ws_not_proxy_attachment(
    provider, backend, monkeypatch
):
    backend.discovery_extras = [
        {
            "targetId": "PAGE-PROXY",
            "type": "page",
            "url": "chrome-native://newtab/",
            "title": "New Tab",
        }
    ]
    monkeypatch.setattr(
        tabs,
        "_evaluate_in_target",
        lambda *args, **kwargs: pytest.fail(
            "exact /json pages must use their direct page WebSocket"
        ),
    )

    inventory = provider.get_tabs(_Driver())

    assert [tab["title"] for tab in inventory] == ["One", "Two"]
    assert _web.remembered_target() == "ws://page/A"
    assert "PROXY" not in repr(inventory)


def test_browser_target_visibility_uses_one_flattened_attached_session(
    monkeypatch
):
    sent = []

    class _Connection:
        def send(self, payload):
            sent.append(json.loads(payload))

        def recv(self):
            request = sent[-1]
            if request["method"] == "Target.attachToTarget":
                return json.dumps(
                    {"id": request["id"], "result": {"sessionId": "child-1"}}
                )
            return json.dumps(
                {
                    "id": request["id"],
                    "result": {"result": {"value": "visible"}},
                }
            )

        def close(self):
            pass

    import websocket

    opened = {}

    def create_connection(url, **kwargs):
        opened.update(url=url, **kwargs)
        return _Connection()

    monkeypatch.setattr(websocket, "create_connection", create_connection)

    value = tabs._evaluate_in_target(
        "ws://browser", "TARGET-INTERNAL", "document.visibilityState",
        timeout=1.25,
    )

    assert value == "visible"
    assert sent == [
        {
            "id": 1,
            "method": "Target.attachToTarget",
            "params": {"targetId": "TARGET-INTERNAL", "flatten": True},
        },
        {
            "id": 2,
            "sessionId": "child-1",
            "method": "Runtime.evaluate",
            "params": {
                "expression": "document.visibilityState",
                "returnByValue": True,
            },
        },
    ]
    assert opened == {
        "url": "ws://browser",
        "timeout": 1.25,
        "suppress_origin": True,
    }


def test_discovery_collects_existing_targets_before_the_command_response(
    monkeypatch
):
    sent = []
    replies = [
        {
            "method": "Target.targetCreated",
            "params": {
                "targetInfo": {
                    "targetId": "259",
                    "type": "page",
                    "url": "https://background.test/",
                }
            },
        },
        {
            "method": "Target.targetCreated",
            "params": {
                "targetInfo": {
                    "targetId": "TAB-PROXY",
                    "type": "tab",
                    "url": "",
                }
            },
        },
        {"id": 1, "result": {}},
    ]

    class _Connection:
        def send(self, payload):
            sent.append(json.loads(payload))

        def recv(self):
            return json.dumps(replies.pop(0))

        def close(self):
            pass

    import websocket

    monkeypatch.setattr(
        websocket, "create_connection", lambda url, **kwargs: _Connection()
    )

    found = tabs._discover_target_infos("ws://browser", timeout=1.0)

    assert [target["targetId"] for target in found] == ["259", "TAB-PROXY"]
    assert sent == [
        {
            "id": 1,
            "method": "Target.setDiscoverTargets",
            "params": {"discover": True, "filter": [{}]},
        }
    ]


def test_closed_targets_are_removed_without_reordering_survivors(provider, backend):
    provider.get_tabs(_Driver())
    backend.close("A")
    backend.activate("B")

    inventory = provider.get_tabs(_Driver())

    assert [(tab["index"], tab["title"]) for tab in inventory] == [(0, "Two")]


def test_inventory_falls_back_to_a_unique_exact_title(provider, backend):
    for target in backend.targets:
        target["url"] = "about:blank"

    inventory = provider.get_tabs(_Driver())

    assert [tab["identifier"] for tab in inventory] == ["One", "Two"]


def test_inventory_returns_no_identifier_when_url_and_title_are_ambiguous(
    provider, backend
):
    for target in backend.targets:
        target["url"] = "about:blank"
        target["title"] = "New Tab"

    inventory = provider.get_tabs(_Driver())

    assert [tab["identifier"] for tab in inventory] == [None, None]


@pytest.mark.parametrize(
    "package",
    ["", "com.example.native", "com.example.webview"],
)
def test_native_or_webview_foreground_packages_are_rejected_without_cdp(
    provider, backend, monkeypatch, package
):
    driver = _Driver()
    monkeypatch.setattr(driver, "current_package", package)
    monkeypatch.setattr(
        _web, "sockets", lambda: pytest.fail("must not inspect sockets")
    )

    with pytest.raises(WebSurfaceUnavailable):
        provider.get_tabs(driver)


def test_cloud_sessions_are_rejected_without_adb(provider, backend, monkeypatch):
    monkeypatch.setattr(_web, "reachable", lambda: False)
    monkeypatch.setattr(
        _web, "sockets", lambda: pytest.fail("cloud must not inspect adb sockets")
    )

    with pytest.raises(WebSurfaceUnavailable):
        provider.get_tabs(_Driver())


def test_only_the_browser_socket_is_accepted(provider, backend, monkeypatch):
    monkeypatch.setattr(
        _web,
        "sockets",
        lambda: [_web.Socket("webview_devtools_remote_12", 12, "webview")],
    )

    with pytest.raises(WebSurfaceUnavailable):
        provider.get_tabs(_Driver())


def test_version_endpoint_must_name_the_foreground_chrome_package(
    provider, backend, monkeypatch
):
    original = backend.read_json

    def wrong_package(port, path, timeout=8.0):
        value = original(port, path, timeout)
        if path == "/json/version":
            value["Android-Package"] = "com.chrome.beta"
        return value

    monkeypatch.setattr(tabs, "_read_json", wrong_package)

    with pytest.raises(WebSurfaceUnavailable):
        provider.get_tabs(_Driver())


class TestIosTabs:
    """Tabs as the WebKit wire can serve them: LISTED, not driven. The iwdp
    endpoint enumerates every inspectable page and visibility marks the active
    one; creating, activating or closing a page has no protocol counterpart
    (Chrome's Target.createTarget/activateTarget/closeTarget), so the three
    mutations refuse with that reason rather than half-imitating a UI action."""

    @pytest.fixture(autouse=True)
    def _ios(self, monkeypatch):
        monkeypatch.setitem(_config._config, "platform", "ios")

    def test_get_tabs_lists_the_devices_pages(self, monkeypatch):
        from testmu_appium._helpers import _web_ios

        monkeypatch.setattr(_web_ios, "ensure_proxy", lambda *_a, **_k: 32000)
        monkeypatch.setattr(_web_ios, "list_targets", lambda _port: [
            {"webSocketDebuggerUrl": "ws://a", "title": "Cart",
             "url": "https://shop.example/cart"},
            {"webSocketDebuggerUrl": "ws://b", "title": "",
             "url": "https://news.example/"},
        ])
        visible = {"ws://a": True, "ws://b": False}

        class _Channel:
            def __init__(self, ws_url, **_kwargs):
                self._ws_url = ws_url

            def is_visible(self):
                return visible[self._ws_url]

        monkeypatch.setattr(_web_ios, "IosChannel", _Channel)
        tabs = testmu_appium.get_tabs(_Driver())
        assert tabs == [
            {"index": 0, "url": "https://shop.example/cart", "title": "Cart",
             "active": True, "identifier": "Cart"},
            {"index": 1, "url": "https://news.example/", "title": "",
             "active": False, "identifier": "https://news.example/"},
        ]

    def test_a_page_that_cannot_answer_is_not_active(self, monkeypatch):
        from testmu_appium._helpers import _web_ios

        monkeypatch.setattr(_web_ios, "ensure_proxy", lambda *_a, **_k: 32000)
        monkeypatch.setattr(_web_ios, "list_targets", lambda _port: [
            {"webSocketDebuggerUrl": "ws://gone", "title": "Stale", "url": "x"},
        ])

        class _Dead:
            def __init__(self, *_a, **_k):
                pass

            def is_visible(self):
                raise RuntimeError("socket closed")

        monkeypatch.setattr(_web_ios, "IosChannel", _Dead)
        (tab,) = testmu_appium.get_tabs(_Driver())
        assert tab["active"] is False

    @pytest.mark.parametrize("mutate", [
        lambda d: testmu_appium.new_tab(d, url="https://example.com"),
        lambda d: testmu_appium.switch_tab(d, index=1),
        lambda d: testmu_appium.close_tab(d, index=0),
    ], ids=["new", "switch", "close"])
    def test_mutations_refuse_naming_the_missing_protocol(self, mutate):
        with pytest.raises(UnsupportedOnPlatform) as error:
            mutate(_Driver())
        assert error.value.platform == "ios"
        assert "WebKit" in str(error.value)


def test_new_tab_resolves_runtime_variables_and_uses_target_transport(
    provider, backend
):
    set_var("base", "https://created.test")

    provider.new_tab(_Driver(), "{{base}}/landing?secret=1")

    create = next(call for call in backend.calls if call[1] == "Target.createTarget")
    assert create[2] == {
        "url": "https://created.test/landing?secret=1",
        "forTab": True,
    }
    assert provider.get_tabs(_Driver())[-1]["active"] is True
    assert _web.remembered_target().endswith("/N1")


def test_new_tab_defaults_to_about_blank(provider, backend):
    provider.new_tab(_Driver(), None)

    create = next(call for call in backend.calls if call[1] == "Target.createTarget")
    assert create[2] == {"url": "about:blank", "forTab": True}


def test_new_tab_confirms_the_new_discovered_page_not_the_proxy_return_id(
    provider, backend
):
    backend.create_return_id = "TAB-PROXY"

    result = provider.new_tab(_Driver(), "https://created.test/")

    assert result["url"] == "https://created.test/"
    assert result["active"] is True
    assert "TAB-PROXY" not in repr(result)


@pytest.mark.parametrize(
    "url",
    ["javascript:alert(1)", "file:///tmp/a", "about:config", "example.com"],
)
def test_new_tab_rejects_urls_outside_the_contract_before_cdp(
    provider, backend, url
):
    with pytest.raises(ValueError):
        provider.new_tab(_Driver(), url)

    assert backend.calls == []


def test_http_fallback_is_selected_before_mutation(provider, backend):
    backend.target_transport = False

    provider.new_tab(_Driver(), "https://created.test/")
    provider.switch_tab(_Driver(), index=0, title="https://one.test/path")

    assert ("PUT", "/json/new?https%3A%2F%2Fcreated.test%2F") \
        in backend.http_mutations
    assert ("GET", "/json/activate/A") in backend.http_mutations
    assert not any(method == "Target.createTarget" for _, method, _ in backend.calls)


def test_switch_uses_identifier_with_index_as_a_consistency_guard(
    provider, backend
):
    provider.switch_tab(
        _Driver(), index=1, title="https://two.test/"
    )

    assert backend.target("B")["visible"] is True
    assert _web.remembered_target().endswith("/B")
    assert _web.remembered_target("com.android.chrome").endswith("/B")

    with pytest.raises(RuntimeError, match="drifted"):
        provider.switch_tab(
            _Driver(), index=0, title="https://two.test/"
        )


def test_switch_resolves_identifier_variables_at_replay_time(provider, backend):
    set_var("tenant", "two")

    provider.switch_tab(
        _Driver(), index=1, title="https://{{tenant}}.test/"
    )

    assert backend.target("B")["visible"] is True


def test_web_verbs_immediately_after_switch_reach_the_new_target(
    provider, backend
):
    provider.switch_tab(
        _Driver(), index=1, title="https://two.test/"
    )
    first_followup = len(backend.calls)

    set_cookies(
        _Driver(),
        [{"name": "scope", "value": "two", "url": "https://two.test/"}],
    )
    set_local_storage(_Driver(), {"selected": "two"})
    refresh(_Driver(), surface="web")
    go_back(_Driver(), surface="web")
    go_forward(_Driver(), surface="web")

    followups = backend.calls[first_followup:]
    acted = [
        (ws_url, method)
        for ws_url, method, _ in followups
        if method in {
            "Network.setCookies",
            "Runtime.callFunctionOn",
            "Page.reload",
            "Page.getNavigationHistory",
            "Page.navigateToHistoryEntry",
        }
    ]
    assert acted
    assert all(ws_url == "ws://page/B" for ws_url, _ in acted)


def test_switch_fails_closed_on_ambiguous_identifier(provider, backend):
    backend.targets[1]["url"] = backend.targets[0]["url"]

    with pytest.raises(RuntimeError, match="multiple"):
        provider.switch_tab(
            _Driver(), index=0, title="https://one.test/path"
        )

    assert backend.target("A")["visible"] is True


def test_switch_fails_closed_when_the_recorded_identity_disappears(
    provider, backend
):
    with pytest.raises(RuntimeError, match="no open tabs"):
        provider.switch_tab(
            _Driver(), index=0, title="https://missing.test/"
        )

    assert backend.target("A")["visible"] is True


def test_close_active_activates_the_previous_logical_tab(provider, backend):
    backend.activate("B")

    provider.close_tab(_Driver(), index=1, title="https://two.test/")

    assert [target["id"] for target in backend.targets] == ["A"]
    assert backend.target("A")["visible"] is True
    assert any(
        method == "Target.activateTarget" and params == {"targetId": "A"}
        for _, method, params in backend.calls
    )


def test_close_active_index_zero_activates_the_next_tab(provider, backend):
    provider.close_tab(_Driver(), index=0, title="https://one.test/path")

    assert [target["id"] for target in backend.targets] == ["B"]
    assert backend.target("B")["visible"] is True


def test_close_background_leaves_the_active_tab_unchanged(provider, backend):
    provider.close_tab(_Driver(), index=1, title="https://two.test/")

    assert [target["id"] for target in backend.targets] == ["A"]
    assert not any(
        method == "Target.activateTarget"
        for _, method, _ in backend.calls
    )


def test_close_defaults_to_the_active_tab(provider, backend):
    provider.close_tab(_Driver(), index=None, title=None)

    assert [target["id"] for target in backend.targets] == ["B"]
    assert backend.target("B")["visible"] is True


def test_close_refuses_the_final_tab(provider, backend):
    backend.targets[:] = backend.targets[:1]

    with pytest.raises(RuntimeError, match="final"):
        provider.close_tab(_Driver(), index=None, title=None)

    assert [target["id"] for target in backend.targets] == ["A"]


def test_close_uses_documented_http_fallback_when_close_target_is_unavailable(
    provider, backend
):
    backend.close_target = False

    provider.close_tab(_Driver(), index=1, title="https://two.test/")

    assert ("GET", "/json/close/B") in backend.http_mutations


def test_a_non_capability_cdp_failure_does_not_retry_through_http(
    provider, backend, monkeypatch
):
    channel = backend.channel()

    class _BrokenChannel(channel):
        def call(self, method, params=None):
            if method == "Target.activateTarget":
                raise RuntimeError("connection lost")
            return super().call(method, params)

    monkeypatch.setattr(_web, "Channel", _BrokenChannel)

    with pytest.raises(RuntimeError, match="outcome is unknown"):
        provider.switch_tab(_Driver(), index=1, title="https://two.test/")

    assert not backend.http_mutations


def test_post_mutation_visibility_timeout_fails_closed(
    provider, backend, monkeypatch
):
    monkeypatch.setattr(backend, "activate", lambda target_id: None)
    monkeypatch.setattr(tabs, "_MUTATION_DEADLINE_S", 0.01)
    monkeypatch.setattr(tabs, "_POLL_INTERVAL_S", 0)

    with pytest.raises(TimeoutError, match="within 5 seconds"):
        provider.switch_tab(_Driver(), index=1, title="https://two.test/")


def test_web_surface_reset_clears_tab_ordering(provider, backend):
    provider.get_tabs(_Driver())
    assert provider._orders
    # The public registry owns a different provider; pin this provider into it
    # so the web teardown contract is tested without reaching private globals.
    from testmu_appium._helpers import tabs as public_tabs

    original = public_tabs._PROVIDERS["android"]
    public_tabs._PROVIDERS["android"] = provider
    try:
        _web.reset()
    finally:
        public_tabs._PROVIDERS["android"] = original

    assert provider._orders == {}
