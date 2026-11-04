"""Configurations — the versioned settings a workspace runs with."""

from __future__ import annotations

# Python internals
from dataclasses import dataclass
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterable,
    Awaitable,
    BinaryIO,
    Iterable,
    overload,
)

# Current package
from dlthub_sdk._glue.base import Collection, Entity
from dlthub_sdk._glue.context import Async, Listing, M, Sync, _Ctx
from dlthub_sdk._glue.enums import EntityKind
from dlthub_sdk.domain.files import FileEntry
from dlthub_sdk.errors import NotFound

if TYPE_CHECKING:
    # Typing only: domain never imports _gen at runtime.
    # Current package
    from dlthub_sdk._gen.api.models import (
        ConfigurationResponse,
        ListPageConfigurationResponse,
    )
    from dlthub_sdk._gen.dataplane_api.models import (
        ConfigurationResponse as DataplaneConfigurationResponse,
    )

    #: The upload answers with the data plane's own copy of the class.
    ConfigurationPayload = ConfigurationResponse | DataplaneConfigurationResponse


@dataclass(frozen=True, repr=False)
class Configuration(Entity[M]):
    """One uploaded version of a workspace's configuration."""

    version: int
    """Version number within the workspace, starting at 1 and incremented by each
    upload.
    """
    id: str
    """Unique ID (a UUID)."""
    content_hash: str
    """Hash of the package contents: base64 SHA3-256 over each file's path and digest,
    as dlt computes when building the package; identical file sets give identical
    hashes.
    """
    file_count: int
    """Number of files in the package."""
    size_bytes: int
    """Size of the uploaded package in bytes."""
    profiles: tuple[str, ...]
    """Profile names found in `<profile>.config.toml` / `<profile>.secrets.toml` file
    names, sorted.
    """
    created_at: datetime
    """When it was created."""
    created_by: str
    """The `organization_membership_id` of the member who uploaded it."""
    updated_at: datetime
    """When it was last changed."""

    _identity = ("version", "id")
    _kind = EntityKind.CONFIGURATION

    @overload
    def files(self: Configuration[Sync]) -> tuple[FileEntry, ...]: ...

    @overload
    def files(self: Configuration[Async]) -> Awaitable[tuple[FileEntry, ...]]: ...

    def files(self) -> tuple[FileEntry, ...] | Awaitable[tuple[FileEntry, ...]]:
        """List the files this configuration holds.

        The manifest is stored with the content rather than with the record,
        so this is a fresh read every time.

        Returns:
            One entry per file, in the platform's order; awaitable in async mode.

        Raises:
            DataplaneTokenRejected: The data plane rejected the token the
                platform issued for it.
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            NotFound: The configuration no longer exists.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()
        configuration_id = self.id
        return self._ctx.run(
            lambda t: t.get_configuration_files(
                workspace_id=workspace_id,
                dataplane_url=dataplane_url,
                configuration_id=configuration_id,
            ),
            FileEntry._all_from_payload,
        )

    @staticmethod
    def _from_payload(
        ctx: _Ctx[Any], payload: ConfigurationPayload
    ) -> Configuration[Any]:
        return Configuration._bind(
            ctx,
            Configuration(
                version=payload.version,
                id=str(payload.id),
                content_hash=payload.content_hash,
                file_count=payload.file_count,
                size_bytes=payload.size_bytes,
                profiles=tuple(payload.profiles),
                created_at=payload.created_at,
                created_by=str(payload.created_by),
                updated_at=payload.updated_at,
            ),
        )


class Configurations(Collection[M]):
    """The configurations of one workspace.

    :meth:`list` yields the newest version first.
    """

    _entity = Configuration

    def _listing(self) -> Listing[ConfigurationResponse]:
        workspace_id = self._ctx.require_workspace()
        return lambda t, limit, offset: t.list_configurations(
            workspace_id=workspace_id, limit=limit, offset=offset, version=None
        )

    @overload
    def upload(
        self: Configurations[Sync], *, data: bytes | BinaryIO
    ) -> Configuration[Sync]: ...

    @overload
    def upload(
        self: Configurations[Async], *, data: bytes | BinaryIO
    ) -> Awaitable[Configuration[Async]]: ...

    def upload(
        self, *, data: bytes | BinaryIO
    ) -> Configuration[Any] | Awaitable[Configuration[Any]]:
        """Store a new version of the workspace's configuration.

        The platform reads the package for the hash, the file list and the
        profile names. To skip an unchanged upload, compare the hash dlt's
        package builder returned with ``latest().content_hash``.

        Args:
            data: A configuration package built by dlt's package builder (a
                gzipped tar of the ``.dlt`` settings folder that carries dlt's
                ``manifest.yaml``), as bytes or a binary file object.

        Returns:
            The stored configuration, one version above the last; awaitable in
            async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            Conflict: The current state does not allow the call, e.g. the workspace is
                archived; `code` and `message` say why.
            DataplaneTokenRejected: The data plane rejected the token the
                platform issued for it.
            InvalidResponse: The platform returned an upload address this SDK
                version cannot use; upgrade dlthub-client.
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            ScopeMissing: Reached without a workspace in scope.
            TransportError: The upload did not complete. A version is written
                only once the content arrives, but a request that never
                produced a response cannot say whether it did — read
                ``latest()`` before retrying.
        """
        workspace_id = self._ctx.require_workspace()
        return self._ctx.run(
            lambda t: t.upload_configuration(workspace_id=workspace_id, data=data),
            Configuration._from_payload,
        )

    @overload
    def get(self: Configurations[Sync], *, version: int) -> Configuration[Sync]: ...

    @overload
    def get(
        self: Configurations[Async], *, version: int
    ) -> Awaitable[Configuration[Async]]: ...

    def get(
        self, *, version: int
    ) -> Configuration[Any] | Awaitable[Configuration[Any]]:
        """Return one configuration by version.

        Args:
            version: The version to read, counting up from 1.

        Returns:
            The configuration; awaitable in async mode.

        Raises:
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            NotFound: The workspace has no such version.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()

        def parse(
            ctx: _Ctx[Any], payload: ListPageConfigurationResponse
        ) -> Configuration[Any]:
            if not payload.items:
                raise NotFound(EntityKind.CONFIGURATION, str(version))
            return Configuration._from_payload(ctx, payload.items[0])

        return self._ctx.run(
            lambda t: t.list_configurations(
                workspace_id=workspace_id, limit=1, offset=0, version=version
            ),
            parse,
        )

    @overload
    def latest(self: Configurations[Sync]) -> Configuration[Sync]: ...

    @overload
    def latest(self: Configurations[Async]) -> Awaitable[Configuration[Async]]: ...

    def latest(self) -> Configuration[Any] | Awaitable[Configuration[Any]]:
        """Return the configuration a run would use now.

        Returns:
            The newest version; awaitable in async mode.

        Raises:
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            NotFound: The workspace has none yet.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        return self._ctx.run(
            lambda t: t.get_configuration_latest(workspace_id=workspace_id),
            Configuration._from_payload,
        )

    @overload
    def count(self: Configurations[Sync]) -> int: ...

    @overload
    def count(self: Configurations[Async]) -> Awaitable[int]: ...

    def count(self) -> int | Awaitable[int]:
        """Return how many versions the workspace holds.

        Returns:
            The count; awaitable in async mode. Saturates at 10,001.

        Raises:
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            ScopeMissing: Reached without a workspace in scope.
        """
        return self._ctx.count(self._listing())

    @overload
    def list(
        self: Configurations[Sync], *, limit: int | None = None, offset: int = 0
    ) -> Iterable[Configuration[Sync]]: ...

    @overload
    def list(
        self: Configurations[Async], *, limit: int | None = None, offset: int = 0
    ) -> AsyncIterable[Configuration[Async]]: ...

    def list(
        self, *, limit: int | None = None, offset: int = 0
    ) -> Iterable[Configuration[Any]] | AsyncIterable[Configuration[Any]]:
        """Yield the workspace's configurations, paging lazily.

        Args:
            limit: Return at most this many. ``None`` walks to the end, or
                to row 10,100, past which the platform does not page.
            offset: Skip this many, server-side.

        Returns:
            An iterable of configurations; async-iterable in async mode.

        Raises:
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            ScopeMissing: Reached without a workspace in scope.
            ValueError: A negative ``limit`` or ``offset``.
        """
        return self._ctx.page(
            self._listing(), Configuration._from_payload, limit=limit, offset=offset
        )
