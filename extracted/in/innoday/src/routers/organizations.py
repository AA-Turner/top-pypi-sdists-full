"""
Organization Management API Router

Provides REST API endpoints for:
- Organization CRUD operations
- Organization membership management
- Organization settings and configuration

Note: Board, ticket, repository, and integration endpoints have been moved to their respective routers.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlmodel import Session, func, select

from src.api.middleware.team_secret import require_team_secret
from src.database import get_session
from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.user import User
from src.middleware.rbac import (
    get_current_user,
    require_org_role,
    resolve_organization,
    verify_org_membership,
)
from src.utils.license_utils import ensure_top_tier_license

router = APIRouter(prefix="/api/v1/organizations", tags=["organizations"])


# ============================================================================
# Helper Functions
# ============================================================================


def is_platform_organization(org: Organization) -> bool:
    """Check if an organization is the platform organization."""
    return org.alias == "platform-admin"


# ============================================================================
# Request/Response Models
# ============================================================================


class OrganizationCreate(BaseModel):
    """Request model for creating an organization"""

    name: str = Field(max_length=100)
    alias: Optional[str] = Field(
        None,
        max_length=50,
        description="Short identifier; auto-derived from name if omitted",
    )
    description: Optional[str] = Field(None, max_length=500)
    website: Optional[str] = Field(None, max_length=200)
    jira_url: Optional[str] = Field(None, max_length=500)
    github_url: Optional[str] = Field(None, max_length=500)
    trello_url: Optional[str] = Field(None, max_length=500)


class OrganizationUpdate(BaseModel):
    """Request model for updating an organization"""

    name: Optional[str] = Field(None, max_length=100)
    alias: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    website: Optional[str] = Field(None, max_length=200)
    jira_url: Optional[str] = Field(None, max_length=500)
    github_url: Optional[str] = Field(None, max_length=500)
    trello_url: Optional[str] = Field(None, max_length=500)
    settings: Optional[Dict[str, Any]] = None


class OrganizationResponse(BaseModel):
    """Response model for organization data.

    `alias` is the sole org identifier. The legacy `slug` response key has been
    removed — clients read `alias`.
    """

    id: str
    name: str
    alias: str
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    jira_url: Optional[str] = None
    github_url: Optional[str] = None
    trello_url: Optional[str] = None
    settings: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime
    is_platform_org: bool = False
    role: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class OrganizationWithStats(OrganizationResponse):
    """Organization response with statistics"""

    member_count: int = 0
    project_count: int = 0
    repository_count: int = 0
    ticket_count: int = 0
    board_count: int = 0


class MembershipCreate(BaseModel):
    """Request model for adding a member to an organization"""

    user_id: str
    #: DEVELOPER, not MEMBER. Adding someone to an organization means they are
    #: going to work in it, and MEMBER cannot: releases, board sync and ticket
    #: writes all require DEVELOPER or higher. The old default produced accounts
    #: that could read everything and change nothing, and the failure surfaced
    #: late and obscurely -- `innoday release` tagged every repository and only
    #: then returned "Requires DEVELOPER role or higher". MEMBER remains
    #: available for genuinely read-only people; it is just no longer the
    #: assumption.
    role: OrganizationRole = OrganizationRole.DEVELOPER


class MembershipUpdate(BaseModel):
    """Request model for updating a membership"""

    role: Optional[OrganizationRole] = None
    is_active: Optional[bool] = None


class MembershipResponse(BaseModel):
    """Response model for organization membership"""

    id: str
    organization_id: str
    user_id: str
    role: OrganizationRole
    is_active: bool
    joined_at: datetime
    updated_at: datetime
    user: Optional["UserResponse"] = None

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    """Basic user response model"""

    id: str
    email: EmailStr
    full_name: Optional[str]
    is_active: bool = True  # User domain model has no is_active; always True

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_user(cls, user: "User") -> "UserResponse":
        return cls(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=True,
        )


# ============================================================================
# Organization CRUD Endpoints
# ============================================================================


@router.get("", response_model=List[OrganizationResponse])
async def list_organizations(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    """
    List all organizations the current user is a member of.

    Returns organizations with basic information.
    """
    # Get organizations user is a member of, along with their role in each
    statement = (
        select(Organization, OrganizationMembership.role)
        .join(OrganizationMembership)
        .where(
            OrganizationMembership.user_id == current_user.id,
            OrganizationMembership.is_active == True,
        )
        .offset(skip)
        .limit(limit)
        .order_by(Organization.name)
    )

    rows = session.exec(statement).all()

    # Add platform org flag and the caller's role
    responses = []
    for org, role in rows:
        org_dict = org.model_dump()
        org_dict["is_platform_org"] = is_platform_organization(org)
        org_dict["role"] = role.value if role else None
        responses.append(OrganizationResponse(**org_dict))

    return responses


@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
    # Tier C: org/user lifecycle — team secret as a second factor.
    dependencies=[Depends(require_team_secret)],
)
async def create_organization(
    organization: OrganizationCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Create a new organization.

    The creating user becomes the owner of the organization.
    """
    # Validate / generate alias
    if organization.alias:
        if session.exec(
            select(Organization).where(Organization.alias == organization.alias)
        ).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Organization with alias '{organization.alias}' already exists",
            )
    else:
        base_alias = Organization.generate_alias(organization.name)
        alias, counter = base_alias, 1
        while session.exec(
            select(Organization).where(Organization.alias == alias)
        ).first():
            alias = f"{base_alias}-{counter}"
            counter += 1
        organization.alias = alias

    # Create organization
    db_organization = Organization(
        id=str(uuid4()),
        **organization.model_dump(),
        settings={},
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    session.add(db_organization)

    # Add creator as owner
    membership = OrganizationMembership(
        id=str(uuid4()),
        organization_id=db_organization.id,
        user_id=current_user.id,
        role=OrganizationRole.ADMIN,
        is_owner=True,
        is_active=True,
        joined_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    session.add(membership)
    session.commit()
    session.refresh(db_organization)

    # Every organization gets an active license by default (top tier for now —
    # see ensure_top_tier_license). Without this, ticket/board/user creation
    # 402s immediately for a brand-new org.
    ensure_top_tier_license(db_organization.id, session)
    # ensure_top_tier_license commits, which expires session-loaded objects.
    session.refresh(db_organization)

    org_dict = db_organization.model_dump()
    org_dict["is_platform_org"] = is_platform_organization(db_organization)

    return OrganizationResponse(**org_dict)


@router.get("/{organization_id}", response_model=OrganizationWithStats)
async def get_organization(
    organization_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """
    Get a specific organization with statistics.
    Accepts UUID or alias as {organization_id}.
    User must be a member of the organization.
    """
    organization = resolve_organization(organization_id, session)

    # Verify membership

    # Get statistics
    from src.domain.board import BoardRegistration
    from src.domain.project import Project
    from src.domain.repository import Repository
    from src.domain.ticket import Ticket

    org_id = organization.id
    member_count = (
        session.exec(
            select(func.count(OrganizationMembership.id)).where(
                OrganizationMembership.organization_id == org_id,
                OrganizationMembership.is_active == True,
            )
        ).first()
        or 0
    )

    project_count = (
        session.exec(
            select(func.count(Project.id)).where(Project.organization_id == org_id)
        ).first()
        or 0
    )

    repository_count = (
        session.exec(
            select(func.count(Repository.id)).where(
                Repository.organization_id == org_id
            )
        ).first()
        or 0
    )

    ticket_count = (
        session.exec(
            select(func.count(Ticket.id)).where(Ticket.organization_id == org_id)
        ).first()
        or 0
    )

    board_count = (
        session.exec(
            select(func.count(BoardRegistration.id)).where(
                BoardRegistration.organization_id == org_id
            )
        ).first()
        or 0
    )

    org_dict = organization.model_dump()
    org_dict["is_platform_org"] = is_platform_organization(organization)
    org_dict["member_count"] = member_count
    org_dict["project_count"] = project_count
    org_dict["repository_count"] = repository_count
    org_dict["ticket_count"] = ticket_count
    org_dict["board_count"] = board_count

    return OrganizationWithStats(**org_dict)


@router.put("/{organization_id}", response_model=OrganizationResponse)
async def update_organization(
    organization_id: str,
    organization_update: OrganizationUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.ADMIN)),
):
    """
    Update an organization. Accepts UUID or alias as {organization_id}.
    Requires ADMIN role. Platform organization cannot be modified.
    """
    organization = resolve_organization(organization_id, session)

    if is_platform_organization(organization):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Platform organization cannot be modified",
        )

    update_data = organization_update.model_dump(exclude_unset=True)

    # Validate alias uniqueness if being changed
    if "alias" in update_data and update_data["alias"] != organization.alias:
        if session.exec(
            select(Organization).where(
                Organization.alias == update_data["alias"],
                Organization.id != organization.id,
            )
        ).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Organization with alias '{update_data['alias']}' already exists",
            )

    for field, value in update_data.items():
        setattr(organization, field, value)

    organization.updated_at = datetime.now(timezone.utc)

    session.add(organization)
    session.commit()
    session.refresh(organization)

    org_dict = organization.model_dump()
    org_dict["is_platform_org"] = is_platform_organization(organization)

    return OrganizationResponse(**org_dict)


