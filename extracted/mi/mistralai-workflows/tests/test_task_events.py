import json
from typing import Any

import pytest
from pydantic import ValidationError
from temporalio.client import WorkflowHandle
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core._events import event_interceptor
from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.core.config.config import WorkerConfig
from mistralai.workflows.core.execution.workflow_run_config import WorkflowRunConfig
from mistralai.workflows.protocol.v1.events import (
    ActivityTaskCompleted,
    ActivityTaskStarted,
    JSONPatchPayload,
    JSONPatchReplace,
    WorkflowEventCategory,
    WorkflowEventType,
)
from mistralai.workflows.testing import (
    ALL_EVENT_CATEGORIES,
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
from .utils import create_capturing_mock_event_publisher, create_test_worker_with_events, emitted


@pytest.mark.asyncio
async def test_simple_task_in_activity_emits_events(
    temporal_env: WorkflowEnvironment, event_categories: frozenset[WorkflowEventCategory]
) -> None:
    """Test that a simple task in an activity emits started and completed events."""
    captured_events: list[Any] = []

    mock_client = create_capturing_mock_event_publisher(captured_events)

    async with EventContext(mock_client, emitted_event_categories=event_categories):
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
                emitted(expected_events, event_categories),
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
async def test_stateful_task_emits_in_progress_events(
    temporal_env: WorkflowEnvironment, event_categories: frozenset[WorkflowEventCategory]
) -> None:
    """Test that a task with state updates emits in_progress events."""
    captured_events: list[Any] = []

    mock_client = create_capturing_mock_event_publisher(captured_events)

    async with EventContext(mock_client, emitted_event_categories=event_categories):
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
                emitted(expected_events, event_categories),
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
async def test_nested_tasks_emit_hierarchical_events(
    temporal_env: WorkflowEnvironment, event_categories: frozenset[WorkflowEventCategory]
) -> None:
    """Test that nested tasks emit events in the correct order."""
    captured_events: list[Any] = []

    mock_client = create_capturing_mock_event_publisher(captured_events)

    async with EventContext(mock_client, emitted_event_categories=event_categories):
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
                emitted(expected_events, event_categories),
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
    temporal_env: WorkflowEnvironment, event_categories: frozenset[WorkflowEventCategory]
) -> None:
    """Test that tasks in workflows emit events via local activities."""
    captured_events: list[Any] = []

    mock_client = create_capturing_mock_event_publisher(captured_events)

    async with EventContext(mock_client, emitted_event_categories=event_categories):
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
                emitted(expected_events, event_categories),
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
async def test_task_events_ordered_within_activity(
    temporal_env: WorkflowEnvironment, event_categories: frozenset[WorkflowEventCategory]
) -> None:
    """Test that task events within a single activity maintain strict FIFO ordering."""
    captured_events: list[Any] = []

    mock_client = create_capturing_mock_event_publisher(captured_events)

    async with EventContext(mock_client, emitted_event_categories=event_categories):
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
                emitted(expected_events, event_categories),
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


