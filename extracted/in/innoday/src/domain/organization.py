"""
Organization Domain Models

Defines the Organization, OrganizationMembership, and OrganizationLicense models
to replace the Client concept with a clearer organizational structure.
"""

import re
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy import JSON, Column, UniqueConstraint
from sqlmodel import Field, Relationship

from src.domain._base import TimestampMixin

if TYPE_CHECKING:
    from .board import BoardRegistration
    from .container_execution import ContainerExecution
    from .license import LicenseTier
    from .project import Project
    from .release import Release
    from .repository import Repository
    from .ticket import Ticket
    from .user import User


class OrganizationRole(str, Enum):
    """Organization-level roles for members."""

    MEMBER = "MEMBER"  # Read tickets, view summaries
    ADMIN = "ADMIN"  # Manage members, settings, create projects
    DEVELOPER = "DEVELOPER"  # Sync boards, manage tickets — no member/project creation


# Capability ranking, used by verify_org_membership to treat a required role as a
# MINIMUM rather than an exact match.
#
# Without this the check was `membership.role != required_role`, so a route asking for
# DEVELOPER *rejected an ADMIN* — 9 routes (7 board, 2 release) locked admins out of
# board sync, while six ticket routes hand-rolled
# `if membership.role not in (DEVELOPER, ADMIN)` precisely because equality could not
# express "either". The rank makes ADMIN strictly more capable, which is what
# CLAUDE.md's access table already described.
#
# Enum definition order is not the ranking — declare it explicitly so reordering the
# enum can never silently change who has access.
ORGANIZATION_ROLE_RANK: dict["OrganizationRole", int] = {
    OrganizationRole.MEMBER: 1,
    OrganizationRole.DEVELOPER: 2,
    OrganizationRole.ADMIN: 3,
}


def role_satisfies(actual: OrganizationRole, minimum: OrganizationRole) -> bool:
    """Whether ``actual`` meets or exceeds ``minimum``.

    Ownership (``OrganizationMembership.is_owner``) is deliberately orthogonal to this
    ranking — an owner is not a fourth role, it is a flag on a membership, and routes
    that care check it directly.
    """
    return ORGANIZATION_ROLE_RANK.get(actual, 0) >= ORGANIZATION_ROLE_RANK.get(
        minimum, 0
    )


class Organization(TimestampMixin, table=True):
    """
    Organization represents a company, team, or group using InnoDay.
    All users belong to an organization, and licenses are at the org level.

    This replaces the Client model with clearer organizational boundaries.
    """

    __tablename__ = "organizations"

    # Identity
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(max_length=100, index=True)
    alias: str = Field(
        max_length=50,
        unique=True,
        index=True,
        description="Globally-unique URL-friendly identifier for the org "
        "(e.g. 'bp', 'hs'); auto-derived from name if not provided. Also used "
        "as the org's identifier in CLI config keys, keyring entries, and API "
        "path lookups (see resolve_organization in src/middleware/rbac.py). "
        "NOTE: org alias is unique system-wide (it replaced the old org slug). "
        "This is DIFFERENT from Project.alias, which is unique only within an "
        "organization -- see src/domain/project.py.",
    )

    # Organization details
    description: Optional[str] = Field(default=None, max_length=500)
    website: Optional[str] = Field(default=None, max_length=200)
    logo_url: Optional[str] = Field(default=None, max_length=500)

    # Integration URLs (inherited from current Client model)
    jira_url: Optional[str] = Field(default=None, max_length=500)
    github_url: Optional[str] = Field(default=None, max_length=500)
    trello_url: Optional[str] = Field(default=None, max_length=500)

    # Platform-related fields (only used by platform organization)
    support_email: Optional[str] = Field(default=None, max_length=255)
    billing_email: Optional[str] = Field(default=None, max_length=255)
    stripe_customer_id: Optional[str] = Field(default=None, max_length=255)
    billing_plan: Optional[str] = Field(default=None, max_length=100)

    # Organization settings
    settings: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    # When True, any authenticated user may join this org WITHOUT an invite
    # (`innoday join <org>`). Default off = invite-only. A transition aid for
    # onboarding; owners/admins flip it on to open self-registration.
    allow_self_registration: bool = Field(
        default=False,
        description="If True, authenticated users can self-join without an invite.",
    )

    # Status
    is_active: bool = Field(default=True)

    # Relationships (forward references to avoid circular imports)
    memberships: List["OrganizationMembership"] = Relationship(
        back_populates="organization"
    )
    license: Optional["OrganizationLicense"] = Relationship(
        back_populates="organization"
    )  # One license per org (current limitation)
    tickets: List["Ticket"] = Relationship(back_populates="organization")
    projects: List["Project"] = Relationship(back_populates="organization")
    board_registrations: List["BoardRegistration"] = Relationship(
        back_populates="organization"
    )
    container_executions: List["ContainerExecution"] = Relationship(
        back_populates="organization"
    )
    repositories: List["Repository"] = Relationship(
        back_populates="organization", sa_relationship_kwargs={"lazy": "select"}
    )
    releases: List["Release"] = Relationship(back_populates="organization")

    @staticmethod
    def generate_alias(name: str) -> str:
        """Derive a URL-friendly alias from organization name."""
        alias = re.sub(r"[^a-zA-Z0-9\s-]", "", name.lower())
        alias = re.sub(r"[\s-]+", "-", alias)
        alias = alias.strip("-")
        if not alias:
            alias = f"org-{str(uuid.uuid4())[:8]}"
        elif len(alias) > 50:
            alias = alias[:47] + f"-{str(uuid.uuid4())[:3]}"
        return alias

    def __init__(self, **data):
        """Auto-generate alias from name when not provided."""
        if "alias" not in data and "name" in data:
            data["alias"] = self.generate_alias(data["name"])
        super().__init__(**data)


