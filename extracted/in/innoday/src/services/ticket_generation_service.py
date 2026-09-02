"""
Ticket Generation Service - AI-driven ticket creation from scope documents.

This service consolidates existing components to generate structured tickets
from scope documents using Claude AI.

Reuses:
- ClaudeTicketParser: AI analysis and ticket parsing
- BoardTicketCreationService: Ticket creation on external boards
- ScopeService: Scope document management
"""

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from uuid import uuid4

from pydantic import BaseModel, Field
from sqlmodel import Session, select

from src.domain import (
    BoardRegistration,
    GenerationStatus,
    Organization,
    Project,
    ScopeDocument,
    ScopeStatus,
    ScopeTicketGeneration,
)
from src.services.board_ticket_creation_service import (
    BoardTicketCreationService,
    TicketCreateRequest,
    TicketCreateResponse,
)
from src.services.claude_ticket_parser import ClaudeTicketParser, ParsedTicket
from src.services.scope_service import ScopeService

logger = logging.getLogger(__name__)


class GenerationOptions(BaseModel):
    """Options for ticket generation"""

    create_epics: bool = Field(default=True, description="Create epic tickets")
    create_hierarchy: bool = Field(default=True, description="Link stories to epics")
    additional_context: Optional[str] = Field(
        None, description="Additional context for AI"
    )
    max_tickets: int = Field(default=50, ge=1, le=100)


class TicketGenerationResponse(BaseModel):
    """Response from ticket generation"""

    generation_id: str
    status: GenerationStatus
    tickets_generated: int
    epics_created: int
    stories_created: int
    tasks_created: int
    board_url: str
    epic_tickets: List[Dict] = Field(
        default_factory=list, description="Epic tickets with children"
    )
    generation_time_seconds: Optional[int] = None


