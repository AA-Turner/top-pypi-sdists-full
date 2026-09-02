"""API endpoints for project scope management."""

from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from src.database import get_session
from src.domain.organization import Organization
from src.domain.project import Project, ProjectStatus
from src.domain.project_update import ProjectUpdate, UpdateType
from src.domain.scope_document import ScopeDocument, ScopeStatus
from src.domain.user import User
from src.middleware.rbac import get_current_user, require_org_role
from src.routers.boards import resolve_board_sync_credential
from src.services.scope_service import ScopeService
from src.services.ticket_generation_service import (
    GenerationOptions,
    TicketGenerationResponse,
    TicketGenerationService,
)

router = APIRouter(prefix="/api/v1", tags=["scopes"])


# Request/Response Models
class CreateScopeRequest(BaseModel):
    """Request to create initial scope document."""

    requirements: str = Field(..., description="Initial requirements from client")
    created_by: str = Field(..., description="User ID or 'agent'")


class UpdateScopeRequest(BaseModel):
    """Request to update scope document."""

    refined_scope: Optional[str] = None
    deliverables: Optional[str] = None
    success_criteria: Optional[str] = None
    assumptions: Optional[str] = None
    exclusions: Optional[str] = None
    technical_requirements: Optional[str] = None
    estimated_hours: Optional[int] = None
    estimated_cost: Optional[float] = None
    confidence_score: Optional[float] = None


class AddProjectUpdateRequest(BaseModel):
    """Request to add a project update."""

    update_type: UpdateType
    content: str
    created_by: str = Field(..., description="User ID or 'agent'")
    requires_client_input: bool = False


class ProcessUpdateRequest(BaseModel):
    """Request to process a project update."""

    response: Optional[str] = None


class UpdateProjectStatusRequest(BaseModel):
    """Request to update project status."""

    date: datetime = Field(..., description="Status change date")
    description: str = Field(..., description="Reason for status change")


class ScopeDocumentResponse(BaseModel):
    """Response with scope document details."""

    id: str
    project_id: str
    version: int
    is_current: bool
    status: ScopeStatus
    requirements: str
    refined_scope: str
    deliverables: Optional[str]
    success_criteria: Optional[str]
    assumptions: Optional[str]
    exclusions: Optional[str]
    estimated_hours: Optional[int]
    estimated_cost: Optional[float]
    technical_requirements: Optional[str]
    clarification_rounds: int
    confidence_score: Optional[float]
    created_at: datetime
    updated_at: datetime
    finalized_at: Optional[datetime]
    created_by: str


class ProjectUpdateResponse(BaseModel):
    """Response with project update details."""

    id: str
    project_id: str
    update_type: UpdateType
    content: str
    scope_document_id: Optional[str]
    processed: bool
    processed_at: Optional[datetime]
    response: Optional[str]
    requires_client_input: bool
    context: Optional[str]
    created_by: str
    created_at: datetime
    updated_at: datetime


