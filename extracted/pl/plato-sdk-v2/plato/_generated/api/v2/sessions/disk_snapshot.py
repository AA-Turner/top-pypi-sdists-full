"""Disk Snapshot"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import CreateDiskSnapshotRequest, CreateDiskSnapshotResponse


def _build_request_args(
    session_id: str,
    body: CreateDiskSnapshotRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/v2/sessions/{session_id}/disk_snapshot"

    headers: dict[str, str] = {}
    if authorization is not None:
        headers["authorization"] = authorization
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
    session_id: str,
    body: CreateDiskSnapshotRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> CreateDiskSnapshotResponse:
    """Create a disk-only snapshot of all jobs in the session (no memory).

    Disk snapshots capture only the disk state. On resume, the VM will do a
    fresh boot with the preserved disk state. This is faster to create and
    smaller to store than full snapshots.

    Optional request body allows overriding artifact metadata:
    - override_service: Override simulator/service name
    - override_version: Override version/git_hash
    - override_dataset: Override dataset name"""

    request_args = _build_request_args(
        session_id=session_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return CreateDiskSnapshotResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    session_id: str,
    body: CreateDiskSnapshotRequest,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> CreateDiskSnapshotResponse:
    """Create a disk-only snapshot of all jobs in the session (no memory).

    Disk snapshots capture only the disk state. On resume, the VM will do a
    fresh boot with the preserved disk state. This is faster to create and
    smaller to store than full snapshots.

    Optional request body allows overriding artifact metadata:
    - override_service: Override simulator/service name
    - override_version: Override version/git_hash
    - override_dataset: Override dataset name"""

    request_args = _build_request_args(
        session_id=session_id,
        body=body,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return CreateDiskSnapshotResponse.model_validate(response.json())
