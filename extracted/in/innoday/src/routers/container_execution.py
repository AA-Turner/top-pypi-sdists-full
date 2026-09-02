"""API endpoints for Claude Code container execution tracking.

**NOT IMPLEMENTED.** Every route here is a stub and returns 501. The intended shape
is unchanged — execute Claude Code in a Docker container, track status, manage
lifecycle, scope history per organization — but none of it is built.

They previously lied about it. `execute_container` returned
`{"status": "pending"}` with a freshly-minted UUID, so a client would poll a
non-existent execution forever; the other five raised 404 "not found", which reads
as "your id is wrong" rather than "this feature does not exist". 501 is the honest
answer and keeps the route shape for whoever builds it.

The supporting `ContainerService` (542 lines) and `ClaudeLicenseService` (208 lines,
existed to cap concurrent containers by licence tier) were deleted along with three
`User` methods that only it called — nothing referenced any of them. Their env vars
(`CLAUDE_CODE_DOCKER_IMAGE`, `MAX_CONCURRENT_CONTAINERS`, `CONTAINER_WORKSPACE_BASE`,
`DEFAULT_CONTAINER_TIMEOUT`, `CLAUDE_LICENSE_*`) are deliberately absent from
`.env.example` for the same reason. See #427.
"""

import logging
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlmodel import Session

from src.database import get_session
from src.domain.organization import Organization
from src.middleware.rbac import require_org_role

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["container-execution"])


# Request/Response Models
class ContainerExecutionRequest(BaseModel):
    """Request to execute Claude Code in a container"""

    repository_url: str = Field(description="GitHub repository URL to analyze")
    branch: Optional[str] = Field(default="main", description="Branch to checkout")
    claude_code_prompt: str = Field(description="Instructions for Claude Code")
    cpu_limit: Optional[str] = Field(default="2", description="CPU cores limit")
    memory_limit: Optional[str] = Field(default="4g", description="Memory limit")
    timeout_seconds: Optional[int] = Field(
        default=3600, description="Execution timeout"
    )
    user_id: UUID = Field(description="User requesting the execution")


class ContainerExecutionStatus(BaseModel):
    """Container execution status"""

    execution_id: UUID
    status: str  # pending, running, completed, failed, cancelled
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    output: Optional[str] = None
    error: Optional[str] = None
    repository_url: str
    branch: str
    user_id: UUID
    organization_id: UUID


class ContainerExecutionListResponse(BaseModel):
    """List of container executions"""

    executions: List[ContainerExecutionStatus]
    total: int
    page: int
    page_size: int


# Endpoints
@router.post("/organizations/{organization_id}/containers/execute")
async def execute_container(
    organization_id: UUID,
    request: ContainerExecutionRequest,
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
) -> ContainerExecutionStatus:
    """
    Execute Claude Code in a Docker container for the specified repository.

    This endpoint:
    1. Validates the organization and user exist
    2. Creates a container execution record
    3. Launches a Docker container with Claude Code
    4. Returns the execution status for tracking
    """
    raise HTTPException(
        status_code=501,
        detail="Container execution is not implemented. See GitHub issue #427.",
    )


@router.get("/organizations/{organization_id}/containers/executions")
async def list_executions(
    organization_id: UUID,
    user_id: Optional[UUID] = Query(None, description="Filter by user"),
    status: Optional[str] = Query(None, description="Filter by status"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
) -> ContainerExecutionListResponse:
    """
    List container executions for the organization.

    Supports filtering by:
    - User ID
    - Execution status (pending, running, completed, failed, cancelled)
    """
    raise HTTPException(
        status_code=501,
        detail="Container execution is not implemented. See GitHub issue #427.",
    )


@router.get("/organizations/{organization_id}/containers/executions/{execution_id}")
async def get_execution_status(
    organization_id: UUID,
    execution_id: UUID,
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
) -> ContainerExecutionStatus:
    """
    Get the status of a specific container execution.

    Returns current status, output (if available), and error information.
    """
    raise HTTPException(
        status_code=501,
        detail="Container execution is not implemented. See GitHub issue #427.",
    )


@router.post(
    "/organizations/{organization_id}/containers/executions/{execution_id}/cancel"
)
async def cancel_execution(
    organization_id: UUID,
    execution_id: UUID,
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
) -> ContainerExecutionStatus:
    """
    Cancel a running container execution.

    This will:
    1. Stop the Docker container
    2. Update the execution status to 'cancelled'
    3. Preserve any partial output
    """
    raise HTTPException(
        status_code=501,
        detail="Container execution is not implemented. See GitHub issue #427.",
    )


@router.delete("/organizations/{organization_id}/containers/executions/{execution_id}")
async def delete_execution(
    organization_id: UUID,
    execution_id: UUID,
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
) -> dict:
    """
    Delete a container execution record.

    This only removes the database record. The container must already be stopped.
    """
    raise HTTPException(
        status_code=501,
        detail="Container execution is not implemented. See GitHub issue #427.",
    )


@router.get(
    "/organizations/{organization_id}/containers/executions/{execution_id}/logs"
)
async def get_execution_logs(
    organization_id: UUID,
    execution_id: UUID,
    tail: Optional[int] = Query(None, description="Number of lines from the end"),
    session: Session = Depends(get_session),
    _org: Organization = Depends(require_org_role()),
) -> dict:
    """
    Get real-time logs from a container execution.

    Supports tailing the last N lines of output.
    """
    raise HTTPException(
        status_code=501,
        detail="Container execution is not implemented. See GitHub issue #427.",
    )
