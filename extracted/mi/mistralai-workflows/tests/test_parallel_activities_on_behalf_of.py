"""The parallel fan-out must follow each workflow's own on_behalf_of declaration."""

from typing import List

import pytest
import temporalio.activity
from pydantic import BaseModel
from temporalio.testing import WorkflowEnvironment

import mistralai.workflows as workflows
from mistralai.workflows import get_workflow_definition, workflow
from mistralai.workflows.constants import OBO_PARALLEL_EXECUTION_WORKFLOW_NAME, PARALLEL_EXECUTION_WORKFLOW_NAME
from mistralai.workflows.core.execution.concurrency._concurrency_workflow import (
    OnBehalfOfParallelExecutionWorkflow,
    ParallelExecutionWorkflow,
)
from mistralai.workflows.core.execution.concurrency.execute_activities_in_parallel import (
    execute_activities_in_parallel,
)
from mistralai.workflows.core.temporal.context_handler_interceptor import ContextHandlerInterceptor
from mistralai.workflows.core.utils.contextvars import unwrap_contextual_result

from .utils import create_test_worker


@workflows.activity()
async def report_scheduling_workflow_type(marker: str) -> str:
    """Report which fan-out workflow scheduled this activity."""
    return f"{marker}:{temporalio.activity.info().workflow_type}"


class NoParams(BaseModel):
    pass


class ChildSelector(BaseModel):
    child_on_behalf_of: bool


@workflow.define(name="test-fanout-child-obo", on_behalf_of=True)
class OboFanoutChild:
    @workflow.entrypoint
    async def run(self) -> List[str]:
        return await execute_activities_in_parallel(activity=report_scheduling_workflow_type, items=["child"])


@workflow.define(name="test-fanout-child-plain")
class PlainFanoutChild:
    @workflow.entrypoint
    async def run(self) -> List[str]:
        return await execute_activities_in_parallel(activity=report_scheduling_workflow_type, items=["child"])


@workflow.define(name="test-fanout-parent-obo", on_behalf_of=True)
class OboFanoutParent:
    @workflow.entrypoint
    async def run(self, input: ChildSelector) -> List[str]:
        child = OboFanoutChild if input.child_on_behalf_of else PlainFanoutChild
        return await workflow.execute_workflow(child, params=NoParams())


@workflow.define(name="test-fanout-parent-plain")
class PlainFanoutParent:
    @workflow.entrypoint
    async def run(self, input: ChildSelector) -> List[str]:
        child = OboFanoutChild if input.child_on_behalf_of else PlainFanoutChild
        return await workflow.execute_workflow(child, params=NoParams())


_ALL_WORKFLOWS = [
    OboFanoutParent,
    PlainFanoutParent,
    OboFanoutChild,
    PlainFanoutChild,
    ParallelExecutionWorkflow,
    OnBehalfOfParallelExecutionWorkflow,
]


class TestFanOutWorkflowSelection:
    @pytest.mark.asyncio
    @pytest.mark.timeout(60)
    @pytest.mark.parametrize("parent_on_behalf_of", [True, False], ids=["obo-parent", "plain-parent"])
    @pytest.mark.parametrize("child_on_behalf_of", [True, False], ids=["obo-child", "plain-child"])
    async def test_child_fan_out_follows_child_declaration_not_parent(
        self,
        temporal_env_with_converter: WorkflowEnvironment,
        parent_on_behalf_of: bool,
        child_on_behalf_of: bool,
    ) -> None:
        parent = OboFanoutParent if parent_on_behalf_of else PlainFanoutParent
        expected_fanout = (
            OBO_PARALLEL_EXECUTION_WORKFLOW_NAME if child_on_behalf_of else PARALLEL_EXECUTION_WORKFLOW_NAME
        )

        async with create_test_worker(
            temporal_env_with_converter,
            workflows=_ALL_WORKFLOWS,
            activities=[report_scheduling_workflow_type],
            interceptors=[ContextHandlerInterceptor()],
        ):
            handle = await temporal_env_with_converter.client.start_workflow(
                get_workflow_definition(parent).name,
                {"child_on_behalf_of": child_on_behalf_of},
                id=f"test-fanout-p{int(parent_on_behalf_of)}-c{int(child_on_behalf_of)}",
                task_queue="test-task-queue",
            )
            _, result = unwrap_contextual_result(await handle.result())

        assert result == {"result": [f"child:{expected_fanout}"]}
