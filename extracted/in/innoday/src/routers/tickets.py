"""
Ticket management API endpoints.

This module provides endpoints for managing tickets within organizations
and boards, including CRUD operations and filtering.
"""

import logging
from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Header,
    HTTPException,
    Query,
)
from fastapi import status as status_codes
from pydantic import BaseModel, Field
from sqlalchemy import func, nullslast, or_
from sqlmodel import Session, select

from src.database import get_session
from src.domain.board import BoardRegistration, BoardSyncHistory, SyncStatus
from src.domain.organization import Organization, OrganizationRole
from src.domain.project import Project, ProjectRepository
from src.domain.repository import Repository
from src.domain.repository_issue import RepositoryIssue
from src.domain.ticket import Ticket, TicketComment, TicketStatus
from src.domain.user import User
from src.middleware.rbac import (
    get_current_user,
    not_found,
    require_org_role,
    resolve_organization,
    resolve_project_ref,
)
from src.routers.projects import resolve_project
from src.services.board_sync_service import sync_board_tickets_task
from src.services.ticket_release import (
    CURRENT_RELEASE,
    NO_CURRENT_RELEASE_DETAIL,
    ReleaseNotOutstanding,
    current_release_version,
    resolve_ticket_release,
)
from src.utils.license_utils import (
    can_create_ticket,
    track_usage,
)

logger = logging.getLogger(__name__)

# Ceiling on GET /{org}/work's page size. The endpoint merges two sources in
# Python, so an unbounded limit meant an unbounded merge -- it was previously
# unvalidated entirely.
MAX_UNIFIED_WORK_LIMIT = 500

router = APIRouter(prefix="/api/v1/organizations", tags=["tickets"])


# Pydantic models for request/response
class TicketCreate(BaseModel):
    """Request model for creating a ticket"""

    summary: str = Field(..., description="Ticket summary/title")
    description: Optional[str] = Field(None, description="Detailed description")
    assignee: Optional[str] = Field(None, description="Assignee username or ID")
    status: TicketStatus = Field(TicketStatus.BACKLOG, description="Initial status")
    url: Optional[str] = Field(None, description="External ticket URL")
    created_by: Optional[str] = Field(None, description="Creator user ID")
    project_id: Optional[str] = Field(
        None,
        description="Project to attach this ticket to (for tickets created outside a board)",
    )
    release: Optional[str] = Field(
        None,
        max_length=100,
        description=(
            "Release version to plan this ticket into. Must be one of the "
            "project's outstanding releases (planned or in progress), or "
            "'current' for the version being cut. Matched exactly, "
            "case-sensitively."
        ),
    )
    push_to_board: bool = Field(
        True,
        description=(
            "If the project has an active external board, also create the "
            "ticket on that board at create time (best-effort). Set false for "
            "bulk/parse flows that would otherwise fire one synchronous "
            "external board call per ticket."
        ),
    )


class TicketUpdate(BaseModel):
    """Request model for updating a ticket"""

    summary: Optional[str] = Field(None, description="New summary")
    description: Optional[str] = Field(None, description="New description")
    assignee: Optional[str] = Field(None, description="New assignee")
    status: Optional[TicketStatus] = Field(None, description="New status")
    url: Optional[str] = Field(None, description="New URL")
    release: Optional[str] = Field(
        None,
        max_length=100,
        description=(
            "Release version to plan this ticket into. Must be one of the "
            "project's outstanding releases (planned or in progress), or "
            "'current' for the version being cut. Pass \"\" to take the ticket "
            "out of its release. Matched exactly, case-sensitively."
        ),
    )
    project_id: Optional[str] = Field(
        None, description="Project to (re)attach this ticket to"
    )


class CommentCreate(BaseModel):
    """Request model for creating a comment"""

    comment: str = Field(..., description="Comment text")
    commenter_id: str = Field(..., description="Commenter user ID")
    parent_comment_id: Optional[int] = Field(
        None, description="Parent comment ID for threading"
    )


class TicketCancel(BaseModel):
    """Request model for cancelling a ticket. A note is mandatory -- cancelling
    is a soft, reversible status change, and the note is the only record of
    why, so it must never be empty."""

    note: str = Field(..., min_length=1, description="Reason for cancelling")


class RefreshRequest(BaseModel):
    """Request model for refreshing tickets from external board"""

    board_id: str = Field(..., description="Board registration ID to refresh")


class UnifiedWorkItem(BaseModel):
    """A work item from any source: ticket or GitHub issue."""

    type: str
    id: str
    summary: str
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    source_platform: str
    assignee: Optional[str] = None
    url: Optional[str] = None
    external_id: Optional[str] = None
    parent_external_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


def get_org_tickets(
    session: Session,
    organization_id: str,
    *,
    source_platform: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assignee: Optional[str] = None,
    newest_first: bool = False,
    max_rows: Optional[int] = None,
) -> list:
    """Org tickets, optionally filtered and bounded in SQL.

    The filters and ``max_rows`` exist so ``get_unified_work`` no longer loads
    every ticket in the org into memory just to slice a page off the end.
    """
    query = select(Ticket).where(
        Ticket.organization_id == organization_id,
        Ticket.deleted_at.is_(None),
    )
    if source_platform is not None:
        # "unknown" is the API's label for a ticket with no platform recorded.
        if source_platform == "unknown":
            query = query.where(
                or_(Ticket.source_platform.is_(None), Ticket.source_platform == "")
            )
        else:
            query = query.where(Ticket.source_platform == source_platform)
    if status is not None:
        query = query.where(Ticket.status == status)
    if priority is not None:
        query = query.where(Ticket.priority == priority)
    if assignee is not None:
        query = query.where(Ticket.assignee == assignee)
    if newest_first:
        query = query.order_by(nullslast(Ticket.updated_at.desc()))
    if max_rows is not None:
        query = query.limit(max_rows)
    return session.exec(query).all()


