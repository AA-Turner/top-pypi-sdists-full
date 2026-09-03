"""Set Artifact Mcp Config"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import ArtifactInfoResponse, ArtifactMcpConfig


def _build_request_args(
    artifact_id: str,
    body: ArtifactMcpConfig,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/artifacts/{artifact_id}/mcp_config"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "PUT",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    artifact_id: str,
    body: ArtifactMcpConfig,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ArtifactInfoResponse:
    """Set the MCP endpoint config stored on an artifact (admin only).

    The registration/snapshot paths carry mcp_config forward automatically;
    this exists to correct or backfill an already-registered artifact. Readers
    (job MCP URLs, resolve-tag) prefer this over the simulator config."""

    request_args = _build_request_args(
        artifact_id=artifact_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return ArtifactInfoResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    artifact_id: str,
    body: ArtifactMcpConfig,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> ArtifactInfoResponse:
    """Set the MCP endpoint config stored on an artifact (admin only).

    The registration/snapshot paths carry mcp_config forward automatically;
    this exists to correct or backfill an already-registered artifact. Readers
    (job MCP URLs, resolve-tag) prefer this over the simulator config."""

    request_args = _build_request_args(
        artifact_id=artifact_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return ArtifactInfoResponse.model_validate(response.json())
