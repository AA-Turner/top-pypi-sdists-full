"""Upsert Session Preview Url"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import SessionPreviewUrlsResponse, UpsertSessionPreviewUrlRequest


def _build_request_args(
    public_id: str,
    body: UpsertSessionPreviewUrlRequest,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/sessions/{public_id}/preview-urls"

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
    public_id: str,
    body: UpsertSessionPreviewUrlRequest,
    x_api_key: str | None = None,
) -> SessionPreviewUrlsResponse:
    """Publish an external preview link for a session.

    Labels are unique case-insensitively. Reusing a label replaces its URL in
    place, making repeated world-stage calls idempotent."""

    request_args = _build_request_args(
        public_id=public_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return SessionPreviewUrlsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    public_id: str,
    body: UpsertSessionPreviewUrlRequest,
    x_api_key: str | None = None,
) -> SessionPreviewUrlsResponse:
    """Publish an external preview link for a session.

    Labels are unique case-insensitively. Reusing a label replaces its URL in
    place, making repeated world-stage calls idempotent."""

    request_args = _build_request_args(
        public_id=public_id,
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return SessionPreviewUrlsResponse.model_validate(response.json())
