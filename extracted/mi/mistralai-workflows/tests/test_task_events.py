from typing import Any

import pytest
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.protocol.v1.events import JSONPatchPayload, JSONPatchReplace
from mistralai.workflows.testing import (
    activity_completed,
    activity_started,
    compare_itemwise,
    custom_task_completed,
    custom_task_in_progress,
    custom_task_started,
    workflow_completed,
    workflow_started,
)

from .fixtures_task import (
    NestedTasksWorkflow,
    SimpleTaskWorkflow,
    StatefulTaskWorkflow,
    TaskInWorkflowWorkflow,
    nested_tasks_activity,
    simple_task_activity,
    stateful_task_activity,
)
from .utils import create_capturing_mock_events_client, create_test_worker_with_events


@pytest.mark.asyncio
async def test_simple_task_in_activity_emits_events(temporal_env: WorkflowEnvironment) -> None:
    """Test that a simple task in an activity emits started and completed events."""
    captured_events: list[Any] = []

    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[SimpleTaskWorkflow],
            activities=[simple_task_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "simple_task_workflow",
                id="test-simple-task-events",
                task_queue="test-task-queue",
            )
            await handle.result()

            expected_events = [
                activity_started(
                    "__internal__emit_workflow_started",
                    workflow_name="simple_task_workflow",
                ),
                workflow_started("simple_task_workflow"),
                activity_completed(
                    "__internal__emit_workflow_started",
                    workflow_name="simple_task_workflow",
                ),
                activity_started(
                    "simple_task_activity",
                    workflow_name="simple_task_workflow",
                ),
                custom_task_started("test_task", {}, workflow_name="simple_task_workflow"),
                custom_task_completed("test_task", {}, workflow_name="simple_task_workflow"),
                activity_completed(
                    "simple_task_activity",
                    workflow_name="simple_task_workflow",
                ),
                activity_started(
                    "__internal__emit_workflow_completed",
                    workflow_name="simple_task_workflow",
                ),
                workflow_completed("simple_task_workflow"),
                activity_completed(
                    "__internal__emit_workflow_completed",
                    workflow_name="simple_task_workflow",
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
                },
            )
            assert len(errors) == 0, "Event sequence mismatch:\n" + "\n".join(errors)


@pytest.mark.asyncio
async def test_stateful_task_emits_in_progress_events(temporal_env: WorkflowEnvironment) -> None:
    """Test that a task with state updates emits in_progress events."""
    captured_events: list[Any] = []

    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[StatefulTaskWorkflow],
            activities=[stateful_task_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "stateful_task_workflow",
                0,
                id="test-stateful-task-events",
                task_queue="test-task-queue",
            )
            await handle.result()

            expected_events = [
                activity_started(
                    "__internal__emit_workflow_started",
                    workflow_name="stateful_task_workflow",
                ),
                workflow_started("stateful_task_workflow"),
                activity_completed(
                    "__internal__emit_workflow_started",
                    workflow_name="stateful_task_workflow",
                ),
                activity_started(
                    "stateful_task_activity",
                    workflow_name="stateful_task_workflow",
                ),
                custom_task_started(
                    "stateful_task",
                    {"progress": 0, "status": "pending"},
                    workflow_name="stateful_task_workflow",
                ),
                custom_task_in_progress(
                    "stateful_task",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/status", value="processing", op="replace"),
                            JSONPatchReplace(path="/progress", value=50, op="replace"),
                        ]
                    ),
                    workflow_name="stateful_task_workflow",
                ),
                custom_task_in_progress(
                    "stateful_task",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/status", value="completed", op="replace"),
                            JSONPatchReplace(path="/progress", value=100, op="replace"),
                        ]
                    ),
                    workflow_name="stateful_task_workflow",
                ),
                custom_task_completed(
                    "stateful_task",
                    {"progress": 100, "status": "completed"},
                    workflow_name="stateful_task_workflow",
                ),
                activity_completed(
                    "stateful_task_activity",
                    workflow_name="stateful_task_workflow",
                ),
                activity_started(
                    "__internal__emit_workflow_completed",
                    workflow_name="stateful_task_workflow",
                ),
                workflow_completed("stateful_task_workflow"),
                activity_completed(
                    "__internal__emit_workflow_completed",
                    workflow_name="stateful_task_workflow",
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
                    "attributes.payload.value",
                },
            )
            assert len(errors) == 0, "Event sequence mismatch:\n" + "\n".join(errors)


