"""Get Next Session For Annotator"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    exclude_session_id: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/session/next-for-annotator"

    params: dict[str, Any] = {}
    if exclude_session_id is not None:
        params["exclude_session_id"] = exclude_session_id

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
    exclude_session_id: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Get Next Session For Annotator"""

    request_args = _build_request_args(
        exclude_session_id=exclude_session_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    exclude_session_id: str | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Get Next Session For Annotator"""

    request_args = _build_request_args(
        exclude_session_id=exclude_session_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
