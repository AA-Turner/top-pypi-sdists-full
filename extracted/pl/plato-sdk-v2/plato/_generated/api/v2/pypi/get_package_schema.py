"""Get Package Schema"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    repo: str,
    package_name: str,
    version: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/pypi/{repo}/packages/{package_name}/schema"

    params: dict[str, Any] = {}
    if version is not None:
        params["version"] = version

    return {
        "method": "GET",
        "url": url,
        "params": params,
    }


def sync(
    client: httpx.Client,
    repo: str,
    package_name: str,
    version: str | None = None,
) -> Any:
    """Get the JSON schema for a package's configuration.

    Extracts schema.json from the package wheel file.
    If version is not specified, uses the latest version.

    The schema file should be at: {package_namespace}/schema.json
    For example: plato/agent/computer_use/schema.json"""

    request_args = _build_request_args(
        repo=repo,
        package_name=package_name,
        version=version,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    repo: str,
    package_name: str,
    version: str | None = None,
) -> Any:
    """Get the JSON schema for a package's configuration.

    Extracts schema.json from the package wheel file.
    If version is not specified, uses the latest version.

    The schema file should be at: {package_namespace}/schema.json
    For example: plato/agent/computer_use/schema.json"""

    request_args = _build_request_args(
        repo=repo,
        package_name=package_name,
        version=version,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
