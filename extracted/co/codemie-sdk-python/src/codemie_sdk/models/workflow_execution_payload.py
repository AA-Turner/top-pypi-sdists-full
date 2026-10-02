"""Workflow execution payload models."""

from pydantic import BaseModel, ConfigDict, Field


class WorkflowExecutionCreateRequest(BaseModel):
    """Request model for workflow execution creation."""

    model_config = ConfigDict(populate_by_name=True)

    user_input: str | dict | list | int | float | bool = Field(
        None, description="User input for the workflow execution"
    )
    file_name: str | None = Field(
        None, description="File name associated with the workflow execution"
    )
    conversation_id: str | None = Field(
        None, description="Conversation ID for workflow chat mode"
    )
    session_id: str | None = Field(
        None,
        description="Session identifier for Langfuse tracing. If not provided, execution_id will be used as fallback.",
    )
    propagate_headers: bool = Field(
        default=False,
        description="Enable propagation of X-* HTTP headers to MCP servers during tool execution",
    )
    tags: list[str] | None = Field(
        None, description="Tags to attach to the workflow execution trace in Langfuse"
    )
