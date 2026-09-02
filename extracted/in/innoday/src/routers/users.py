"""
User Management API Router for InnoDay Platform

This module provides RESTful endpoints for user profile management,
integration status tracking, and user authentication state.

CLI INTEGRATION EXPECTATIONS:
============================

The CLI tool should interact with these endpoints as follows:

1. ONBOARDING WORKFLOW:
   - CLI creates user profile via POST /api/v1/users
   - CLI updates integration status via PUT /api/v1/users/{id}/integrations
   - CLI retrieves profile for display via GET /api/v1/users/{id}

2. TOKEN MANAGEMENT PATTERN:
   - CLI stores API tokens securely (outside this system)
   - CLI tests token validity before updating integration status
   - CLI sets connected=False when tokens expire/revoked
   - Agent uses integration status to determine available operations

3. CLI COMMANDS:
   **There is no `innoday user` command, and there never has been.** This block
   listed four of them as "expected... for reference"; they were a sketch of an
   interface nobody built, and reading them as real is how somebody ends up
   debugging why `innoday user status` is not recognised. What exists:
   - `innoday init` -- create the local identity and write ~/.innoday/config.json
   - `innoday whoami` / `innoday config show` -- who this install is
   - `innoday auth identity --set <handle> --platform <p>` -- map a board handle
     to yourself on the current project
   Creating a user *for someone else* is `scripts/bootstrap_cli.py seed-user`,
   deliberately not a CLI command (see CLAUDE.md).

4. AUTHENTICATION FLOW:
   - CLI handles user authentication (OAuth, API keys, etc.)
   - CLI calls POST /api/v1/users/{id}/login to update session tracking
   - Agent uses last_login_at for user activity monitoring
"""

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlmodel import Session, select

from src.api.middleware.team_secret import require_team_secret
from src.database import get_session
from src.domain.user import User, UserRole
from src.middleware.rbac import get_admin_user, get_authenticated_user, get_current_user
from src.services.user_provisioning import UserProvisioningError, provision_user

logger = logging.getLogger(__name__)

# UserProvisioningError.reason -> HTTP status. 503 is an operator problem,
# 502 is Supabase refusing, 409 is a duplicate address.
_PROVISIONING_STATUS = {
    "not_configured": status.HTTP_503_SERVICE_UNAVAILABLE,
    "upstream": status.HTTP_502_BAD_GATEWAY,
    "duplicate": status.HTTP_409_CONFLICT,
}

router = APIRouter(prefix="/api/v1", tags=["users"])


# Pydantic models for request/response
class UserCreate(BaseModel):
    """Model for creating a new user"""

    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=1000)
    timezone: str = Field(default="UTC", max_length=50)
    language: str = Field(default="en", max_length=10)
    role: UserRole = Field(default=UserRole.MEMBER)

    # Platform member flag (Phase 1: Deprecate Client Concept)
    is_platform_member: bool = Field(default=False)


class UserUpdate(BaseModel):
    """Model for updating user information"""

    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=1000)
    avatar_url: Optional[str] = Field(None, max_length=500)
    timezone: Optional[str] = Field(None, max_length=50)
    language: Optional[str] = Field(None, max_length=10)


class IntegrationUpdate(BaseModel):
    """
    Model for updating external service integration status.

    This model manages the connection metadata for external services (GitHub, Trello, Jira)
    without storing sensitive authentication tokens. The CLI or other clients should:

    1. Store API tokens/credentials securely outside this system
    2. Test connectivity with those tokens
    3. Update integration status via this model to inform the agent of available services

    Purpose:
    - Validates service names to prevent typos
    - Groups related metadata fields for atomic updates
    - Provides clear API contract for integration management
    - Enables the agent to know which operations are available per user

    Usage Example:
    ```python
    # After CLI successfully connects to GitHub with a token
    integration_update = IntegrationUpdate(
        service="github",
        connected=True,
        username="johndoe"
    )
    # POST /api/v1/users/{user_id}/integrations
    ```

    Security Note:
    - Never include actual API tokens or passwords in this model
    - Only connection status and public metadata is stored
    """

    service: str = Field(
        ...,
        pattern=r"^(github|trello|jira)$",
        description="Service name - must be one of: github, trello, jira",
    )
    connected: bool = Field(
        ..., description="Whether the service is currently connected and accessible"
    )
    username: Optional[str] = Field(
        None,
        description="Public username/identifier for the service (e.g., GitHub username)",
    )
    instance_url: Optional[str] = Field(
        None, description="For Jira: the instance URL (e.g., 'company.atlassian.net')"
    )
    email: Optional[str] = Field(
        None, description="For Jira: the email address associated with the account"
    )


