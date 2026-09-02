from __future__ import annotations

from typing import Any, List, TypedDict, cast
from typing_extensions import NotRequired, Optional

from .apps import EnvVar, EnvVarInput, EnvVarUpdate, LayerRef
from .bridge import AsyncBridge
from .console import (
    AsyncConsoleClient,
    AsyncPaginatedList,
    PaginatedList,
)
from .utils import convert_to_snake_case


class Layer(TypedDict):
    id: str
    """Unique layer identifier."""

    slug: str
    """Human-readable layer slug."""

    description: NotRequired[str]
    """Optional description of the layer's purpose."""

    layers: List[LayerRef]
    """Base layers included by this layer, in priority order."""

    env_vars: List[EnvVar]
    """Environment variables defined in this layer."""

    app_count: int
    """Number of apps that reference this layer."""

    created_at: str
    """ISO 8601 timestamp of creation."""

    updated_at: str
    """ISO 8601 timestamp of last modification."""


class LayerAppRef(TypedDict):
    id: str
    """Unique app identifier (UUID)."""

    slug: str
    """Human-readable app slug."""

    layer_position: int
    """Index of this layer in the app's layers array."""


class AsyncLayers:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def get(self, id_or_slug: str) -> Layer | None:
        """Get a layer by ID or slug.

        Args:
            id_or_slug: Layer ID or slug.
        """
        result = await self._client.get_or_none(f"/api/v2/layers/{id_or_slug}")
        if result is None:
            return None
        return cast(Layer, convert_to_snake_case(result))

    async def list(
        self,
        *,
        search: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> AsyncPaginatedList[Layer]:
        """List all layers in the organization.

        Args:
            search: Search query for filtering.
            cursor: Pagination cursor.
            limit: Maximum number of items to return.
        """
        params: dict[str, Any] = {}
        if search is not None:
            params["search"] = search
        if cursor is not None:
            params["cursor"] = cursor
        if limit is not None:
            params["limit"] = limit
        return await self._client.get_paginated(
            "/api/v2/layers",
            cursor=None,
            params=params if params else None,
        )

    async def create(
        self,
        slug: str,
        *,
        description: Optional[str] = None,
        layers: Optional[List[str]] = None,
        env_vars: Optional[List[EnvVarInput]] = None,
    ) -> Layer:
        """Create a new layer.

        Args:
            slug: Human-readable layer slug.
            description: Optional description of the layer's purpose.
            layers: Base layer IDs or slugs to include.
            env_vars: Environment variables for this layer.
        """
        body: dict[str, Any] = {"slug": slug}
        if description is not None:
            body["description"] = description
        if layers is not None:
            body["layers"] = layers
        if env_vars is not None:
            body["env_vars"] = env_vars
        result = await self._client.post("/api/v2/layers", body)
        return cast(Layer, convert_to_snake_case(result))

    async def update(
        self,
        layer: str,
        *,
        slug: Optional[str] = None,
        description: Optional[str] = None,
        layers: Optional[List[str]] = None,
        env_vars: Optional[List[EnvVarUpdate]] = None,
    ) -> Layer:
        """Update a layer.

        Args:
            layer: Layer ID or slug.
            slug: New layer slug.
            description: New description.
            layers: Replace all included layers.
            env_vars: Deep merge with existing environment variables.
        """
        body: dict[str, Any] = {}
        if slug is not None:
            body["slug"] = slug
        if description is not None:
            body["description"] = description
        if layers is not None:
            body["layers"] = layers
        if env_vars is not None:
            body["env_vars"] = env_vars
        result = await self._client.patch(f"/api/v2/layers/{layer}", body)
        return cast(Layer, convert_to_snake_case(result))

    async def delete(self, layer: str) -> None:
        """Delete a layer.

        Args:
            layer: Layer ID or slug.
        """
        await self._client.delete(f"/api/v2/layers/{layer}")

    async def apps(
        self,
        layer: str,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> AsyncPaginatedList[LayerAppRef]:
        """List apps that reference this layer.

        Args:
            layer: Layer ID or slug.
            cursor: Pagination cursor.
            limit: Maximum number of items to return.
        """
        params: dict[str, Any] = {}
        if cursor is not None:
            params["cursor"] = cursor
        if limit is not None:
            params["limit"] = limit
        return await self._client.get_paginated(
            f"/api/v2/layers/{layer}/apps",
            cursor=None,
            params=params if params else None,
        )


class Layers:
    def __init__(self, client: AsyncConsoleClient, bridge: AsyncBridge):
        self._client = client
        self._bridge = bridge
        self._async = AsyncLayers(client)

    def get(self, id_or_slug: str) -> Layer | None:
        """Get a layer by ID or slug.

        Args:
            id_or_slug: Layer ID or slug.
        """
        return self._bridge.run(self._async.get(id_or_slug))

    def list(
        self,
        *,
        search: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> PaginatedList[Layer]:
        """List all layers in the organization.

        Args:
            search: Search query for filtering.
            cursor: Pagination cursor.
            limit: Maximum number of items to return.
        """
        paginated = self._bridge.run(
            self._async.list(search=search, cursor=cursor, limit=limit)
        )
        return PaginatedList(self._bridge, paginated)

    def create(
        self,
        slug: str,
        *,
        description: Optional[str] = None,
        layers: Optional[List[str]] = None,
        env_vars: Optional[List[EnvVarInput]] = None,
    ) -> Layer:
        """Create a new layer.

        Args:
            slug: Human-readable layer slug.
            description: Optional description of the layer's purpose.
            layers: Base layer IDs or slugs to include.
            env_vars: Environment variables for this layer.
        """
        return self._bridge.run(
            self._async.create(
                slug, description=description, layers=layers, env_vars=env_vars
            )
        )

    def update(
        self,
        layer: str,
        *,
        slug: Optional[str] = None,
        description: Optional[str] = None,
        layers: Optional[List[str]] = None,
        env_vars: Optional[List[EnvVarUpdate]] = None,
    ) -> Layer:
        """Update a layer.

        Args:
            layer: Layer ID or slug.
            slug: New layer slug.
            description: New description.
            layers: Replace all included layers.
            env_vars: Deep merge with existing environment variables.
        """
        return self._bridge.run(
            self._async.update(
                layer,
                slug=slug,
                description=description,
                layers=layers,
                env_vars=env_vars,
            )
        )

    def delete(self, layer: str) -> None:
        """Delete a layer.

        Args:
            layer: Layer ID or slug.
        """
        self._bridge.run(self._async.delete(layer))

    def apps(
        self,
        layer: str,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> PaginatedList[LayerAppRef]:
        """List apps that reference this layer.

        Args:
            layer: Layer ID or slug.
            cursor: Pagination cursor.
            limit: Maximum number of items to return.
        """
        paginated = self._bridge.run(
            self._async.apps(layer, cursor=cursor, limit=limit)
        )
        return PaginatedList(self._bridge, paginated)
