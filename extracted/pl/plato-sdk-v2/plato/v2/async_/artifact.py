"""Plato SDK v2 - Async Artifact operations."""

from __future__ import annotations

import asyncio
import time

import httpx

from plato._generated.api.v2.artifacts import get_artifact
from plato._generated.models import ArtifactInfoResponse
from plato.v2._wait_for_ready import (
    ARTIFACT_POLL_INTERVAL_SECONDS,
    ARTIFACT_TERMINAL_STATUSES,
    ARTIFACT_WAIT_TIMEOUT_SECONDS,
)


class AsyncArtifactManager:
    """Manager for async artifact operations, accessed via plato.artifacts."""

    def __init__(self, http_client: httpx.AsyncClient, api_key: str):
        self._http = http_client
        self._api_key = api_key

    async def get(self, artifact_id: str) -> ArtifactInfoResponse:
        """Get artifact information by ID.

        Args:
            artifact_id: The artifact ID to look up

        Returns:
            ArtifactInfoResponse with status and metadata

        Raises:
            httpx.HTTPStatusError: If artifact not found or request fails

        Examples:
            >>> from plato.v2 import AsyncPlato
            >>> plato = AsyncPlato()
            >>> artifact = await plato.artifacts.get("abc123")
            >>> print(artifact.status)  # "creating", "ready", or "failed"
        """
        return await get_artifact.asyncio(
            client=self._http,
            artifact_id=artifact_id,
            x_api_key=self._api_key,
        )

    async def wait_for_ready(
        self,
        artifact_id: str,
        *,
        timeout: float = ARTIFACT_WAIT_TIMEOUT_SECONDS,
        poll_interval: float = ARTIFACT_POLL_INTERVAL_SECONDS,
    ) -> ArtifactInfoResponse:
        """Poll the artifact until its snapshot has finished.

        Snapshotting is asynchronous: the snapshot endpoints return once the
        artifact row exists (status ``creating``) while the VM uploads in the
        background, and the artifact can only be started from once it is
        ``ready``. Returns the artifact once its status is ``ready`` or
        ``failed`` — the caller decides what ``failed`` means to it.

        Raises:
            TimeoutError: If the artifact is still creating after ``timeout`` seconds.

        Examples:
            >>> artifact = await plato.artifacts.wait_for_ready(result.artifact_id)
            >>> assert artifact.status == "ready"
        """
        deadline = time.monotonic() + timeout
        while True:
            artifact = await self.get(artifact_id)
            if artifact.status in ARTIFACT_TERMINAL_STATUSES:
                return artifact
            if time.monotonic() >= deadline:
                raise TimeoutError(f"Artifact {artifact_id} still '{artifact.status}' after {timeout:g}s")
            await asyncio.sleep(poll_interval)