@pytest.mark.asyncio
async def test_nested_tasks_emit_hierarchical_events(temporal_env: WorkflowEnvironment) -> None:
    """Test that nested tasks emit events in the correct order."""
    captured_events: list[Any] = []

    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[NestedTasksWorkflow],
            activities=[nested_tasks_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "nested_tasks_workflow",
                id="test-nested-tasks-events",
                task_queue="test-task-queue",
            )
            await handle.result()

            expected_events = [
                activity_started(
                    "__internal__emit_workflow_started",
                    workflow_name="nested_tasks_workflow",
                ),
                workflow_started("nested_tasks_workflow"),
                activity_completed(
                    "__internal__emit_workflow_started",
                    workflow_name="nested_tasks_workflow",
                ),
                activity_started(
                    "nested_tasks_activity",
                    workflow_name="nested_tasks_workflow",
                ),
                custom_task_started(
                    "outer_task",
                    {"level": "outer"},
                    workflow_name="nested_tasks_workflow",
                ),
                custom_task_in_progress(
                    "outer_task",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/progress", value=50, op="replace"),
                        ]
                    ),
                    workflow_name="nested_tasks_workflow",
                ),
                custom_task_started(
                    "inner_task",
                    {"level": "inner"},
                    workflow_name="nested_tasks_workflow",
                ),
                custom_task_in_progress(
                    "inner_task",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/progress", value=100, op="replace"),
                        ]
                    ),
                    workflow_name="nested_tasks_workflow",
                ),
                custom_task_completed(
                    "inner_task",
                    {"level": "inner", "progress": 100},
                    workflow_name="nested_tasks_workflow",
                ),
                custom_task_in_progress(
                    "outer_task",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/progress", value=100, op="replace"),
                        ]
                    ),
                    workflow_name="nested_tasks_workflow",
                ),
                custom_task_completed(
                    "outer_task",
                    {"level": "outer", "progress": 100},
                    workflow_name="nested_tasks_workflow",
                ),
                activity_completed(
                    "nested_tasks_activity",
                    workflow_name="nested_tasks_workflow",
                ),
                activity_started(
                    "__internal__emit_workflow_completed",
                    workflow_name="nested_tasks_workflow",
                ),
                workflow_completed("nested_tasks_workflow"),
                activity_completed(
                    "__internal__emit_workflow_completed",
                    workflow_name="nested_tasks_workflow",
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
                    "attributes.payload.value",
                },
            )
            assert len(errors) == 0, "Event sequence mismatch:\n" + "\n".join(errors)


