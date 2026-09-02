"""
Consolidated Board Management API Router

Provides REST API endpoints for:
- Board registration and synchronization
- Ticket creation on boards with AI support
- AI-powered board summaries

This router consolidates functionality from:
- boards.py (registration/sync)
- board_tickets.py (ticket creation)
- board_summaries.py (AI summaries, now the `summaries` table)
"""

import logging
import random
import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

import httpx
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Header,
    HTTPException,
    Query,
)
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlmodel import Session, select

from src.adapters import BoardAdapterError
from src.api.linear_api import is_uuid
from src.database import get_session
from src.domain import (
    BoardRegistration,
    BoardSyncHistory,
    BoardType,
    Organization,
    OrganizationRole,
    Project,
    Summary,
    SummaryType,
    SyncStatus,
    Ticket,
    TicketStatus,
    TimelineEventType,
    User,
)
from src.middleware.rbac import (
    conflict,
    get_current_user,
    not_found,
    require_org_role,
    resolve_organization,
    resolve_project_ref,
)
from src.services.board_clear_service import clear_board_tickets, soft_delete_board
from src.services.board_credential_service import (
    get_board_credential_payload,
    legacy_token_to_payload,
    payload_to_legacy_token,
    set_board_credential,
)
from src.services.board_sync_service import board_sync_service, sync_board_tickets_task
from src.services.board_ticket_creation_service import (
    BoardTicketCreationService,
    BulkTicketCreateRequest,
    BulkTicketCreateResponse,
    TicketCreateRequest,
    TicketCreateResponse,
)
from src.services.claude_ticket_parser import (
    ClaudeTicketParser,
    ParsedTicket,
    TicketParseRequest,
    TicketParseResponse,
)
from src.services.jira_oauth_service import (
    JiraOAuthError,
    build_authorize_url,
    exchange_code_for_tokens,
    parse_and_verify_state,
    resolve_cloud_id,
)
from src.services.org_credential_service import get_github_credentials
from src.services.project_timeline_writer import add_timeline_entry
from src.services.workspace_onboard import WorkspaceOnboardService
from src.utils.time_windows import as_utc

logger = logging.getLogger(__name__)

# Initialize router with unified API prefix
router = APIRouter(prefix="/api/v1", tags=["boards"])


# ============================================================================
# Request/Response Models
# ============================================================================


# Board Registration Models
class BoardRegistrationCreate(BaseModel):
    """Request model for creating a board registration"""

    board_url: str = Field(..., description="Full URL to the board (Trello/Jira)")
    board_name: str = Field(
        ..., max_length=255, description="Display name for the board"
    )
    board_type: BoardType = Field(..., description="Type of board (trello or jira)")
    project_id: str = Field(
        ...,
        description=(
            "Project this board belongs to (required -- a board cannot exist "
            "without a project). Must belong to the same organization."
        ),
    )

    @field_validator("board_url")
    @classmethod
    def validate_board_url(cls, v, info):
        """Validate board URL format based on board type"""
        board_type = info.data.get("board_type")

        if board_type == BoardType.TRELLO:
            if not re.match(r"https://trello\.com/b/[\w]+", v):
                raise ValueError(
                    "Invalid Trello board URL format. Expected: https://trello.com/b/{board_id}"
                )
        elif board_type == BoardType.JIRA:
            if not re.match(r"https://[\w\-]+\.atlassian\.net/", v):
                raise ValueError(
                    "Invalid Jira URL format. Expected Atlassian hosted instance."
                )
        elif board_type == BoardType.NOTION:
            # Notion database URLs: https://www.notion.so/{database_id}?v={view_id}
            # Database ID is 32-char hex string (may have hyphens in UUID format)
            if not re.match(r"https://(?:www\.)?notion\.so/[a-f0-9]{32}", v):
                raise ValueError(
                    "Invalid Notion database URL. Expected: https://www.notion.so/{database_id}"
                )
        elif board_type == BoardType.LINEAR:
            if not re.match(r"https://linear\.app/.+/team/.+", v):
                raise ValueError(
                    "Invalid Linear team URL. Expected: https://linear.app/{workspace}/team/{team-key}"
                )
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "board_url": "https://trello.com/b/abc123/my-project-board",
                "board_name": "My Project Board",
                "board_type": "trello",
            }
        }
    )


class BoardRegistrationUpdate(BaseModel):
    """Request model for updating a board registration"""

    board_name: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None
    auto_sync_enabled: Optional[bool] = None
    sync_frequency_hours: Optional[int] = Field(None, ge=1, le=168)


class BoardRegistrationResponse(BaseModel):
    """Response model for board registration data"""

    id: str
    user_id: str
    organization_id: str
    project_id: str
    board_name: str
    board_url: str
    board_type: BoardType
    board_external_id: str
    is_active: bool
    auto_sync_enabled: bool
    sync_frequency_hours: Optional[int]
    created_at: datetime
    updated_at: datetime
    last_sync_at: Optional[datetime]
    sync_status: Optional[SyncStatus] = None
    last_sync_tickets: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# Sync Models
class SyncRequest(BaseModel):
    """Request model for triggering board synchronization"""

    full_sync: bool = Field(
        default=False, description="Perform full sync vs incremental"
    )
    dry_run: bool = Field(default=False, description="Preview changes without applying")
    force: bool = Field(
        default=False, description="Force sync even if recent sync exists"
    )
    since: Optional[datetime] = Field(
        default=None,
        description=(
            "Only re-process tickets the board says moved at or after this "
            "instant. Tickets InnoDay has never seen are still imported "
            "however old they are, so this narrows work, never coverage. "
            "Omitted (the default) processes everything, unchanged."
        ),
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"full_sync": False, "dry_run": False, "force": False}
        }
    )


class SyncResponse(BaseModel):
    """Response model for sync operations"""

    sync_id: str
    status: SyncStatus
    message: str
    tickets_found: Optional[int] = None
    tickets_created: Optional[int] = None
    tickets_updated: Optional[int] = None
    started_at: datetime
    estimated_completion: Optional[datetime] = None


class TicketFieldsResponse(BaseModel):
    """Ticket fields returned by a single-ticket sync"""

    id: int
    summary: str
    description: Optional[str] = None
    status: TicketStatus
    url: Optional[str] = None
    release: Optional[str] = None
    priority: Optional[str] = None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TicketSyncResponse(BaseModel):
    """Response model for single-ticket sync"""

    ticket: TicketFieldsResponse
    was_created: bool


# Ticket Creation Models
class ParseAndCreateRequest(BaseModel):
    """Request to parse text and create tickets from it"""

    text: str = Field(..., description="Text to parse into tickets")
    context: Optional[str] = Field(None, description="Context about the text")
    auto_create: bool = Field(False, description="Automatically create parsed tickets")
    board_id: str = Field(..., description="Board registration ID to create tickets on")
    default_list_id: Optional[str] = Field(None, description="Default Trello list ID")
    default_assignee: Optional[str] = Field(None, description="Default assignee")
    max_tickets: int = Field(10, description="Maximum tickets to create")


class ParseAndCreateResponse(BaseModel):
    """Response from parsing and optionally creating tickets"""

    parsed_tickets: List[ParsedTicket] = Field(
        ..., description="Tickets parsed from text"
    )
    created_tickets: List[TicketCreateResponse] = Field(
        default_factory=list, description="Tickets created on board"
    )
    failed_tickets: List[Dict] = Field(
        default_factory=list, description="Failed ticket creations"
    )
    parse_summary: str = Field(..., description="Summary of parsing")
    parse_confidence: float = Field(..., description="Confidence in parsing (0-1)")
    parse_notes: Optional[str] = Field(None, description="Notes from parsing")


# Summary Models
class SummarizeRequest(BaseModel):
    """Request model for board ticket summarization"""

    summary_type: SummaryType = Field(
        default=SummaryType.STATUS, description="Type of summary to generate"
    )
    include_comments: bool = Field(
        default=True, description="Include ticket comments in analysis"
    )
    max_comment_count: int = Field(
        default=3, ge=0, le=10, description="Maximum comments per ticket to analyze"
    )
    time_window_hours: Optional[int] = Field(
        default=24, ge=1, le=168, description="Time window for 'recent' items (hours)"
    )
    since_version: Optional[str] = Field(
        default=None,
        description="Git tag or version string to use as the baseline for release summaries (e.g. 'v1.4.0'). Only used when summary_type=release.",
    )
    github_org: Optional[str] = Field(
        default=None,
        description="GitHub org to fetch commits from for release summaries (e.g. 'havilandsoftware'). Defaults to org slug.",
    )


