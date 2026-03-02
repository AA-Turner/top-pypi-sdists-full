"""Get Snapshot Lineage"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import ArtifactLineageResponse, SnapshotConfig


def _build_request_args(
    artifact_id: str,
    include_full_details: bool | None = False,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/cluster/snapshots/lineage"

    params: dict[str, Any] = {}
    if artifact_id is not None:
        params["artifact_id"] = artifact_id
    if include_full_details is not None:
        params["include_full_details"] = include_full_details

    return {
        "method": "GET",
        "url": url,
        "params": params,
    }


def sync(
    client: httpx.Client,
    artifact_id: str,
    include_full_details: bool | None = False,
) -> SnapshotConfig | ArtifactLineageResponse:
    """Build and return the full snapshot lineage for a given artifact ID.

    This works for both regular snapshots and blockdiff checkpoints.

    Args:
        artifact_id: The artifact ID to build lineage for
        include_full_details: If True, returns full artifact details for migration purposes.
                             If False (default), returns minimal SnapshotConfig for VM operations."""

    request_args = _build_request_args(
        artifact_id=artifact_id,
        include_full_details=include_full_details,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return response.json()


async def asyncio(
    client: httpx.AsyncClient,
    artifact_id: str,
    include_full_details: bool | None = False,
) -> SnapshotConfig | ArtifactLineageResponse:
    """Build and return the full snapshot lineage for a given artifact ID.

    This works for both regular snapshots and blockdiff checkpoints.

    Args:
        artifact_id: The artifact ID to build lineage for
        include_full_details: If True, returns full artifact details for migration purposes.
                             If False (default), returns minimal SnapshotConfig for VM operations."""

    request_args = _build_request_args(
        artifact_id=artifact_id,
        include_full_details=include_full_details,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return response.json()
