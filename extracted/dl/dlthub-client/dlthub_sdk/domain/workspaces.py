"""Workspaces."""

from __future__ import annotations

# Python internals
import os
from dataclasses import dataclass
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterable,
    Awaitable,
    Iterable,
    Mapping,
    overload,
)

# Current package
from dlthub_sdk._glue.base import Collection, Entity
from dlthub_sdk._glue.context import Async, Listing, M, Sync, _Ctx
from dlthub_sdk._glue.enums import EntityKind
from dlthub_sdk._glue.keep import KEEP, Keep
from dlthub_sdk._glue.urls import segment, web_ui_base
from dlthub_sdk.domain.configurations import Configurations
from dlthub_sdk.domain.deployments import Deployments
from dlthub_sdk.domain.job_runs import JobRuns
from dlthub_sdk.domain.jobs import Jobs
from dlthub_sdk.domain.telemetry import Telemetry
from dlthub_sdk.domain.variables import Variables

if TYPE_CHECKING:
    # Typing only: domain never imports _gen at runtime.
    # Current package
    from dlthub_sdk._gen.api.models import (
        OrganizationWorkspaceResponse,
        WorkspaceMemberResponse,
        WorkspaceMeResponse,
        WorkspaceResponse,
    )

    #: get returns the plain model, list the organization-scoped one.
    WorkspacePayload = WorkspaceResponse | OrganizationWorkspaceResponse


def _injected_dataplane_url() -> str | None:
    """The plane URL the runtime injected, if this process is a platform run.

    A run on an external provider cannot resolve the plane's public subdomain,
    so the runtime tells it where the plane is and that outranks the address the
    API reports.

    Returns:
        The injected plane URL, or ``None`` outside a platform run.
    """
    return os.environ.get("RUNTIME__DATAPLANE_BASE_URL") or None


@dataclass(frozen=True)
class WorkspaceMember:
    """One member of a workspace: a person or a service account (workspace API key)."""

    email: str
    """The email of the user."""
    user_id: str
    """The ID of the user."""
    role: str
    """The role of the user in the workspace."""
    name: str | None
    """Display name; `None` when the user has no name set."""

    @staticmethod
    def _from_payload(
        _ctx: _Ctx[Any], payload: WorkspaceMemberResponse
    ) -> WorkspaceMember:
        return WorkspaceMember(
            email=payload.email,
            user_id=str(payload.user_id),
            role=payload.role,
            name=payload.name if isinstance(payload.name, str) else None,
        )


@dataclass(frozen=True)
class WorkspaceCaller:
    """Who the token belongs to, and what they may do in one workspace."""

    email: str
    """The email of the current user."""
    user_id: str
    """The ID of the current user."""
    organization_membership_id: str
    """The ID of the organization member in the parent organization."""
    organization_id: str
    """Unique ID (a UUID)."""
    organization_role: str
    """The role of the user in the parent organization."""
    workspace_role: str
    """The role of the user in this workspace."""

    @staticmethod
    def _from_payload(_ctx: _Ctx[Any], payload: WorkspaceMeResponse) -> WorkspaceCaller:
        return WorkspaceCaller(
            email=payload.email,
            user_id=str(payload.user_id),
            organization_membership_id=str(payload.organization_membership_id),
            organization_id=str(payload.organization.id),
            organization_role=payload.organization_role,
            workspace_role=payload.workspace_role,
        )


