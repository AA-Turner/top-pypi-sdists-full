"""Tests for the SmartWait subsystem (network-idle poller, config, chrome gate)."""
import json
import time

import pytest
from unittest.mock import MagicMock, call

from testmu_selenium._helpers import smart_wait as sw


def _perf_entry(method, request_id, type_="XHR", ts=None):
    """Build one Chrome performance-log entry as get_log('performance') returns it."""
    return {
        "timestamp": ts if ts is not None else time.time() * 1000,
        "message": json.dumps(
            {"message": {"method": method, "params": {"requestId": request_id, "type": type_}}}
        ),
    }


def _batched_get_log(batches):
    """Return a get_log side_effect that yields each batch once, then [] forever."""
    queue = list(batches)

    def _get_log(_kind):
        return queue.pop(0) if queue else []

    return _get_log


class TestParseFeatureFlags:
    def test_none_returns_defaults(self):
        cfg = sw._parse_feature_flags(None)
        assert cfg["vision_min"] == 5.0
        assert cfg["vision_max"] == 5.0
        assert cfg["non_vision_max"] == 10.0
        assert cfg["dom_idle_threshold"] == 0.3
        assert cfg["dom_idle_max"] == 1.5

    def test_payload_overrides_known_keys_only(self):
        cfg = sw._parse_feature_flags(
            {"kaneai_web_smart_wait": {"payload": {"non_vision_max": 4.0, "bogus": 99}}}
        )
        assert cfg["non_vision_max"] == 4.0
        assert "bogus" not in cfg

    def test_malformed_shapes_fall_back(self):
        expected = {
            "vision_min": 5.0, "vision_max": 5.0, "non_vision_max": 10.0,
            "dom_idle_threshold": 0.3, "dom_idle_max": 1.5,
        }
        assert sw._parse_feature_flags({"kaneai_web_smart_wait": "nope"}) == expected
        assert sw._parse_feature_flags({}) == expected


class TestLoadFeatureFlags:
    def test_unset_returns_none(self, monkeypatch):
        monkeypatch.delenv("KANEAI_FEATURE_FLAGS", raising=False)
        assert sw.load_feature_flags() is None

    def test_invalid_json_returns_none(self, monkeypatch):
        monkeypatch.setenv("KANEAI_FEATURE_FLAGS", "{not json")
        assert sw.load_feature_flags() is None

    def test_valid_json_parsed(self, monkeypatch):
        monkeypatch.setenv("KANEAI_FEATURE_FLAGS", json.dumps({"a": 1}))
        assert sw.load_feature_flags() == {"a": 1}


class TestIsChrome:
    @pytest.mark.parametrize("name,expected", [
        ("chrome", True), ("Chrome", True), ("chromium", True),
        ("firefox", False), ("MicrosoftEdge", False), ("", False),
    ])
    def test_browser_names(self, name, expected):
        d = MagicMock()
        d.capabilities = {"browserName": name}
        assert sw._is_chrome(d) is expected

    def test_caps_access_error_is_false(self):
        d = MagicMock()
        type(d).capabilities = property(lambda self: (_ for _ in ()).throw(RuntimeError()))
        assert sw._is_chrome(d) is False


class TestNetworkWait:
    def test_idle_when_no_traffic(self, caplog):
        # Intentionally spends ~200ms in the real _WAIT_BUFFER_S quiet buffer.
        d = MagicMock()
        d.get_log.return_value = []
        with caplog.at_level("INFO"):
            sw._smart_network_wait(d, timeout=1.0)
        assert "Network idle after" in caplog.text

    def test_idle_after_request_then_response(self, caplog):
        now = time.time() * 1000
        d = MagicMock()
        d.get_log.side_effect = _batched_get_log([
            [_perf_entry("Network.requestWillBeSent", "r1", ts=now)],
            [_perf_entry("Network.responseReceived", "r1", ts=now)],
        ])
        with caplog.at_level("INFO"):
            sw._smart_network_wait(d, timeout=2.0)
        assert "Network idle after" in caplog.text

    def test_timeout_when_request_never_completes(self, caplog):
        now = time.time() * 1000
        d = MagicMock()
        d.get_log.side_effect = _batched_get_log([
            [_perf_entry("Network.requestWillBeSent", "r1", ts=now)],
        ])
        with caplog.at_level("INFO"):
            sw._smart_network_wait(d, timeout=0.3)
        assert "Network wait timeout after" in caplog.text

    def test_noise_types_ignored(self, caplog):
        now = time.time() * 1000
        d = MagicMock()
        d.get_log.side_effect = _batched_get_log([
            [_perf_entry("Network.requestWillBeSent", "doc", type_="Document", ts=now)],
        ])
        with caplog.at_level("INFO"):
            sw._smart_network_wait(d, timeout=1.0)
        # Document-type request is filtered out, so we still reach idle.
        assert "Network idle after" in caplog.text

    def test_get_log_failure_returns_cleanly(self, caplog):
        d = MagicMock()
        d.get_log.side_effect = RuntimeError("no perf log")
        with caplog.at_level("INFO"):
            sw._smart_network_wait(d, timeout=0.3)
        # No perf events ever arrive -> idle path (empty request map) after buffer.
        assert "Network idle after" in caplog.text


