"""Organization invites (auth P3, PF-350).

An invite is a pending grant of org membership at a chosen role, sent to an
email address. On acceptance it becomes a real ``OrganizationMembership`` row
(with ``invited_by`` copied across — finally giving that vestigial column
meaning). The opaque ``token`` is hashed at rest (SHA-256); the raw value goes
only into the invite email's accept link.

Who can send an invite (§4): an org ADMIN/owner for their own org, OR any
platform user for any org (the ``is_org_admin`` short-circuit). Accepting makes
the invitee an **ordinary member** — never a platform user (that is operator-only).
"""

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, UniqueConstraint
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, Relationship

from src.domain._base import TimestampMixin
from src.domain.organization import OrganizationRole

if TYPE_CHECKING:
    from src.domain.organization import Organization

DEFAULT_INVITE_TTL_DAYS = 14


class InviteStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"


def generate_invite_token() -> str:
    """Raw opaque invite token; embedded in the accept link, hashed at rest."""
    return secrets.token_urlsafe(32)


def hash_invite_token(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()


class OrganizationInvite(TimestampMixin, table=True):
    """A pending invitation to join an organization."""

    __tablename__ = "organization_invites"

    id: str = Field(default_factory=lambda: secrets.token_urlsafe(16), primary_key=True)
    organization_id: str = Field(foreign_key="organizations.id", index=True)
    email: str = Field(index=True, max_length=255)  # invitee
    # Both enum columns are VARCHAR(20) in the database, not native Postgres
    # enums -- that is what the migration built. `native_enum=False` keeps the
    # Python-side coercion while storing a plain string, so adding a role or a
    # status needs no `ALTER TYPE`.
    role: OrganizationRole = Field(
        default=OrganizationRole.DEVELOPER,
        sa_column=Column(
            SAEnum(OrganizationRole, native_enum=False, length=20),
            nullable=False,
        ),
    )
    invited_by: str = Field(foreign_key="users.id")  # the inviter

    # Opaque token, hashed at rest; the raw value is in the accept link only.
    token_hash: str = Field(index=True, max_length=64)
    status: InviteStatus = Field(
        default=InviteStatus.PENDING,
        sa_column=Column(
            SAEnum(InviteStatus, native_enum=False, length=20),
            nullable=False,
        ),
    )

    # If Supabase created/emailed the invite (inviteUserByEmail), its auth id.
    supabase_invite_id: Optional[str] = Field(default=None, max_length=255)

    expires_at: datetime = Field(
        default_factory=lambda: (
            datetime.now(timezone.utc) + timedelta(days=DEFAULT_INVITE_TTL_DAYS)
        )
    )
    accepted_at: Optional[datetime] = Field(default=None)

    organization: Optional["Organization"] = Relationship()

    # One live invite per (org, email). Enforced at the app layer for a
    # partial-unique semantic (only while PENDING); the table constraint below
    # is a coarse guard that a full re-invite flow revokes-then-recreates around.
    __table_args__ = (
        UniqueConstraint(
            "organization_id", "email", "token_hash", name="uq_org_invite_token"
        ),
    )

    def is_expired(self) -> bool:
        exp = self.expires_at
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) > exp

    def is_acceptable(self) -> bool:
        return self.status == InviteStatus.PENDING and not self.is_expired()

    def mark_accepted(self) -> None:
        self.status = InviteStatus.ACCEPTED
        self.accepted_at = datetime.now(timezone.utc)
        self.touch()

    def revoke(self) -> None:
        self.status = InviteStatus.REVOKED
        self.touch()
