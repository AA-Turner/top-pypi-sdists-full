"""Who the token belongs to, across every organization they are in."""

from __future__ import annotations

# Python internals
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic

# Current package
from dlthub_sdk._glue.context import M, _Ctx
from dlthub_sdk.domain.organizations import Organization

if TYPE_CHECKING:
    # Typing only: domain never imports _gen at runtime.
    # Current package
    from dlthub_sdk._gen.api.models import MeResponse


@dataclass(frozen=True)
class OrganizationMembership(Generic[M]):
    """An organization the caller belongs to, and their role in it."""

    # doc: sdk
    organization: Organization[M]
    """The organization, bound and ready to navigate from."""
    role: str
    """The role of the user in the organization."""
    is_active: bool
    """Whether the membership is active."""


@dataclass(frozen=True)
class Caller(Generic[M]):
    """The person the token belongs to.

    Returned for a user token or a user API key; a service-account API key gets
    :class:`~dlthub_sdk.NotAuthorized` instead (see :meth:`~dlthub_sdk.Runtime.me`).
    :meth:`Organization.me` and :meth:`Workspace.me` answer for any caller.
    """

    email: str
    """The email of the current user."""
    user_id: str
    """The ID of the current user."""
    organization_membership_id: str
    """Your membership id in `latest_organization`."""
    name: str | None
    """The user's display name (full name); `None` if the identity provider supplied
    none.
    """
    primary_organization: Organization[M]
    """The organization where new workspaces are created by default."""
    latest_organization: Organization[M]
    """The organization you used most recently."""
    organization_memberships: tuple[OrganizationMembership[M], ...]
    """Every organization they belong to."""

    @staticmethod
    def _from_payload(ctx: _Ctx[Any], payload: MeResponse) -> Caller[Any]:
        return Caller(
            email=payload.email,
            user_id=str(payload.user_id),
            organization_membership_id=str(payload.organization_membership_id),
            name=payload.name if isinstance(payload.name, str) else None,
            primary_organization=Organization._from_payload(
                ctx, payload.primary_organization
            ),
            latest_organization=Organization._from_payload(
                ctx, payload.latest_organization
            ),
            organization_memberships=tuple(
                OrganizationMembership(
                    organization=Organization._from_payload(ctx, m.organization),
                    role=m.role,
                    is_active=m.is_active,
                )
                for m in (
                    payload.organization_memberships
                    if isinstance(payload.organization_memberships, list)
                    else ()
                )
            ),
        )