class TestDomWait:
    def test_logs_reason_and_elapsed(self, caplog):
        d = MagicMock()
        d.timeouts.script = 30.0
        d.execute_async_script.return_value = {"reason": "idle", "elapsed_ms": 390}
        with caplog.at_level("INFO"):
            sw._smart_dom_wait(d, threshold_s=0.3, max_s=1.5)
        assert "DOM idle after 0.39s (reason: idle)" in caplog.text

    def test_sets_then_restores_script_timeout(self):
        d = MagicMock()
        d.timeouts.script = 30.0
        d.execute_async_script.return_value = {"reason": "max", "elapsed_ms": 1500}
        sw._smart_dom_wait(d, threshold_s=0.3, max_s=1.5)
        calls = [c.args[0] for c in d.set_script_timeout.call_args_list]
        assert calls == [1.5 + sw._SCRIPT_TIMEOUT_MARGIN_S, 30.0]

    def test_script_failure_is_swallowed(self, caplog):
        d = MagicMock()
        d.timeouts.script = 30.0
        d.execute_async_script.side_effect = RuntimeError("script blew up")
        with caplog.at_level("INFO"):
            sw._smart_dom_wait(d, threshold_s=0.3, max_s=1.5)
        # No DOM-idle INFO line; error went to debug; no exception escaped.
        assert "DOM idle after" not in caplog.text
        # Prior timeout is still restored even when the script raises.
        calls = [c.args[0] for c in d.set_script_timeout.call_args_list]
        assert calls == [1.5 + sw._SCRIPT_TIMEOUT_MARGIN_S, 30.0]

    def test_skips_timeout_change_when_prev_unreadable(self):
        d = MagicMock()
        type(d.timeouts).script = property(lambda self: (_ for _ in ()).throw(RuntimeError()))
        d.execute_async_script.return_value = {"reason": "idle", "elapsed_ms": 100}
        sw._smart_dom_wait(d, threshold_s=0.3, max_s=1.5)
        d.set_script_timeout.assert_not_called()


class TestSmartWaitClass:
    def _chrome(self):
        d = MagicMock()
        d.capabilities = {"browserName": "chrome"}
        return d

    def test_non_chrome_is_noop(self, monkeypatch):
        net = MagicMock()
        dom = MagicMock()
        monkeypatch.setattr(sw, "_smart_network_wait", net)
        monkeypatch.setattr(sw, "_smart_dom_wait", dom)
        d = MagicMock()
        d.capabilities = {"browserName": "firefox"}
        sw.SmartWait(d).smart_wait(is_vision=False)
        net.assert_not_called()
        dom.assert_not_called()

    def test_non_vision_runs_network_then_dom(self, monkeypatch):
        manager = MagicMock()
        monkeypatch.setattr(sw, "_smart_network_wait", manager.net)
        monkeypatch.setattr(sw, "_smart_dom_wait", manager.dom)
        d = self._chrome()
        sw.SmartWait(d).smart_wait(is_vision=False)
        assert manager.mock_calls == [call.net(d, timeout=10.0), call.dom(d, 0.3, 1.5)]

    def test_zero_max_skips_that_wait(self, monkeypatch):
        calls = []
        monkeypatch.setattr(sw, "_smart_network_wait", lambda *a, **k: calls.append("net"))
        monkeypatch.setattr(sw, "_smart_dom_wait", lambda *a, **k: calls.append("dom"))
        ff = {"kaneai_web_smart_wait": {"payload": {"non_vision_max": 0, "dom_idle_max": 0}}}
        sw.SmartWait(self._chrome(), feature_flags=ff).smart_wait(is_vision=False)
        assert calls == []

    def test_vision_sleeps_min_then_network(self, monkeypatch):
        sleeps = []
        net = MagicMock()
        dom = MagicMock()
        monkeypatch.setattr(sw.time, "sleep", lambda s: sleeps.append(s))
        monkeypatch.setattr(sw, "_smart_network_wait", net)
        monkeypatch.setattr(sw, "_smart_dom_wait", dom)
        ff = {"kaneai_web_smart_wait": {"payload": {"vision_min": 2.0, "vision_max": 5.0}}}
        d = self._chrome()
        sw.SmartWait(d, feature_flags=ff).smart_wait(is_vision=True)
        assert sleeps == [2.0]
        net.assert_called_once_with(d, timeout=3.0)  # remaining = 5.0 - 2.0
        dom.assert_not_called()

    def test_malformed_config_does_not_raise(self, monkeypatch):
        monkeypatch.setattr(sw, "_smart_network_wait", MagicMock())
        monkeypatch.setattr(sw, "_smart_dom_wait", MagicMock())
        ff = {"kaneai_web_smart_wait": {"payload": {"non_vision_max": "abc"}}}
        # Must not raise — the never-raises contract.
        sw.SmartWait(self._chrome(), feature_flags=ff).smart_wait(is_vision=False)

    def test_uses_env_flags_when_none_passed(self, monkeypatch):
        monkeypatch.setenv(
            "KANEAI_FEATURE_FLAGS",
            json.dumps({"kaneai_web_smart_wait": {"payload": {"non_vision_max": 3.0}}}),
        )
        inst = sw.SmartWait(self._chrome())
        assert inst.config["non_vision_max"] == 3.0
