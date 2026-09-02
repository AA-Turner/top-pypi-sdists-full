"""
Project Management API Router

Provides REST API endpoints for managing projects and their components.
"""

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlmodel import Session, select

from src.database import get_session
from src.domain.board import BoardRegistration
from src.domain.organization import Organization, OrganizationRole
from src.domain.project import (
    Project,
    ProjectPriority,
    ProjectRepository,
    ProjectStatus,
    RepositoryLayer,
)
from src.domain.user import User
from src.middleware.rbac import (
    get_current_user,
    not_found,
    require_org_role,
    resolve_organization,
)
from src.services.project_service import ProjectService

logger = logging.getLogger(__name__)


def resolve_project(project_ref: str, org_id: str, session: Session) -> Project:
    """
    Look up a project within an org by UUID, alias, or name (case-insensitive).
    Raises 404 if not found or belongs to a different org, 409 if a *name*
    matches more than one project.

    **The order is the guarantee.** Id, then alias, then name -- and only the
    first two are unique. `projects.id` is the primary key and
    `uq_project_org_alias` covers `(organization_id, alias)`; `projects.name`
    has no constraint at all, so several projects in one org may share one.

    The name branch therefore refuses rather than picks. It used to be a plain
    `.first()` on an unordered query: with two projects called "Platform" the
    answer was whichever row Postgres happened to return, and it could differ
    between two identical requests. Twenty-nine call sites read this, so a
    silent arbitrary pick means a ticket created against, or a summary written
    for, the wrong project -- with nothing anywhere saying a choice was made.
    An ambiguous name is a question only the caller can answer, so it is asked.

    No duplicate names existed when this was written (measured: zero, and zero
    names colliding with another project's alias). This is the trap being
    disarmed before it arms itself, not a bug being chased.
    """
    from sqlalchemy import func as sa_func

    project = (
        session.get(Project, project_ref)
        or session.exec(
            select(Project).where(
                sa_func.upper(Project.alias) == project_ref.upper(),
                Project.organization_id == org_id,
            )
        ).first()
    )

    if project is None:
        by_name = session.exec(
            select(Project)
            .where(
                sa_func.lower(Project.name) == project_ref.lower(),
                Project.organization_id == org_id,
            )
            # Ordered so that the *error* below is reproducible too -- an
            # unordered listing would name the candidates in a different order
            # each time it was read.
            .order_by(Project.alias)
        ).all()
        if len(by_name) > 1:
            raise HTTPException(
                status_code=409,
                detail=(
                    f"{len(by_name)} projects in this organization are named "
                    f"{project_ref!r}. Use the alias instead: "
                    + ", ".join(p.alias for p in by_name if p.alias)
                ),
            )
        project = by_name[0] if by_name else None

    if not project:
        raise not_found("Project", project_ref)
    if project.organization_id != org_id:
        raise HTTPException(
            status_code=403, detail="Project belongs to a different organization"
        )
    return project


def _resolve_board_id(project_id: str, session: Session) -> Optional[str]:
    """Return the ID of the project's attached board, if any (0 or 1)."""
    board = session.exec(
        select(BoardRegistration).where(BoardRegistration.project_id == project_id)
    ).first()
    return board.id if board else None


# Initialize router
router = APIRouter(tags=["projects"])


# Request/Response Models
class ProjectCreate(BaseModel):
    """Request model for creating a project"""

    name: str = Field(..., max_length=255, description="Project name")
    description: str = Field(..., max_length=2000, description="Project description")
    alias: str = Field(
        ...,
        max_length=10,
        min_length=1,
        description="Short uppercase code used as ticket prefix (e.g. BP, PF, HS). "
        "Required; unique within the organization.",
    )
    goals: Optional[str] = Field(
        None, description="Markdown-formatted goals and milestones"
    )
    scope_limitations: Optional[str] = Field(None, description="What's out of scope")
    spec: Optional[str] = Field(
        None, description="One-paragraph plain-language description of the project"
    )
    project_context: Optional[str] = Field(
        None,
        description="Full markdown block of repo summaries, active work, and conventions",
    )
    priority: ProjectPriority = Field(default=ProjectPriority.MEDIUM)
    status: ProjectStatus = Field(default=ProjectStatus.PLANNING)
    tags: Optional[List[str]] = Field(default_factory=list)


