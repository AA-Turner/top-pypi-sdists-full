"""List Assignments"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import AssignmentListResponse


def _build_request_args(
    session_id: str | None = None,
    status: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/assignments"

    params: dict[str, Any] = {}
    if session_id is not None:
        params["session_id"] = session_id
    if status is not None:
        params["status"] = status

    headers: dict[str, str] = {}
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
    session_id: str | None = None,
    status: str | None = None,
    x_api_key: str | None = None,
) -> AssignmentListResponse:
    """List assignments for your org."""

    request_args = _build_request_args(
        session_id=session_id,
        status=status,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AssignmentListResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str | None = None,
    status: str | None = None,
    x_api_key: str | None = None,
) -> AssignmentListResponse:
    """List assignments for your org."""

    request_args = _build_request_args(
        session_id=session_id,
        status=status,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AssignmentListResponse.model_validate(response.json())
