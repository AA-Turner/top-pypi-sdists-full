"""Platform API endpoints using organization-based access control."""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import func, text
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlmodel import Session, select

from src.api.middleware.team_secret import require_team_secret
from src.database import get_session
from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.user import User
from src.middleware.rbac import get_current_user

router = APIRouter(prefix="/api/v1/platform", tags=["platform"])


# Request/Response Models
class PlatformInfoResponse(BaseModel):
    """Response model for platform organization information.

    Note: sourced from Organization.alias -- Organization no longer has a
    separate `slug` field, but the response key is kept as `slug` here.
    """

    id: str
    name: str
    slug: str
    description: Optional[str]
    website: Optional[str]
    support_email: Optional[str]
    billing_email: Optional[str]
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class PlatformSetupRequest(BaseModel):
    """Request model for comprehensive platform setup"""

    platform_name: str = Field(..., min_length=1, max_length=100)
    admin_email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    admin_name: str = Field(..., min_length=1, max_length=100)
    # Integration tokens (will be stored in settings, not database)
    github_token: Optional[str] = Field(None, min_length=1)
    jira_token: Optional[str] = Field(None, min_length=1)
    jira_email: Optional[str] = Field(None, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    jira_url: Optional[str] = Field(None)
    trello_api_key: Optional[str] = Field(None, min_length=1)
    trello_token: Optional[str] = Field(None, min_length=1)
    claude_api_key: Optional[str] = Field(None, min_length=1)

    # Platform settings
    support_email: Optional[str] = Field(None, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    billing_email: Optional[str] = Field(None, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    website: Optional[str] = Field(None)


class PlatformSetupResponse(BaseModel):
    """Response model for platform setup completion"""

    platform_id: str
    admin_user_id: str
    api_key: str
    platform_name: str
    integrations_configured: Dict[str, bool]
    setup_complete: bool


class PlatformSettingsUpdate(BaseModel):
    """Request model for updating platform settings"""

    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    website: Optional[str] = Field(None, max_length=200)
    support_email: Optional[str] = Field(None, max_length=255)
    billing_email: Optional[str] = Field(None, max_length=255)
    settings: Optional[Dict[str, Any]] = None


class PlatformStatusResponse(BaseModel):
    """Response model for platform status"""

    platform_configured: bool
    platform_name: str
    support_email: Optional[str]
    total_organizations: int
    total_users: int
    platform_version: str


# Helper Functions
def get_platform_organization(session: Session) -> Optional[Organization]:
    """Get the platform organization (identified by having users with PLATFORM role)"""
    # For v0.1.0 simplified approach: look for organization with platform-related alias
    # In future versions, add is_platform field to Organization model
    statement = select(Organization).where(
        (Organization.alias == "platform")
        | (Organization.alias == "innoday-platform")
        | (Organization.name.ilike("%platform%"))
    )
    return session.exec(statement).first()


async def require_platform_access(
    user: User = Depends(get_current_user),
) -> User:
    """The caller must be an authenticated platform member.

    **403, not 401.** 401 means "I do not know who you are" and tells a client to
    authenticate again; 403 means "I know exactly who you are, and you may not do
    this". Answering 401 to a perfectly valid token sends the CLI round a loop
    that cannot succeed, and CLAUDE.md's own RLS section already names 403 as what
    the CLI expects for an authorization failure.

    `is_platform_member` is the only live notion of platform admin, so this is
    read directly rather than through a helper -- there used to be a
    `check_platform_access(user, session)` wrapping this one attribute behind a
    session it never used.
    """
    if not user.is_platform_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden - Platform access required",
        )
    return user


# API Endpoints


@router.get(
    "/info",
    response_model=PlatformInfoResponse,
    summary="Get platform organization information",
    description="Get information about the platform organization (requires platform access)",
)
async def get_platform_info(
    user: User = Depends(require_platform_access),
    session: Session = Depends(get_session),
):
    """Get platform organization information"""
    platform_org = get_platform_organization(session)
    if not platform_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Platform organization not found",
        )

    return PlatformInfoResponse(
        id=platform_org.id,
        name=platform_org.name,
        slug=platform_org.alias,
        description=platform_org.description,
        website=platform_org.website,
        support_email=platform_org.support_email,
        billing_email=platform_org.billing_email,
        created_at=platform_org.created_at.isoformat(),
        updated_at=platform_org.updated_at.isoformat(),
    )


@router.put(
    "/settings",
    response_model=PlatformInfoResponse,
    summary="Update platform settings",
    description="Update platform organization settings (requires platform access)",
)
async def update_platform_settings(
    update_data: PlatformSettingsUpdate,
    user: User = Depends(require_platform_access),
    session: Session = Depends(get_session),
):
    """Update platform organization settings"""
    platform_org = get_platform_organization(session)
    if not platform_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Platform organization not found",
        )

    # Update only provided fields
    update_dict = update_data.model_dump(exclude_unset=True)

    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No update data provided"
        )

    # Update platform organization
    for key, value in update_dict.items():
        if hasattr(platform_org, key) and key != "id":
            setattr(platform_org, key, value)

    session.add(platform_org)
    session.commit()
    session.refresh(platform_org)

    return PlatformInfoResponse(
        id=platform_org.id,
        name=platform_org.name,
        slug=platform_org.alias,
        description=platform_org.description,
        website=platform_org.website,
        support_email=platform_org.support_email,
        billing_email=platform_org.billing_email,
        created_at=platform_org.created_at.isoformat(),
        updated_at=platform_org.updated_at.isoformat(),
    )


