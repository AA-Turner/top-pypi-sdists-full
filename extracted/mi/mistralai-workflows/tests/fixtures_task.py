from typing import Any

from pydantic import BaseModel

from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.task import task
from mistralai.workflows.core.workflow import workflow


class TaskTestState(BaseModel):
    progress: int = 0
    status: str = "pending"


class TaskResult(BaseModel):
    task_id: str
    final_progress: int
    final_status: str


@activity(name="simple_task_activity")
async def simple_task_activity() -> str:
    async with task("test_task") as t:
        return t.id


@activity(name="stateful_task_activity")
async def stateful_task_activity(initial_progress: int = 0) -> TaskResult:
    initial_state = TaskTestState(progress=initial_progress, status="pending")
    async with task("stateful_task", state=initial_state) as t:
        await t.update_state({"progress": 50, "status": "processing"})
        await t.update_state({"progress": 100, "status": "completed"})
        return TaskResult(
            task_id=t.id,
            final_progress=t.state.progress,
            final_status=t.state.status,
        )


@activity(name="set_state_task_activity")
async def set_state_task_activity() -> TaskResult:
    initial_state = TaskTestState(progress=0, status="pending")
    async with task("set_state_task", state=initial_state) as t:
        new_state = TaskTestState(progress=100, status="completed")
        await t.set_state(new_state)
        return TaskResult(
            task_id=t.id,
            final_progress=t.state.progress,
            final_status=t.state.status,
        )


@activity(name="failing_task_activity")
async def failing_task_activity() -> None:
    async with task("failing_task"):
        raise ValueError("Intentional test error")


@activity(name="failing_task_no_retry_activity", retry_policy_max_attempts=1)
async def failing_task_no_retry_activity() -> None:
    """Failing activity with no retries - for testing task failure spans in isolation."""
    async with task("failing_task"):
        raise ValueError("Intentional test error")


@activity(name="nested_tasks_activity")
async def nested_tasks_activity() -> dict[str, Any]:
    outer_result = {}
    inner_result = {}

    async with task("outer_task", state={"level": "outer"}) as outer:
        await outer.update_state({"progress": 50})
        outer_result["mid_progress"] = outer.state["progress"]

        async with task("inner_task", state={"level": "inner"}) as inner:
            await inner.update_state({"progress": 100})
            inner_result["progress"] = inner.state["progress"]

        await outer.update_state({"progress": 100})
        outer_result["final_progress"] = outer.state["progress"]

    return {
        "outer": outer_result,
        "inner": inner_result,
    }


@workflow.define(name="simple_task_workflow")
class SimpleTaskWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return await simple_task_activity()


@workflow.define(name="stateful_task_workflow")
class StatefulTaskWorkflow:
    @workflow.entrypoint
    async def run(self, initial_progress: int = 0) -> TaskResult:
        return await stateful_task_activity(initial_progress)


@workflow.define(name="set_state_task_workflow")
class SetStateTaskWorkflow:
    @workflow.entrypoint
    async def run(self) -> TaskResult:
        return await set_state_task_activity()


@workflow.define(name="task_in_workflow")
class TaskInWorkflowWorkflow:
    @workflow.entrypoint
    async def run(self) -> TaskResult:
        initial_state = TaskTestState(progress=0, status="pending")
        async with task("workflow_task", state=initial_state) as t:
            # Simulate work across multiple steps
            await t.update_state({"progress": 50, "status": "processing"})

            await simple_task_activity()

            await t.update_state({"progress": 100, "status": "completed"})

            return TaskResult(
                task_id=t.id,
                final_progress=t.state.progress,
                final_status=t.state.status,
            )


@workflow.define(name="failing_task_workflow")
class FailingTaskWorkflow:
    @workflow.entrypoint
    async def run(self) -> None:
        await failing_task_activity()


@workflow.define(name="failing_task_no_retry_workflow")
class FailingTaskNoRetryWorkflow:
    @workflow.entrypoint
    async def run(self) -> None:
        await failing_task_no_retry_activity()


@workflow.define(name="nested_tasks_workflow")
class NestedTasksWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        return await nested_tasks_activity()


@activity(name="process_step_1")
async def process_step_1() -> str:
    return "step1_complete"


@activity(name="process_step_2")
async def process_step_2() -> str:
    return "step2_complete"


@activity(name="process_step_3")
async def process_step_3() -> str:
    return "step3_complete"


@workflow.define(name="task_spanning_activities_workflow")
class TaskSpanningActivitiesWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        initial_state = TaskTestState(progress=0, status="starting")
        results = []

        async with task("multi_activity_task", state=initial_state) as t:
            await t.update_state({"progress": 10, "status": "running"})

            result1 = await process_step_1()
            results.append(result1)
            await t.update_state({"progress": 33, "status": "step1_done"})

            result2 = await process_step_2()
            results.append(result2)
            await t.update_state({"progress": 66, "status": "step2_done"})

            result3 = await process_step_3()
            results.append(result3)
            await t.update_state({"progress": 100, "status": "completed"})

            assert isinstance(t.state, TaskTestState)
            return {
                "task_id": t.id,
                "final_progress": t.state.progress,
                "final_status": t.state.status,
                "activity_results": results,
            }
