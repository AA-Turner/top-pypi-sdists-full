"""Upload Package"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status


def _build_request_args(
    repo: str,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/pypi/{repo}/"

    return {
        "method": "POST",
        "url": url,
    }


def sync(
    client: httpx.Client,
    repo: str,
) -> Any:
    """Upload a package to the repository.

    Accepts multipart form data as sent by twine or uv publish.
    The 'name' field must be included in the form data for permission checking."""

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
    """Upload a package to the repository.

    Accepts multipart form data as sent by twine or uv publish.
    The 'name' field must be included in the form data for permission checking."""

    request_args = _build_request_args(
        repo=repo,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