@router.get(
    "/status",
    response_model=PlatformStatusResponse,
    summary="Get platform status",
    description="Get overall platform status and statistics",
)
async def get_platform_status(
    session: Session = Depends(get_session),
    _user: User = Depends(require_platform_access),
):
    """Get platform status (public endpoint)"""
    platform_org = get_platform_organization(session)

    # Get statistics
    from src.domain.user import User

    total_organizations = session.exec(select(Organization)).all()
    total_users = session.exec(select(User)).all()

    # Get version from version module
    from src.version import get_display_version

    return PlatformStatusResponse(
        platform_configured=platform_org is not None,
        platform_name=platform_org.name if platform_org else "InnoDay Platform",
        support_email=platform_org.support_email if platform_org else None,
        total_organizations=len(total_organizations),
        total_users=len(total_users),
        platform_version=get_display_version(),
    )


@router.post(
    "/setup",
    dependencies=[Depends(require_team_secret)],
    response_model=PlatformSetupResponse,
    summary="Comprehensive platform setup",
    description="Complete platform setup with admin user and integrations",
)
async def setup_platform(
    setup_data: PlatformSetupRequest,
    session: Session = Depends(get_session),
    _user: User = Depends(require_platform_access),
):
    """Comprehensive platform setup with configuration and admin user"""

    from src.domain.license import LicenseTier
    from src.domain.user import User, UserRole

    # Check if platform is already set up
    existing_org = get_platform_organization(session)
    if existing_org:
        # Check if we have an admin user
        admin_user = session.exec(
            select(User).where(User.email == setup_data.admin_email)
        ).first()

        if admin_user:
            # Ensure the admin user has the correct role/flags even if already set up
            admin_user.role = UserRole.ADMIN
            admin_user.is_platform_member = True
            session.add(admin_user)
            session.commit()
            return PlatformSetupResponse(
                platform_id=existing_org.id,
                admin_user_id=admin_user.id,
                api_key=admin_user.id,  # For now, use user ID as API key
                platform_name=existing_org.name,
                integrations_configured={
                    "github": bool(setup_data.github_token),
                    "jira": bool(setup_data.jira_token),
                    "trello": bool(setup_data.trello_token),
                    "claude": bool(setup_data.claude_api_key),
                },
                setup_complete=True,
            )

    try:
        # 1. Create platform organization if it doesn't exist
        if not existing_org:
            platform_org = Organization(
                name=setup_data.platform_name,
                alias="innoday-platform",
                description="Platform administration organization",
                support_email=setup_data.support_email or setup_data.admin_email,
                billing_email=setup_data.billing_email or setup_data.admin_email,
                website=setup_data.website,
                settings={
                    "integrations": {
                        "github": {"configured": bool(setup_data.github_token)},
                        "jira": {
                            "configured": bool(setup_data.jira_token),
                            "url": setup_data.jira_url,
                            "email": setup_data.jira_email,
                        },
                        "trello": {"configured": bool(setup_data.trello_token)},
                        "claude": {"configured": bool(setup_data.claude_api_key)},
                    }
                },
            )
            session.add(platform_org)
            session.flush()
        else:
            platform_org = existing_org
            # Update settings with integration info
            platform_org.settings["integrations"] = {
                "github": {"configured": bool(setup_data.github_token)},
                "jira": {
                    "configured": bool(setup_data.jira_token),
                    "url": setup_data.jira_url,
                    "email": setup_data.jira_email,
                },
                "trello": {"configured": bool(setup_data.trello_token)},
                "claude": {"configured": bool(setup_data.claude_api_key)},
            }
            if setup_data.support_email:
                platform_org.support_email = setup_data.support_email
            if setup_data.billing_email:
                platform_org.billing_email = setup_data.billing_email
            if setup_data.website:
                platform_org.website = setup_data.website

        # 2. Create or update admin user
        admin_user = session.exec(
            select(User).where(User.email == setup_data.admin_email)
        ).first()

        if not admin_user:
            admin_user = User(
                email=setup_data.admin_email,
                full_name=setup_data.admin_name,
                first_name=(
                    setup_data.admin_name.split()[0]
                    if " " in setup_data.admin_name
                    else setup_data.admin_name
                ),
                last_name=(
                    setup_data.admin_name.split()[-1]
                    if " " in setup_data.admin_name
                    else ""
                ),
                role=UserRole.ADMIN,
                is_platform_member=True,
            )
            session.add(admin_user)
            session.flush()
        else:
            # Update existing user to admin
            admin_user.role = UserRole.ADMIN
            admin_user.is_platform_member = True
            admin_user.full_name = setup_data.admin_name

        # 3. Create platform membership for admin
        existing_membership = session.exec(
            select(OrganizationMembership).where(
                OrganizationMembership.user_id == admin_user.id,
                OrganizationMembership.organization_id == platform_org.id,
            )
        ).first()

        if not existing_membership:
            membership = OrganizationMembership(
                user_id=admin_user.id,
                organization_id=platform_org.id,
                role=OrganizationRole.ADMIN,
                is_owner=True,
                is_active=True,
            )
            session.add(membership)
        else:
            existing_membership.role = OrganizationRole.ADMIN
            existing_membership.is_owner = True
            existing_membership.is_active = True

        # 4. Create platform license if needed
        from src.domain.organization import OrganizationLicense

        platform_tier = session.exec(
            select(LicenseTier).where(LicenseTier.name == "platform_owner")
        ).first()

        if not platform_tier:
            # Create platform owner tier
            platform_tier = LicenseTier(
                name="platform_owner",
                display_name="Platform Owner",
                tier_level=1000,
                max_users=-1,  # Unlimited
                max_developers=-1,
                max_tickets=-1,
                max_boards=-1,
                max_repositories=-1,
                features={"all_features": True},
                price_monthly=0,
                price_yearly=0,
            )
            session.add(platform_tier)
            session.flush()

        # Check for existing license
        existing_license = session.exec(
            select(OrganizationLicense).where(
                OrganizationLicense.organization_id == platform_org.id
            )
        ).first()

        if not existing_license:
            platform_license = OrganizationLicense(
                organization_id=platform_org.id,
                license_tier_id=platform_tier.id,
                status="ACTIVE",
                auto_renew=False,
            )
            session.add(platform_license)

        # 5. Validate integrations (basic checks)
        integrations_valid = {}

        # Note: Actual token validation would require API calls
        # For now, we just check if tokens are provided
        integrations_valid["github"] = bool(setup_data.github_token)
        integrations_valid["jira"] = bool(
            setup_data.jira_token and setup_data.jira_email
        )
        integrations_valid["trello"] = bool(
            setup_data.trello_api_key and setup_data.trello_token
        )
        integrations_valid["claude"] = bool(setup_data.claude_api_key)

        # Commit all changes
        session.commit()
        session.refresh(platform_org)
        session.refresh(admin_user)

        # Generate API key (for now, use user ID)
        api_key = admin_user.id

        return PlatformSetupResponse(
            platform_id=platform_org.id,
            admin_user_id=admin_user.id,
            api_key=api_key,
            platform_name=platform_org.name,
            integrations_configured=integrations_valid,
            setup_complete=True,
        )

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Platform setup failed: {str(e)}",
        )


