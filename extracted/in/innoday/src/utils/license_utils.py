"""
License validation and usage tracking utilities.

This module provides helper functions for license enforcement throughout the application.
It should be used by other modules to check license limits and track usage.

ARCHITECTURE NOTES:
==================
- All license checks go through this module for consistency
- Usage tracking is atomic and handles concurrency
- Functions work with both async and sync contexts
- License validation is cached for performance
"""

from datetime import date, datetime, timedelta, timezone
from typing import Dict, Optional, Tuple

from sqlalchemy import and_, func, select
from sqlmodel import Session

from src.domain.license import LicenseTier, UsageTracking
from src.domain.organization import OrganizationLicense
from src.domain.user import User


class LicenseError(Exception):
    """Base exception for licensing errors"""


class LicenseExpiredError(LicenseError):
    """License has expired"""


class LicenseLimitExceededError(LicenseError):
    """License limit exceeded"""

    def __init__(self, resource: str, limit: int, current: int):
        self.resource = resource
        self.limit = limit
        self.current = current
        super().__init__(f"{resource} limit exceeded: {current}/{limit}")


class FeatureNotAvailableError(LicenseError):
    """Feature not available in current tier"""


def get_client_license_info(
    organization_id: str, session: Session
) -> Optional[Tuple[OrganizationLicense, LicenseTier]]:
    """
    Get active license information for a organization.

    Args:
        organization_id: The client ID
        session: Database session

    Returns:
        Tuple of (OrganizationLicense, LicenseTier) or None if no active license
    """
    result = session.exec(
        select(OrganizationLicense, LicenseTier)
        .join(LicenseTier)
        .where(
            and_(
                OrganizationLicense.organization_id == organization_id,
                OrganizationLicense.status == "ACTIVE",
            )
        )
    ).first()

    return result


def is_license_active(organization_id: str, session: Session) -> bool:
    """
    Check if client has an active license.

    Args:
        organization_id: The client ID
        session: Database session

    Returns:
        True if license is active and not expired
    """
    license_info = get_client_license_info(organization_id, session)
    if not license_info:
        return False

    client_license, _ = license_info
    return client_license.is_active


def check_license_feature(organization_id: str, feature: str, session: Session) -> bool:
    """
    Check if a client's license includes a specific feature.

    Args:
        organization_id: The client ID
        feature: Feature name to check
        session: Database session

    Returns:
        True if feature is available
    """
    license_info = get_client_license_info(organization_id, session)
    if not license_info:
        return False

    _, tier = license_info
    return tier.has_feature(feature)


def validate_user_limit(organization_id: str, session: Session) -> bool:
    """
    Check if client can add more users.

    Args:
        organization_id: The client ID
        session: Database session

    Returns:
        True if user can be added

    Raises:
        LicenseLimitExceededError: If user limit would be exceeded
    """
    license_info = get_client_license_info(organization_id, session)
    if not license_info:
        raise LicenseError("No active license found")

    _, tier = license_info

    # If no limit, always allow
    if tier.max_users is None:
        return True

    # Count current users
    current_users = session.exec(
        select(func.count(User.id)).where(
            User.default_organization_id == organization_id
        )
    ).one()

    if current_users >= tier.max_users:
        raise LicenseLimitExceededError("users", tier.max_users, current_users)

    return True


def validate_board_limit(organization_id: str, session: Session) -> bool:
    """
    Check if client can add more boards.

    Args:
        organization_id: The client ID
        session: Database session

    Returns:
        True if board can be added

    Raises:
        LicenseLimitExceededError: If board limit would be exceeded
    """
    license_info = get_client_license_info(organization_id, session)
    if not license_info:
        raise LicenseError("No active license found")

    _, tier = license_info

    # If no limit, always allow
    if tier.max_boards is None:
        return True

    # Count current boards (placeholder - would need board_registrations table)
    # For now, return True since board registration feature isn't implemented yet
    current_boards = 0  # TODO: Implement when board registration is added

    if current_boards >= tier.max_boards:
        raise LicenseLimitExceededError("boards", tier.max_boards, current_boards)

    return True


def validate_daily_ticket_limit(
    organization_id: str, user_id: str, session: Session
) -> bool:
    """
    Check if user can create more tickets today.

    Args:
        organization_id: The client ID
        user_id: The user ID
        session: Database session

    Returns:
        True if ticket can be created

    Raises:
        LicenseLimitExceededError: If daily ticket limit would be exceeded
    """
    license_info = get_client_license_info(organization_id, session)
    if not license_info:
        raise LicenseError("No active license found")

    _, tier = license_info

    # If no limit, always allow
    if tier.daily_ticket_limit is None:
        return True

    # Get today's ticket count for this user
    today = datetime.now(timezone.utc).date()
    result = session.exec(
        select(func.coalesce(UsageTracking.usage_count, 0)).where(
            and_(
                UsageTracking.organization_id == organization_id,
                UsageTracking.user_id == user_id,
                UsageTracking.usage_type == "ticket_created",
                func.date(UsageTracking.usage_date) == today,
            )
        )
    ).first()
    current_tickets = result[0] if result is not None else 0

    if current_tickets >= tier.daily_ticket_limit:
        raise LicenseLimitExceededError(
            "daily_tickets", tier.daily_ticket_limit, current_tickets
        )

    return True


