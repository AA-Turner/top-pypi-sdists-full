"""The remote web debug providers: a cloud device's WebView/pages reached over
the Mobile Binary on the device host, with every loopback address in its
answers rewritten to that host."""
import pytest

from testmu_appium import _config
from testmu_appium._helpers import _web, _web_remote


@pytest.fixture(autouse=True)
def _cloud(monkeypatch):
    monkeypatch.setattr(_config, "run_target", "cloud", raising=False)
    monkeypatch.setenv("HOST_IP", "10.1.2.3")
    monkeypatch.setenv("MOBILE_BINARY_PORT", "31000")
    _web_remote.reset()
    yield
    _web_remote.reset()


def _mb(monkeypatch, answer):
    calls = []

    def post(url, payload, timeout):
        calls.append((url, payload))
        return answer

    monkeypatch.setattr(_web_remote, "_post_json", post)
    return calls


class TestAvailability:
    def test_available_only_on_a_cloud_run_with_a_host(self, monkeypatch):
        assert _web_remote.available() is True
        monkeypatch.setattr(_config, "run_target", "local", raising=False)
        assert _web_remote.available() is False

    def test_not_available_without_the_host_details(self, monkeypatch):
        monkeypatch.delenv("HOST_IP")
        monkeypatch.setattr(_web_remote, "rd_details", lambda: {})
        assert _web_remote.available() is False

    def test_debug_transport_picks_the_remote_provider(self, monkeypatch):
        monkeypatch.setitem(_config._config, "platform", "android")
        assert isinstance(_web.debug_transport(), _web_remote.RemoteAndroidWebDebugTransport)
        monkeypatch.setitem(_config._config, "platform", "ios")
        assert isinstance(_web.debug_transport(), _web_remote.RemoteIosWebDebugTransport)

    def test_a_local_run_keeps_the_local_provider(self, monkeypatch):
        monkeypatch.setattr(_config, "run_target", "local", raising=False)
        monkeypatch.setitem(_config._config, "platform", "android")
        assert isinstance(_web.debug_transport(), _web.LocalAdbWebDebugTransport)


class TestRewrite:
    def test_loopback_hosts_become_the_device_host(self):
        assert (_web_remote.rewrite_host("ws://127.0.0.1:9501/devtools/page/A1", "10.1.2.3")
                == "ws://10.1.2.3:9501/devtools/page/A1")
        assert (_web_remote.rewrite_host("ws://localhost:9222/devtools/page/1", "10.1.2.3")
                == "ws://10.1.2.3:9222/devtools/page/1")

    def test_a_real_host_is_left_alone(self):
        url = "ws://10.9.9.9:9501/devtools/page/A1"
        assert _web_remote.rewrite_host(url, "10.1.2.3") == url

    def test_a_page_with_no_authority_gets_the_host_and_the_endpoint_port(self):
        assert (_web_remote.rewrite_host("ws:///devtools/page/A1", "10.1.2.3", 9540)
                == "ws://10.1.2.3:9540/devtools/page/A1")
        assert (_web_remote.rewrite_host("ws://localhost/devtools/page/A1", "10.1.2.3", 9540)
                == "ws://10.1.2.3:9540/devtools/page/A1")

    def test_host_details_are_read_once_per_session(self, monkeypatch):
        reads = []
        monkeypatch.delenv("HOST_IP")
        monkeypatch.delenv("MOBILE_BINARY_PORT")
        monkeypatch.setattr(_web_remote, "rd_details",
                            lambda: reads.append(1) or {"HOST_IP": "10.1.2.3", "MOBILE_BINARY_PORT": "31000"})
        assert _web_remote.host_port() == ("10.1.2.3", "31000")
        assert _web_remote.host_port() == ("10.1.2.3", "31000")
        assert len(reads) == 1


