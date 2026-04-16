"""Delete Annotation"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status


def _build_request_args(
    annotation_public_id: str,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/annotations/{annotation_public_id}"

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
    annotation_public_id: str,
    x_api_key: str | None = None,
) -> None:
    """Delete an annotation and descendants. Author only (admin can delete any)."""

    request_args = _build_request_args(
        annotation_public_id=annotation_public_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return None


async def asyncio(
    client: httpx.AsyncClient,
    annotation_public_id: str,
    x_api_key: str | None = None,
) -> None:
    """Delete an annotation and descendants. Author only (admin can delete any)."""

    request_args = _build_request_args(
        annotation_public_id=annotation_public_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return None