class SummaryResponse(BaseModel):
    """Response model for generated summaries"""

    id: str
    summary: str
    summary_type: SummaryType
    stats: Dict[str, Any]
    active_tickets: Optional[List[Dict[str, Any]]] = []
    recent_completions: Optional[List[Dict[str, Any]]] = []
    highlights: List[str]
    concerns: List[str]
    motivational_message: str
    generated_at: datetime
    generation_time_ms: int
    message: str


# ============================================================================
# Helper Functions
# ============================================================================


def extract_board_id(board_url: str, board_type: BoardType) -> str:
    """Extract the external board ID from the URL"""
    if board_type == BoardType.TRELLO:
        match = re.search(r"/b/([^/]+)", board_url)
        if match:
            return match.group(1)
        raise ValueError("Could not extract board ID from Trello URL")

    elif board_type == BoardType.JIRA:
        match = re.search(r"/boards/(\d+)", board_url)
        if match:
            return match.group(1)

        match = re.search(r"/projects/([A-Z]+)", board_url, re.IGNORECASE)
        if match:
            return match.group(1).upper()

        match = re.search(r"/browse/([A-Z]+)-", board_url, re.IGNORECASE)
        if match:
            return match.group(1).upper()

        raise ValueError("Could not extract board ID from Jira URL")

    elif board_type == BoardType.NOTION:
        # Extract 32-character hex database ID (with or without hyphens)
        # Notion IDs can be: a1b2c3d4... (32 chars) or a1b2c3d4-e5f6-... (UUID format)
        match = re.search(
            r"([a-f0-9]{32}|[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})",
            board_url,
        )
        if match:
            # Remove hyphens to get clean 32-char ID
            return match.group(1).replace("-", "")
        raise ValueError("Could not extract database ID from Notion URL")

    elif board_type == BoardType.LINEAR:
        match = re.search(r"/team/([A-Z0-9\-]+)", board_url, re.IGNORECASE)
        if match:
            return match.group(1).upper()
        raise ValueError("Could not extract team key from Linear URL")

    raise ValueError(f"Unsupported board type: {board_type}")


async def validate_board_access(
    board_external_id: str,
    board_type: BoardType,
    token: str,
    board_url: Optional[str] = None,
    auth_type: str = "basic",
    cloud_id: Optional[str] = None,
) -> bool:
    """
    Validate that the provided token can access the board.

    Makes a lightweight API call to the board provider to confirm credentials work.
    Token format:
      - Jira:   "email:api_token" (Basic Auth) -- or a raw OAuth 2.0 3LO
                access token when auth_type="oauth2" (validating a stored
                OAuth credential, not a raw incoming header value)
      - Linear: raw API key
      - Trello: raw token (API key validation skipped here)
      - GitHub: raw personal access token
      - Notion: raw integration secret

    auth_type/cloud_id only apply to Jira, and only matter when
    auth_type="oauth2": in that case `token` is treated as a Bearer access
    token and the request goes through
    https://api.atlassian.com/ex/jira/{cloud_id} instead of the Basic Auth
    email:api_token split -- see GitHub issue #296. Every other call site
    (raw X-Integration-Token headers on register_board/update_board_credential)
    keeps calling this with the default auth_type="basic", completely
    unaffected.
    """
    import httpx

    if not token or len(token.strip()) < 10:
        return False

    try:
        if board_type == BoardType.JIRA and auth_type == "oauth2":
            if not cloud_id:
                logger.warning("Jira OAuth validation requires cloud_id")
                return False
            oauth_base_url = f"https://api.atlassian.com/ex/jira/{cloud_id}"
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{oauth_base_url}/rest/api/3/myself",
                    headers={
                        "Accept": "application/json",
                        "Authorization": f"Bearer {token}",
                    },
                )
            if resp.status_code == 200:
                logger.info(
                    f"Jira OAuth credentials valid for board {board_external_id}"
                )
                return True
            logger.warning(f"Jira OAuth auth failed: HTTP {resp.status_code}")
            return False

        if board_type == BoardType.JIRA:
            if ":" not in token:
                logger.warning("Jira token must be 'email:api_token' format")
                return False
            email, api_token = token.split(":", 1)
            # Derive the Atlassian base URL from the board URL (e.g. https://company.atlassian.net)
            base_url = "https://atlassian.net"
            if board_url:
                m = re.match(r"(https://[^/]+\.atlassian\.net)", board_url)
                if m:
                    base_url = m.group(1)
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    f"{base_url}/rest/api/3/myself",
                    auth=(email, api_token),
                    headers={"Accept": "application/json"},
                )
            if resp.status_code == 200:
                logger.info(f"Jira credentials valid for board {board_external_id}")
                return True
            logger.warning(f"Jira auth failed: HTTP {resp.status_code}")
            return False

        elif board_type == BoardType.LINEAR:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    "https://api.linear.app/graphql",
                    json={"query": "{ viewer { id name } }"},
                    headers={
                        "Authorization": token,
                        "Content-Type": "application/json",
                    },
                )
            if resp.status_code == 200 and "errors" not in resp.json():
                return True
            logger.warning(f"Linear auth failed: HTTP {resp.status_code}")
            return False

        elif board_type == BoardType.TRELLO:
            # Trello requires both API key and token; we can only do a basic length check here
            logger.info(f"Trello board {board_external_id}: token length check passed")
            return True

        elif board_type == BoardType.NOTION:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    "https://api.notion.com/v1/users/me",
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Notion-Version": "2022-06-28",
                    },
                )
            return resp.status_code == 200

        else:
            # GitHub and unknown types: accept if token is non-empty
            return True

    except Exception as exc:
        logger.warning(f"Board access validation error for {board_type}: {exc}")
        return False


def _get_summary_prompt(summary_type: SummaryType) -> str:
    """Get the appropriate prompt for the summary type"""
    prompts = {
        SummaryType.STATUS: """
        Analyze the board and provide a comprehensive status summary in 3-4 detailed sentences:
        
        1. CURRENTLY ACTIVE TICKETS:
           - List ALL tickets that are IN PROGRESS with assignees and how long in status
           - List tickets IN TEST or IN REVIEW
           - Highlight any tickets that have been stuck (>3 days in same status)
        
        2. RECENTLY COMPLETED (Last 7 Days):
           - Summarize tickets completed in the last 7 days
           - Group by theme or feature area if patterns exist
           - Credit the team members who completed them
        
        3. LAST 48 HOURS ACTIVITY:
           - What was accomplished in the last 48 hours specifically?
           - Any new tickets started?
           - Velocity trends (accelerating/steady/slowing)
        
        4. CONCERNS & BLOCKERS:
           - Any tickets stuck or blocked?
           - Resource bottlenecks?
           - Items needing immediate attention?
        
        Provide a comprehensive overview that captures the team's momentum, achievements, and current focus areas.
        Be specific with ticket IDs and titles. Write 3-4 substantial sentences that provide meaningful insights
        about the board's current state, recent progress, and areas requiring attention. Include specific metrics
        and concrete examples where relevant. Aim for approximately 100-150 words total.
        """,
        SummaryType.DAILY: """
        Generate a daily standup summary focused on the last 24-48 hours.
        """,
        SummaryType.SPRINT: """
        Provide a sprint health overview.
        """,
        SummaryType.WEEKLY: """
        Create a weekly roundup.
        """,
        SummaryType.RELEASE: """
        Generate a release summary covering all work since the specified baseline version.

        Structure your response as:

        ## Release Summary

        ### Tickets Completed Since Last Release
        - List ALL DONE tickets with ticket IDs and titles
        - Group by theme or feature area if patterns emerge
        - Note any tickets still in progress (not yet ready for release)

        ### Commits Across Repositories
        - Summarize the commit history provided, grouped by repository
        - Highlight significant features, fixes, and refactors
        - Call out any breaking changes or migrations

        ### What's In This Release
        - 2-3 sentences describing the main themes of this release
        - Who contributed the most work
        - Any notable firsts or milestones

        ### Risks & Open Items
        - Any in-progress tickets not yet merged/completed
        - Technical debt introduced
        - Items to watch post-release

        Be specific with version numbers, repo names, commit SHAs (short), and ticket IDs.
        Aim for a thorough but scannable document that a team can share as their release notes.
        """,
        SummaryType.CUSTOM: """
        Provide a comprehensive summary of the board's current state.
        """,
    }
    return prompts.get(summary_type, prompts[SummaryType.STATUS])


# Motivational messages pool
MOTIVATIONAL_QUOTES = [
    "🚀 Houston, we have progress! Your team is crushing it!",
    "🎯 Bugs beware: This team means business!",
    "☕ Coffee levels critical, but productivity is astronomical!",
    "🦸 Not all heroes wear capes - some write code and move tickets!",
    "🎪 Step right up to the greatest sprint show on Earth!",
    "🏗️ Bob the Builder called - he wants tips from your team!",
    "🌟 If tickets were stars, you'd be navigating the galaxy!",
    "🍕 Pizza party worthy progress detected! (Virtual pizza counts too)",
    "🎮 Achievement unlocked: Sprint Warrior Level Up!",
    "🔥 Your velocity is so hot, it needs a fire extinguisher!",
]


