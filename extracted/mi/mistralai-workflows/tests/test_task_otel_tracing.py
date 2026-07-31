import json
import logging
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from mistralai.client import Mistral
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs.export import LogRecordExportResult
from opentelemetry.sdk.metrics.export import MetricExportResult, MetricsData
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExportResult
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.trace import SpanKind, StatusCode
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.core.task.task import Task
from mistralai.workflows.core.tracing._otel_config import (
    FORCE_SPAN_ID_ATTRIBUTE,
    FORCE_TRACE_ID_ATTRIBUTE,
    WORKFLOW_ROOT_ID_GENERATOR,
)
from mistralai.workflows.models import EventSpanType

from .fixtures_task import (
    FailingTaskNoRetryWorkflow,
    NestedTasksWorkflow,
    SimpleTaskWorkflow,
    StatefulTaskWorkflow,
    failing_task_no_retry_activity,
    nested_tasks_activity,
    simple_task_activity,
    stateful_task_activity,
)
from .utils import create_test_worker, create_test_worker_with_events

# Module-level exporter/provider (avoids "Overriding TracerProvider" warnings); the forced id
# generator lets the interceptor materialize the root with the id other spans parent onto.
_exporter = InMemorySpanExporter()
_provider = TracerProvider(id_generator=WORKFLOW_ROOT_ID_GENERATOR)
_provider.add_span_processor(SimpleSpanProcessor(_exporter))
trace.set_tracer_provider(_provider)


@pytest.fixture(autouse=True)
def clear_spans():
    _exporter.clear()
    yield
    _exporter.clear()


def get_task_spans() -> list:
    return [s for s in _exporter.get_finished_spans() if s.name.startswith("Task:")]


def _lifecycle_spans(spans: list, lifecycle: str) -> list:
    return [s for s in spans if s.attributes and s.attributes.get("task.lifecycle") == lifecycle]


def _type_spans(spans: list, task_type: str) -> list:
    return [s for s in spans if s.attributes and s.attributes.get("task.type") == task_type]


@pytest.mark.asyncio
async def test_task_span_lifecycle(temporal_env: WorkflowEnvironment) -> None:
    mock_client = AsyncMock(spec=Mistral)
    mock_client.send_event = AsyncMock()

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[SimpleTaskWorkflow],
            activities=[simple_task_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "simple_task_workflow",
                id="test-task-span-lifecycle",
                task_queue="test-task-queue",
            )
            await handle.result()

    task_spans = get_task_spans()
    assert len(task_spans) == 2, f"Expected 2 Task spans (started + completed), got {len(task_spans)}"

    started = _lifecycle_spans(task_spans, "started")
    completed = _lifecycle_spans(task_spans, "completed")
    assert len(started) == 1
    assert len(completed) == 1

    # Verify base attributes on the started span
    s = started[0]
    assert s.name == "Task:test_task"
    assert s.kind == SpanKind.INTERNAL
    assert s.attributes is not None
    assert s.attributes.get("task.id") is not None
    assert s.attributes.get("task.type") == "test_task"
    assert s.attributes.get("wf.type") == EventSpanType.custom_task
    assert s.status.status_code == StatusCode.OK

    # Activity-context attributes
    assert s.attributes.get("wf.activity.type") == "simple_task_activity"
    assert s.attributes.get("wf.activity.attempt") == 1
    assert s.attributes.get("wf.workflow.id") is not None
    assert s.attributes.get("wf.run.id") is not None
    assert s.attributes.get("wf.task_queue") == "test-task-queue"

    # Completed span is a child of the started span
    c = completed[0]
    assert c.status.status_code == StatusCode.OK
    assert c.parent is not None
    assert c.parent.span_id == s.context.span_id

    # Both spans are 0-time (ended immediately)
    for span in task_spans:
        assert span.end_time is not None
        assert span.start_time is not None
        assert span.end_time - span.start_time < 1e9, "Span duration should be < 1s (0-time span)"


