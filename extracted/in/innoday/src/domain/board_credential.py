from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlmodel import Column, Field, Relationship

from src.domain._base import TimestampMixin

if TYPE_CHECKING:
    from src.domain.board import BoardRegistration
    from src.domain.organization import Organization


class BoardCredential(TimestampMixin, table=True):
    """
    Server-side source of truth for a board's API credentials.

    Stores NOT the credential itself, but a pointer (vault_secret_id) into
    Supabase Vault, which holds the encrypted payload. One row per
    board_registration -- a board always has exactly one active credential
    set, replaced (not versioned) on rotation.

    Security note: the actual key/token/email values never touch this table
    or any InnoDay log -- they exist only as ciphertext in vault.secrets and
    plaintext transiently in the vault.decrypted_secrets view at read time,
    accessed exclusively through the get_board_credential() SQL function.
    """

    __tablename__ = "board_credentials"

    id: str = Field(
        default_factory=lambda: str(uuid4()), sa_column=Column(String, primary_key=True)
    )

    # `nullable=False` has to be stated explicitly on both of these. Passing an
    # explicit `sa_column=` bypasses SQLModel's inference, so the `str`
    # annotation stops implying NOT NULL and SQLAlchemy falls back to its own
    # default of nullable=True. Dev's real schema (built by migrations) has both
    # NOT NULL, so without this `SQLModel.metadata.create_all` -- which the test
    # fixtures use -- produced a *more permissive* schema than production, and a
    # row the tests accepted would be rejected in deployment.
    organization_id: str = Field(
        sa_column=Column(
            String,
            ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    board_registration_id: str = Field(
        sa_column=Column(
            String,
            ForeignKey("board_registrations.id", ondelete="CASCADE"),
            unique=True,
            nullable=False,
        )
    )

    # trello / jira / linear / notion -- informs how the JSON payload below
    # should be parsed, without requiring a join back to board_registrations.
    board_type: str = Field(max_length=32)

    # Pointer into Supabase Vault -- NOT the secret itself. The secret column
    # in vault.secrets holds a JSON payload, e.g. {"api_key": "...", "token":
    # "..."} for Trello, {"email": "...", "api_token": "..."} for Jira, or
    # {"token": "..."} for Linear/Notion/GitHub -- one Vault secret per
    # board, not per field. See src/services/board_credential_service.py for
    # the legacy-token <-> payload conversion used at the API boundary.
    vault_secret_id: str = Field(max_length=36)

    last_validated_at: Optional[datetime] = Field(default=None)
    last_rotated_at: Optional[datetime] = Field(default=None)
    rotated_by_user_id: Optional[str] = Field(
        default=None, sa_column=Column(String, ForeignKey("users.id"))
    )

    organization: Optional["Organization"] = Relationship()
    board_registration: Optional["BoardRegistration"] = Relationship()

    __table_args__ = (
        UniqueConstraint("board_registration_id", name="uq_board_credential_per_board"),
        # Built by the migration; declared here so `create_all` (the test
        # fixtures' schema) matches production and autogenerate does not
        # propose dropping it.
        Index("ix_board_credentials_organization_id", "organization_id"),
    )
