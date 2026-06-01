"""Tests for the internal metrics reporter."""

import asyncio
import json
import threading
from unittest.mock import AsyncMock, MagicMock, patch

from smplkit._metrics import _AsyncMetricsReporter, _Counter, _MetricsReporter


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_reporter(**kwargs):
    """Create a _MetricsReporter with mocked HTTP client."""
    defaults = {
        "http_client": MagicMock(),
        "environment": "test",
        "service": "test-service",
        "flush_interval": 60.0,
    }
    defaults.update(kwargs)
    return _MetricsReporter(**defaults)


def _make_async_reporter(**kwargs):
    """Create an _AsyncMetricsReporter with mocked HTTP client."""
    defaults = {
        "http_client": MagicMock(),
        "environment": "test",
        "service": "test-service",
        "flush_interval": 60.0,
    }
    defaults.update(kwargs)
    return _AsyncMetricsReporter(**defaults)


# ===================================================================
# _Counter dataclass
# ===================================================================


class TestCounter:
    def test_defaults(self):
        c = _Counter()
        assert c.value == 0
        assert c.unit is None
        assert c.window_start is not None

    def test_custom_values(self):
        c = _Counter(value=5, unit="evaluations")
        assert c.value == 5
        assert c.unit == "evaluations"


# ===================================================================
# _MetricsReporter — accumulation
# ===================================================================


class TestMetricsReporterAccumulation:
    def test_record_accumulates_values(self):
        reporter = _make_reporter()
        reporter.record("flags.evaluations", 1, unit="evaluations")
        reporter.record("flags.evaluations", 1, unit="evaluations")
        reporter.record("flags.evaluations", 1, unit="evaluations")

        assert len(reporter._counters) == 1
        key = next(iter(reporter._counters))
        assert reporter._counters[key].value == 3
        reporter.close()

    def test_record_with_custom_value(self):
        reporter = _make_reporter()
        reporter.record("logging.loggers_discovered", 10, unit="loggers")
        key = next(iter(reporter._counters))
        assert reporter._counters[key].value == 10
        reporter.close()

    def test_different_dimensions_separate_counters(self):
        reporter = _make_reporter()
        reporter.record("flags.evaluations", dimensions={"flag": "checkout-v2"})
        reporter.record("flags.evaluations", dimensions={"flag": "dark-mode"})
        assert len(reporter._counters) == 2
        reporter.close()

    def test_same_dimensions_accumulate(self):
        reporter = _make_reporter()
        reporter.record("flags.evaluations", dimensions={"flag": "checkout-v2"})
        reporter.record("flags.evaluations", dimensions={"flag": "checkout-v2"})
        assert len(reporter._counters) == 1
        key = next(iter(reporter._counters))
        assert reporter._counters[key].value == 2
        reporter.close()

    def test_base_dimensions_injected(self):
        reporter = _make_reporter(environment="prod", service="user-svc")
        reporter.record("flags.evaluations", dimensions={"flag": "x"})
        key = next(iter(reporter._counters))
        dims = dict(key[1])
        assert dims["environment"] == "prod"
        assert dims["service"] == "user-svc"
        assert dims["flag"] == "x"
        reporter.close()

    def test_unit_first_write_wins(self):
        reporter = _make_reporter()
        reporter.record("flags.evaluations", unit="evaluations")
        reporter.record("flags.evaluations", unit="different")
        key = next(iter(reporter._counters))
        assert reporter._counters[key].unit == "evaluations"
        reporter.close()

    def test_unit_set_on_first_non_none(self):
        reporter = _make_reporter()
        reporter.record("flags.evaluations")
        reporter.record("flags.evaluations", unit="evaluations")
        key = next(iter(reporter._counters))
        assert reporter._counters[key].unit == "evaluations"
        reporter.close()


# ===================================================================
# _MetricsReporter — gauge
# ===================================================================