@router.delete(
    "/{organization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    # Tier C: org/user lifecycle — team secret as a second factor.
    dependencies=[Depends(require_team_secret)],
)
async def delete_organization(
    organization_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Delete an organization. Accepts UUID or alias as {organization_id}.
    Requires OWNER privileges (is_owner=True).
    Platform organization cannot be deleted.
    """
    organization = resolve_organization(organization_id, session)

    if is_platform_organization(organization):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Platform organization cannot be deleted",
        )

    # Deliberately NOT a Depends(require_org_role(...)): this needs the
    # OrganizationMembership itself to read `is_owner`, and require_org_role returns
    # the Organization. Ownership is a flag on the membership, not a role, so the
    # rank ordering can't express it.
    membership = verify_org_membership(current_user.id, organization.id, session)
    if not membership.is_owner and not current_user.is_platform_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Organization deletion requires owner privileges",
        )

    # Cascade-delete in FK dependency order (children before parents)
    from src.services.organization_cascade import delete_organization_cascade

    delete_organization_cascade(session, organization.id)

    session.delete(organization)
    session.commit()


# ============================================================================
# Organization Membership Endpoints
# ============================================================================


@router.get("/{organization_id}/members", response_model=List[MembershipResponse])
async def list_organization_members(
    organization_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    is_active: Optional[bool] = Query(True),
    role: Optional[OrganizationRole] = Query(None),
    _org: Organization = Depends(require_org_role()),
):
    """
    List members of an organization.

    User must be a member of the organization.
    """
    # Verify organization exists
    resolve_organization(organization_id, session)

    # Verify membership

    # Build query
    statement = select(OrganizationMembership).where(
        OrganizationMembership.organization_id == organization_id
    )

    if is_active is not None:
        statement = statement.where(OrganizationMembership.is_active == is_active)

    if role:
        statement = statement.where(OrganizationMembership.role == role)

    memberships = session.exec(
        statement.order_by(OrganizationMembership.joined_at.desc())
    ).all()

    # Load user data
    responses = []
    for membership in memberships:
        user = session.get(User, membership.user_id)
        membership_dict = membership.model_dump()
        if user:
            membership_dict["user"] = UserResponse.from_user(user)
        responses.append(MembershipResponse(**membership_dict))

    return responses


@router.post(
    "/{organization_id}/members",
    response_model=MembershipResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_organization_member(
    organization_id: str,
    membership: MembershipCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.ADMIN)),
):
    """
    Add a member to an organization.

    Requires ADMIN role.
    """
    # Verify organization exists
    resolve_organization(organization_id, session)

    # Verify admin/owner membership

    # Check if user exists
    user = session.get(User, membership.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Check if already a member
    existing = session.exec(
        select(OrganizationMembership).where(
            OrganizationMembership.organization_id == organization_id,
            OrganizationMembership.user_id == membership.user_id,
        )
    ).first()

    if existing:
        if existing.is_active:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User is already a member",
            )
        else:
            # Reactivate membership
            existing.is_active = True
            existing.role = membership.role
            existing.updated_at = datetime.now(timezone.utc)
            session.add(existing)
            session.commit()
            session.refresh(existing)

            membership_dict = existing.model_dump()
            membership_dict["user"] = UserResponse.from_user(user)
            return MembershipResponse(**membership_dict)

    # Create new membership
    db_membership = OrganizationMembership(
        id=str(uuid4()),
        organization_id=organization_id,
        user_id=membership.user_id,
        role=membership.role,
        is_active=True,
        joined_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    session.add(db_membership)
    session.commit()
    session.refresh(db_membership)

    membership_dict = db_membership.model_dump()
    membership_dict["user"] = UserResponse.from_user(user)

    return MembershipResponse(**membership_dict)


@router.put(
    "/{organization_id}/members/{user_id}",
    response_model=MembershipResponse,
)
async def update_organization_member(
    organization_id: str,
    user_id: str,
    membership_update: MembershipUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Update a member's role or status in an organization.

    Requires ADMIN role.
    Cannot modify your own role if you're the only owner.
    """
    # Verify organization exists
    resolve_organization(organization_id, session)

    # Deliberately inline: the caller's own membership is needed below to compare
    # against the target's, which a Depends(require_org_role(...)) returning the
    # Organization cannot supply.
    current_membership = verify_org_membership(
        current_user.id, organization_id, session, OrganizationRole.ADMIN
    )

    # Get target membership
    target_membership = session.exec(
        select(OrganizationMembership).where(
            OrganizationMembership.organization_id == organization_id,
            OrganizationMembership.user_id == user_id,
        )
    ).first()

    if not target_membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found",
        )

    # Prevent the only owner from demoting themselves
    if user_id == current_user.id and current_membership.is_owner:
        owner_count = (
            session.exec(
                select(func.count(OrganizationMembership.id)).where(
                    OrganizationMembership.organization_id == organization_id,
                    OrganizationMembership.is_owner == True,
                    OrganizationMembership.is_active == True,
                )
            ).first()
            or 0
        )

        if owner_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove the only owner",
            )

    # Update membership
    update_data = membership_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(target_membership, field, value)

    target_membership.updated_at = datetime.now(timezone.utc)

    session.add(target_membership)
    session.commit()
    session.refresh(target_membership)

    # Load user data
    user = session.get(User, target_membership.user_id)
    membership_dict = target_membership.model_dump()
    if user:
        membership_dict["user"] = UserResponse.from_user(user)

    return MembershipResponse(**membership_dict)


