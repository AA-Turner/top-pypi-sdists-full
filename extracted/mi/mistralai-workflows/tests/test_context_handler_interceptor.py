from datetime import timedelta

import pytest
from pydantic import BaseModel
from temporalio.testing import WorkflowEnvironment

import mistralai.workflows as workflows
from mistralai.workflows import workflow
from mistralai.workflows.core.temporal.context_handler_interceptor import ContextHandlerInterceptor
from mistralai.workflows.core.utils.contextvars import unwrap_contextual_result
from mistralai.workflows.testing import create_test_worker


class ActivityResult(BaseModel):
    value: str


@workflows.activity(_skip_registering=True)
async def return_activity_result() -> ActivityResult:
    return ActivityResult(value="activity result")


@workflow.define(name="nested-context-activity-result")
class NestedContextActivityResultWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        result = await return_activity_result()
        return result.value


@pytest.mark.asyncio
async def test_activity_result_is_unwrapped_with_duplicate_context_interceptors(
    temporal_env_with_converter: WorkflowEnvironment,
) -> None:
    async with create_test_worker(
        temporal_env_with_converter,
        workflows=[NestedContextActivityResultWorkflow],
        activities=[return_activity_result],
        interceptors=[ContextHandlerInterceptor(), ContextHandlerInterceptor()],
    ):
        handle = await temporal_env_with_converter.client.start_workflow(
            NestedContextActivityResultWorkflow.run,
            id="nested-context-activity-result",
            task_queue="test-task-queue",
            execution_timeout=timedelta(seconds=10),
        )

        _, result = unwrap_contextual_result(await handle.result())

    assert result == {"result": "activity result"}
