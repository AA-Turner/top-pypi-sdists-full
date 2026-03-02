"""Get Flows"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import Flow


def _build_request_args(
    job_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/jobs/{job_id}/flows"

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
    job_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> list[Flow]:
    """Get parsed flows for a job's artifact.

    Returns the flows YAML content parsed into typed Flow objects with
    discriminated union step types for proper OpenAPI schema generation.

    Args:
        job_id: The job public ID.

    Returns:
        List of Flow objects.

    Raises:
        404: If job not found.
        400: If job has no artifact_id."""

    request_args = _build_request_args(
        job_id=job_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    job_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> list[Flow]:
    """Get parsed flows for a job's artifact.

    Returns the flows YAML content parsed into typed Flow objects with
    discriminated union step types for proper OpenAPI schema generation.

    Args:
        job_id: The job public ID.

    Returns:
        List of Flow objects.

    Raises:
        404: If job not found.
        400: If job has no artifact_id."""

    request_args = _build_request_args(
        job_id=job_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
