import json

import httpx

from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context


def _build_metadata_header() -> str:
    metadata: dict[str, str] = {"call_type": "workflows"}
    context = retrieve_context()
    if context is not None and context.execution_id is not None:
        metadata["execution_id"] = context.execution_id
    return json.dumps(metadata)


def inject_metadata(request: httpx.Request) -> None:
    request.headers["x-metadata"] = _build_metadata_header()


async def inject_metadata_async(request: httpx.Request) -> None:
    request.headers["x-metadata"] = _build_metadata_header()
