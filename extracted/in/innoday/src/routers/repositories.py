"""
Consolidated Repository Management API Router

Provides REST API endpoints for:
- Repository CRUD operations
- GitHub/GitLab repository registration and discovery
- Repository issue synchronization
- Project repository associations
- GitHub organization registration and sync

This router consolidates functionality from:
- repositories.py (base CRUD)
- git_registrations.py (Git platform registration)
- repository_issues.py (issue synchronization)
- github.py (GitHub org registration)
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
    Query,
    status,
)
from pydantic import BaseModel, ConfigDict, Field
from sqlmodel import Session, select

from src.database import get_session
from src.domain import (
    GitHubOrgRegistration,
    GitHubSyncHistory,
    Organization,
    OrganizationRole,
    ProjectRepository,
    Repository,
    RepositoryIssue,
    RepositoryLayer,
    User,
)
from src.middleware.rbac import (
    conflict,
    get_current_user,
    not_found,
    require_org_role,
    resolve_organization,
)
from src.routers.projects import resolve_project
from src.services.github_issue_sync import GitHubIssueSyncService
from src.services.org_credential_service import get_github_credentials

logger = logging.getLogger(__name__)

# Initialize router with unified API prefix
router = APIRouter(prefix="/api/v1", tags=["repositories"])


# ============================================================================
# Request/Response Models
# ============================================================================


# Repository Models
class RepositoryBase(BaseModel):
    """Base repository model"""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    url: Optional[str] = None
    github_url: Optional[str] = None
    full_name: Optional[str] = None
    is_private: bool = False
    language: Optional[str] = None
    technologies: List[str] = []
    is_active: bool = True
    external_id: Optional[str] = None
    layer: Optional[RepositoryLayer] = None


class RepositoryCreate(RepositoryBase):
    """Request model for creating a repository"""


class RepositoryUpdate(BaseModel):
    """Request model for updating a repository"""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    url: Optional[str] = None
    github_url: Optional[str] = None
    is_private: Optional[bool] = None
    language: Optional[str] = None
    technologies: Optional[List[str]] = None
    is_active: Optional[bool] = None
    layer: Optional[RepositoryLayer] = None


class RepositoryResponse(BaseModel):
    """Response model for repository data"""

    id: str
    organization_id: str
    name: str
    description: Optional[str]
    url: Optional[str]
    github_url: Optional[str]
    full_name: Optional[str]
    is_private: bool
    language: Optional[str]
    technologies: List[str]
    is_active: bool
    external_id: Optional[str]
    layer: Optional[RepositoryLayer]
    stars: int
    forks: int
    open_issues_count: int
    archived: bool
    archived_at: Optional[datetime]
    deleted: bool
    deleted_at: Optional[datetime]
    last_synced_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Issue Models
class IssueSyncRequest(BaseModel):
    """Request model for syncing repository issues"""

    state_filter: str = Field(
        default="all", description="Issue state filter", pattern="^(open|closed|all)$"
    )
    since: Optional[datetime] = Field(
        default=None, description="Only sync issues updated after this date"
    )
    dry_run: bool = Field(
        default=False, description="Preview sync without making changes"
    )


class IssueSyncResponse(BaseModel):
    """Response model for issue sync operations"""

    success: bool
    message: str
    statistics: Dict[str, int]
    errors: List[str] = []
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None


class RepositoryIssueResponse(BaseModel):
    """Response model for repository issues"""

    id: str
    github_issue_id: int
    repository_id: str
    title: str
    body: Optional[str]
    is_open: bool
    github_url: str
    github_created_at: datetime
    github_updated_at: datetime
    created_at: datetime
    updated_at: datetime
    last_synced_at: datetime

    model_config = ConfigDict(from_attributes=True)


# RepositoryDiscoveryRequest / RepositoryImportRequest lived here as the bodies of
# the two org-scoped 501 stubs. Both were removed with them — the real
# discovery/import routes are project-scoped (routers/projects.py) and carry their
# own request models.


# GitHub Organization Models
class GitHubOrgRegistrationCreate(BaseModel):
    """Request model for creating a GitHub organization registration."""

    organization_id: str = Field(description="Organization UUID to associate with")
    organization: str = Field(description="GitHub organization name")
    sync_readme: bool = Field(
        default=True, description="Whether to sync README content"
    )
    sync_interval_minutes: int = Field(
        default=60,
        ge=15,
        le=1440,
        description="Sync interval in minutes (15 min to 24 hours)",
    )


class GitHubOrgRegistrationResponse(BaseModel):
    """Response model for GitHub organization registration."""

    id: str
    user_id: str
    organization_id: str
    organization: str
    sync_enabled: bool
    sync_readme: bool
    sync_interval_minutes: int
    status: str
    last_error: Optional[str]
    last_sync_at: Optional[datetime]
    last_sync_repos_count: Optional[int]
    total_repos_count: Optional[int]
    created_at: datetime
    updated_at: datetime


class GitHubOrgRegistrationUpdate(BaseModel):
    """Request model for updating a GitHub organization registration."""

    sync_enabled: Optional[bool] = None
    sync_readme: Optional[bool] = None
    sync_interval_minutes: Optional[int] = Field(None, ge=15, le=1440)


class SyncHistoryResponse(BaseModel):
    """One repository-sync attempt, as `GET .../repositories/sync-history` returns it.

    **One grain: a project.** Every row is one topic-discovery run against one
    project's repositories (`GitHubConnectService._record_sync_history`), so the
    counts on any two rows are comparable. They were not before #658: the table
    also held rows from an org-wide registration sync that counted every
    repository the registration reached, so an org-wide 40 and a project 8
    interleaved in one list read as 32 repositories vanishing.

    Both keys stay on the wire even though the route now filters by project: a
    caller reading a list still has to know which tenant and project it belongs
    to without holding the request that produced it.
    """

    id: str
    #: The tenant. NULL only on a legacy row written before #650.
    organization_id: Optional[str] = None
    #: The project whose repositories this attempt covered. NULL only on a legacy
    #: row: it predates #650, or it came from the org-wide sync #658 deleted.
    project_id: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime]
    status: str
    repositories_synced: int
    repositories_created: int
    repositories_updated: int
    repositories_failed: int
    readmes_synced: int
    error_message: Optional[str]
    duration_seconds: Optional[float]
    api_calls_made: Optional[int]


# ============================================================================
# Repository CRUD Endpoints
# ============================================================================


@router.post(
    "/organizations/{organization_id}/repositories",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_repository(
    organization_id: str,
    repository: RepositoryCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """Create a new repository"""
    # Verify organization exists and user has access
    org = resolve_organization(organization_id, session)

    # Check for duplicate
    existing = session.exec(
        select(Repository).where(
            Repository.organization_id == organization_id,
            Repository.name == repository.name,
        )
    ).first()

    if existing:
        raise conflict("Repository", repository.name)

    # Create repository
    repo_data = repository.model_dump()
    # Ensure full_name is set (required field in DB)
    if not repo_data.get("full_name"):
        # If full_name not provided, construct it from org and repo name
        repo_data["full_name"] = f"{org.name}/{repository.name}"

    db_repository = Repository(
        id=str(uuid4()),
        organization_id=organization_id,
        **repo_data,
    )

    session.add(db_repository)
    session.commit()
    session.refresh(db_repository)

    logger.info(
        f"Created repository {db_repository.id} for organization {organization_id}"
    )
    return db_repository


@router.get(
    "/organizations/{organization_id}/repositories",
    response_model=List[RepositoryResponse],
)
async def list_repositories(
    organization_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    refresh: bool = Query(False, description="Refresh from GitHub before returning"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    layer: Optional[RepositoryLayer] = Query(None, description="Filter by layer"),
    language: Optional[str] = Query(None, description="Filter by language"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=500, description="Number of items to retrieve"),
    _org: Organization = Depends(require_org_role()),
):
    """List repositories for an organization. Pass ?refresh=true to pull latest state from GitHub."""
    from src.api.github_api import GitHubAPI

    org = resolve_organization(organization_id, session)

    if refresh:
        # Vault, same as every other GitHub read. This used to be the one
        # keyring-backed GitHub call left, so the same org could look connected
        # here and unconnected on the sync endpoint (or vice versa).
        creds = get_github_credentials(session, org.id)
        if not creds:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"No GitHub credentials found for organization '{org.alias}'. Connect GitHub first.",
            )
        github_api = GitHubAPI(creds["token"])
        github_org = creds["github_org"]

        try:
            remote_repos = await github_api.get_all_organization_repositories(
                github_org
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"GitHub fetch failed: {e}",
            )

        now = datetime.now(timezone.utc)
        remote_ids = set()

        for raw in remote_repos:
            parsed = github_api.parse_repository_data(raw)
            remote_ids.add(parsed["id"])
            topics = raw.get("topics", [])

            existing = session.get(Repository, parsed["id"])
            if existing:
                existing.name = parsed["name"]
                existing.full_name = parsed["full_name"]
                existing.url = parsed["url"]
                existing.description = parsed.get("description")
                existing.language = parsed.get("language")
                existing.stars = parsed.get("stars", 0)
                existing.forks = parsed.get("forks", 0)
                existing.open_issues_count = parsed.get("open_issues_count", 0)
                existing.is_private = parsed.get("is_private", False)
                existing.github_updated_at = parsed.get("github_updated_at")
                # Track archive state transitions
                if parsed.get("archived") and not existing.archived:
                    existing.archived_at = now
                existing.archived = parsed.get("archived", False)
                existing.last_synced_at = now
                existing.updated_at = now
                session.add(existing)
            else:
                from src.services.github_connect_service import GitHubConnectService

                detected_layer = GitHubConnectService(session).detect_repository_layer(
                    repo_name=parsed["name"],
                    primary_language=parsed.get("language"),
                    topics=topics,
                )
                repo = Repository(
                    id=parsed["id"],
                    organization_id=organization_id,
                    name=parsed["name"],
                    full_name=parsed["full_name"],
                    url=parsed["url"],
                    description=parsed.get("description"),
                    language=parsed.get("language"),
                    stars=parsed.get("stars", 0),
                    forks=parsed.get("forks", 0),
                    open_issues_count=parsed.get("open_issues_count", 0),
                    is_private=parsed.get("is_private", False),
                    archived=parsed.get("archived", False),
                    archived_at=now if parsed.get("archived") else None,
                    layer=detected_layer.value,
                    github_created_at=parsed.get("github_created_at"),
                    github_updated_at=parsed.get("github_updated_at"),
                    last_synced_at=now,
                )
                session.add(repo)

        # Mark repos no longer on GitHub as deleted
        existing_repos = session.exec(
            select(Repository).where(Repository.organization_id == organization_id)
        ).all()
        for repo in existing_repos:
            if repo.id not in remote_ids and not repo.deleted:
                repo.deleted = True
                repo.deleted_at = now
                repo.updated_at = now
                session.add(repo)

        session.commit()

    query = select(Repository).where(Repository.organization_id == organization_id)
    if is_active is not None:
        query = query.where(Repository.is_active == is_active)
    if layer:
        query = query.where(Repository.layer == layer)
    if language:
        query = query.where(Repository.language == language)

    return session.exec(query.offset(skip).limit(limit).order_by(Repository.name)).all()


@router.get(
    "/organizations/{organization_id}/repositories/{repository_id}",
    response_model=RepositoryResponse,
)
async def get_repository(
    organization_id: str,
    repository_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """Get a specific repository"""
    # Verify organization exists and user has access
    resolve_organization(organization_id, session)

    # Get repository
    repository = session.exec(
        select(Repository).where(
            Repository.id == repository_id,
            Repository.organization_id == organization_id,
        )
    ).first()

    if not repository:
        raise not_found("Repository", repository_id)

    return repository


@router.put(
    "/organizations/{organization_id}/repositories/{repository_id}",
    response_model=RepositoryResponse,
)
async def update_repository(
    organization_id: str,
    repository_id: str,
    repository_update: RepositoryUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """Update a repository"""
    # Verify organization exists and user has access
    resolve_organization(organization_id, session)

    # Get repository
    repository = session.exec(
        select(Repository).where(
            Repository.id == repository_id,
            Repository.organization_id == organization_id,
        )
    ).first()

    if not repository:
        raise not_found("Repository", repository_id)

    # Update repository
    update_data = repository_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(repository, field, value)

    repository.updated_at = datetime.now(timezone.utc)

    session.add(repository)
    session.commit()
    session.refresh(repository)

    logger.info(f"Updated repository {repository_id}")
    return repository


@router.delete(
    "/organizations/{organization_id}/repositories/{repository_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_repository(
    organization_id: str,
    repository_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role(OrganizationRole.ADMIN)),
):
    """Delete a repository"""
    # Verify organization exists and user has admin access
    resolve_organization(organization_id, session)

    # Get repository
    repository = session.exec(
        select(Repository).where(
            Repository.id == repository_id,
            Repository.organization_id == organization_id,
        )
    ).first()

    if not repository:
        raise not_found("Repository", repository_id)

    # Delete repository
    session.delete(repository)
    session.commit()

    logger.info(f"Deleted repository {repository_id}")


# Repository discovery/import live on the PROJECT-scoped routes in
# routers/projects.py (`.../projects/{project_id}/repositories/{discover,import}`)
# — that is what the CLI calls. Org-scoped duplicates used to sit here returning
# 501 "temporarily unavailable during API reorganization"; they were removed, since
# an endpoint that only ever 501s is worse than no endpoint (it advertises itself
# in the OpenAPI schema as though it worked).


# ============================================================================
# Issue Synchronization Endpoints
# ============================================================================


@router.post(
    "/organizations/{organization_id}/repositories/{repository_id}/sync-issues",
    response_model=IssueSyncResponse,
)
async def sync_repository_issues(
    organization_id: str,
    repository_id: str,
    request: IssueSyncRequest,
    x_github_token: str = Header(..., description="GitHub access token"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """Sync GitHub issues for a specific repository"""
    # Verify organization exists and user has access
    resolve_organization(organization_id, session)

    # Validate repository exists and belongs to organization
    repository = session.exec(
        select(Repository).where(
            Repository.id == repository_id,
            Repository.organization_id == organization_id,
        )
    ).first()

    if not repository:
        raise not_found("Repository", repository_id)

    # Initialize sync service
    sync_service = GitHubIssueSyncService(session)

    start_time = datetime.now(timezone.utc)

    try:
        # Perform sync
        stats = await sync_service.sync_repository_issues(
            repository_id=repository.id,
            token=x_github_token,
            state_filter=request.state_filter,
            since=request.since,
            dry_run=request.dry_run,
        )

        end_time = datetime.now(timezone.utc)
        duration = (end_time - start_time).total_seconds()

        return IssueSyncResponse(
            success=True,
            message=f"Successfully synced issues for repository {repository.name}",
            statistics=stats,
            errors=[],
            started_at=start_time,
            completed_at=end_time,
            duration_seconds=duration,
        )

    except Exception as e:
        logger.error(f"Issue sync failed for repository {repository_id}: {e}")
        end_time = datetime.now(timezone.utc)
        duration = (end_time - start_time).total_seconds()

        return IssueSyncResponse(
            success=False,
            message="Issue synchronization failed",
            statistics={},
            errors=[str(e)],
            started_at=start_time,
            completed_at=end_time,
            duration_seconds=duration,
        )


@router.get(
    "/organizations/{organization_id}/repositories/{repository_id}/issues",
    response_model=List[RepositoryIssueResponse],
)
async def list_repository_issues(
    organization_id: str,
    repository_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    is_open: Optional[bool] = Query(None, description="Filter by open/closed status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    _org: Organization = Depends(require_org_role()),
):
    """List issues for a repository"""
    # Verify organization exists and user has access
    resolve_organization(organization_id, session)

    # Validate repository exists and belongs to organization
    repository = session.exec(
        select(Repository).where(
            Repository.id == repository_id,
            Repository.organization_id == organization_id,
        )
    ).first()

    if not repository:
        raise not_found("Repository", repository_id)

    # Build query
    query = select(RepositoryIssue).where(
        RepositoryIssue.repository_id == repository_id
    )

    if is_open is not None:
        query = query.where(RepositoryIssue.is_open == is_open)

    # Execute query with pagination
    issues = session.exec(
        query.offset(skip)
        .limit(limit)
        .order_by(RepositoryIssue.github_updated_at.desc())
    ).all()

    return issues


# ============================================================================
# Project Repository Association Endpoints
# ============================================================================
#
# Note: there is deliberately no "add repository to project" endpoint here.
# Repos are attached to a project only via auto-discovery by GitHub topic
# label -- see POST /organizations/{org_id}/projects/{project_id}/repositories/discover
# in src/routers/projects.py, which wraps GitHubConnectService.sync_project_repositories.
#
# There is also deliberately no "remove repository from project" endpoint
# here -- this used to be a duplicate of projects.py's DELETE endpoint at the
# same path (dead at runtime, shadowed by router registration order, but
# confusing to maintain as two copies). The canonical implementation lives
# in src/routers/projects.py, which also removes the project's GitHub topic
# label from the repo itself via GitHubConnectService.remove_project_repository
# -- something this old copy never did, it only touched InnoDay's own tables.


def _layer_value(layer: Optional[RepositoryLayer]) -> Optional[str]:
    """The lowercase value of a link layer, or None when it says nothing.

    `UNASSIGNED` means "nobody classified this for this project", which is not
    an answer -- the caller should fall back to the repository's own layer
    rather than overwrite a real value with a placeholder.
    """
    if layer is None or layer == RepositoryLayer.UNASSIGNED:
        return None
    return layer.value


@router.get(
    "/organizations/{organization_id}/projects/{project_id}/repositories",
    response_model=List[RepositoryResponse],
)
async def list_project_repositories(
    organization_id: str,
    project_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    layer: Optional[RepositoryLayer] = Query(None, description="Filter by layer"),
    _org: Organization = Depends(require_org_role()),
):
    """List repositories associated with a project"""
    # Verify organization exists and user has access
    resolve_organization(organization_id, session)

    # Resolve through the shared helper, which accepts a UUID, an alias, or a
    # name -- this route used to match on `Project.id` alone, so it was the one
    # place a project reference that works everywhere else 404s:
    #
    #     innoday --project BLASTOFF summary   -> fine
    #     innoday --project BLASTOFF sync      -> fine
    #     innoday --project BLASTOFF repos list -> 404
    #
    # An alias is what a person actually has to hand; the UUID is not. And the
    # failure is a bare 404, indistinguishable from "that project does not
    # exist", so the working form is not discoverable from the error.
    project = resolve_project(project_id, organization_id, session)

    # Build query (active links only -- soft-deleted repos that lost the
    # project's topic label are excluded)
    query = (
        # **Both sides of the link.** `Repository.layer` is the org-wide guess;
        # `ProjectRepository.layer` is what somebody decided this repo is *to
        # this project*, and it is the one that governs. Selecting only the
        # repository meant a per-project classification was invisible here:
        # `repos set-layer bps-ui-demo --layer design` reported success and
        # `repos list` went on showing `ui`, which reads as a command that did
        # nothing.
        select(Repository, ProjectRepository.layer)
        .join(ProjectRepository)
        .where(
            # project.id, not the incoming ref -- that ref may be an alias, and
            # joining on it would silently return nothing rather than 404.
            ProjectRepository.project_id == project.id,
            ProjectRepository.is_active == True,
        )
    )

    if layer:
        query = query.where(ProjectRepository.layer == layer)

    rows = session.exec(query.order_by(Repository.name)).all()

    # Build the responses rather than returning the ORM rows, so the link's
    # layer can win without assigning to `Repository.layer` -- that would mark
    # the row dirty and let a later commit write a project's opinion onto the
    # organisation-wide record.
    return [
        RepositoryResponse.model_validate(
            {
                **repository.model_dump(),
                "layer": _layer_value(link_layer) or repository.layer,
            }
        )
        for repository, link_layer in rows
    ]


# ============================================================================
# GitHub Organization Registration Endpoints (Legacy)
# ============================================================================


@router.post(
    "/organizations/{organization_id}/github-registrations",
    response_model=GitHubOrgRegistrationResponse,
)
async def create_github_registration(
    organization_id: str,
    registration: GitHubOrgRegistrationCreate,
    session: Session = Depends(get_session),
    x_integration_token: Optional[str] = Header(None),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """
    Register a GitHub organization for repository synchronization.

    Requires X-Integration-Token header with valid GitHub token.
    """
    # Verify organization exists and user has access
    resolve_organization(organization_id, session)

    if not x_integration_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Integration-Token header required",
        )

    # Validate GitHub token and organization access
    try:
        from src.api.github_api import GitHubAPI

        github_api = GitHubAPI(x_integration_token)

        # Validate token
        await github_api.validate_token()

        # Check organization access
        if not await github_api.validate_organization_access(registration.organization):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No access to organization: {registration.organization}",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"GitHub validation failed: {str(e)}",
        )

    # Check if registration already exists
    existing = session.exec(
        select(GitHubOrgRegistration).where(
            GitHubOrgRegistration.user_id == current_user.id,
            GitHubOrgRegistration.organization_id == organization_id,
            GitHubOrgRegistration.organization == registration.organization,
        )
    ).first()

    if existing:
        raise conflict("GitHub organization", registration.organization)

    # Create new registration
    github_registration = GitHubOrgRegistration(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        organization_id=organization_id,
        organization=registration.organization,
        sync_enabled=True,
        sync_readme=registration.sync_readme,
        sync_interval_minutes=registration.sync_interval_minutes,
        status="active",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    session.add(github_registration)
    session.commit()
    session.refresh(github_registration)

    logger.info(
        f"Created GitHub registration {github_registration.id} for org {registration.organization}"
    )

    return GitHubOrgRegistrationResponse(**github_registration.model_dump())


@router.get(
    "/organizations/{organization_id}/github-registrations",
    response_model=List[GitHubOrgRegistrationResponse],
)
async def list_github_registrations(
    organization_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """List all GitHub organization registrations for an organization"""
    # Verify organization exists and user has access
    resolve_organization(organization_id, session)

    registrations = session.exec(
        select(GitHubOrgRegistration)
        .where(GitHubOrgRegistration.organization_id == organization_id)
        .order_by(GitHubOrgRegistration.created_at.desc())
    ).all()

    return [GitHubOrgRegistrationResponse(**reg.model_dump()) for reg in registrations]


@router.get(
    "/organizations/{organization_id}/github-registrations/{registration_id}",
    response_model=GitHubOrgRegistrationResponse,
)
async def get_github_registration(
    organization_id: str,
    registration_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """Get a specific GitHub organization registration"""
    # Verify organization exists and user has access
    resolve_organization(organization_id, session)

    registration = session.exec(
        select(GitHubOrgRegistration).where(
            GitHubOrgRegistration.id == registration_id,
            GitHubOrgRegistration.organization_id == organization_id,
        )
    ).first()

    if not registration:
        raise not_found("GitHub registration", registration_id)

    return GitHubOrgRegistrationResponse(**registration.model_dump())


@router.put(
    "/organizations/{organization_id}/github-registrations/{registration_id}",
    response_model=GitHubOrgRegistrationResponse,
)
async def update_github_registration(
    organization_id: str,
    registration_id: str,
    update_data: GitHubOrgRegistrationUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """Update a GitHub organization registration"""
    # Verify organization exists and user has access
    resolve_organization(organization_id, session)

    registration = session.exec(
        select(GitHubOrgRegistration).where(
            GitHubOrgRegistration.id == registration_id,
            GitHubOrgRegistration.organization_id == organization_id,
        )
    ).first()

    if not registration:
        raise not_found("GitHub registration", registration_id)

    # Update fields
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(registration, field, value)

    registration.updated_at = datetime.now(timezone.utc)

    session.add(registration)
    session.commit()
    session.refresh(registration)

    logger.info(f"Updated GitHub registration {registration_id}")

    return GitHubOrgRegistrationResponse(**registration.model_dump())


@router.delete(
    "/organizations/{organization_id}/github-registrations/{registration_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_github_registration(
    organization_id: str,
    registration_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role(OrganizationRole.ADMIN)),
):
    """Delete a GitHub organization registration"""
    # Verify organization exists and user has admin access
    resolve_organization(organization_id, session)

    registration = session.exec(
        select(GitHubOrgRegistration).where(
            GitHubOrgRegistration.id == registration_id,
            GitHubOrgRegistration.organization_id == organization_id,
        )
    ).first()

    if not registration:
        raise not_found("GitHub registration", registration_id)

    session.delete(registration)
    session.commit()

    logger.info(f"Deleted GitHub registration {registration_id}")


@router.get(
    "/organizations/{organization_id}/projects/{project_id}/repositories/sync-history",
    response_model=List[SyncHistoryResponse],
)
async def get_sync_history(
    organization_id: str,
    project_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    _org: Organization = Depends(require_org_role()),
):
    """Recent repository-sync attempts for a project, newest first.

    **Keyed on the project, because that is the only grain the table has.** This
    route used to read `github_sync_history` through
    `github_org_registration_id`, the org-wide registration sync's key -- a sync
    that #658 deleted, along with the column. Every remaining row is written by
    `GitHubConnectService._record_sync_history`, one per topic-discovery attempt
    for one project, so a registration is neither a key nor a filter here any
    more.
    """
    # Verify organization exists and user has access
    resolve_organization(organization_id, session)

    # Through the shared helper, so an alias works here exactly as it does on
    # `GET .../projects/{project_id}/repositories` -- an alias is what a person
    # has to hand, and matching on `Project.id` alone would 404 on it.
    project = resolve_project(project_id, organization_id, session)

    sync_history = session.exec(
        select(GitHubSyncHistory)
        .where(GitHubSyncHistory.project_id == project.id)
        .order_by(GitHubSyncHistory.started_at.desc())
        .limit(limit)
    ).all()

    return [SyncHistoryResponse(**sync.model_dump()) for sync in sync_history]
