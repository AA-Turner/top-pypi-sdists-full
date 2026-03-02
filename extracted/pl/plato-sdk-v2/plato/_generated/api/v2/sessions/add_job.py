"""Add Job"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import AddJobRequest, AddJobResponse


def _build_request_args(
    session_id: str,
    body: AddJobRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/sessions/{session_id}/jobs"

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
    session_id: str,
    body: AddJobRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AddJobResponse:
    """Add a new job to an existing session.

    The new job will:
    1. Become part of the session's job group
    2. Be matched to an available VM via the resource matcher
    3. Automatically join the session's WireGuard network if one exists

    If the session has a network (from a previous connect_network call),
    the new job will automatically be added as a member and connected
    when the VM is allocated.

    Use wait_for_ready on the job_id to wait for VM allocation and network setup."""

    request_args = _build_request_args(
        session_id=session_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AddJobResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    body: AddJobRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AddJobResponse:
    """Add a new job to an existing session.

    The new job will:
    1. Become part of the session's job group
    2. Be matched to an available VM via the resource matcher
    3. Automatically join the session's WireGuard network if one exists

    If the session has a network (from a previous connect_network call),
    the new job will automatically be added as a member and connected
    when the VM is allocated.

    Use wait_for_ready on the job_id to wait for VM allocation and network setup."""

    request_args = _build_request_args(
        session_id=session_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AddJobResponse.model_validate(response.json())
