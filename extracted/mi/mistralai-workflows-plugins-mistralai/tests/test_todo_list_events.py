from typing import Any

import pytest
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.workflow import workflow
from mistralai.workflows.plugins.mistralai import TodoList, TodoListItem
from mistralai.workflows.protocol.v1.events import JSONPatchAdd, JSONPatchPayload, JSONPatchRemove, JSONPatchReplace
from mistralai.workflows.testing import (
    compare_itemwise,
    create_capturing_mock_events_client,
    create_test_worker_with_events,
    custom_task_completed,
    custom_task_in_progress,
    custom_task_started,
)


@activity(name="todo_list_basic_activity")
async def todo_list_basic_activity() -> dict[str, Any]:
    """Basic activity testing TodoListItem.set_status() method."""
    items = [
        TodoListItem(title="First task", description="Do the first thing"),
        TodoListItem(title="Second task", description="Do the second thing"),
    ]
    async with TodoList(items=items) as t:
        await items[0].set_status("in_progress")
        await items[0].set_status("done")
        await items[1].set_status("in_progress")
        return {"task_id": t.id, "items": [{"id": item.id, "status": item.status} for item in t.items]}


@activity(name="todo_item_context_manager_activity")
async def todo_item_context_manager_activity() -> dict[str, Any]:
    """Activity testing TodoListItem context manager for automatic status transitions."""
    item1 = TodoListItem(title="Task with context manager", description="Auto status transitions")
    item2 = TodoListItem(title="Manual task", description="Manual status control")

    async with TodoList(items=[item1, item2]) as t:
        # Use context manager - should auto-set in_progress on enter, done on exit
        async with item1:
            pass  # Work happens here

        # Manual status control for item2
        await item2.set_status("in_progress")
        await item2.set_status("done")

        return {"task_id": t.id, "items": [{"id": item.id, "status": item.status} for item in t.items]}


@activity(name="todo_list_add_item_activity")
async def todo_list_add_item_activity() -> dict[str, Any]:
    """Activity testing dynamic add_item()."""
    item1 = TodoListItem(title="Initial task", description="Already in the list")

    async with TodoList(items=[item1]) as t:
        item2 = TodoListItem(title="Dynamic task", description="Added on the fly")
        await t.add_item(item2)

        await item1.set_status("in_progress")
        await item1.set_status("done")
        await item2.set_status("in_progress")
        await item2.set_status("done")

        return {"task_id": t.id, "item_count": len(t.items)}


@activity(name="todo_list_remove_item_activity")
async def todo_list_remove_item_activity() -> dict[str, Any]:
    """Activity testing dynamic remove_item()."""
    item1 = TodoListItem(title="Task to keep", description="Will remain in the list")
    item2 = TodoListItem(title="Task to remove", description="Will be removed")

    async with TodoList(items=[item1, item2]) as t:
        # Remove item2 before processing
        await t.remove_item(item2)

        await item1.set_status("in_progress")
        await item1.set_status("done")

        return {"task_id": t.id, "item_count": len(t.items)}


@activity(name="todo_item_exception_activity")
async def todo_item_exception_activity() -> dict[str, Any]:
    """Activity testing that exception in context manager leaves status as in_progress."""
    item = TodoListItem(title="Failing task", description="Will fail during execution")

    async with TodoList(items=[item]) as t:
        try:
            async with item:
                raise ValueError("Simulated failure")
        except ValueError:
            pass  # Catch the exception to continue

        # Status should still be in_progress (not done, not failed)
        return {"task_id": t.id, "item_status": item.status}


@workflow.define(name="todo_list_basic_workflow")
class TodoListBasicWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        return await todo_list_basic_activity()


@workflow.define(name="todo_item_context_manager_workflow")
class TodoItemContextManagerWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        return await todo_item_context_manager_activity()


@workflow.define(name="todo_list_add_item_workflow")
class TodoListAddItemWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        return await todo_list_add_item_activity()


@workflow.define(name="todo_list_remove_item_workflow")
class TodoListRemoveItemWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        return await todo_list_remove_item_activity()