# ============================================================================
# Board Registration & Management Endpoints
# ============================================================================


@router.post(
    "/organizations/{organization_id}/boards",
    response_model=BoardRegistrationResponse,
)
async def register_board(
    organization_id: str,
    board_data: BoardRegistrationCreate,
    token: str = Header(..., alias="X-Integration-Token"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """
    Register a board for synchronization.

    The integration token is passed in the X-Integration-Token header. It is
    validated, then persisted as an encrypted Supabase Vault secret
    (board_credentials table) so sync_board/create_board_ticket/etc. don't
    require the caller to re-supply it on every subsequent call.
    """
    # Validate organization exists and user has access
    organization = session.exec(
        select(Organization).where(Organization.id == organization_id)
    ).first()
    if not organization:
        raise not_found("Organization", organization_id)

    # Validate the project exists and belongs to this organization -- a board
    # cannot be registered without one. The ref is resolved first: it is a body
    # field, which `normalize_path_refs` cannot reach, so
    # `{"project_id": "PF"}` used to 404 here -- and `board register` is the one
    # call a new project makes before anything else works.
    board_data.project_id = resolve_project_ref(
        board_data.project_id, organization_id, session
    )
    project = session.exec(
        select(Project).where(
            Project.id == board_data.project_id,
            Project.organization_id == organization_id,
        )
    ).first()
    if not project:
        raise not_found("Project", board_data.project_id)

    # Extract board external ID from URL
    try:
        board_external_id = extract_board_id(
            board_data.board_url, board_data.board_type
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Linear's URL exposes the team's short key (e.g. "UI"), but its GraphQL
    # mutations (issueCreate, etc.) require the team's actual UUID. Resolve
    # here, once, at registration time, so board_external_id always stores
    # something usable for real API calls -- not just a human-readable
    # substring of the URL. (Found via a live test: a board registered from
    # a URL like linear.app/<workspace>/team/UI/all had board_external_id
    # equal to "UI", and every subsequent issueCreate failed with "Argument
    # Validation Error" on teamId until this resolution was added.)
    if board_data.board_type == BoardType.LINEAR and not is_uuid(board_external_id):
        from src.api.linear_api import LinearAPI

        linear_api = LinearAPI(api_key=token)
        resolved_id = await linear_api.resolve_team_id_by_key(board_external_id)
        if not resolved_id:
            raise HTTPException(
                status_code=400,
                detail=f"Could not resolve Linear team key '{board_external_id}' to a team ID. Check the board URL and token.",
            )
        board_external_id = resolved_id

    # Validate board access with token (don't store token)
    if not await validate_board_access(
        board_external_id, board_data.board_type, token, board_url=board_data.board_url
    ):
        raise HTTPException(
            status_code=403,
            detail="Cannot access board with provided token. Please check your credentials.",
        )

    # Check for existing registration
    existing = session.exec(
        select(BoardRegistration).where(
            BoardRegistration.organization_id == organization_id,
            BoardRegistration.board_external_id == board_external_id,
            BoardRegistration.board_type == board_data.board_type,
        )
    ).first()

    if existing:
        raise conflict("Board", board_external_id)

    # Create new registration
    registration = BoardRegistration(
        id=str(uuid4()),
        user_id=current_user.id,
        organization_id=organization_id,
        project_id=board_data.project_id,
        board_name=board_data.board_name,
        board_url=board_data.board_url,
        board_type=board_data.board_type,
        board_external_id=board_external_id,
        is_active=True,
        auto_sync_enabled=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    session.add(registration)
    registration_id = registration.id
    session.commit()

    add_timeline_entry(
        session,
        organization_id=organization_id,
        project_id=board_data.project_id,
        event_type=TimelineEventType.BOARD_ATTACHED,
        title="Board attached to project",
        summary=f"{board_data.board_name} ({board_data.board_type.value}) was attached to the project.",
        created_by=current_user.id,
        metadata={"board_registration_id": registration_id},
    )
    session.commit()

    try:
        payload = legacy_token_to_payload(board_data.board_type, token)
        set_board_credential(
            session, registration_id, organization_id, board_data.board_type, payload
        )
    except Exception as e:
        # Registration itself already succeeded and was already validated
        # against the real board -- don't fail the whole request over a
        # credential-persistence error, but make sure it's visible, since a
        # board with no stored credential will need a token supplied on
        # every subsequent call until this is retried.
        logger.error(f"Failed to persist credential for board {registration_id}: {e}")

    logger.info(f"Board registered: {registration_id} for user {current_user.id}")
    return registration


@router.get(
    "/organizations/{organization_id}/boards",
    response_model=List[BoardRegistrationResponse],
)
async def list_organization_boards(
    organization_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    active_only: bool = Query(
        default=True, description="Only return active board registrations"
    ),
    project_id: Optional[str] = Query(
        default=None, description="Filter to the board registered for this project"
    ),
    _org: Organization = Depends(require_org_role()),
):
    """List all board registrations for an organization"""
    # Validate organization exists
    organization = session.exec(
        select(Organization).where(Organization.id == organization_id)
    ).first()
    if not organization:
        raise not_found("Organization", organization_id)

    # Build query
    query = select(BoardRegistration).where(
        BoardRegistration.organization_id == organization_id
    )

    if active_only:
        query = query.where(BoardRegistration.is_active == True)

    if project_id:
        # A query parameter -- see `resolve_project_ref`. An alias here silently
        # returned no boards rather than the project's one.
        query = query.where(
            BoardRegistration.project_id
            == resolve_project_ref(project_id, organization_id, session)
        )

    # Execute query
    registrations = session.exec(
        query.order_by(BoardRegistration.created_at.desc())
    ).all()

    return [BoardRegistrationResponse.model_validate(reg) for reg in registrations]


@router.get(
    "/organizations/{organization_id}/boards/{board_id}",
    response_model=BoardRegistrationResponse,
)
async def get_board_registration(
    organization_id: str,
    board_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """Get a specific board registration by ID"""
    registration = session.exec(
        select(BoardRegistration).where(
            BoardRegistration.id == board_id,
            BoardRegistration.organization_id == organization_id,
        )
    ).first()

    if not registration:
        raise not_found("Board registration", board_id)

    return registration


@router.put(
    "/organizations/{organization_id}/boards/{board_id}",
    response_model=BoardRegistrationResponse,
)
async def update_board_registration(
    organization_id: str,
    board_id: str,
    update_data: BoardRegistrationUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """Update a board registration"""
    registration = session.exec(
        select(BoardRegistration).where(
            BoardRegistration.id == board_id,
            BoardRegistration.organization_id == organization_id,
        )
    ).first()

    if not registration:
        raise not_found("Board registration", board_id)

    # Apply updates
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(registration, field, value)

    registration.updated_at = datetime.now(timezone.utc)

    session.add(registration)
    session.commit()
    session.refresh(registration)

    logger.info(f"Board registration updated: {board_id}")
    return registration


class BoardCredentialUpdateResponse(BaseModel):
    board_id: str
    board_type: BoardType
    updated_at: datetime


@router.patch(
    "/organizations/{organization_id}/boards/{board_id}/credential",
    response_model=BoardCredentialUpdateResponse,
)
async def update_board_credential(
    organization_id: str,
    board_id: str,
    token: str = Header(..., alias="X-Integration-Token"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """
    Rotate the stored credential for an already-registered board.

    Validates the new token against the real board provider, then upserts
    it into Vault via set_board_credential (create_secret if this board has
    never had one stored, update_secret in place otherwise) -- same
    persistence path register_board uses, without re-registering the board
    itself. Use this when a token expires/rotates; register_board rejects
    boards that already exist (409 conflict), so this is the only way to
    replace a credential without deleting and recreating the registration.
    """
    registration = session.exec(
        select(BoardRegistration).where(
            BoardRegistration.id == board_id,
            BoardRegistration.organization_id == organization_id,
        )
    ).first()

    if not registration:
        raise not_found("Board registration", board_id)

    if not await validate_board_access(
        registration.board_external_id,
        registration.board_type,
        token,
        board_url=registration.board_url,
    ):
        raise HTTPException(
            status_code=403,
            detail="Cannot access board with provided token. Please check your credentials.",
        )

    payload = legacy_token_to_payload(registration.board_type, token)
    set_board_credential(
        session, board_id, organization_id, registration.board_type, payload
    )

    logger.info(f"Board credential rotated: {board_id}")
    return BoardCredentialUpdateResponse(
        board_id=board_id,
        board_type=registration.board_type,
        updated_at=datetime.now(timezone.utc),
    )


# ============================================================================
# Jira OAuth 2.0 (3LO) Endpoints -- GitHub issue #296
#
# Atlassian's edge rejects Basic Auth (email:api_token) for requests from
# this app's hosting platform's shared egress IPs, returning 401 with
# WWW-Authenticate: OAuth. These endpoints implement the durable fix --
# OAuth 2.0 (3LO) -- as a dual-mode addition: existing Basic Auth boards
# keep working unmodified (see update_board_credential above); boards that
# go through this flow instead get an {"auth_type": "oauth2", ...} Vault
# payload (see src.services.board_credential_service /
# src.services.jira_oauth_service).
# ============================================================================


class JiraOAuthAuthorizeResponse(BaseModel):
    """Response model for the Jira OAuth authorize kickoff endpoint."""

    authorize_url: str
    state: str


@router.get(
    "/organizations/{organization_id}/boards/{board_id}/oauth/jira/authorize",
    response_model=JiraOAuthAuthorizeResponse,
)
async def start_jira_oauth(
    organization_id: str,
    board_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """
    Build the Atlassian authorize URL for a Jira board.

    Returns the URL rather than issuing an HTTP redirect directly, so
    callers (browser-based UI or CLI) can choose how to present it --
    consent is a one-time, per-user, per-Jira-site browser click-through
    that can't be automated the way pasting an X-Integration-Token can.
    """
    registration = session.exec(
        select(BoardRegistration).where(
            BoardRegistration.id == board_id,
            BoardRegistration.organization_id == organization_id,
        )
    ).first()

    if not registration:
        raise not_found("Board registration", board_id)

    if registration.board_type != BoardType.JIRA:
        raise HTTPException(
            status_code=400,
            detail="OAuth 2.0 (3LO) is only supported for Jira boards",
        )

    try:
        authorize_url, state = build_authorize_url(
            organization_id=organization_id, board_id=board_id
        )
    except JiraOAuthError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return JiraOAuthAuthorizeResponse(authorize_url=authorize_url, state=state)


class JiraOAuthCallbackResponse(BaseModel):
    """Response model for the Jira OAuth callback endpoint."""

    board_id: str
    cloud_id: str
    site_url: str


@router.get(
    "/boards/oauth/jira/callback",
    response_model=JiraOAuthCallbackResponse,
)
async def jira_oauth_callback(
    code: str,
    state: str,
    session: Session = Depends(get_session),
):
    """
    Atlassian redirects here with `code` and `state` after the user
    consents. This route's full path (/api/v1/boards/oauth/jira/callback)
    is FIXED -- no organization_id/board_id path params -- because it must
    exactly match the single callback URL pre-registered in Atlassian's
    app console (BOARD_OAUTH_REDIRECT_URI_JIRA); Atlassian requires an
    exact string match with no wildcards or path templates, so a per-board
    URL can't be registered there.

    organization_id/board_id are instead recovered from the signed `state`
    param via parse_and_verify_state -- this doubles as both CSRF
    protection and the only source of those IDs, so state must be verified
    BEFORE any board lookup is attempted (there's no board_id to look up
    until state has been parsed).

    No X-User-ID header is required here -- this endpoint is hit directly
    by Atlassian's redirect (the browser), not by an authenticated API
    caller, so identity/membership is established by the signed `state`
    token, not by request headers.
    """
    parsed = parse_and_verify_state(state)
    if parsed is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OAuth state parameter — possible CSRF attempt.",
        )

    organization_id, board_id = parsed

    registration = session.exec(
        select(BoardRegistration).where(
            BoardRegistration.id == board_id,
            BoardRegistration.organization_id == organization_id,
        )
    ).first()

    if not registration:
        raise not_found("Board registration", board_id)

    try:
        token_response = await exchange_code_for_tokens(code)
        cloud_id, site_url = await resolve_cloud_id(
            access_token=token_response["access_token"],
            board_url=registration.board_url,
        )
    except JiraOAuthError as e:
        raise HTTPException(status_code=502, detail=str(e))

    expires_in = token_response.get("expires_in", 3600)
    try:
        expires_in = int(expires_in)
    except (TypeError, ValueError):
        expires_in = 3600
    expires_at = (
        datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    ).isoformat()

    payload = {
        "auth_type": "oauth2",
        "access_token": token_response["access_token"],
        "refresh_token": token_response["refresh_token"],
        "expires_at": expires_at,
        "cloud_id": cloud_id,
        "site_url": site_url,
    }

    set_board_credential(
        session, board_id, organization_id, registration.board_type, payload
    )

    logger.info(f"Jira OAuth credential stored for board {board_id}")
    return JiraOAuthCallbackResponse(
        board_id=board_id, cloud_id=cloud_id, site_url=site_url
    )


@router.delete("/organizations/{organization_id}/boards/{board_id}")
async def delete_board_registration(
    organization_id: str,
    board_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role(OrganizationRole.ADMIN)),
):
    """Delete a board registration"""
    registration = session.exec(
        select(BoardRegistration).where(
            BoardRegistration.id == board_id,
            BoardRegistration.organization_id == organization_id,
        )
    ).first()

    if not registration:
        raise not_found("Board registration", board_id)

    # Logical delete only -- keep the row (and its tickets) for audit; cascade
    # soft-delete the board's tickets. Never a hard delete.
    cleared = soft_delete_board(session, registration)

    logger.info(
        f"Board registration soft-deleted: {board_id} (cleared {cleared} tickets)"
    )
    return {
        "message": "Board registration deleted successfully",
        "cleared": cleared,
    }


@router.post("/organizations/{organization_id}/boards/{board_id}/clear")
async def clear_board(
    organization_id: str,
    board_id: str,
    dry_run: bool = False,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """Clear a board: logically delete all its tickets (set deleted_at). The
    board registration stays active. Reversible via re-sync -- tickets still
    present at source are revived on the next sync. `dry_run=true` returns the
    count without mutating.

    TODO: a `restore`/undo endpoint (undo is re-sync-only today).
    """

    registration = session.exec(
        select(BoardRegistration).where(
            BoardRegistration.id == board_id,
            BoardRegistration.organization_id == organization_id,
        )
    ).first()
    if not registration:
        raise not_found("Board registration", board_id)

    cleared = clear_board_tickets(session, board_id, dry_run=dry_run)
    if not dry_run:
        logger.info(f"Board cleared: {board_id} ({cleared} tickets)")
    return {"cleared": cleared}


# ============================================================================
# Board Probe Endpoint — lightweight connectivity check
# ============================================================================


@router.post("/organizations/{organization_id}/boards/{board_id}/probe")
async def probe_board(
    organization_id: str,
    board_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
) -> Dict[str, Any]:
    """
    Test board connectivity without running a full sync.

    Validates that the board registration exists and is active, then returns the
    top 5 tickets already in the database that are actively in progress
    (status not in: done, todo, backlog, draft). This gives a quick sanity check
    that the right board is connected and the org is set up correctly.

    Does NOT require X-Integration-Token — uses data already in the database.
    """

    board = session.exec(
        select(BoardRegistration).where(
            BoardRegistration.id == board_id,
            BoardRegistration.organization_id == organization_id,
        )
    ).first()

    if not board:
        raise not_found("Board registration", board_id)

    if not board.is_active:
        raise HTTPException(status_code=400, detail="Board registration is not active")

    # Fetch top 5 active tickets (in_progress or in_review) from the DB
    excluded = [
        TicketStatus.DONE,
        TicketStatus.TODO,
        TicketStatus.BACKLOG,
        TicketStatus.DRAFT,
    ]
    active_tickets = session.exec(
        select(Ticket)
        .where(
            Ticket.board_registration_id == board_id,
            ~Ticket.status.in_(excluded),
            Ticket.deleted_at.is_(None),
        )
        .order_by(Ticket.updated_at.desc())
        .limit(5)
    ).all()

    ticket_list = [
        {
            "id": str(t.id),
            "summary": t.summary,
            "status": t.status.value if hasattr(t.status, "value") else str(t.status),
            "assignee": t.assignee,
            "external_ticket_id": t.external_ticket_id,
            "url": t.url,
        }
        for t in active_tickets
    ]

    return {
        "credentials_valid": True,
        "board_id": board_id,
        "board_name": board.board_name,
        "board_type": (
            board.board_type.value
            if hasattr(board.board_type, "value")
            else str(board.board_type)
        ),
        "active_tickets": ticket_list,
        "message": (
            f"Board is registered and active. {len(ticket_list)} in-progress ticket(s) found."
            if ticket_list
            else "Board is registered and active. No in-progress tickets found yet — run a sync first."
        ),
    }


# ============================================================================
# Board Synchronization Endpoints
# ============================================================================


def resolve_board_sync_credential(
    session: Session,
    organization_id: str,
    board_id: str,
    token: Optional[str] = None,
) -> Tuple[BoardRegistration, str]:
    """Resolve the credential a sync should run with: the caller's if they
    supplied one, otherwise the board's own credential from Vault.

    Every endpoint that syncs against a board needs the same four steps --
    look the registration up *within the calling organization*, refuse an
    inactive board, fall back to Vault, and fail with a remedy if there is no
    credential anywhere. `sync_board` had them inline and the other two sync
    endpoints had none: they declared `X-Integration-Token` as
    `Header(...)` (required), so a caller with a perfectly good Vault
    credential got a 422 and the only way to satisfy them was to send a
    credential from somewhere off-platform. That is what pushed the CLI into
    reading `~/.innoday/config.json` and posting whatever it found (#609).

    The `is_active` check lives here rather than at the call sites because it
    is a precondition of *resolving a credential to sync with*, not of the
    individual endpoint -- an inactive board must not sync no matter which
    route asked. Both previous inline copies already did it, so this changes
    nothing for them; `generate_tickets_from_scope` gains the check, which its
    own docstring already promised ("Board must be registered and active").

    Returns the registration alongside the token because every caller needs
    both, and re-querying would be a second trip for a row already in hand.
    """
    registration = session.exec(
        select(BoardRegistration).where(
            BoardRegistration.id == board_id,
            BoardRegistration.organization_id == organization_id,
        )
    ).first()

    if not registration:
        raise not_found("Board registration", board_id)

    if not registration.is_active:
        raise HTTPException(status_code=400, detail="Board registration is not active")

    if token:
        return registration, token

    stored_payload = get_board_credential_payload(session, board_id)
    if not stored_payload:
        raise HTTPException(
            status_code=400,
            detail=(
                "No credentials found for this board — register it with a "
                "token, or supply X-Integration-Token."
            ),
        )

    return registration, payload_to_legacy_token(
        registration.board_type, stored_payload
    )


def _age_phrase(started_at: Optional[datetime]) -> str:
    """When a run started, and how long ago: `2026-08-13 23:24 UTC (17 min ago)`.

    The wall-clock time is what an operator matches against a deploy log; the
    age is what tells them at a glance whether this is a live sync or wreckage.
    `started_at` is a naive column, so `as_utc` before subtracting.
    """
    started = as_utc(started_at)
    if started is None:
        return "at an unrecorded time"
    minutes = max(0, int((datetime.now(timezone.utc) - started).total_seconds() // 60))
    return f"{started:%Y-%m-%d %H:%M UTC} ({minutes} min ago)"


@router.post(
    "/organizations/{organization_id}/boards/{board_id}/sync",
    response_model=SyncResponse,
)
async def sync_board(
    organization_id: str,
    board_id: str,
    sync_request: SyncRequest,
    background_tasks: BackgroundTasks,
    token: Optional[str] = Header(None, alias="X-Integration-Token"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """
    Trigger board synchronization.

    The integration token can be passed in the X-Integration-Token header
    (useful for testing/override); if omitted, falls back to the credential
    stored in Vault at registration time. This endpoint queues a background
    task to perform the actual synchronization.
    """
    registration, token = resolve_board_sync_credential(
        session, organization_id, board_id, token
    )

    # Check for recent sync if not forcing
    if not sync_request.force:
        recent_sync = session.exec(
            select(BoardSyncHistory).where(
                BoardSyncHistory.board_registration_id == board_id,
                BoardSyncHistory.sync_status.in_(
                    [SyncStatus.PENDING, SyncStatus.IN_PROGRESS]
                ),
                # A preview never wrote anything, so an abandoned one has nothing
                # to protect and must not stand in the way of real work.
                BoardSyncHistory.dry_run.is_(False),  # type: ignore[union-attr]
            )
        ).first()

        if recent_sync:
            # Name the row that is doing the blocking, and the way out. The
            # refusal used to describe neither, so an operator facing a row a
            # dead process left behind saw only "sync already in progress" and
            # had no reason to think anything was wrong (#613).
            raise HTTPException(
                status_code=429,
                detail=(
                    f"Sync already in progress for this board: run "
                    f"{recent_sync.id} started {_age_phrase(recent_sync.started_at)} "
                    f"and has not reported yet. If it is stuck, sync again with "
                    f'`innoday board sync --force` (API: "force": true).'
                ),
            )

    # Create sync history entry
    sync_history = BoardSyncHistory(
        id=str(uuid4()),
        board_registration_id=board_id,
        sync_status=SyncStatus.PENDING,
        dry_run=bool(sync_request.dry_run),
        tickets_found=0,
        tickets_created=0,
        tickets_updated=0,
        tickets_skipped=0,
        started_at=datetime.now(timezone.utc),
        synced_by=current_user.id,
    )

    session.add(sync_history)
    session.commit()
    session.refresh(sync_history)

    # Queue background sync task
    background_tasks.add_task(
        sync_board_tickets_task,
        registration_id=board_id,
        sync_history_id=sync_history.id,
        token=token,
        options=sync_request.model_dump(),
    )

    logger.info(f"Board sync queued: {sync_history.id} for registration {board_id}")

    return SyncResponse(
        sync_id=sync_history.id,
        status=sync_history.sync_status,
        message="Board sync queued successfully",
        tickets_found=0,
        tickets_created=0,
        tickets_updated=0,
        started_at=sync_history.started_at,
        estimated_completion=datetime.now(timezone.utc),
    )


@router.post(
    "/organizations/{organization_id}/boards/{board_id}/tickets/{external_key}/sync",
    response_model=TicketSyncResponse,
)
async def sync_single_ticket(
    organization_id: str,
    board_id: str,
    external_key: str,
    token: Optional[str] = Header(None, alias="X-Integration-Token"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """
    Fetch one ticket from the connected board immediately and upsert it,
    without waiting for the next scheduled sync cycle.

    The integration token can be passed in the X-Integration-Token header for
    a one-off override; if omitted, it resolves from the credential stored in
    Vault at registration time -- the same rule `sync_board` follows. It was
    a required header until #609, which meant a caller had to supply a board
    credential from outside the platform for a board whose credential was
    already stored.
    """
    _registration, token = resolve_board_sync_credential(
        session, organization_id, board_id, token
    )

    try:
        was_created, ticket = await board_sync_service.sync_single_ticket(
            registration_id=board_id,
            external_key=external_key,
            token=token,
            session=session,
        )
    except BoardAdapterError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return TicketSyncResponse(
        ticket=TicketFieldsResponse.model_validate(ticket),
        was_created=was_created,
    )


@router.get(
    "/organizations/{organization_id}/boards/{board_id}/sync-history",
    response_model=List[Dict],
)
async def get_sync_history(
    organization_id: str,
    board_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    limit: int = Query(
        default=10, ge=1, le=100, description="Number of sync records to return"
    ),
    _org: Organization = Depends(require_org_role()),
):
    """Get synchronization history for a board registration"""
    # Validate registration exists
    registration = session.exec(
        select(BoardRegistration).where(
            BoardRegistration.id == board_id,
            BoardRegistration.organization_id == organization_id,
        )
    ).first()

    if not registration:
        raise not_found("Board registration", board_id)

    # Get sync history
    sync_history = session.exec(
        select(BoardSyncHistory)
        .where(BoardSyncHistory.board_registration_id == board_id)
        .order_by(BoardSyncHistory.started_at.desc())
        .limit(limit)
    ).all()

    return [
        {
            "id": sync.id,
            "sync_status": sync.sync_status,
            "tickets_found": sync.tickets_found,
            "tickets_created": sync.tickets_created,
            "tickets_updated": sync.tickets_updated,
            "tickets_skipped": sync.tickets_skipped,
            "error_message": sync.error_message,
            "started_at": sync.started_at,
            "completed_at": sync.completed_at,
            "duration_seconds": sync.duration_seconds,
            "synced_by": sync.synced_by,
        }
        for sync in sync_history
    ]


# ============================================================================
# Ticket Creation Endpoints
# ============================================================================


@router.post(
    "/organizations/{organization_id}/tickets/parse",
    response_model=TicketParseResponse,
)
async def parse_text_to_tickets(
    organization_id: str,
    request: TicketParseRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """
    Parse unstructured text into structured tickets using Claude AI.

    This endpoint uses Claude to intelligently parse meeting notes, requirements,
    or any text into well-structured tickets with titles, descriptions, and metadata.
    """
    # Verify organization exists and user is member
    org = resolve_organization(organization_id, session)

    # Parse text using Claude
    parser = ClaudeTicketParser(organization_alias=org.alias)

    try:
        response = await parser.parse_text_to_tickets(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse text: {str(e)}")


@router.post(
    "/organizations/{organization_id}/boards/{board_id}/tickets",
    response_model=TicketCreateResponse,
)
async def create_board_ticket(
    organization_id: str,
    board_id: str,
    ticket_data: TicketCreateRequest,
    background_tasks: BackgroundTasks,
    token: Optional[str] = Header(None, alias="X-Integration-Token"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """
    Create a ticket on a registered board.

    This endpoint:
    1. Creates the ticket on the external board (Trello/Jira/Linear)
    2. Stores it in InnoDay database
    3. Returns the created ticket with external metadata

    The integration token can be passed in the X-Integration-Token header
    (useful for testing/override); if omitted, BoardTicketCreationService
    resolves it from the Vault-stored credential set at registration time.
    """
    # Verify organization and membership
    resolve_organization(organization_id, session)

    # Verify board belongs to organization
    board = session.get(BoardRegistration, board_id)
    if not board or board.organization_id != organization_id:
        raise HTTPException(
            status_code=404, detail="Board not found in this organization"
        )

    # Create ticket
    service = BoardTicketCreationService(session)

    try:
        response = await service.create_ticket_on_board(
            board_registration_id=board_id,
            ticket_data=ticket_data,
            user_id=current_user.id,
            token=token,
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create ticket: {str(e)}"
        )


@router.post(
    "/organizations/{organization_id}/boards/{board_id}/tickets/bulk",
    response_model=BulkTicketCreateResponse,
)
async def create_board_tickets_bulk(
    organization_id: str,
    board_id: str,
    bulk_request: BulkTicketCreateRequest,
    background_tasks: BackgroundTasks,
    token: Optional[str] = Header(None, alias="X-Integration-Token"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """
    Create multiple tickets on a registered board.

    Useful for creating tickets from parsed text or bulk imports. The
    integration token can be passed in the X-Integration-Token header; if
    omitted, resolved from the Vault-stored credential.
    """
    # Verify organization and membership
    resolve_organization(organization_id, session)

    # Verify board belongs to organization
    board = session.get(BoardRegistration, board_id)
    if not board or board.organization_id != organization_id:
        raise HTTPException(
            status_code=404, detail="Board not found in this organization"
        )

    # Create tickets
    service = BoardTicketCreationService(session)

    try:
        response = await service.create_tickets_bulk(
            board_registration_id=board_id,
            bulk_request=bulk_request,
            user_id=current_user.id,
            token=token,
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create tickets: {str(e)}"
        )


@router.post(
    "/organizations/{organization_id}/boards/{board_id}/tickets/parse-and-create",
    response_model=ParseAndCreateResponse,
)
async def parse_and_create_tickets(
    organization_id: str,
    board_id: str,
    request: ParseAndCreateRequest,
    background_tasks: BackgroundTasks,
    token: Optional[str] = Header(None, alias="X-Integration-Token"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role(OrganizationRole.DEVELOPER)),
):
    """
    Parse text into tickets using Claude AI and optionally create them on the board.

    This is the main endpoint that combines Claude's parsing with ticket creation.
    It can:
    1. Parse unstructured text into structured tickets
    2. Show the parsed tickets for review
    3. Optionally auto-create them on the external board

    The integration token can be passed in the X-Integration-Token header
    (only needed if auto_create is set); if omitted, resolved from the
    Vault-stored credential.
    """
    # Verify organization and membership
    org = resolve_organization(organization_id, session)

    # Verify board belongs to organization
    board = session.get(BoardRegistration, board_id)
    if not board or board.organization_id != organization_id:
        raise HTTPException(
            status_code=404, detail="Board not found in this organization"
        )

    # Parse text using Claude
    parser = ClaudeTicketParser(organization_alias=org.alias)

    parse_request = TicketParseRequest(
        text=request.text,
        context=request.context,
        board_type=board.board_type.value,
        default_assignee=request.default_assignee,
        max_tickets=request.max_tickets,
    )

    try:
        parse_response = await parser.parse_text_to_tickets(parse_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse text: {str(e)}")

    # Prepare response
    response = ParseAndCreateResponse(
        parsed_tickets=parse_response.tickets,
        parse_summary=parse_response.summary,
        parse_confidence=parse_response.confidence,
        parse_notes=parse_response.notes,
    )

    # If auto_create is enabled, create the tickets
    if request.auto_create and parse_response.tickets:
        service = BoardTicketCreationService(session)

        for parsed_ticket in parse_response.tickets:
            try:
                # Convert parsed ticket to create request
                create_request = TicketCreateRequest(
                    summary=parsed_ticket.summary,
                    description=parsed_ticket.description,
                    assignee=parsed_ticket.assignee,
                    labels=parsed_ticket.labels,
                    priority=parsed_ticket.priority,
                    list_id=request.default_list_id,
                    epic_link=parsed_ticket.epic,
                    story_points=(
                        int(parsed_ticket.estimated_hours)
                        if parsed_ticket.estimated_hours
                        else None
                    ),
                )

                # Create the ticket
                created = await service.create_ticket_on_board(
                    board_registration_id=board_id,
                    ticket_data=create_request,
                    user_id=current_user.id,
                    token=token,
                )
                response.created_tickets.append(created)

            except Exception as e:
                response.failed_tickets.append(
                    {"ticket": parsed_ticket.model_dump(), "error": str(e)}
                )

    return response


@router.get("/organizations/{organization_id}/boards/{board_id}/lists")
async def get_board_lists(
    organization_id: str,
    board_id: str,
    token: Optional[str] = Header(None, alias="X-Integration-Token"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """
    Get available lists/columns for a board.

    For Trello, returns the lists. For Jira, returns issue types. The
    integration token can be passed in the X-Integration-Token header; if
    omitted, resolved from the Vault-stored credential.
    """
    # Verify organization and membership
    resolve_organization(organization_id, session)

    # Verify board belongs to organization
    board = session.get(BoardRegistration, board_id)
    if not board or board.organization_id != organization_id:
        raise HTTPException(
            status_code=404, detail="Board not found in this organization"
        )

    # Get lists from the service
    service = BoardTicketCreationService(session)

    try:
        lists = await service.get_available_lists(board_id, token)
        return lists
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get lists: {str(e)}")


# ============================================================================
async def _fetch_commits_since_tag(
    github_org: str,
    since_tag: str,
    token: Optional[str],
    max_per_repo: int = 50,
) -> Dict[str, List[Dict[str, str]]]:
    """
    Fetch commits across all non-archived repos in a GitHub org since a given tag.

    Returns a dict keyed by repo name with lists of commit dicts:
      {"sha": "abc1234", "message": "...", "author": "...", "date": "..."}

    Skips repos that don't have the tag or whose API call fails.
    """
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    results: Dict[str, List[Dict[str, str]]] = {}

    async with httpx.AsyncClient(timeout=20.0) as client:
        # List repos
        resp = await client.get(
            f"https://api.github.com/orgs/{github_org}/repos",
            headers=headers,
            params={"per_page": 100, "sort": "pushed"},
        )
        if resp.status_code != 200:
            logger.warning(
                f"GitHub repos list failed: {resp.status_code} {resp.text[:200]}"
            )
            return results

        repos = [r for r in resp.json() if not r.get("archived")]

        for repo in repos:
            repo_name = repo["name"]
            try:
                commits_resp = await client.get(
                    f"https://api.github.com/repos/{github_org}/{repo_name}/commits",
                    headers=headers,
                    params={
                        "sha": repo.get("default_branch", "main"),
                        "per_page": max_per_repo,
                    },
                )
                if commits_resp.status_code != 200:
                    continue

                tag_sha: Optional[str] = None
                tag_resp = await client.get(
                    f"https://api.github.com/repos/{github_org}/{repo_name}/git/ref/tags/{since_tag}",
                    headers=headers,
                )
                if tag_resp.status_code == 200:
                    tag_data = tag_resp.json()
                    tag_sha = tag_data.get("object", {}).get("sha")
                    # Peeled tags point to a tag object — resolve to commit SHA
                    if tag_data.get("object", {}).get("type") == "tag":
                        tag_obj_resp = await client.get(
                            f"https://api.github.com/repos/{github_org}/{repo_name}/git/tags/{tag_sha}",
                            headers=headers,
                        )
                        if tag_obj_resp.status_code == 200:
                            tag_sha = tag_obj_resp.json().get("object", {}).get("sha")

                commits: List[Dict[str, str]] = []
                for c in commits_resp.json():
                    if tag_sha and c["sha"] == tag_sha:
                        break
                    msg = c.get("commit", {}).get("message", "").splitlines()[0]
                    author = c.get("commit", {}).get("author", {}).get("name") or c.get(
                        "author", {}
                    ).get("login", "unknown")
                    date = c.get("commit", {}).get("author", {}).get("date", "")[:10]
                    commits.append(
                        {
                            "sha": c["sha"][:7],
                            "message": msg,
                            "author": author,
                            "date": date,
                        }
                    )

                if commits:
                    results[repo_name] = commits

            except Exception as exc:
                logger.debug(f"Skipping {repo_name} commit fetch: {exc}")
                continue

    return results


# Board Summary Endpoints
# ============================================================================


async def _assemble_board_summary_data(
    organization_id: str,
    board_id: str,
    summary_type: SummaryType,
    since_version: Optional[str],
    github_org: Optional[str],
    session: Session,
) -> Dict[str, Any]:
    """
    Assemble the structured ticket/stats data used to write a board summary.

    This is pure data assembly -- it never calls Claude/Anthropic. It is
    shared by the `summary-data` endpoint (HS-297): the caller (a Claude
    Code session, via the MCP `get_board_summary_data` tool, or the CLI)
    is responsible for turning this data into prose.

    Raises HTTPException(404) if the board or its tickets can't be found.
    """
    # Verify board exists and belongs to organization
    board_reg = session.exec(
        select(BoardRegistration)
        .where(BoardRegistration.id == board_id)
        .where(BoardRegistration.organization_id == organization_id)
    ).first()

    if not board_reg:
        raise not_found("Board", board_id)

    # Get tickets for the board (exclude soft-deleted -- they must not surface
    # in board summaries / the get_board_summary_data MCP tool / CLI summary).
    tickets = session.exec(
        select(Ticket)
        .where(Ticket.board_registration_id == board_id)
        .where(Ticket.organization_id == organization_id)
        .where(Ticket.deleted_at.is_(None))
    ).all()

    if not tickets:
        raise HTTPException(404, "No tickets found for this board")

    # Group tickets by status and time windows
    now = datetime.now(timezone.utc)
    last_7_days = now - timedelta(days=7)
    last_48_hours = now - timedelta(hours=48)
    last_24_hours = now - timedelta(hours=24)

    # Categorize tickets
    active_tickets = {
        "in_progress": [],
        "in_review": [],
        "todo_assigned": [],
        "blocked": [],
    }
    recent_completions = {"last_48_hours": [], "last_7_days": [], "last_24_hours": []}
    backlog_tickets = []

    for ticket in tickets:
        # Active work
        if ticket.status == TicketStatus.IN_PROGRESS:
            active_tickets["in_progress"].append(ticket)
        elif ticket.status == TicketStatus.IN_REVIEW:
            active_tickets["in_review"].append(ticket)
        elif ticket.status == TicketStatus.TODO:
            if ticket.assignee:
                active_tickets["todo_assigned"].append(ticket)
            else:
                backlog_tickets.append(ticket)
        elif ticket.status == TicketStatus.BACKLOG:
            backlog_tickets.append(ticket)

        # Recent completions
        elif ticket.status == TicketStatus.DONE:
            completed_at = as_utc(ticket.completed_at)
            if completed_at:
                if completed_at > last_24_hours:
                    recent_completions["last_24_hours"].append(ticket)
                if completed_at > last_48_hours:
                    recent_completions["last_48_hours"].append(ticket)
                if completed_at > last_7_days:
                    recent_completions["last_7_days"].append(ticket)

    # Calculate statistics
    total_active = sum(len(tickets) for tickets in active_tickets.values())

    stats = {
        "total_tickets": len(tickets),
        "active_tickets": total_active,
        "in_progress": len(active_tickets["in_progress"]),
        "in_review": len(active_tickets["in_review"]),
        "todo_assigned": len(active_tickets["todo_assigned"]),
        "blocked": len(active_tickets["blocked"]),
        "completed_24h": len(recent_completions["last_24_hours"]),
        "completed_48h": len(recent_completions["last_48_hours"]),
        "completed_7d": len(recent_completions["last_7_days"]),
        "backlog": len(backlog_tickets),
    }

    # Get organization to get the slug (used for GitHub commit lookups)
    org = session.exec(
        select(Organization).where(Organization.id == organization_id)
    ).first()

    if not org:
        raise not_found("Organization", organization_id)

    prompt = _get_summary_prompt(summary_type)

    # Build detailed context messages -- the same structured context that
    # used to be sent to Anthropic. Now returned to the caller (a Claude
    # Code session) so IT can write the summary text from this data.
    messages = [
        f"Board: {board_reg.board_name}",
        f"Generated: {now.strftime('%Y-%m-%d %H:%M UTC')}",
    ]

    # Add currently active tickets
    messages.append("\n=== CURRENTLY ACTIVE TICKETS ===")
    if total_active > 0:
        for status, tickets_list in active_tickets.items():
            if tickets_list:
                messages.append(
                    f"\n{status.upper().replace('_', ' ')} ({len(tickets_list)} tickets):"
                )
                for t in tickets_list[:10]:
                    updated_at = as_utc(t.updated_at)
                    days_in_status = (now - updated_at).days if updated_at else 0
                    messages.append(f"- {t.summary}")
                    messages.append(
                        f"  Assignee: {t.assignee or 'Unassigned'} | Days in status: {days_in_status}"
                    )
    else:
        messages.append("No currently active tickets.")

    if summary_type == SummaryType.RELEASE:
        # For release summaries, include ALL done tickets (not just last 7 days)
        all_done = session.exec(
            select(Ticket)
            .where(Ticket.board_registration_id == board_id)
            .where(Ticket.organization_id == organization_id)
            .where(Ticket.status == TicketStatus.DONE)
            .where(Ticket.deleted_at.is_(None))
        ).all()

        since_tag_label = since_version or "last release"
        messages.append(f"\n=== TICKETS COMPLETED SINCE {since_tag_label.upper()} ===")
        if all_done:
            for t in all_done[:50]:
                key = t.external_ticket_id or str(t.id)[:8]
                done_date = (
                    t.completed_at.strftime("%Y-%m-%d") if t.completed_at else "unknown"
                )
                messages.append(
                    f"- [{key}] {t.summary} (done: {done_date}, by: {t.assignee or 'unknown'})"
                )
        else:
            messages.append("No completed tickets found.")

        messages.append("\n=== IN PROGRESS (not yet in release) ===")
        for t in active_tickets.get("in_progress", []) + active_tickets.get(
            "in_review", []
        ):
            messages.append(f"- {t.summary} (assignee: {t.assignee or 'unassigned'})")

        # Fetch GitHub commits if since_version is provided
        if since_version:
            # This org's Vault credential, never the process-wide GITHUB_TOKEN --
            # that is the operator's, shared by every tenant. And it cannot just
            # be left unset: `_fetch_commits_since_tag` treats a falsy token as
            # *anonymous*, so an unconfigured tenant would get a silent partial
            # summary (private repos missing) that reads exactly like a correct
            # one. Say so in `messages` instead.
            creds = get_github_credentials(session, organization_id)
            github_token = (creds or {}).get("token")
            if not github_token:
                messages.append(
                    f"\n=== GITHUB COMMITS ===\nGitHub is not connected for "
                    f"organization '{org.alias or organization_id}', so no commits "
                    f"could be read. Connect GitHub for this organization to "
                    f"include commit history in a release summary."
                )
            else:
                # #550's project-aware resolution: which InnoDay org owns a
                # project and which GitHub org hosts its repos are independent, so
                # `org.alias` was only ever right by coincidence.
                # `board_reg.project_id` is NOT NULL, so the project is available.
                board_project = session.get(Project, board_reg.project_id)
                gh_org = github_org or WorkspaceOnboardService(session).github_org(
                    org, board_project
                )
                try:
                    commit_data = await _fetch_commits_since_tag(
                        github_org=gh_org,
                        since_tag=since_version,
                        token=github_token,
                    )
                    if commit_data:
                        messages.append(
                            f"\n=== GITHUB COMMITS SINCE {since_version} ==="
                        )
                        for repo_name, commits in commit_data.items():
                            messages.append(
                                f"\nRepository: {repo_name} ({len(commits)} commits)"
                            )
                            for c in commits[:20]:
                                messages.append(
                                    f"  [{c['sha']}] {c['message']} — {c['author']} ({c['date']})"
                                )
                    else:
                        messages.append(
                            f"\n=== GITHUB COMMITS ===\nNo commits found since "
                            f"{since_version} in GitHub org '{gh_org}' (check the "
                            f"org name and the stored credential's scope)."
                        )
                except Exception as exc:
                    logger.warning(f"GitHub commit fetch failed: {exc}")
                    messages.append(
                        f"\n=== GITHUB COMMITS ===\nFailed to fetch commits: {exc}"
                    )

    else:
        # Add recent completions
        messages.append("\n=== RECENTLY COMPLETED (Last 7 Days) ===")
        if recent_completions["last_7_days"]:
            messages.append(
                f"Total completed in last 7 days: {len(recent_completions['last_7_days'])}"
            )
            for t in recent_completions["last_7_days"][:10]:
                completion_date_str = (
                    t.completed_at.strftime("%Y-%m-%d") if t.completed_at else "Unknown"
                )
                messages.append(f"- {t.summary}")
                messages.append(
                    f"  Completed: {completion_date_str} | By: {t.assignee or 'Unknown'}"
                )
        else:
            messages.append("No tickets completed in the last 7 days.")

    # Prepare active tickets list for response
    active_tickets_list = []
    for status, tickets_list in active_tickets.items():
        for t in tickets_list[:20]:
            active_tickets_list.append(
                {
                    "id": t.id,
                    "key": t.external_ticket_id or str(t.id)[:8],
                    "summary": t.summary,
                    "status": status,
                    "assignee": t.assignee or "Unassigned",
                    "days_in_status": (
                        (now - as_utc(t.updated_at)).days if t.updated_at else 0
                    ),
                }
            )

    # Prepare recent completions list for response
    recent_completions_list = []
    sorted_completions = sorted(
        recent_completions["last_7_days"],
        key=lambda t: (
            as_utc(t.completed_at) or datetime.min.replace(tzinfo=timezone.utc)
        ),
        reverse=True,
    )

    for t in sorted_completions[:20]:
        completed_at = as_utc(t.completed_at)
        days_ago = (now - completed_at).days if completed_at else None
        recent_completions_list.append(
            {
                "id": t.id,
                "key": t.external_ticket_id or str(t.id)[:8],
                "summary": t.summary,
                "completed_date": (
                    t.completed_at.strftime("%Y-%m-%d") if t.completed_at else "Unknown"
                ),
                "days_ago": days_ago,
                "release": t.release or None,
                "completed_by": t.assignee or "Unknown",
                "in_last_48h": t in recent_completions["last_48_hours"],
                "in_last_24h": t in recent_completions["last_24_hours"],
            }
        )

    return {
        "board_id": board_id,
        "board_name": board_reg.board_name,
        "summary_type": summary_type,
        "generated_at": now.isoformat(),
        "stats": stats,
        "active_tickets": active_tickets_list,
        "recent_completions": recent_completions_list,
        "messages": messages,
        "prompt": prompt,
        "ticket_count": len(tickets),
    }


@router.get(
    "/organizations/{organization_id}/boards/{board_id}/summary-data",
    summary="Fetch structured board data for writing a summary",
)
async def get_board_summary_data(
    organization_id: str,
    board_id: str,
    summary_type: SummaryType = Query(
        default=SummaryType.STATUS, description="Type of summary to prepare data for"
    ),
    since_version: Optional[str] = Query(
        default=None,
        description="Git tag or version string baseline for release summaries (e.g. 'v1.4.0').",
    ),
    github_org: Optional[str] = Query(
        default=None,
        description="GitHub org to fetch commits from for release summaries. Defaults to org slug.",
    ),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """
    Assemble and return the raw structured data needed to write a board summary.

    This endpoint never calls Claude/Anthropic -- it only fetches tickets,
    groups them by status and time window, computes stats, and returns a
    `messages`/`prompt` context bundle equivalent to what used to be sent
    to Anthropic server-side.

    Callers (e.g. the MCP `get_board_summary_data` tool, invoked from a
    Claude Code session) are expected to write the actual summary prose
    from this data themselves, then persist it via
    `POST .../boards/{board_id}/summaries`.
    """

    return await _assemble_board_summary_data(
        organization_id=organization_id,
        board_id=board_id,
        summary_type=summary_type,
        since_version=since_version,
        github_org=github_org,
        session=session,
    )


class SaveSummaryRequest(BaseModel):
    """Request body for persisting an externally-written board summary."""

    summary_type: SummaryType = Field(
        default=SummaryType.STATUS, description="Type of summary being saved"
    )
    summary: str = Field(..., description="The summary text, already written")
    stats: Dict[str, Any] = Field(
        default_factory=dict, description="Stats payload used to write the summary"
    )
    highlights: List[str] = Field(
        default_factory=list, description="Key positive points"
    )
    concerns: List[str] = Field(
        default_factory=list, description="Issues requiring attention"
    )
    motivational_message: Optional[str] = Field(
        default=None,
        description="Optional motivational message; a random one is chosen if omitted",
    )


@router.post(
    "/organizations/{organization_id}/boards/{board_id}/summaries",
    response_model=SummaryResponse,
    summary="Persist a board summary written externally (e.g. by Claude Code)",
)
async def save_board_summary(
    organization_id: str,
    board_id: str,
    request: SaveSummaryRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """
    Persist a summary that was written externally -- e.g. by the calling
    Claude Code session, after fetching data from `get_board_summary_data`
    -- to the same `summaries` table/shape the old Anthropic-backed
    endpoint wrote to. `list_board_summaries`/`summary-latest` continue to
    work transparently on summaries saved this way.

    No Anthropic/Claude API call happens here.
    """
    # Verify board exists and belongs to organization
    board_reg = session.exec(
        select(BoardRegistration)
        .where(BoardRegistration.id == board_id)
        .where(BoardRegistration.organization_id == organization_id)
    ).first()

    if not board_reg:
        raise not_found("Board", board_id)

    motivational_quote = request.motivational_message or random.choice(
        MOTIVATIONAL_QUOTES
    )

    board_summary = Summary(
        board_registration_id=board_id,
        organization_id=organization_id,
        project_id=board_reg.project_id,
        # The sentinel, stated explicitly: this path appends a history log to a
        # board and has no window to key uniqueness on. See src/domain/summary.py.
        window_spec="",
        summary_type=request.summary_type,
        body_markdown=request.summary,
        summary_data={"saved_externally": True},
        ticket_stats=request.stats,
        highlights=request.highlights,
        concerns=request.concerns,
        motivational_quote=motivational_quote,
        token_usage=0,
        generation_time_ms=0,
        created_by=current_user.id,
    )

    session.add(board_summary)
    session.commit()
    session.refresh(board_summary)

    return SummaryResponse(
        id=board_summary.id,
        summary=request.summary,
        summary_type=request.summary_type,
        stats=request.stats,
        active_tickets=[],
        recent_completions=[],
        highlights=request.highlights,
        concerns=request.concerns,
        motivational_message=motivational_quote,
        generated_at=board_summary.created_at,
        generation_time_ms=0,
        message=f"Summary saved successfully! {motivational_quote}",
    )


@router.get(
    "/organizations/{organization_id}/boards/{board_id}/summaries",
    summary="Get historical summaries for a board",
)
async def get_board_summaries(
    organization_id: str,
    board_id: str,
    summary_type: Optional[SummaryType] = Query(
        None, description="Filter by summary type"
    ),
    limit: int = Query(
        default=10, ge=1, le=50, description="Maximum summaries to return"
    ),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """
    Retrieve historical summaries for a board.

    Returns persisted summaries ordered by creation date (newest first).
    """
    # Verify board exists and belongs to organization
    board_reg = session.exec(
        select(BoardRegistration)
        .where(BoardRegistration.id == board_id)
        .where(BoardRegistration.organization_id == organization_id)
    ).first()

    if not board_reg:
        raise not_found("Board", board_id)

    query = select(Summary).where(
        Summary.board_registration_id == board_id,
        Summary.organization_id == organization_id,
    )

    if summary_type:
        query = query.where(Summary.summary_type == summary_type)

    summaries = session.exec(
        query.order_by(Summary.created_at.desc()).limit(limit)
    ).all()

    return {
        "summaries": [s.to_dict() for s in summaries],
        "count": len(summaries),
        "message": random.choice(
            [
                "📚 History loaded! Time travel to past summaries complete!",
                "🔮 Crystal ball activated! Here are your historical insights!",
                "📜 Ancient scrolls retrieved! (Well, as ancient as your data goes)",
            ]
        ),
    }


@router.get(
    "/organizations/{organization_id}/boards/{board_id}/summaries/latest",
    summary="Get the most recent summary for a board",
)
async def get_latest_summary(
    organization_id: str,
    board_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _org: Organization = Depends(require_org_role()),
):
    """Get the most recent summary for a board."""
    # Verify board exists and belongs to organization
    board_reg = session.exec(
        select(BoardRegistration)
        .where(BoardRegistration.id == board_id)
        .where(BoardRegistration.organization_id == organization_id)
    ).first()

    if not board_reg:
        raise not_found("Board", board_id)

    summary = session.exec(
        select(Summary)
        .where(
            Summary.board_registration_id == board_id,
            Summary.organization_id == organization_id,
        )
        .order_by(Summary.created_at.desc())
    ).first()

    if not summary:
        raise HTTPException(404, "No summaries found for this board")

    response = summary.to_dict()
    response["message"] = f"Latest summary retrieved! {summary.motivational_quote}"
    return response
