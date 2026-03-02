"""Upload Chronos Package"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import BodyUploadChronosPackage, UploadPackageResponse


def _build_request_args(
    body: BodyUploadChronosPackage,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v2/chronos-packages/upload"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
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
    body: BodyUploadChronosPackage,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> UploadPackageResponse:
    """Upload and publish a chronos package to CodeArtifact.

    This endpoint handles the entire deployment flow securely:
    1. Validates package ownership
    2. Publishes to CodeArtifact using server credentials
    3. Registers artifact in database

    Args:
        package_name: Name of the package
        version: Semantic version (e.g., 1.0.0)
        alias: Display name for the package
        description: Package description
        agents: JSON string of agent names (e.g., '["agent1", "agent2"]')
        wheel_file: Built wheel file (.whl)
        sdist_file: Built source distribution (.tar.gz)
        principal: Authenticated principal

    Returns:
        Upload confirmation with artifact ID

    Raises:
        HTTPException: 403 if package owned by different org, 409 if version exists"""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return UploadPackageResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: BodyUploadChronosPackage,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> UploadPackageResponse:
    """Upload and publish a chronos package to CodeArtifact.

    This endpoint handles the entire deployment flow securely:
    1. Validates package ownership
    2. Publishes to CodeArtifact using server credentials
    3. Registers artifact in database

    Args:
        package_name: Name of the package
        version: Semantic version (e.g., 1.0.0)
        alias: Display name for the package
        description: Package description
        agents: JSON string of agent names (e.g., '["agent1", "agent2"]')
        wheel_file: Built wheel file (.whl)
        sdist_file: Built source distribution (.tar.gz)
        principal: Authenticated principal

    Returns:
        Upload confirmation with artifact ID

    Raises:
        HTTPException: 403 if package owned by different org, 409 if version exists"""

    request_args = _build_request_args(
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return UploadPackageResponse.model_validate(response.json())
