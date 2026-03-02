"""Get Public Url"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import AppSchemasEnvResponsesPublicUrlResponse


def _build_request_args(
    job_group_id: str,
    port: int | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v1/env/{job_group_id}/public_url"

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
    job_group_id: str,
    port: int | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AppSchemasEnvResponsesPublicUrlResponse:
    """Get the public URL for the environment.

    Args:
        job_group_id: The job group identifier
        port: Optional port to forward to. If provided, the subdomain will be
              formatted as {job_group_id}--{port} to enable port forwarding.

    Returns:
        Public URL in format:
        - https://{job_group_id}.sims.plato.so (no port)
        - https://{job_group_id}--{port}.sims.plato.so (with port)"""

    request_args = _build_request_args(
        job_group_id=job_group_id,
        port=port,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return AppSchemasEnvResponsesPublicUrlResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    job_group_id: str,
    port: int | None = None,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> AppSchemasEnvResponsesPublicUrlResponse:
    """Get the public URL for the environment.

    Args:
        job_group_id: The job group identifier
        port: Optional port to forward to. If provided, the subdomain will be
              formatted as {job_group_id}--{port} to enable port forwarding.

    Returns:
        Public URL in format:
        - https://{job_group_id}.sims.plato.so (no port)
        - https://{job_group_id}--{port}.sims.plato.so (with port)"""

    request_args = _build_request_args(
        job_group_id=job_group_id,
        port=port,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return AppSchemasEnvResponsesPublicUrlResponse.model_validate(response.json())
