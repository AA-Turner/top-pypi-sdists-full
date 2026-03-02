"""Get Public Url"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import AppApiV2SchemasSessionPublicUrlResponse


def _build_request_args(
    session_id: str,
    port: int | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/sessions/{session_id}/public_url"

    params: dict[str, Any] = {}
    if port is not None:
        params["port"] = port

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
    session_id: str,
    port: int | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AppApiV2SchemasSessionPublicUrlResponse:
    """Get public URLs for all jobs in a session.

    Returns browser-accessible URLs in format:
    - {job_id}--{port}.sims.plato.so (when port is provided)
    - {job_id}.sims.plato.so (when port is not provided)

    Args:
        session_id: The session ID.
        port: Port number for the URLs (optional).

    Returns:
        PublicUrlResponse with public URL for each job."""

    request_args = _build_request_args(
        session_id=session_id,
        port=port,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AppApiV2SchemasSessionPublicUrlResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    port: int | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AppApiV2SchemasSessionPublicUrlResponse:
    """Get public URLs for all jobs in a session.

    Returns browser-accessible URLs in format:
    - {job_id}--{port}.sims.plato.so (when port is provided)
    - {job_id}.sims.plato.so (when port is not provided)

    Args:
        session_id: The session ID.
        port: Port number for the URLs (optional).

    Returns:
        PublicUrlResponse with public URL for each job."""

    request_args = _build_request_args(
        session_id=session_id,
        port=port,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AppApiV2SchemasSessionPublicUrlResponse.model_validate(response.json())
