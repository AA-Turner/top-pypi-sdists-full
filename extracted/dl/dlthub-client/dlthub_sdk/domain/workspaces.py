"""Workspaces."""

from __future__ import annotations

# Python internals
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


@dataclass(frozen=True)
class WorkspaceMember:
    """One person with access to a workspace.

    Attributes:
        email: Their email, which is how the platform identifies a person.
        user_id: Their user uuid.
        role: What they may do in this workspace.
        name: Display name, or ``None`` when the identity provider supplied
            none.
    """

    email: str
    user_id: str
    role: str
    name: str | None

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
    """Who the token belongs to, and what they may do in one workspace.

    Attributes:
        email: The caller's email.
        user_id: The caller's user uuid.
        identity_id: The caller's member uuid in the owning organization.
        organization_id: The owning organization's uuid.
        organization_role: The caller's role in that organization.
        role: The caller's role in this workspace.
    """

    email: str
    user_id: str
    identity_id: str
    organization_id: str
    organization_role: str
    role: str

    @staticmethod
    def _from_payload(_ctx: _Ctx[Any], payload: WorkspaceMeResponse) -> WorkspaceCaller:
        return WorkspaceCaller(
            email=payload.email,
            user_id=str(payload.user_id),
            identity_id=str(payload.organization_identity_id),
            organization_id=str(payload.organization.id),
            organization_role=payload.organization_role,
            role=payload.workspace_role,
        )


@dataclass(frozen=True, repr=False)
class Workspace(Entity[M]):
    """A workspace: the unit a job is deployed into.

    Attributes:
        id: The workspace's uuid.
        name: Workspace name, which need not be unique.
        description: Free-text description, or ``None``.
        organization_id: Owning organization's uuid.
        dataplane_id: Data plane the workspace is assigned to.
        playground: Whether this is the caller's auto-created personal
            workspace. A playground is single-member and cannot be renamed.
        predefined_profiles: Profile names the platform offers for this workspace,
            keyed by access level. Empty when it declares none.
        created_at: When the workspace was created.
    """

    id: str
    name: str
    description: str | None
    organization_id: str
    dataplane_id: str
    playground: bool
    predefined_profiles: Mapping[str, str]
    created_at: datetime

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
            BadRequest: The workspace is a playground (see :attr:`playground`),
                which cannot be updated.
            NotAuthorized: The caller may not manage this workspace.
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
            limit: Return at most this many. ``None`` walks to the end.
            offset: Skip this many, server-side.

        Returns:
            An iterable of members; async-iterable in async mode.

        Raises:
            NotAuthorized: The caller may not list this workspace's members.
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

        One call, and it answers for an API key as well as a user token.

        Returns:
            The caller's identity and roles; awaitable in async mode.

        Raises:
            NotAuthorized: The caller has no access to this workspace.
            NotFound: The workspace no longer exists.
        """
        workspace_id = self.id
        return self._ctx.run(
            lambda t: t.workspace_me(workspace_id=workspace_id),
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
                dataplane_url=payload.dataplane_url,
            ),
            Workspace(
                id=workspace_id,
                name=payload.name,
                description=payload.description,
                organization_id=str(payload.organization_id),
                dataplane_id=payload.dataplane_id,
                playground=bool(payload.is_playground),
                predefined_profiles=dict(
                    getattr(payload.predefined_profiles, "additional_properties", {})
                    or {}
                ),
                created_at=payload.date_added,
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
            BadRequest: The organization has no data plane set yet, so it cannot
                hold workspaces (set one with ``Organization.set_dataplane``), or
                the organization in scope is not a uuid.
            NotAuthorized: The caller may not create workspaces here.
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
            BadRequest: ``id`` is not a uuid.
            NotFound: No such workspace, or it is not visible to this caller.
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
        """Return how many workspaces the organization has, without fetching them.

        Args:
            organization_id: Overrides the organization in scope. Required when
                the context carries none.

        Returns:
            The workspace count; awaitable in async mode. Saturates at 10,001.

        Raises:
            BadRequest: The organization in scope is not a uuid.
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

        Args:
            organization_id: Overrides the organization in scope. Required when
                the context carries none.
            limit: Return at most this many workspaces. ``None`` walks to the end.
            offset: Skip this many workspaces, server-side.

        Returns:
            An iterable of workspaces; async-iterable in async mode.

        Raises:
            BadRequest: The organization in scope is not a uuid.
            ScopeMissing: No organization in scope and none passed.
            ValueError: A negative ``limit`` or ``offset``.
        """
        return self._ctx.page(
            self._listing(organization_id),
            Workspace._from_payload,
            limit=limit,
            offset=offset,
        )
