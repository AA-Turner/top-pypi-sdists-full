"""Fork"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import ForkJobResult


def _build_request_args(
    job_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/jobs/{job_id}/fork"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    job_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ForkJobResult:
    """Fork a running job's VM, creating a cloned VM on the same node.

    The source VM is briefly paused while its memory and disk state are captured,
    then immediately resumed. A new VM boots from the captured state.

    Returns 503 if the worker has no free VM slots."""

    request_args = _build_request_args(
        job_id=job_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ForkJobResult.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    job_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ForkJobResult:
    """Fork a running job's VM, creating a cloned VM on the same node.

    The source VM is briefly paused while its memory and disk state are captured,
    then immediately resumed. A new VM boots from the captured state.

    Returns 503 if the worker has no free VM slots."""

    request_args = _build_request_args(
        job_id=job_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ForkJobResult.model_validate(response.json())