class TicketGenerationService:
    """
    AI-driven ticket generation from scope documents.

    Consolidates existing services to minimize code duplication:
    - Uses ClaudeTicketParser for AI analysis
    - Uses BoardTicketCreationService for ticket creation
    - Uses ScopeService for scope management
    """

    def __init__(self, session: Session):
        self.session = session
        self.scope_service = ScopeService(session)
        self.board_service = BoardTicketCreationService(session)
        # ClaudeTicketParser will be initialized per-organization

    async def generate_tickets_from_scope(
        self,
        scope_id: str,
        board_id: str,
        user_id: str,
        token: str,
        options: GenerationOptions,
    ) -> TicketGenerationResponse:
        """
        Generate tickets from scope document using AI.

        Steps:
        1. Validate scope is FINAL
        2. Check for existing generation (prevent duplicates)
        3. Build AI prompt with scope context
        4. Parse scope into structured tickets
        5. Create tickets on external board
        6. Track generation in database
        """
        # Get scope document
        scope = self.session.get(ScopeDocument, scope_id)
        if not scope:
            raise ValueError(f"Scope document {scope_id} not found")

        if scope.status != ScopeStatus.FINAL:
            raise ValueError(
                f"Scope must be FINAL status to generate tickets (current: {scope.status})"
            )

        # Get project and organization
        project = self.session.get(Project, scope.project_id)
        if not project:
            raise ValueError(f"Project {scope.project_id} not found")

        organization = self.session.get(Organization, project.organization_id)
        if not organization:
            raise ValueError(f"Organization {project.organization_id} not found")

        # Get board registration
        board = self.session.get(BoardRegistration, board_id)
        if not board:
            raise ValueError(f"Board {board_id} not found")

        # Check for existing generation
        existing = self.session.exec(
            select(ScopeTicketGeneration)
            .where(ScopeTicketGeneration.scope_document_id == scope_id)
            .where(ScopeTicketGeneration.board_registration_id == board_id)
            .where(ScopeTicketGeneration.status == GenerationStatus.COMPLETED)
        ).first()

        if existing:
            raise ValueError(
                f"Tickets already generated for this scope on this board (generation_id: {existing.id})"
            )

        # Create generation tracking record
        generation = ScopeTicketGeneration(
            id=str(uuid4()),
            scope_document_id=scope_id,
            project_id=project.id,
            organization_id=organization.id,
            board_registration_id=board_id,
            status=GenerationStatus.IN_PROGRESS,
            created_by=user_id,
        )
        self.session.add(generation)
        self.session.commit()

        try:
            # Build AI prompt and parse tickets
            parsed_tickets = await self._parse_scope_with_ai(
                scope, project, organization, options
            )

            # Create tickets on external board
            created_tickets, epic_mapping = await self._create_tickets_on_board(
                parsed_tickets, board_id, token, user_id, options
            )

            # Update generation record
            generation.status = GenerationStatus.COMPLETED
            generation.tickets_generated = len(created_tickets)
            generation.epics_created = sum(1 for t in parsed_tickets if t.epic is None)
            generation.stories_created = sum(
                1 for t in parsed_tickets if t.epic is not None
            )
            generation.tasks_created = 0  # Can enhance later
            generation.ticket_ids = [t.id for t in created_tickets]
            generation.external_ticket_ids = [t.external_id for t in created_tickets]
            generation.epic_mapping = epic_mapping
            generation.completed_at = datetime.now(timezone.utc)

            self.session.add(generation)
            self.session.commit()

            # Build response
            epic_tickets = self._build_epic_hierarchy(parsed_tickets, created_tickets)

            return TicketGenerationResponse(
                generation_id=generation.id,
                status=generation.status,
                tickets_generated=generation.tickets_generated,
                epics_created=generation.epics_created,
                stories_created=generation.stories_created,
                tasks_created=generation.tasks_created,
                board_url=board.board_url,
                epic_tickets=epic_tickets,
                generation_time_seconds=generation.duration_seconds,
            )

        except Exception as e:
            # Mark as failed
            generation.status = GenerationStatus.FAILED
            generation.error_message = str(e)
            generation.completed_at = datetime.now(timezone.utc)
            self.session.add(generation)
            self.session.commit()

            logger.error(f"Ticket generation failed for scope {scope_id}: {str(e)}")
            raise

    async def _parse_scope_with_ai(
        self,
        scope: ScopeDocument,
        project: Project,
        organization: Organization,
        options: GenerationOptions,
    ) -> List[ParsedTicket]:
        """
        Use Claude AI to parse scope document into structured tickets.

        Reuses ClaudeTicketParser for AI integration.
        """
        # Initialize parser with organization context
        parser = ClaudeTicketParser(organization_alias=organization.alias)

        # Build comprehensive prompt
        prompt_text = self._build_scope_prompt(scope, project, options)

        # Parse using existing Claude parser
        from src.services.claude_ticket_parser import TicketParseRequest

        parse_request = TicketParseRequest(
            text=prompt_text,
            context=f"Project: {project.name}. Generate hierarchical ticket structure from scope.",
            max_tickets=options.max_tickets,
        )

        parse_response = await parser.parse_text_to_tickets(parse_request)

        logger.info(
            f"Parsed {len(parse_response.tickets)} tickets from scope {scope.id}"
        )
        return parse_response.tickets

    def _build_scope_prompt(
        self, scope: ScopeDocument, project: Project, options: GenerationOptions
    ) -> str:
        """Build AI prompt for scope analysis"""
        prompt_parts = [
            f"# Project: {project.name}",
            f"\n{project.description or ''}\n",
            f"## Goals\n{project.goals or 'Not specified'}\n",
            f"## Refined Scope\n{scope.refined_scope}\n",
        ]

        if scope.deliverables:
            prompt_parts.append(f"## Deliverables\n{scope.deliverables}\n")

        if scope.technical_requirements:
            prompt_parts.append(
                f"## Technical Requirements\n{scope.technical_requirements}\n"
            )

        if scope.success_criteria:
            prompt_parts.append(f"## Success Criteria\n{scope.success_criteria}\n")

        if scope.estimated_hours:
            prompt_parts.append(
                f"## Estimated Effort\n{scope.estimated_hours} hours total\n"
            )

        if options.additional_context:
            prompt_parts.append(
                f"## Additional Context\n{options.additional_context}\n"
            )

        if options.create_epics:
            prompt_parts.append(
                "\n**Instructions:** Break this down into epics (major features) and stories (user-facing functionality). "
                "Use the 'epic' field to create hierarchy."
            )

        return "\n".join(prompt_parts)

    async def _create_tickets_on_board(
        self,
        parsed_tickets: List[ParsedTicket],
        board_id: str,
        token: str,
        user_id: str,
        options: GenerationOptions,
    ) -> Tuple[List[TicketCreateResponse], Dict[str, List[str]]]:
        """
        Create tickets on external board.

        Reuses BoardTicketCreationService for ticket creation.
        Returns (created_tickets, epic_mapping)
        """
        created_tickets = []
        epic_mapping: Dict[str, List[str]] = {}

        # First pass: Create epics
        epic_id_map: Dict[str, str] = {}  # epic_name -> external_id
        for parsed in parsed_tickets:
            if parsed.epic is None:  # This is an epic
                try:
                    request = TicketCreateRequest(
                        summary=parsed.summary,
                        description=parsed.description or "",
                        priority=parsed.priority,
                        labels=parsed.labels or [],
                        story_points=(
                            int(parsed.estimated_hours)
                            if parsed.estimated_hours
                            else None
                        ),
                    )

                    created = await self.board_service.create_ticket_on_board(
                        board_registration_id=board_id,
                        ticket_data=request,
                        user_id=user_id,
                        token=token,
                    )
                    created_tickets.append(created)
                    epic_id_map[parsed.summary] = created.external_id
                    epic_mapping[created.external_id] = []

                    logger.info(
                        f"Created epic: {created.external_id} - {parsed.summary}"
                    )

                except Exception as e:
                    logger.error(f"Failed to create epic {parsed.summary}: {str(e)}")

        # Second pass: Create stories linked to epics
        for parsed in parsed_tickets:
            if parsed.epic:  # This is a story
                try:
                    epic_link = epic_id_map.get(parsed.epic)

                    request = TicketCreateRequest(
                        summary=parsed.summary,
                        description=parsed.description or "",
                        priority=parsed.priority,
                        labels=parsed.labels or [],
                        epic_link=epic_link,
                        story_points=(
                            int(parsed.estimated_hours)
                            if parsed.estimated_hours
                            else None
                        ),
                    )

                    created = await self.board_service.create_ticket_on_board(
                        board_registration_id=board_id,
                        ticket_data=request,
                        user_id=user_id,
                        token=token,
                    )
                    created_tickets.append(created)

                    if epic_link and epic_link in epic_mapping:
                        epic_mapping[epic_link].append(created.external_id)

                    logger.info(
                        f"Created story: {created.external_id} - {parsed.summary} (epic: {epic_link})"
                    )

                except Exception as e:
                    logger.error(f"Failed to create story {parsed.summary}: {str(e)}")

        return created_tickets, epic_mapping

    def _build_epic_hierarchy(
        self,
        parsed_tickets: List[ParsedTicket],
        created_tickets: List[TicketCreateResponse],
    ) -> List[Dict]:
        """Build epic hierarchy for response"""
        epic_tickets = []

        # Map parsed tickets to created tickets
        ticket_map = {t.summary: t for t in created_tickets}

        for parsed in parsed_tickets:
            if parsed.epic is None:  # This is an epic
                created = ticket_map.get(parsed.summary)
                if created:
                    children = [
                        ticket_map[p.summary].external_id
                        for p in parsed_tickets
                        if p.epic == parsed.summary and p.summary in ticket_map
                    ]

                    epic_tickets.append(
                        {
                            "external_id": created.external_id,
                            "summary": parsed.summary,
                            "child_count": len(children),
                            "children": children,
                        }
                    )

        return epic_tickets
