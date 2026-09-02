"""Container execution domain model for tracking Claude Code Docker container runs."""

from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, Optional
from uuid import uuid4

from pydantic import ConfigDict
from sqlmodel import Field, Relationship, SQLModel

from src.domain._base import TimestampMixin

if TYPE_CHECKING:
    from .organization import Organization
    from .user import User


class ContainerStatus(str, Enum):
    """Status enum for container execution tracking."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class ContainerExecution(TimestampMixin, table=True):
    """
    Model for tracking Claude Code container executions.

    This model tracks all container executions initiated through the agent,
    including the instruction, repository, execution status, and results.
    """

    __tablename__ = "container_executions"

    # Primary identification
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)

    # User and organization context
    user_id: str = Field(foreign_key="users.id", index=True)
    organization_id: str = Field(
        foreign_key="organizations.id", nullable=False, index=True
    )

    # Container information
    container_id: Optional[str] = Field(default=None, index=True)  # Docker container ID
    container_name: Optional[str] = Field(default=None)  # Human-readable container name

    # Execution parameters
    instruction: str = Field(
        description="The coding task or instruction for Claude Code"
    )
    github_repo: str = Field(description="Repository URL to checkout and analyze")
    branch: str = Field(default="main", description="Git branch to checkout")
    command: Optional[str] = Field(
        default=None, description="Actual command executed in container"
    )

    # Execution status and timing
    status: ContainerStatus = Field(default=ContainerStatus.PENDING, index=True)
    started_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    completed_at: Optional[datetime] = Field(default=None)
    timeout_seconds: int = Field(
        default=600, description="Execution timeout in seconds"
    )

    # Results and output
    exit_code: Optional[int] = Field(default=None)
    output: Optional[str] = Field(default=None, description="Container stdout output")
    error_output: Optional[str] = Field(
        default=None, description="Container stderr output"
    )
    error_message: Optional[str] = Field(
        default=None, description="Execution error description"
    )

    # Metadata and configuration
    container_options: Optional[str] = Field(
        default=None, description="JSON string of Docker options"
    )
    resource_limits: Optional[str] = Field(
        default=None, description="JSON string of resource limits"
    )

    # Audit fields

    # Relationships
    user: "User" = Relationship(back_populates="container_executions")
    organization: "Organization" = Relationship(back_populates="container_executions")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def duration_seconds(self) -> Optional[float]:
        """Calculate execution duration in seconds."""
        if self.completed_at and self.started_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    @property
    def is_running(self) -> bool:
        """Check if the container is currently running."""
        return self.status == ContainerStatus.RUNNING

    @property
    def is_completed(self) -> bool:
        """Check if the container execution has completed (success or failure)."""
        return self.status in [
            ContainerStatus.COMPLETED,
            ContainerStatus.FAILED,
            ContainerStatus.TIMEOUT,
            ContainerStatus.CANCELLED,
        ]

    @property
    def was_successful(self) -> bool:
        """Check if the container execution was successful."""
        return self.status == ContainerStatus.COMPLETED and (
            self.exit_code == 0 or self.exit_code is None
        )

    def get_container_options_dict(self) -> Dict[str, Any]:
        """Parse container options from JSON string."""
        if not self.container_options:
            return {}

        import json

        try:
            return json.loads(self.container_options)
        except (json.JSONDecodeError, TypeError):
            return {}

    def set_container_options_dict(self, options: Dict[str, Any]) -> None:
        """Set container options as JSON string."""
        import json

        self.container_options = json.dumps(options) if options else None

    def get_resource_limits_dict(self) -> Dict[str, Any]:
        """Parse resource limits from JSON string."""
        if not self.resource_limits:
            return {}

        import json

        try:
            return json.loads(self.resource_limits)
        except (json.JSONDecodeError, TypeError):
            return {}

    def set_resource_limits_dict(self, limits: Dict[str, Any]) -> None:
        """Set resource limits as JSON string."""
        import json

        self.resource_limits = json.dumps(limits) if limits else None

    def mark_as_running(
        self, container_id: str, container_name: Optional[str] = None
    ) -> None:
        """Mark the execution as running with container details."""
        self.status = ContainerStatus.RUNNING
        self.container_id = container_id
        self.container_name = container_name
        self.touch()

    def mark_as_completed(
        self,
        exit_code: int,
        output: Optional[str] = None,
        error_output: Optional[str] = None,
    ) -> None:
        """Mark the execution as completed with results."""
        self.status = ContainerStatus.COMPLETED
        self.exit_code = exit_code
        self.output = output
        self.error_output = error_output
        self.completed_at = datetime.now(timezone.utc)
        self.touch()

    def mark_as_failed(
        self,
        error_message: str,
        exit_code: Optional[int] = None,
        error_output: Optional[str] = None,
    ) -> None:
        """Mark the execution as failed with error details."""
        self.status = ContainerStatus.FAILED
        self.error_message = error_message
        self.exit_code = exit_code
        self.error_output = error_output
        self.completed_at = datetime.now(timezone.utc)
        self.touch()

    def mark_as_timeout(self) -> None:
        """Mark the execution as timed out."""
        self.status = ContainerStatus.TIMEOUT
        self.error_message = f"Execution timed out after {self.timeout_seconds} seconds"
        self.completed_at = datetime.now(timezone.utc)
        self.touch()

    def mark_as_cancelled(self, reason: Optional[str] = None) -> None:
        """Mark the execution as cancelled."""
        self.status = ContainerStatus.CANCELLED
        self.error_message = reason or "Execution cancelled by user"
        self.completed_at = datetime.now(timezone.utc)
        self.touch()


# Pydantic models for API requests/responses
class ContainerExecuteRequest(SQLModel):
    """Request model for executing Claude Code in a container."""

    instruction: str = Field(
        description="The coding task or instruction for Claude Code"
    )
    github_repo: str = Field(
        description="GitHub repository URL to checkout and analyze"
    )
    branch: str = Field(default="main", description="Git branch to checkout")
    timeout: int = Field(
        default=600, ge=30, le=3600, description="Execution timeout in seconds (30s-1h)"
    )
    container_options: Optional[Dict[str, Any]] = Field(
        default=None, description="Optional Docker container options"
    )
    resource_limits: Optional[Dict[str, Any]] = Field(
        default=None, description="Optional resource limits"
    )


class ContainerExecuteResponse(SQLModel):
    """Response model for container execution requests."""

    execution_id: str = Field(description="Unique execution identifier")
    status: ContainerStatus = Field(description="Current execution status")
    container_id: Optional[str] = Field(description="Docker container ID")
    message: str = Field(description="Status message")
    started_at: datetime = Field(description="Execution start time")


class ContainerExecutionSummary(SQLModel):
    """Summary model for container execution listings."""

    id: str
    instruction: str
    github_repo: str
    branch: str
    status: ContainerStatus
    started_at: datetime
    completed_at: Optional[datetime]
    duration_seconds: Optional[float]
    was_successful: bool
    user_id: str


class ContainerExecutionDetail(SQLModel):
    """Detailed model for individual container execution."""

    id: str
    user_id: str
    client_id: Optional[str]
    organization_id: Optional[str]
    container_id: Optional[str]
    container_name: Optional[str]
    instruction: str
    github_repo: str
    branch: str
    command: Optional[str]
    status: ContainerStatus
    started_at: datetime
    completed_at: Optional[datetime]
    timeout_seconds: int
    exit_code: Optional[int]
    output: Optional[str]
    error_output: Optional[str]
    error_message: Optional[str]
    container_options: Optional[Dict[str, Any]]
    resource_limits: Optional[Dict[str, Any]]
    duration_seconds: Optional[float]
    was_successful: bool
    created_at: datetime
    updated_at: datetime
