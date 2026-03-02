"""Get World Schema"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import WorldSchemaResponse


def _build_request_args(
    package_name: str,
    version: str | None = None,
    allow_prerelease: bool | None = False,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/registry/worlds/{package_name}/schema"

    params: dict[str, Any] = {}
    if version is not None:
        params["version"] = version
    if allow_prerelease is not None:
        params["allow_prerelease"] = allow_prerelease

    return {
        "method": "GET",
        "url": url,
        "params": params,
    }


def sync(
    client: httpx.Client,
    package_name: str,
    version: str | None = None,
    allow_prerelease: bool | None = False,
) -> WorldSchemaResponse:
    """Get schema for a world package from the registry.

    First tries the registry's schema endpoint, then falls back to
    extracting schema.json directly from the wheel."""

    request_args = _build_request_args(
        package_name=package_name,
        version=version,
        allow_prerelease=allow_prerelease,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return WorldSchemaResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    package_name: str,
    version: str | None = None,
    allow_prerelease: bool | None = False,
) -> WorldSchemaResponse:
    """Get schema for a world package from the registry.

    First tries the registry's schema endpoint, then falls back to
    extracting schema.json directly from the wheel."""

    request_args = _build_request_args(
        package_name=package_name,
        version=version,
        allow_prerelease=allow_prerelease,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return WorldSchemaResponse.model_validate(response.json())
