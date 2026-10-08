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
    """An organization the caller belongs to, and their role in it.

    Attributes:
        organization: The organization, bound and ready to navigate from.
        role: The caller's role in it.
        is_active: Whether the membership is currently active.
    """

    organization: Organization[M]
    role: str
    is_active: bool


@dataclass(frozen=True)
class Caller(Generic[M]):
    """The human the token belongs to.

    Only a user token reaches this: the platform gates ``/me`` to human
    principals, so an API key gets :class:`~dlthub_sdk.NotAuthorized` instead —
    see :meth:`~dlthub_sdk.Runtime.me`. Every other caller identity in the SDK
    is scoped, and answers for any principal: :meth:`Organization.me` and
    :meth:`Workspace.me`.

    Attributes:
        email: The caller's email.
        user_id: The caller's user uuid.
        organization_membership_id: Their member uuid in the organization the platform
            considers current.
        name: Display name, when the identity provider supplied one.
        primary_organization: Where new workspaces are created by default.
        latest_organization: The organization they most recently worked in.
        organization_memberships: Every organization they belong to.
    """

    email: str
    user_id: str
    organization_membership_id: str
    name: str | None
    primary_organization: Organization[M]
    latest_organization: Organization[M]
    organization_memberships: tuple[OrganizationMembership[M], ...]

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
