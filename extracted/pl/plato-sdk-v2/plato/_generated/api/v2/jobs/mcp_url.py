"""Mcp Url"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import McpUrlResult


def _build_request_args(
    job_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/jobs/{job_id}/mcp_url"

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
) -> McpUrlResult:
    """Get the MCP endpoint URL for a specific job.

    Returns a browser-accessible URL built from the simulator's
    mcp_port/mcp_path config: {job_id}--{mcp_port}.sims.plato.so{mcp_path}

    Args:
        job_id: The job public ID.

    Returns:
        McpUrlResult with the MCP endpoint URL.

    Raises:
        404: If job not found."""

    request_args = _build_request_args(
        job_id=job_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return McpUrlResult.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    job_id: str,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> McpUrlResult:
    """Get the MCP endpoint URL for a specific job.

    Returns a browser-accessible URL built from the simulator's
    mcp_port/mcp_path config: {job_id}--{mcp_port}.sims.plato.so{mcp_path}

    Args:
        job_id: The job public ID.

    Returns:
        McpUrlResult with the MCP endpoint URL.

    Raises:
        404: If job not found."""

    request_args = _build_request_args(
        job_id=job_id,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return McpUrlResult.model_validate(response.json())