@router.post(
    "/init",
    dependencies=[Depends(require_team_secret)],
    response_model=PlatformInfoResponse,
    summary="Initialize platform organization",
    description="Initialize the platform organization if it doesn't exist",
    deprecated=True,
)
async def initialize_platform(
    session: Session = Depends(get_session),
    _user: User = Depends(require_platform_access),
):
    """Initialize platform organization (one-time setup) - DEPRECATED: Use /setup instead"""
    # Check if platform organization already exists
    existing = get_platform_organization(session)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Platform organization already exists",
        )

    # Create platform organization
    platform_org = Organization(
        name="InnoDay Platform",
        alias="innoday-platform",
        description="Platform administration organization",
        support_email="hello@havilandsoftware.com",
        billing_email="billing@havilandsoftware.com",
    )

    session.add(platform_org)
    session.commit()
    session.refresh(platform_org)

    # Get platform owner license tier
    from src.domain.license import LicenseTier
    from src.domain.organization import OrganizationLicense

    statement = select(LicenseTier).where(LicenseTier.name == "platform_owner")
    platform_tier = session.exec(statement).first()

    if platform_tier:
        # Create license for platform organization
        platform_license = OrganizationLicense(
            organization_id=platform_org.id,
            license_tier_id=platform_tier.id,
            status="ACTIVE",
            auto_renew=False,
        )
        session.add(platform_license)
        session.commit()

    return PlatformInfoResponse(
        id=platform_org.id,
        name=platform_org.name,
        slug=platform_org.alias,
        description=platform_org.description,
        website=platform_org.website,
        support_email=platform_org.support_email,
        billing_email=platform_org.billing_email,
        created_at=platform_org.created_at.isoformat(),
        updated_at=platform_org.updated_at.isoformat(),
    )