@pytest.mark.asyncio
async def test_workflow_spans_nest_under_materialized_workflow_root(temporal_env: WorkflowEnvironment) -> None:
    from mistralai.workflows.core._events.event_interceptor import EventInterceptor
    from mistralai.workflows.core.tracing._temporal_tracing_interceptor import (
        get_span_recording_interceptors,
        get_trace_context_interceptors,
    )

    mock_client = AsyncMock(spec=Mistral)
    mock_client.send_event = AsyncMock()

    async with EventContext(mock_client):
        async with create_test_worker(
            temporal_env,
            workflows=[SimpleTaskWorkflow],
            activities=[simple_task_activity],
            # Full interceptor stack (matching the worker) so ExecuteActivity spans are emitted too.
            interceptors=[*get_trace_context_interceptors(), EventInterceptor(), *get_span_recording_interceptors()],
        ):
            handle = await temporal_env.client.start_workflow(
                "simple_task_workflow",
                id="test-workflow-root-parenting",
                task_queue="test-task-queue",
            )
            await handle.result()

    spans = _exporter.get_finished_spans()
    root = [s for s in spans if s.name.startswith("StartWorkflow:")]
    assert len(root) == 1, f"expected exactly one materialized StartWorkflow root span, got {[s.name for s in root]}"
    root_span_id = root[0].context.span_id
    assert root[0].parent is None or root[0].parent.span_id != root_span_id

    # The force-id attributes are popped host-side and must never reach the exported span.
    root_attrs = root[0].attributes or {}
    assert FORCE_TRACE_ID_ATTRIBUTE not in root_attrs and FORCE_SPAN_ID_ATTRIBUTE not in root_attrs

    # RunWorkflow and the internal lifecycle activities are peers under the materialized root.
    run_workflow = [s for s in spans if s.name.startswith("RunWorkflow:")]
    internal_starts = [s for s in spans if s.name.startswith("StartActivity:__internal__")]
    assert internal_starts, "expected internal __internal__ StartActivity spans"
    for span in run_workflow + internal_starts:
        assert span.parent is not None
        assert span.parent.span_id == root_span_id, (
            f"{span.name} should be a child of the StartWorkflow root, got parent {span.parent.span_id:016x}"
        )

    # RunWorkflow/CompleteWorkflow (contrib) and ExecuteActivity (ours) all carry temporalWorkflowID,
    # so the trace filter keeps them even for child executions (which emit no StartWorkflow root).
    tagged = [s for s in spans if s.name.startswith(("RunWorkflow:", "CompleteWorkflow:", "ExecuteActivity:"))]
    assert {"RunWorkflow", "CompleteWorkflow", "ExecuteActivity"} <= {s.name.split(":")[0] for s in tagged}
    for span in tagged:
        assert span.attributes and span.attributes.get("temporalWorkflowID"), (
            f"{span.name} must carry temporalWorkflowID for trace scoping"
        )


@pytest.mark.asyncio
async def test_stateful_task_state_updates(temporal_env: WorkflowEnvironment) -> None:
    mock_client = AsyncMock(spec=Mistral)
    mock_client.send_event = AsyncMock()

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[StatefulTaskWorkflow],
            activities=[stateful_task_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "stateful_task_workflow",
                0,
                id="test-stateful-task-span",
                task_queue="test-task-queue",
            )
            await handle.result()

    task_spans = _type_spans(get_task_spans(), "stateful_task")
    # 1 started + 2 state_updated + 1 completed = 4
    assert len(task_spans) == 4, f"Expected 4 stateful_task spans, got {len(task_spans)}"

    started = _lifecycle_spans(task_spans, "started")
    state_updated = _lifecycle_spans(task_spans, "state_updated")
    completed = _lifecycle_spans(task_spans, "completed")
    assert len(started) == 1
    assert len(state_updated) == 2
    assert len(completed) == 1

    # Started span carries initial state
    assert started[0].attributes["task.has_state"] is True
    initial_state = json.loads(started[0].attributes["task.initial_state"])
    assert initial_state["progress"] == 0
    assert initial_state["status"] == "pending"

    # State updates are ordered by time and carry previews
    state_updated.sort(key=lambda s: s.start_time)

    state_1 = json.loads(state_updated[0].attributes["task.state_preview"])
    assert state_1["progress"] == 50
    assert state_1["status"] == "processing"

    state_2 = json.loads(state_updated[1].attributes["task.state_preview"])
    assert state_2["progress"] == 100
    assert state_2["status"] == "completed"

    # Completed span carries final state
    final_state = json.loads(completed[0].attributes["task.final_state"])
    assert final_state["progress"] == 100
    assert final_state["status"] == "completed"


