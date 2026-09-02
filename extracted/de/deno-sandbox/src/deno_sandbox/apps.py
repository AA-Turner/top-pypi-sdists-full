from __future__ import annotations

from typing import Any, AsyncIterator, Dict, Iterator, List, TypedDict, Union, cast
from typing_extensions import Literal, NotRequired, Optional

from .utils import convert_to_snake_case
from .bridge import AsyncBridge
from .console import (
    PaginatedList,
    AsyncConsoleClient,
    AsyncPaginatedList,
)


class EnvVar(TypedDict):
    id: str
    """Unique identifier for the environment variable."""

    key: str
    """The environment variable name."""

    value: NotRequired[str]
    """The value. Omitted when ``secret`` is true."""

    secret: bool
    """Whether the value is masked in API responses."""

    contexts: Union[Literal["all"], list[str]]
    """Deployment contexts this variable applies to."""


class EnvVarInput(TypedDict, total=False):
    key: str
    """The environment variable name."""

    value: str
    """The environment variable value."""

    secret: bool
    """Whether to mask the value in API responses."""

    contexts: Union[Literal["all"], list[str]]
    """Deployment contexts this variable applies to."""


class EnvVarUpdate(TypedDict, total=False):
    id: str
    """ID of the existing variable to update or delete."""

    key: str
    """Variable name. Used for matching when ``id`` is not provided."""

    value: str
    """New value for the variable."""

    secret: bool
    """Whether to mask the value in API responses."""

    contexts: Union[Literal["all"], list[str]]
    """Deployment contexts this variable applies to."""

    delete: bool
    """Set to true to remove this variable."""


class Runtime(TypedDict, total=False):
    type: Literal["dynamic", "static"]
    """``dynamic`` runs a Deno process; ``static`` serves pre-built files."""

    entrypoint: str
    """Main module path. Required when ``type`` is ``dynamic``."""

    args: list[str]
    """Additional CLI arguments passed to the entrypoint."""

    cwd: str
    """Working directory or static file root."""

    spa: bool
    """Enable single-page application mode. Only for ``static`` type."""


class Config(TypedDict, total=False):
    framework: Literal[
        "",
        "nextjs",
        "astro",
        "nuxt",
        "remix",
        "solidstart",
        "tanstackstart",
        "sveltekit",
        "fresh",
        "lume",
    ]
    """Framework preset. Mutually exclusive with ``runtime``."""

    install: str | None
    """Custom install command. Omit to skip the install step."""

    build: str | None
    """Custom build command. Omit to skip the build step."""

    predeploy: str | None
    """Command to run before each deployment. Omit to skip."""

    runtime: Runtime
    """Runtime configuration. Mutually exclusive with ``framework``."""

    crons: bool
    """Whether cron jobs are enabled for revisions of the app. When false, revisions that register cron jobs using ``Deno.cron`` fail to build. Defaults to true."""


class LayerRef(TypedDict):
    id: str
    """Unique layer identifier."""

    slug: str
    """Human-readable layer slug."""


class RuntimeLog(TypedDict, total=False):
    timestamp: str
    """ISO 8601 timestamp of the log entry."""

    level: Literal["debug", "info", "warn", "error"]
    """Log severity level."""

    message: str
    """Log message content."""

    revision_id: str
    """Revision that produced this log entry."""

    region: str
    """Region where the isolate was running."""

    trace_id: str
    """OpenTelemetry trace ID for request correlation."""

    span_id: str
    """OpenTelemetry span ID."""


class RuntimeLogsResponse(TypedDict):
    logs: list[RuntimeLog]
    """Array of log entries."""

    next_cursor: str | None
    """Cursor for fetching the next page, or null if no more results."""


class AppListItem(TypedDict):
    id: str
    """The unique identifier for the app."""

    slug: str
    """The human readable identifier for the app."""

    layers: NotRequired[list[LayerRef]]
    """Layers referenced by this app, in priority order."""

    created_at: str
    """The ISO 8601 timestamp when the app was created."""

    updated_at: str
    """The ISO 8601 timestamp when the app was last updated."""


class App(TypedDict):
    id: str
    """The unique identifier for the app."""

    slug: str
    """The human readable identifier for the app."""

    layers: NotRequired[list[LayerRef]]
    """Layers referenced by this app, in priority order."""

    env_vars: NotRequired[list[EnvVar]]
    """App-specific environment variables."""

    config: NotRequired[Config]
    """Default build and runtime configuration for new revisions."""

    created_at: str
    """The ISO 8601 timestamp when the app was created."""

    updated_at: str
    """The ISO 8601 timestamp when the app was last updated."""


