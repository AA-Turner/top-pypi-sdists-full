"""Get Testcase Metadata For Scoring"""

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
    url = f"/api/v1/testcases/metadata-for-scoring/{public_id}"

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
    public_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Get limited test case metadata for the scoring page.
    Returns: publicId, name, scoringTypes, prompt.
    This endpoint is designed for annotators - prompt is included to help them
    understand what they're evaluating."""

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
    """Get limited test case metadata for the scoring page.
    Returns: publicId, name, scoringTypes, prompt.
    This endpoint is designed for annotators - prompt is included to help them
    understand what they're evaluating."""

    request_args = _build_request_args(
        public_id=public_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
