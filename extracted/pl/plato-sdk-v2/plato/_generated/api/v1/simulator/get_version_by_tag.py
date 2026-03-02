"""Get Version By Tag"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import GetVersionByTagRequest, GetVersionByTagResponse


def _build_request_args(
    body: GetVersionByTagRequest,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/simulator/get-version-by-tag"

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
    }


def sync(
    client: httpx.Client,
    body: GetVersionByTagRequest,
) -> GetVersionByTagResponse:
    """Get the git hash for a simulator by tag name using Postgres.
    This endpoint is used by CI/CD to fetch git hashes for branch tags."""

    request_args = _build_request_args(
        body=body,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return GetVersionByTagResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: GetVersionByTagRequest,
) -> GetVersionByTagResponse:
    """Get the git hash for a simulator by tag name using Postgres.
    This endpoint is used by CI/CD to fetch git hashes for branch tags."""

    request_args = _build_request_args(
        body=body,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return GetVersionByTagResponse.model_validate(response.json())
