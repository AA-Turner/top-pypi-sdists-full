"""Where activities and `execute_workflow` can be called from.

`execute_workflow` only starts child workflows from workflow code. A call from anywhere else,
including from inside an activity, raises before the workflow runs. Direct activity calls
remain supported in-process with their existing retry policy.
"""

from collections import Counter
from collections.abc import Awaitable, Callable, Iterator
from http import HTTPStatus
from typing import Any

import pytest
from pydantic import BaseModel
from temporalio.testing import ActivityEnvironment, WorkflowEnvironment

from mistralai.workflows import activity, get_workflow_definition, workflow
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException
from mistralai.workflows.testing import create_test_worker

calls: Counter[str] = Counter()


@activity()
async def greet_with_kwargs(name: str, **kwargs: Any) -> str:
    calls["greet_with_kwargs"] += 1
    return f"Hi, {name} (" + ", ".join(f"{key}={value}" for key, value in sorted(kwargs.items())) + ")"


class GreetingParams(BaseModel):
    name: str


@workflow.define(name="execution-context-greeting")
class GreetingWorkflow:
    @workflow.entrypoint
    async def run(self, name: str) -> str:
        calls["GreetingWorkflow"] += 1
        return f"Hi, {name}"


@workflow.define(name="execution-context-custom-greeting", enforce_determinism=False)
class CustomGreetingWorkflow:
    @workflow.entrypoint
    async def execute(self, name: str) -> str:
        calls["CustomGreetingWorkflow"] += 1
        return f"Hi, {name}"


@activity()
async def call_greeting_entrypoint(custom_entrypoint: bool, params: Any) -> Any:
    if custom_entrypoint:
        return await CustomGreetingWorkflow().execute(params)
    return await GreetingWorkflow().run(params)


@activity()
async def start_greeting_workflow(wait: bool) -> str:
    await workflow.execute_workflow(GreetingWorkflow, params=GreetingParams(name="Ada"), wait=wait)
    return "started"


async def _execute_from_test_code(wait: bool) -> Any:
    return await workflow.execute_workflow(GreetingWorkflow, params=GreetingParams(name="Ada"), wait=wait)


async def _execute_from_activity(wait: bool) -> Any:
    return await ActivityEnvironment().run(start_greeting_workflow, wait)


@pytest.fixture(autouse=True)
def reset_calls() -> Iterator[None]:
    calls.clear()
    yield


class TestExecuteWorkflowOutsideWorkflow:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("wait", [True, False], ids=["wait", "no_wait"])
    @pytest.mark.parametrize(
        "execute", [_execute_from_test_code, _execute_from_activity], ids=["from_test_code", "from_activity"]
    )
    async def test_raises_without_running_the_workflow(
        self, execute: Callable[[bool], Awaitable[Any]], wait: bool
    ) -> None:
        with pytest.raises(WorkflowsException) as exc_info:
            await execute(wait)

        assert exc_info.value.code == ErrorCode.CHILD_WORKFLOW_OUTSIDE_WORKFLOW
        assert calls["GreetingWorkflow"] == 0


class TestDirectWorkflowEntrypoint:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("custom_entrypoint", [False, True], ids=["run", "custom-unsandboxed"])
    @pytest.mark.parametrize("from_activity", [False, True], ids=["from_test_code", "from_activity"])
    async def test_raises_without_running_the_workflow(self, custom_entrypoint: bool, from_activity: bool) -> None:
        params = {"name": "Ada"}
        with pytest.raises(WorkflowsException) as exc_info:
            if from_activity:
                await ActivityEnvironment().run(call_greeting_entrypoint, custom_entrypoint, params)
            elif custom_entrypoint:
                await CustomGreetingWorkflow().execute(params)
            else:
                await GreetingWorkflow().run(params)

        assert exc_info.value.code == ErrorCode.CHILD_WORKFLOW_OUTSIDE_WORKFLOW
        assert exc_info.value.status == HTTPStatus.BAD_REQUEST
        entrypoint = "CustomGreetingWorkflow.execute()" if custom_entrypoint else "GreetingWorkflow.run()"
        assert f"{entrypoint} can only be called from workflow code" in str(exc_info.value)
        assert not calls

    @pytest.mark.asyncio
    @pytest.mark.parametrize("workflow_type", [GreetingWorkflow, CustomGreetingWorkflow])
    async def test_runs_on_test_worker(self, temporal_env: WorkflowEnvironment, workflow_type: type) -> None:
        async with create_test_worker(temporal_env, workflows=[workflow_type]):
            result = await temporal_env.client.execute_workflow(
                get_workflow_definition(workflow_type).name,
                {"name": "Ada"},
                id="test-direct-entrypoint-on-worker",
                task_queue="test-task-queue",
            )

        assert result == {"result": "Hi, Ada"}


class TestDirectActivityCall:
    @pytest.mark.asyncio
    async def test_runs_in_process(self) -> None:
        assert await greet_with_kwargs("Ada", colour="blue", size=3) == "Hi, Ada (colour=blue, size=3)"
