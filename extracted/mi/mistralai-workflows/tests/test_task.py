from typing import Any
from unittest.mock import patch

import pytest

from mistralai.workflows.core.task.task import Task

from .fixtures_interactive_workflow import mock_should_publish_event  # noqa: F401
from .fixtures_task import (
    NestedTasksWorkflow,
    SetStateTaskWorkflow,
    SimpleTaskWorkflow,
    StatefulTaskWorkflow,
    TaskInWorkflowWorkflow,
    TaskSpanningActivitiesWorkflow,
    nested_tasks_activity,
    process_step_1,
    process_step_2,
    process_step_3,
    set_state_task_activity,
    simple_task_activity,
    stateful_task_activity,
)
from .utils import create_test_worker


@pytest.mark.usefixtures("mock_should_publish_event")
class TestTaskCreation:
    def test_task_creation_with_type_only(self) -> None:
        task: Task[None] = Task(type="test-task")
        assert task.type == "test-task"
        assert task.state is None
        assert task.id is not None

    def test_task_creation_with_state(self) -> None:
        initial_state = {"progress": 0, "status": "pending"}
        task: Task[dict] = Task(type="processing", state=initial_state)
        assert task.type == "processing"
        assert task.state == initial_state

    def test_task_creation_with_explicit_id(self) -> None:
        task: Task[None] = Task(type="test-task", id="custom-id-123")
        assert task.id == "custom-id-123"

    def test_task_creation_in_activity_succeeds(self) -> None:
        with patch("mistralai.workflows.core.task.task.temporalio.activity.in_activity", return_value=True):
            task: Task[None] = Task(type="test-task")
            assert task.type == "test-task"

    def test_task_creation_in_workflow_succeeds(self) -> None:
        with patch("mistralai.workflows.core.task.task.temporalio.workflow.in_workflow", return_value=True):
            with patch("mistralai.workflows.core.task.task.temporalio.workflow.uuid4", return_value="mock-uuid"):
                task: Task[None] = Task(type="test-task", id="explicit-id")
                assert task.type == "test-task"
                assert task.id == "explicit-id"


@pytest.mark.usefixtures("mock_should_publish_event")
class TestTaskStateManagement:
    @pytest.mark.asyncio
    async def test_set_state_updates_task_state(self) -> None:
        task: Task[dict] = Task(type="processing", state={"progress": 0})
        await task.set_state({"progress": 50})
        assert task.state == {"progress": 50}

    @pytest.mark.asyncio
    async def test_set_state_on_stateless_task_raises_error(self) -> None:
        task: Task[None] = Task(type="processing")
        with pytest.raises(RuntimeError, match="Cannot set_state\\(\\) on task created without state"):
            await task.set_state({"progress": 50})  # type: ignore

    @pytest.mark.asyncio
    async def test_update_state_with_dict(self) -> None:
        task: Task[dict] = Task(type="processing", state={"progress": 0, "status": "pending"})
        await task.update_state({"progress": 50})
        assert task.state == {"progress": 50, "status": "pending"}

    @pytest.mark.asyncio
    async def test_update_state_on_stateless_task_raises_error(self) -> None:
        task: Task[None] = Task(type="processing")
        with pytest.raises(RuntimeError, match="Cannot update_state\\(\\) on task created without state"):
            await task.update_state({"progress": 50})  # type: ignore


@pytest.mark.usefixtures("mock_should_publish_event")
class TestTaskExecution:
    @pytest.mark.asyncio
    async def test_simple_task_in_activity_executes(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[SimpleTaskWorkflow],
            activities=[simple_task_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "simple_task_workflow",
                id="test-simple-task-exec",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result is not None

    @pytest.mark.asyncio
    async def test_stateful_task_in_activity_executes(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[StatefulTaskWorkflow],
            activities=[stateful_task_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "stateful_task_workflow",
                {"initial_progress": 25},
                id="test-stateful-task-exec",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["final_progress"] == 100
            assert result["final_status"] == "completed"

    @pytest.mark.asyncio
    async def test_task_with_state_updates_executes(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[SetStateTaskWorkflow],
            activities=[set_state_task_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "set_state_task_workflow",
                id="test-state-updates-exec",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["final_progress"] == 100
            assert result["final_status"] == "completed"

    @pytest.mark.asyncio
    async def test_nested_tasks_execute(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[NestedTasksWorkflow],
            activities=[nested_tasks_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "nested_tasks_workflow",
                id="test-nested-tasks-exec",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result is not None

    @pytest.mark.asyncio
    async def test_task_in_workflow_executes(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[TaskInWorkflowWorkflow],
            activities=[simple_task_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "task_in_workflow",
                id="test-workflow-task-exec",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["final_progress"] == 100
            assert result["final_status"] == "completed"

    @pytest.mark.asyncio
    async def test_task_spanning_multiple_activities_executes(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[TaskSpanningActivitiesWorkflow],
            activities=[process_step_1, process_step_2, process_step_3],
        ):
            handle = await temporal_env.client.start_workflow(
                "task_spanning_activities_workflow",
                id="test-spanning-task-exec",
                task_queue="test-task-queue",
            )

            try:
                result = await handle.result()
            except Exception as e:
                pytest.fail(f"Workflow failed with: {e}")

            actual_result = result.get("result", result)

            assert "final_progress" in actual_result
            assert actual_result["final_progress"] == 100
            assert actual_result["final_status"] == "completed"
            assert actual_result["activity_results"] == ["step1_complete", "step2_complete", "step3_complete"]
            assert "task_id" in actual_result
