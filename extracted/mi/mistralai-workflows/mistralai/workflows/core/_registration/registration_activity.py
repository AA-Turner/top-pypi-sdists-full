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
    search_key_metadata: dict[str, str] | None = None,
) -> bool:
    """Register an execution. Returns True on success, False if the endpoint is not available (404/405)."""
    client = get_worker_client(headers=config.worker.mistral_api_headers)
    try:
        await client.register_execution_async(
            temporal_workflow_id=temporal_workflow_id,
            temporal_run_id=temporal_run_id,
            workflow_name=workflow_name,
            task_queue=task_queue,
            temporal_parent_workflow_id=temporal_parent_workflow_id,
            temporal_root_workflow_id=temporal_root_workflow_id,
            execution_token_hash=execution_token_hash,
            search_key_metadata=search_key_metadata,
        )
    except SDKError as exc:
        # Retrocompatibility: 404 means the API version doesn't expose
        # the /register endpoint yet.
        # 405 means the endpoint exists but only accepts GET (old backends
        # that route GET /executions/{execution_id} to this path).
        if exc.status_code in (404, 405):
            return False
        raise
    return True
