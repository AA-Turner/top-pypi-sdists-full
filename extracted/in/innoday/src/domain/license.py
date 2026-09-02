"""
License domain models for the InnoDay platform.

This module defines the licensing system that controls feature access,
usage limits, and user quotas based on subscription tiers.

License Tiers:
- Guidance: 2 users, 1 board, 25 tickets/day per user
- Spark: 5 users, 1 board, 100 tickets/day per user
- Sprint: 15 users, 5 boards, 500 tickets/day per user
- Velocity: No restrictions

ARCHITECTURE NOTES:
==================
1. License data is accessed ONLY through API endpoints
2. No direct database access from CLI, Agent, or UI
3. License validation happens at the API layer
4. Usage tracking is atomic and real-time
5. All license changes are audited
"""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from uuid import uuid4

from sqlalchemy import JSON, ForeignKey, String, UniqueConstraint
from sqlmodel import Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.domain.organization import Organization, OrganizationLicense
    from src.domain.user import User


class LicenseTier(SQLModel, table=True):
    """
    License tier definitions that control platform limits.

    This is a system table that defines the available license tiers.
    It should be seeded during migration and rarely changed.
    """

    __tablename__ = "license_tiers"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str = Field(
        unique=True, index=True, max_length=50
    )  # guidance, spark, sprint, velocity
    display_name: str = Field(max_length=100)

    # Limits (NULL means unlimited)
    max_users: Optional[int] = Field(default=None)
    max_boards: Optional[int] = Field(default=None)
    daily_ticket_limit: Optional[int] = Field(default=None)  # Per user
    api_rate_limit: Optional[int] = Field(default=None)  # Per hour
    sync_interval_minutes: int = Field(default=0)  # 0 means real-time

    # Additional features as JSON
    features: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    organization_licenses: List["OrganizationLicense"] = Relationship(
        back_populates="tier"
    )

    def has_feature(self, feature: str) -> bool:
        """Check if this tier has a specific feature enabled"""
        return self.features.get(feature, False)

    def get_limit(self, resource: str) -> Optional[int]:
        """Get the limit for a specific resource, None means unlimited"""
        limits = {
            "users": self.max_users,
            "boards": self.max_boards,
            "daily_tickets": self.daily_ticket_limit,
            "api_calls": self.api_rate_limit,
        }
        return limits.get(resource)


# ClientLicense model removed - use OrganizationLicense instead


class UsageTracking(SQLModel, table=True):
    """
    Usage tracking for license enforcement.

    Tracks daily usage per user per organization for various resources.
    This data is used to enforce license limits in real-time.
    """

    __tablename__ = "usage_tracking"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)

    # Organization foreign key
    organization_id: str = Field(
        sa_column=Column(
            String, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
        ),
        description="Organization this usage tracking belongs to",
    )

    user_id: str = Field(
        sa_column=Column(String, ForeignKey("users.id", ondelete="CASCADE"))
    )

    # Usage tracking
    usage_type: str = Field(max_length=50)  # ticket_created, board_synced, api_call
    usage_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).date()
    )
    usage_count: int = Field(default=1)

    # Timestamp
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    organization: "Organization" = Relationship()
    user: Optional["User"] = Relationship()

    # Constraints
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "user_id",
            "usage_type",
            "usage_date",
            name="uq_usage_per_day_org",
        ),
    )

    def get_organization_id(self) -> str:
        """Get organization ID."""
        return self.organization_id

    def get_organization(self) -> "Organization":
        """Get organization object."""
        return self.organization


class LicenseAuditLog(SQLModel, table=True):
    """
    Audit log for all license-related changes.

    Tracks license upgrades, downgrades, suspensions, and other changes
    for compliance and debugging purposes.
    """

    __tablename__ = "license_audit_log"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)

    # Organization foreign key
    organization_id: str = Field(
        sa_column=Column(String, ForeignKey("organizations.id"), nullable=False),
        description="Organization this audit log belongs to",
    )

    license_tier_id: str = Field(
        sa_column=Column(String, ForeignKey("license_tiers.id"))
    )

    # Audit details
    action: str = Field(max_length=50)  # created, upgraded, downgraded, suspended, etc.
    previous_tier_id: Optional[str] = Field(
        default=None, sa_column=Column(String, ForeignKey("license_tiers.id"))
    )
    reason: Optional[str] = Field(default=None)
    performed_by: Optional[str] = Field(
        default=None, sa_column=Column(String, ForeignKey("users.id"))
    )

    # Timestamp
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    organization: "Organization" = Relationship()
    tier: Optional["LicenseTier"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[LicenseAuditLog.license_tier_id]"}
    )
    previous_tier: Optional["LicenseTier"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[LicenseAuditLog.previous_tier_id]"}
    )
    user: Optional["User"] = Relationship()

    def get_organization_id(self) -> str:
        """Get organization ID."""
        return self.organization_id

    def get_organization(self) -> "Organization":
        """Get organization object."""
        return self.organization