class UserResponse(BaseModel):
    """Response model for user data (no sensitive information)"""

    id: str
    email: str
    full_name: str
    bio: Optional[str]
    avatar_url: Optional[str]
    timezone: str
    language: str
    role: UserRole

    # Platform member flag (Phase 1: Deprecate Client Concept)
    is_platform_member: bool

    # Integration status (metadata only, no tokens)
    github_connected: bool
    github_username: Optional[str]
    jira_connected: bool
    jira_instance_url: Optional[str]
    jira_email: Optional[str]

    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime]


class IntegrationStatusResponse(BaseModel):
    """Response model for integration status"""

    github: Dict[str, bool | str | None]
    jira: Dict[str, bool | str | None]


# User CRUD endpoints
@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    # Explicit route-level team-secret gate (defense-in-depth on top of
    # TeamSecretMiddleware) — guarantees the shared dev/deployed API can't
    # create users without the team secret even if the global middleware's
    # config or exemptions ever changed. No-op locally (TEAM_ACCESS_SECRET
    # unset). See src/api/middleware/team_secret.py.
    dependencies=[Depends(require_team_secret)],
)
async def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_authenticated_user),
):
    """
    Create a new user profile (locked down — auth P4, PF-350).

    This is no longer an anonymous endpoint. Ordinary users are created
    implicitly: via invite-accept (lazy Supabase mirror) or by creating an org.
    Direct creation is reserved for platform staff (operator/seeding actions).

    Args:
        user_data: User creation data
        session: Database session
        current_user: The authenticated caller (must be a platform member)

    Returns:
        Created user profile (without sensitive data)

    Raises:
        HTTPException: If the caller isn't a platform member, or email exists
    """
    if not current_user.is_platform_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Direct user creation is restricted to platform staff. "
            "Ordinary users are created via invite-accept or org creation.",
        )
    # Provisioning lives in a service because the signup-approval path
    # (src/routers/webui/routes.py) must create users the identical way. The
    # ordering it enforces -- Supabase identity first, refuse rather than leave
    # an identity-less row -- is the part that must not be reimplemented.
    try:
        provisioned = provision_user(
            session,
            email=user_data.email,
            full_name=user_data.full_name,
            role=user_data.role,
            is_platform_member=user_data.is_platform_member,
            bio=user_data.bio,
            timezone=user_data.timezone,
            language=user_data.language,
        )
        return provisioned.user
    except UserProvisioningError as exc:
        raise HTTPException(
            status_code=_PROVISIONING_STATUS[exc.reason], detail=str(exc)
        )
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}",
        )


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Get user profile by ID.

    Args:
        user_id: User ID
        session: Database session

    Returns:
        User profile (without sensitive data)

    Raises:
        HTTPException: If user not found
    """
    try:
        logger.info(f"Fetching user: {user_id}")

        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found",
            )

        return user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch user: {str(e)}",
        )


@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    limit: int = 100,
    offset: int = 0,
    admin_user: User = Depends(get_admin_user),
    session: Session = Depends(get_session),
):
    """
    Get all users with pagination (admin only).

    Args:
        limit: Maximum number of users to return
        offset: Number of users to skip
        admin_user: Authenticated admin user
        session: Database session

    Returns:
        List of user profiles
    """
    try:
        logger.info(
            f"Admin {admin_user.id} fetching users with limit={limit}, offset={offset}"
        )

        users = session.exec(select(User).offset(offset).limit(limit)).all()

        return users

    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch users: {str(e)}",
        )


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Update user profile.

    Args:
        user_id: User ID
        user_data: Updated user data
        session: Database session

    Returns:
        Updated user profile

    Raises:
        HTTPException: If user not found
    """
    try:
        logger.info(f"Updating user: {user_id}")

        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found",
            )

        # Update fields if provided
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        user.updated_at = datetime.now(timezone.utc)

        session.add(user)
        session.commit()
        session.refresh(user)

        logger.info(f"Updated user {user_id}")
        return user

    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}",
        )


