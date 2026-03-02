"""Get Testcases In Set"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    set_id: int,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/testcases/sets/{set_id}/testcases"

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
    set_id: int,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Get Testcases In Set"""

    request_args = _build_request_args(
        set_id=set_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    set_id: int,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Get Testcases In Set"""

    request_args = _build_request_args(
        set_id=set_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
