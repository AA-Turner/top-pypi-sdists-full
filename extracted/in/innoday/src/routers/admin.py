"""
Admin Router for Platform Administration

This module consolidates all platform administration endpoints including:
- Platform configuration and settings
- License management
- Organization administration
- System health and monitoring
- Platform setup and initialization

All endpoints follow the pattern: /api/v1/admin/...
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, EmailStr, Field
from sqlmodel import Session, func, select

from src.api.middleware.team_secret import require_team_secret
from src.database import get_session
from src.domain.license import LicenseTier, UsageTracking
from src.domain.organization import (
    Organization,
    OrganizationLicense,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.repository import Repository
from src.domain.ticket import Ticket
from src.domain.user import User, UserRole
from src.middleware.rbac import resolve_organization
from src.routers.platform import require_platform_access


# Helper function to get platform organization
def get_platform_organization(session: Session) -> Optional[Organization]:
    """Get the platform organization (alias: platform-admin)"""
    return session.exec(
        select(Organization).where(Organization.alias == "platform-admin")
    ).first()


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


# =============================================================================
# Request/Response Models
# =============================================================================


class PlatformInfo(BaseModel):
    """Platform information and configuration"""

    organization_id: str = Field(..., description="Platform organization ID")
    name: str = Field(..., description="Platform name")
    version: str = Field(..., description="Platform version")
    environment: str = Field(
        ..., description="Environment (development/staging/production)"
    )
    initialized: bool = Field(..., description="Whether platform is initialized")
    settings: Dict[str, Any] = Field(
        default_factory=dict, description="Platform settings"
    )


class PlatformSettings(BaseModel):
    """Platform configuration settings"""

    allow_self_registration: bool = Field(
        True, description="Allow users to self-register"
    )
    require_email_verification: bool = Field(
        False, description="Require email verification"
    )
    default_license_tier: str = Field(
        "guidance", description="Default license tier for new organizations"
    )
    max_organizations_per_user: int = Field(
        5, ge=1, description="Maximum organizations per user"
    )
    enable_ai_features: bool = Field(True, description="Enable AI features globally")
    maintenance_mode: bool = Field(False, description="Enable maintenance mode")
    maintenance_message: Optional[str] = Field(
        None, description="Message to show during maintenance"
    )


class PlatformSetupRequest(BaseModel):
    """Request for complete platform setup"""

    admin_email: EmailStr = Field(..., description="Admin user email")
    admin_full_name: str = Field(..., description="Admin full name")
    platform_name: str = Field("InnoDay Platform", description="Platform name")
    platform_settings: PlatformSettings = Field(default_factory=PlatformSettings)


class PlatformStatistics(BaseModel):
    """Platform-wide statistics"""

    total_organizations: int
    total_users: int
    total_projects: int
    total_repositories: int
    total_tickets: int
    active_users_today: int
    active_users_week: int
    storage_used_gb: float
    api_calls_today: int
    api_calls_month: int


class LicenseTierCreate(BaseModel):
    """Request to create a new license tier"""

    name: str = Field(..., description="Tier name")
    display_name: str = Field(..., description="Display name")
    description: Optional[str] = Field(None, description="Tier description")
    features: Dict[str, bool] = Field(default_factory=dict, description="Feature flags")
    limits: Dict[str, int] = Field(default_factory=dict, description="Resource limits")
    price_monthly: float = Field(0, ge=0, description="Monthly price")
    price_yearly: float = Field(0, ge=0, description="Yearly price")
    is_active: bool = Field(True, description="Whether tier is available")


class OrganizationAdmin(BaseModel):
    """Organization administration model"""

    organization_id: str
    name: str
    created_at: datetime
    member_count: int
    project_count: int
    repository_count: int
    ticket_count: int
    license_tier: Optional[str]
    is_active: bool
    last_activity: Optional[datetime]


# Every route below is gated by `require_platform_access` from the platform
# router -- real token auth plus `is_platform_member`. This file used to define
# its own `require_platform_admin`, first as a stub comparing a hardcoded literal
# to a query parameter, then as a pass-through alias for the real guard. The alias
# added a name and no behaviour, so the routes now name the guard they use. See
# CLAUDE.md's Tier C table for the history.


# =============================================================================
# Platform Management Endpoints
# =============================================================================


@router.get("/platform/info", response_model=PlatformInfo)
async def get_platform_info(
    session: Session = Depends(get_session),
    admin: User = Depends(require_platform_access),
):
    """
    Get platform information and configuration.

    Returns comprehensive platform details including version,
    environment, and current settings.
    """
    platform_org = get_platform_organization(session)

    if not platform_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Platform organization not found",
        )

    # Both from the shared resolvers, like /health and /api/v1/public/status.
    # `environment` was a third local read of ENVIRONMENT, with a third default
    # ("development"), so this route could report `development` on the same
    # process where /health reported `production` (#619).
    from src.env_loader import get_environment
    from src.version import get_version

    return PlatformInfo(
        organization_id=platform_org.id,
        name=platform_org.name,
        version=get_version(),
        environment=get_environment(),
        initialized=True,
        settings=platform_org.settings or {},
    )


@router.put("/platform/settings", response_model=PlatformSettings)
async def update_platform_settings(
    settings: PlatformSettings,
    session: Session = Depends(get_session),
    admin: User = Depends(require_platform_access),
):
    """
    Update platform-wide settings.

    Modifies global platform configuration that affects
    all organizations and users.
    """
    platform_org = get_platform_organization(session)

    if not platform_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Platform organization not found",
        )

    # Update platform settings
    if not platform_org.settings:
        platform_org.settings = {}

    platform_org.settings.update(settings.model_dump())
    platform_org.updated_at = datetime.now(timezone.utc)

    session.add(platform_org)
    session.commit()

    logger.info(f"Platform settings updated by admin {admin.id}")

    return settings


@router.post(
    "/platform/setup",
    status_code=status.HTTP_201_CREATED,
    # Tier C: creates the platform org + its first user, so it carries the team
    # secret as a second factor on top of the user token.
    dependencies=[Depends(require_team_secret)],
)
async def setup_platform(
    request: PlatformSetupRequest,
    session: Session = Depends(get_session),
    _admin: User = Depends(require_platform_access),
):
    """
    Complete platform setup with admin user and initial configuration.

    This endpoint should only be called once during initial setup.
    Creates the platform organization, admin user, and default license tiers.
    """
    # Check if platform is already set up
    existing_platform = get_platform_organization(session)
    if existing_platform:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Platform is already initialized",
        )

    # Create platform organization
    platform_org = Organization(
        name=request.platform_name,
        alias="platform",
        description="Platform administration organization",
        is_platform_org=True,
        settings=request.platform_settings.model_dump(),
    )
    session.add(platform_org)

    # Create admin user
    admin_user = User(
        email=request.admin_email,
        full_name=request.admin_full_name,
        role=UserRole.ADMIN,
        is_platform_member=True,
    )
    session.add(admin_user)

    # Create admin membership in platform org
    admin_membership = OrganizationMembership(
        user_id=admin_user.id,
        organization_id=platform_org.id,
        role=OrganizationRole.ADMIN,
        is_owner=True,
        is_active=True,
    )
    session.add(admin_membership)

    # Create default license tiers
    default_tiers = [
        LicenseTier(
            name="guidance",
            display_name="Guidance",
            max_users=2,
            max_boards=1,
            daily_ticket_limit=25,
            api_rate_limit=60,
        ),
        LicenseTier(
            name="spark",
            display_name="Spark",
            max_users=5,
            max_boards=1,
            daily_ticket_limit=100,
            api_rate_limit=300,
        ),
        LicenseTier(
            name="sprint",
            display_name="Sprint",
            max_users=15,
            max_boards=5,
            daily_ticket_limit=500,
            api_rate_limit=1000,
        ),
        LicenseTier(
            name="velocity",
            display_name="Velocity",
            max_users=None,
            max_boards=None,
            daily_ticket_limit=None,
            api_rate_limit=None,
        ),
    ]

    for tier in default_tiers:
        session.add(tier)

    session.commit()

    logger.info(f"Platform initialized with admin user {admin_user.email}")

    return {
        "status": "success",
        "message": "Platform initialized successfully",
        "platform_org_id": platform_org.id,
        "admin_user_id": admin_user.id,
        "license_tiers_created": len(default_tiers),
    }


@router.get("/platform/statistics", response_model=PlatformStatistics)
async def get_platform_statistics(
    session: Session = Depends(get_session),
    admin: User = Depends(require_platform_access),
):
    """
    Get platform-wide statistics and metrics.

    Returns comprehensive statistics about platform usage,
    including organizations, users, projects, and resource utilization.
    """
    # Calculate statistics
    total_orgs = session.exec(select(func.count(Organization.id))).one()
    total_users = session.exec(select(func.count(User.id))).one()
    total_projects = session.exec(
        select(func.count()).select_from(select(Organization).subquery())
    ).one()  # Placeholder
    total_repos = session.exec(select(func.count(Repository.id))).one()
    total_tickets = session.exec(select(func.count(Ticket.id))).one()

    # Active users (simplified - should check actual activity)
    today = datetime.now(timezone.utc).date()
    week_ago = today - timedelta(days=7)

    active_today = session.exec(
        select(func.count(User.id)).where(func.date(User.last_login_at) == today)
    ).one()

    active_week = session.exec(
        select(func.count(User.id)).where(func.date(User.last_login_at) >= week_ago)
    ).one()

    # API usage (from usage tracking)
    api_calls_today = (
        session.exec(
            select(func.sum(UsageTracking.usage_count))
            .where(func.date(UsageTracking.usage_date) == today)
            .where(UsageTracking.usage_type == "api_call")
        ).one()
        or 0
    )

    month_start = today.replace(day=1)
    api_calls_month = (
        session.exec(
            select(func.sum(UsageTracking.usage_count))
            .where(func.date(UsageTracking.usage_date) >= month_start)
            .where(UsageTracking.usage_type == "api_call")
        ).one()
        or 0
    )

    return PlatformStatistics(
        total_organizations=total_orgs,
        total_users=total_users,
        total_projects=total_projects,
        total_repositories=total_repos,
        total_tickets=total_tickets,
        active_users_today=active_today,
        active_users_week=active_week,
        storage_used_gb=0.0,  # Placeholder
        api_calls_today=api_calls_today,
        api_calls_month=api_calls_month,
    )


# =============================================================================
# License Management Endpoints
# =============================================================================


@router.get("/licenses/tiers", response_model=List[LicenseTier])
async def list_license_tiers(
    include_inactive: bool = Query(False, description="Include inactive tiers"),
    session: Session = Depends(get_session),
    admin: User = Depends(require_platform_access),
):
    """
    List all available license tiers.

    Returns all license tiers with their features and limits.
    Optionally includes inactive tiers.
    """
    query = select(LicenseTier)
    if not include_inactive:
        query = query.where(LicenseTier.is_active == True)

    tiers = session.exec(query.order_by(LicenseTier.price_monthly)).all()
    return tiers


@router.post(
    "/licenses/tiers", response_model=LicenseTier, status_code=status.HTTP_201_CREATED
)
async def create_license_tier(
    tier: LicenseTierCreate,
    session: Session = Depends(get_session),
    admin: User = Depends(require_platform_access),
):
    """
    Create a new license tier.

    Adds a new licensing option with specific features and limits.
    """
    # Check if tier name already exists
    existing = session.exec(
        select(LicenseTier).where(LicenseTier.name == tier.name)
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"License tier '{tier.name}' already exists",
        )

    new_tier = LicenseTier(**tier.model_dump())
    session.add(new_tier)
    session.commit()
    session.refresh(new_tier)

    logger.info(f"License tier '{new_tier.name}' created by admin {admin.id}")

    return new_tier


@router.put("/licenses/tiers/{tier_name}", response_model=LicenseTier)
async def update_license_tier(
    tier_name: str,
    updates: LicenseTierCreate,
    session: Session = Depends(get_session),
    admin: User = Depends(require_platform_access),
):
    """
    Update an existing license tier.

    Modifies features, limits, or pricing for a license tier.
    Changes affect new subscriptions only.
    """
    tier = session.exec(
        select(LicenseTier).where(LicenseTier.name == tier_name)
    ).first()

    if not tier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"License tier '{tier_name}' not found",
        )

    # Update tier fields
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(tier, field, value)

    tier.updated_at = datetime.now(timezone.utc)
    session.add(tier)
    session.commit()
    session.refresh(tier)

    logger.info(f"License tier '{tier.name}' updated by admin {admin.id}")

    return tier


@router.post("/licenses/assign", status_code=status.HTTP_201_CREATED)
async def assign_license_to_organization(
    organization_id: str,
    tier_name: str,
    valid_until: Optional[datetime] = None,
    session: Session = Depends(get_session),
    admin: User = Depends(require_platform_access),
):
    """
    Assign a license tier to an organization.

    Grants an organization access to specific features and limits
    based on the assigned license tier.
    """
    # Verify organization exists
    resolve_organization(organization_id, session)

    # Verify tier exists
    tier = session.exec(
        select(LicenseTier).where(LicenseTier.name == tier_name)
    ).first()

    if not tier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"License tier '{tier_name}' not found",
        )

    # Check for existing active license
    existing_license = session.exec(
        select(OrganizationLicense)
        .where(OrganizationLicense.organization_id == organization_id)
        .where(OrganizationLicense.status == "ACTIVE")
    ).first()

    if existing_license:
        # Deactivate existing license
        existing_license.status = "CANCELLED"
        existing_license.valid_until = datetime.now(timezone.utc)
        session.add(existing_license)

    # Create new license
    new_license = OrganizationLicense(
        organization_id=organization_id,
        license_tier_id=tier.id,
        status="ACTIVE",
        valid_from=datetime.now(timezone.utc),
        valid_until=valid_until,
        auto_renew=valid_until is None,  # Auto-renew if no expiry
    )

    session.add(new_license)
    session.commit()

    logger.info(
        f"License tier '{tier_name}' assigned to organization {organization_id} by admin {admin.id}"
    )

    return {
        "status": "success",
        "organization_id": organization_id,
        "license_tier": tier_name,
        "valid_from": new_license.valid_from.isoformat(),
        "valid_until": valid_until.isoformat() if valid_until else None,
        "auto_renew": new_license.auto_renew,
    }


# =============================================================================
# Organization Administration Endpoints
# =============================================================================


@router.get("/organizations", response_model=List[OrganizationAdmin])
async def list_all_organizations(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    include_inactive: bool = Query(False),
    session: Session = Depends(get_session),
    admin: User = Depends(require_platform_access),
):
    """
    List all organizations on the platform.

    Returns comprehensive information about each organization
    including member counts, resource usage, and license status.
    """
    query = select(Organization)
    if not include_inactive:
        query = query.where(Organization.is_active == True)

    query = query.offset(offset).limit(limit)
    organizations = session.exec(query).all()

    result = []
    for org in organizations:
        # Get counts (simplified - should be optimized)
        member_count = session.exec(
            select(func.count(OrganizationMembership.id))
            .where(OrganizationMembership.organization_id == org.id)
            .where(OrganizationMembership.is_active == True)
        ).one()

        ticket_count = session.exec(
            select(func.count(Ticket.id)).where(Ticket.organization_id == org.id)
        ).one()

        repo_count = session.exec(
            select(func.count(Repository.id)).where(
                Repository.organization_id == org.id
            )
        ).one()

        # Get active license
        license = session.exec(
            select(OrganizationLicense)
            .where(OrganizationLicense.organization_id == org.id)
            .where(OrganizationLicense.status == "ACTIVE")
        ).first()

        license_tier = None
        if license:
            tier = session.get(LicenseTier, license.license_tier_id)
            license_tier = tier.name if tier else None

        result.append(
            OrganizationAdmin(
                organization_id=org.id,
                name=org.name,
                created_at=org.created_at,
                member_count=member_count,
                project_count=0,  # Placeholder
                repository_count=repo_count,
                ticket_count=ticket_count,
                license_tier=license_tier,
                is_active=org.is_active,
                last_activity=org.updated_at,
            )
        )

    return result


@router.put("/organizations/{organization_id}/status")
async def update_organization_status(
    organization_id: str,
    is_active: bool,
    reason: Optional[str] = None,
    session: Session = Depends(get_session),
    admin: User = Depends(require_platform_access),
):
    """
    Activate or deactivate an organization.

    Suspending an organization prevents access but preserves data.
    """
    org = resolve_organization(organization_id, session)

    if org.alias == "platform-admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot modify platform organization status",
        )

    org.is_active = is_active
    org.updated_at = datetime.now(timezone.utc)

    # Log the action
    if not org.settings:
        org.settings = {}

    org.settings["status_history"] = org.settings.get("status_history", [])
    org.settings["status_history"].append(
        {
            "changed_to": "active" if is_active else "suspended",
            "changed_by": admin.id,
            "changed_at": datetime.now(timezone.utc).isoformat(),
            "reason": reason,
        }
    )

    session.add(org)
    session.commit()

    logger.info(
        f"Organization {organization_id} status changed to {'active' if is_active else 'suspended'} by admin {admin.id}"
    )

    return {
        "status": "success",
        "organization_id": organization_id,
        "is_active": is_active,
        "reason": reason,
    }


@router.delete(
    "/organizations/{organization_id}",
    # Tier C: org/user lifecycle — team secret as a second factor.
    dependencies=[Depends(require_team_secret)],
)
async def delete_organization(
    organization_id: str,
    confirm: bool = Query(False, description="Confirm deletion"),
    session: Session = Depends(get_session),
    admin: User = Depends(require_platform_access),
):
    """
    Permanently delete an organization and all its data.

    This action is irreversible and will delete all associated
    projects, repositories, tickets, and memberships.
    """
    if not confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Deletion must be confirmed with confirm=true parameter",
        )

    org = resolve_organization(organization_id, session)

    if org.alias == "platform-admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete platform organization",
        )

    # Cascade-delete in FK dependency order (children before parents)
    from src.services.organization_cascade import delete_organization_cascade

    delete_organization_cascade(session, org.id)

    session.delete(org)
    session.commit()

    logger.warning(
        f"Organization {organization_id} permanently deleted by admin {admin.id}"
    )

    return {
        "status": "success",
        "message": f"Organization {org.name} permanently deleted",
        "deleted_at": datetime.now(timezone.utc).isoformat(),
    }


# =============================================================================
# System Maintenance Endpoints
# =============================================================================


@router.post("/maintenance/enable")
async def enable_maintenance_mode(
    message: str = "System is under maintenance. Please try again later.",
    estimated_duration_minutes: Optional[int] = None,
    session: Session = Depends(get_session),
    admin: User = Depends(require_platform_access),
):
    """
    Enable platform-wide maintenance mode.

    This will prevent non-admin users from accessing the platform
    and display a maintenance message.
    """
    platform_org = get_platform_organization(session)

    if not platform_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Platform organization not found",
        )

    if not platform_org.settings:
        platform_org.settings = {}

    platform_org.settings["maintenance"] = {
        "enabled": True,
        "message": message,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "estimated_end": (
            (
                datetime.now(timezone.utc)
                + timedelta(minutes=estimated_duration_minutes)
            ).isoformat()
            if estimated_duration_minutes
            else None
        ),
        "enabled_by": admin.id,
    }

    session.add(platform_org)
    session.commit()

    logger.warning(f"Maintenance mode enabled by admin {admin.id}")

    return {
        "status": "success",
        "maintenance_enabled": True,
        "message": message,
        "estimated_duration_minutes": estimated_duration_minutes,
    }


@router.post("/maintenance/disable")
async def disable_maintenance_mode(
    session: Session = Depends(get_session),
    admin: User = Depends(require_platform_access),
):
    """
    Disable platform-wide maintenance mode.

    Restores normal platform access for all users.
    """
    platform_org = get_platform_organization(session)

    if not platform_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Platform organization not found",
        )

    if platform_org.settings and "maintenance" in platform_org.settings:
        maintenance_info = platform_org.settings["maintenance"]
        maintenance_info["enabled"] = False
        maintenance_info["ended_at"] = datetime.now(timezone.utc).isoformat()
        maintenance_info["disabled_by"] = admin.id

    session.add(platform_org)
    session.commit()

    logger.info(f"Maintenance mode disabled by admin {admin.id}")

    return {
        "status": "success",
        "maintenance_enabled": False,
        "message": "Platform is now accessible",
    }
