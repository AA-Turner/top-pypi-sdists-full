"""Lookup Package Version"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import PackageLookupResponse


def _build_request_args(
    package_name: str,
    version: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/chronos-packages/{package_name}/versions/{version}"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    package_name: str,
    version: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> PackageLookupResponse:
    """Lookup a specific package version to get artifact ID.

    Args:
        package_name: Name of the package
        version: Semantic version (e.g., 1.0.13)
        principal: Authenticated principal

    Returns:
        Package info with artifact_id for the specific version

    Raises:
        HTTPException: 404 if package/version not found"""

    request_args = _build_request_args(
        package_name=package_name,
        version=version,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return PackageLookupResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    package_name: str,
    version: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> PackageLookupResponse:
    """Lookup a specific package version to get artifact ID.

    Args:
        package_name: Name of the package
        version: Semantic version (e.g., 1.0.13)
        principal: Authenticated principal

    Returns:
        Package info with artifact_id for the specific version

    Raises:
        HTTPException: 404 if package/version not found"""

    request_args = _build_request_args(
        package_name=package_name,
        version=version,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return PackageLookupResponse.model_validate(response.json())