@pytest.mark.asyncio
async def test_task_in_workflow_uses_local_activities_for_events(
    temporal_env: WorkflowEnvironment,
) -> None:
    """Test that tasks in workflows emit events via local activities."""
    captured_events: list[Any] = []

    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[TaskInWorkflowWorkflow],
            activities=[simple_task_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "task_in_workflow",
                id="test-task-in-workflow-events",
                task_queue="test-task-queue",
            )
            await handle.result()

            expected_events = [
                activity_started(
                    "__internal__emit_workflow_started",
                    workflow_name="task_in_workflow",
                ),
                workflow_started("task_in_workflow"),
                activity_completed(
                    "__internal__emit_workflow_started",
                    workflow_name="task_in_workflow",
                ),
                activity_started(
                    "__internal__persist_task_span_context",
                    workflow_name="task_in_workflow",
                ),
                activity_completed(
                    "__internal__persist_task_span_context",
                    workflow_name="task_in_workflow",
                ),
                activity_started(
                    "__internal__emit_task_started",
                    workflow_name="task_in_workflow",
                ),
                custom_task_started(
                    "workflow_task",
                    {"progress": 0, "status": "pending"},
                    workflow_name="task_in_workflow",
                ),
                activity_completed(
                    "__internal__emit_task_started",
                    workflow_name="task_in_workflow",
                ),
                activity_started(
                    "__internal__emit_task_in_progress",
                    workflow_name="task_in_workflow",
                ),
                custom_task_in_progress(
                    "workflow_task",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/progress", value=50, op="replace"),
                            JSONPatchReplace(path="/status", value="processing", op="replace"),
                        ]
                    ),
                    workflow_name="task_in_workflow",
                ),
                activity_completed(
                    "__internal__emit_task_in_progress",
                    workflow_name="task_in_workflow",
                ),
                activity_started(
                    "simple_task_activity",
                    workflow_name="task_in_workflow",
                ),
                custom_task_started("test_task", {}, workflow_name="task_in_workflow"),
                custom_task_completed("test_task", {}, workflow_name="task_in_workflow"),
                activity_completed(
                    "simple_task_activity",
                    workflow_name="task_in_workflow",
                ),
                activity_started(
                    "__internal__emit_task_in_progress",
                    workflow_name="task_in_workflow",
                ),
                custom_task_in_progress(
                    "workflow_task",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/progress", value=100, op="replace"),
                            JSONPatchReplace(path="/status", value="completed", op="replace"),
                        ]
                    ),
                    workflow_name="task_in_workflow",
                ),
                activity_completed(
                    "__internal__emit_task_in_progress",
                    workflow_name="task_in_workflow",
                ),
                activity_started(
                    "__internal__emit_task_completed",
                    workflow_name="task_in_workflow",
                ),
                custom_task_completed(
                    "workflow_task",
                    {"progress": 100, "status": "completed"},
                    workflow_name="task_in_workflow",
                ),
                activity_completed(
                    "__internal__emit_task_completed",
                    workflow_name="task_in_workflow",
                ),
                activity_started(
                    "__internal__emit_workflow_completed",
                    workflow_name="task_in_workflow",
                ),
                workflow_completed("task_in_workflow"),
                activity_completed(
                    "__internal__emit_workflow_completed",
                    workflow_name="task_in_workflow",
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
                    "attributes.payload.value",
                },
            )
            assert len(errors) == 0, "Event sequence mismatch:\n" + "\n".join(errors)


@pytest.mark.asyncio
async def test_task_events_ordered_within_activity(temporal_env: WorkflowEnvironment) -> None:
    """Test that task events within a single activity maintain strict FIFO ordering."""
    captured_events: list[Any] = []

    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[StatefulTaskWorkflow],
            activities=[stateful_task_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "stateful_task_workflow",
                0,
                id="test-task-event-ordering",
                task_queue="test-task-queue",
            )
            await handle.result()

            expected_events = [
                activity_started(
                    "__internal__emit_workflow_started",
                    workflow_name="stateful_task_workflow",
                ),
                workflow_started("stateful_task_workflow"),
                activity_completed(
                    "__internal__emit_workflow_started",
                    workflow_name="stateful_task_workflow",
                ),
                activity_started(
                    "stateful_task_activity",
                    workflow_name="stateful_task_workflow",
                ),
                custom_task_started(
                    "stateful_task",
                    {"progress": 0, "status": "pending"},
                    workflow_name="stateful_task_workflow",
                ),
                custom_task_in_progress(
                    "stateful_task",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/status", value="processing", op="replace"),
                            JSONPatchReplace(path="/progress", value=50, op="replace"),
                        ]
                    ),
                    workflow_name="stateful_task_workflow",
                ),
                custom_task_in_progress(
                    "stateful_task",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/status", value="completed", op="replace"),
                            JSONPatchReplace(path="/progress", value=100, op="replace"),
                        ]
                    ),
                    workflow_name="stateful_task_workflow",
                ),
                custom_task_completed(
                    "stateful_task",
                    {"progress": 100, "status": "completed"},
                    workflow_name="stateful_task_workflow",
                ),
                activity_completed(
                    "stateful_task_activity",
                    workflow_name="stateful_task_workflow",
                ),
                activity_started(
                    "__internal__emit_workflow_completed",
                    workflow_name="stateful_task_workflow",
                ),
                workflow_completed("stateful_task_workflow"),
                activity_completed(
                    "__internal__emit_workflow_completed",
                    workflow_name="stateful_task_workflow",
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
                    "attributes.payload.value",
                },
            )
            assert len(errors) == 0, "Event sequence mismatch:\n" + "\n".join(errors)