def get_org_github_issues(
    session: Session,
    organization_id: str,
    *,
    is_open: Optional[bool] = None,
    newest_first: bool = False,
    max_rows: Optional[int] = None,
) -> list:
    """Repo issues for every active repository linked to the org's projects."""
    repo_ids = session.exec(
        select(ProjectRepository.repository_id)
        .join(Project, Project.id == ProjectRepository.project_id)
        .where(
            Project.organization_id == organization_id,
            ProjectRepository.is_active == True,
        )
    ).all()
    if not repo_ids:
        return []
    query = select(RepositoryIssue).where(RepositoryIssue.repository_id.in_(repo_ids))
    if is_open is not None:
        query = query.where(RepositoryIssue.is_open == is_open)
    if newest_first:
        query = query.order_by(nullslast(RepositoryIssue.updated_at.desc()))
    if max_rows is not None:
        query = query.limit(max_rows)
    return session.exec(query).all()


# ============================================================================
# Organization-level ticket endpoints
# ============================================================================


def _resolve_release_for_write(
    value: Optional[str],
    organization_id: str,
    project_id: Optional[str],
    session: Session,
) -> Optional[str]:
    """The version to store for a submitted ``release``, or a 422.

    **422, with ``detail`` as a plain string.** The CLI f-strings ``detail`` into
    its error line and the MCP server hands the raw body to an agent, so a dict
    would reach a human as ``{'msg': ...}``. One readable sentence naming the
    value, the project and every outstanding version lets an agent self-correct in
    a single turn.
    """
    try:
        return resolve_ticket_release(
            session,
            organization_id=organization_id,
            project_id=project_id,
            value=value,
        )
    except ReleaseNotOutstanding as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


def _resolve_release_filter(
    value: str, organization_id: str, project_id: str, session: Session
) -> str:
    """Turn a ``release`` filter value into the version string to match on.

    ``project_id`` is required, not optional: a version string is only meaningful
    within a project. Every caller reaches this from a route with the project in
    its path, so no form of the question can lack one.

    Anything other than :data:`CURRENT_RELEASE` is used verbatim -- the join is
    free text (``ticket.release``, no foreign key), so an unknown version is a
    legitimate query that simply matches nothing rather than an error. **That
    half is not shared with the write path and must not become shared:** a
    submitted version is validated against the project's outstanding releases and
    stored as the release row's own string, so every reader of the column matches
    it byte-exactly. Only the sentinel means the same thing on both sides.

    So the sentinel resolves through :func:`current_release_version` -- the one
    place that answers "which version is current" -- and all this adds is the
    HTTP shape of "there isn't one".
    """
    if value != CURRENT_RELEASE:
        return value

    version = current_release_version(
        session, organization_id=organization_id, project_id=project_id
    )
    if version is None:
        raise HTTPException(
            status_code=status_codes.HTTP_404_NOT_FOUND,
            detail=NO_CURRENT_RELEASE_DETAIL.format(project=project_id),
        )
    return version


