"""Requests to join the platform from someone who has no account yet.

Distinct from ``OrganizationInvite``, which is a *grant already made*: it carries
an ``organization_id`` and an ``invited_by``, because a member with authority
decided to let a specific person into a specific org. A signup request has
neither. Nobody has decided anything yet, and there is no org in the picture --
it is a stranger asking, and it becomes a ``User`` only when a platform member
approves it. Modelling it as an invite would mean inventing an org and an
inviter that do not exist.

Reaching this table at all requires the deployment's team secret, so this is a
queue of people who already had one credential, not an open front door. The
approval step is what turns "holds the team secret" into "has an account" --
deliberately, because the team secret is shared, static, and cannot be attributed
to a person.
"""

import secrets
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlalchemy import Column, DateTime, ForeignKey, Index, String, text
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field

from src.domain._base import TimestampMixin


class SignupRequestStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"


class SignupRequest(TimestampMixin, table=True):
    """One person asking for platform access, awaiting a decision.

    Every column below that the migration builds with something other than
    SQLModel's inferred default states an explicit ``sa_column``. The table was
    created by ``create_all`` before its migration ever ran anywhere, so the
    two were free to disagree in silence -- and did, in four columns, an index
    and two ``ON DELETE`` clauses. The migration is the intended shape
    (timezone-aware timestamps, the status stored as a plain ``VARCHAR`` like
    every other status column here); the declarations here are pinned to it, so
    ``alembic check`` is what catches the next divergence rather than a deploy.
    """

    __tablename__ = "signup_requests"

    # The dashboard's only query: everything still pending, oldest first.
    __table_args__ = (
        Index("ix_signup_requests_status_created", "status", "created_at"),
    )

    id: str = Field(default_factory=lambda: secrets.token_urlsafe(16), primary_key=True)

    # Not unique at the table level: a denied request should not permanently
    # bar the address, and someone who asks twice before anyone looks should not
    # get a 500. The route keeps at most one PENDING row per address instead.
    email: str = Field(index=True, max_length=255)
    full_name: str = Field(max_length=100)

    # Free text from the requester -- "I'm the new contractor on PF". The only
    # thing an approver has to go on beyond the address itself, so it is worth
    # storing even though nothing validates it.
    note: Optional[str] = Field(default=None, max_length=500)

    # Stored as a plain VARCHAR holding the enum's NAME, matching every other
    # status column here -- `native_enum=False` keeps the Python-side coercion
    # without creating a Postgres enum type. A native enum is what `create_all`
    # built and what then made the migration unrunnable.
    status: SignupRequestStatus = Field(
        default=SignupRequestStatus.PENDING,
        sa_column=Column(
            SAEnum(SignupRequestStatus, native_enum=False, length=20),
            nullable=False,
            server_default="PENDING",
        ),
    )

    # Who decided, and when. Null while PENDING. Kept after a decision so the
    # queue doubles as an audit trail of who let whom in.
    #
    # SET NULL, not CASCADE: deleting the admin who approved someone must not
    # delete the record that they were approved.
    decided_by: Optional[str] = Field(
        default=None,
        sa_column=Column(
            String(64), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
        ),
    )
    decided_at: Optional[datetime] = Field(
        default=None, sa_column=Column(DateTime(timezone=True), nullable=True)
    )

    # Set on approval, so the row points at the account it produced.
    created_user_id: Optional[str] = Field(
        default=None,
        sa_column=Column(
            String(64), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
        ),
    )

    # TimestampMixin declares these as naive datetimes; this table's migration
    # builds them timezone-aware, so they are redeclared rather than inherited.
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )

    def is_pending(self) -> bool:
        return self.status == SignupRequestStatus.PENDING

    def decide(self, status: SignupRequestStatus, by_user_id: str) -> None:
        self.status = status
        self.decided_by = by_user_id
        self.decided_at = datetime.now(timezone.utc)
        self.touch()
