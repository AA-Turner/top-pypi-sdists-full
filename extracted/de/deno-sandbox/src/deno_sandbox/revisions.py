from __future__ import annotations

import warnings
from typing import (
    Any,
    AsyncIterator,
    Dict,
    Iterator,
    List,
    TypedDict,
    Union,
    cast,
    overload,
)
from typing_extensions import Literal, NotRequired, Optional

from .apps import Config, EnvVar, LayerRef
from .timelines import Timeline

from .bridge import AsyncBridge
from .console import (
    AsyncConsoleClient,
    AsyncPaginatedList,
    PaginatedList,
)
from .utils import convert_to_snake_case


class FileAsset(TypedDict):
    kind: Literal["file"]
    encoding: Literal["utf-8", "base64"]
    content: str


class SymlinkAsset(TypedDict):
    kind: Literal["symlink"]
    target: str


Asset = Union[FileAsset, SymlinkAsset]


class EnvVarInputForDeploy(TypedDict):
    key: str
    value: str


# A revision's garbage-collection policy. "auto" follows the normal
# inactivity-based cleanup; "indefinite" exempts the revision from automatic
# deletion (enterprise opt-in).
RevisionRetention = Literal["auto", "indefinite"]


class RevisionListItem(TypedDict):
    id: str
    """The unique identifier for the revision."""

    status: Literal["skipped", "queued", "building", "succeeded", "failed"]
    """The current revision lifecycle status."""

    failure_reason: str | None
    """Reason for failure, or null if not failed."""

    created_at: str
    """The ISO 8601 timestamp when the revision was created."""

    cancellation_requested_at: str | None
    """ISO 8601 timestamp when cancellation was requested, or null."""

    build_finished_at: str | None
    """ISO 8601 timestamp when the build completed, or null if still building."""

    deleted_at: str | None
    """ISO 8601 timestamp of deletion, or null if active."""

    retention: NotRequired[RevisionRetention]
    """Garbage-collection policy: "auto" (normal inactivity-based cleanup) or
    "indefinite" (exempt from automatic deletion).

    Only present for enterprise organizations opted in to revision retention."""


class Revision(TypedDict):
    id: str
    """The unique identifier for the revision."""

    status: Literal["skipped", "queued", "building", "succeeded", "failed"]
    """The current revision lifecycle status."""

    failure_reason: str | None
    """Reason for failure, or null if not failed."""

    layers: NotRequired[list[LayerRef]]
    """Layers referenced by this revision, in priority order."""

    env_vars: NotRequired[list[EnvVar]]
    """Revision-specific environment variables (immutable once created)."""

    config: NotRequired[Config]
    """Build and runtime configuration used for this revision."""

    created_at: str
    """The ISO 8601 timestamp when the revision was created."""

    cancellation_requested_at: str | None
    """ISO 8601 timestamp when cancellation was requested, or null."""

    build_finished_at: str | None
    """ISO 8601 timestamp when the build completed, or null if still building."""

    deleted_at: str | None
    """ISO 8601 timestamp of deletion, or null if active."""

    retention: NotRequired[RevisionRetention]
    """Garbage-collection policy: "auto" (normal inactivity-based cleanup) or
    "indefinite" (exempt from automatic deletion).

    Only present for enterprise organizations opted in to revision retention."""


ProgressStageStatus = Literal[
    "pending",
    "running",
    "succeeded",
    "skipped",
    "failed",
    "timed_out",
    "cancelled",
    "errored",
]


class ProgressStage(TypedDict):
    status: ProgressStageStatus
    """The current status of this stage."""

    start: NotRequired[str | None]
    """ISO 8601 timestamp when the stage started, or null."""

    end: NotRequired[str | None]
    """ISO 8601 timestamp when the stage ended, or null."""


class RevisionProgress(TypedDict):
    queued: NotRequired[ProgressStage]
    """Queue stage status."""

    preparing: NotRequired[ProgressStage]
    """Preparation stage status."""

    installing: NotRequired[ProgressStage]
    """Dependency installation stage status."""

    building: NotRequired[ProgressStage]
    """Build command execution stage status."""

    deploying: NotRequired[ProgressStage]
    """Artifact upload and routing stage status."""