class TicketCreationConfig(BaseModel):
    """Board destination, labels, issue type, and optional parent epic used by quick-tickets"""

    board_id: str
    labels: List[str] = Field(default_factory=list)
    issue_type: Optional[str] = None
    parent_epic: Optional[str] = None


class ProjectUpdate(BaseModel):
    """Request model for updating a project"""

    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    alias: Optional[str] = Field(
        None, max_length=10, description="Short uppercase code used as ticket prefix"
    )
    goals: Optional[str] = None
    scope_limitations: Optional[str] = None
    spec: Optional[str] = None
    project_context: Optional[str] = None
    priority: Optional[ProjectPriority] = None
    status: Optional[ProjectStatus] = None
    tags: Optional[List[str]] = None
    ticket_creation_config: Optional[TicketCreationConfig] = Field(
        None, description="Board destination, labels, issue type, optional parent epic"
    )


class ProjectResponse(BaseModel):
    """Response model for project data"""

    id: str
    organization_id: str
    alias: str
    name: str
    description: str
    goals: Optional[str]
    scope_limitations: Optional[str]
    spec: Optional[str]
    project_context: Optional[str]
    status: str
    priority: str
    tags: List[str]
    board_registration_id: Optional[str]
    ticket_creation_config: Optional[TicketCreationConfig]
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class RepositoryDiscoverResponse(BaseModel):
    """Response model for a project repository auto-discovery/sync run"""

    sync_id: str
    project_id: str
    status: str
    github_label: Optional[str] = None
    repositories_synced: int
    new_repositories: List[Dict]
    reactivated_repositories: int = 0
    updated_repositories: int
    deactivated_repositories: int = 0
    deactivated_repository_names: List[str] = []
    timestamp: str


class ProjectRepositoryUpdate(BaseModel):
    """Body for updating a project's repository link.

    A body, not query parameters. FastAPI binds a bare `Optional[...]` handler
    argument from the **query string**, so these fields used to travel there --
    which meant sending them in a JSON body, the way every other update route in
    this API accepts them, looked correct and silently changed nothing.
    """

    layer: Optional[RepositoryLayer] = None
    is_primary: Optional[bool] = None
    is_primary_project: Optional[bool] = None
    purpose: Optional[str] = None


class ProjectRepositoryResponse(BaseModel):
    """Response model for project repository link"""

    id: str
    project_id: str
    repository_id: str
    layer: str
    is_primary: bool
    #: This project owns the repo's release path -- NOT a variant of is_primary
    #: above, which says the repo is the project's main repo. Defaulted rather
    #: than required so the field is additive for any existing client.
    is_primary_project: bool = False
    purpose: Optional[str]
    added_at: str

    model_config = ConfigDict(from_attributes=True)


class BoardAttach(BaseModel):
    """Request model for attaching a board to a project"""

    board_registration_id: str = Field(
        ..., description="Board registration ID to attach"
    )


# API Endpoints


