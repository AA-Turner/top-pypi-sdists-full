"""Wait For Ready"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import WaitForReadyResponse


def _build_request_args(
    session_id: str,
    timeout: int | None = 10,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/sessions/{session_id}/wait_for_ready"

    params: dict[str, Any] = {}
    if timeout is not None:
        params["timeout"] = timeout

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "params": params,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    session_id: str,
    timeout: int | None = 10,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> WaitForReadyResponse:
    """Wait for all jobs in a session to be ready (RUNNING status with worker IP).

    Uses the job ready notification service to wait for all jobs in parallel.
    Falls back to checking job status directly if notifications time out.

    Args:
        session_id: The session ID.
        timeout: Maximum time to wait in seconds (default: 300).

    Returns:
        WaitForReadyResponse with ready status for each job.

    Raises:
        404: If session not found.
        408: If jobs don't become ready within timeout."""

    request_args = _build_request_args(
        session_id=session_id,
        timeout=timeout,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return WaitForReadyResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    timeout: int | None = 10,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> WaitForReadyResponse:
    """Wait for all jobs in a session to be ready (RUNNING status with worker IP).

    Uses the job ready notification service to wait for all jobs in parallel.
    Falls back to checking job status directly if notifications time out.

    Args:
        session_id: The session ID.
        timeout: Maximum time to wait in seconds (default: 300).

    Returns:
        WaitForReadyResponse with ready status for each job.

    Raises:
        404: If session not found.
        408: If jobs don't become ready within timeout."""

    request_args = _build_request_args(
        session_id=session_id,
        timeout=timeout,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return WaitForReadyResponse.model_validate(response.json())
