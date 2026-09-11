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
    from dlthub_sdk._gen.api.models import CurrentUserResponse


@dataclass(frozen=True)
class OrganizationMembership(Generic[M]):
    """An organization the caller belongs to, and their role in it.

    Attributes:
        organization: The organization, bound and ready to navigate from.
        role: The caller's role in it.
        active: Whether the membership is currently active.
    """

    organization: Organization[M]
    role: str
    active: bool


@dataclass(frozen=True)
class Caller(Generic[M]):
    """The human the token belongs to.

    Only a user token reaches this: the platform gates ``/user`` to human
    principals, so an API key gets :class:`~dlthub_sdk.NotAuthorized` instead —
    see :meth:`~dlthub_sdk.Runtime.me`. Every other caller identity in the SDK
    is scoped, and answers for any principal: :meth:`Organization.me` and
    :meth:`Workspace.me`.

    Attributes:
        email: The caller's email.
        user_id: The caller's user uuid.
        identity_id: Their member uuid in the organization the platform
            considers current.
        name: Display name, when the identity provider supplied one.
        primary_organization: Where new workspaces are created by default.
        last_organization: The organization they most recently worked in.
        memberships: Every organization they belong to.
    """

    email: str
    user_id: str
    identity_id: str
    name: str | None
    primary_organization: Organization[M]
    last_organization: Organization[M]
    memberships: tuple[OrganizationMembership[M], ...]

    @staticmethod
    def _from_payload(ctx: _Ctx[Any], payload: CurrentUserResponse) -> Caller[Any]:
        return Caller(
            email=payload.email,
            user_id=str(payload.user_id),
            identity_id=str(payload.identity_id),
            name=payload.name if isinstance(payload.name, str) else None,
            primary_organization=Organization._from_payload(
                ctx, payload.primary_organization
            ),
            last_organization=Organization._from_payload(
                ctx, payload.last_organization
            ),
            memberships=tuple(
                OrganizationMembership(
                    organization=Organization._from_payload(ctx, m.organization),
                    role=m.role,
                    active=m.active,
                )
                for m in (
                    payload.organizations
                    if isinstance(payload.organizations, list)
                    else ()
                )
            ),
        )