@router.delete(
    "/users/{user_id}",
    # Tier C: user lifecycle — team secret as a second factor.
    dependencies=[Depends(require_team_secret)],
)
async def delete_user(
    user_id: str,
    admin_user: User = Depends(get_admin_user),
    session: Session = Depends(get_session),
):
    """
    Delete user profile (admin only).

    Args:
        user_id: User ID
        admin_user: Authenticated admin user
        session: Database session

    Returns:
        Success message

    Raises:
        HTTPException: If user not found
    """
    try:
        logger.info(f"Admin {admin_user.id} deleting user: {user_id}")

        # Prevent self-deletion
        if user_id == admin_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete your own account",
            )

        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found",
            )

        session.delete(user)
        session.commit()

        logger.info(f"Admin {admin_user.id} deleted user {user_id}")
        return {"message": f"User {user_id} deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}",
        )


# Integration management endpoints
@router.get("/users/{user_id}/integrations", response_model=IntegrationStatusResponse)
async def get_user_integrations(
    user_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Get user's integration status (metadata only, no sensitive tokens).

    Args:
        user_id: User ID
        session: Database session

    Returns:
        Integration status for all services

    Raises:
        HTTPException: If user not found
    """
    try:
        logger.info(f"Fetching integration status for user: {user_id}")

        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found",
            )

        return IntegrationStatusResponse(**user.get_integration_status())

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching integrations for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch user integrations: {str(e)}",
        )


@router.put("/users/{user_id}/integrations")
async def update_user_integration(
    user_id: str,
    integration_data: IntegrationUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Update user integration status.

    Args:
        user_id: User ID
        integration_data: Integration update data
        session: Database session

    Returns:
        Success message

    Raises:
        HTTPException: If user not found
    """
    try:
        logger.info(
            f"Updating {integration_data.service} integration for user: {user_id}"
        )

        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found",
            )

        user.update_integration_status(
            service=integration_data.service,
            connected=integration_data.connected,
            username=integration_data.username,
            instance_url=integration_data.instance_url,
            email=integration_data.email,
        )

        session.add(user)
        session.commit()

        logger.info(
            f"Updated {integration_data.service} integration for user {user_id}"
        )
        return {
            "message": f"{integration_data.service.title()} integration updated successfully",
            "service": integration_data.service,
            "connected": integration_data.connected,
        }

    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating integration for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update integration: {str(e)}",
        )


@router.post("/users/{user_id}/login")
async def update_last_login(
    user_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Update user's last login timestamp.

    Args:
        user_id: User ID
        session: Database session

    Returns:
        Success message

    Raises:
        HTTPException: If user not found
    """
    try:
        logger.info(f"Updating last login for user: {user_id}")

        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found",
            )

        user.update_last_login()
        session.add(user)
        session.commit()

        logger.info(f"Updated last login for user {user_id}")
        return {
            "message": "Last login updated successfully",
            "last_login_at": user.last_login_at.isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating last login for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update last login: {str(e)}",
        )


# Admin-only user management endpoints
@router.put("/users/{user_id}/role", response_model=UserResponse)
async def update_user_role(
    user_id: str,
    new_role: UserRole,
    admin_user: User = Depends(get_admin_user),
    session: Session = Depends(get_session),
):
    """
    Update user role (admin only).

    Args:
        user_id: User ID
        new_role: New role to assign
        admin_user: Authenticated admin user
        session: Database session

    Returns:
        Updated user profile

    Raises:
        HTTPException: If user not found or trying to change own role
    """
    try:
        logger.info(f"Admin {admin_user.id} updating role for user: {user_id}")

        # Prevent changing own role
        if user_id == admin_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot change your own role",
            )

        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found",
            )

        old_role = user.role
        user.role = new_role
        user.updated_at = datetime.now(timezone.utc)

        session.add(user)
        session.commit()
        session.refresh(user)

        logger.info(
            f"Admin {admin_user.id} updated user {user_id} role from {old_role} to {new_role}"
        )
        return user

    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating role for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user role: {str(e)}",
        )