class TestMetricsReporterGauge:
    def test_gauge_replaces_value(self):
        reporter = _make_reporter()
        reporter.record_gauge("platform.websocket_connections", 1, unit="connections")
        reporter.record_gauge("platform.websocket_connections", 0, unit="connections")
        key = next(iter(reporter._gauges))
        assert reporter._gauges[key].value == 0
        reporter.close()

    def test_gauge_separate_from_counters(self):
        reporter = _make_reporter()
        reporter.record("flags.evaluations")
        reporter.record_gauge("platform.websocket_connections", 1)
        assert len(reporter._counters) == 1
        assert len(reporter._gauges) == 1
        reporter.close()

    def test_gauge_unit_first_write_wins(self):
        reporter = _make_reporter()
        reporter.record_gauge("platform.websocket_connections", 1, unit="connections")
        reporter.record_gauge("platform.websocket_connections", 0, unit="other")
        key = next(iter(reporter._gauges))
        assert reporter._gauges[key].unit == "connections"
        reporter.close()

    def test_gauge_unit_set_on_first_non_none(self):
        reporter = _make_reporter()
        reporter.record_gauge("platform.websocket_connections", 1)
        reporter.record_gauge("platform.websocket_connections", 0, unit="connections")
        key = next(iter(reporter._gauges))
        assert reporter._gauges[key].unit == "connections"
        reporter.close()


# ===================================================================
# _MetricsReporter — flush
# ===================================================================


class TestMetricsReporterFlush:
    def test_flush_sends_http_post(self):
        reporter = _make_reporter()
        mock_httpx = MagicMock()
        reporter._http_client.get_httpx_client.return_value = mock_httpx

        reporter.record("flags.evaluations", 3, unit="evaluations", dimensions={"flag": "x"})
        reporter._flush()

        mock_httpx.post.assert_called_once()
        args, kwargs = mock_httpx.post.call_args
        assert args[0] == "/api/v1/metrics/bulk"
        assert kwargs["headers"]["Content-Type"] == "application/vnd.api+json"
        payload = json.loads(kwargs["content"])
        assert len(payload["data"]) == 1
        entry = payload["data"][0]
        assert entry["type"] == "metric"
        assert entry["attributes"]["name"] == "flags.evaluations"
        assert entry["attributes"]["value"] == 3
        assert entry["attributes"]["unit"] == "evaluations"
        assert entry["attributes"]["period_seconds"] == 60
        assert "recorded_at" in entry["attributes"]
        dims = entry["attributes"]["dimensions"]
        assert dims["environment"] == "test"
        assert dims["service"] == "test-service"
        assert dims["flag"] == "x"
        reporter.close()

    def test_flush_includes_gauges(self):
        reporter = _make_reporter()
        mock_httpx = MagicMock()
        reporter._http_client.get_httpx_client.return_value = mock_httpx

        reporter.record("flags.evaluations", 1, unit="evaluations")
        reporter.record_gauge("platform.websocket_connections", 1, unit="connections")
        reporter._flush()

        payload = json.loads(mock_httpx.post.call_args[1]["content"])
        assert len(payload["data"]) == 2

        names = {e["attributes"]["name"] for e in payload["data"]}
        assert names == {"flags.evaluations", "platform.websocket_connections"}
        reporter.close()

    def test_flush_resets_counters(self):
        reporter = _make_reporter()
        mock_httpx = MagicMock()
        reporter._http_client.get_httpx_client.return_value = mock_httpx

        reporter.record("flags.evaluations")
        reporter.record_gauge("platform.websocket_connections", 1)
        reporter._flush()

        assert reporter._counters == {}
        assert reporter._gauges == {}
        reporter.close()

    def test_flush_empty_sends_no_http(self):
        reporter = _make_reporter()
        mock_httpx = MagicMock()
        reporter._http_client.get_httpx_client.return_value = mock_httpx

        reporter._flush()
        mock_httpx.post.assert_not_called()
        reporter.close()

    def test_flush_after_flush_sends_no_http(self):
        reporter = _make_reporter()
        mock_httpx = MagicMock()
        reporter._http_client.get_httpx_client.return_value = mock_httpx

        reporter.record("flags.evaluations")
        reporter._flush()
        mock_httpx.post.reset_mock()
        reporter._flush()
        mock_httpx.post.assert_not_called()
        reporter.close()

    def test_flush_http_error_swallowed(self):
        reporter = _make_reporter()
        mock_httpx = MagicMock()
        mock_httpx.post.side_effect = Exception("network error")
        reporter._http_client.get_httpx_client.return_value = mock_httpx

        reporter.record("flags.evaluations")
        reporter._flush()  # Should not raise

        # Data is discarded after failed flush
        assert reporter._counters == {}
        reporter.close()

    def test_flush_public_method(self):
        reporter = _make_reporter()
        mock_httpx = MagicMock()
        reporter._http_client.get_httpx_client.return_value = mock_httpx

        reporter.record("flags.evaluations")
        reporter.flush()
        mock_httpx.post.assert_called_once()
        reporter.close()


