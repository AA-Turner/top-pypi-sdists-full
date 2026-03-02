"""Launch Job"""

from __future__ import annotations

from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LaunchJobRequest, LaunchJobResponse


def _build_request_args(
    body: LaunchJobRequest,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/jobs/launch"

    headers: dict[str, str] = {}
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
    body: LaunchJobRequest,
    x_api_key: str | None = None,
) -> LaunchJobResponse:
    """Launch a job with runtime package installation.

    This endpoint creates a VM from a base image and installs the world package
    at runtime via uv. The base image comes from the world's schema.json.

    World and agent code is NOT baked into the image - it's installed at boot time."""

    request_args = _build_request_args(
        body=body,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LaunchJobResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: LaunchJobRequest,
    x_api_key: str | None = None,
) -> LaunchJobResponse:
    """Launch a job with runtime package installation.

    This endpoint creates a VM from a base image and installs the world package
    at runtime via uv. The base image comes from the world's schema.json.

    World and agent code is NOT baked into the image - it's installed at boot time."""

    request_args = _build_request_args(
        body=body,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LaunchJobResponse.model_validate(response.json())
