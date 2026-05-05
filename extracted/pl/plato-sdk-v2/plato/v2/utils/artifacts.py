"""Helpers for working with snapshot artifacts."""

from __future__ import annotations

import asyncio
import logging
import time

import httpx

from plato._generated.api.v2.artifacts import get_artifact
from plato._generated.models import ArtifactInfoResponse

logger = logging.getLogger(__name__)

DEFAULT_ARTIFACT_TIMEOUT_SECONDS: float = 600.0
DEFAULT_ARTIFACT_POLL_INTERVAL_SECONDS: float = 5.0
ARTIFACT_READY_STATUS = "ready"
ARTIFACT_TERMINAL_FAILED_STATUSES = frozenset({"failed"})


class ArtifactFailedError(RuntimeError):
    """Raised when an artifact reaches a terminal failure status while polling."""

    def __init__(self, artifact_id: str, status: str):
        super().__init__(f"Artifact {artifact_id} reached terminal status {status!r}")
        self.artifact_id = artifact_id
        self.status = status


async def wait_for_artifact_ready(
    client: httpx.AsyncClient,
    artifact_id: str,
    *,
    api_key: str | None = None,
    timeout: float = DEFAULT_ARTIFACT_TIMEOUT_SECONDS,
    poll_interval: float = DEFAULT_ARTIFACT_POLL_INTERVAL_SECONDS,
) -> ArtifactInfoResponse:
    """Poll the artifact endpoint until the artifact reaches status 'ready'.

    Args:
        client: Async HTTP client used to talk to the Plato API.
        artifact_id: Artifact ID returned from a snapshot/snapshot-store call.
        api_key: Optional X-API-Key header value.
        timeout: Max seconds to wait. Defaults to 10 minutes.
        poll_interval: Seconds between polls. Defaults to 5 seconds.

    Returns:
        The final ArtifactInfoResponse (status == "ready").

    Raises:
        ArtifactFailedError: If the artifact reaches a terminal failure status
            (e.g. "failed") before becoming ready.
        TimeoutError: If the artifact does not reach status 'ready' within `timeout`.
    """
    deadline = time.monotonic() + timeout
    last_status: str | None = None
    while True:
        info = await get_artifact.asyncio(
            client=client,
            artifact_id=artifact_id,
            x_api_key=api_key,
        )
        last_status = info.status
        if last_status == ARTIFACT_READY_STATUS:
            return info
        if last_status in ARTIFACT_TERMINAL_FAILED_STATUSES:
            raise ArtifactFailedError(artifact_id, last_status)

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError(f"Artifact {artifact_id} not ready after {timeout:.0f}s (last status={last_status})")
        await asyncio.sleep(min(poll_interval, remaining))