@router.delete(
    "/{organization_id}/members/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_organization_member(
    organization_id: str,
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Remove a member from an organization.

    Requires ADMIN role.
    Cannot remove the only owner.
    Users can remove themselves unless they're the only owner.
    """
    # Verify organization exists
    resolve_organization(organization_id, session)

    # Get target membership
    target_membership = session.exec(
        select(OrganizationMembership).where(
            OrganizationMembership.organization_id == organization_id,
            OrganizationMembership.user_id == user_id,
        )
    ).first()

    if not target_membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found",
        )

    # Deliberately NOT a Depends(require_org_role(...)): the requirement is
    # conditional on *who* is being removed, and a dependency always runs. Removing
    # someone else needs ADMIN; removing yourself needs only membership. Converting
    # this would either demand ADMIN to leave an org, or let any member remove
    # anyone.
    if user_id != current_user.id:
        verify_org_membership(
            current_user.id, organization_id, session, OrganizationRole.ADMIN
        )
    else:
        verify_org_membership(current_user.id, organization_id, session)

    # Prevent removing the only owner
    if target_membership.is_owner:
        owner_count = (
            session.exec(
                select(func.count(OrganizationMembership.id)).where(
                    OrganizationMembership.organization_id == organization_id,
                    OrganizationMembership.is_owner == True,
                    OrganizationMembership.is_active == True,
                )
            ).first()
            or 0
        )

        if owner_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove the only owner",
            )

    # Soft delete (deactivate) the membership
    target_membership.is_active = False
    target_membership.updated_at = datetime.now(timezone.utc)

    session.add(target_membership)
    session.commit()
