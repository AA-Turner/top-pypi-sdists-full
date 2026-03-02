"""Deploy"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    public_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/releases/{public_id}/deploy"

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
    public_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Deploy a release to tenant. Streams results as NDJSON.

    Each line is a JSON object with:
    - item_type: "simulator", "artifact", "testcase", or "testcase_artifact"
    - item_id: identifier for the item
    - success: bool
    - action: "created", "updated",  or "failed"
    - error: optional error message"""

    request_args = _build_request_args(
        public_id=public_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    public_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Deploy a release to tenant. Streams results as NDJSON.

    Each line is a JSON object with:
    - item_type: "simulator", "artifact", "testcase", or "testcase_artifact"
    - item_id: identifier for the item
    - success: bool
    - action: "created", "updated",  or "failed"
    - error: optional error message"""

    request_args = _build_request_args(
        public_id=public_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
