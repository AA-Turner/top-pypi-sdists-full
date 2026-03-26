"""Create Review Browser"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import AnchorSessionResponse, CreateAnchorSessionRequest


def _build_request_args(
    body: CreateAnchorSessionRequest,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/browser/create"

    headers: dict[str, str] = {}
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
    body: CreateAnchorSessionRequest,
    x_api_key: str | None = None,
) -> AnchorSessionResponse:
    """Create an Anchor Browser session for reviewing a preview.

    Navigates the browser to the target URL. Returns the session info
    including the live_view_url for embedding in an iframe and the
    cdp_url for taking screenshots."""

    request_args = _build_request_args(
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AnchorSessionResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: CreateAnchorSessionRequest,
    x_api_key: str | None = None,
) -> AnchorSessionResponse:
    """Create an Anchor Browser session for reviewing a preview.

    Navigates the browser to the target URL. Returns the session info
    including the live_view_url for embedding in an iframe and the
    cdp_url for taking screenshots."""

    request_args = _build_request_args(
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AnchorSessionResponse.model_validate(response.json())