# ===================================================================
# _MetricsReporter — timer
# ===================================================================


class TestMetricsReporterTimer:
    def test_timer_starts_lazily(self):
        reporter = _make_reporter()
        assert reporter._timer is None
        reporter.record("flags.evaluations")
        assert reporter._timer is not None
        reporter.close()

    def test_timer_not_started_when_no_records(self):
        reporter = _make_reporter()
        assert reporter._timer is None
        reporter.close()
        assert reporter._timer is None

    def test_timer_not_started_after_close(self):
        reporter = _make_reporter()
        reporter.close()
        reporter.record("flags.evaluations")
        assert reporter._timer is None


# ===================================================================
# _MetricsReporter — close
# ===================================================================


class TestMetricsReporterClose:
    def test_close_flushes(self):
        reporter = _make_reporter()
        mock_httpx = MagicMock()
        reporter._http_client.get_httpx_client.return_value = mock_httpx

        reporter.record("flags.evaluations")
        reporter.close()

        mock_httpx.post.assert_called_once()
        assert reporter._counters == {}

    def test_close_cancels_timer(self):
        reporter = _make_reporter()
        reporter.record("flags.evaluations")
        assert reporter._timer is not None
        reporter.close()
        assert reporter._timer is None

    def test_close_idempotent(self):
        reporter = _make_reporter()
        mock_httpx = MagicMock()
        reporter._http_client.get_httpx_client.return_value = mock_httpx

        reporter.record("flags.evaluations")
        reporter.close()
        reporter.close()  # Should not raise

        mock_httpx.post.assert_called_once()


# ===================================================================
# _MetricsReporter — thread safety
# ===================================================================