@workflow.define(name="todo_item_exception_workflow")
class TodoItemExceptionWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        return await todo_item_exception_activity()


@pytest.mark.asyncio
async def test_todo_list_emits_events(temporal_env: WorkflowEnvironment) -> None:
    """Test that TodoList emits correct custom task events for status updates."""
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[TodoListBasicWorkflow],
            activities=[todo_list_basic_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "todo_list_basic_workflow",
                id="test-todo-list-events",
                task_queue="test-task-queue",
            )
            await handle.result()

            # Filter to only custom_task events
            custom_task_events = [e for e in captured_events if e.event_type.value.startswith("CUSTOM_TASK_")]

            expected_events = [
                custom_task_started(
                    "todo_list",
                    {
                        "items": [
                            {
                                "id": "item-1",
                                "status": "todo",
                                "title": "First task",
                                "description": "Do the first thing",
                            },
                            {
                                "id": "item-2",
                                "status": "todo",
                                "title": "Second task",
                                "description": "Do the second thing",
                            },
                        ]
                    },
                    workflow_name="todo_list_basic_workflow",
                ),
                custom_task_in_progress(
                    "todo_list",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/items/0/status", value="in_progress", op="replace"),
                        ]
                    ),
                    workflow_name="todo_list_basic_workflow",
                ),
                custom_task_in_progress(
                    "todo_list",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/items/0/status", value="done", op="replace"),
                        ]
                    ),
                    workflow_name="todo_list_basic_workflow",
                ),
                custom_task_in_progress(
                    "todo_list",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/items/1/status", value="in_progress", op="replace"),
                        ]
                    ),
                    workflow_name="todo_list_basic_workflow",
                ),
                custom_task_completed(
                    "todo_list",
                    {
                        "items": [
                            {
                                "id": "item-1",
                                "status": "done",
                                "title": "First task",
                                "description": "Do the first thing",
                            },
                            {
                                "id": "item-2",
                                "status": "in_progress",
                                "title": "Second task",
                                "description": "Do the second thing",
                            },
                        ]
                    },
                    workflow_name="todo_list_basic_workflow",
                ),
            ]

            errors = compare_itemwise(
                expected_events,
                custom_task_events,
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
async def test_todo_item_context_manager_emits_events(temporal_env: WorkflowEnvironment) -> None:
    """Test that TodoListItem context manager auto-sets in_progress -> done and emits correct events."""
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[TodoItemContextManagerWorkflow],
            activities=[todo_item_context_manager_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "todo_item_context_manager_workflow",
                id="test-todo-item-context-manager",
                task_queue="test-task-queue",
            )
            await handle.result()

            custom_task_events = [e for e in captured_events if e.event_type.value.startswith("CUSTOM_TASK_")]

            expected_events = [
                custom_task_started(
                    "todo_list",
                    {
                        "items": [
                            {
                                "id": "item-1",
                                "status": "todo",
                                "title": "Task with context manager",
                                "description": "Auto status transitions",
                            },
                            {
                                "id": "item-2",
                                "status": "todo",
                                "title": "Manual task",
                                "description": "Manual status control",
                            },
                        ]
                    },
                    workflow_name="todo_item_context_manager_workflow",
                ),
                # Context manager enter: item1 -> in_progress
                custom_task_in_progress(
                    "todo_list",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/items/0/status", value="in_progress", op="replace"),
                        ]
                    ),
                    workflow_name="todo_item_context_manager_workflow",
                ),
                # Context manager exit: item1 -> done
                custom_task_in_progress(
                    "todo_list",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/items/0/status", value="done", op="replace"),
                        ]
                    ),
                    workflow_name="todo_item_context_manager_workflow",
                ),
                # Manual: item2 -> in_progress
                custom_task_in_progress(
                    "todo_list",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/items/1/status", value="in_progress", op="replace"),
                        ]
                    ),
                    workflow_name="todo_item_context_manager_workflow",
                ),
                # Manual: item2 -> done
                custom_task_in_progress(
                    "todo_list",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/items/1/status", value="done", op="replace"),
                        ]
                    ),
                    workflow_name="todo_item_context_manager_workflow",
                ),
                custom_task_completed(
                    "todo_list",
                    {
                        "items": [
                            {
                                "id": "item-1",
                                "status": "done",
                                "title": "Task with context manager",
                                "description": "Auto status transitions",
                            },
                            {
                                "id": "item-2",
                                "status": "done",
                                "title": "Manual task",
                                "description": "Manual status control",
                            },
                        ]
                    },
                    workflow_name="todo_item_context_manager_workflow",
                ),
            ]

            errors = compare_itemwise(
                expected_events,
                custom_task_events,
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
async def test_todo_list_add_item_emits_events(temporal_env: WorkflowEnvironment) -> None:
    """Test that add_item() works and emits correct events with JSON patch add operation."""
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[TodoListAddItemWorkflow],
            activities=[todo_list_add_item_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "todo_list_add_item_workflow",
                id="test-todo-list-add-item",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            # Verify that we have 2 items after adding one
            assert result["result"]["item_count"] == 2

            custom_task_events = [e for e in captured_events if e.event_type.value.startswith("CUSTOM_TASK_")]

            expected_events = [
                # 1. started (with 1 item)
                custom_task_started(
                    "todo_list",
                    {
                        "items": [
                            {
                                "id": "item-1",
                                "status": "todo",
                                "title": "Initial task",
                                "description": "Already in the list",
                            },
                        ]
                    },
                    workflow_name="todo_list_add_item_workflow",
                ),
                # 2. in_progress (add_item - JSON patch add operation)
                custom_task_in_progress(
                    "todo_list",
                    JSONPatchPayload(
                        value=[
                            JSONPatchAdd(
                                path="/items/1",
                                value={
                                    "id": "item-2",
                                    "status": "todo",
                                    "title": "Dynamic task",
                                    "description": "Added on the fly",
                                },
                                op="add",
                            ),
                        ]
                    ),
                    workflow_name="todo_list_add_item_workflow",
                ),
                # 3. in_progress (item1 -> in_progress)
                custom_task_in_progress(
                    "todo_list",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/items/0/status", value="in_progress", op="replace"),
                        ]
                    ),
                    workflow_name="todo_list_add_item_workflow",
                ),
                # 4. in_progress (item1 -> done)
                custom_task_in_progress(
                    "todo_list",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/items/0/status", value="done", op="replace"),
                        ]
                    ),
                    workflow_name="todo_list_add_item_workflow",
                ),
                # 5. in_progress (item2 -> in_progress)
                custom_task_in_progress(
                    "todo_list",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/items/1/status", value="in_progress", op="replace"),
                        ]
                    ),
                    workflow_name="todo_list_add_item_workflow",
                ),
                # 6. in_progress (item2 -> done)
                custom_task_in_progress(
                    "todo_list",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/items/1/status", value="done", op="replace"),
                        ]
                    ),
                    workflow_name="todo_list_add_item_workflow",
                ),
                # 7. completed (with 2 items)
                custom_task_completed(
                    "todo_list",
                    {
                        "items": [
                            {
                                "id": "item-1",
                                "status": "done",
                                "title": "Initial task",
                                "description": "Already in the list",
                            },
                            {
                                "id": "item-2",
                                "status": "done",
                                "title": "Dynamic task",
                                "description": "Added on the fly",
                            },
                        ]
                    },
                    workflow_name="todo_list_add_item_workflow",
                ),
            ]

            errors = compare_itemwise(
                expected_events,
                custom_task_events,
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
async def test_todo_list_remove_item_emits_events(temporal_env: WorkflowEnvironment) -> None:
    """Test that remove_item() works and emits correct events with JSON patch remove operation."""
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[TodoListRemoveItemWorkflow],
            activities=[todo_list_remove_item_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "todo_list_remove_item_workflow",
                id="test-todo-list-remove-item",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            # Verify that we have 1 item after removing one
            assert result["result"]["item_count"] == 1

            custom_task_events = [e for e in captured_events if e.event_type.value.startswith("CUSTOM_TASK_")]

            expected_events = [
                # 1. started (with 2 items)
                custom_task_started(
                    "todo_list",
                    {
                        "items": [
                            {
                                "id": "item-1",
                                "status": "todo",
                                "title": "Task to keep",
                                "description": "Will remain in the list",
                            },
                            {
                                "id": "item-2",
                                "status": "todo",
                                "title": "Task to remove",
                                "description": "Will be removed",
                            },
                        ]
                    },
                    workflow_name="todo_list_remove_item_workflow",
                ),
                # 2. in_progress (remove_item - JSON patch remove operation)
                custom_task_in_progress(
                    "todo_list",
                    JSONPatchPayload(
                        value=[
                            JSONPatchRemove(path="/items/1", value=None, op="remove"),
                        ]
                    ),
                    workflow_name="todo_list_remove_item_workflow",
                ),
                # 3. in_progress (item1 -> in_progress)
                custom_task_in_progress(
                    "todo_list",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/items/0/status", value="in_progress", op="replace"),
                        ]
                    ),
                    workflow_name="todo_list_remove_item_workflow",
                ),
                # 4. in_progress (item1 -> done)
                custom_task_in_progress(
                    "todo_list",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/items/0/status", value="done", op="replace"),
                        ]
                    ),
                    workflow_name="todo_list_remove_item_workflow",
                ),
                # 5. completed (with 1 item)
                custom_task_completed(
                    "todo_list",
                    {
                        "items": [
                            {
                                "id": "item-1",
                                "status": "done",
                                "title": "Task to keep",
                                "description": "Will remain in the list",
                            },
                        ]
                    },
                    workflow_name="todo_list_remove_item_workflow",
                ),
            ]

            errors = compare_itemwise(
                expected_events,
                custom_task_events,
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
async def test_todo_item_exception_leaves_in_progress(temporal_env: WorkflowEnvironment) -> None:
    """Test that exception in context manager leaves status as in_progress (no done event)."""
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[TodoItemExceptionWorkflow],
            activities=[todo_item_exception_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "todo_item_exception_workflow",
                id="test-todo-item-exception",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            # Status should be "in_progress" (not changed on exception)
            assert result["result"]["item_status"] == "in_progress"

            custom_task_events = [e for e in captured_events if e.event_type.value.startswith("CUSTOM_TASK_")]

            expected_events = [
                # 1. started (with 1 item in "todo" status)
                custom_task_started(
                    "todo_list",
                    {
                        "items": [
                            {
                                "id": "item-1",
                                "status": "todo",
                                "title": "Failing task",
                                "description": "Will fail during execution",
                            },
                        ]
                    },
                    workflow_name="todo_item_exception_workflow",
                ),
                # 2. in_progress (item -> in_progress via context manager enter)
                custom_task_in_progress(
                    "todo_list",
                    JSONPatchPayload(
                        value=[
                            JSONPatchReplace(path="/items/0/status", value="in_progress", op="replace"),
                        ]
                    ),
                    workflow_name="todo_item_exception_workflow",
                ),
                # 3. completed (item still in_progress - no "done" event because exception occurred)
                custom_task_completed(
                    "todo_list",
                    {
                        "items": [
                            {
                                "id": "item-1",
                                "status": "in_progress",
                                "title": "Failing task",
                                "description": "Will fail during execution",
                            },
                        ]
                    },
                    workflow_name="todo_item_exception_workflow",
                ),
            ]

            errors = compare_itemwise(
                expected_events,
                custom_task_events,
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
async def test_unbound_item_raises_error() -> None:
    """Test that set_status on unbound item raises RuntimeError."""
    item = TodoListItem(title="Unbound item", description="Not bound to any TodoList")

    with pytest.raises(RuntimeError, match="not bound"):
        await item.set_status("in_progress")


@pytest.mark.asyncio
async def test_unbound_item_context_manager_raises_error() -> None:
    """Test that using context manager on unbound item raises RuntimeError."""
    item = TodoListItem(title="Unbound item", description="Not bound to any TodoList")

    with pytest.raises(RuntimeError, match="not bound"):
        async with item:
            pass