@router.get(
    "/api/v1/organizations/{org_id}/projects", response_model=List[ProjectResponse]
)
async def list_projects(
    org_id: str,
    status: Optional[ProjectStatus] = Query(None),
    priority: Optional[ProjectPriority] = Query(None),
    tags: Optional[str] = Query(None, description="Comma-separated tags"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """List all projects for an organization with optional filters"""
    service = ProjectService(session)

    # Parse tags if provided
    tag_list = tags.split(",") if tags else None

    projects = await service.list_projects(
        organization_id=org_id,
        status=status,
        priority=priority,
        tags=tag_list,
    )

    return [
        ProjectResponse(
            id=p.id,
            organization_id=p.organization_id,
            alias=p.alias,
            name=p.name,
            description=p.description,
            goals=p.goals,
            scope_limitations=p.scope_limitations,
            spec=p.spec,
            project_context=p.project_context,
            status=p.status.value,
            priority=p.priority.value,
            tags=p.tags,
            board_registration_id=_resolve_board_id(p.id, session),
            ticket_creation_config=p.ticket_creation_config,
            created_at=p.created_at.isoformat(),
            updated_at=p.updated_at.isoformat(),
        )
        for p in projects
    ]


@router.post("/api/v1/organizations/{org_id}/projects", response_model=ProjectResponse)
async def create_project(
    org_id: str,
    project: ProjectCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.ADMIN)),
):
    """Create a new project.

    When this is the org's *first* project, every membership in the org has its
    `default_project_id` seeded to it -- inside the same transaction as the
    insert, which is why that lives in `ProjectService.create_project` and not
    here: "did this org have no projects?" is only answerable before the row
    lands.
    """
    service = ProjectService(session)

    created = await service.create_project(
        organization_id=org_id,
        name=project.name,
        description=project.description,
        alias=project.alias,
        goals=project.goals,
        scope_limitations=project.scope_limitations,
        spec=project.spec,
        project_context=project.project_context,
        priority=project.priority,
        status=project.status,
        tags=project.tags,
    )

    return ProjectResponse(
        id=created.id,
        organization_id=created.organization_id,
        alias=created.alias,
        name=created.name,
        description=created.description,
        goals=created.goals,
        scope_limitations=created.scope_limitations,
        spec=created.spec,
        project_context=created.project_context,
        status=created.status.value,
        priority=created.priority.value,
        tags=created.tags,
        board_registration_id=_resolve_board_id(created.id, session),
        ticket_creation_config=created.ticket_creation_config,
        created_at=created.created_at.isoformat(),
        updated_at=created.updated_at.isoformat(),
    )