# Health check for platform setup
@router.get(
    "/health",
    summary="Check platform health",
    description="Check if platform is properly configured and healthy",
)
async def check_platform_health(
    detailed: bool = False, session: Session = Depends(get_session)
):
    """Check platform health status with optional integration validation"""
    platform_org = get_platform_organization(session)

    # A real round trip, not an inference. This was the literal `True` with the
    # comment "We're here, so DB is working" -- a check that could not fail, and
    # it rendered as a green tick next to four checks that can, which is worse
    # than not reporting it at all. `all(checks.values())` below now has one
    # member that reflects the database rather than the handler's own liveness.
    try:
        session.exec(text("SELECT 1"))
        database_connection = True
    except Exception:
        database_connection = False

    health_status: Dict[str, Any] = {
        "status": "healthy",
        "checks": {
            "platform_organization": platform_org is not None,
            "platform_configured": False,
            "has_platform_users": False,
            "has_license": False,
            "database_connection": database_connection,
        },
    }

    if platform_org:
        # Check configuration
        health_status["checks"]["platform_configured"] = bool(
            platform_org.support_email
            and platform_org.support_email != "admin@innoday.local"
        )

        # Check for platform users (is_platform_member flag on User)
        from src.domain.user import User as UserModel

        platform_member_count = (
            session.exec(
                select(func.count(UserModel.id)).where(
                    UserModel.is_platform_member == True
                )
            ).first()
            or 0
        )
        health_status["checks"]["has_platform_users"] = platform_member_count > 0

        # Check for license
        from src.domain.organization import OrganizationLicense

        license_exists = (
            session.exec(
                select(OrganizationLicense).where(
                    OrganizationLicense.organization_id == platform_org.id
                )
            ).first()
            is not None
        )
        health_status["checks"]["has_license"] = license_exists

        # Check integrations if detailed flag is set
        if (
            detailed
            and platform_org.settings
            and "integrations" in platform_org.settings
        ):
            health_status["integrations"] = {}
            integrations = platform_org.settings.get("integrations", {})

            # `healthy` is three-valued, matching validate_service_credential's
            # `valid`: True/False are verdicts, **None means nothing was
            # proved**. Nothing here calls the third-party service, so a
            # configured integration reports None -- it previously reported
            # `True` under the comment "Would validate with actual API call",
            # which is a fabricated pass, and the one state an operator most
            # needs to distinguish (configured-but-broken) was the one it hid.
            for integration, config in integrations.items():
                if config.get("configured"):
                    health_status["integrations"][integration] = {
                        "configured": True,
                        "healthy": None,
                        "message": "Configured; not validated against the service",
                    }
                else:
                    health_status["integrations"][integration] = {
                        "configured": False,
                        "healthy": False,
                        "message": "Not configured",
                    }

    # Overall status
    all_checks_pass = all(health_status["checks"].values())
    health_status["status"] = "healthy" if all_checks_pass else "degraded"

    return health_status


