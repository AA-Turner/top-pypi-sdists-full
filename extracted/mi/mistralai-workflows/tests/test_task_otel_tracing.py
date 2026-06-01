import json
from unittest.mock import AsyncMock, patch

import pytest
from mistralai.client import Mistral
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.trace import SpanKind, StatusCode
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.core.task.task import Task
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
from .utils import create_test_worker_with_events

# Module-level exporter and provider to avoid "Overriding TracerProvider" warnings
_exporter = InMemorySpanExporter()
_provider = TracerProvider()
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
