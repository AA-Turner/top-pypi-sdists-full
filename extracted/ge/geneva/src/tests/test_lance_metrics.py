# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Tests for the Lance object-store metrics bridge (geneva.telemetry)."""

import logging
import subprocess
import sys
from collections.abc import Iterator

import pytest
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader

from geneva import telemetry


@pytest.fixture(autouse=True)
def _reset_telemetry() -> Iterator[None]:
    telemetry._reset_state()
    yield
    telemetry._reset_state()


def _in_memory_provider() -> MeterProvider:
    """A real provider with no exporter threads and no global registration."""
    return MeterProvider(metric_readers=[InMemoryMetricReader()])


def test_bridge_skipped_when_telemetry_disabled(monkeypatch) -> None:
    """No collector URL means no provider, so the bridge is never installed."""
    monkeypatch.delenv(telemetry.OTEL_COLLECTOR_URL_ENV, raising=False)
    calls: list = []
    monkeypatch.setattr(telemetry, "_init_lance_metrics", calls.append)

    telemetry.init()

    assert calls == []


def test_bridge_skipped_when_metrics_init_fails(monkeypatch) -> None:
    """A failed metrics init leaves no provider; the bridge must not install."""
    monkeypatch.setenv(telemetry.OTEL_COLLECTOR_URL_ENV, "http://localhost:4317")
    monkeypatch.setattr(telemetry, "_init_metrics", lambda url, resource: None)
    monkeypatch.setattr(telemetry, "_init_tracing", lambda url, resource: None)
    calls: list = []
    monkeypatch.setattr(telemetry, "_init_lance_metrics", calls.append)

    telemetry.init()

    assert calls == []


def test_bridge_receives_geneva_provider(monkeypatch) -> None:
    """When metrics init succeeds, the bridge gets Geneva's own provider."""
    monkeypatch.setenv(telemetry.OTEL_COLLECTOR_URL_ENV, "http://localhost:4317")
    provider = _in_memory_provider()

    def fake_init_metrics(url, resource) -> None:  # noqa: ANN001
        telemetry._meter_provider = provider

    monkeypatch.setattr(telemetry, "_init_metrics", fake_init_metrics)
    monkeypatch.setattr(telemetry, "_init_tracing", lambda url, resource: None)
    calls: list = []
    monkeypatch.setattr(telemetry, "_init_lance_metrics", calls.append)

    telemetry.init()

    assert calls == [provider]


def test_lance_metrics_default_on(monkeypatch) -> None:
    """With no opt-out set, the bridge is installed on the given provider."""
    monkeypatch.delenv(telemetry.LANCE_METRICS_ENV, raising=False)
    calls: list = []
    monkeypatch.setattr(
        "lance.otel.instrument_lance_metrics",
        lambda provider: calls.append(provider) or True,
    )
    provider = _in_memory_provider()

    telemetry._init_lance_metrics(provider)

    assert calls == [provider]


@pytest.mark.parametrize("value", ["off", "false", "0", "no", "OFF"])
def test_lance_metrics_opt_out(monkeypatch, value: str) -> None:
    """GENEVA_ENABLE_OTEL_LANCE_METRICS=false disables the bridge."""
    monkeypatch.setenv(telemetry.LANCE_METRICS_ENV, value)
    calls: list = []
    monkeypatch.setattr(
        "lance.otel.instrument_lance_metrics",
        lambda provider: calls.append(provider) or True,
    )

    telemetry._init_lance_metrics(_in_memory_provider())

    assert calls == []


@pytest.mark.parametrize("value", ["1", "true", "yes", "on", "ON"])
def test_lance_metrics_explicit_truthy_enables(monkeypatch, value: str) -> None:
    """Explicit truthy values keep the bridge on."""
    monkeypatch.setenv(telemetry.LANCE_METRICS_ENV, value)
    calls: list = []
    monkeypatch.setattr(
        "lance.otel.instrument_lance_metrics",
        lambda provider: calls.append(provider) or True,
    )

    telemetry._init_lance_metrics(_in_memory_provider())

    assert len(calls) == 1


@pytest.mark.parametrize("value", ["disabled", "ofr", "banana"])
def test_lance_metrics_unrecognized_value_fails_closed(
    monkeypatch, caplog, value: str
) -> None:
    """Unrecognized values disable the bridge and warn (fail closed)."""
    monkeypatch.setenv(telemetry.LANCE_METRICS_ENV, value)
    calls: list = []
    monkeypatch.setattr(
        "lance.otel.instrument_lance_metrics",
        lambda provider: calls.append(provider) or True,
    )

    with caplog.at_level(logging.WARNING, logger="geneva.telemetry"):
        telemetry._init_lance_metrics(_in_memory_provider())

    assert calls == []
    assert any("unrecognized" in r.message for r in caplog.records)


def test_lance_metrics_unavailable(monkeypatch, caplog) -> None:
    """An older pylance without lance.otel disables the bridge quietly."""
    monkeypatch.delenv(telemetry.LANCE_METRICS_ENV, raising=False)
    # A None entry makes `from lance.otel import ...` raise ImportError.
    monkeypatch.setitem(sys.modules, "lance.otel", None)

    with caplog.at_level(logging.INFO, logger="geneva.telemetry"):
        telemetry._init_lance_metrics(_in_memory_provider())

    assert any("unavailable" in r.message for r in caplog.records)


def test_lance_metrics_recorder_conflict_warns(monkeypatch, caplog) -> None:
    """A pre-existing Rust metrics recorder produces one clear warning."""
    monkeypatch.setattr("lance.otel.instrument_lance_metrics", lambda provider: False)

    with caplog.at_level(logging.WARNING, logger="geneva.telemetry"):
        telemetry._init_lance_metrics(_in_memory_provider())

    assert any("recorder" in r.message for r in caplog.records)


def test_lance_metrics_failure_never_raises(monkeypatch, caplog) -> None:
    """A bridge bug must never break telemetry init (or the job)."""

    def boom(provider) -> bool:  # noqa: ANN001
        raise RuntimeError("boom")

    monkeypatch.setattr("lance.otel.instrument_lance_metrics", boom)

    with caplog.at_level(logging.WARNING, logger="geneva.telemetry"):
        telemetry._init_lance_metrics(_in_memory_provider())

    assert any("failed to enable" in r.message for r in caplog.records)


# Subprocess: the Rust recorder is process-global and cannot be uninstalled.
_E2E_SCRIPT = """
import os, tempfile
import pyarrow as pa
import lance
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader
from lance.otel import instrument_lance_metrics

reader = InMemoryMetricReader()
provider = MeterProvider(metric_readers=[reader])
assert instrument_lance_metrics(provider)

with tempfile.TemporaryDirectory() as d:
    uri = os.path.join(d, "t.lance")
    lance.write_dataset(pa.table({"a": list(range(100))}), uri)
    lance.dataset(uri).to_table()

names = {
    metric.name
    for rm in reader.get_metrics_data().resource_metrics
    for sm in rm.scope_metrics
    for metric in sm.metrics
}
assert "lance_object_store_requests_total" in names, names
assert "lance_object_store_request_duration_seconds_bucket" in names, names
print("OK")
"""


def test_bridge_end_to_end_subprocess() -> None:
    """Real bridge + real (local-file) Lance I/O exports object-store metrics."""
    proc = subprocess.run(
        [sys.executable, "-c", _E2E_SCRIPT],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stderr
    assert "OK" in proc.stdout