@router.get("/api/v1/organizations/{org_id}/projects/{project_id}")
async def get_project(
    org_id: str,
    project_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Get project details. Accepts UUID, alias, or name as {project_id}."""
    org = resolve_organization(org_id, session)
    project = resolve_project(project_id, org.id, session)

    return ProjectResponse(
        id=project.id,
        organization_id=project.organization_id,
        alias=project.alias,
        name=project.name,
        description=project.description,
        goals=project.goals,
        scope_limitations=project.scope_limitations,
        spec=project.spec,
        project_context=project.project_context,
        status=project.status.value,
        priority=project.priority.value,
        tags=project.tags,
        board_registration_id=_resolve_board_id(project.id, session),
        ticket_creation_config=project.ticket_creation_config,
        created_at=project.created_at.isoformat(),
        updated_at=project.updated_at.isoformat(),
    )


@router.put(
    "/api/v1/organizations/{org_id}/projects/{project_id}",
    response_model=ProjectResponse,
)
async def update_project(
    org_id: str,
    project_id: str,
    updates: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.ADMIN)),
):
    """Update project metadata. Accepts UUID, alias, or name as {project_id}."""
    org = resolve_organization(org_id, session)
    service = ProjectService(session)

    project = resolve_project(project_id, org.id, session)
    update_dict = updates.model_dump(exclude_unset=True)
    try:
        updated = await service.update_project(project.id, **update_dict)
    except ValueError as e:
        # A rejected alias -- taken, or held by an archived project -- is
        # something the caller can act on, and `_normalize_alias`'s message says
        # how. Uncaught it left the route with a 500 on an ordinary refusal, the
        # same shape as create before it caught this.
        raise HTTPException(status_code=400, detail=str(e))

    return ProjectResponse(
        id=updated.id,
        organization_id=updated.organization_id,
        alias=updated.alias,
        name=updated.name,
        description=updated.description,
        goals=updated.goals,
        scope_limitations=updated.scope_limitations,
        spec=updated.spec,
        project_context=updated.project_context,
        status=updated.status.value,
        priority=updated.priority.value,
        tags=updated.tags,
        board_registration_id=_resolve_board_id(updated.id, session),
        ticket_creation_config=updated.ticket_creation_config,
        created_at=updated.created_at.isoformat(),
        updated_at=updated.updated_at.isoformat(),
    )


@router.delete("/api/v1/organizations/{org_id}/projects/{project_id}")
async def delete_project(
    org_id: str,
    project_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.ADMIN)),
):
    """Archive a project. Accepts UUID, alias, or name as {project_id}.

    Archives -- the row is never removed and the alias stays taken. The
    response identifies what changed and its prior status so the caller can
    report and audit the outcome rather than echoing a fixed string.
    """
    org = resolve_organization(org_id, session)
    service = ProjectService(session)

    project = resolve_project(project_id, org.id, session)
    previous_status = project.status.value
    await service.delete_project(project.id)
    return {
        "message": "Project archived successfully",
        "id": project.id,
        "alias": project.alias,
        "name": project.name,
        "status": ProjectStatus.ARCHIVED.value,
        "previous_status": previous_status,
    }


@router.post(
    "/api/v1/organizations/{org_id}/projects/{project_id}/repositories/discover",
    response_model=RepositoryDiscoverResponse,
)
async def discover_project_repositories(
    org_id: str,
    project_id: str,
    github_label: Optional[str] = Query(
        None,
        description=(
            "GitHub topic to search for. Defaults to the project's alias "
            "(lowercased) if omitted."
        ),
    ),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    # DEVELOPER, not ADMIN. Discovery attaches repos that GitHub already says
    # carry the project's topic -- it grants no access the caller did not have,
    # and someone blocked on a repo could not clone it either, so GitHub's own
    # permissions are the real boundary. Requiring ADMIN meant a DEVELOPER's
    # `innoday sync` completed its board stage and then 403'd on repositories,
    # which is also every new member's default role.
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """
    Auto-discover and attach repositories to a project by GitHub topic label.

    This is the only way repos are attached to a project -- there is no
    manual link step. Repos tagged with the project's topic (its alias
    lowercased, by convention) on GitHub are found, registered if new, and linked to this
    project automatically. Safe to call repeatedly (idempotent upsert).
    """
    from src.services.github_connect_service import GitHubConnectService

    org = resolve_organization(org_id, session)
    project = resolve_project(project_id, org.id, session)

    try:
        result = await GitHubConnectService(session).sync_project_repositories(
            organization_id=org.id,
            project_id=project.id,
            github_label=github_label,
        )
        return RepositoryDiscoverResponse(
            sync_id=result["sync_id"],
            project_id=result["project_id"],
            status=result["status"],
            github_label=github_label
            or (project.alias.lower() if project.alias else None),
            repositories_synced=result["repositories_synced"],
            new_repositories=result["changes"]["new_repositories"],
            reactivated_repositories=result["changes"]["reactivated_repositories"],
            updated_repositories=result["changes"]["updated_repositories"],
            deactivated_repositories=result["changes"]["deactivated_repositories"],
            deactivated_repository_names=result["changes"][
                "deactivated_repository_names"
            ],
            timestamp=result["timestamp"],
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/api/v1/organizations/{org_id}/projects/{project_id}/repositories/{repo_id}",
    response_model=ProjectRepositoryResponse,
)
async def update_repository_in_project(
    org_id: str,
    project_id: str,
    repo_id: str,
    body: Optional[ProjectRepositoryUpdate] = None,
    # Query forms, kept for one release so a client mid-upgrade is not broken.
    # Deprecated: send a body.
    layer: Optional[RepositoryLayer] = None,
    is_primary: Optional[bool] = None,
    is_primary_project: Optional[bool] = None,
    purpose: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.ADMIN)),
):
    """Update repository layer or role in project.

    ``is_primary`` and ``is_primary_project`` point opposite ways and are easy to
    mistake for each other: the first says this repo is the project's main repo,
    the second says this project owns the repo's release path. See
    ``ProjectRepository.is_primary_project``.
    """
    org = resolve_organization(org_id, session)
    project = resolve_project(project_id, org.id, session)

    project_repo = session.exec(
        select(ProjectRepository).where(
            ProjectRepository.project_id == project.id,
            ProjectRepository.repository_id == repo_id,
            ProjectRepository.is_active == True,
        )
    ).first()

    if not project_repo:
        raise HTTPException(status_code=404, detail="Repository not found in project")

    # Body wins; the query form is the deprecated fallback.
    if body is not None:
        layer = body.layer if body.layer is not None else layer
        is_primary = body.is_primary if body.is_primary is not None else is_primary
        is_primary_project = (
            body.is_primary_project
            if body.is_primary_project is not None
            else is_primary_project
        )
        purpose = body.purpose if body.purpose is not None else purpose

    # Update fields
    if layer is not None:
        project_repo.layer = layer
    if is_primary is not None:
        project_repo.is_primary = is_primary
    if is_primary_project is not None:
        if is_primary_project:
            # Clear the repo's primary elsewhere first. uq_repo_primary_project
            # would otherwise reject this as an IntegrityError -- a 500 for what
            # is a legitimate request to *move* a repo's release path, and the
            # index cannot tell "move it here" from "two primaries" on its own.
            for other in session.exec(
                select(ProjectRepository).where(
                    ProjectRepository.repository_id == repo_id,
                    ProjectRepository.project_id != project.id,
                    ProjectRepository.is_primary_project == True,  # noqa: E712
                )
            ).all():
                other.is_primary_project = False
                session.add(other)
            session.flush()
        project_repo.is_primary_project = is_primary_project
    if purpose is not None:
        project_repo.purpose = purpose

    session.commit()
    session.refresh(project_repo)

    return ProjectRepositoryResponse(
        id=project_repo.id,
        project_id=project_repo.project_id,
        repository_id=project_repo.repository_id,
        layer=project_repo.layer.value,
        is_primary=project_repo.is_primary,
        is_primary_project=project_repo.is_primary_project,
        purpose=project_repo.purpose,
        added_at=project_repo.added_at.isoformat(),
    )


@router.delete(
    "/api/v1/organizations/{org_id}/projects/{project_id}/repositories/{repo_id}"
)
async def remove_repository_from_project(
    org_id: str,
    project_id: str,
    repo_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.ADMIN)),
):
    """
    Remove a repository from a project.

    This removes the project's GitHub topic label from the repo on GitHub
    itself, then soft-deletes the link to match -- GitHub is the source of
    truth. The link is deactivated, not hard-deleted, so re-adding the topic
    label later reactivates the same row (see ProjectRepository.is_active).
    """
    from src.services.github_connect_service import GitHubConnectService

    org = resolve_organization(org_id, session)
    project = resolve_project(project_id, org.id, session)

    try:
        result = await GitHubConnectService(session).remove_project_repository(
            organization_id=org.id,
            project_id=project.id,
            repository_id=repo_id,
        )
    except ValueError as e:
        detail = str(e)
        status_code = 404 if "not found" in detail.lower() else 400
        raise HTTPException(status_code=status_code, detail=detail)

    return {
        "message": "Repository removed from project successfully",
        "removed_topic": result["removed_topic"],
    }


@router.post("/api/v1/organizations/{org_id}/projects/{project_id}/board")
async def attach_board_to_project(
    org_id: str,
    project_id: str,
    board_attach: BoardAttach,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.ADMIN)),
):
    """Attach an existing board to a project"""
    org = resolve_organization(org_id, session)
    service = ProjectService(session)
    project = resolve_project(project_id, org.id, session)

    try:
        await service.attach_board(
            project_id=project.id,
            board_registration_id=board_attach.board_registration_id,
        )
        return {"message": "Board attached to project successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/v1/organizations/{org_id}/projects/{project_id}/overview")
async def get_project_overview(
    org_id: str,
    project_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Get complete project overview with all related data"""
    org = resolve_organization(org_id, session)
    service = ProjectService(session)
    project = resolve_project(project_id, org.id, session)

    try:
        overview = await service.get_project_overview(project.id)
        return overview
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/api/v1/organizations/{org_id}/projects/{project_id}/issues")
async def get_project_issues(
    org_id: str,
    project_id: str,
    layer: Optional[RepositoryLayer] = Query(None),
    status: Optional[str] = Query(None, description="open or closed"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Get all GitHub issues from project repositories"""
    org = resolve_organization(org_id, session)
    from src.domain.repository_issue import RepositoryIssue

    project = resolve_project(project_id, org.id, session)

    query = select(ProjectRepository).where(
        ProjectRepository.project_id == project.id,
        ProjectRepository.is_active == True,
    )
    if layer:
        query = query.where(ProjectRepository.layer == layer)

    project_repos = session.exec(query).all()
    repo_ids = [pr.repository_id for pr in project_repos]

    if not repo_ids:
        return []

    # Get issues from repositories
    issues_query = select(RepositoryIssue).where(
        RepositoryIssue.repository_id.in_(repo_ids)
    )

    if status == "open":
        issues_query = issues_query.where(RepositoryIssue.is_open == True)
    elif status == "closed":
        issues_query = issues_query.where(RepositoryIssue.is_open == False)

    issues = session.exec(issues_query).all()

    return [
        {
            "id": issue.id,
            "github_issue_id": issue.github_issue_id,
            "repository_id": issue.repository_id,
            "title": issue.title,
            "is_open": issue.is_open,
            "github_url": issue.github_url,
            "created_at": (
                issue.github_created_at.isoformat() if issue.github_created_at else None
            ),
            "updated_at": (
                issue.github_updated_at.isoformat() if issue.github_updated_at else None
            ),
        }
        for issue in issues
    ]


@router.post("/api/v1/organizations/{org_id}/projects/{project_id}/summary")
async def create_project_summary(
    org_id: str,
    project_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Generate an AI-powered summary of the project."""
    org = resolve_organization(org_id, session)
    project = resolve_project(project_id, org.id, session)

    return {
        "project_id": project.id,
        "summary": f"Project {project.name} is in {project.status.value} status with {project.priority.value} priority.",
        "key_points": [
            f"Status: {project.status.value}",
            f"Priority: {project.priority.value}",
            f"Created: {project.created_at.isoformat()}",
        ],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/api/v1/organizations/{org_id}/projects/{project_id}/health")
async def get_project_health_endpoint(
    org_id: str,
    project_id: str,
    probe: bool = Query(
        True,
        description=(
            "Contact each active board and time the round trip. On by default — "
            "without it the answer is assembled purely from InnoDay's own "
            "database. Pass false to skip the outbound calls."
        ),
    ),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """Is this project working — database, boards, and their credentials.

    One call in place of four. `GET /health` answers for the database globally
    and knows nothing about a project; `.../boards` says what is registered;
    `.../boards/{id}/sync-history` says whether the last sync worked; and only a
    `--dry-run` sync — asynchronous, ~50s, poll loop — proved a board was
    reachable at all. Three of those four read only InnoDay's own database, so
    the verdict a caller assembled from them could be confidently wrong about an
    expired credential.

    **`probe` defaults to true.** It shipped defaulting off, which meant the
    default answer to this endpoint's own question came entirely from InnoDay's
    database — so a board whose credential expired months ago read as healthy.
    That is the non-answer this route exists to replace. `probe=false` stays for
    callers that genuinely want the cheap view.

    Probing is bounded: a deadline per board, a deadline on credential/adapter
    setup (an OAuth Jira board mints a token over the network there), a total
    budget across all boards, and capped concurrency. The probe phase cannot
    fail the response — the database verdict and the sync ages are the half that
    cannot fail, and a misbehaving third party must not turn this into a 500.

    **`reachable` is three-valued**, like `validate_service_credential`'s
    `valid`: `true`/`false` are verdicts, `null` means nothing was proved —
    probing was skipped, the registration is inactive, no credential is stored,
    or the budget ran out before this board was reached. Collapsing "could not
    ask" into `false` would report a working board as broken. A board that was
    asked and did not answer in time *is* `false`.

    **`last_sync_age_seconds` is a number, not a verdict.** Whether that is
    "stale" is the caller's policy: a board synced hourly and one synced weekly
    are both correct, and this endpoint cannot know which it is looking at.
    Dry-run rows are excluded — a preview is not evidence of freshness, per
    `BoardSyncHistory.dry_run`.

    **DEVELOPER, matching `POST .../boards/{id}/sync`.** With `probe=true` this
    drives an outbound call per board using that board's stored credential, and
    it is strictly cheaper than the sync the same role can already trigger.
    Guarding it more loosely than the operation it approximates would be the
    wrong way round.
    """
    from src.services.project_health_service import get_project_health

    org = resolve_organization(org_id, session)
    project = resolve_project(project_id, org.id, session)

    health = await get_project_health(
        session=session,
        organization=org,
        project_id=project.id,
        probe=probe,
    )
    health["project_alias"] = project.alias
    return health