# Endpoints
@router.post(
    "/organizations/{org_id}/projects/{project_id}/scope",
    response_model=ScopeDocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_scope_document(
    org_id: str,
    project_id: str,
    request: CreateScopeRequest,
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Create initial scope document for a project."""
    # Verify project exists and belongs to organization
    #
    # The five 404s in this file used to end "... in organization {org_id}". Both
    # path params now arrive resolved (see `normalize_path_refs`), so that named
    # an org UUID the caller had not typed -- and since an unresolvable project
    # ref 404s inside the guard, the only way to reach these messages is a project
    # UUID belonging to another org. One identifier, the one that was sent.
    project = session.exec(
        select(Project).where(
            Project.id == project_id, Project.organization_id == org_id
        )
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found in this organization",
        )

    service = ScopeService(session)
    scope = service.create_initial_scope(
        project_id=project_id,
        requirements=request.requirements,
        created_by=request.created_by,
    )

    return ScopeDocumentResponse.model_validate(scope, from_attributes=True)


@router.get(
    "/organizations/{org_id}/projects/{project_id}/scope",
    response_model=Optional[ScopeDocumentResponse],
)
async def get_current_scope(
    org_id: str,
    project_id: str,
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Get current active scope document for a project."""
    # Verify project exists and belongs to organization
    project = session.exec(
        select(Project).where(
            Project.id == project_id, Project.organization_id == org_id
        )
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found in this organization",
        )

    service = ScopeService(session)
    scope = service.get_current_scope(project_id)

    if not scope:
        return None

    return ScopeDocumentResponse.model_validate(scope, from_attributes=True)


@router.put(
    "/organizations/{org_id}/projects/{project_id}/scope/{scope_id}",
    response_model=ScopeDocumentResponse,
)
async def update_scope_document(
    org_id: str,
    project_id: str,
    scope_id: str,
    request: UpdateScopeRequest,
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Update a scope document."""
    # Verify scope belongs to project in organization
    scope = session.exec(
        select(ScopeDocument)
        .join(Project)
        .where(
            ScopeDocument.id == scope_id,
            ScopeDocument.project_id == project_id,
            Project.organization_id == org_id,
        )
    ).first()

    if not scope:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Scope {scope_id} not found"
        )

    service = ScopeService(session)
    updated_scope = service.update_scope(
        scope_id=scope_id, **request.model_dump(exclude_unset=True)
    )

    return ScopeDocumentResponse.model_validate(updated_scope, from_attributes=True)


@router.post(
    "/organizations/{org_id}/projects/{project_id}/scope/{scope_id}/finalize",
    response_model=ScopeDocumentResponse,
)
async def finalize_scope(
    org_id: str,
    project_id: str,
    scope_id: str,
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Mark scope document as final and ready for approval."""
    # Verify scope belongs to project in organization
    scope = session.exec(
        select(ScopeDocument)
        .join(Project)
        .where(
            ScopeDocument.id == scope_id,
            ScopeDocument.project_id == project_id,
            Project.organization_id == org_id,
        )
    ).first()

    if not scope:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Scope {scope_id} not found"
        )

    service = ScopeService(session)
    finalized_scope = service.finalize_scope(scope_id)

    return ScopeDocumentResponse.model_validate(finalized_scope, from_attributes=True)


@router.post(
    "/organizations/{org_id}/projects/{project_id}/updates",
    response_model=ProjectUpdateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_project_update(
    org_id: str,
    project_id: str,
    request: AddProjectUpdateRequest,
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Add an update to the project requirements workflow."""
    # Verify project exists and belongs to organization
    project = session.exec(
        select(Project).where(
            Project.id == project_id, Project.organization_id == org_id
        )
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found in this organization",
        )

    # Get current scope if exists
    service = ScopeService(session)
    current_scope = service.get_current_scope(project_id)

    update = service.add_project_update(
        project_id=project_id,
        update_type=request.update_type,
        content=request.content,
        created_by=request.created_by,
        scope_document_id=current_scope.id if current_scope else None,
        requires_client_input=request.requires_client_input,
    )

    return ProjectUpdateResponse.model_validate(update, from_attributes=True)


@router.get(
    "/organizations/{org_id}/projects/{project_id}/updates",
    response_model=List[ProjectUpdateResponse],
)
async def get_project_updates(
    org_id: str,
    project_id: str,
    pending_only: bool = False,
    requires_input: bool = False,
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Get project updates."""
    # Verify project exists and belongs to organization
    project = session.exec(
        select(Project).where(
            Project.id == project_id, Project.organization_id == org_id
        )
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found in this organization",
        )

    service = ScopeService(session)

    if requires_input:
        updates = service.get_updates_requiring_input(project_id)
    elif pending_only:
        updates = service.get_pending_updates(project_id)
    else:
        # Get all updates
        updates = session.exec(
            select(ProjectUpdate)
            .where(ProjectUpdate.project_id == project_id)
            .order_by(ProjectUpdate.created_at)
        ).all()

    return [
        ProjectUpdateResponse.model_validate(u, from_attributes=True) for u in updates
    ]


@router.put(
    "/organizations/{org_id}/projects/{project_id}/updates/{update_id}/process",
    response_model=ProjectUpdateResponse,
)
async def process_project_update(
    org_id: str,
    project_id: str,
    update_id: str,
    request: ProcessUpdateRequest,
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Process a project update."""
    # Verify update belongs to project in organization
    update = session.exec(
        select(ProjectUpdate)
        .join(Project)
        .where(
            ProjectUpdate.id == update_id,
            ProjectUpdate.project_id == project_id,
            Project.organization_id == org_id,
        )
    ).first()

    if not update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Update {update_id} not found",
        )

    service = ScopeService(session)
    processed_update = service.process_update(
        update_id=update_id, response=request.response
    )

    return ProjectUpdateResponse.model_validate(processed_update, from_attributes=True)


@router.put(
    "/organizations/{org_id}/projects/{project_id}/status/{status}", response_model=dict
)
async def update_project_status(
    org_id: str,
    project_id: str,
    status: ProjectStatus,
    request: UpdateProjectStatusRequest,
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
):
    """Update project status (for approval workflow)."""
    # Verify project exists and belongs to organization
    project = session.exec(
        select(Project).where(
            Project.id == project_id, Project.organization_id == org_id
        )
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found in this organization",
        )

    # Update project status
    project.status = status
    project.updated_at = datetime.now(timezone.utc)

    session.add(project)
    session.commit()

    # Log the status change as a project update
    service = ScopeService(session)
    service.add_project_update(
        project_id=project_id,
        update_type=UpdateType.FEEDBACK,
        content=f"Project status changed to {status}: {request.description}",
        created_by="system",
    )

    return {
        "project_id": project_id,
        "status": status,
        "date": request.date,
        "description": request.description,
        "message": f"Project status updated to {status}",
    }


# Request model for ticket generation
class GenerateTicketsRequest(BaseModel):
    """Request to generate tickets from scope document."""

    board_id: str = Field(..., description="Board registration ID")
    create_epics: bool = Field(default=True, description="Create epic tickets")
    create_hierarchy: bool = Field(default=True, description="Link stories to epics")
    additional_context: Optional[str] = Field(
        None, description="Additional context for AI"
    )
    max_tickets: int = Field(default=50, ge=1, le=100)


@router.post(
    "/organizations/{org_id}/projects/{project_id}/scope/{scope_id}/generate",
    response_model=TicketGenerationResponse,
)
async def generate_tickets_from_scope(
    org_id: str,
    project_id: str,
    scope_id: str,
    request: GenerateTicketsRequest,
    x_integration_token: Optional[str] = Header(None, alias="X-Integration-Token"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Generate tickets on external board from scope document using AI.

    This endpoint uses Claude AI to analyze the scope document and generate
    a structured hierarchy of tickets (epics, stories, tasks) on the specified board.

    **Requirements:**
    - Scope must be in FINAL status
    - Board must be registered and active
    - A credential for the board: either the one stored in Vault at
      registration time (the normal path), or an X-Integration-Token header
      for a one-off override. The header was required until #609, which
      forced a caller to supply a board credential from outside the platform
      even when the board already had one stored.

    **Process:**
    1. Validates scope is finalized
    2. Checks for duplicate generation
    3. Uses Claude AI to parse scope into tickets
    4. Creates tickets on external board
    5. Tracks generation for audit trail

    **Example Request:**
    ```json
    {
        "board_id": "uuid-of-board",
        "create_epics": true,
        "create_hierarchy": true,
        "additional_context": "Focus on MVP features first"
    }
    ```

    **Example Response:**
    ```json
    {
        "generation_id": "uuid",
        "status": "completed",
        "tickets_generated": 25,
        "epics_created": 3,
        "stories_created": 22,
        "board_url": "https://company.atlassian.net/board/123",
        "epic_tickets": [
            {
                "external_id": "PROJ-101",
                "summary": "Authentication System",
                "child_count": 5,
                "children": ["PROJ-102", "PROJ-103", ...]
            }
        ]
    }
    ```
    """
    # Verify scope belongs to project in organization
    scope = session.exec(
        select(ScopeDocument)
        .join(Project)
        .where(
            ScopeDocument.id == scope_id,
            ScopeDocument.project_id == project_id,
            Project.organization_id == org_id,
        )
    ).first()

    if not scope:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Scope {scope_id} not found"
        )

    # The board's own credential is the normal source; the header is a
    # one-off override. Shared with both board sync endpoints so all three
    # resolve identically -- see resolve_board_sync_credential's docstring.
    _registration, token = resolve_board_sync_credential(
        session, org_id, request.board_id, x_integration_token
    )

    # Initialize service and generate tickets
    service = TicketGenerationService(session)

    try:
        options = GenerationOptions(
            create_epics=request.create_epics,
            create_hierarchy=request.create_hierarchy,
            additional_context=request.additional_context,
            max_tickets=request.max_tickets,
        )

        response = await service.generate_tickets_from_scope(
            scope_id=scope_id,
            board_id=request.board_id,
            user_id=current_user.id,
            token=token,
            options=options,
        )

        return response

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ticket generation failed: {str(e)}",
        )
