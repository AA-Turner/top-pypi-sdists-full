import mistralai.workflows as workflows
from mistralai.workflows.client import translate_model
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context
from mistralai.workflows.core.worker_client import get_worker_client
from mistralai.workflows.protocol.v1.worker import ExecutorIdentityResult


@workflows.activity()
async def fetch_executor_identity(execution_token: str) -> ExecutorIdentityResult:
    api_key = config.common.mistral_api_key
    if not api_key:
        raise Exception("Error fetching executor identity: Mistral API key is not set")

    server_url = config.worker.server_url.rstrip("/")
    async with get_worker_client(base_url=server_url, api_key=api_key.get_secret_value()) as client:
        result = await client.executor_identity_async(execution_token=execution_token)
        return translate_model(ExecutorIdentityResult, result)


@workflows.workflow.define(
    name="example-executor-identity-e2e-workflow",
    workflow_description="E2E test: retrieves executor identity using execution token",
    on_behalf_of=True,
)
class ExecutorIdentityE2EWorkflow:
    @workflows.workflow.entrypoint
    async def run(self) -> ExecutorIdentityResult:
        context = retrieve_context()
        if not context or not context.execution_token:
            raise Exception("Error fetching executor identity: execution token is not set")
        return await fetch_executor_identity(context.execution_token)
