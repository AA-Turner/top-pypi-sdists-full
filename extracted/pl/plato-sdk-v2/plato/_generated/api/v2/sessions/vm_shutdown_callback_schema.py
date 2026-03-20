"""VM shutdown callback webhook schema"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import VMShutdownCallbackPayload


def _build_request_args(
    body: VMShutdownCallbackPayload,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/sessions/webhook-schemas/vm-shutdown"

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
    }


def sync(
    client: httpx.Client,
    body: VMShutdownCallbackPayload,
) -> Any:
    """Documents the payload shape POSTed to shutdown_callback_url. This endpoint is not called directly — it exists so the OpenAPI spec includes VMShutdownCallbackPayload for SDK generation."""

    request_args = _build_request_args(
        body=body,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    body: VMShutdownCallbackPayload,
) -> Any:
    """Documents the payload shape POSTed to shutdown_callback_url. This endpoint is not called directly — it exists so the OpenAPI spec includes VMShutdownCallbackPayload for SDK generation."""

    request_args = _build_request_args(
        body=body,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
