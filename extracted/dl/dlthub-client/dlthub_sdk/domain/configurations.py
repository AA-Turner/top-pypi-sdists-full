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

if TYPE_CHECKING:
    # Typing only: domain never imports _gen at runtime.
    # Current package
    from dlthub_sdk._gen.api.models import ConfigurationResponse
    from dlthub_sdk._gen.dataplane_api.models import (
        ConfigurationResponse as DataplaneConfigurationResponse,
    )

    #: The upload answers with the data plane's own copy of the class.
    ConfigurationPayload = ConfigurationResponse | DataplaneConfigurationResponse


@dataclass(frozen=True, repr=False)
class Configuration(Entity[M]):
    """One uploaded version of a workspace's configuration.

    Attributes:
        version: Which version this is, counting up from 1 per workspace.
        id: Its uuid.
        content_hash: Hash of the uploaded content, so an unchanged upload is
            recognisable.
        file_count: How many files it holds.
        size: Total size in bytes.
        profiles: The profiles the configuration files define.
        created_at: When it was uploaded.
        created_by: Who uploaded it.
        updated_at: When it last changed.
    """

    version: int
    id: str
    content_hash: str
    file_count: int
    size: int
    profiles: tuple[str, ...]
    created_at: datetime
    created_by: str
    updated_at: datetime

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
                size=payload.size,
                # The platform sends one comma-separated string.
                profiles=tuple(
                    stripped
                    for p in payload.profiles.split(",")
                    if (stripped := p.strip())
                ),
                created_at=payload.date_added,
                created_by=str(payload.created_by),
                updated_at=payload.date_updated,
            ),
        )


class Configurations(Collection[M]):
    """The configurations of one workspace, newest version last."""

    _entity = Configuration

    def _listing(self) -> Listing[ConfigurationResponse]:
        workspace_id = self._ctx.require_workspace()
        return lambda t, limit, offset: t.list_configurations(
            workspace_id=workspace_id, limit=limit, offset=offset
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

        The archive is opaque here, as for :meth:`Deployments.upload`; the
        platform reads it for the hash, the file list and the profile names.

        Args:
            data: A gzipped tar of the configuration files, as bytes or a
                binary file object to stream from.

        Returns:
            The stored configuration, one version above the last; awaitable in
            async mode.

        Raises:
            Conflict: The workspace cannot take a configuration right now.
            InvalidResponse: The platform authorised an upload the SDK could
                not address.
            NotAuthorized: The caller may not write this workspace's
                configuration.
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
            NotFound: The workspace has no such version.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        return self._ctx.run(
            lambda t: t.get_configuration(workspace_id=workspace_id, version=version),
            Configuration._from_payload,
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
            NotFound: The workspace has none yet.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        return self._ctx.run(
            lambda t: t.get_latest_configuration(workspace_id=workspace_id),
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
            limit: Return at most this many. ``None`` walks to the end.
            offset: Skip this many, server-side.

        Returns:
            An iterable of configurations; async-iterable in async mode.

        Raises:
            ScopeMissing: Reached without a workspace in scope.
            ValueError: A negative ``limit`` or ``offset``.
        """
        return self._ctx.page(
            self._listing(), Configuration._from_payload, limit=limit, offset=offset
        )
