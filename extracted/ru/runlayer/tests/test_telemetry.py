"""Tests for best-effort CLI tracing (runlayer_cli.telemetry)."""

from __future__ import annotations

import pytest

from runlayer_cli import telemetry


@pytest.fixture(autouse=True)
def _reset_telemetry_state():
    """Reset module globals around each test (idempotent init guard)."""
    telemetry.shutdown_cli_tracing()
    yield
    telemetry.shutdown_cli_tracing()


def test_init_noop_when_unconfigured() -> None:
    # No host/api_key -> tracing stays disabled, no exception.
    telemetry.init_cli_tracing(host=None, api_key=None, collector_version="1.2.3")

    headers: dict[str, str] = {}
    telemetry.inject_trace_context(headers)
    assert headers == {}  # nothing injected when disabled


def test_init_noop_when_opted_out(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RUNLAYER_TELEMETRY_DISABLED", "1")
    telemetry.init_cli_tracing(
        host="https://app.example.com", api_key="rl_secret", collector_version="1.2.3"
    )

    headers: dict[str, str] = {}
    telemetry.inject_trace_context(headers)
    assert "traceparent" not in headers


def test_command_span_is_a_noop_context_manager_when_disabled() -> None:
    # Must work as a context manager even when tracing never initialized.
    with telemetry.command_span("cli.scan", command="scan"):
        executed = True
    assert executed


def test_shutdown_is_safe_without_init() -> None:
    # Should never raise even if init was never called.
    telemetry.shutdown_cli_tracing()


def test_init_and_inject_when_configured() -> None:
    telemetry.init_cli_tracing(
        host="https://app.example.com",
        api_key="rl_secret",
        collector_version="9.9.9",
    )

    with telemetry.command_span("cli.scan", command="scan"):
        headers: dict[str, str] = {}
        telemetry.inject_trace_context(headers)

    # When tracing is active, a W3C traceparent is injected inside a span.
    assert "traceparent" in headers