class TestAndroid:
    def test_forward_asks_the_mobile_binary_for_the_foreground_package(self, monkeypatch):
        calls = _mb(monkeypatch, {"status": "Success", "devtoolsPort": "9540", "pages": []})
        t = _web_remote.RemoteAndroidWebDebugTransport()
        assert t.reachable() is True
        (socket,) = t.sockets()
        assert t.pids_of("com.example.app") is None

        assert t.forward(socket) == ("10.1.2.3", 9540)
        (url, payload), = calls
        assert url == "http://10.1.2.3:31000/v1.0/startdevtools"
        assert payload == {"os": "android", "bundleId": "com.example.app"}
        # Forwarded once per package, not once per action.
        assert t.forward(socket) == ("10.1.2.3", 9540)
        assert len(calls) == 1

    def test_the_port_is_read_off_the_pages_when_the_host_binary_omits_it(self, monkeypatch):
        _mb(monkeypatch, {"status": "Success", "pages": [
            {"webSocketDebuggerUrl": "ws://localhost:9601/devtools/page/X"}]})
        t = _web_remote.RemoteAndroidWebDebugTransport()
        t.pids_of("com.example.app")
        assert t.forward(t.sockets()[0]) == ("10.1.2.3", 9601)

    def test_no_port_anywhere_is_an_error(self, monkeypatch):
        _mb(monkeypatch, {"status": "Success", "pages": []})
        t = _web_remote.RemoteAndroidWebDebugTransport()
        t.pids_of("com.example.app")
        with pytest.raises(RuntimeError, match="no devtools port"):
            t.forward(t.sockets()[0])

    def test_a_refusal_is_an_error_the_scan_marks_dead(self, monkeypatch):
        _mb(monkeypatch, {"status": "Failed", "error": "device not found"})
        t = _web_remote.RemoteAndroidWebDebugTransport()
        t.pids_of("com.example.app")
        with pytest.raises(RuntimeError, match="device not found"):
            t.forward(t.sockets()[0])

    def test_list_targets_reads_the_host_port_and_rewrites_pages(self, monkeypatch):
        seen = []

        def get(url, timeout):
            seen.append(url)
            return [
                {"type": "page", "webSocketDebuggerUrl": "ws://127.0.0.1:9540/devtools/page/A"},
                {"type": "service_worker", "webSocketDebuggerUrl": "ws://127.0.0.1:9540/devtools/page/B"},
                {"type": "page"},
            ]

        monkeypatch.setattr(_web_remote, "_get_json", get)
        t = _web_remote.RemoteAndroidWebDebugTransport()
        targets = t.list_targets(("10.1.2.3", 9540))
        assert seen == ["http://10.1.2.3:9540/json"]
        assert [x["webSocketDebuggerUrl"] for x in targets] == ["ws://10.1.2.3:9540/devtools/page/A"]

    def test_channel_is_the_cdp_channel(self):
        t = _web_remote.RemoteAndroidWebDebugTransport()
        assert isinstance(t.channel("ws://10.1.2.3:9540/devtools/page/A"), _web.Channel)


class TestIos:
    def test_forward_uses_the_iwdp_page_port_for_the_session_udid(self, monkeypatch):
        monkeypatch.setitem(_config._config, "udid", "00008030-AAAA")
        calls = _mb(monkeypatch, {"status": "Success", "iwdpPort": "9502", "pages": []})
        t = _web_remote.RemoteIosWebDebugTransport()
        assert t.pids_of("com.example.app") is None
        assert t.forward(t.sockets()[0]) == ("10.1.2.3", 9502)
        (_, payload), = calls
        assert payload == {"os": "ios", "deviceId": "00008030-AAAA"}

    def test_the_udid_comes_from_the_live_session_when_not_configured(self, monkeypatch):
        monkeypatch.setitem(_config._config, "udid", "")
        from testmu_appium._helpers import driver as driver_mod

        class _Driver:
            capabilities = {"platformName": "iOS", "udid": "00008030-BBBB"}

        monkeypatch.setattr(driver_mod, "get_driver", lambda profile="default": _Driver())
        calls = _mb(monkeypatch, {"status": "Success", "iwdpPort": 9503})
        t = _web_remote.RemoteIosWebDebugTransport()
        t.forward(t.sockets()[0])
        assert calls[0][1]["deviceId"] == "00008030-BBBB"

    def test_an_old_host_binary_without_the_port_is_a_clear_error(self, monkeypatch):
        monkeypatch.setitem(_config._config, "udid", "u")
        _mb(monkeypatch, {"status": "Success", "pages": []})
        t = _web_remote.RemoteIosWebDebugTransport()
        with pytest.raises(RuntimeError, match="iwdpPort"):
            t.forward(t.sockets()[0])

    def test_list_targets_reads_iwdp_on_the_host_and_rewrites(self, monkeypatch):
        from testmu_appium._helpers import _web_ios
        seen = []

        def json_(port, path="/json", timeout=8.0, host="127.0.0.1"):
            seen.append((host, port))
            return [{"webSocketDebuggerUrl": "ws://localhost:9502/devtools/page/1", "appId": "PID:7"}]

        monkeypatch.setattr(_web_ios, "_json", json_)
        _web_ios._state.foreground_pid = 0
        t = _web_remote.RemoteIosWebDebugTransport()
        targets = t.list_targets(("10.1.2.3", 9502))
        assert seen == [("10.1.2.3", 9502)]
        assert targets[0]["webSocketDebuggerUrl"] == "ws://10.1.2.3:9502/devtools/page/1"

    def test_channel_is_the_webkit_channel(self):
        from testmu_appium._helpers._web_ios import IosChannel
        t = _web_remote.RemoteIosWebDebugTransport()
        assert isinstance(t.channel("ws://10.1.2.3:9502/devtools/page/1"), IosChannel)


def test_prepare_web_surface_does_not_spawn_a_local_proxy_for_a_cloud_device(monkeypatch):
    from testmu_appium import perception
    from testmu_appium._helpers import _web_ios
    monkeypatch.setitem(_config._config, "platform", "ios")
    monkeypatch.setattr(_web_ios, "ensure_proxy", lambda *a, **k: pytest.fail("spawned locally"))
    assert perception.prepare_web_surface() is None