class TestEmittedEventCategories:
    @pytest.mark.asyncio
    async def test_activity_events_are_not_emitted_by_default(self, temporal_env: WorkflowEnvironment) -> None:
        captured_events: list[Any] = []

        async with EventContext(create_capturing_mock_event_publisher(captured_events)):
            async with create_test_worker_with_events(
                temporal_env, workflows=[SimpleTaskWorkflow], activities=[simple_task_activity]
            ):
                await temporal_env.client.execute_workflow(
                    "simple_task_workflow", id="test-default-categories", task_queue="test-task-queue"
                )

        assert captured_events
        assert {e.event_type.category for e in captured_events} == {
            WorkflowEventCategory.WORKFLOW,
            WorkflowEventCategory.CUSTOM_TASK,
        }

    @pytest.mark.asyncio
    async def test_enabled_activity_category_emits_user_activity_events(
        self, temporal_env: WorkflowEnvironment
    ) -> None:
        captured_events: list[Any] = []

        async with EventContext(
            create_capturing_mock_event_publisher(captured_events), emitted_event_categories=ALL_EVENT_CATEGORIES
        ):
            async with create_test_worker_with_events(
                temporal_env, workflows=[SimpleTaskWorkflow], activities=[simple_task_activity]
            ):
                await temporal_env.client.execute_workflow(
                    "simple_task_workflow", id="test-all-categories", task_queue="test-task-queue"
                )

        user_activity_events = [
            e.event_type
            for e in captured_events
            if isinstance(e, ActivityTaskStarted | ActivityTaskCompleted)
            and e.attributes.activity_name == "simple_task_activity"
        ]
        assert user_activity_events == [
            WorkflowEventType.ACTIVITY_TASK_STARTED,
            WorkflowEventType.ACTIVITY_TASK_COMPLETED,
        ]

    @pytest.mark.asyncio
    async def test_custom_task_events_cannot_be_disabled(self, temporal_env: WorkflowEnvironment) -> None:
        captured_events: list[Any] = []

        async with EventContext(create_capturing_mock_event_publisher(captured_events), emitted_event_categories=set()):
            async with create_test_worker_with_events(
                temporal_env, workflows=[StatefulTaskWorkflow], activities=[stateful_task_activity]
            ):
                await temporal_env.client.execute_workflow(
                    "stateful_task_workflow", id="test-no-category", task_queue="test-task-queue"
                )

        assert {e.event_type.category for e in captured_events} == {WorkflowEventCategory.CUSTOM_TASK}

    def test_worker_setting_without_custom_task_is_rejected(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("EMITTED_EVENT_CATEGORIES", "WORKFLOW,ACTIVITY")

        with pytest.raises(ValidationError, match="CUSTOM_TASK"):
            WorkerConfig()

    def test_worker_setting_can_send_only_custom_task(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("EMITTED_EVENT_CATEGORIES", "CUSTOM_TASK")

        assert WorkerConfig().emitted_event_categories == [WorkflowEventCategory.CUSTOM_TASK]

    @pytest.mark.parametrize("value", ["", " ", ","])
    def test_empty_worker_setting_is_rejected(self, monkeypatch: pytest.MonkeyPatch, value: str) -> None:
        monkeypatch.setenv("EMITTED_EVENT_CATEGORIES", value)

        with pytest.raises(ValidationError):
            WorkerConfig()

    def test_worker_setting_is_comma_separated(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("EMITTED_EVENT_CATEGORIES", "WORKFLOW, CUSTOM_TASK, ACTIVITY")

        assert WorkerConfig().emitted_event_categories == [
            WorkflowEventCategory.WORKFLOW,
            WorkflowEventCategory.CUSTOM_TASK,
            WorkflowEventCategory.ACTIVITY,
        ]

    @pytest.mark.asyncio
    async def test_disabled_workflow_category_schedules_no_emitter(self, temporal_env: WorkflowEnvironment) -> None:
        captured_events: list[Any] = []

        async with EventContext(
            create_capturing_mock_event_publisher(captured_events),
            emitted_event_categories={WorkflowEventCategory.CUSTOM_TASK},
        ):
            async with create_test_worker_with_events(
                temporal_env, workflows=[TaskInWorkflowWorkflow], activities=[simple_task_activity]
            ):
                handle: WorkflowHandle[Any, Any] = await temporal_env.client.start_workflow(
                    "task_in_workflow", id="test-no-workflow-emitters", task_queue="test-task-queue"
                )
                await handle.result()
                local_activities = await _local_activity_types(handle)

        assert {e.event_type.category for e in captured_events} == {WorkflowEventCategory.CUSTOM_TASK}
        assert not [name for name in local_activities if name.startswith("__internal__emit_workflow_")]
        assert "__internal__emit_task_started" in local_activities

    @pytest.mark.asyncio
    async def test_run_started_with_workflow_events_keeps_sending_them(self, temporal_env: WorkflowEnvironment) -> None:
        """A run that recorded WORKFLOW still sends its lifecycle events after the worker turns WORKFLOW off."""
        captured_events: list[Any] = []

        async def recorded_before_the_setting_changed() -> WorkflowRunConfig:
            return WorkflowRunConfig(emitted_event_categories=ALL_EVENT_CATEGORIES)

        with pytest.MonkeyPatch.context() as monkeypatch:
            monkeypatch.setattr(event_interceptor, "record_workflow_run_config", recorded_before_the_setting_changed)
            async with EventContext(
                create_capturing_mock_event_publisher(captured_events),
                emitted_event_categories={WorkflowEventCategory.CUSTOM_TASK},
            ):
                async with create_test_worker_with_events(
                    temporal_env, workflows=[TaskInWorkflowWorkflow], activities=[simple_task_activity]
                ):
                    await temporal_env.client.execute_workflow(
                        "task_in_workflow", id="test-workflow-events-follow-snapshot", task_queue="test-task-queue"
                    )

        workflow_event_types = [
            e.event_type for e in captured_events if e.event_type.category == WorkflowEventCategory.WORKFLOW
        ]
        assert workflow_event_types == [
            WorkflowEventType.WORKFLOW_EXECUTION_STARTED,
            WorkflowEventType.WORKFLOW_EXECUTION_COMPLETED,
        ]
        assert WorkflowEventCategory.ACTIVITY not in {e.event_type.category for e in captured_events}


async def _local_activity_types(handle: WorkflowHandle[Any, Any]) -> list[str]:
    names = []
    async for event in handle.fetch_history_events():
        if event.HasField("marker_recorded_event_attributes"):
            for payload in event.marker_recorded_event_attributes.details["data"].payloads:
                names.append(str(json.loads(payload.data).get("activity_type", "")))
    return names
