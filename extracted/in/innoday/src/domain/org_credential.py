from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlmodel import Column, Field, Relationship

from src.domain._base import TimestampMixin

if TYPE_CHECKING:
    from src.domain.organization import Organization


class OrgCredential(TimestampMixin, table=True):
    """
    Server-side source of truth for an organization-scoped integration's API
    credentials (e.g. GitHub).

    Mirrors BoardCredential's Vault-pointer pattern exactly, but keyed by
    (organization_id, integration_type) rather than board_registration_id --
    GitHub's connection is organization-scoped, not board-scoped (no
    BoardRegistration involved), so it needed its own table rather than a
    nullable board_registration_id bolted onto board_credentials (which
    would risk every existing Jira/Trello/Linear/Notion call site relying
    on that column being required).

    Stores NOT the credential itself, but a pointer (vault_secret_id) into
    Supabase Vault, which holds the encrypted payload. One row per
    (organization_id, integration_type) pair -- an org has exactly one
    active credential set per integration type, replaced (not versioned)
    on rotation.

    Security note: the actual token/secret values never touch this table
    or any InnoDay log -- they exist only as ciphertext in vault.secrets and
    plaintext transiently in the vault.decrypted_secrets view at read time,
    accessed exclusively through the get_org_credential() SQL function.
    """

    __tablename__ = "org_credentials"

    id: str = Field(
        default_factory=lambda: str(uuid4()), sa_column=Column(String, primary_key=True)
    )

    organization_id: str = Field(
        sa_column=Column(String, ForeignKey("organizations.id", ondelete="CASCADE"))
    )

    # "github" today; generic so a future org-scoped integration can reuse
    # this table instead of needing its own parallel one.
    integration_type: str = Field(max_length=32)

    # Pointer into Supabase Vault -- NOT the secret itself. The secret
    # column in vault.secrets holds a JSON payload, e.g. {"token": "...",
    # "github_org": "..."} for GitHub -- one Vault secret per (org,
    # integration_type) pair. See src/services/org_credential_service.py
    # for the read/write functions used at the API boundary.
    vault_secret_id: str = Field(max_length=36)

    last_validated_at: Optional[datetime] = Field(default=None)
    last_rotated_at: Optional[datetime] = Field(default=None)
    rotated_by_user_id: Optional[str] = Field(
        default=None, sa_column=Column(String, ForeignKey("users.id"))
    )

    organization: Optional["Organization"] = Relationship()

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "integration_type",
            name="uq_org_credential_per_org_integration",
        ),
    )
