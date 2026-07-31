import asyncio
import uuid
from datetime import timedelta
from types import SimpleNamespace
from typing import Any

import pytest
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader
from opentelemetry.sdk.metrics.view import ExplicitBucketHistogramAggregation, View
from temporalio import activity, workflow
from temporalio.runtime import (
    BUFFERED_METRIC_KIND_COUNTER,
    BUFFERED_METRIC_KIND_GAUGE,
    BUFFERED_METRIC_KIND_HISTOGRAM,
    MetricBuffer,
    MetricBufferDurationFormat,
    Runtime,
    TelemetryConfig,
)
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import UnsandboxedWorkflowRunner, Worker

from mistralai.workflows.core.temporal import runtime_metrics
from mistralai.workflows.core.temporal.runtime_metrics import build_temporal_metric_views, pump_runtime_metrics


@activity.defn
async def _noop_activity() -> str:
    return "act"


@workflow.defn
class _ExampleWorkflow:
    @workflow.run
    async def run(self) -> str:
        # Exercise a regular and a local activity so their runtime histograms are emitted too, widening
        # coverage of the "every emitted histogram is pinned" assertion below.
        await workflow.execute_activity(_noop_activity, start_to_close_timeout=timedelta(seconds=30))
        await workflow.execute_local_activity(_noop_activity, start_to_close_timeout=timedelta(seconds=30))
        return "ok"


def _update(name: str, kind: int, value: float, attributes: dict[str, Any], *, unit: str = "", description: str = ""):
    metric = SimpleNamespace(name=name, kind=kind, unit=unit, description=description)
    return SimpleNamespace(metric=metric, value=value, attributes=attributes)


class _FakeBuffer:
    """Serves batches of updates on successive retrieve_updates() calls, then empties."""

    def __init__(self, batches: list[list[Any]]) -> None:
        self._batches = list(batches)

    def retrieve_updates(self) -> list[Any]:
        return self._batches.pop(0) if self._batches else []


def _reader_and_provider(views: list[View] | None = None) -> tuple[InMemoryMetricReader, MeterProvider]:
    reader = InMemoryMetricReader()
    return reader, MeterProvider(metric_readers=[reader], views=tuple(views or ()))


def _metrics_by_name(reader: InMemoryMetricReader) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for rm in reader.get_metrics_data().resource_metrics:
        for sm in rm.scope_metrics:
            for metric in sm.metrics:
                out[metric.name] = metric
    return out


async def _run_pump_once(
    buffer: Any, provider: MeterProvider, *, interval_s: float = 0.01, buffer_size: int = 100_000
) -> None:
    """Start the pump, let it drain one batch, then cancel so the final drain + flush runs."""
    task = asyncio.create_task(
        pump_runtime_metrics(
            buffer,
            provider.get_meter("test"),
            interval_s=interval_s,
            meter_provider=provider,
            buffer_size=buffer_size,
        )
    )
    await asyncio.sleep(0.05)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task