class OrganizationMembership(TimestampMixin, table=True):
    """
    Links users to organizations with specific roles.
    Users can belong to multiple organizations with different roles.
    """

    __tablename__ = "organization_memberships"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    organization_id: str = Field(foreign_key="organizations.id", index=True)

    # Membership details
    # DEVELOPER by default -- see MembershipCreate in routers/organizations.py.
    # This is the storage-level default for any path that does not name a role.
    role: OrganizationRole = Field(default=OrganizationRole.DEVELOPER)
    is_owner: bool = Field(
        default=False
    )  # Org creator; can delete org and manage licenses
    is_active: bool = Field(default=True)
    joined_at: datetime = Field(default_factory=datetime.utcnow)
    invited_by: Optional[str] = Field(default=None)

    # The project this person lands on in this org -- per user *and* per org,
    # which is why it lives on the membership rather than on `User`. Someone in
    # three orgs has three answers, and a column on `User` could only hold one.
    #
    # The row is already uniquely keyed by `uq_user_org_membership`
    # (user_id, organization_id) below, so this needs no uniqueness rule of its
    # own: there is at most one membership per pair, hence at most one default.
    #
    # Nullable, and NULL is meaningful: an org with no projects yet has nothing
    # to default to. Seeded when the org's first project is created, and
    # backfilled to the oldest project per org by the migration that added it.
    default_project_id: Optional[str] = Field(
        default=None, foreign_key="projects.id", nullable=True, index=True
    )

    # Relationships (forward references)
    user: Optional["User"] = Relationship(back_populates="organization_memberships")
    organization: Optional["Organization"] = Relationship(back_populates="memberships")

    # Constraints
    __table_args__ = (
        UniqueConstraint("user_id", "organization_id", name="uq_user_org_membership"),
    )

    def is_admin_or_owner(self) -> bool:
        """Check if user has admin privileges in the organization.

        Ownership always implies admin capability: an owner is admin-or-higher
        regardless of the stored `role`. (Previously this ignored `is_owner`,
        so an owner whose role wasn't exactly ADMIN was wrongly treated as a
        non-admin.)
        """
        return self.is_owner or self.role == OrganizationRole.ADMIN

    def can_manage_members(self) -> bool:
        """Check if user can invite/manage other members."""
        return self.is_admin_or_owner()

    def can_manage_settings(self) -> bool:
        """Check if user can modify organization settings."""
        return self.is_admin_or_owner()

    def can_manage_licenses(self) -> bool:
        """Check if user can manage organization licenses (owner only)."""
        return self.is_owner


class OrganizationLicense(TimestampMixin, table=True):
    """
    Organization license assignments (replaces ClientLicense concept).

    CURRENT LIMITATION: Each organization has exactly one active license at a time.
    This is a simplification for the initial implementation. In the future, this
    could be extended to support multiple licenses per organization (e.g., different
    licenses for different teams/departments within the same organization).

    The Client model should NOT have licenses - all licensing is now organization-based,
    providing clearer boundaries for multi-tenant usage tracking and billing.
    """

    __tablename__ = "organization_licenses"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    organization_id: str = Field(foreign_key="organizations.id", index=True)
    license_tier_id: str = Field(foreign_key="license_tiers.id")

    # License status and validity
    status: str = Field(
        max_length=50, default="ACTIVE"
    )  # ACTIVE, EXPIRED, SUSPENDED, CANCELLED
    valid_from: datetime = Field(default_factory=datetime.utcnow)
    valid_until: Optional[datetime] = Field(default=None)
    auto_renew: bool = Field(default=False)

    # Relationships (forward references)
    organization: Optional["Organization"] = Relationship(back_populates="license")
    tier: Optional["LicenseTier"] = Relationship(back_populates="organization_licenses")

    # Constraints
    __table_args__ = (
        UniqueConstraint("organization_id", name="uq_one_license_per_organization"),
    )

    @property
    def is_active(self) -> bool:
        """Check if license is currently active and valid."""
        if self.status != "ACTIVE":
            return False

        now = datetime.now(timezone.utc)
        if self.valid_until and now > self.valid_until:
            return False

        return True

    @property
    def days_until_expiry(self) -> Optional[int]:
        """Get number of days until license expires."""
        if not self.valid_until:
            return None

        delta = self.valid_until - datetime.now(timezone.utc)
        return max(0, delta.days)
