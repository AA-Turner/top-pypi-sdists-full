"""Simple Index"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    repo: str,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/pypi/{repo}/simple/"

    return {
        "method": "GET",
        "url": url,
    }


def sync(
    client: httpx.Client,
    repo: str,
) -> Any:
    """List all packages in the repository.

    Returns an HTML page with links to each package, per PEP 503.
    Uses CodeArtifact ListPackages API since the simple index isn't served directly."""

    request_args = _build_request_args(
        repo=repo,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    repo: str,
) -> Any:
    """List all packages in the repository.

    Returns an HTML page with links to each package, per PEP 503.
    Uses CodeArtifact ListPackages API since the simple index isn't served directly."""

    request_args = _build_request_args(
        repo=repo,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
