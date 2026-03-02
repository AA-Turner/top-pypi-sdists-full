"""Archive Session Logs Endpoint"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import LogStatusResponse


def _build_request_args(
    session_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/session/{session_id}/logs/archive"

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
    session_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> LogStatusResponse:
    """Manually archive session logs to S3 Glacier Instant Retrieval.

    Returns the status after archiving."""

    request_args = _build_request_args(
        session_id=session_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LogStatusResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> LogStatusResponse:
    """Manually archive session logs to S3 Glacier Instant Retrieval.

    Returns the status after archiving."""

    request_args = _build_request_args(
        session_id=session_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LogStatusResponse.model_validate(response.json())
