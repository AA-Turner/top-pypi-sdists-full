"""Get Review Widget Schema"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import ReviewWidgetSchemaResponse


def _build_request_args() -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/reviews/schema/widgets"

    return {
        "method": "GET",
        "url": url,
    }


def sync(
    client: httpx.Client,
) -> ReviewWidgetSchemaResponse:
    """Return available render and feedback widgets."""

    request_args = _build_request_args()

    response = client.request(**request_args)
    raise_for_status(response)
    return ReviewWidgetSchemaResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
) -> ReviewWidgetSchemaResponse:
    """Return available render and feedback widgets."""

    request_args = _build_request_args()

    response = await client.request(**request_args)
    raise_for_status(response)
    return ReviewWidgetSchemaResponse.model_validate(response.json())