class TestPumpTranslation:
    @pytest.mark.asyncio
    async def test_counter_sums_deltas(self) -> None:
        reader, provider = _reader_and_provider()
        buffer = _FakeBuffer(
            [
                [
                    _update("temporal_workflow_completed_total", BUFFERED_METRIC_KIND_COUNTER, 2, {"namespace": "ns"}),
                    _update("temporal_workflow_completed_total", BUFFERED_METRIC_KIND_COUNTER, 3, {"namespace": "ns"}),
                ]
            ]
        )
        await _run_pump_once(buffer, provider)

        point = next(iter(_metrics_by_name(reader)["temporal_workflow_completed_total"].data.data_points))
        assert point.value == 5  # deltas summed by the cumulative counter
        assert point.attributes["namespace"] == "ns"

    @pytest.mark.asyncio
    async def test_gauge_keeps_last_value(self) -> None:
        reader, provider = _reader_and_provider()
        buffer = _FakeBuffer(
            [
                [
                    _update("temporal_worker_task_slots_available", BUFFERED_METRIC_KIND_GAUGE, 10, {"q": "a"}),
                    _update("temporal_worker_task_slots_available", BUFFERED_METRIC_KIND_GAUGE, 4, {"q": "a"}),
                ]
            ]
        )
        await _run_pump_once(buffer, provider)

        assert next(iter(_metrics_by_name(reader)["temporal_worker_task_slots_available"].data.data_points)).value == 4

    @pytest.mark.asyncio
    async def test_histogram_records_observations_into_pinned_buckets(self) -> None:
        views = [
            View(
                instrument_name="temporal_workflow_endtoend_latency",
                aggregation=ExplicitBucketHistogramAggregation(boundaries=[10.0, 100.0, 1000.0]),
            )
        ]
        reader, provider = _reader_and_provider(views)
        buffer = _FakeBuffer(
            [
                [
                    _update("temporal_workflow_endtoend_latency", BUFFERED_METRIC_KIND_HISTOGRAM, 5, {}, unit="ms"),
                    _update("temporal_workflow_endtoend_latency", BUFFERED_METRIC_KIND_HISTOGRAM, 50, {}, unit="ms"),
                    _update("temporal_workflow_endtoend_latency", BUFFERED_METRIC_KIND_HISTOGRAM, 5000, {}, unit="ms"),
                ]
            ]
        )
        await _run_pump_once(buffer, provider)

        metric = _metrics_by_name(reader)["temporal_workflow_endtoend_latency"]
        point = next(iter(metric.data.data_points))
        assert point.count == 3
        assert list(point.explicit_bounds) == [10.0, 100.0, 1000.0]
        assert list(point.bucket_counts) == [1, 1, 0, 1]  # <=10, <=100, <=1000, >1000
        assert metric.unit == "ms"

    @pytest.mark.asyncio
    async def test_unprefixed_name_is_normalized(self) -> None:
        reader, provider = _reader_and_provider()
        buffer = _FakeBuffer([[_update("workflow_failed_total", BUFFERED_METRIC_KIND_COUNTER, 1, {})]])
        await _run_pump_once(buffer, provider)
        assert "temporal_workflow_failed_total" in _metrics_by_name(reader)

    @pytest.mark.asyncio
    async def test_bad_update_is_swallowed_and_next_still_records(self) -> None:
        reader, provider = _reader_and_provider()

        class _BadAttrs:
            def keys(self) -> Any:
                raise RuntimeError("boom")

        good = _update("temporal_workflow_completed_total", BUFFERED_METRIC_KIND_COUNTER, 7, {})
        bad = _update("temporal_workflow_failed_total", BUFFERED_METRIC_KIND_COUNTER, 1, _BadAttrs())
        await _run_pump_once(_FakeBuffer([[bad, good]]), provider)

        names = _metrics_by_name(reader)
        assert "temporal_workflow_completed_total" in names
        assert "temporal_workflow_failed_total" not in names

    @pytest.mark.asyncio
    async def test_final_drain_on_cancel_captures_last_batch(self) -> None:
        reader, provider = _reader_and_provider()
        # Long interval so the loop's first drain returns [] then sleeps; cancel fires mid-sleep, so only
        # the cancel-time final drain can surface the update (fails if that block is removed).
        buffer = _FakeBuffer(
            [[], [_update("temporal_activity_task_received_total", BUFFERED_METRIC_KIND_COUNTER, 9, {})]]
        )
        await _run_pump_once(buffer, provider, interval_s=10.0)
        assert "temporal_activity_task_received_total" in _metrics_by_name(reader)

    @pytest.mark.asyncio
    async def test_flush_failure_on_shutdown_still_raises_cancelled(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # A force_flush error on shutdown must not mask the CancelledError the worker awaits.
        _, provider = _reader_and_provider()

        def _boom() -> None:
            raise RuntimeError("flush exploded")

        monkeypatch.setattr(provider, "force_flush", _boom)
        buffer = _FakeBuffer([[_update("temporal_workflow_completed_total", BUFFERED_METRIC_KIND_COUNTER, 1, {})]])
        await _run_pump_once(buffer, provider)  # asserts CancelledError (not RuntimeError) propagates

    @pytest.mark.asyncio
    async def test_near_capacity_batch_warns(self) -> None:
        # A drained batch >= 80% of buffer_size signals core may be dropping; the pump must warn.
        import structlog

        _, provider = _reader_and_provider()
        batch = [_update("temporal_workflow_completed_total", BUFFERED_METRIC_KIND_COUNTER, 1, {}) for _ in range(8)]
        with structlog.testing.capture_logs() as logs:
            await _run_pump_once(_FakeBuffer([batch]), provider, buffer_size=10)
        assert any("near capacity" in e.get("event", "") for e in logs), logs


class TestBucketBoundaries:
    def test_known_latency_histograms_have_pinned_boundaries(self) -> None:
        required = {
            "temporal_workflow_endtoend_latency",
            "temporal_activity_execution_latency",
            "temporal_activity_succeed_endtoend_latency",
            "temporal_workflow_task_schedule_to_start_latency",
        }
        assert required <= set(runtime_metrics.TEMPORAL_HISTOGRAM_BOUNDARIES)

    @pytest.mark.asyncio
    async def test_exported_buckets_match_captured_boundaries(self) -> None:
        expected = runtime_metrics.TEMPORAL_HISTOGRAM_BOUNDARIES["temporal_workflow_endtoend_latency"]
        reader, provider = _reader_and_provider(build_temporal_metric_views())
        buffer = _FakeBuffer(
            [[_update("temporal_workflow_endtoend_latency", BUFFERED_METRIC_KIND_HISTOGRAM, 1234, {}, unit="ms")]]
        )
        await _run_pump_once(buffer, provider)

        point = next(iter(_metrics_by_name(reader)["temporal_workflow_endtoend_latency"].data.data_points))
        assert list(point.explicit_bounds) == expected


class TestBufferedRuntimeMetrics:
    """End-to-end: run workflows (with activities) against a Runtime wired to a MetricBuffer and assert the
    drained updates carry the names/attributes/kinds the pump forwards, counters are deltas, and every
    emitted histogram has pinned bucket boundaries."""

    @pytest.mark.asyncio
    async def test_buffered_updates_carry_temporal_prefix_attrs_and_kinds(self) -> None:
        runs = 3
        buffer = MetricBuffer(50000, MetricBufferDurationFormat.MILLISECONDS)
        runtime = Runtime(telemetry=TelemetryConfig(metrics=buffer, attach_service_name=False))
        async with await WorkflowEnvironment.start_time_skipping(runtime=runtime) as env:
            task_queue = f"tq-{uuid.uuid4()}"
            async with Worker(
                env.client,
                task_queue=task_queue,
                workflows=[_ExampleWorkflow],
                activities=[_noop_activity],
                workflow_runner=UnsandboxedWorkflowRunner(),
            ):
                for _ in range(runs):
                    result = await env.client.execute_workflow(
                        _ExampleWorkflow.run, id=f"wf-{uuid.uuid4()}", task_queue=task_queue
                    )
                    assert result == "ok"
            updates = buffer.retrieve_updates()

        assert updates, "expected buffered runtime metric updates from the worker"
        names = {u.metric.name for u in updates}
        attr_keys: set[str] = set()
        for u in updates:
            attr_keys |= set(dict(u.attributes).keys())

        assert all(n.startswith("temporal_") for n in names)  # core already prefixes -> normalization is idempotent
        assert "temporal_workflow_completed" in names
        assert {"namespace", "task_queue", "workflow_type"} <= attr_keys
        assert {u.metric.kind for u in updates} == {
            BUFFERED_METRIC_KIND_COUNTER,
            BUFFERED_METRIC_KIND_GAUGE,
            BUFFERED_METRIC_KIND_HISTOGRAM,
        }

        # Counters are deltas: summing over N completions gives N (cumulative would give more).
        completed_delta_sum = sum(
            u.value
            for u in updates
            if u.metric.name == "temporal_workflow_completed" and u.metric.kind == BUFFERED_METRIC_KIND_COUNTER
        )
        assert completed_delta_sum == runs

        # Every histogram core emits must have pinned bucket boundaries. If an SDK upgrade adds a new
        # histogram (or renames one), this fails so we know to add a matching View / re-capture buckets.
        emitted_histograms = {
            runtime_metrics._normalize_name(u.metric.name)
            for u in updates
            if u.metric.kind == BUFFERED_METRIC_KIND_HISTOGRAM
        }
        unpinned = emitted_histograms - set(runtime_metrics.TEMPORAL_HISTOGRAM_BOUNDARIES)
        assert not unpinned, (
            f"Temporal core emits histograms with no pinned buckets (SDK upgrade?): {sorted(unpinned)}. "
            "Add them to TEMPORAL_HISTOGRAM_BOUNDARIES (buckets captured from the live series)."
        )
