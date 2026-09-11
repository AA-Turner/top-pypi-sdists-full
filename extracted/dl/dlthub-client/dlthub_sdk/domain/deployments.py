"""Deployments — the versioned code a workspace runs."""

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
    from dlthub_sdk._gen.api.models import DeploymentResponse
    from dlthub_sdk._gen.dataplane_api.models import (
        DeploymentResponse as DataplaneDeploymentResponse,
    )

    #: The upload answers with the data plane's own copy of the class.
    DeploymentPayload = DeploymentResponse | DataplaneDeploymentResponse


@dataclass(frozen=True, repr=False)
class Deployment(Entity[M]):
    """One uploaded version of a workspace's code.

    Attributes:
        version: Which version this is, counting up from 1 per workspace.
        id: Its uuid.
        content_hash: Hash of the uploaded content, so an unchanged upload is
            recognisable.
        file_count: How many files it holds.
        size: Total size in bytes.
        requirements_size: Size of the requirements manifest in bytes.
        created_at: When it was uploaded.
        created_by: Who uploaded it.
        updated_at: When it last changed.
    """

    version: int
    id: str
    content_hash: str
    file_count: int
    size: int
    requirements_size: int
    created_at: datetime
    created_by: str
    updated_at: datetime

    _identity = ("version", "id")
    _kind = EntityKind.DEPLOYMENT

    @overload
    def files(self: Deployment[Sync]) -> tuple[FileEntry, ...]: ...

    @overload
    def files(self: Deployment[Async]) -> Awaitable[tuple[FileEntry, ...]]: ...

    def files(self) -> tuple[FileEntry, ...] | Awaitable[tuple[FileEntry, ...]]:
        """List the files this deployment holds.

        The manifest is stored with the content rather than with the record,
        so this is a fresh read every time.

        Returns:
            One entry per file, in the platform's order; awaitable in async mode.

        Raises:
            NotFound: The deployment no longer exists.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()
        deployment_id = self.id
        return self._ctx.run(
            lambda t: t.get_deployment_files(
                workspace_id=workspace_id,
                dataplane_url=dataplane_url,
                deployment_id=deployment_id,
            ),
            FileEntry._all_from_payload,
        )

    @staticmethod
    def _from_payload(ctx: _Ctx[Any], payload: DeploymentPayload) -> Deployment[Any]:
        return Deployment._bind(
            ctx,
            Deployment(
                version=payload.version,
                id=str(payload.id),
                content_hash=payload.content_hash,
                file_count=payload.file_count,
                size=payload.size,
                requirements_size=payload.requirements_size,
                created_at=payload.date_added,
                created_by=str(payload.created_by),
                updated_at=payload.date_updated,
            ),
        )


class Deployments(Collection[M]):
    """The deployments of one workspace, newest version last."""

    _entity = Deployment

    def _listing(self) -> Listing[DeploymentResponse]:
        workspace_id = self._ctx.require_workspace()
        return lambda t, limit, offset: t.list_deployments(
            workspace_id=workspace_id, limit=limit, offset=offset
        )

    @overload
    def upload(
        self: Deployments[Sync],
        *,
        code: bytes | BinaryIO,
        requirements: bytes | BinaryIO,
    ) -> Deployment[Sync]: ...

    @overload
    def upload(
        self: Deployments[Async],
        *,
        code: bytes | BinaryIO,
        requirements: bytes | BinaryIO,
    ) -> Awaitable[Deployment[Async]]: ...

    def upload(
        self, *, code: bytes | BinaryIO, requirements: bytes | BinaryIO
    ) -> Deployment[Any] | Awaitable[Deployment[Any]]:
        """Store a new version of the workspace's code.

        The archive is opaque here: building it is the caller's job, and the
        platform derives the hash, the size and the file list by reading it. To
        skip an unchanged upload, compare your own hash against
        :attr:`Deployment.content_hash` on ``latest()`` first.

        Args:
            code: A gzipped tar of the workspace, as bytes or a binary file
                object to stream from.
            requirements: The requirements manifest that goes with it, as bytes
                or a binary file object. Opaque to the SDK.

        Returns:
            The stored deployment, one version above the last; awaitable in
            async mode.

        Raises:
            Conflict: The workspace cannot take a deployment right now.
            InvalidResponse: The platform authorised an upload the SDK could
                not address.
            NotAuthorized: The caller may not deploy to this workspace.
            ScopeMissing: Reached without a workspace in scope.
            TransportError: The upload did not complete. A version is written
                only once the content arrives, but a request that never
                produced a response cannot say whether it did — read
                ``latest()`` before retrying.
        """
        workspace_id = self._ctx.require_workspace()
        return self._ctx.run(
            lambda t: t.upload_deployment(
                workspace_id=workspace_id, code=code, requirements=requirements
            ),
            Deployment._from_payload,
        )

    @overload
    def get(self: Deployments[Sync], *, version: int) -> Deployment[Sync]: ...

    @overload
    def get(
        self: Deployments[Async], *, version: int
    ) -> Awaitable[Deployment[Async]]: ...

    def get(self, *, version: int) -> Deployment[Any] | Awaitable[Deployment[Any]]:
        """Return one deployment by version.

        Args:
            version: The version to read, counting up from 1.

        Returns:
            The deployment; awaitable in async mode.

        Raises:
            NotFound: The workspace has no such version.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        return self._ctx.run(
            lambda t: t.get_deployment(workspace_id=workspace_id, version=version),
            Deployment._from_payload,
        )

    @overload
    def latest(self: Deployments[Sync]) -> Deployment[Sync]: ...

    @overload
    def latest(self: Deployments[Async]) -> Awaitable[Deployment[Async]]: ...

    def latest(self) -> Deployment[Any] | Awaitable[Deployment[Any]]:
        """Return the deployment a run would use now.

        Returns:
            The newest version; awaitable in async mode.

        Raises:
            NotFound: The workspace has none yet.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        return self._ctx.run(
            lambda t: t.get_latest_deployment(workspace_id=workspace_id),
            Deployment._from_payload,
        )

    @overload
    def count(self: Deployments[Sync]) -> int: ...

    @overload
    def count(self: Deployments[Async]) -> Awaitable[int]: ...

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
        self: Deployments[Sync], *, limit: int | None = None, offset: int = 0
    ) -> Iterable[Deployment[Sync]]: ...

    @overload
    def list(
        self: Deployments[Async], *, limit: int | None = None, offset: int = 0
    ) -> AsyncIterable[Deployment[Async]]: ...

    def list(
        self, *, limit: int | None = None, offset: int = 0
    ) -> Iterable[Deployment[Any]] | AsyncIterable[Deployment[Any]]:
        """Yield the workspace's deployments, paging lazily.

        Args:
            limit: Return at most this many. ``None`` walks to the end.
            offset: Skip this many, server-side.

        Returns:
            An iterable of deployments; async-iterable in async mode.

        Raises:
            ScopeMissing: Reached without a workspace in scope.
            ValueError: A negative ``limit`` or ``offset``.
        """
        return self._ctx.page(
            self._listing(), Deployment._from_payload, limit=limit, offset=offset
        )
