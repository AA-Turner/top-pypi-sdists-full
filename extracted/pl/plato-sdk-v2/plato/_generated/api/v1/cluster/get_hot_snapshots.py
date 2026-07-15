"""Get Hot Snapshots"""

from __future__ import annotations

from typing import Any

import httpx

from plato._generated.errors import raise_for_status
from plato._generated.models import HotSnapshotsResponse


def _build_request_args(
    lookback_days: int | None = 7,
    max_artifacts: int | None = 5000,
    max_bytes: int | None = None,
    max_docker_images: int | None = 50,
    min_peer_nodes: int | None = 1,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = "/api/v1/cluster/snapshots/hot"

    params: dict[str, Any] = {}
    if lookback_days is not None:
        params["lookback_days"] = lookback_days
    if max_artifacts is not None:
        params["max_artifacts"] = max_artifacts
    if max_bytes is not None:
        params["max_bytes"] = max_bytes
    if max_docker_images is not None:
        params["max_docker_images"] = max_docker_images
    if min_peer_nodes is not None:
        params["min_peer_nodes"] = min_peer_nodes

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
    lookback_days: int | None = 7,
    max_artifacts: int | None = 5000,
    max_bytes: int | None = None,
    max_docker_images: int | None = 50,
    min_peer_nodes: int | None = 1,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> HotSnapshotsResponse:
    """Return the representative 'hot' set a fresh node should prefetch.

    Admin-only. Combines two signals so a freshly-booted node can warm its
    cache before dispatchers accept work (consumed by ``platoctl artifact
    prefetch-hot``):

    - **Hot artifacts**: ranked by job launch count over ``lookback_days``,
      filtered to those at least ``min_peer_nodes`` live peers still hold, then
      truncated to ``max_artifacts`` / ``max_bytes`` (peer-reported sizes).
    - **Hot docker images**: top fresh-boot ECR rootfs images by launch count
      (the node resolves each to a snapshot-store rootfs manifest itself)."""

    request_args = _build_request_args(
        lookback_days=lookback_days,
        max_artifacts=max_artifacts,
        max_bytes=max_bytes,
        max_docker_images=max_docker_images,
        min_peer_nodes=min_peer_nodes,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return HotSnapshotsResponse.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    lookback_days: int | None = 7,
    max_artifacts: int | None = 5000,
    max_bytes: int | None = None,
    max_docker_images: int | None = 50,
    min_peer_nodes: int | None = 1,
    authorization: str | None = None,
    x_api_key: str | None = None,
) -> HotSnapshotsResponse:
    """Return the representative 'hot' set a fresh node should prefetch.

    Admin-only. Combines two signals so a freshly-booted node can warm its
    cache before dispatchers accept work (consumed by ``platoctl artifact
    prefetch-hot``):

    - **Hot artifacts**: ranked by job launch count over ``lookback_days``,
      filtered to those at least ``min_peer_nodes`` live peers still hold, then
      truncated to ``max_artifacts`` / ``max_bytes`` (peer-reported sizes).
    - **Hot docker images**: top fresh-boot ECR rootfs images by launch count
      (the node resolves each to a snapshot-store rootfs manifest itself)."""

    request_args = _build_request_args(
        lookback_days=lookback_days,
        max_artifacts=max_artifacts,
        max_bytes=max_bytes,
        max_docker_images=max_docker_images,
        min_peer_nodes=min_peer_nodes,
        authorization=authorization,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return HotSnapshotsResponse.model_validate(response.json())
