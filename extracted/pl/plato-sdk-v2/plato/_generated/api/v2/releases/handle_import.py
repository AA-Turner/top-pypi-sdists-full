"""Handle Import"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import ImportRequest, ImportResponse


def _build_request_args(
    body: ImportRequest,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/releases/import"

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
    }


def sync(
    client: httpx.Client,
    body: ImportRequest,
) -> ImportResponse:
    """Import a single item. IDs are preserved exactly from source.
    - simulator: create or update by name
    - others: create only (skip if exists by id)

    Returns 500 on any error. Internal service auth required."""

    request_args = _build_request_args(
        body=body,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ImportResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: ImportRequest,
) -> ImportResponse:
    """Import a single item. IDs are preserved exactly from source.
    - simulator: create or update by name
    - others: create only (skip if exists by id)

    Returns 500 on any error. Internal service auth required."""

    request_args = _build_request_args(
        body=body,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ImportResponse.model_validate(response.json())
