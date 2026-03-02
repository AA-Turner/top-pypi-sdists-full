"""Execute Ssh Command"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import ExecuteSSHRequest, ExecuteSSHResponse


def _build_request_args(
    public_id: str,
    body: ExecuteSSHRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/sandbox/public-build/vm/{public_id}/execute"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    public_id: str,
    body: ExecuteSSHRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ExecuteSSHResponse:
    """Execute an SSH command on a VM via NATS.

    The command is executed asynchronously. Use the correlation_id with the
    /events/{correlation_id} SSE endpoint to receive the result."""

    request_args = _build_request_args(
        public_id=public_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ExecuteSSHResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    public_id: str,
    body: ExecuteSSHRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ExecuteSSHResponse:
    """Execute an SSH command on a VM via NATS.

    The command is executed asynchronously. Use the correlation_id with the
    /events/{correlation_id} SSE endpoint to receive the result."""

    request_args = _build_request_args(
        public_id=public_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ExecuteSSHResponse.model_validate(response.json())
