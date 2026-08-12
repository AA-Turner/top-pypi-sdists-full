import json

import httpx
import temporalio.activity

from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context


def _build_metadata_header() -> str:
    metadata: dict[str, str] = {"call_type": "workflows"}
    if temporalio.activity.in_activity():
        activity_info = temporalio.activity.info()
        if activity_info.workflow_id is not None:
            metadata["execution_id"] = activity_info.workflow_id
        if activity_info.workflow_run_id is not None:
            metadata["run_id"] = activity_info.workflow_run_id
        metadata["task_id"] = activity_info.activity_id
        metadata["attempt"] = str(activity_info.attempt)
    else:
        context = retrieve_context()
        if context is not None and context.execution_id is not None:
            metadata["execution_id"] = context.execution_id
    return json.dumps(metadata)


def inject_metadata(request: httpx.Request) -> None:
    request.headers["x-metadata"] = _build_metadata_header()


async def inject_metadata_async(request: httpx.Request) -> None:
    request.headers["x-metadata"] = _build_metadata_header()