# ============================================================================
# Reporting views (platform administrators only)
#
# The underlying views are revoked from anon/authenticated at the database level
# (see alembic 20260804_020000_secure_reporting_views), and the app connects as a
# single `postgres` role that bypasses RLS -- so `require_platform_access` below
# is the boundary that actually holds. Keep that check on every endpoint here.
# ============================================================================


def _read_report_view(session: Session, view: str) -> List[Dict[str, Any]]:
    """Read a reporting view, or 503 if it is not present.

    The views are created by an alembic migration, not by SQLModel metadata, so a
    database that has not been migrated (or the SQLite test harness) simply lacks
    them. A clear 503 beats a raw OperationalError leaking through as a 500.
    """
    try:
        rows = session.exec(text(f"SELECT * FROM {view}")).mappings().all()  # noqa: S608
    except (OperationalError, ProgrammingError):
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                f"Reporting view '{view}' is unavailable — run `alembic upgrade head`."
            ),
        )
    return [dict(r) for r in rows]


@router.get("/reports/project-access", response_model=List[Dict[str, Any]])
async def get_project_access_report(
    _user: User = Depends(require_platform_access),
    session: Session = Depends(get_session),
):
    """Per-project map: org, GitHub config, synced repos, and who can access it.

    Exposes user emails across every organization, hence platform-only.
    """
    return _read_report_view(session, "v_project_access")


@router.get("/reports/user-tokens", response_model=List[Dict[str, Any]])
async def get_user_tokens_report(
    _user: User = Depends(require_platform_access),
    session: Session = Depends(get_session),
):
    """CLI tokens with their owning user.

    `token_hash` is a SHA-256 digest -- the raw token is shown once at mint time
    and never stored, so nothing here can be replayed as a credential.
    """
    return _read_report_view(session, "v_user_tokens")
