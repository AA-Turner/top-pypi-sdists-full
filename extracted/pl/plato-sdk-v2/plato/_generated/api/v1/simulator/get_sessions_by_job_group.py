"""Get Sessions By Job Group"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import SessionListResponse


def _build_request_args(
    job_group_id: str,
    page: int | None = 1,
    page_size: int | None = 50,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/simulator/sessions/by-job-group/{job_group_id}"

    params: dict[str, Any] = {}
    if page is not None:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = page_size

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
    job_group_id: str,
    page: int | None = 1,
    page_size: int | None = 50,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> SessionListResponse:
    """Get paginated list of sessions for a specific job group ID"""

    request_args = _build_request_args(
        job_group_id=job_group_id,
        page=page,
        page_size=page_size,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SessionListResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    job_group_id: str,
    page: int | None = 1,
    page_size: int | None = 50,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> SessionListResponse:
    """Get paginated list of sessions for a specific job group ID"""

    request_args = _build_request_args(
        job_group_id=job_group_id,
        page=page,
        page_size=page_size,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SessionListResponse.model_validate(response.json())
