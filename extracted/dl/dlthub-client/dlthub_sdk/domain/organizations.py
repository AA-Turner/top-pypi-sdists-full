"""Organizations — the tenant a workspace belongs to."""

from __future__ import annotations

# Python internals
from dataclasses import dataclass
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterable,
    Awaitable,
    Generic,
    Iterable,
    overload,
)

# Current package
from dlthub_sdk._glue.base import Collection, Entity
from dlthub_sdk._glue.context import Async, Listing, M, Sync, _Ctx
from dlthub_sdk._glue.enums import EntityKind
from dlthub_sdk.domain.workspaces import Workspace, Workspaces

if TYPE_CHECKING:
    # Typing only: domain never imports _gen at runtime.
    # Current package
    from dlthub_sdk._gen.api.models import OrganizationMeResponse, OrganizationResponse


@dataclass(frozen=True)
class Membership(Generic[M]):
    """A workspace the caller belongs to, and their role in it.

    Attributes:
        workspace: The workspace, bound and ready to navigate from.
        role: The caller's role in it.
    """

    workspace: Workspace[M]
    role: str


@dataclass(frozen=True)
class OrganizationCaller(Generic[M]):
    """Who the token belongs to, and what they may do in one organization.

    Attributes:
        email: The caller's email.
        user_id: The caller's user uuid.
        identity_id: The caller's member uuid in this organization.
        role: The caller's role in this organization.
        memberships: The organization's workspaces the caller belongs to.
    """

    email: str
    user_id: str
    identity_id: str
    role: str
    memberships: tuple[Membership[M], ...]

    @staticmethod
    def _from_payload(
        ctx: _Ctx[Any], payload: OrganizationMeResponse
    ) -> OrganizationCaller[Any]:
        return OrganizationCaller(
            email=payload.email,
            user_id=str(payload.user_id),
            identity_id=str(payload.identity_id),
            role=payload.role,
            memberships=tuple(
                Membership(
                    workspace=Workspace._from_payload(ctx, m.workspace), role=m.role
                )
                for m in (
                    payload.workspaces if isinstance(payload.workspaces, list) else ()
                )
            ),
        )


@dataclass(frozen=True, repr=False)
class Organization(Entity[M]):
    """An organization: what workspaces, members and billing hang off.

    Attributes:
        id: The organization's uuid.
        name: Organization name.
        description: Free-text description, or ``None``.
        dataplane_id: Default data plane for new workspaces, when one is set.
        created_at: When the organization was created.
    """

    id: str
    name: str
    description: str | None
    dataplane_id: str | None
    created_at: datetime

    _identity = ("id", "name")
    _kind = EntityKind.ORGANIZATION

    @overload
    def set_dataplane(
        self: Organization[Sync], *, dataplane_id: str
    ) -> Organization[Sync]: ...

    @overload
    def set_dataplane(
        self: Organization[Async], *, dataplane_id: str
    ) -> Awaitable[Organization[Async]]: ...

    def set_dataplane(
        self, *, dataplane_id: str
    ) -> Organization[Any] | Awaitable[Organization[Any]]:
        """Choose the data plane this organization's workspaces live on.

        Must be set before the organization can hold any workspace, and it
        fixes where that data resides.

        Args:
            dataplane_id: The data plane to assign.

        Returns:
            A fresh snapshot; awaitable in async mode.

        Raises:
            BadRequest: No such data plane, or the organization already has one.
            NotAuthorized: The caller may not administer this organization.
        """
        organization_id = self.id
        return self._ctx.run(
            lambda t: t.set_organization_region(
                organization_id=organization_id, dataplane_id=dataplane_id
            ),
            Organization._from_payload,
        )

    @overload
    def me(self: Organization[Sync]) -> OrganizationCaller[Sync]: ...

    @overload
    def me(self: Organization[Async]) -> Awaitable[OrganizationCaller[Async]]: ...

    def me(self) -> OrganizationCaller[Any] | Awaitable[OrganizationCaller[Any]]:
        """Who the caller is here, what they may do, and where they belong.

        One call, and it answers for an API key as well as a user token.

        Returns:
            The caller's identity, role, and workspace memberships in this
            organization; awaitable in async mode.

        Raises:
            NotAuthorized: The caller has no access to this organization.
            NotFound: The organization no longer exists.
        """
        organization_id = self.id
        return self._ctx.run(
            lambda t: t.organization_me(organization_id=organization_id),
            OrganizationCaller._from_payload,
        )

    @property
    def workspaces(self) -> Workspaces[M]:
        """The workspaces in this organization.

        Returns:
            A collection scoped to this organization, so ``list()`` needs no
            ``organization_id``.
        """
        return Workspaces(self._ctx)

    @staticmethod
    def _from_payload(
        ctx: _Ctx[Any], payload: OrganizationResponse
    ) -> Organization[Any]:
        organization_id = str(payload.id)
        return Organization._bind(
            ctx.narrow(organization_id=organization_id),
            Organization(
                id=organization_id,
                name=payload.name,
                description=payload.description,
                dataplane_id=payload.dataplane_id,
                created_at=payload.date_added,
            ),
        )


class Organizations(Collection[M]):
    """The organizations the caller belongs to."""

    _entity = Organization

    def _listing(self) -> Listing[OrganizationResponse]:
        return lambda t, limit, offset: t.list_organizations(limit=limit, offset=offset)

    @overload
    def get(self: Organizations[Sync], *, id: str) -> Organization[Sync]: ...

    @overload
    def get(
        self: Organizations[Async], *, id: str
    ) -> Awaitable[Organization[Async]]: ...

    def get(self, *, id: str) -> Organization[Any] | Awaitable[Organization[Any]]:
        """Return one organization by id.

        Args:
            id: The organization uuid.

        Returns:
            The organization; awaitable in async mode.

        Raises:
            BadRequest: ``id`` is not a uuid.
            NotFound: No such organization, or it is not visible to this caller.
        """
        return self._ctx.run(
            lambda t: t.get_organization(organization_id=id),
            Organization._from_payload,
        )

    @overload
    def count(self: Organizations[Sync]) -> int: ...

    @overload
    def count(self: Organizations[Async]) -> Awaitable[int]: ...

    def count(self) -> int | Awaitable[int]:
        """Return how many organizations the caller belongs to.

        Returns:
            The organization count; awaitable in async mode. Saturates at 10,001.
        """
        return self._ctx.count(self._listing())

    @overload
    def list(
        self: Organizations[Sync], *, limit: int | None = None, offset: int = 0
    ) -> Iterable[Organization[Sync]]: ...

    @overload
    def list(
        self: Organizations[Async], *, limit: int | None = None, offset: int = 0
    ) -> AsyncIterable[Organization[Async]]: ...

    def list(
        self, *, limit: int | None = None, offset: int = 0
    ) -> Iterable[Organization[Any]] | AsyncIterable[Organization[Any]]:
        """Yield the organizations the caller belongs to, paging lazily.

        Needs no scope, so this is the entry point when the caller knows no ids
        yet.

        Args:
            limit: Return at most this many. ``None`` walks to the end.
            offset: Skip this many, server-side.

        Returns:
            An iterable of organizations; async-iterable in async mode.

        Raises:
            ValueError: A negative ``limit`` or ``offset``.
        """
        return self._ctx.page(
            self._listing(), Organization._from_payload, limit=limit, offset=offset
        )