BuildStep = Literal["preparing", "installing", "building", "deploying"]


class BuildLogEntry(TypedDict):
    timestamp: str
    """ISO 8601 timestamp of the log entry."""

    level: Literal["debug", "info", "warn", "error"]
    """Log severity level."""

    message: str
    """Log message content."""

    step: NotRequired[BuildStep]
    """Build step that produced this log."""

    timeline: NotRequired[str]
    """Timeline slug, if the log is associated with a specific timeline."""


# Keep old name as alias for backward compatibility
RevisionWithoutTimelines = RevisionListItem


class AsyncRevisions:
    def __init__(self, client: AsyncConsoleClient):
        self._client = client

    @overload
    async def get(self, id: str) -> Revision | None: ...

    @overload
    async def get(self, app: str, id: str) -> Revision | None: ...

    async def get(self, *args: str) -> Revision | None:
        """Get a revision by its ID.

        Args:
            id: The revision ID (globally unique).

        .. deprecated::
            The two-argument form ``get(app, id)`` is deprecated.
            Use ``get(id)`` instead — revision IDs are globally unique.
        """
        if len(args) == 2:
            warnings.warn(
                "revisions.get(app, id) is deprecated. "
                "Use revisions.get(id) instead — revision IDs are globally unique.",
                DeprecationWarning,
                stacklevel=2,
            )
            revision_id = args[1]
        elif len(args) == 1:
            revision_id = args[0]
        else:
            raise TypeError(
                f"get() takes 1 or 2 positional arguments but {len(args)} were given"
            )

        result = await self._client.get_or_none(f"/api/v2/revisions/{revision_id}")
        if result is None:
            return None
        raw_result = convert_to_snake_case(result)
        return cast(Revision, raw_result)

    async def list(
        self,
        app: str,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        status: Optional[
            Literal["skipped", "queued", "building", "succeeded", "failed"]
        ] = None,
    ) -> AsyncPaginatedList[RevisionListItem]:
        """List revisions for a specific app.

        Args:
            app: The app ID or slug.
            cursor: The cursor for pagination.
            limit: Limit the number of items to return.
            status: Filter by revision status.
        """
        options: dict[str, Any] = {}
        if cursor is not None:
            options["cursor"] = cursor
        if limit is not None:
            options["limit"] = limit
        if status is not None:
            options["status"] = status
        return await self._client.get_paginated(
            f"/api/v2/apps/{app}/revisions",
            cursor=None,
            params=options if options else None,
        )

    async def delete(self, revision: str) -> None:
        """Delete a revision.

        Cannot delete active or currently building revisions.

        Args:
            revision: The revision ID.
        """
        await self._client.delete(f"/api/v2/revisions/{revision}")

    async def cancel(self, revision: str) -> Revision:
        """Cancel a revision build.

        Cancellation is asynchronous — this returns immediately with the current
        revision state. The ``cancellation_requested_at`` field will be set, but
        the revision may still be in ``building`` status. Poll the revision or use
        the progress endpoint to wait for the ``failed`` state.

        Args:
            revision: The revision ID.
        """
        result = await self._client.post(f"/api/v2/revisions/{revision}/cancel", {})
        return cast(Revision, convert_to_snake_case(result))

    async def progress(self, revision: str) -> AsyncIterator[RevisionProgress]:
        """Stream revision build progress.

        Yields RevisionProgress events as the revision progresses through
        its build stages. The stream ends when the revision reaches a
        terminal state (succeeded, failed, or skipped).

        Args:
            revision: The revision ID.
        """
        async for event in self._client.stream_ndjson(
            f"/api/v2/revisions/{revision}/progress"
        ):
            yield cast(RevisionProgress, convert_to_snake_case(event))

    async def build_logs(
        self,
        revision: str,
        *,
        step: Optional[BuildStep] = None,
        timeline: Optional[str] = None,
    ) -> AsyncIterator[BuildLogEntry]:
        """Stream build logs for a revision.

        Yields BuildLogEntry events as they are produced during the build.

        Args:
            revision: The revision ID.
            step: Filter logs by build step.
            timeline: Filter logs by timeline slug.
        """
        params: dict[str, Any] = {}
        if step is not None:
            params["step"] = step
        if timeline is not None:
            params["timeline"] = timeline
        async for event in self._client.stream_ndjson(
            f"/api/v2/revisions/{revision}/build_logs",
            params=params if params else None,
        ):
            yield cast(BuildLogEntry, convert_to_snake_case(event))

    async def timelines(self, revision: str) -> List[Timeline]:
        """Get timelines for a revision.

        Args:
            revision: The revision ID.
        """
        result = await self._client.get(f"/api/v2/revisions/{revision}/timelines")
        return [cast(Timeline, convert_to_snake_case(item)) for item in result]

    async def deploy(
        self,
        app: str,
        assets: Dict[str, Asset],
        *,
        config: Optional[Config] = None,
        layers: Optional[List[str]] = None,
        env_vars: Optional[List[EnvVarInputForDeploy]] = None,
        labels: Optional[Dict[str, str]] = None,
        production: Optional[bool] = None,
        preview: Optional[bool] = None,
        retention: Optional[RevisionRetention] = None,
    ) -> Revision:
        """Deploy a revision by uploading source files as assets.

        Args:
            app: The app ID or slug.
            assets: Dict mapping file paths to Asset objects.
            config: Optional build/runtime configuration.
            layers: Layer IDs or slugs to reference for this revision.
            env_vars: Optional environment variables for this revision.
            labels: Optional labels (e.g., git metadata).
            production: Whether to deploy to the production timeline.
                Defaults to true on the server.
            preview: Whether to deploy as a preview deployment.
                Defaults to false on the server.
            retention: Garbage-collection policy for the new revision. "auto"
                (the default) follows the normal inactivity-based cleanup;
                "indefinite" exempts it from automatic deletion. "indefinite"
                is enterprise opt-in and is rejected without the entitlement.

        Returns:
            The created Revision (build is async; poll for status).
        """
        body: Dict[str, Any] = {"assets": assets}
        if config is not None:
            body["config"] = config
        if layers is not None:
            body["layers"] = layers
        if env_vars is not None:
            body["env_vars"] = env_vars
        if labels is not None:
            body["labels"] = labels
        if production is not None:
            body["production"] = production
        if preview is not None:
            body["preview"] = preview
        if retention is not None:
            body["retention"] = retention
        result = await self._client.post(f"/api/v2/apps/{app}/deploy", body)
        return cast(Revision, convert_to_snake_case(result))

    async def set_retention(
        self, revision: str, retention: RevisionRetention
    ) -> Revision:
        """Set a revision's garbage-collection policy.

        "auto" follows the normal inactivity-based cleanup; "indefinite"
        exempts the revision from automatic deletion. "indefinite" is only
        available to enterprise organizations that have opted in to revision
        retention — contact Deno support to enable it, and it is rejected
        without the entitlement. Setting "auto" is always permitted for an
        already-retained revision.

        Args:
            revision: The revision ID.
            retention: The garbage-collection policy ("auto" or "indefinite").

        Returns:
            The updated Revision.
        """
        result = await self._client.patch(
            f"/api/v2/revisions/{revision}", {"retention": retention}
        )
        return cast(Revision, convert_to_snake_case(result))


