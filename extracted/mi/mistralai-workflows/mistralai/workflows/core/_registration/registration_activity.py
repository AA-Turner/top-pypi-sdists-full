from __future__ import annotations

from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.config.config import INTERNAL_ACTIVITY_PREFIX, config
from mistralai.workflows.core.worker_client import get_worker_client
from mistralai.workflows.worker_client.errors.sdkerror import SDKError

REGISTER_EXECUTION_ACTIVITY_NAME = f"{INTERNAL_ACTIVITY_PREFIX}register_execution"


@activity(name=REGISTER_EXECUTION_ACTIVITY_NAME, _allow_reserved_name=True)
async def _register_execution(
    temporal_workflow_id: str,
    temporal_run_id: str,
    workflow_name: str,
    task_queue: str,
    temporal_parent_workflow_id: str | None,
    temporal_root_workflow_id: str | None,
    execution_token_hash: str,
) -> bool:
    """Register an execution. Returns True on success, False if the endpoint is not available (404)."""
    api_key = config.common.mistral_api_key.get_secret_value() if config.common.mistral_api_key else None
    client = get_worker_client(api_key=api_key, headers=config.worker.mistral_api_headers)
    try:
        await client.register_execution_async(
            temporal_workflow_id=temporal_workflow_id,
            temporal_run_id=temporal_run_id,
            workflow_name=workflow_name,
            task_queue=task_queue,
            temporal_parent_workflow_id=temporal_parent_workflow_id,
            temporal_root_workflow_id=temporal_root_workflow_id,
            execution_token_hash=execution_token_hash,
        )
    except SDKError as exc:
        # Retrocompatibility: 404 means the API version doesn't expose
        # the /register endpoint yet.
        if exc.status_code == 404:
            return False
        raise
    return True
