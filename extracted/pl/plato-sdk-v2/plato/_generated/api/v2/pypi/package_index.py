"""Package Index"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    repo: str,
    package_name: str,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/pypi/{repo}/simple/{package_name}/"

    return {
        "method": "GET",
        "url": url,
    }


def sync(
    client: httpx.Client,
    repo: str,
    package_name: str,
) -> Any:
    """List all versions/files for a specific package.

    Returns an HTML page with links to each file (wheel, sdist), per PEP 503.
    URLs are rewritten to point to our proxy instead of CodeArtifact."""

    request_args = _build_request_args(
        repo=repo,
        package_name=package_name,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    repo: str,
    package_name: str,
) -> Any:
    """List all versions/files for a specific package.

    Returns an HTML page with links to each file (wheel, sdist), per PEP 503.
    URLs are rewritten to point to our proxy instead of CodeArtifact."""

    request_args = _build_request_args(
        repo=repo,
        package_name=package_name,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
