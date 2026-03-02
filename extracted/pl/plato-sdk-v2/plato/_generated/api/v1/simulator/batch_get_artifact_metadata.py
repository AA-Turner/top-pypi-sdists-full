"""Batch Get Artifact Metadata"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import BatchArtifactMetadataRequest, BatchArtifactMetadataResponse


def _build_request_args(
    body: BatchArtifactMetadataRequest,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/simulator/artifacts/batch-metadata"

    return {
        "method": "POST",
        "url": url,
        "json": body.model_dump(mode="json", exclude_none=True),
    }


def sync(
    client: httpx.Client,
    body: BatchArtifactMetadataRequest,
) -> BatchArtifactMetadataResponse:
    """Get metadata for multiple artifacts by their IDs"""

    request_args = _build_request_args(
        body=body,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return BatchArtifactMetadataResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    body: BatchArtifactMetadataRequest,
) -> BatchArtifactMetadataResponse:
    """Get metadata for multiple artifacts by their IDs"""

    request_args = _build_request_args(
        body=body,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return BatchArtifactMetadataResponse.model_validate(response.json())