def validate_container_execution_limit(
    organization_id: str, user_id: str, session: Session
) -> bool:
    """
    Check if user can create a new container execution within license limits.

    Args:
        organization_id: The client ID
        user_id: The user ID
        session: Database session

    Returns:
        True if container execution is allowed

    Raises:
        LicenseLimitExceededError: If container execution limit would be exceeded
    """
    license_info = get_client_license_info(organization_id, session)
    if not license_info:
        raise LicenseError("No active license found")

    _, tier = license_info

    # For now, container executions follow the same limits as daily tickets
    # In the future, we can add specific container execution limits to license tiers
    if tier.daily_ticket_limit is None:
        return True

    # Get today's container execution count for this user
    today = datetime.now(timezone.utc).date()
    result = session.exec(
        select(func.coalesce(UsageTracking.usage_count, 0)).where(
            and_(
                UsageTracking.organization_id == organization_id,
                UsageTracking.user_id == user_id,
                UsageTracking.usage_type == "container_execution",
                func.date(UsageTracking.usage_date) == today,
            )
        )
    ).first()
    current_executions = result[0] if result is not None else 0

    # Use the same limit as daily tickets for container executions
    if current_executions >= tier.daily_ticket_limit:
        raise LicenseLimitExceededError(
            "daily_container_executions", tier.daily_ticket_limit, current_executions
        )

    return True


def validate_api_rate_limit(organization_id: str, session: Session) -> bool:
    """
    Check if client is within API rate limits.

    Args:
        organization_id: The client ID
        session: Database session

    Returns:
        True if API call is allowed

    Raises:
        LicenseLimitExceededError: If API rate limit would be exceeded
    """
    license_info = get_client_license_info(organization_id, session)
    if not license_info:
        raise LicenseError("No active license found")

    _, tier = license_info

    # If no limit, always allow
    if tier.api_rate_limit is None:
        return True

    # Get API calls in the last hour
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    current_calls = session.exec(
        select(func.coalesce(func.sum(UsageTracking.usage_count), 0)).where(
            and_(
                UsageTracking.organization_id == organization_id,
                UsageTracking.usage_type == "api_call",
                UsageTracking.created_at >= one_hour_ago,
            )
        )
    ).one()

    if current_calls >= tier.api_rate_limit:
        raise LicenseLimitExceededError(
            "api_calls_per_hour", tier.api_rate_limit, current_calls
        )

    return True


def track_usage(
    organization_id: str,
    user_id: str,
    usage_type: str,
    session: Session,
    count: int = 1,
) -> bool:
    """
    Track usage for license enforcement.

    Args:
        organization_id: The client ID
        user_id: The user ID
        usage_type: Type of usage (ticket_created, board_synced, api_call)
        session: Database session
        count: Usage count to add (default 1)

    Returns:
        True if successfully tracked
    """
    try:
        today = datetime.now(timezone.utc).date()

        # Try to find existing record for today
        existing = session.exec(
            select(UsageTracking).where(
                and_(
                    UsageTracking.organization_id == organization_id,
                    UsageTracking.user_id == user_id,
                    UsageTracking.usage_type == usage_type,
                    func.date(UsageTracking.usage_date) == today,
                )
            )
        ).first()

        if existing:
            # Handle if existing is returned as a SQLAlchemy Row object
            if hasattr(existing, "_fields"):  # SQLAlchemy Row object
                existing = existing[0]
            elif isinstance(existing, tuple):
                existing = existing[0]

        if existing:
            # Update existing record
            existing.usage_count += count
        else:
            # Create new record
            new_usage = UsageTracking(
                organization_id=organization_id,
                user_id=user_id,
                usage_type=usage_type,
                usage_date=today,
                usage_count=count,
            )
            session.add(new_usage)

        # Note: Commit is removed - caller should handle commit
        return True

    except Exception:
        session.rollback()
        return False


