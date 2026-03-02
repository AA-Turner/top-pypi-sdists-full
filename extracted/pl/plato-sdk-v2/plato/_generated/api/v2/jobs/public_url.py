"""Public Url"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import PublicUrlResult


def _build_request_args(
    job_id: str,
    port: int | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/jobs/{job_id}/public_url"

    params: dict[str, Any] = {}
    if port is not None:
        params["port"] = port

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "params": params,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    job_id: str,
    port: int | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> PublicUrlResult:
    """Get public URL for a specific job.

    Returns browser-accessible URL in format:
    - {job_id}--{port}.sims.plato.so (when port is provided)
    - {job_id}.sims.plato.so (when port is not provided)

    Args:
        job_id: The job public ID.
        port: Port number for the URL (optional).

    Returns:
        PublicUrlResult with public URL.

    Raises:
        404: If job not found."""

    request_args = _build_request_args(
        job_id=job_id,
        port=port,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return PublicUrlResult.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    job_id: str,
    port: int | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> PublicUrlResult:
    """Get public URL for a specific job.

    Returns browser-accessible URL in format:
    - {job_id}--{port}.sims.plato.so (when port is provided)
    - {job_id}.sims.plato.so (when port is not provided)

    Args:
        job_id: The job public ID.
        port: Port number for the URL (optional).

    Returns:
        PublicUrlResult with public URL.

    Raises:
        404: If job not found."""

    request_args = _build_request_args(
        job_id=job_id,
        port=port,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return PublicUrlResult.model_validate(response.json())