@pytest.mark.asyncio
async def test_failed_task_records_error(temporal_env: WorkflowEnvironment) -> None:
    mock_client = AsyncMock(spec=Mistral)
    mock_client.send_event = AsyncMock()

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[FailingTaskNoRetryWorkflow],
            activities=[failing_task_no_retry_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "failing_task_no_retry_workflow",
                id="test-failed-task-span",
                task_queue="test-task-queue",
            )
            try:
                await handle.result()
            except Exception:
                pass  # Expected failure

    task_spans = _type_spans(get_task_spans(), "failing_task")
    assert len(task_spans) == 2, f"Expected 2 failing_task spans, got {len(task_spans)}"

    started = _lifecycle_spans(task_spans, "started")
    failed = _lifecycle_spans(task_spans, "failed")
    assert len(started) == 1
    assert len(failed) == 1

    # Started span succeeded
    assert started[0].status.status_code == StatusCode.OK

    # Failed span has ERROR status and error details
    f = failed[0]
    assert f.status.status_code == StatusCode.ERROR
    assert "Intentional test error" in str(f.attributes.get("error.message", ""))

    # Failed span is child of started span
    assert f.parent is not None
    assert f.parent.span_id == started[0].context.span_id


@pytest.mark.asyncio
async def test_nested_tasks_create_parent_child_spans(temporal_env: WorkflowEnvironment) -> None:
    mock_client = AsyncMock(spec=Mistral)
    mock_client.send_event = AsyncMock()

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[NestedTasksWorkflow],
            activities=[nested_tasks_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "nested_tasks_workflow",
                id="test-nested-task-spans",
                task_queue="test-task-queue",
            )
            await handle.result()

    all_task_spans = get_task_spans()

    outer_spans = _type_spans(all_task_spans, "outer_task")
    inner_spans = _type_spans(all_task_spans, "inner_task")

    outer_started = _lifecycle_spans(outer_spans, "started")
    inner_started = _lifecycle_spans(inner_spans, "started")

    assert len(outer_started) == 1, "Expected 1 outer_task started span"
    assert len(inner_started) == 1, "Expected 1 inner_task started span"

    outer_root = outer_started[0]
    inner_root = inner_started[0]

    # Inner task's started span is a child of the outer task's started span
    assert inner_root.parent is not None, "Inner started span should have a parent"
    assert inner_root.parent.span_id == outer_root.context.span_id, (
        "Inner started span's parent should be the outer started span"
    )

    # Both share the same trace
    assert inner_root.context.trace_id == outer_root.context.trace_id, "Nested spans should share the same trace_id"

    # All non-started spans within a task are children of their task's started span
    for span in outer_spans:
        if span.attributes.get("task.lifecycle") != "started":
            assert span.parent is not None
            assert span.parent.span_id == outer_root.context.span_id

    for span in inner_spans:
        if span.attributes.get("task.lifecycle") != "started":
            assert span.parent is not None
            assert span.parent.span_id == inner_root.context.span_id


_NOT_FOUND_RESPONSE = SimpleNamespace(ok=False, status_code=404, text="not found", reason="Not Found")
_FORBIDDEN_RESPONSE = SimpleNamespace(ok=False, status_code=403, text="forbidden", reason="Forbidden")


def test_span_export_failure_warns_with_404_hint_and_status() -> None:
    from mistralai.workflows.core.tracing import _otel_config
    from mistralai.workflows.core.tracing._otel_config import _LoggingOTLPSpanExporter

    exporter = _LoggingOTLPSpanExporter(endpoint="http://invalid-endpoint:4318/v1/traces")
    with patch.object(OTLPSpanExporter, "_export", return_value=_NOT_FOUND_RESPONSE):
        with patch("mistralai.workflows.core.tracing._otel_config.logger.warning") as mock_warning:
            result = exporter.export([])

    assert result is SpanExportResult.FAILURE
    mock_warning.assert_called_once_with(
        f"Failed to export OpenTelemetry traces: {_otel_config._OTLP_404_HINT}",
        endpoint="http://invalid-endpoint:4318/v1/traces",
        status_code=404,
    )


def test_metric_export_failure_warns_with_404_hint_and_status() -> None:
    from mistralai.workflows.core.tracing import _otel_config
    from mistralai.workflows.core.tracing._otel_config import _LoggingOTLPMetricExporter

    exporter = _LoggingOTLPMetricExporter(endpoint="http://invalid-endpoint:4318/v1/metrics")
    with patch.object(OTLPMetricExporter, "_export", return_value=_NOT_FOUND_RESPONSE):
        with patch("mistralai.workflows.core.tracing._otel_config.logger.warning") as mock_warning:
            result = exporter.export(MetricsData(resource_metrics=[]))

    assert result is MetricExportResult.FAILURE
    mock_warning.assert_called_once_with(
        f"Failed to export OpenTelemetry metrics: {_otel_config._OTLP_404_HINT}",
        endpoint="http://invalid-endpoint:4318/v1/metrics",
        status_code=404,
    )


