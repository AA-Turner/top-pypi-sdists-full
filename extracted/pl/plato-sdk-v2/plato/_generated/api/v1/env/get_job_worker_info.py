"""Get Job Worker Info"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import JobWorkerInfoResponse


def _build_request_args(
    job_public_id: str,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/env/job/{job_public_id}/worker_info"

    return {
        "method": "GET",
        "url": url,
    }


def sync(
    client: httpx.Client,
    job_public_id: str,
) -> JobWorkerInfoResponse:
    """Get worker information for a specific job ID (used by proxy router)."""

    request_args = _build_request_args(
        job_public_id=job_public_id,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return JobWorkerInfoResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    job_public_id: str,
) -> JobWorkerInfoResponse:
    """Get worker information for a specific job ID (used by proxy router)."""

    request_args = _build_request_args(
        job_public_id=job_public_id,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return JobWorkerInfoResponse.model_validate(response.json())
