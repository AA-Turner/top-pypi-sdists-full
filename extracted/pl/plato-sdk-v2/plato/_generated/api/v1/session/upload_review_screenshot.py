"""Upload Review Screenshot"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import BodyUploadReviewScreenshot


def _build_request_args(
    body: BodyUploadReviewScreenshot,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/session/upload-review-screenshot"

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
    body: BodyUploadReviewScreenshot,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Upload a review screenshot to S3.
    Used by the data-review Chrome extension to upload annotated screenshots.
    Supports both user session and API key authentication."""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    body: BodyUploadReviewScreenshot,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> Any:
    """Upload a review screenshot to S3.
    Used by the data-review Chrome extension to upload annotated screenshots.
    Supports both user session and API key authentication."""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
