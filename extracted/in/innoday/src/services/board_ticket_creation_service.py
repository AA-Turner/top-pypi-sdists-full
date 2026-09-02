"""
Board Ticket Creation Service

This service handles creating tickets on external boards (Trello/Jira)
and syncing them back to InnoDay's database.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field
from sqlmodel import Session

from src.adapters import (
    BaseBoardAdapter,
)
from src.domain.board import BoardRegistration, BoardType
from src.domain.organization import Organization
from src.domain.ticket import TicketStatus
from src.services.board_adapter_factory import (
    build_board_adapter,
    is_oauth_jira,
    resolve_board_token,
)

logger = logging.getLogger(__name__)


class TicketCreateRequest(BaseModel):
    """Request model for creating a ticket"""

    summary: str = Field(..., max_length=500, description="Ticket title/summary")
    description: Optional[str] = Field(
        None, max_length=5000, description="Detailed description"
    )
    assignee: Optional[str] = Field(None, description="Assignee email or username")
    labels: List[str] = Field(default_factory=list, description="Labels/tags")
    priority: Optional[str] = Field(None, description="Priority level")
    due_date: Optional[datetime] = Field(None, description="Due date")
    status: Optional[str] = Field(
        None,
        description=(
            "Initial status/workflow-state for the ticket (e.g. 'Todo', "
            "'In Progress', 'Done'). Falls back to 'TODO' when omitted. For "
            "external boards, the value is matched (case-insensitively) "
            "against the board's own workflow-state names."
        ),
    )

    # Board-specific fields
    list_id: Optional[str] = Field(None, description="Trello list ID")
    list_name: Optional[str] = Field(
        None, description="Trello list name (alternative to ID)"
    )
    project_key: Optional[str] = Field(None, description="Jira project key")
    issue_type: Optional[str] = Field(default="Task", description="Jira issue type")
    epic_link: Optional[str] = Field(None, description="Epic to link to")
    story_points: Optional[int] = Field(None, description="Story points estimate")


class BulkTicketCreateRequest(BaseModel):
    """Request model for creating multiple tickets"""

    tickets: List[TicketCreateRequest] = Field(
        ..., description="List of tickets to create"
    )
    default_list_id: Optional[str] = Field(
        None, description="Default Trello list if not specified per ticket"
    )
    default_assignee: Optional[str] = Field(
        None, description="Default assignee if not specified per ticket"
    )
    default_labels: List[str] = Field(
        default_factory=list, description="Labels to add to all tickets"
    )


class TicketCreateResponse(BaseModel):
    """Response model for created ticket"""

    id: int = Field(..., description="InnoDay ticket ID")
    external_id: str = Field(..., description="External board ticket ID")
    external_url: str = Field(..., description="URL to ticket on external board")
    summary: str
    description: Optional[str]
    status: TicketStatus
    board_id: str
    board_name: str
    created_at: datetime
    created_by: str


class BulkTicketCreateResponse(BaseModel):
    """Response for bulk ticket creation"""

    created: List[TicketCreateResponse] = Field(
        ..., description="Successfully created tickets"
    )
    failed: List[Dict[str, Any]] = Field(
        default_factory=list, description="Failed tickets with errors"
    )
    summary: str = Field(..., description="Summary of the operation")


class BoardTicketCreationService:
    """
    Service for creating tickets on external boards

    Now uses adapter pattern internally to abstract platform differences.
    """

    def __init__(self, session: Session):
        """
        Initialize the service

        Args:
            session: Database session
        """
        self.session = session
        # Cache adapters by (board_id, token) -- see _get_adapter
        self.adapters: Dict[Tuple[str, str], BaseBoardAdapter] = {}

    def _resolve_token(
        self,
        board_reg: BoardRegistration,
        org: Optional[Organization],
        token: Optional[str] = None,
    ) -> str:
        """Resolve this board's credential.

        **A delegate, not a chain.** The chain itself -- caller-supplied token,
        then Vault, then a refusal that names the store to fix it in -- moved to
        `board_adapter_factory.resolve_board_token` when a second caller
        (`ticket_status_service`) needed it. It is one function because two
        copies of it had already drifted once: `get_available_lists`
        dereferenced ``org.alias`` without checking ``org`` for None, so an
        orphaned board raised ``AttributeError`` → 500 rather than a clear error.

        The method stays so this service's callers, and the tests that describe
        its behaviour, keep addressing the thing they are about.
        """
        return resolve_board_token(self.session, board_reg, org, token)

    async def _get_adapter(
        self, board_reg: BoardRegistration, token: str
    ) -> BaseBoardAdapter:
        """Get or create the adapter for this board.

        Delegates construction to the shared factory, so this path supports
        exactly what board sync supports -- including OAuth Jira and Notion,
        both of which this service's own copy of the switch used to reject.
        """
        # Cache key includes the token, not just the board id. Keyed on the id
        # alone, the first adapter ever built for a board keeps being reused with
        # its original token baked in, so a rotated credential (or a one-off
        # X-Integration-Token) silently applies to later operations on this
        # instance. Instances are per-request, so this was never a cross-user
        # leak -- but ticket_generation_service holds one across many creates,
        # and a rotated credential was ignored regardless.
        #
        # OAuth-mode Jira is never cached: see is_oauth_jira in the factory.
        oauth_jira = is_oauth_jira(board_reg, token)
        cache_key = (board_reg.id, token)
        if not oauth_jira and cache_key in self.adapters:
            return self.adapters[cache_key]

        # No legacy_credentials argument: this is now the same call BoardSyncService
        # makes, which is the point of #525 phase 3.
        adapter = await build_board_adapter(board_reg, token, self.session)

        if not oauth_jira:
            self.adapters[cache_key] = adapter
        return adapter

    async def create_ticket_on_board(
        self,
        board_registration_id: str,
        ticket_data: TicketCreateRequest,
        user_id: str,
        token: Optional[str] = None,
    ) -> TicketCreateResponse:
        """
        Create a single ticket on an external board

        Args:
            board_registration_id: ID of the board registration
            ticket_data: Ticket data to create
            user_id: ID of the user creating the ticket
            token: Optional API token (if not provided, will try to get from credentials)

        Returns:
            Created ticket response

        Raises:
            ValueError: If board registration not found or inactive
            Exception: If ticket creation fails
        """
        # Get board registration
        board_reg = self.session.get(BoardRegistration, board_registration_id)
        if not board_reg:
            raise ValueError(f"Board registration {board_registration_id} not found")

        if not board_reg.is_active:
            raise ValueError(
                f"Board registration {board_registration_id} is not active"
            )

        # Get organization
        org = self.session.get(Organization, board_reg.organization_id)
        if not org:
            raise ValueError(f"Organization {board_reg.organization_id} not found")

        token = self._resolve_token(board_reg, org, token)

        # Get adapter and create ticket
        adapter = await self._get_adapter(board_reg, token)
        await adapter.initialize(token)

        # Prepare ticket data for adapter
        adapter_ticket_data = {
            "summary": ticket_data.summary,
            "description": ticket_data.description,
            "assignee": ticket_data.assignee,
            "labels": ticket_data.labels,
            "priority": ticket_data.priority,
            "due_date": ticket_data.due_date,
            # Caller may override; default remains "TODO" when unspecified.
            "status": ticket_data.status or "TODO",
        }

        # Add platform-specific fields
        if board_reg.board_type == BoardType.TRELLO:
            adapter_ticket_data["list_id"] = ticket_data.list_id
            adapter_ticket_data["list_name"] = ticket_data.list_name
        elif board_reg.board_type == BoardType.JIRA:
            # NOTE: previously fell back to board_reg.board_external_id when
            # no explicit project_key was given -- but for Jira,
            # board_external_id is the numeric BOARD id (e.g. "80"), not a
            # project KEY (e.g. "ITPT"). Confirmed live: this made every
            # ticket-creation call with no explicit project_key send
            # project_key="80" to Jira's API, which then rejected it with
            # "The target project doesn't exist or you don't have permission
            # to create issues in it." -- silently shadowing the adapter's
            # own correctly-resolved self.project_key (from
            # _init_project_config's board-configuration lookup). Only set
            # this key when the caller explicitly provided one; let the
            # adapter fall back to its own resolved project key otherwise.
            if ticket_data.project_key:
                adapter_ticket_data["project_key"] = ticket_data.project_key
            adapter_ticket_data["issue_type"] = ticket_data.issue_type or "Task"
            adapter_ticket_data["epic_link"] = ticket_data.epic_link
            adapter_ticket_data["story_points"] = ticket_data.story_points

        # Create ticket using adapter
        created_ticket = await adapter.create_ticket(
            board_reg.board_external_id, adapter_ticket_data
        )

        # Apply an explicitly-requested status to the external board. Board
        # adapters (e.g. Linear) create the ticket in the board's own default
        # workflow state and do NOT honour a status on create -- setting it is
        # a separate transition. So when the caller asked for a specific
        # status, do that transition now. Best-effort: if the board rejects
        # the state name we surface it but keep the successfully-created
        # ticket rather than failing the whole create.
        if ticket_data.status:
            try:
                created_ticket = await adapter.update_ticket_status(
                    created_ticket, ticket_data.status
                )
            except Exception as e:
                logger.warning(
                    "Ticket %s created but status '%s' could not be applied: %s",
                    created_ticket.external_ticket_id,
                    ticket_data.status,
                    e,
                )

        # Ensure ticket is stored in database
        if not created_ticket.id:
            # Store in database if adapter didn't
            created_ticket.organization_id = board_reg.organization_id
            created_ticket.board_registration_id = board_reg.id
            created_ticket.project_id = board_reg.project_id
            # Attribute the row to the creating user, matching the InnoDay-only
            # create path (create_ticket_by_id sets created_by). Without this,
            # board-pushed tickets persisted with created_by=NULL while
            # otherwise-identical InnoDay-only tickets did not.
            if not created_ticket.created_by:
                created_ticket.created_by = user_id
            self.session.add(created_ticket)
            self.session.commit()
            self.session.refresh(created_ticket)

        logger.info(
            f"Created ticket {created_ticket.id} on board {board_reg.board_name}"
        )

        # Return response
        return TicketCreateResponse(
            id=created_ticket.id,
            external_id=created_ticket.external_ticket_id,
            external_url=created_ticket.url
            or f"https://example.com/ticket/{created_ticket.external_ticket_id}",
            summary=created_ticket.summary,
            description=created_ticket.description,
            status=created_ticket.status,
            board_id=board_reg.id,
            board_name=board_reg.board_name,
            created_at=created_ticket.created_at,
            created_by=user_id,
        )

    async def create_tickets_bulk(
        self,
        board_registration_id: str,
        bulk_request: BulkTicketCreateRequest,
        user_id: str,
        token: Optional[str] = None,
    ) -> BulkTicketCreateResponse:
        """
        Create multiple tickets on an external board

        Args:
            board_registration_id: ID of the board registration
            bulk_request: Bulk ticket creation request
            user_id: ID of the user creating tickets
            token: Optional API token

        Returns:
            Bulk creation response with created and failed tickets
        """
        created = []
        failed = []

        for ticket_data in bulk_request.tickets:
            try:
                # Apply defaults if not specified
                if not ticket_data.list_id and bulk_request.default_list_id:
                    ticket_data.list_id = bulk_request.default_list_id

                if not ticket_data.assignee and bulk_request.default_assignee:
                    ticket_data.assignee = bulk_request.default_assignee

                if bulk_request.default_labels:
                    ticket_data.labels.extend(bulk_request.default_labels)

                # Create the ticket
                response = await self.create_ticket_on_board(
                    board_registration_id, ticket_data, user_id, token
                )
                created.append(response)

            except Exception as e:
                logger.error(f"Failed to create ticket '{ticket_data.summary}': {e}")
                failed.append({"ticket": ticket_data.model_dump(), "error": str(e)})

        return BulkTicketCreateResponse(
            created=created,
            failed=failed,
            summary=f"Created {len(created)} tickets, {len(failed)} failed",
        )

    async def get_available_lists(
        self, board_registration_id: str, token: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Get available lists/columns for a board

        Args:
            board_registration_id: Board registration ID
            token: Optional API token

        Returns:
            List of dicts with 'id' and 'name' keys
        """
        board_reg = self.session.get(BoardRegistration, board_registration_id)
        if not board_reg:
            raise ValueError(f"Board registration {board_registration_id} not found")

        # Guard org for None -- every sibling method does, and this one didn't:
        # an orphaned board turned org.alias into an AttributeError → 500.
        org = self.session.get(Organization, board_reg.organization_id)
        if not org:
            raise ValueError(f"Organization {board_reg.organization_id} not found")

        token = self._resolve_token(board_reg, org, token)

        # Get adapter and retrieve metadata
        adapter = await self._get_adapter(board_reg, token)
        await adapter.initialize(token)
        metadata = await adapter.get_board_metadata()

        # Format response based on board type
        if board_reg.board_type == BoardType.TRELLO:
            # Return Trello lists
            lists = metadata.get("lists", [])
            return [{"id": lst["id"], "name": lst["name"]} for lst in lists]

        elif board_reg.board_type == BoardType.JIRA:
            # Return Jira statuses or issue types
            statuses = metadata.get("statuses", [])
            if statuses:
                return [
                    {"id": s.get("id", s.get("name")), "name": s.get("name", "Unknown")}
                    for s in statuses
                ]
            else:
                # Fallback to common issue types
                return [
                    {"id": "Task", "name": "Task"},
                    {"id": "Bug", "name": "Bug"},
                    {"id": "Story", "name": "Story"},
                    {"id": "Epic", "name": "Epic"},
                ]

        elif board_reg.board_type == BoardType.LINEAR:
            states = metadata.get("status_options", [])
            return [{"id": s, "name": s} for s in states]

        return []
