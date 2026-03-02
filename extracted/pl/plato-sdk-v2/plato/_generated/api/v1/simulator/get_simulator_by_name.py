"""Get Simulator By Name"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    simulator_name: str,
    public_urls_for_reviews: bool | None = False,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/simulator/{simulator_name}"

    params: dict[str, Any] = {}
    if public_urls_for_reviews is not None:
        params["public_urls_for_reviews"] = public_urls_for_reviews

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
    simulator_name: str,
    public_urls_for_reviews: bool | None = False,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Get full simulator object by name.

    If public_urls_for_reviews=true, generates presigned URLs for S3 paths in reviews."""

    request_args = _build_request_args(
        simulator_name=simulator_name,
        public_urls_for_reviews=public_urls_for_reviews,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    simulator_name: str,
    public_urls_for_reviews: bool | None = False,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Get full simulator object by name.

    If public_urls_for_reviews=true, generates presigned URLs for S3 paths in reviews."""

    request_args = _build_request_args(
        simulator_name=simulator_name,
        public_urls_for_reviews=public_urls_for_reviews,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
