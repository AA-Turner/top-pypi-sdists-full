"""List Jobs"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import ListJobsResponse


def _build_request_args(
    session_id: str,
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
        "method": "GET",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    session_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ListJobsResponse:
    """List all jobs in a session."""

    request_args = _build_request_args(
        session_id=session_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ListJobsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ListJobsResponse:
    """List all jobs in a session."""

    request_args = _build_request_args(
        session_id=session_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ListJobsResponse.model_validate(response.json())
