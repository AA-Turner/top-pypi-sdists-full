# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit tests for the future-tied root job span + phase events.

These exercise the observability contract from PR #971 WITHOUT a Ray cluster,
using an in-memory span exporter and a mocked ``ray.get``:

  * the root span (``backfill``/``bulk_load``) closes exactly once, OK on
    success and ERROR on failure — guards the reviewer-flagged "root span ends
    OK even when the job raises" regression,
  * ``RayJobFuture.result()`` drives that close for both sync and fire-and-forget
    callers,
  * ``_emit_phase`` writes both an OTel span event and a durable JobRecord event,
  * the dispatch / geneva.job / worker_setup sub-spans keep their topology.
"""

from collections.abc import Iterator
from typing import NoReturn
from unittest.mock import MagicMock

import pytest
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
    InMemorySpanExporter,
)
from opentelemetry.trace import StatusCode

from geneva import telemetry
from geneva.runners.ray.pipeline import RayJobFuture


@pytest.fixture
def exporter() -> Iterator[InMemorySpanExporter]:
    """Inject an in-memory tracer provider (no collector / env needed)."""
    exp = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exp))
    telemetry._reset_state()
    telemetry._initialized = True
    telemetry._tracer_provider = provider
    telemetry._tracer = provider.get_tracer("test")
    yield exp
    telemetry._reset_state()


def _finished(exp: InMemorySpanExporter, name: str) -> ReadableSpan:
    return next(s for s in exp.get_finished_spans() if s.name == name)


def _ray_future(job_id: str = "j1") -> RayJobFuture:
    # ray_obj_ref is only handed to the (mocked) ray.get; job_tracker=None makes
    # status() a no-op so no cluster is touched.
    return RayJobFuture(job_id=job_id, ray_obj_ref=object())


# --- JobFuture._close_span -------------------------------------------------


def test_close_span_ok_on_success(exporter) -> None:
    fut = _ray_future()
    fut._otel_span = telemetry.open_span("backfill", {"job_id": "j1"})
    fut._close_span(None)
    span = _finished(exporter, "backfill")
    # No explicit status set on success -> UNSET (Jaeger/Tempo treat as OK).
    assert span.status.status_code == StatusCode.UNSET
    assert span.attributes["job_id"] == "j1"


def test_close_span_error_on_failure(exporter) -> None:
    fut = _ray_future()
    fut._otel_span = telemetry.open_span("backfill", {"job_id": "j1"})
    fut._close_span(RuntimeError("boom"))
    span = _finished(exporter, "backfill")
    assert span.status.status_code == StatusCode.ERROR
    assert any(e.name == "exception" for e in span.events)


def test_close_span_is_idempotent(exporter) -> None:
    fut = _ray_future()
    fut._otel_span = telemetry.open_span("backfill", {"job_id": "j1"})
    fut._close_span(None)
    fut._close_span(RuntimeError("late"))  # already closed -> ignored
    spans = [s for s in exporter.get_finished_spans() if s.name == "backfill"]
    assert len(spans) == 1
    assert spans[0].status.status_code == StatusCode.UNSET


def test_close_span_noop_when_untied(exporter) -> None:
    # Sync-wrapper futures never set _otel_span; closing must be a silent no-op.
    fut = _ray_future()
    fut._close_span(RuntimeError("boom"))
    assert exporter.get_finished_spans() == ()


# --- RayJobFuture.result() drives the close --------------------------------


def test_result_closes_span_ok(exporter, monkeypatch) -> None:
    import ray

    monkeypatch.setattr(ray, "get", lambda ref, timeout=None: {"rows": 1})
    fut = _ray_future()
    fut._otel_span = telemetry.open_span("backfill", {"job_id": "j1"})
    assert fut.result() == {"rows": 1}
    assert _finished(exporter, "backfill").status.status_code == StatusCode.UNSET


def test_result_closes_span_error_and_reraises(exporter, monkeypatch) -> None:
    import ray

    def _boom(ref, timeout=None) -> NoReturn:
        raise RuntimeError("job failed")

    monkeypatch.setattr(ray, "get", _boom)
    fut = _ray_future()
    fut._otel_span = telemetry.open_span("backfill", {"job_id": "j1"})
    with pytest.raises(RuntimeError, match="job failed"):
        fut.result()
    assert _finished(exporter, "backfill").status.status_code == StatusCode.ERROR


def test_result_timeout_poll_leaves_span_open(exporter, monkeypatch) -> None:
    # A bounded-timeout poll raises GetTimeoutError (a TimeoutError subclass)
    # while the job is still running. That must NOT close the root span, or the
    # eventually-successful run would be idempotently mislabeled ERROR.
    import ray

    calls = {"n": 0}

    def _get(ref, timeout=None) -> dict:
        calls["n"] += 1
        if calls["n"] == 1:
            raise TimeoutError("still running")  # ray.get(timeout=T) style
        return {"ok": True}

    monkeypatch.setattr(ray, "get", _get)
    fut = _ray_future()
    fut._otel_span = telemetry.open_span("backfill", {"job_id": "j1"})

    with pytest.raises(TimeoutError):
        fut.result(timeout=0.01)
    assert exporter.get_finished_spans() == ()  # span left open
    assert fut._span_closed is False

    assert fut.result() == {"ok": True}  # eventual success closes it OK
    assert _finished(exporter, "backfill").status.status_code == StatusCode.UNSET


# --- _emit_phase: span event + durable JobRecord event ---------------------


def test_emit_phase_writes_both_destinations(exporter) -> None:
    from geneva.runners.ray.pipeline import _emit_phase

    hist = MagicMock()
    span = telemetry.open_span("backfill", {"job_id": "j1"})
    with telemetry.attach_span(span):
        _emit_phase(hist, "j1", "Cluster provisioning")
    telemetry.close_span(span)

    finished = _finished(exporter, "backfill")
    # The span event keeps the verbose "Entering phase:" prefix; the durable
    # JobRecord event stores the bare phase name (what the events line renders).
    assert any(
        e.name == "Entering phase: Cluster provisioning" for e in finished.events
    )
    hist.add_event.assert_called_once_with("j1", "Cluster provisioning")


def test_emit_phase_durable_event_skipped_without_job_id(exporter) -> None:
    from geneva.runners.ray.pipeline import _emit_phase

    hist = MagicMock()
    span = telemetry.open_span("backfill", {})
    with telemetry.attach_span(span):
        _emit_phase(hist, None, "Job planning")  # no job_id -> no durable write
    telemetry.close_span(span)
    hist.add_event.assert_not_called()


# --- sub-span topology (dispatch / geneva.job / worker_setup) --------------


def test_dispatch_worker_setup_topology(exporter) -> None:
    # Mirrors the driver+worker flow: dispatch is a non-attaching sibling of
    # geneva.job (both under the job-type root); worker_setup nests in geneva.job.
    root = telemetry.open_span("backfill", {"job_id": "j1"})
    with telemetry.attach_span(root):
        disp = telemetry.open_span("dispatch", {"job_type": "backfill"})
        carrier = telemetry.inject_context()
        telemetry.close_span(disp)
    job, tok = telemetry.start_linked_span(carrier, "geneva.job", {"job_id": "j1"})
    setup = telemetry.open_span("worker_setup", {"job_id": "j1"})
    telemetry.close_span(setup)
    telemetry.end_job_span(job, tok, None)
    telemetry.close_span(root)

    s = {x.name: x for x in exporter.get_finished_spans()}
    root_id = s["backfill"].context.span_id
    assert s["dispatch"].parent.span_id == root_id
    assert s["geneva.job"].parent.span_id == root_id
    assert s["worker_setup"].parent.span_id == s["geneva.job"].context.span_id
    assert len({x.context.trace_id for x in s.values()}) == 1


# --- report_plan_progress (live planning-bar feed) -------------------------


def test_report_plan_progress_noop_without_tracker() -> None:
    from geneva.runners.ray.jobtracker import report_plan_progress

    # Local runs pass job_tracker=None; must be a silent no-op.
    report_plan_progress(None, desc="building tasks", n=1, total=10)


def test_report_plan_progress_pushes_substep_and_counter() -> None:
    from geneva.runners.ray.jobtracker import (
        PLAN_FRAGMENTS_METRIC,
        report_plan_progress,
    )

    tracker = MagicMock()
    report_plan_progress(tracker, desc="building tasks", n=3, total=10)
    tracker.set_total.remote.assert_called_once_with(PLAN_FRAGMENTS_METRIC, 10)
    tracker.set_desc.remote.assert_called_once_with(
        PLAN_FRAGMENTS_METRIC, "building tasks"
    )
    tracker.set.remote.assert_called_once_with(PLAN_FRAGMENTS_METRIC, 3)


def test_report_plan_progress_counter_only_tick() -> None:
    from geneva.runners.ray.jobtracker import (
        PLAN_FRAGMENTS_METRIC,
        report_plan_progress,
    )

    tracker = MagicMock()
    report_plan_progress(tracker, n=42)  # in-loop tick: only the counter moves
    tracker.set.remote.assert_called_once_with(PLAN_FRAGMENTS_METRIC, 42)
    tracker.set_total.remote.assert_not_called()
    tracker.set_desc.remote.assert_not_called()


def test_report_plan_progress_suppresses_actor_errors() -> None:
    from geneva.runners.ray.jobtracker import report_plan_progress

    tracker = MagicMock()
    tracker.set_desc.remote.side_effect = RuntimeError("actor unreachable")
    # A dead/unreachable tracker must never break planning.
    report_plan_progress(tracker, desc="counting rows")