def get_usage_summary(organization_id: str, session: Session, days: int = 30) -> Dict:
    """
    Get usage summary for a client over specified period.

    Args:
        organization_id: The client ID
        session: Database session
        days: Number of days to look back

    Returns:
        Dictionary with usage metrics
    """
    license_info = get_client_license_info(organization_id, session)
    if not license_info:
        return {}

    _, tier = license_info

    # Calculate date range
    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    # Get usage data
    usage_data = {}

    # Users count
    user_count = session.exec(
        select(func.count(User.id)).where(
            User.default_organization_id == organization_id
        )
    ).one()
    usage_data["users"] = {
        "current": user_count,
        "limit": tier.max_users,
        "percentage": (user_count / tier.max_users * 100) if tier.max_users else 0,
    }

    # Tickets created in period
    tickets_created = session.exec(
        select(func.coalesce(func.sum(UsageTracking.usage_count), 0)).where(
            and_(
                UsageTracking.organization_id == organization_id,
                UsageTracking.usage_type == "ticket_created",
                func.date(UsageTracking.usage_date) >= start_date,
                func.date(UsageTracking.usage_date) <= end_date,
            )
        )
    ).one()
    usage_data["tickets_created"] = {
        "current": tickets_created,
        "limit": tier.daily_ticket_limit,
        "period_days": days,
    }

    # API calls in period
    api_calls = session.exec(
        select(func.coalesce(func.sum(UsageTracking.usage_count), 0)).where(
            and_(
                UsageTracking.organization_id == organization_id,
                UsageTracking.usage_type == "api_call",
                func.date(UsageTracking.usage_date) >= start_date,
                func.date(UsageTracking.usage_date) <= end_date,
            )
        )
    ).one()
    usage_data["api_calls"] = {
        "current": api_calls,
        "limit": tier.api_rate_limit,
        "period_days": days,
    }

    return usage_data


TOP_LICENSE_TIER_NAME = "velocity"


def ensure_top_tier_license(
    organization_id: str, session: Session
) -> OrganizationLicense:
    """
    Guarantee an organization has an active license, defaulting to the top tier.

    Business decision: every organization gets Velocity (the top tier) by
    default for now — there is no self-serve tier selection yet, so an org
    with no license is a bug, not an intentional free/limited state. This is
    idempotent: if the org already has an active license, it is returned
    unchanged rather than replaced.

    Callers that need a different tier for a specific test or scenario
    should construct `OrganizationLicense` directly rather than going through
    this helper.
    """
    existing = session.exec(
        select(OrganizationLicense).where(
            and_(
                OrganizationLicense.organization_id == organization_id,
                OrganizationLicense.status == "ACTIVE",
            )
        )
    ).first()
    # session.exec(select(...)) with the SQLAlchemy-imported `select` used in
    # this module can return a Row wrapper rather than the model instance
    # directly (see the same pattern handled in track_usage above).
    if existing is not None and (
        hasattr(existing, "_fields") or isinstance(existing, tuple)
    ):
        existing = existing[0]
    if existing:
        return existing

    tier = session.exec(
        select(LicenseTier).where(LicenseTier.name == TOP_LICENSE_TIER_NAME)
    ).first()
    if tier is not None and (hasattr(tier, "_fields") or isinstance(tier, tuple)):
        tier = tier[0]
    if not tier:
        raise LicenseError(
            f"License tier '{TOP_LICENSE_TIER_NAME}' does not exist — seed license_tiers before creating organizations"
        )

    license_row = OrganizationLicense(
        organization_id=organization_id,
        license_tier_id=tier.id,
        status="ACTIVE",
    )
    session.add(license_row)
    session.commit()
    session.refresh(license_row)
    return license_row


def get_license_tier_name(organization_id: str, session: Session) -> Optional[str]:
    """
    Get the license tier name for a organization.

    Args:
        organization_id: The client ID
        session: Database session

    Returns:
        License tier name or None if no license
    """
    license_info = get_client_license_info(organization_id, session)
    if not license_info:
        return None

    _, tier = license_info
    return tier.name


def requires_license_check(func):
    """
    Decorator to enforce license checking on functions.

    This decorator can be used on functions that need license validation.
    The decorated function must accept organization_id and session parameters.
    """

    def wrapper(*args, **kwargs):
        # Extract organization_id and session from kwargs
        organization_id = kwargs.get("organization_id")
        session = kwargs.get("session")

        if not organization_id or not session:
            raise ValueError(
                "organization_id and session parameters required for license checking"
            )

        # Check if license is active
        if not is_license_active(organization_id, session):
            raise LicenseExpiredError("License is not active or has expired")

        return func(*args, **kwargs)

    return wrapper


# Convenience functions for common license validations
def can_create_ticket(organization_id: str, user_id: str, session: Session) -> bool:
    """Check if user can create a ticket (combines license and daily limit checks)"""
    try:
        if not is_license_active(organization_id, session):
            return False

        validate_daily_ticket_limit(organization_id, user_id, session)
        return True
    except (LicenseError, LicenseLimitExceededError):
        return False


def can_add_user(organization_id: str, session: Session) -> bool:
    """Check if client can add a new user"""
    try:
        if not is_license_active(organization_id, session):
            return False

        validate_user_limit(organization_id, session)
        return True
    except (LicenseError, LicenseLimitExceededError):
        return False


def can_add_board(organization_id: str, session: Session) -> bool:
    """Check if client can add a new board"""
    try:
        if not is_license_active(organization_id, session):
            return False

        validate_board_limit(organization_id, session)
        return True
    except (LicenseError, LicenseLimitExceededError):
        return False


def can_make_api_call(organization_id: str, session: Session) -> bool:
    """Check if client can make an API call (rate limiting)"""
    try:
        if not is_license_active(organization_id, session):
            return False

        validate_api_rate_limit(organization_id, session)
        return True
    except (LicenseError, LicenseLimitExceededError):
        return False
