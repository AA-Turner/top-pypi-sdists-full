from typing import Any

import pytest
from temporalio.client import WorkflowFailureError
from temporalio.exceptions import ApplicationError, CancelledError
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.protocol.v1.events import CustomTaskCompleted
from mistralai.workflows.testing import (
    activity_completed,
    activity_started,
    compare_itemwise,
    custom_task_completed,
    custom_task_failed,
    custom_task_started,
    workflow_canceled,
    workflow_completed,
    workflow_failed,
    workflow_started,
)

from .fixtures_interactive_workflow import (
    BasicWorkflow,
    SimpleApprovalWorkflow,
    TimeoutTestWorkflow,
    WorkflowWithValidationFailure,
)
from .utils import create_capturing_mock_events_client, create_test_worker_with_events, wait_for_pending_inputs


@pytest.mark.asyncio
async def test_basic_workflow_emits_lifecycle_events(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []

    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[BasicWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "basic_workflow",
                {"value": "test-value"},
                id="test-basic-workflow-events",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            assert result["result"]["status"] == "completed"
            assert result["result"]["value"] == "test-value"

            expected_events = [
                activity_started("__internal__emit_workflow_started", workflow_name="basic_workflow"),
                workflow_started("basic_workflow"),
                activity_completed("__internal__emit_workflow_started", workflow_name="basic_workflow"),
                activity_started("__internal__emit_workflow_completed", workflow_name="basic_workflow"),
                workflow_completed("basic_workflow"),
                activity_completed("__internal__emit_workflow_completed", workflow_name="basic_workflow"),
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
async def test_wait_for_input_emits_lifecycle_events(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []

    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[SimpleApprovalWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "simple_approval_workflow",
                {"request_id": "req-event-test", "description": "Test event emission"},
                id="test-wait-for-input-events",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            pending_task_id = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {"task_id": pending_task_id, "input": {"approved": True, "reason": "Test"}},
            )

            result = await handle.result()
            assert result["status"] == "approved"

            expected_events = [
                activity_started("__internal__emit_workflow_started", workflow_name="simple_approval_workflow"),
                workflow_started("simple_approval_workflow"),
                activity_completed("__internal__emit_workflow_started", workflow_name="simple_approval_workflow"),
                activity_started("__emit_waiting_for_input_started", workflow_name="simple_approval_workflow"),
                custom_task_started("wait_for_input", {}, workflow_name="simple_approval_workflow"),
                activity_completed("__emit_waiting_for_input_started", workflow_name="simple_approval_workflow"),
                activity_started("__emit_waiting_for_input_completed", workflow_name="simple_approval_workflow"),
                custom_task_completed(
                    "wait_for_input",
                    {},
                    workflow_name="simple_approval_workflow",
                ),
                activity_completed("__emit_waiting_for_input_completed", workflow_name="simple_approval_workflow"),
                activity_started("__internal__emit_workflow_completed", workflow_name="simple_approval_workflow"),
                workflow_completed("simple_approval_workflow"),
                activity_completed("__internal__emit_workflow_completed", workflow_name="simple_approval_workflow"),
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
                    "attributes.custom_task_id",
                    "attributes.input",
                    "attributes.result",
                    "attributes.payload",
                },
            )
            assert len(errors) == 0, "Event sequence mismatch:\n" + "\n".join(errors)

            # Ensure wait_for_input completed task event contains input params
            workflow_completed_event = next(
                event for event in captured_events if isinstance(event, CustomTaskCompleted)
            )
            assert workflow_completed_event.attributes.payload.value.get("input") == {
                "approved": True,
                "reason": "Test",
            }


@pytest.mark.asyncio
async def test_wait_for_input_emits_failed_event_on_validation_error(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []

    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[WorkflowWithValidationFailure],
        ):
            handle = await temporal_env.client.start_workflow(
                "workflow_with_validation_failure",
                {"request_id": "req-validation-test"},
                id="test-validation-failure",
                task_queue="test-task-queue",
            )

            result = await handle.result()
            assert result["status"] == "error"

            expected_events = [
                activity_started(
                    "__internal__emit_workflow_started",
                    workflow_name="workflow_with_validation_failure",
                ),
                workflow_started("workflow_with_validation_failure"),
                activity_completed(
                    "__internal__emit_workflow_started",
                    workflow_name="workflow_with_validation_failure",
                ),
                activity_started(
                    "__emit_waiting_for_input_started",
                    workflow_name="workflow_with_validation_failure",
                ),
                custom_task_started(
                    "wait_for_input",
                    {},
                    workflow_name="workflow_with_validation_failure",
                ),
                activity_completed(
                    "__emit_waiting_for_input_started",
                    workflow_name="workflow_with_validation_failure",
                ),
                activity_started(
                    "__emit_waiting_for_input_failed",
                    workflow_name="workflow_with_validation_failure",
                ),
                custom_task_failed(
                    "wait_for_input",
                    "",
                    workflow_name="workflow_with_validation_failure",
                ),
                activity_completed(
                    "__emit_waiting_for_input_failed",
                    workflow_name="workflow_with_validation_failure",
                ),
                activity_started(
                    "__internal__emit_workflow_completed",
                    workflow_name="workflow_with_validation_failure",
                ),
                workflow_completed("workflow_with_validation_failure"),
                activity_completed(
                    "__internal__emit_workflow_completed",
                    workflow_name="workflow_with_validation_failure",
                ),
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
                    "attributes.custom_task_id",
                    "attributes.input",
                    "attributes.result",
                    "attributes.payload",
                    "attributes.failure.message",
                },
            )
            assert len(errors) == 0, "Event sequence mismatch:\n" + "\n".join(errors)


@pytest.mark.asyncio
async def test_wait_for_input_emits_failed_event_on_cancellation(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []

    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[SimpleApprovalWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "simple_approval_workflow",
                {"request_id": "req-cancel-test", "description": "Test cancellation"},
                id="test-wait-for-input-cancel",
                task_queue="test-task-queue",
            )

            await wait_for_pending_inputs(handle, expected_count=1)

            await handle.cancel()

            # Wait for workflow to complete with cancellation
            with pytest.raises(WorkflowFailureError) as exc_info:
                await handle.result()

            assert isinstance(exc_info.value.cause, CancelledError)

            expected_events = [
                activity_started("__internal__emit_workflow_started", workflow_name="simple_approval_workflow"),
                workflow_started("simple_approval_workflow"),
                activity_completed("__internal__emit_workflow_started", workflow_name="simple_approval_workflow"),
                activity_started("__emit_waiting_for_input_started", workflow_name="simple_approval_workflow"),
                custom_task_started("wait_for_input", {}, workflow_name="simple_approval_workflow"),
                activity_completed("__emit_waiting_for_input_started", workflow_name="simple_approval_workflow"),
                activity_started("__emit_waiting_for_input_failed", workflow_name="simple_approval_workflow"),
                custom_task_failed(
                    "wait_for_input",
                    "",
                    workflow_name="simple_approval_workflow",
                ),
                activity_completed("__emit_waiting_for_input_failed", workflow_name="simple_approval_workflow"),
                activity_started("__internal__emit_workflow_canceled", workflow_name="simple_approval_workflow"),
                workflow_canceled("simple_approval_workflow"),
                activity_completed("__internal__emit_workflow_canceled", workflow_name="simple_approval_workflow"),
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
                    "attributes.custom_task_id",
                    "attributes.input",
                    "attributes.result",
                    "attributes.payload",
                    "attributes.failure.message",
                    "attributes.reason",
                },
            )
            assert len(errors) == 0, "Event sequence mismatch:\n" + "\n".join(errors)


@pytest.mark.asyncio
async def test_wait_for_input_timeout(temporal_env: WorkflowEnvironment) -> None:
    """Test that wait_for_input respects the timeout parameter."""
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[TimeoutTestWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "simple_approval_workflow_with_timeout",
                {},
                id="test-wait-for-input-timeout",
                task_queue="test-task-queue",
            )

            # Wait for workflow to complete with timeout
            with pytest.raises(WorkflowFailureError) as exc_info:
                await handle.result()

            assert isinstance(exc_info.value.cause, ApplicationError)
            assert "TimeoutError" in str(exc_info.value.cause)

            # Verify events were emitted correctly
            expected_events = [
                activity_started(
                    "__internal__emit_workflow_started", workflow_name="simple_approval_workflow_with_timeout"
                ),
                workflow_started("simple_approval_workflow_with_timeout"),
                activity_completed(
                    "__internal__emit_workflow_started", workflow_name="simple_approval_workflow_with_timeout"
                ),
                activity_started(
                    "__emit_waiting_for_input_started", workflow_name="simple_approval_workflow_with_timeout"
                ),
                custom_task_started("wait_for_input", {}, workflow_name="simple_approval_workflow_with_timeout"),
                activity_completed(
                    "__emit_waiting_for_input_started", workflow_name="simple_approval_workflow_with_timeout"
                ),
                activity_started(
                    "__emit_waiting_for_input_failed", workflow_name="simple_approval_workflow_with_timeout"
                ),
                custom_task_failed("wait_for_input", "", workflow_name="simple_approval_workflow_with_timeout"),
                activity_completed(
                    "__emit_waiting_for_input_failed", workflow_name="simple_approval_workflow_with_timeout"
                ),
                activity_started(
                    "__internal__emit_workflow_failed", workflow_name="simple_approval_workflow_with_timeout"
                ),
                workflow_failed("simple_approval_workflow_with_timeout"),
                activity_completed(
                    "__internal__emit_workflow_failed", workflow_name="simple_approval_workflow_with_timeout"
                ),
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
                    "attributes.custom_task_id",
                    "attributes.input",
                    "attributes.result",
                    "attributes.payload",
                    "attributes.failure.message",
                },
            )
            assert len(errors) == 0, "Event sequence mismatch:\n" + "\n".join(errors)
