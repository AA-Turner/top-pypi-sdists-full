"""Handle Get Existing Public Ids"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import ExistingPublicIdsResponse


def _build_request_args(
    import_type: str,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/releases/existing/{import_type}"

    return {
        "method": "GET",
        "url": url,
    }


def sync(
    client: httpx.Client,
    import_type: str,
) -> ExistingPublicIdsResponse:
    """Get all existing public_ids for a given import type on this tenant.
    Useful for checking what already exists before deploying a release.

    Internal service auth required."""

    request_args = _build_request_args(
        import_type=import_type,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ExistingPublicIdsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    import_type: str,
) -> ExistingPublicIdsResponse:
    """Get all existing public_ids for a given import type on this tenant.
    Useful for checking what already exists before deploying a release.

    Internal service auth required."""

    request_args = _build_request_args(
        import_type=import_type,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ExistingPublicIdsResponse.model_validate(response.json())
