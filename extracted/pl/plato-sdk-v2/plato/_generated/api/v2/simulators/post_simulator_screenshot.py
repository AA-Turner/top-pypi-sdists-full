"""Post Simulator Screenshot"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import AddScreenshotRequest, AddScreenshotResponse


def _build_request_args(
    name: str,
    body: AddScreenshotRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/simulators/{name}/screenshots"

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
    name: str,
    body: AddScreenshotRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AddScreenshotResponse:
    """Reserve a screenshot slot and return a presigned PUT URL.

    The entry is persisted on the simulator before this call returns, so
    callers only need to do a follow-up PUT of the bytes to `upload_url`."""

    request_args = _build_request_args(
        name=name,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AddScreenshotResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    name: str,
    body: AddScreenshotRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AddScreenshotResponse:
    """Reserve a screenshot slot and return a presigned PUT URL.

    The entry is persisted on the simulator before this call returns, so
    callers only need to do a follow-up PUT of the bytes to `upload_url`."""

    request_args = _build_request_args(
        name=name,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AddScreenshotResponse.model_validate(response.json())
