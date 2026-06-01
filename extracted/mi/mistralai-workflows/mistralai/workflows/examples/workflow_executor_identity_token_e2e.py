import base64
import json
from typing import Any

from temporalio.exceptions import ApplicationError

import mistralai.workflows as workflows
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context
from mistralai.workflows.core.worker_client import get_worker_client
from mistralai.workflows.protocol.v1.worker import ExecutorIdentityResult


def _decode_jwt_payload(token: str) -> dict[str, Any]:
    payload_segment = token.split(".")[1]
    padded = payload_segment + "=" * (-len(payload_segment) % 4)
    result: dict[str, Any] = json.loads(base64.urlsafe_b64decode(padded))
    return result


@workflows.activity()
async def fetch_executor_identity_via_token(execution_token: str) -> ExecutorIdentityResult:
    api_key = config.common.mistral_api_key
    if not api_key:
        raise ApplicationError(
            "Error fetching executor identity token: Mistral API key is not set",
            non_retryable=True,
        )

    server_url = config.worker.server_url.rstrip("/")
    async with get_worker_client(base_url=server_url, api_key=api_key.get_secret_value()) as client:
        result = await client.executor_identity_token_async(execution_token=execution_token)

    try:
        claims = _decode_jwt_payload(result.token)
        data: dict[str, Any] = claims.get("data") or claims
        return ExecutorIdentityResult(
            customer_id=data["customer_id"],
            workspace_id=data["workspace_id"],
            user_id=data.get("user_id"),
            organization_id=data.get("organization_id"),
        )
    except Exception as exc:
        raise ApplicationError(
            f"Failed to decode executor identity token: {exc}",
            non_retryable=True,
        ) from exc


@workflows.workflow.define(
    name="example-executor-identity-token-e2e-workflow",
    workflow_description="E2E test: retrieves executor identity token and decodes it",
    on_behalf_of=True,
)
class ExecutorIdentityTokenE2EWorkflow:
    @workflows.workflow.entrypoint
    async def run(self) -> ExecutorIdentityResult:
        context = retrieve_context()
        if not context or not context.execution_token:
            raise ApplicationError(
                "Error fetching executor identity token: execution token is not set",
                non_retryable=True,
            )
        return await fetch_executor_identity_via_token(context.execution_token)