@dataclass(frozen=True, repr=False)
class Workspace(Entity[M]):
    """A workspace: the unit a job is deployed into."""

    id: str
    """Unique ID (a UUID)."""
    name: str
    """The name of the workspace."""
    description: str | None
    """Free-text description of the workspace; `None` when none is set."""
    organization_id: str
    """The ID of the parent organization."""
    dataplane_id: str
    """Identifier of the data plane that holds this workspace's user data. Matches the
    subdomain of the plane's public entrypoint.
    """
    is_playground: bool
    """Whether this is the user's auto-created personal playground workspace. A
    playground has a single member and cannot be updated, archived, shared, or given
    API keys.
    """
    predefined_profiles: Mapping[str, str]
    """Profile names the platform offers for this workspace, keyed by access level.
    Empty when it declares none.
    """
    created_at: datetime
    """When it was created."""
    archived_at: datetime | None
    """When the workspace was archived; `None` when live. An archived workspace rejects
    all changes except unarchiving, though owners can still manage its workspace
    variables.
    """

    _identity = ("id", "name")
    _kind = EntityKind.WORKSPACE

    @overload
    def update(
        self: Workspace[Sync],
        *,
        name: str | Keep = KEEP,
        description: str | None | Keep = KEEP,
    ) -> Workspace[Sync]: ...

    @overload
    def update(
        self: Workspace[Async],
        *,
        name: str | Keep = KEEP,
        description: str | None | Keep = KEEP,
    ) -> Awaitable[Workspace[Async]]: ...

    def update(
        self, *, name: str | Keep = KEEP, description: str | None | Keep = KEEP
    ) -> Workspace[Any] | Awaitable[Workspace[Any]]:
        """Change the workspace's name, its description, or both.

        Args:
            name: New name. Omit to leave it unchanged.
            description: New description. Pass ``None`` to clear it, omit to
                leave it unchanged.

        Returns:
            A fresh snapshot; awaitable in async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            Conflict: The current state does not allow the call, e.g. the workspace is
                archived; `code` and `message` say why.
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            NotFound: The workspace no longer exists.
        """
        workspace_id = self.id
        return self._ctx.run(
            lambda t: t.update_workspace(
                workspace_id=workspace_id, name=name, description=description
            ),
            Workspace._from_payload,
        )

    @overload
    def archive(self: Workspace[Sync]) -> Workspace[Sync]: ...

    @overload
    def archive(self: Workspace[Async]) -> Awaitable[Workspace[Async]]: ...

    def archive(self) -> Workspace[Any] | Awaitable[Workspace[Any]]:
        """Freeze the workspace: its schedules stop and it refuses changes.

        Returns:
            A fresh snapshot with ``archived_at`` set; awaitable in async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            Conflict: The current state does not allow the call, e.g. the workspace is
                archived; `code` and `message` say why.
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            NotFound: The workspace no longer exists.
        """
        workspace_id = self.id
        return self._ctx.run(
            lambda t: t.archive_workspace(workspace_id=workspace_id),
            Workspace._from_payload,
        )

    @overload
    def unarchive(self: Workspace[Sync]) -> Workspace[Sync]: ...

    @overload
    def unarchive(self: Workspace[Async]) -> Awaitable[Workspace[Async]]: ...

    def unarchive(self) -> Workspace[Any] | Awaitable[Workspace[Any]]:
        """Reopen an archived workspace and restart its schedules.

        Returns:
            A fresh snapshot with ``archived_at`` cleared; awaitable in async mode.

        Raises:
            Conflict: The current state does not allow the call, e.g. the workspace is
                archived; `code` and `message` say why.
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            NotFound: The workspace no longer exists.
        """
        workspace_id = self.id
        return self._ctx.run(
            lambda t: t.unarchive_workspace(workspace_id=workspace_id),
            Workspace._from_payload,
        )

    @overload
    def members(
        self: Workspace[Sync], *, limit: int | None = None, offset: int = 0
    ) -> Iterable[WorkspaceMember]: ...

    @overload
    def members(
        self: Workspace[Async], *, limit: int | None = None, offset: int = 0
    ) -> AsyncIterable[WorkspaceMember]: ...

    def members(
        self, *, limit: int | None = None, offset: int = 0
    ) -> Iterable[WorkspaceMember] | AsyncIterable[WorkspaceMember]:
        """Who has access to this workspace, and in what role.

        Args:
            limit: Return at most this many. ``None`` walks to the end, or
                to row 10,100, past which the platform does not page.
            offset: Skip this many, server-side.

        Returns:
            An iterable of members; async-iterable in async mode.

        Raises:
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            ValueError: A negative ``limit`` or ``offset``.
        """
        workspace_id = self.id

        def listing(t: Any, page: int, skip: int) -> Any:
            return t.list_workspace_members(
                workspace_id=workspace_id, limit=page, offset=skip
            )

        return self._ctx.page(
            listing, WorkspaceMember._from_payload, limit=limit, offset=offset
        )

    @overload
    def me(self: Workspace[Sync]) -> WorkspaceCaller: ...

    @overload
    def me(self: Workspace[Async]) -> Awaitable[WorkspaceCaller]: ...

    def me(self) -> WorkspaceCaller | Awaitable[WorkspaceCaller]:
        """Who the caller is here, and what they may do.

        One call, and it answers for an API key as well as a user token. Also
        records this workspace as the caller's most recent one, so
        :meth:`Runtime.me` then reports its organization as `latest_organization`.

        Returns:
            The caller's identity and roles; awaitable in async mode.

        Raises:
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            NotFound: The workspace no longer exists.
        """
        workspace_id = self.id
        return self._ctx.run(
            lambda t: t.get_workspace_me(workspace_id=workspace_id),
            WorkspaceCaller._from_payload,
        )

    @property
    def dashboard_url(self) -> str:
        """Where this workspace's dashboard lives in the web UI.

        Derived from the control-plane URL given at connect time, so it points
        at whichever environment this client talks to.

        Returns:
            An absolute URL.
        """
        return f"{web_ui_base(self._ctx.base_url)}/w/{segment(self.id)}"

    @property
    def job_runs(self) -> JobRuns[M]:
        """The job runs of this workspace, across all its jobs.

        Named in full because a workspace also has pipeline runs, reached
        through :attr:`telemetry`.

        Returns:
            A collection scoped to this workspace; narrow to one job with the
            ``job_id`` argument on its methods.
        """
        return JobRuns(self._ctx)

    @property
    def deployments(self) -> Deployments[M]:
        """The versions of code this workspace has been given.

        Returns:
            A collection scoped to this workspace.
        """
        return Deployments(self._ctx)

    @property
    def configurations(self) -> Configurations[M]:
        """The versions of configuration this workspace has been given.

        Returns:
            A collection scoped to this workspace.
        """
        return Configurations(self._ctx)

    @property
    def telemetry(self) -> Telemetry[M]:
        """What the platform observed of the pipelines this workspace ran.

        Returns:
            This workspace's telemetry, read from its data plane.
        """
        return Telemetry(self._ctx)

    @property
    def variables(self) -> Variables[M]:
        """The variables this workspace's job runs read.

        Returns:
            The variables of this workspace, in all their scopes.
        """
        return Variables(self._ctx)

    @property
    def jobs(self) -> Jobs[M]:
        """The jobs deployed in this workspace.

        Returns:
            A collection scoped to this workspace.
        """
        return Jobs(self._ctx)

    @staticmethod
    def _from_payload(ctx: _Ctx[Any], payload: WorkspacePayload) -> Workspace[Any]:
        workspace_id = str(payload.id)
        return Workspace._bind(
            ctx.narrow(
                workspace_id=workspace_id,
                organization_id=str(payload.organization_id),
                dataplane_url=_injected_dataplane_url() or payload.dataplane_url,
            ),
            Workspace(
                id=workspace_id,
                name=payload.name,
                description=payload.description,
                organization_id=str(payload.organization_id),
                dataplane_id=payload.dataplane_id,
                is_playground=bool(payload.is_playground),
                predefined_profiles=dict(
                    getattr(payload.predefined_profiles, "additional_properties", {})
                    or {}
                ),
                created_at=payload.created_at,
                archived_at=(
                    payload.archived_at
                    if isinstance(payload.archived_at, datetime)
                    else None
                ),
            ),
        )


