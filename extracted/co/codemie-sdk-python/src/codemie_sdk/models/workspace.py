"""Models for agent workspace data structures."""

from pydantic import BaseModel, ConfigDict, Field


class Workspace(BaseModel):
    """Agent workspace that belongs to one conversation (or workflow execution)."""

    model_config = ConfigDict(extra="ignore")

    id: str
    conversation_id: str
    user_id: str | None = None
    name: str | None = None
    status: str | None = None


class WorkspaceFileItem(BaseModel):
    """One file listed in a workspace."""

    model_config = ConfigDict(extra="ignore")

    path: str
    mime_type: str | None = None
    checksum: str | None = None
    size: int | None = None
    version: int | None = None


class WorkspaceFileContent(WorkspaceFileItem):
    """A workspace file with its content (text, or base64 for images)."""

    is_binary: bool = False
    content: str | None = None
    content_encoding: str | None = None


class WorkspaceDeleteFileResponse(BaseModel):
    """Result of deleting a workspace file."""

    model_config = ConfigDict(extra="ignore")

    message: str
    deleted: bool


class ExecuteWorkspaceScriptResponse(BaseModel):
    """Result of running a script stored in a workspace."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    message: str
    output: str
    workspace_files: list[WorkspaceFileItem] = Field(
        default_factory=list, alias="workspaceFiles"
    )
    warnings: list[str] = Field(default_factory=list)
