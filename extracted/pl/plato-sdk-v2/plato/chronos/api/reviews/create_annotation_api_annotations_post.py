"""Create Annotation"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import AnnotationResponse, CreateAnnotationRequest


def _build_request_args(
    body: CreateAnnotationRequest,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/annotations"

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
    body: CreateAnnotationRequest,
    x_api_key: str | None = None,
) -> AnnotationResponse:
    """Create an annotation."""

    request_args = _build_request_args(
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AnnotationResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: CreateAnnotationRequest,
    x_api_key: str | None = None,
) -> AnnotationResponse:
    """Create an annotation."""

    request_args = _build_request_args(
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AnnotationResponse.model_validate(response.json())
