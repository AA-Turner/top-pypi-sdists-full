import asyncio
from typing import Any

import pytest
from temporalio.client import WorkflowFailureError
from temporalio.common import RetryPolicy
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.core.temporal.context_handler_interceptor import ContextHandlerInterceptor
from mistralai.workflows.protocol.v1.events import WorkflowExecutionStarted
from mistralai.workflows.testing import (
    activity_completed,
    activity_started,
    compare_itemwise,
    workflow_completed,
    workflow_failed,
    workflow_started,
)

from .fixtures import (
    CANParams,
    ChildWorkflow,
    ContinueAsNewWorkflow,
    FailingWorkflow,
    ParentWorkflow,
    PureWorkflow,
    RetryingWorkflow,
    WorkflowWithDisplayName,
)
from .utils import create_capturing_mock_events_client, create_test_worker_with_events


@pytest.mark.asyncio
async def test_basic_workflow_emits_lifecycle_events(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[PureWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "pure_workflow",
                {"name": "test-value"},
                id="test-basic-workflow-events",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            assert result["result"] == "Workflow says: test-value"

            expected_events = [
                activity_started("__internal__emit_workflow_started", workflow_name="pure_workflow"),
                workflow_started("pure_workflow"),
                activity_completed("__internal__emit_workflow_started", workflow_name="pure_workflow"),
                activity_started("__internal__emit_workflow_completed", workflow_name="pure_workflow"),
                workflow_completed("pure_workflow"),
                activity_completed("__internal__emit_workflow_completed", workflow_name="pure_workflow"),
            ]

            errors = compare_itemwise(
                expected_events,
                captured_events,
                exclude_paths={
                    "event_id",
                    "event_timestamp",
                    "root_workflow_exec_id",
                    "parent_workflow_exec_id",
                    "workflow_exec_id",
                    "workflow_run_id",
                    "attributes.task_id",
                    "attributes.input",
                    "attributes.result",
                },
            )
            assert len(errors) == 0, "Event sequence mismatch:\n" + "\n".join(errors)


@pytest.mark.asyncio
async def test_child_workflow_started_event_has_parent_exec_id(
    temporal_env_with_converter: WorkflowEnvironment,
) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env_with_converter,
            workflows=[ParentWorkflow, ChildWorkflow],
            interceptors=[ContextHandlerInterceptor()],
        ):
            handle = await temporal_env_with_converter.client.start_workflow(
                "parent_workflow",
                "test-child-events",
                id="test-child-parent-exec-id",
                task_queue="test-task-queue",
            )
            await handle.result()

    started_events = [e for e in captured_events if isinstance(e, WorkflowExecutionStarted)]
    parent_started = next(e for e in started_events if e.workflow_name == "parent_workflow")
    child_started = next(e for e in started_events if e.workflow_name == "child_workflow")

    assert parent_started.parent_workflow_exec_id is None
    assert child_started.parent_workflow_exec_id == parent_started.workflow_exec_id


@pytest.mark.asyncio
async def test_workflow_started_event_includes_display_name(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[WorkflowWithDisplayName],
        ):
            handle = await temporal_env.client.start_workflow(
                "workflow_with_display_name",
                {"name": "test-value"},
                id="test-display-name-events",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            assert result["result"] == "Display name workflow says: test-value"

            started_events = [e for e in captured_events if isinstance(e, WorkflowExecutionStarted)]
            assert len(started_events) == 1
            assert started_events[0].attributes.display_name == "My Friendly Workflow"


@pytest.mark.asyncio
async def test_workflow_started_event_display_name_is_none_when_not_set(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[PureWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "pure_workflow",
                {"name": "test-value"},
                id="test-no-display-name-events",
                task_queue="test-task-queue",
            )

            await handle.result()

            started_events = [e for e in captured_events if isinstance(e, WorkflowExecutionStarted)]
            assert len(started_events) == 1
            assert started_events[0].attributes.display_name is None


@pytest.mark.asyncio
async def test_workflow_failure_emits_failed_event(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[FailingWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "failing_workflow",
                {"message": "test-error"},
                id="test-workflow-failure-events",
                retry_policy=RetryPolicy(maximum_attempts=1),
                task_queue="test-task-queue",
            )

            async def wait_for_events(expected_count: int, timeout_seconds: float = 5.0) -> None:
                loop = asyncio.get_running_loop()
                deadline = loop.time() + timeout_seconds
                while loop.time() < deadline:
                    if len(captured_events) >= expected_count:
                        return
                    await asyncio.sleep(0.1)
                raise TimeoutError("Did not receive expected workflow events in time")

            await wait_for_events(expected_count=6)

            with pytest.raises(WorkflowFailureError) as exc_info:
                await handle.result()
            assert "Intentional failure: test-error" in str(exc_info.value.cause)

            expected_events = [
                activity_started("__internal__emit_workflow_started", workflow_name="failing_workflow"),
                workflow_started("failing_workflow"),
                activity_completed("__internal__emit_workflow_started", workflow_name="failing_workflow"),
                activity_started("__internal__emit_workflow_failed", workflow_name="failing_workflow"),
                workflow_failed("failing_workflow"),
                activity_completed("__internal__emit_workflow_failed", workflow_name="failing_workflow"),
            ]

            errors = compare_itemwise(
                expected_events,
                captured_events,
                exclude_paths={
                    "event_id",
                    "event_timestamp",
                    "root_workflow_exec_id",
                    "parent_workflow_exec_id",
                    "workflow_exec_id",
                    "workflow_run_id",
                    "attributes.task_id",
                    "attributes.input",
                    "attributes.result",
                    "attributes.failure.message",
                },
            )
            assert len(errors) == 0, "Event sequence mismatch:\n" + "\n".join(errors)


@pytest.mark.asyncio
async def test_continue_as_new_event_has_continued_run_id(
    temporal_env_with_converter: WorkflowEnvironment,
) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env_with_converter,
            workflows=[ContinueAsNewWorkflow],
            interceptors=[ContextHandlerInterceptor()],
        ):
            handle = await temporal_env_with_converter.client.start_workflow(
                "test-events-can-workflow",
                CANParams(iteration=0),
                id="test-can-continued-run-id",
                task_queue="test-task-queue",
            )
            await handle.result()

    started_events = [
        e
        for e in captured_events
        if isinstance(e, WorkflowExecutionStarted) and e.workflow_name == "test-events-can-workflow"
    ]
    assert len(started_events) == 2

    first_run = started_events[0]
    second_run = started_events[1]

    assert first_run.continued_run_id is None
    assert second_run.continued_run_id == first_run.workflow_run_id


@pytest.mark.asyncio
async def test_retrying_workflow_has_attempt_and_continued_run_id(
    temporal_env_with_converter: WorkflowEnvironment,
) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env_with_converter,
            workflows=[RetryingWorkflow],
            interceptors=[ContextHandlerInterceptor()],
        ):
            handle = await temporal_env_with_converter.client.start_workflow(
                "test-events-retrying-workflow",
                id="test-retrying-workflow-events",
                task_queue="test-task-queue",
                retry_policy=RetryPolicy(maximum_attempts=2),
            )
            await handle.result()

    started_events = [
        e
        for e in captured_events
        if isinstance(e, WorkflowExecutionStarted) and e.workflow_name == "test-events-retrying-workflow"
    ]
    assert len(started_events) == 2

    first_run = started_events[0]
    second_run = started_events[1]

    assert first_run.attributes.attempt == 1
    assert first_run.continued_run_id is None

    assert second_run.attributes.attempt == 2
    assert second_run.continued_run_id == first_run.workflow_run_id
