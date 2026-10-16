from __future__ import annotations

from mistralai.workflows.core._registration.null_value_compat import call_stripping_nulls_on_rejection
from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.config.config import INTERNAL_ACTIVITY_PREFIX, config
from mistralai.workflows.core.worker_client import get_worker_client

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
    search_key_metadata: dict[str, str | None] | None = None,
) -> bool:
    client = get_worker_client(headers=config.worker.mistral_api_headers)
    await call_stripping_nulls_on_rejection(
        lambda metadata: client.register_execution_async(
            temporal_workflow_id=temporal_workflow_id,
            temporal_run_id=temporal_run_id,
            workflow_name=workflow_name,
            task_queue=task_queue,
            temporal_parent_workflow_id=temporal_parent_workflow_id,
            temporal_root_workflow_id=temporal_root_workflow_id,
            execution_token_hash=execution_token_hash,
            search_key_metadata=metadata,
        ),
        search_key_metadata,
    )
    return True