class Workspaces(Collection[M]):
    """Workspace lookup, scoped by the context it is reached through."""

    _entity = Workspace

    def _listing(
        self, organization_id: str | None
    ) -> Listing[OrganizationWorkspaceResponse]:
        org_id = organization_id or self._ctx.require_organization()
        return lambda t, limit, offset: t.list_workspaces(
            organization_id=org_id, limit=limit, offset=offset
        )

    @overload
    def create(
        self: Workspaces[Sync],
        *,
        name: str,
        description: str | None = None,
        organization_id: str | None = None,
    ) -> Workspace[Sync]: ...

    @overload
    def create(
        self: Workspaces[Async],
        *,
        name: str,
        description: str | None = None,
        organization_id: str | None = None,
    ) -> Awaitable[Workspace[Async]]: ...

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
        organization_id: str | None = None,
    ) -> Workspace[Any] | Awaitable[Workspace[Any]]:
        """Create a workspace in an organization.

        Args:
            name: Name for the new workspace. Names need not be unique.
            description: Free-text description, or ``None`` for none.
            organization_id: Overrides the organization in scope. Required when
                the context carries none.

        Returns:
            The new workspace, scoped so its jobs are reachable; awaitable in
            async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            Conflict: The current state does not allow the call, e.g. the workspace is
                archived; `code` and `message` say why.
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            NotFound: No such organization.
            ScopeMissing: No organization in scope and none passed.
        """
        org_id = organization_id or self._ctx.require_organization()
        return self._ctx.run(
            lambda t: t.create_workspace(
                organization_id=org_id, name=name, description=description
            ),
            Workspace._from_payload,
        )

    @overload
    def get(self: Workspaces[Sync], *, id: str) -> Workspace[Sync]: ...

    @overload
    def get(self: Workspaces[Async], *, id: str) -> Awaitable[Workspace[Async]]: ...

    def get(self, *, id: str) -> Workspace[Any] | Awaitable[Workspace[Any]]:
        """Return one workspace by id.

        Args:
            id: The workspace uuid.

        Returns:
            The workspace; awaitable in async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            NotFound: No such workspace.
        """
        return self._ctx.run(
            lambda t: t.get_workspace(workspace_id=id), Workspace._from_payload
        )

    @overload
    def count(self: Workspaces[Sync], *, organization_id: str | None = None) -> int: ...

    @overload
    def count(
        self: Workspaces[Async], *, organization_id: str | None = None
    ) -> Awaitable[int]: ...

    def count(self, *, organization_id: str | None = None) -> int | Awaitable[int]:
        """Count the workspaces of one organization, without fetching them.

        Counts the live (unarchived) workspaces of the organization that the
        caller can see.

        Args:
            organization_id: Overrides the organization in scope. Required when
                the context carries none.

        Returns:
            The workspace count; awaitable in async mode. Saturates at 10,001.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            NotFound: No such organization.
            ScopeMissing: No organization in scope and none passed.
        """
        return self._ctx.count(self._listing(organization_id))

    @overload
    def list(
        self: Workspaces[Sync],
        *,
        organization_id: str | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> Iterable[Workspace[Sync]]: ...

    @overload
    def list(
        self: Workspaces[Async],
        *,
        organization_id: str | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> AsyncIterable[Workspace[Async]]: ...

    def list(
        self,
        *,
        organization_id: str | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> Iterable[Workspace[Any]] | AsyncIterable[Workspace[Any]]:
        """Yield the workspaces of one organization, paging lazily.

        Yields the live (unarchived) workspaces of the organization that the
        caller can see. Errors from the platform are raised when iteration
        begins.

        Args:
            organization_id: Overrides the organization in scope. Required when
                the context carries none.
            limit: Return at most this many workspaces. ``None`` walks to the end, or
                to row 10,100, past which the platform does not page.
            offset: Skip this many workspaces, server-side.

        Returns:
            An iterable of workspaces; async-iterable in async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            NotFound: No such organization.
            ScopeMissing: No organization in scope and none passed.
            ValueError: A negative `limit` or `offset`.
        """
        return self._ctx.page(
            self._listing(organization_id),
            Workspace._from_payload,
            limit=limit,
            offset=offset,
        )
