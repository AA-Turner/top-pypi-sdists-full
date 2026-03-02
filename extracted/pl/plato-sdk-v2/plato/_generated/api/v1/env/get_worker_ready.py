"""Get Worker Ready"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import WorkerReadyResponse


def _build_request_args(
    job_id: str,
    timeout: int | None = 300,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/env/{job_id}/worker_ready"

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
    timeout: int | None = 300,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> WorkerReadyResponse:
    """Check if the workers for this job group are ready and healthy.

    Uses the persistent job ready notification service to wait for job readiness.
    Falls back to checking Redis if notification not received (in case we missed it).
    Raises 500 if job not ready after all checks."""

    request_args = _build_request_args(
        job_id=job_id,
        timeout=timeout,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return WorkerReadyResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    job_id: str,
    timeout: int | None = 300,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> WorkerReadyResponse:
    """Check if the workers for this job group are ready and healthy.

    Uses the persistent job ready notification service to wait for job readiness.
    Falls back to checking Redis if notification not received (in case we missed it).
    Raises 500 if job not ready after all checks."""

    request_args = _build_request_args(
        job_id=job_id,
        timeout=timeout,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return WorkerReadyResponse.model_validate(response.json())
