"""Get Active Session"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import ActiveSessionResponse


def _build_request_args(
    job_group_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/env/{job_group_id}/active_session"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    job_group_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ActiveSessionResponse:
    """Get Active Session"""

    request_args = _build_request_args(
        job_group_id=job_group_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ActiveSessionResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    job_group_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ActiveSessionResponse:
    """Get Active Session"""

    request_args = _build_request_args(
        job_group_id=job_group_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ActiveSessionResponse.model_validate(response.json())
