"""Take Review Screenshot"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import ScreenshotResponse


def _build_request_args(
    cdp_url: str,
    session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/browser/screenshot"

    params: dict[str, Any] = {}
    if cdp_url is not None:
        params["cdp_url"] = cdp_url
    if session_id is not None:
        params["session_id"] = session_id

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "POST",
        "url": url,
        "params": params,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    cdp_url: str,
    session_id: str | None = None,
    x_api_key: str | None = None,
) -> ScreenshotResponse:
    """Take a screenshot of the current browser page via CDP.

    Optionally uploads to S3 if session_id is provided."""

    request_args = _build_request_args(
        cdp_url=cdp_url,
        session_id=session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ScreenshotResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    cdp_url: str,
    session_id: str | None = None,
    x_api_key: str | None = None,
) -> ScreenshotResponse:
    """Take a screenshot of the current browser page via CDP.

    Optionally uploads to S3 if session_id is provided."""

    request_args = _build_request_args(
        cdp_url=cdp_url,
        session_id=session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ScreenshotResponse.model_validate(response.json())