@router.get("/{organization_id}/tickets", response_model=List[Ticket])
async def get_all_organization_tickets(
    organization_id: str,
    status: Optional[TicketStatus] = None,
    assignee: Optional[str] = None,
    assigned_to: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Get all tickets across all boards in the organization.

    Two different assignee filters, and they are not interchangeable:
    `assignee` matches the board's own display-name string, `assigned_to`
    matches the resolved `users.id` FK. Anything holding a user id -- the CLI,
    the MCP server's check_status -- wants `assigned_to`; passing a user id as
    `assignee` matches nothing at all.

    **There is deliberately no ``release`` filter here.** A version string means
    something only inside a project -- PF's v1.9.0 and BPAI's v1.9.0 are unrelated
    releases that happen to share a name -- so filtering an organization-wide
    collection by version would merge two different answers into one. The release
    filters live on the project-scoped route below, where the project is part of
    the path and the meaningless form cannot be expressed.
    """
    resolve_organization(organization_id, session)

    # Build query
    statement = select(Ticket).where(Ticket.organization_id == organization_id)
    statement = statement.where(Ticket.deleted_at.is_(None))

    if status:
        statement = statement.where(Ticket.status == status)
    else:
        statement = statement.where(Ticket.status != TicketStatus.DRAFT)
    if assignee:
        statement = statement.where(Ticket.assignee == assignee)
    if assigned_to:
        statement = statement.where(Ticket.assigned_to == assigned_to)

    tickets = session.exec(statement).all()
    return tickets


# ============================================================================
# Project-level ticket endpoints
# ============================================================================


@router.get(
    "/{organization_id}/projects/{project_id}/tickets", response_model=List[Ticket]
)
async def get_project_tickets(
    organization_id: str,
    project_id: str,
    status: Optional[TicketStatus] = None,
    assignee: Optional[str] = None,
    assigned_to: Optional[str] = None,
    # A plain default, not `Query(...)`: `Query(None)` is only resolved by FastAPI
    # when the route is reached over HTTP, and these route functions are also
    # called directly in tests -- where the default arrives as a `Query` object,
    # which is truthy, so the filter fires and the driver rejects the bind.
    release: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Get all tickets for a specific project.

    Same two non-interchangeable assignee filters as the org-level route:
    `assignee` matches the board's display-name string, `assigned_to` matches
    the resolved `users.id` FK. A caller holding a user id wants `assigned_to`.

    ``release`` filters by version: a literal string such as ``v1.9.0``, or
    ``current`` for whatever this project is cutting now. **This is the only place
    a release filter belongs**, because a version means something only inside a
    project -- PF's v1.9.0 and BPAI's v1.9.0 are unrelated releases that happen to
    share a name. The project is in the path here, so the meaningless
    organization-wide form cannot be expressed.

    The filter reads ``ticket.release``, a **free-text version string with no
    foreign key** to `releases`. A version nothing carries therefore matches
    nothing rather than erroring, and a ticket whose version no longer exists
    still matches that version -- both are honest readings of the column.

    ``current`` resolves through ``next_release``, the same helper the dashboard,
    the Releases tab and ``/releases/current/tickets`` use, so none of them can
    name a different version than another.
    """
    project = session.get(Project, project_id)
    if not project:
        raise not_found("Project", project_id)
    if project.organization_id != organization_id:
        raise HTTPException(
            status_code=403, detail="Project belongs to a different organization"
        )

    statement = select(Ticket).where(Ticket.project_id == project_id)
    statement = statement.where(Ticket.deleted_at.is_(None))

    if status:
        statement = statement.where(Ticket.status == status)
    else:
        statement = statement.where(Ticket.status != TicketStatus.DRAFT)
    if assignee:
        statement = statement.where(Ticket.assignee == assignee)
    if assigned_to:
        statement = statement.where(Ticket.assigned_to == assigned_to)
    if release:
        statement = statement.where(
            Ticket.release
            == _resolve_release_filter(release, organization_id, project_id, session)
        )

    return session.exec(statement).all()


@router.get(
    "/{organization_id}/projects/{project_id}/tickets/current-release",
    response_model=List[Ticket],
)
async def get_project_current_release_tickets(
    organization_id: str,
    project_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """The tickets in the release this project is cutting. Nothing to pass.

    The same answer as ``?release=current`` on the collection above, as a route
    something can be pointed at without composing a query string. Both the
    organization and the project are path segments, so there is no parameter to
    get wrong and no version to know in advance.

    Returns plain ``Ticket`` rows. ``/releases/current/tickets`` returns the
    *release* with its tickets nested -- that one answers "what is this release"
    and carries the version, notes and counts a summary needs; this one answers
    "which tickets".
    """
    project = session.get(Project, project_id)
    if not project:
        raise not_found("Project", project_id)
    if project.organization_id != organization_id:
        raise HTTPException(
            status_code=403, detail="Project belongs to a different organization"
        )

    version = _resolve_release_filter(
        CURRENT_RELEASE, organization_id, project_id, session
    )
    return session.exec(
        select(Ticket).where(
            Ticket.project_id == project_id,
            Ticket.release == version,
            Ticket.deleted_at.is_(None),
            Ticket.status != TicketStatus.DRAFT,
        )
    ).all()


@router.get(
    "/{organization_id}/projects/{project_id}/tickets/unreleased",
    response_model=List[Ticket],
)
async def get_project_unreleased_tickets(
    organization_id: str,
    project_id: str,
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Finished work that never carried a version -- the release-note candidates.

    ``release IS NULL OR release = ''``, because board sync writes an **empty
    string** when a ticket carries no version label. Testing only for NULL files
    those under "planned into something named", which is not a distinction
    anyone means. This is the same predicate the Releases tab has used since
    PF-398 (``webui/data.py``'s ``done_unreleased``), promoted to the API so the
    workflow page can ask for it without re-deriving the rule -- and so the two
    surfaces cannot drift into disagreeing about what "unreleased" means.

    ``CANCELLED`` is excluded by the ``DONE``-only filter rather than lumped in:
    cancelled work never shipped, so offering it for a release would misreport
    what that release contained.

    Newest movement first and no status sort -- they are all DONE, so the only
    useful order is "most recently finished", which is also the most likely to
    belong in the release being cut.
    """
    # `resolve_project`, so `{project_id}` accepts a UUID, an alias or a name --
    # what every scrum route on the same page already accepts, and what
    # `resolve_project` exists to make uniform. A bare `session.get` took the
    # UUID only, so `.../projects/pf/tickets/unreleased` 404d beside
    # `.../projects/pf/scrums`, which is a difference nobody could have
    # predicted from the URLs. It resolves within `_org.id` -- the resolved org,
    # never the raw `{organization_id}` segment, which may itself be an alias --
    # and keeps the answers this route already gave: 404 for a reference that
    # names nothing, 403 for one that names another org's project.
    project = resolve_project(project_id, _org.id, session)

    return session.exec(
        select(Ticket)
        .where(
            Ticket.project_id == project.id,
            or_(Ticket.release.is_(None), Ticket.release == ""),  # type: ignore[union-attr]
            Ticket.deleted_at.is_(None),  # type: ignore[union-attr]
            Ticket.status == TicketStatus.DONE,
        )
        .order_by(Ticket.updated_at.desc())  # type: ignore[union-attr]
        .limit(limit)
    ).all()


# ============================================================================
# Board-level ticket endpoints
# ============================================================================


@router.get("/{organization_id}/boards/{board_id}/tickets", response_model=List[Ticket])
async def get_board_tickets(
    organization_id: str,
    board_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Get all tickets for a specific board"""
    # Verify organization exists
    resolve_organization(organization_id, session)

    # Verify board belongs to organization
    board = session.get(BoardRegistration, board_id)
    if not board or board.organization_id != organization_id:
        raise HTTPException(
            status_code=404, detail="Board not found in this organization"
        )

    # Get tickets for this board
    statement = select(Ticket).where(Ticket.board_registration_id == board_id)
    statement = statement.where(Ticket.deleted_at.is_(None))
    tickets = session.exec(statement).all()

    return tickets


@router.post(
    "/{organization_id}/boards/{board_id}/tickets/local-only", response_model=Ticket
)
async def create_ticket(
    organization_id: str,
    board_id: str,
    ticket_data: TicketCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """
    Create an InnoDay-only ticket associated with a board, without writing to
    the external board (Trello/Jira/Linear).

    NOTE: this path was previously the same as
    POST /{organization_id}/boards/{board_id}/tickets, which silently shadowed
    src/routers/boards.py's create_board_ticket (the endpoint that actually
    writes to the external board) since both routers were registered under
    the same prefix and FastAPI dispatches to whichever route was registered
    first. That collision meant every "create a ticket on the external board"
    request silently created an InnoDay-only ticket instead. Moved to this
    distinct path to make the two behaviors unambiguous; nothing depended on
    the old shared path (verified: the CLI and MCP create_ticket call the
    org-scoped, non-board route; only create_board_ticket used the old
    shared path, and it wanted boards.py's behavior, not this one's).
    """
    # Verify organization exists
    resolve_organization(organization_id, session)

    # Verify board belongs to organization
    board = session.get(BoardRegistration, board_id)
    if not board or board.organization_id != organization_id:
        raise HTTPException(
            status_code=404, detail="Board not found in this organization"
        )

    # Check license limits
    if not can_create_ticket(organization_id, current_user.id, session):
        raise HTTPException(
            status_code=402, detail="Ticket creation limit exceeded for current license"
        )

    # Create ticket -- project_id comes from the board (required, per
    # BoardRegistration.project_id), not from the request body. So that is the
    # project the release must be outstanding on: a version string only means
    # anything inside one project.
    #
    # **`ticket_data.project_id` is therefore never read on this route**, which is
    # why it is not passed through `resolve_project_ref` like every other inbound
    # project ref, and why it is named in this route's exemption in
    # `tests/test_project_refs_are_resolved.py`. Resolving it would add a 404 for
    # a value that currently changes nothing.
    release = (
        _resolve_release_for_write(
            ticket_data.release, organization_id, board.project_id, session
        )
        if ticket_data.release is not None
        else None
    )

    ticket = Ticket(
        summary=ticket_data.summary,
        description=ticket_data.description,
        assignee=ticket_data.assignee,
        status=ticket_data.status,
        release=release,
        organization_id=organization_id,
        project_id=board.project_id,
        board_registration_id=board_id,
        created_by=ticket_data.created_by or current_user.id,
    )

    session.add(ticket)
    session.commit()
    session.refresh(ticket)

    # Track usage
    track_usage(organization_id, current_user.id, "ticket_created", session)

    return ticket


@router.get(
    "/{organization_id}/boards/{board_id}/tickets/{ticket_id}", response_model=Ticket
)
async def get_ticket(
    organization_id: str,
    board_id: str,
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Get a specific ticket"""
    # Verify organization exists
    resolve_organization(organization_id, session)

    # Get ticket and verify it belongs to this board/org
    ticket = session.get(Ticket, ticket_id)
    if (
        not ticket
        or ticket.organization_id != organization_id
        or ticket.board_registration_id != board_id
    ):
        raise not_found("Ticket", str(ticket_id))

    return ticket


@router.put(
    "/{organization_id}/boards/{board_id}/tickets/{ticket_id}", response_model=Ticket
)
async def update_ticket(
    organization_id: str,
    board_id: str,
    ticket_id: int,
    ticket_update: TicketUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """Update a ticket"""
    # Get ticket and verify it belongs to this board/org
    ticket = session.get(Ticket, ticket_id)
    if (
        not ticket
        or ticket.organization_id != organization_id
        or ticket.board_registration_id != board_id
    ):
        raise not_found("Ticket", str(ticket_id))

    # Update fields
    if ticket_update.summary is not None:
        ticket.summary = ticket_update.summary
    if ticket_update.description is not None:
        ticket.description = ticket_update.description
    if ticket_update.assignee is not None:
        ticket.assignee = ticket_update.assignee
    if ticket_update.status is not None:
        ticket.status = ticket_update.status

    # **The destination project is resolved before the release, and the release
    # before either is assigned.** One PUT can move a ticket and set its version
    # together; validating against the project it arrived on would let it land on
    # project B carrying project A's version -- the orphaned state this validation
    # exists to prevent, manufactured by the code meant to prevent it. Nothing is
    # written to `ticket` until both have passed, so a rejected release does not
    # leave a half-applied move behind.
    destination_project_id = ticket.project_id
    if ticket_update.project_id is not None:
        # A body field: `normalize_path_refs` reaches path params only, so an
        # alias here 404'd on a project the caller can see. A UUID short-circuits,
        # leaving the cross-org check below to do exactly what it did before.
        ticket_update.project_id = resolve_project_ref(
            ticket_update.project_id, organization_id, session
        )
        project = session.get(Project, ticket_update.project_id)
        if not project or project.organization_id != organization_id:
            raise HTTPException(
                status_code=404, detail="Project not found in this organization"
            )
        destination_project_id = project.id

    # Keyed off the payload, never off `ticket.release`: board sync writes
    # unmatched external versions (`2026.08-hotfix`), and validating the stored
    # value would make every such ticket impossible to update at all.
    if ticket_update.release is not None:
        ticket.release = _resolve_release_for_write(
            ticket_update.release, organization_id, destination_project_id, session
        )
    ticket.project_id = destination_project_id

    session.add(ticket)
    session.commit()
    session.refresh(ticket)

    return ticket


async def _try_push_ticket_to_board(
    board: BoardRegistration,
    ticket_data: "TicketCreate",
    user_id: str,
    session: Session,
) -> Optional[Ticket]:
    """
    Best-effort push of a newly-created ticket to its project's external board.

    Returns the created board-linked Ticket on success, or None on any failure
    (missing credentials, adapter error, network) -- in which case the caller
    falls back to an InnoDay-only create. Never raises: a board being
    unreachable must not break ticket creation.

    The requested status (e.g. IN_PROGRESS) is passed through to the board:
    create_ticket_on_board applies it as a workflow-state transition after
    creating the issue (best-effort -- an unmatched state name is logged but
    does not fail the create).
    """
    # Imported lazily to keep the heavier service/adapter import graph out of
    # module load for the InnoDay-only path that never touches a board.
    from src.services.board_ticket_creation_service import (
        BoardTicketCreationService,
        TicketCreateRequest,
    )

    try:
        service = BoardTicketCreationService(session)
        request = TicketCreateRequest(
            summary=ticket_data.summary,
            description=ticket_data.description,
            assignee=ticket_data.assignee,
            # Pass the requested status through so the board reflects it too,
            # not just the InnoDay row. TicketStatus is a str enum; send its
            # value ("in progress", "todo", ...) which the adapter matches
            # case-insensitively against the board's own state names. The
            # service applies it as a best-effort transition; an unmatched
            # name is logged, not fatal.
            status=ticket_data.status.value if ticket_data.status else None,
        )
        response = await service.create_ticket_on_board(
            board_registration_id=board.id,
            ticket_data=request,
            user_id=user_id,
        )
        created = session.get(Ticket, response.id)
        if created is not None:
            logger.info(
                "Pushed ticket %s to board %s (%s) on create",
                created.id,
                board.board_name,
                board.board_type,
            )
        return created
    except Exception:  # noqa: BLE001 -- best-effort; log and fall back
        # Roll back any partial board-side DB writes so the fallback
        # InnoDay-only create starts from a clean session.
        session.rollback()
        logger.warning(
            "Board push failed for new ticket on board %s (%s); "
            "falling back to InnoDay-only create",
            board.id,
            board.board_type,
            exc_info=True,
        )
        return None


@router.post("/{organization_id}/tickets", response_model=Ticket)
async def create_ticket_by_id(
    organization_id: str,
    ticket_data: TicketCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """
    Create a ticket scoped only to the organization (no board_id required).

    This mirrors the board-scoped `create_ticket` endpoint above but is used by
    clients (CLI, MCP server) that create standalone tickets not tied to any
    board — e.g. DRAFT tickets captured directly by a developer or agent.
    project_id is required -- a ticket must always belong to a project.
    """

    # Verify organization exists
    resolve_organization(organization_id, session)

    if not ticket_data.project_id:
        raise HTTPException(
            status_code=400,
            detail="project_id is required -- a ticket must belong to a project",
        )

    # A body field, so `normalize_path_refs` never saw it. `{"project_id": "PF"}`
    # answered "Project not found in this organization" for a project the caller
    # is a member of -- while the CLI's own docs say an alias works anywhere a
    # UUID does. A UUID short-circuits, so the org check below is unchanged.
    ticket_data.project_id = resolve_project_ref(
        ticket_data.project_id, organization_id, session
    )

    project = session.get(Project, ticket_data.project_id)
    if not project or project.organization_id != organization_id:
        raise HTTPException(
            status_code=404, detail="Project not found in this organization"
        )

    # Before the board push below, not after: a 422 must cost nothing, and a
    # ticket already created on Linear cannot be un-created. Only when one was
    # actually submitted -- a create that names no release reads no releases, so
    # a project with none can still take tickets.
    release = (
        _resolve_release_for_write(
            ticket_data.release, organization_id, ticket_data.project_id, session
        )
        if ticket_data.release is not None
        else None
    )

    # Check license limits
    if not can_create_ticket(organization_id, current_user.id, session):
        raise HTTPException(
            status_code=402, detail="Ticket creation limit exceeded for current license"
        )

    # If the project has an active external board, push the ticket straight
    # to it now instead of leaving it InnoDay-only (which previously required
    # a separate board sync -- and sync only pulls *from* the board, so an
    # InnoDay-created ticket never reached Linear/Jira/Trello at all). This is
    # best-effort: any failure to reach the board falls back to creating the
    # plain InnoDay-only ticket so ticket creation never breaks on a board
    # outage. See create_ticket_on_board, which creates the single
    # board-linked row itself (populating source_platform/external_ticket_id/
    # url) -- so we do NOT pre-create an InnoDay row in the board path, to
    # avoid a duplicate.
    if ticket_data.push_to_board:
        board = session.exec(
            select(BoardRegistration).where(
                BoardRegistration.project_id == ticket_data.project_id,
                BoardRegistration.is_active == True,  # noqa: E712
            )
        ).first()

        if board is not None:
            pushed = await _try_push_ticket_to_board(
                board, ticket_data, current_user.id, session
            )
            if pushed is not None:
                # **The board path drops the release unless it is set here.** The
                # row comes back from BoardTicketCreationService, whose
                # TicketCreateRequest has no `release` field, so the endpoint
                # would answer 200 with `release: null` -- a create that looks
                # like it worked and did not. `push_to_board` defaults to true,
                # so this is the common path, not an edge case.
                if release is not None:
                    pushed.release = release
                    session.add(pushed)
                    session.commit()
                    session.refresh(pushed)
                track_usage(organization_id, current_user.id, "ticket_created", session)
                return pushed
            # else: push failed -- fall through to InnoDay-only create below.

    ticket = Ticket(
        summary=ticket_data.summary,
        description=ticket_data.description,
        assignee=ticket_data.assignee,
        status=ticket_data.status,
        release=release,
        organization_id=organization_id,
        project_id=ticket_data.project_id,
        created_by=ticket_data.created_by or current_user.id,
    )

    session.add(ticket)
    session.commit()
    session.refresh(ticket)

    track_usage(organization_id, current_user.id, "ticket_created", session)

    return ticket


@router.get("/{organization_id}/tickets/{ticket_id}", response_model=Ticket)
async def get_ticket_by_id(
    organization_id: str,
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """
    Get a single ticket by ID, scoped only to the organization (no board_id
    required). Mirrors update_ticket_by_id's org-scoped pattern below; used by
    clients (CLI `tickets show`, MCP server) that know the ticket's
    organization and ID, not which board it lives on. Without this route the
    org-scoped path had only PUT/POST registered, so a GET returned 405.
    """

    ticket = session.get(Ticket, ticket_id)
    if not ticket or ticket.organization_id != organization_id:
        raise not_found("Ticket", str(ticket_id))

    return ticket


@router.put("/{organization_id}/tickets/{ticket_id}", response_model=Ticket)
async def update_ticket_by_id(
    organization_id: str,
    ticket_id: int,
    ticket_update: TicketUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """
    Update a ticket by ID, scoped only to the organization (no board_id required).

    This mirrors the board-scoped `update_ticket` endpoint above but is used by
    clients (CLI, MCP server) that only know the ticket's organization and ID,
    not which board it lives on.
    """

    # Get ticket and verify it belongs to this organization
    ticket = session.get(Ticket, ticket_id)
    if not ticket or ticket.organization_id != organization_id:
        raise not_found("Ticket", str(ticket_id))

    # Update fields
    if ticket_update.summary is not None:
        ticket.summary = ticket_update.summary
    if ticket_update.description is not None:
        ticket.description = ticket_update.description
    if ticket_update.assignee is not None:
        ticket.assignee = ticket_update.assignee
    if ticket_update.status is not None:
        ticket.status = ticket_update.status

    # **The destination project is resolved before the release, and the release
    # before either is assigned.** One PUT can move a ticket and set its version
    # together; validating against the project it arrived on would let it land on
    # project B carrying project A's version -- the orphaned state this validation
    # exists to prevent, manufactured by the code meant to prevent it. Nothing is
    # written to `ticket` until both have passed, so a rejected release does not
    # leave a half-applied move behind.
    destination_project_id = ticket.project_id
    if ticket_update.project_id is not None:
        # A body field: `normalize_path_refs` reaches path params only, so an
        # alias here 404'd on a project the caller can see. A UUID short-circuits,
        # leaving the cross-org check below to do exactly what it did before.
        ticket_update.project_id = resolve_project_ref(
            ticket_update.project_id, organization_id, session
        )
        project = session.get(Project, ticket_update.project_id)
        if not project or project.organization_id != organization_id:
            raise HTTPException(
                status_code=404, detail="Project not found in this organization"
            )
        destination_project_id = project.id

    # Keyed off the payload, never off `ticket.release`: board sync writes
    # unmatched external versions (`2026.08-hotfix`), and validating the stored
    # value would make every such ticket impossible to update at all.
    if ticket_update.release is not None:
        ticket.release = _resolve_release_for_write(
            ticket_update.release, organization_id, destination_project_id, session
        )
    ticket.project_id = destination_project_id

    session.add(ticket)
    session.commit()
    session.refresh(ticket)

    return ticket


def _cancel_ticket(
    ticket: Ticket,
    note: str,
    current_user: User,
    session: Session,
) -> Ticket:
    """Shared soft-cancel logic: set status to CANCELLED and record the
    mandatory note as a comment, atomically. Tickets are never hard-deleted --
    see GH #291."""
    ticket.status = TicketStatus.CANCELLED
    session.add(ticket)

    comment = TicketComment(
        ticket_id=ticket.id,
        comment=note,
        commenter_id=current_user.id,
    )
    session.add(comment)

    session.commit()
    session.refresh(ticket)
    return ticket


@router.post("/{organization_id}/tickets/{ticket_id}/cancel", response_model=Ticket)
async def cancel_ticket_by_id(
    organization_id: str,
    ticket_id: int,
    cancel_request: TicketCancel,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """
    Cancel a ticket by ID, scoped only to the organization (no board_id
    required). Soft-cancel only -- sets status to CANCELLED and records the
    mandatory note as a comment; never removes the row. Mirrors
    update_ticket_by_id's org-scoped pattern above, used by clients (CLI, MCP
    server) that only know the ticket's organization and ID, not its board.
    """

    ticket = session.get(Ticket, ticket_id)
    if not ticket or ticket.organization_id != organization_id:
        raise not_found("Ticket", str(ticket_id))

    return _cancel_ticket(ticket, cancel_request.note, current_user, session)


@router.delete("/{organization_id}/boards/{board_id}/tickets/{ticket_id}")
async def delete_ticket(
    organization_id: str,
    board_id: str,
    ticket_id: int,
    cancel_request: TicketCancel,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.ADMIN)),
):
    """Cancel a board-scoped ticket. Kept for board-scoped callers; behaves
    identically to the org-scoped cancel above -- soft-cancel only, never a
    true delete. Despite the HTTP verb, this never removes the row -- see
    GH #291."""
    # Get ticket and verify it belongs to this board/org
    ticket = session.get(Ticket, ticket_id)
    if (
        not ticket
        or ticket.organization_id != organization_id
        or ticket.board_registration_id != board_id
    ):
        raise not_found("Ticket", str(ticket_id))

    return _cancel_ticket(ticket, cancel_request.note, current_user, session)


# ============================================================================
# Ticket synchronization endpoints
# ============================================================================


@router.post("/{organization_id}/boards/{board_id}/tickets/sync")
async def sync_board_tickets(
    organization_id: str,
    board_id: str,
    background_tasks: BackgroundTasks,
    x_integration_token: str = Header(..., alias="X-Integration-Token"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """Synchronize tickets from the external board"""
    resolve_organization(organization_id, session)

    board = session.get(BoardRegistration, board_id)
    if not board or board.organization_id != organization_id:
        raise HTTPException(
            status_code=404, detail="Board not found in this organization"
        )

    sync_history = BoardSyncHistory(
        id=str(uuid4()),
        board_registration_id=board_id,
        sync_status=SyncStatus.PENDING,
        tickets_found=0,
        tickets_created=0,
        tickets_updated=0,
        tickets_skipped=0,
        started_at=datetime.now(timezone.utc),
    )
    session.add(sync_history)
    session.commit()
    session.refresh(sync_history)

    background_tasks.add_task(
        sync_board_tickets_task,
        registration_id=board_id,
        sync_history_id=sync_history.id,
        token=x_integration_token,
    )

    return {
        "status": "sync_started",
        "sync_id": sync_history.id,
        "message": f"Synchronization started for board {board.board_name}",
        "board_id": board_id,
    }


# ============================================================================
# Ticket comment endpoints
# ============================================================================


@router.post(
    "/{organization_id}/tickets/{ticket_id}/comments", response_model=TicketComment
)
async def create_ticket_comment(
    organization_id: str,
    ticket_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Add a comment to a ticket"""
    # Verify ticket exists and belongs to organization
    ticket = session.get(Ticket, ticket_id)
    if not ticket or ticket.organization_id != organization_id:
        raise not_found("Ticket", str(ticket_id))

    # Create comment
    comment = TicketComment(
        ticket_id=ticket_id,
        comment=comment_data.comment,
        commenter_id=comment_data.commenter_id or current_user.id,
        parent_comment_id=comment_data.parent_comment_id,
    )

    session.add(comment)
    session.commit()
    session.refresh(comment)

    return comment


@router.get(
    "/{organization_id}/tickets/{ticket_id}/comments",
    response_model=List[TicketComment],
)
async def get_ticket_comments(
    organization_id: str,
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Get all comments for a ticket"""
    # Verify ticket exists and belongs to organization
    ticket = session.get(Ticket, ticket_id)
    if not ticket or ticket.organization_id != organization_id:
        raise not_found("Ticket", str(ticket_id))

    # Get comments
    statement = select(TicketComment).where(TicketComment.ticket_id == ticket_id)
    comments = session.exec(statement).all()

    return comments


# ============================================================================
# Unified work endpoint
# ============================================================================


@router.get("/{organization_id}/work", response_model=List[UnifiedWorkItem])
async def get_unified_work(
    organization_id: str,
    type: Optional[str] = None,
    source_platform: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assignee: Optional[str] = None,
    limit: int = Query(100, ge=1, le=MAX_UNIFIED_WORK_LIMIT),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """
    Get all work items across all boards and repositories for an organization.

    Merges board tickets (Trello, Jira, Notion, Linear) and GitHub issues
    into a single unified list, sorted by updated_at descending.

    Filtering, ordering and bounding all happen in SQL. The two sources have
    different shapes so the final merge is still in Python, but each side is
    capped at ``offset + limit`` rows — the most that can possibly contribute
    to this page, since each source's items keep their relative order in the
    merged list. Previously every ticket and issue in the org was loaded to
    produce one page, and ``limit``/``offset`` were unvalidated.
    """
    resolve_organization(organization_id, session)

    window = offset + limit
    items: List[UnifiedWorkItem] = []

    if type is None or type == "ticket":
        tickets = get_org_tickets(
            session,
            organization_id,
            source_platform=source_platform,
            status=status,
            priority=priority,
            assignee=assignee,
            newest_first=True,
            max_rows=window,
        )
        for t in tickets:
            sp = t.source_platform or "unknown"
            t_status = t.status.value if hasattr(t.status, "value") else str(t.status)
            items.append(
                UnifiedWorkItem(
                    type="ticket",
                    id=str(t.id),
                    summary=t.summary,
                    description=t.description,
                    status=t_status,
                    priority=t.priority,
                    source_platform=sp,
                    assignee=t.assignee,
                    url=t.url,
                    external_id=t.external_ticket_id,
                    parent_external_id=t.parent_external_id,
                    created_at=t.created_at,
                    updated_at=t.updated_at,
                )
            )

    if type is None or type == "github_issue":
        # A repo issue records no priority or assignee, and its only statuses
        # are open/closed — so any of those filters excludes the whole branch
        # rather than being applied row by row (which is what the old Python
        # filtering did, after loading every issue).
        branch_matches = (
            (source_platform is None or source_platform == "github")
            and not priority
            and not assignee
            and (status is None or status in ("open", "closed"))
        )
        if branch_matches:
            issues = get_org_github_issues(
                session,
                organization_id,
                is_open=(status == "open") if status else None,
                newest_first=True,
                max_rows=window,
            )
            for issue in issues:
                gh_status = "open" if issue.is_open else "closed"
                items.append(
                    UnifiedWorkItem(
                        type="github_issue",
                        id=str(issue.id),
                        summary=issue.title,
                        description=issue.body,
                        status=gh_status,
                        priority=None,
                        source_platform="github",
                        assignee=None,
                        url=issue.github_url,
                        external_id=str(issue.github_issue_id),
                        parent_external_id=None,
                        created_at=issue.created_at,
                        updated_at=issue.updated_at,
                    )
                )

    items.sort(key=lambda x: x.updated_at or datetime.min, reverse=True)
    return items[offset : offset + limit]


# ---------------------------------------------------------------------------
# Attaching a pull request to a ticket, by hand
# ---------------------------------------------------------------------------


class PullRequestTicketLink(BaseModel):
    """Which ticket a pull request belongs to, when it does not say so itself."""

    ticket_ref: str = Field(
        description="The ticket's reference, e.g. BPAI-417, as the summary printed it"
    )


def _linked_repository(session: Session, project: Project, repo: str) -> Repository:
    """The named repository, if it is linked to this project."""
    row = session.exec(
        select(Repository)
        .join(ProjectRepository, ProjectRepository.repository_id == Repository.id)
        .where(
            ProjectRepository.project_id == project.id,
            ProjectRepository.is_active == True,  # noqa: E712
            func.lower(Repository.name) == repo.lower(),
        )
    ).first()
    if row is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"'{repo}' is not a repository on this project, so a pull "
                "request in it cannot be attached to one of its tickets."
            ),
        )
    return row


@router.put(
    "/{organization_id}/projects/{project_ref}/pull-requests/{repo}/{number}/ticket",
    summary="Attach a pull request to a ticket",
)
async def attach_pull_request(
    organization_id: str,
    project_ref: str,
    repo: str,
    number: int,
    body: PullRequestTicketLink,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """Record that this pull request delivered that ticket.

    **Nothing infers this.** Every other ticket-to-pull-request link is derived
    per request from the branch, the title, then the description -- and on a
    real release ten of thirty-four pull requests said it in none of them. A
    summary proposes a match from the commits; this route is where a person's
    agreement is written down.

    The row is created if the sync has never seen this pull request. The
    pull-request table only ever held what was open at some sync, so a pull
    request that opened and merged between two syncs has no row at all -- and
    "we never saw it" is not a reason to refuse a link somebody is making.
    """
    from src.domain.repository_pull_request import RepositoryPullRequest
    from src.services.ticket_matching import tickets_by_ref

    org = resolve_organization(organization_id, session)
    project = resolve_project(project_ref, org.id, session)
    repository = _linked_repository(session, project, repo)

    tickets = list(
        session.exec(
            select(Ticket).where(
                Ticket.project_id == project.id,
                Ticket.deleted_at.is_(None),
            )
        ).all()
    )
    ticket = tickets_by_ref(project.alias or "", tickets).get(body.ticket_ref.upper())
    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail=f"No ticket on this project answers to '{body.ticket_ref}'.",
        )

    row = session.exec(
        select(RepositoryPullRequest).where(
            RepositoryPullRequest.repository_id == repository.id,
            RepositoryPullRequest.number == number,
        )
    ).first()
    if row is None:
        row = RepositoryPullRequest(
            repository_id=repository.id,
            number=number,
            title="",
            url=f"https://github.com/{repository.full_name}/pull/{number}",
            state="closed",
        )
    row.ticket_id = ticket.id
    session.add(row)
    session.commit()

    return {
        "attached": True,
        "repo": repository.name,
        "number": number,
        "ticket_ref": body.ticket_ref.upper(),
        "ticket_id": ticket.id,
        "title": ticket.summary,
    }


@router.delete(
    "/{organization_id}/projects/{project_ref}/pull-requests/{repo}/{number}/ticket",
    summary="Detach a pull request from a ticket",
)
async def detach_pull_request(
    organization_id: str,
    project_ref: str,
    repo: str,
    number: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """Undo a hand-made attachment, leaving derivation to take over again.

    Only the manual link is cleared. A pull request whose branch names its
    ticket goes on matching afterwards, because that was never this column's
    doing.
    """
    from src.domain.repository_pull_request import RepositoryPullRequest

    org = resolve_organization(organization_id, session)
    project = resolve_project(project_ref, org.id, session)
    repository = _linked_repository(session, project, repo)

    row = session.exec(
        select(RepositoryPullRequest).where(
            RepositoryPullRequest.repository_id == repository.id,
            RepositoryPullRequest.number == number,
        )
    ).first()
    if row is None or row.ticket_id is None:
        raise HTTPException(
            status_code=404,
            detail=f"{repository.name}#{number} is not attached to a ticket by hand.",
        )
    row.ticket_id = None
    session.add(row)
    session.commit()
    return {"attached": False, "repo": repository.name, "number": number}