class Revisions:
    def __init__(self, client: AsyncConsoleClient, bridge: AsyncBridge):
        self._client = client
        self._bridge = bridge
        self._async = AsyncRevisions(client)

    @overload
    def get(self, id: str) -> Revision | None: ...

    @overload
    def get(self, app: str, id: str) -> Revision | None: ...

    def get(self, *args: str) -> Revision | None:
        """Get a revision by its ID.

        Args:
            id: The revision ID (globally unique).

        .. deprecated::
            The two-argument form ``get(app, id)`` is deprecated.
            Use ``get(id)`` instead — revision IDs are globally unique.
        """
        return self._bridge.run(self._async.get(*args))

    def list(
        self,
        app: str,
        *,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
        status: Optional[
            Literal["skipped", "queued", "building", "succeeded", "failed"]
        ] = None,
    ) -> PaginatedList[RevisionListItem]:
        """List revisions for a specific app.

        Args:
            app: The app ID or slug.
            cursor: The cursor for pagination.
            limit: Limit the number of items to return.
            status: Filter by revision status.
        """
        paginated = self._bridge.run(
            self._async.list(app, cursor=cursor, limit=limit, status=status)
        )
        return PaginatedList(self._bridge, paginated)

    def delete(self, revision: str) -> None:
        """Delete a revision.

        Cannot delete active or currently building revisions.

        Args:
            revision: The revision ID.
        """
        self._bridge.run(self._async.delete(revision))

    def cancel(self, revision: str) -> Revision:
        """Cancel a revision build.

        Args:
            revision: The revision ID.
        """
        return self._bridge.run(self._async.cancel(revision))

    def progress(self, revision: str) -> Iterator[RevisionProgress]:
        """Stream revision build progress.

        Yields RevisionProgress events as the revision progresses through
        its build stages. The stream ends when the revision reaches a
        terminal state (succeeded, failed, or skipped).

        Args:
            revision: The revision ID.
        """

        async def _collect() -> list[RevisionProgress]:
            return [event async for event in self._async.progress(revision)]

        return iter(self._bridge.run(_collect()))

    def build_logs(
        self,
        revision: str,
        *,
        step: Optional[BuildStep] = None,
        timeline: Optional[str] = None,
    ) -> Iterator[BuildLogEntry]:
        """Stream build logs for a revision.

        Yields BuildLogEntry events as they are produced during the build.

        Args:
            revision: The revision ID.
            step: Filter logs by build step.
            timeline: Filter logs by timeline slug.
        """

        async def _collect() -> list[BuildLogEntry]:
            return [
                event
                async for event in self._async.build_logs(
                    revision, step=step, timeline=timeline
                )
            ]

        return iter(self._bridge.run(_collect()))

    def timelines(self, revision: str) -> List[Timeline]:
        """Get timelines for a revision.

        Args:
            revision: The revision ID.
        """
        return self._bridge.run(self._async.timelines(revision))

    def deploy(
        self,
        app: str,
        assets: Dict[str, Asset],
        *,
        config: Optional[Config] = None,
        layers: Optional[List[str]] = None,
        env_vars: Optional[List[EnvVarInputForDeploy]] = None,
        labels: Optional[Dict[str, str]] = None,
        production: Optional[bool] = None,
        preview: Optional[bool] = None,
        retention: Optional[RevisionRetention] = None,
    ) -> Revision:
        """Deploy a revision by uploading source files as assets.

        Args:
            app: The app ID or slug.
            assets: Dict mapping file paths to Asset objects.
            config: Optional build/runtime configuration.
            layers: Layer IDs or slugs to reference for this revision.
            env_vars: Optional environment variables for this revision.
            labels: Optional labels (e.g., git metadata).
            production: Whether to deploy to the production timeline.
                Defaults to true on the server.
            preview: Whether to deploy as a preview deployment.
                Defaults to false on the server.
            retention: Garbage-collection policy for the new revision. "auto"
                (the default) follows the normal inactivity-based cleanup;
                "indefinite" exempts it from automatic deletion. "indefinite"
                is enterprise opt-in and is rejected without the entitlement.

        Returns:
            The created Revision (build is async; poll for status).
        """
        return self._bridge.run(
            self._async.deploy(
                app,
                assets,
                config=config,
                layers=layers,
                env_vars=env_vars,
                labels=labels,
                production=production,
                preview=preview,
                retention=retention,
            )
        )

    def set_retention(self, revision: str, retention: RevisionRetention) -> Revision:
        """Set a revision's garbage-collection policy.

        "auto" follows the normal inactivity-based cleanup; "indefinite"
        exempts the revision from automatic deletion. "indefinite" is only
        available to enterprise organizations that have opted in to revision
        retention — contact Deno support to enable it, and it is rejected
        without the entitlement. Setting "auto" is always permitted for an
        already-retained revision.

        Args:
            revision: The revision ID.
            retention: The garbage-collection policy ("auto" or "indefinite").

        Returns:
            The updated Revision.
        """
        return self._bridge.run(self._async.set_retention(revision, retention))