def test_log_export_failure_warns_with_404_hint_and_status() -> None:
    from mistralai.workflows.core.tracing import _otel_config
    from mistralai.workflows.core.tracing._otel_config import _LoggingOTLPLogExporter

    exporter = _LoggingOTLPLogExporter(endpoint="http://invalid-endpoint:4318/v1/logs")
    with patch.object(OTLPLogExporter, "_export", return_value=_NOT_FOUND_RESPONSE):
        with patch("mistralai.workflows.core.tracing._otel_config.logger.warning") as mock_warning:
            result = exporter.export([])

    assert result is LogRecordExportResult.FAILURE
    mock_warning.assert_called_once_with(
        f"Failed to export OpenTelemetry logs: {_otel_config._OTLP_404_HINT}",
        endpoint="http://invalid-endpoint:4318/v1/logs",
        status_code=404,
    )


def test_non_404_export_failure_reports_status_without_hint() -> None:
    from mistralai.workflows.core.tracing import _otel_config
    from mistralai.workflows.core.tracing._otel_config import _LoggingOTLPSpanExporter

    exporter = _LoggingOTLPSpanExporter(endpoint="http://invalid-endpoint:4318/v1/traces")
    with patch.object(OTLPSpanExporter, "_export", return_value=_FORBIDDEN_RESPONSE):
        with patch("mistralai.workflows.core.tracing._otel_config.logger.warning") as mock_warning:
            result = exporter.export([])

    assert result is SpanExportResult.FAILURE
    mock_warning.assert_called_once_with(
        "Failed to export OpenTelemetry traces", endpoint=exporter._endpoint, status_code=403
    )
    assert _otel_config._OTLP_404_HINT not in mock_warning.call_args_list[0].args[0]


def test_export_failure_warning_is_throttled_per_interval() -> None:
    from mistralai.workflows.core.tracing import _otel_config
    from mistralai.workflows.core.tracing._otel_config import _LoggingOTLPSpanExporter

    exporter = _LoggingOTLPSpanExporter(endpoint="http://invalid-endpoint:4318/v1/traces")
    # 1st call logs, 2nd (1s later) is suppressed, 3rd (past the interval) logs again with the count.
    clock = iter([100.0, 101.0, 101.0 + _otel_config._EXPORT_WARN_INTERVAL_SECONDS + 1.0])
    with patch.object(OTLPSpanExporter, "_export", return_value=_NOT_FOUND_RESPONSE):
        with patch("mistralai.workflows.core.tracing._otel_config.time.monotonic", side_effect=lambda: next(clock)):
            with patch("mistralai.workflows.core.tracing._otel_config.logger.warning") as mock_warning:
                exporter.export([])
                exporter.export([])
                exporter.export([])

    assert mock_warning.call_count == 2
    assert mock_warning.call_args_list[1].kwargs["suppressed_failures"] == 1


def test_export_diagnostics_filter_excludes_otel_from_log_export() -> None:
    from mistralai.workflows.core.tracing import _otel_config
    from mistralai.workflows.core.tracing._otel_config import _DropOtelExportDiagnosticsFilter

    log_filter = _DropOtelExportDiagnosticsFilter()

    def record(name: str) -> logging.LogRecord:
        return logging.LogRecord(name, logging.WARNING, __file__, 0, "msg", None, None)

    # Our own export-failure warnings and OTel SDK logs must not be re-exported (feedback loop),
    # while application logs still flow to the OTel log exporter.
    assert log_filter.filter(record(_otel_config.__name__)) is False
    assert log_filter.filter(record("opentelemetry.exporter.otlp.proto.http._log_exporter")) is False
    assert log_filter.filter(record("mistralai.workflows.core.worker")) is True


@pytest.mark.asyncio
async def test_aenter_failure_restores_otel_context() -> None:
    context_before = trace.get_current_span().get_span_context()

    with patch(
        "mistralai.workflows.core.task.task.should_publish_event",
        return_value=True,
    ):
        # create_base_event_fields() raises NotInTemporalContextError outside Temporal
        with pytest.raises(Exception):
            await Task(type="ctx_leak_test").__aenter__()

    context_after = trace.get_current_span().get_span_context()
    assert context_before == context_after, "OTEL context should be restored after __aenter__ failure"
