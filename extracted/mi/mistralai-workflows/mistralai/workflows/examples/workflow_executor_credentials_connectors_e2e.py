from datetime import timedelta

from pydantic import BaseModel

import mistralai.workflows as workflows
from mistralai.workflows.client import get_mistral_client


class ExecutorCredentialsConnectorsResult(BaseModel):
    connector_count: int


@workflows.activity(start_to_close_timeout=timedelta(minutes=1))
async def list_connectors_with_executor_credentials() -> ExecutorCredentialsConnectorsResult:
    client = get_mistral_client(use_executor_credentials=True)
    result = await client.beta.connectors.list_async()
    return ExecutorCredentialsConnectorsResult(connector_count=len(result.items))


@workflows.workflow.define(
    name="example-executor-credentials-connectors-e2e-workflow",
    workflow_description="E2E test: list connectors using executor credentials (staging/prod only)",
    on_behalf_of=True,
)
class ExecutorCredentialsConnectorsE2EWorkflow:
    @workflows.workflow.entrypoint
    async def run(self) -> ExecutorCredentialsConnectorsResult:
        return await list_connectors_with_executor_credentials()
