from uuid import UUID

from pydantic import BaseModel, Field


class CreateWorkspacePayload(BaseModel):
    """Payload for creating a new workspace."""

    name: str = Field(description="Human-readable name for the workspace")
    description: str | None = Field(default=None, description="Optional description")
    project_id: UUID | None = Field(
        default=None,
        description="Project to associate with this workspace (inherits project sharing)",
    )
    tags: list[str] | None = Field(
        default=None,
        description="Additional tags (the 'workspace' tag is always added)",
    )


class UpdateWorkspacePayload(BaseModel):
    """Payload for updating a workspace's mutable fields."""

    name: str | None = Field(default=None, description="New name for the workspace")
    description: str | None = Field(
        default=None, description="New description for the workspace"
    )
