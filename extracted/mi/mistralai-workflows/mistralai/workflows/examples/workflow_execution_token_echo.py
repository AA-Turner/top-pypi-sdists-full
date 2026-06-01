from pydantic import BaseModel

import mistralai.workflows as workflows
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context


class EchoResult(BaseModel):
    execution_token: str | None


class EmptyParams(BaseModel):
    pass


class ModelInput(BaseModel):
    message: str
    count: int = 0


@workflows.workflow.define(
    name="example-execution-token-echo-workflow",
    workflow_description="Echo workflow that returns its execution token",
)
class ExecutionTokenEchoWorkflow:
    @workflows.workflow.entrypoint
    async def run(self) -> EchoResult:
        context = retrieve_context()
        token = context.execution_token if context else None
        return EchoResult(execution_token=token)


@workflows.workflow.define(
    name="example-execution-token-echo-parent-workflow",
    workflow_description="Parent workflow that delegates to the echo child and returns its result",
)
class ExecutionTokenEchoParentWorkflow:
    @workflows.workflow.entrypoint
    async def run(self) -> EchoResult:
        result: EchoResult = await workflows.workflow.execute_workflow(ExecutionTokenEchoWorkflow, params=EmptyParams())
        return result


class DictEchoParams(BaseModel):
    message: str = ""


@workflows.workflow.define(name="example-execution-token-dict-echo-workflow")
class ExecutionTokenDictEchoWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, message: str = "") -> EchoResult:
        context = retrieve_context()
        token = context.execution_token if context else None
        return EchoResult(execution_token=token)


@workflows.workflow.define(name="example-execution-token-dict-echo-parent-workflow")
class ExecutionTokenDictEchoParentWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, message: str = "") -> EchoResult:
        result: EchoResult = await workflows.workflow.execute_workflow(
            ExecutionTokenDictEchoWorkflow, params=DictEchoParams(message=message)
        )
        return result


@workflows.workflow.define(name="example-execution-token-model-echo-workflow")
class ExecutionTokenModelEchoWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, params: ModelInput) -> EchoResult:
        context = retrieve_context()
        token = context.execution_token if context else None
        return EchoResult(execution_token=token)


@workflows.activity()
async def get_execution_token_activity() -> EchoResult:
    context = retrieve_context()
    token = context.execution_token if context else None
    return EchoResult(execution_token=token)


@workflows.workflow.define(
    name="example-execution-token-activity-echo-workflow",
    workflow_description="Workflow that retrieves its execution token from within an activity",
)
class ExecutionTokenActivityEchoWorkflow:
    @workflows.workflow.entrypoint
    async def run(self) -> EchoResult:
        return await get_execution_token_activity()
