"""Update Member"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import NetworkMemberResponse, UpdateMemberRequest


def _build_request_args(
    session_id: str,
    job_id: str,
    body: UpdateMemberRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/networks/{session_id}/members/{job_id}"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "PUT",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    session_id: str,
    job_id: str,
    body: UpdateMemberRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> NetworkMemberResponse:
    """Update a network member (e.g., after VM joins with WireGuard info)."""

    request_args = _build_request_args(
        session_id=session_id,
        job_id=job_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return NetworkMemberResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    job_id: str,
    body: UpdateMemberRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> NetworkMemberResponse:
    """Update a network member (e.g., after VM joins with WireGuard info)."""

    request_args = _build_request_args(
        session_id=session_id,
        job_id=job_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return NetworkMemberResponse.model_validate(response.json())
