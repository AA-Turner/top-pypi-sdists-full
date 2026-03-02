"""Get Plato Config"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import PlatoConfig


def _build_request_args(
    job_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/jobs/{job_id}/plato_config"

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
) -> PlatoConfig:
    """Get parsed plato-config for a job's artifact.

    Returns the plato_config YAML content parsed into a typed PlatoConfig object
    with discriminated union types for services and listeners.

    Args:
        job_id: The job public ID.

    Returns:
        PlatoConfig object.

    Raises:
        404: If job not found or plato_config not found.
        400: If job has no artifact_id."""

    request_args = _build_request_args(
        job_id=job_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return PlatoConfig.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    job_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> PlatoConfig:
    """Get parsed plato-config for a job's artifact.

    Returns the plato_config YAML content parsed into a typed PlatoConfig object
    with discriminated union types for services and listeners.

    Args:
        job_id: The job public ID.

    Returns:
        PlatoConfig object.

    Raises:
        404: If job not found or plato_config not found.
        400: If job has no artifact_id."""

    request_args = _build_request_args(
        job_id=job_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return PlatoConfig.model_validate(response.json())
