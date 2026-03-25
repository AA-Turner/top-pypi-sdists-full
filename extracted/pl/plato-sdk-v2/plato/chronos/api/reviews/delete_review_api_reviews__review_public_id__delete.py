"""Delete Review"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status


def _build_request_args(
    review_public_id: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/reviews/{review_public_id}"

    headers: dict[str, str] = {}
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "DELETE",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    review_public_id: str,
    x_api_key: str | None = None,
) -> None:
    """Delete a review and its annotations. Author only."""

    request_args = _build_request_args(
        review_public_id=review_public_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return None


async def asyncio(
    client: httpx.AsyncClient,
    review_public_id: str,
    x_api_key: str | None = None,
) -> None:
    """Delete a review and its annotations. Author only."""

    request_args = _build_request_args(
        review_public_id=review_public_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return None
