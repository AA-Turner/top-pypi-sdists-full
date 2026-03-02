"""Get App Sim Worker Info"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import AppSimWorkerInfoResponse


def _build_request_args(
    job_group_id: str,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/env/{job_group_id}/app_sim_worker_info"

    return {
        "method": "GET",
        "url": url,
    }


def sync(
    client: httpx.Client,
    job_group_id: str,
) -> AppSimWorkerInfoResponse:
    """Get App Sim Worker Info"""

    request_args = _build_request_args(
        job_group_id=job_group_id,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AppSimWorkerInfoResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    job_group_id: str,
) -> AppSimWorkerInfoResponse:
    """Get App Sim Worker Info"""

    request_args = _build_request_args(
        job_group_id=job_group_id,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AppSimWorkerInfoResponse.model_validate(response.json())