class AsyncApps:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    async def get(self, id_or_slug: str) -> App | None:
        """Get an app by its ID or slug."""
        result = await self._client.get_or_none(f"/api/v2/apps/{id_or_slug}")
        if result is None:
            return None
        raw_result = convert_to_snake_case(result)
        return cast(App, raw_result)

    async def list(
        self,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        labels: Optional[Dict[str, str]] = None,
        layer: Optional[str] = None,
    ) -> AsyncPaginatedList[AppListItem]:
        """List apps of an org.

        Args:
            cursor: The cursor for pagination.
            limit: Limit the number of items to return.
            labels: Filter by labels (e.g. ``{"key": "value"}``).
            layer: Filter by layer ID or slug.
        """
        options: dict[str, Any] = {}
        if cursor is not None:
            options["cursor"] = cursor
        if limit is not None:
            options["limit"] = limit
        if labels is not None:
            for key, value in labels.items():
                options[f"labels[{key}]"] = value
        if layer is not None:
            options["layer"] = layer
        return await self._client.get_paginated(
            "/api/v2/apps", cursor=None, params=options if options else None
        )

    async def create(
        self,
        *,
        slug: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
        layers: Optional[List[str]] = None,
        env_vars: Optional[List[EnvVarInput]] = None,
        config: Optional[Config] = None,
    ) -> App:
        """Create a new app.

        Args:
            slug: Human readable identifier for the app.
            labels: Key-value labels for filtering and grouping.
            layers: Layer IDs or slugs to reference.
            env_vars: App-specific environment variables.
            config: Default build and runtime configuration.
        """
        options: dict[str, Any] = {}
        if slug is not None:
            options["slug"] = slug
        if labels is not None:
            options["labels"] = labels
        if layers is not None:
            options["layers"] = layers
        if env_vars is not None:
            options["env_vars"] = env_vars
        if config is not None:
            options["config"] = config
        result = await self._client.post("/api/v2/apps", options)
        raw_result = convert_to_snake_case(result)
        return cast(App, raw_result)

    async def update(
        self,
        app: str,
        *,
        slug: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
        layers: Optional[List[str]] = None,
        env_vars: Optional[List[EnvVarUpdate]] = None,
        config: Optional[Config] = None,
    ) -> App:
        """Update an existing app.

        Args:
            app: The app ID or slug to update.
            slug: Human readable identifier for the app.
            labels: Replace all labels.
            layers: Replace all layer references.
            env_vars: Deep merge with existing environment variables.
            config: Replace the entire deploy config.
        """
        update: dict[str, Any] = {}
        if slug is not None:
            update["slug"] = slug
        if labels is not None:
            update["labels"] = labels
        if layers is not None:
            update["layers"] = layers
        if env_vars is not None:
            update["env_vars"] = env_vars
        if config is not None:
            update["config"] = config
        result = await self._client.patch(f"/api/v2/apps/{app}", update)
        raw_result = convert_to_snake_case(result)
        return cast(App, raw_result)

    async def delete(self, app: str) -> None:
        """Delete an app by its ID or slug."""
        await self._client.delete(f"/api/v2/apps/{app}")

    async def logs(
        self,
        app: str,
        *,
        start: str,
        end: Optional[str] = None,
        revision_id: Optional[str] = None,
        level: Optional[Literal["debug", "info", "warn", "error"]] = None,
        query: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> RuntimeLogsResponse:
        """Query historical runtime logs for an app.

        Args:
            app: The app ID or slug.
            start: Start of the time range (ISO 8601).
            end: End of the time range (ISO 8601). Defaults to now.
            revision_id: Filter logs by revision ID.
            level: Minimum log severity level.
            query: Full-text search query.
            cursor: The pagination cursor.
            limit: The maximum number of items to return.
        """
        params: dict[str, Any] = {"start": start}
        if end is not None:
            params["end"] = end
        if revision_id is not None:
            params["revision_id"] = revision_id
        if level is not None:
            params["level"] = level
        if query is not None:
            params["query"] = query
        if cursor is not None:
            params["cursor"] = cursor
        if limit is not None:
            params["limit"] = limit
        result = await self._client.get(f"/api/v2/apps/{app}/logs", params)
        return cast(RuntimeLogsResponse, convert_to_snake_case(result))

    async def logs_stream(
        self,
        app: str,
        *,
        start: str,
        end: Optional[str] = None,
        revision_id: Optional[str] = None,
        level: Optional[Literal["debug", "info", "warn", "error"]] = None,
        query: Optional[str] = None,
    ) -> AsyncIterator[RuntimeLog]:
        """Stream runtime logs for an app in real-time.

        Yields RuntimeLog events as they are produced.

        Args:
            app: The app ID or slug.
            start: Start of the time range (ISO 8601).
            end: End of the time range (ISO 8601). Defaults to now.
            revision_id: Filter logs by revision ID.
            level: Minimum log severity level.
            query: Full-text search query.
        """
        params: dict[str, Any] = {"start": start, "stream": "true"}
        if end is not None:
            params["end"] = end
        if revision_id is not None:
            params["revision_id"] = revision_id
        if level is not None:
            params["level"] = level
        if query is not None:
            params["query"] = query
        async for event in self._client.stream_ndjson(
            f"/api/v2/apps/{app}/logs", params=params
        ):
            yield cast(RuntimeLog, convert_to_snake_case(event))


class Apps:
    def __init__(self, client: AsyncConsoleClient, bridge: AsyncBridge):
        self._client = client
        self._bridge = bridge
        self._async = AsyncApps(client)

    def get(self, id_or_slug: str) -> App | None:
        """Get an app by its ID or slug."""
        return self._bridge.run(self._async.get(id_or_slug))

    def list(
        self,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        labels: Optional[Dict[str, str]] = None,
        layer: Optional[str] = None,
    ) -> PaginatedList[AppListItem]:
        """List apps of an org.

        Args:
            cursor: The cursor for pagination.
            limit: Limit the number of items to return.
            labels: Filter by labels (e.g. ``{"key": "value"}``).
            layer: Filter by layer ID or slug.
        """
        paginated = self._bridge.run(
            self._async.list(cursor=cursor, limit=limit, labels=labels, layer=layer)
        )
        return PaginatedList(self._bridge, paginated)

    def create(
        self,
        *,
        slug: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
        layers: Optional[List[str]] = None,
        env_vars: Optional[List[EnvVarInput]] = None,
        config: Optional[Config] = None,
    ) -> App:
        """Create a new app.

        Args:
            slug: Human readable identifier for the app.
            labels: Key-value labels for filtering and grouping.
            layers: Layer IDs or slugs to reference.
            env_vars: App-specific environment variables.
            config: Default build and runtime configuration.
        """
        return self._bridge.run(
            self._async.create(
                slug=slug,
                labels=labels,
                layers=layers,
                env_vars=env_vars,
                config=config,
            )
        )

    def update(
        self,
        app: str,
        *,
        slug: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
        layers: Optional[List[str]] = None,
        env_vars: Optional[List[EnvVarUpdate]] = None,
        config: Optional[Config] = None,
    ) -> App:
        """Update an existing app.

        Args:
            app: The app ID or slug to update.
            slug: Human readable identifier for the app.
            labels: Replace all labels.
            layers: Replace all layer references.
            env_vars: Deep merge with existing environment variables.
            config: Replace the entire deploy config.
        """
        return self._bridge.run(
            self._async.update(
                app,
                slug=slug,
                labels=labels,
                layers=layers,
                env_vars=env_vars,
                config=config,
            )
        )

    def delete(self, app: str) -> None:
        """Delete an app by its ID or slug."""
        self._bridge.run(self._async.delete(app))

    def logs(
        self,
        app: str,
        *,
        start: str,
        end: Optional[str] = None,
        revision_id: Optional[str] = None,
        level: Optional[Literal["debug", "info", "warn", "error"]] = None,
        query: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> RuntimeLogsResponse:
        """Query historical runtime logs for an app.

        Args:
            app: The app ID or slug.
            start: Start of the time range (ISO 8601).
            end: End of the time range (ISO 8601). Defaults to now.
            revision_id: Filter logs by revision ID.
            level: Minimum log severity level.
            query: Full-text search query.
            cursor: The pagination cursor.
            limit: The maximum number of items to return.
        """
        return self._bridge.run(
            self._async.logs(
                app,
                start=start,
                end=end,
                revision_id=revision_id,
                level=level,
                query=query,
                cursor=cursor,
                limit=limit,
            )
        )

    def logs_stream(
        self,
        app: str,
        *,
        start: str,
        end: Optional[str] = None,
        revision_id: Optional[str] = None,
        level: Optional[Literal["debug", "info", "warn", "error"]] = None,
        query: Optional[str] = None,
    ) -> Iterator[RuntimeLog]:
        """Stream runtime logs for an app in real-time.

        Yields RuntimeLog events as they are produced.

        Args:
            app: The app ID or slug.
            start: Start of the time range (ISO 8601).
            end: End of the time range (ISO 8601). Defaults to now.
            revision_id: Filter logs by revision ID.
            level: Minimum log severity level.
            query: Full-text search query.
        """

        async def _collect() -> list[RuntimeLog]:
            return [
                event
                async for event in self._async.logs_stream(
                    app,
                    start=start,
                    end=end,
                    revision_id=revision_id,
                    level=level,
                    query=query,
                )
            ]

        return iter(self._bridge.run(_collect()))