class TestMetricsReporterThreadSafety:
    def test_concurrent_records(self):
        reporter = _make_reporter()
        barrier = threading.Barrier(10)

        def _worker():
            barrier.wait()
            for _ in range(100):
                reporter.record("flags.evaluations")

        threads = [threading.Thread(target=_worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        key = next(iter(reporter._counters))
        assert reporter._counters[key].value == 1000
        reporter.close()


# ===================================================================
# _MetricsReporter — tick
# ===================================================================


class TestMetricsReporterTick:
    def test_tick_concurrent_record_creates_only_one_timer(self):
        """Regression: record() called while a tick flush is in-flight must not start
        a second timer, which would result in two concurrent timers and two POSTs per
        interval."""
        reporter = _make_reporter()
        mock_httpx = MagicMock()
        reporter._http_client.get_httpx_client.return_value = mock_httpx
        reporter.record("flags.evaluations")  # populate buffer + start initial timer

        flush_started = threading.Event()
        flush_can_finish = threading.Event()
        timer_start_count = [0]

        original_start_timer = reporter._start_timer

        def counting_start_timer():
            timer_start_count[0] += 1
            original_start_timer()

        reporter._start_timer = counting_start_timer

        original_post = mock_httpx.post

        def blocking_post(*args, **kwargs):
            flush_started.set()
            flush_can_finish.wait()
            return original_post(*args, **kwargs)

        mock_httpx.post = blocking_post

        tick_thread = threading.Thread(target=reporter._tick)
        tick_thread.start()

        flush_started.wait()
        # Race: record() sees the in-flight timer; must NOT start a second one.
        reporter.record("flags.evaluations")
        flush_can_finish.set()
        tick_thread.join()

        assert timer_start_count[0] == 1  # only _tick itself restarted the timer
        reporter.close()

    def test_tick_flushes_and_restarts_timer(self):
        reporter = _make_reporter()
        mock_httpx = MagicMock()
        reporter._http_client.get_httpx_client.return_value = mock_httpx

        reporter.record("flags.evaluations")
        reporter._tick()

        mock_httpx.post.assert_called_once()
        assert reporter._timer is not None  # Timer restarted
        reporter.close()

    def test_tick_does_not_restart_after_close(self):
        reporter = _make_reporter()
        reporter.record("flags.evaluations")
        reporter._closed = True
        reporter._tick()
        assert reporter._timer is None


# ===================================================================
# _AsyncMetricsReporter — accumulation
# ===================================================================


class TestAsyncMetricsReporterAccumulation:
    def test_record_accumulates(self):
        reporter = _make_async_reporter()
        reporter.record("flags.evaluations", 1)
        reporter.record("flags.evaluations", 1)
        reporter.record("flags.evaluations", 1)

        key = next(iter(reporter._counters))
        assert reporter._counters[key].value == 3
        asyncio.run(reporter.close())

    def test_record_unit_set_on_first_non_none(self):
        reporter = _make_async_reporter()
        reporter.record("flags.evaluations")
        reporter.record("flags.evaluations", unit="evaluations")
        key = next(iter(reporter._counters))
        assert reporter._counters[key].unit == "evaluations"
        asyncio.run(reporter.close())

    def test_gauge_replaces(self):
        reporter = _make_async_reporter()
        reporter.record_gauge("platform.websocket_connections", 1, unit="connections")
        reporter.record_gauge("platform.websocket_connections", 0, unit="connections")

        key = next(iter(reporter._gauges))
        assert reporter._gauges[key].value == 0
        asyncio.run(reporter.close())

    def test_different_dimensions(self):
        reporter = _make_async_reporter()
        reporter.record("flags.evaluations", dimensions={"flag": "a"})
        reporter.record("flags.evaluations", dimensions={"flag": "b"})
        assert len(reporter._counters) == 2
        asyncio.run(reporter.close())


# ===================================================================
# _AsyncMetricsReporter — flush
# ===================================================================


class TestAsyncMetricsReporterFlush:
    def test_async_flush(self):
        reporter = _make_async_reporter()
        mock_httpx = AsyncMock()
        reporter._http_client.get_async_httpx_client.return_value = mock_httpx

        reporter.record("flags.evaluations", 5, unit="evaluations")

        asyncio.run(reporter.flush())

        mock_httpx.post.assert_called_once()
        args, kwargs = mock_httpx.post.call_args
        assert args[0] == "/api/v1/metrics/bulk"
        payload = json.loads(kwargs["content"])
        assert payload["data"][0]["attributes"]["value"] == 5
        asyncio.run(reporter.close())

    def test_async_flush_empty(self):
        reporter = _make_async_reporter()
        mock_httpx = AsyncMock()
        reporter._http_client.get_async_httpx_client.return_value = mock_httpx

        asyncio.run(reporter.flush())
        mock_httpx.post.assert_not_called()
        asyncio.run(reporter.close())

    def test_async_flush_error_swallowed(self):
        reporter = _make_async_reporter()
        mock_httpx = AsyncMock()
        mock_httpx.post.side_effect = Exception("network error")
        reporter._http_client.get_async_httpx_client.return_value = mock_httpx

        reporter.record("flags.evaluations")
        asyncio.run(reporter.flush())  # Should not raise
        assert reporter._counters == {}
        asyncio.run(reporter.close())

    def test_sync_flush_used_by_tick(self):
        reporter = _make_async_reporter()
        mock_httpx = MagicMock()
        reporter._http_client.get_httpx_client.return_value = mock_httpx

        reporter.record("flags.evaluations")
        reporter._flush_sync()

        mock_httpx.post.assert_called_once()
        assert reporter._counters == {}
        asyncio.run(reporter.close())

    def test_sync_flush_empty(self):
        reporter = _make_async_reporter()
        mock_httpx = MagicMock()
        reporter._http_client.get_httpx_client.return_value = mock_httpx

        reporter._flush_sync()
        mock_httpx.post.assert_not_called()
        asyncio.run(reporter.close())

    def test_sync_flush_error_swallowed(self):
        reporter = _make_async_reporter()
        mock_httpx = MagicMock()
        mock_httpx.post.side_effect = Exception("network error")
        reporter._http_client.get_httpx_client.return_value = mock_httpx

        reporter.record("flags.evaluations")
        reporter._flush_sync()  # Should not raise
        asyncio.run(reporter.close())


# ===================================================================
# _AsyncMetricsReporter — close
# ===================================================================


class TestAsyncMetricsReporterClose:
    def test_close_flushes(self):
        reporter = _make_async_reporter()
        mock_httpx = AsyncMock()
        reporter._http_client.get_async_httpx_client.return_value = mock_httpx

        reporter.record("flags.evaluations")
        asyncio.run(reporter.close())

        mock_httpx.post.assert_called_once()

    def test_close_cancels_timer(self):
        reporter = _make_async_reporter()
        reporter.record("flags.evaluations")
        assert reporter._timer is not None
        asyncio.run(reporter.close())
        assert reporter._timer is None

    def test_close_idempotent(self):
        reporter = _make_async_reporter()
        mock_httpx = AsyncMock()
        reporter._http_client.get_async_httpx_client.return_value = mock_httpx

        reporter.record("flags.evaluations")
        asyncio.run(reporter.close())
        asyncio.run(reporter.close())

        mock_httpx.post.assert_called_once()


# ===================================================================
# _AsyncMetricsReporter — timer
# ===================================================================


class TestAsyncMetricsReporterTimer:
    def test_timer_starts_lazily(self):
        reporter = _make_async_reporter()
        assert reporter._timer is None
        reporter.record("flags.evaluations")
        assert reporter._timer is not None
        asyncio.run(reporter.close())

    def test_tick_concurrent_record_creates_only_one_timer(self):
        """Regression: record() called while a tick flush is in-flight must not start
        a second timer."""
        reporter = _make_async_reporter()
        mock_httpx = MagicMock()
        reporter._http_client.get_httpx_client.return_value = mock_httpx
        reporter.record("flags.evaluations")  # populate buffer + start initial timer

        flush_started = threading.Event()
        flush_can_finish = threading.Event()
        timer_start_count = [0]

        original_start_timer = reporter._start_timer

        def counting_start_timer():
            timer_start_count[0] += 1
            original_start_timer()

        reporter._start_timer = counting_start_timer

        original_post = mock_httpx.post

        def blocking_post(*args, **kwargs):
            flush_started.set()
            flush_can_finish.wait()
            return original_post(*args, **kwargs)

        mock_httpx.post = blocking_post

        tick_thread = threading.Thread(target=reporter._tick)
        tick_thread.start()

        flush_started.wait()
        reporter.record("flags.evaluations")
        flush_can_finish.set()
        tick_thread.join()

        assert timer_start_count[0] == 1
        asyncio.run(reporter.close())

    def test_tick_flushes_and_restarts(self):
        reporter = _make_async_reporter()
        mock_httpx = MagicMock()
        reporter._http_client.get_httpx_client.return_value = mock_httpx

        reporter.record("flags.evaluations")
        reporter._tick()

        mock_httpx.post.assert_called_once()
        assert reporter._timer is not None
        asyncio.run(reporter.close())

    def test_tick_no_restart_after_close(self):
        reporter = _make_async_reporter()
        reporter.record("flags.evaluations")
        reporter._closed = True
        reporter._tick()
        assert reporter._timer is None


# ===================================================================
# _AsyncMetricsReporter — thread safety
# ===================================================================


class TestAsyncMetricsReporterThreadSafety:
    def test_concurrent_records(self):
        reporter = _make_async_reporter()
        barrier = threading.Barrier(10)

        def _worker():
            barrier.wait()
            for _ in range(100):
                reporter.record("flags.evaluations")

        threads = [threading.Thread(target=_worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        key = next(iter(reporter._counters))
        assert reporter._counters[key].value == 1000
        asyncio.run(reporter.close())


# ===================================================================
# _AsyncMetricsReporter — gauge
# ===================================================================


class TestAsyncMetricsReporterGauge:
    def test_gauge_unit_first_write_wins(self):
        reporter = _make_async_reporter()
        reporter.record_gauge("platform.websocket_connections", 1, unit="connections")
        reporter.record_gauge("platform.websocket_connections", 0, unit="other")
        key = next(iter(reporter._gauges))
        assert reporter._gauges[key].unit == "connections"
        asyncio.run(reporter.close())

    def test_gauge_unit_set_on_first_non_none(self):
        reporter = _make_async_reporter()
        reporter.record_gauge("platform.websocket_connections", 1)
        reporter.record_gauge("platform.websocket_connections", 0, unit="connections")
        key = next(iter(reporter._gauges))
        assert reporter._gauges[key].unit == "connections"
        asyncio.run(reporter.close())


# ===================================================================
# Integration: SmplClient disable_telemetry
# ===================================================================


class TestSmplClientTelemetry:
    def test_telemetry_enabled_by_default(self):
        from smplkit import SmplClient

        client = SmplClient(api_key="sk_api_test", environment="test")
        assert client._metrics is not None
        client.close()

    def test_telemetry_disabled(self):
        from smplkit import SmplClient

        client = SmplClient(api_key="sk_api_test", environment="test", telemetry=False)
        assert client._metrics is None
        client.close()

    def test_async_telemetry_enabled_by_default(self):
        from smplkit import AsyncSmplClient

        client = AsyncSmplClient(api_key="sk_api_test", environment="test")
        assert client._metrics is not None
        asyncio.run(client.close())

    def test_async_telemetry_disabled(self):
        from smplkit import AsyncSmplClient

        client = AsyncSmplClient(api_key="sk_api_test", environment="test", telemetry=False)
        assert client._metrics is None
        asyncio.run(client.close())


# ===================================================================
# Integration: FlagsClient instrumentation
# ===================================================================


class TestFlagsInstrumentation:
    def _make_flags_client(self, *, with_metrics=True):
        parent = MagicMock()
        parent._api_key = "sk_test"
        parent._environment = "test"
        parent._service = None
        if with_metrics:
            parent._metrics = _MetricsReporter(
                http_client=MagicMock(),
                environment="test",
                service="test-service",
            )
        else:
            parent._metrics = None
        manage = MagicMock()
        parent.manage = manage
        with patch("smplkit.flags.client.AuthenticatedClient"):
            from smplkit.flags.client import FlagsClient

            client = FlagsClient(parent, manage=manage, metrics=parent._metrics)
        return client, parent

    def test_evaluation_records_metrics(self):
        client, parent = self._make_flags_client()
        # Populate flag store with a simple flag
        client._connected = True
        client._environment = "test"
        client._flag_store["checkout-v2"] = {
            "id": "checkout-v2",
            "type": "boolean",
            "default": False,
            "environments": {},
            "rules": [],
        }

        client._evaluate_handle("checkout-v2", False, None)

        metrics = parent._metrics
        # Should have cache miss + evaluation
        counters = dict(metrics._counters)
        names = {k[0] for k in counters}
        assert "flags.evaluations" in names
        assert "flags.cache_misses" in names
        metrics.close()

    def test_cache_hit_records_metrics(self):
        client, parent = self._make_flags_client()
        client._connected = True
        client._environment = "test"
        client._flag_store["checkout-v2"] = {
            "id": "checkout-v2",
            "type": "boolean",
            "default": False,
            "environments": {},
            "rules": [],
        }

        # First call: cache miss
        client._evaluate_handle("checkout-v2", False, None)
        # Second call: cache hit
        client._evaluate_handle("checkout-v2", False, None)

        metrics = parent._metrics
        counters = dict(metrics._counters)
        names = {k[0] for k in counters}
        assert "flags.cache_hits" in names
        assert "flags.cache_misses" in names

        # Find the cache hit counter
        for key, counter in counters.items():
            if key[0] == "flags.cache_hits":
                assert counter.value == 1
            if key[0] == "flags.cache_misses":
                assert counter.value == 1
            if key[0] == "flags.evaluations":
                assert counter.value == 2
        metrics.close()

    def test_no_metrics_when_disabled(self):
        client, parent = self._make_flags_client(with_metrics=False)
        client._connected = True
        client._environment = "test"
        client._flag_store["checkout-v2"] = {
            "id": "checkout-v2",
            "type": "boolean",
            "default": False,
            "environments": {},
            "rules": [],
        }

        client._evaluate_handle("checkout-v2", False, None)
        # Should not raise; parent._metrics is None


# ===================================================================
# Integration: ConfigClient instrumentation
# ===================================================================


class TestConfigInstrumentation:
    def _make_config_client(self, *, with_metrics=True):
        parent = MagicMock()
        parent._api_key = "sk_test"
        parent._environment = "test"
        parent._service = None
        if with_metrics:
            parent._metrics = _MetricsReporter(
                http_client=MagicMock(),
                environment="test",
                service="test-service",
            )
        else:
            parent._metrics = None
        manage = MagicMock()
        parent.manage = manage

        from smplkit.config.client import ConfigClient

        client = ConfigClient(parent, manage=manage, metrics=parent._metrics)
        return client, parent

    def test_resolve_records_metric(self):
        client, parent = self._make_config_client()
        client._connected = True
        client._config_cache["my-config"] = {"host": "localhost"}

        result = client.get("my-config")

        assert dict(result) == {"host": "localhost"}
        metrics = parent._metrics
        counters = dict(metrics._counters)
        names = {k[0] for k in counters}
        assert "config.resolutions" in names

        for key, counter in counters.items():
            if key[0] == "config.resolutions":
                dims = dict(key[1])
                assert dims["config"] == "my-config"
        metrics.close()

    def test_resolve_no_metrics_when_disabled(self):
        client, parent = self._make_config_client(with_metrics=False)
        client._connected = True
        client._config_cache["my-config"] = {"host": "localhost"}

        result = client.get("my-config")
        assert dict(result) == {"host": "localhost"}

    def test_change_listeners_record_metric(self):
        client, parent = self._make_config_client()
        old_cache = {"my-config": {"host": "old"}}
        new_cache = {"my-config": {"host": "new"}}

        client._fire_change_listeners(old_cache, new_cache, source="manual")

        metrics = parent._metrics
        counters = dict(metrics._counters)
        names = {k[0] for k in counters}
        assert "config.changes" in names
        metrics.close()

    def test_no_change_no_metric(self):
        client, parent = self._make_config_client()
        old_cache = {"my-config": {"host": "same"}}
        new_cache = {"my-config": {"host": "same"}}

        client._fire_change_listeners(old_cache, new_cache, source="manual")

        metrics = parent._metrics
        assert len(metrics._counters) == 0
        metrics.close()


# ===================================================================
# Integration: WebSocket instrumentation
# ===================================================================


class TestWebSocketInstrumentation:
    def test_ws_accepts_metrics(self):
        from smplkit._ws import SharedWebSocket

        metrics = _make_reporter()
        ws = SharedWebSocket(app_base_url="https://app.smplkit.com", api_key="sk_test", metrics=metrics)
        assert ws._metrics is metrics
        metrics.close()

    def test_ws_no_metrics(self):
        from smplkit._ws import SharedWebSocket

        ws = SharedWebSocket(app_base_url="https://app.smplkit.com", api_key="sk_test")
        assert ws._metrics is None


# ===================================================================
# Payload format
# ===================================================================


class TestPayloadFormat:
    def test_json_api_structure(self):
        reporter = _make_reporter()
        mock_httpx = MagicMock()
        reporter._http_client.get_httpx_client.return_value = mock_httpx

        reporter.record("flags.evaluations", 42, unit="evaluations", dimensions={"flag": "x"})
        reporter.record_gauge("platform.websocket_connections", 1, unit="connections")
        reporter._flush()

        payload = json.loads(mock_httpx.post.call_args[1]["content"])
        assert "data" in payload
        assert isinstance(payload["data"], list)
        assert len(payload["data"]) == 2

        for entry in payload["data"]:
            assert entry["type"] == "metric"
            attrs = entry["attributes"]
            assert "name" in attrs
            assert "value" in attrs
            assert "unit" in attrs
            assert "period_seconds" in attrs
            assert "dimensions" in attrs
            assert "recorded_at" in attrs
            assert isinstance(attrs["dimensions"], dict)
        reporter.close()
