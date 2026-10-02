"""Workflow execution transition models."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class WorkflowContext(BaseModel):
    """Context snapshot captured at a workflow state transition."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    context_store: dict[str, Any] = {}
    next: list[str] = []
    messages: list[str] = []
    user_input: str | None = None
    final_summary: list[Any] = []


class WorkflowTransition(BaseModel):
    """A single state-to-state transition within a workflow execution."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    execution_id: str
    from_state_id: str | None = None
    to_state_id: str
    workflow_context: WorkflowContext
    date: datetime
