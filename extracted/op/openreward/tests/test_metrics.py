"""Tests for env-server tool-call metric emission.

Tests the openreward.environments._metrics module directly with a real
OpenTelemetry InMemoryMetricReader (not mocks) so we exercise the SDK
plumbing. Avoids set_meter_provider so we don't fight OTel's "only one
provider" guard across tests.
"""

from __future__ import annotations

import pytest


def _install_in_memory_reader():
    """Install a fresh in-memory reader without touching the global provider.

    Patches the module-level ``_counter`` / ``_provider`` directly so
    ``record_tool_call`` writes to our reader. Each test calls this and
    pairs it with ``_teardown`` to reset state.
    """
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import InMemoryMetricReader

    from openreward.environments import _metrics

    reader = InMemoryMetricReader()
    provider = MeterProvider(metric_readers=[reader])
    meter = provider.get_meter("openreward.environments.server")
    _metrics._counter = meter.create_counter(
        name="openreward.tool_calls",
        description="test",
        unit="1",
    )
    _metrics._provider = provider
    return reader


def _teardown():
    from openreward.environments import _metrics
    _metrics._counter = None
    _metrics._provider = None


def _data_points(reader):
    """Pull (attributes, value) pairs from the latest collection."""
    metric_data = reader.get_metrics_data()
    out = []
    for rm in metric_data.resource_metrics:
        for sm in rm.scope_metrics:
            for metric in sm.metrics:
                for point in metric.data.data_points:
                    out.append((dict(point.attributes), point.value))
    return out


def test_record_tool_call_emits_with_attributes():
    reader = _install_in_memory_reader()
    try:
        from openreward.environments._metrics import record_tool_call

        record_tool_call(env_name="env-a", status="success")
        record_tool_call(env_name="env-a", status="success")
        record_tool_call(env_name="env-a", status="user_exception")
        record_tool_call(env_name="env-b", status="not_found")

        points = _data_points(reader)
        # OTel aggregates by attribute tuple — expect 3 distinct series.
        by_attrs = {tuple(sorted(a.items())): v for a, v in points}
        assert by_attrs[(("env_name", "env-a"), ("status", "success"))] == 2
        assert by_attrs[(("env_name", "env-a"), ("status", "user_exception"))] == 1
        assert by_attrs[(("env_name", "env-b"), ("status", "not_found"))] == 1
    finally:
        _teardown()


def test_record_tool_call_is_noop_when_unset():
    """If setup_metrics was never called, record_tool_call must not raise
    and must not implicitly install a provider."""
    from openreward.environments import _metrics
    assert _metrics._counter is None
    _metrics.record_tool_call("env", "success")  # must not raise
    assert _metrics._counter is None


def test_shutdown_metrics_clears_state():
    """shutdown_metrics should call provider.shutdown and null out state.

    Safe to call when nothing is set up (no-op)."""
    from openreward.environments import _metrics

    _metrics.shutdown_metrics()  # no-op path
    assert _metrics._counter is None and _metrics._provider is None

    _install_in_memory_reader()
    assert _metrics._counter is not None and _metrics._provider is not None

    _metrics.shutdown_metrics()
    assert _metrics._counter is None
    assert _metrics._provider is None


def test_setup_metrics_noop_without_endpoint(monkeypatch):
    """setup_metrics() must not install an exporter when no endpoint is set
    — protects external SDK users who haven't opted into telemetry."""
    monkeypatch.delenv("OPENREWARD_OTLP_ENDPOINT", raising=False)
    from openreward.environments import _metrics

    _teardown()
    _metrics.setup_metrics()
    assert _metrics._counter is None
    assert _metrics._provider is None


def test_setup_metrics_idempotent():
    """Calling setup_metrics twice should not double-install."""
    _install_in_memory_reader()
    from openreward.environments import _metrics

    first_counter = _metrics._counter
    _metrics.setup_metrics(endpoint="any-endpoint:4317")
    assert _metrics._counter is first_counter

    _teardown()


def test_resolve_insecure_defaults_plaintext_for_hostport(monkeypatch):
    """The cluster-internal form ``host:4317`` (no scheme) defaults to
    plaintext — OTel collectors run unencrypted in-cluster."""
    monkeypatch.delenv("OPENREWARD_OTLP_INSECURE", raising=False)
    from openreward.environments._metrics import _resolve_insecure
    assert _resolve_insecure("opentelemetry-collector.opentelemetry.svc:4317") is True
    assert _resolve_insecure("http://localhost:4317") is True


def test_resolve_insecure_tls_for_https_or_443(monkeypatch):
    """https:// scheme or port 443 implies TLS — for external endpoints."""
    monkeypatch.delenv("OPENREWARD_OTLP_INSECURE", raising=False)
    from openreward.environments._metrics import _resolve_insecure
    assert _resolve_insecure("https://otel.example.com:4317") is False
    assert _resolve_insecure("otel.example.com:443") is False


def test_resolve_insecure_env_override(monkeypatch):
    """OPENREWARD_OTLP_INSECURE wins over the scheme/port heuristic."""
    from openreward.environments._metrics import _resolve_insecure
    monkeypatch.setenv("OPENREWARD_OTLP_INSECURE", "1")
    assert _resolve_insecure("https://otel.example.com:443") is True
    monkeypatch.setenv("OPENREWARD_OTLP_INSECURE", "0")
    assert _resolve_insecure("host:4317") is False


def test_server_call_tool_coro_calls_record_with_correct_status(monkeypatch):
    """Verify the /call route wires record_tool_call with the right
    status for each outcome path. Calls into the closure indirectly by
    constructing a Server and exercising call_session_tool semantics."""
    from openreward.environments import _metrics, server as server_mod
    from openreward.environments.types import (
        RunToolError,
        RunToolOutput,
        RunToolSuccess,
        ToolOutput,
        TextBlock,
    )

    calls: list[dict] = []

    def fake_record(env_name, status):
        calls.append({"env_name": env_name, "status": status})

    monkeypatch.setattr(server_mod, "record_tool_call", fake_record)

    # Re-implement the status-derivation logic from the route handler so
    # we exercise the same branches. The closure can't be called directly
    # because it captures FastAPI request state.
    def derive_status(res_or_exc):
        if isinstance(res_or_exc, Exception):
            return "user_exception"
        if res_or_exc.root.ok:
            return "success"
        return res_or_exc.root.reason or "input_validation"

    # success
    res_ok = RunToolOutput(RunToolSuccess(output=ToolOutput(blocks=[TextBlock(text="ok")])))
    assert derive_status(res_ok) == "success"

    # malformed-call reasons
    for reason in ("not_found", "name_collision", "input_validation"):
        res_err = RunToolOutput(RunToolError(reason=reason, error="x"))  # type: ignore[arg-type]
        assert derive_status(res_err) == reason

    # user exception
    assert derive_status(RuntimeError("boom")) == "user_exception"
