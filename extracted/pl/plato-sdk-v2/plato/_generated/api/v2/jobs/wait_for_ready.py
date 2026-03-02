"""Wait For Ready"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import WaitForReadyResult


def _build_request_args(
    job_id: str,
    timeout: int | None = 10,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/jobs/{job_id}/wait_for_ready"

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
    job_id: str,
    timeout: int | None = 10,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> WaitForReadyResult:
    """Wait for a job to be ready (RUNNING status with worker IP).

    Uses the job ready notification service to wait for the job to become ready.
    Falls back to checking job status directly if notification times out.

    Args:
        job_id: The job public ID.
        timeout: Maximum time to wait in seconds (default: 300).

    Returns:
        WaitForReadyResult with ready status and worker IPs.

    Raises:
        404: If job not found."""

    request_args = _build_request_args(
        job_id=job_id,
        timeout=timeout,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return WaitForReadyResult.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    job_id: str,
    timeout: int | None = 10,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> WaitForReadyResult:
    """Wait for a job to be ready (RUNNING status with worker IP).

    Uses the job ready notification service to wait for the job to become ready.
    Falls back to checking job status directly if notification times out.

    Args:
        job_id: The job public ID.
        timeout: Maximum time to wait in seconds (default: 300).

    Returns:
        WaitForReadyResult with ready status and worker IPs.

    Raises:
        404: If job not found."""

    request_args = _build_request_args(
        job_id=job_id,
        timeout=timeout,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return WaitForReadyResult.model_validate(response.json())
