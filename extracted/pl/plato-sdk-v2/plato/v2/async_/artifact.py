"""Plato SDK v2 - Async Artifact operations."""

from __future__ import annotations

import httpx

from plato._generated.api.v2.artifacts import get_artifact
from plato._generated.models import ArtifactInfoResponse


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
