from datetime import timedelta

from pydantic import BaseModel

import mistralai.workflows as workflows
from mistralai.workflows.client import get_mistral_client
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context

WORKFLOW_NAME = "example-executor-credentials-e2e-workflow"


class ExecutorCredentialsResult(BaseModel):
    execution_id: str
    workflow_name: str


@workflows.activity(start_to_close_timeout=timedelta(minutes=1))
async def fetch_current_execution_with_executor_credentials() -> ExecutorCredentialsResult:
    context = retrieve_context()
    if context is None or context.execution_id is None:
        raise RuntimeError("Execution ID is not set")
    execution_id = context.execution_id

    client = get_mistral_client(use_executor_credentials=True)
    execution = await client.workflows.executions.get_workflow_execution_async(execution_id=execution_id)
    return ExecutorCredentialsResult(
        execution_id=execution.execution_id,
        workflow_name=execution.workflow_name,
    )


@workflows.workflow.define(
    name=WORKFLOW_NAME,
    workflow_description="E2E test: calls abraxas API using executor credentials",
    on_behalf_of=True,
)
class ExecutorCredentialsE2EWorkflow:
    @workflows.workflow.entrypoint
    async def run(self) -> ExecutorCredentialsResult:
        return await fetch_current_execution_with_executor_credentials()
