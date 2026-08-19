"""Tests for geneva.telemetry (OTLP metrics bootstrap)."""

import subprocess
import sys
from collections.abc import Iterator

import pytest

from geneva import telemetry


@pytest.fixture(autouse=True)
def _reset_telemetry() -> Iterator[None]:
    telemetry._reset_state()
    yield
    telemetry._reset_state()


def test_disabled_when_collector_url_unset(monkeypatch) -> None:
    """With no collector URL, telemetry is a silent no-op."""
    monkeypatch.delenv(telemetry.OTEL_COLLECTOR_URL_ENV, raising=False)

    assert telemetry.get_meter() is None
    assert telemetry.get_histogram("geneva.test.histogram") is None


def test_record_and_flush_are_noops_when_disabled(monkeypatch) -> None:
    """Recording / flushing must never raise, even when disabled."""
    monkeypatch.delenv(telemetry.OTEL_COLLECTOR_URL_ENV, raising=False)

    # None of these should raise or set up a provider.
    telemetry.record_ms("udf_processing_time", 12.0, attributes={"job_id": "j1"})
    telemetry.flush()
    telemetry.shutdown()

    assert telemetry.get_meter() is None


def test_init_is_latched(monkeypatch) -> None:
    """First call latches init so an unset URL doesn't re-run every call."""
    monkeypatch.delenv(telemetry.OTEL_COLLECTOR_URL_ENV, raising=False)

    assert telemetry.get_meter() is None
    assert telemetry._initialized is True


def test_resource_instance_id_is_unique_per_process(monkeypatch) -> None:
    """Workers in one Ray pod must not export independent counters as one series."""
    monkeypatch.setenv("HOSTNAME", "ray-worker-pod")
    monkeypatch.setattr(telemetry.os, "getpid", lambda: 4242)

    resource = telemetry._build_resource()

    assert resource.attributes["service.instance.id"] == "ray-worker-pod-4242"


def test_tracing_is_noop_when_disabled(monkeypatch) -> None:
    """Tracer/span helpers are no-ops (no trace) when telemetry is disabled."""
    monkeypatch.delenv(telemetry.OTEL_COLLECTOR_URL_ENV, raising=False)

    assert telemetry.get_tracer() is None

    # span() yields None and must not raise.
    with telemetry.span("plan", {"job_id": "j1"}) as sp:
        assert sp is None

    # start/end job span are no-ops returning (None, None).
    job_span, token = telemetry.start_job_span({"job_id": "j1"})
    assert job_span is None
    assert token is None
    telemetry.end_job_span(job_span, token, RuntimeError("boom"))

    # propagation helpers are no-ops too.
    assert telemetry.inject_context() == {}
    wspan, wtoken = telemetry.start_linked_span({}, "applier.run")
    assert wspan is None
    assert wtoken is None


def test_worker_span_joins_trace_via_carrier() -> None:
    """inject_context() on the caller + start_linked_span() on the worker put the
    worker span in the same trace, parented to the captured span."""
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )

    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    # Inject an in-memory provider directly (no collector / env needed).
    telemetry._reset_state()
    telemetry._initialized = True
    telemetry._tracer_provider = provider
    telemetry._tracer = provider.get_tracer("test")

    # Caller side (e.g. the pipeline's `execute` scope): root span + carrier.
    root, root_tok = telemetry.start_job_span({"job_id": "j1"})
    carrier = telemetry.inject_context()
    assert "traceparent" in carrier
    telemetry.end_job_span(root, root_tok)

    # Worker side (a different process in reality): rebuild parent from carrier.
    wspan, wtok = telemetry.start_linked_span(carrier, "applier.run")
    telemetry.end_job_span(wspan, wtok)

    spans = {s.name: s for s in exporter.get_finished_spans()}
    job, applier = spans["geneva.job"], spans["applier.run"]
    assert applier.context.trace_id == job.context.trace_id
    assert applier.parent is not None
    assert applier.parent.span_id == job.context.span_id


# Subprocess: the flag is read at `import geneva`, already done in this process.
_INIT_ON_IMPORT_SCRIPT = """
import os, sys
if sys.argv[1] == "1":
    os.environ["GENEVA_TELEMETRY_INIT_ON_IMPORT"] = "1"
else:
    os.environ.pop("GENEVA_TELEMETRY_INIT_ON_IMPORT", None)
import geneva
from geneva import telemetry
print(telemetry._initialized)
"""


@pytest.mark.parametrize(("flag", "expected"), [("1", "True"), ("0", "False")])
def test_init_on_import_flag(flag: str, expected: str) -> None:
    """The flag makes `import geneva` init telemetry; without it, lazy."""
    proc = subprocess.run(
        [sys.executable, "-c", _INIT_ON_IMPORT_SCRIPT, flag],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == expected
