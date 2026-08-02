"""Pydantic models for serializable workflow input."""

from typing import Any, TypeVar

from pydantic import BaseModel, Field, JsonValue

ConfigT = TypeVar("ConfigT", bound=BaseModel)


class WorkflowTaskInput[ConfigT: BaseModel](BaseModel):
    """Serializable input for running a task as a durable workflow.

    Combines the task-specific config (e.g. AgentTaskConfig) with the
    initial state and task ID. The generic parameter ensures type-safe
    deserialization at the workflow entrypoint.

    ``task_queue`` lives on WorkflowAPIRemoteTask (caller-side routing), not here.
    """

    task_config: ConfigT
    task_id: str = ""
    initial_state_dict: dict[str, Any] = {}
    parent_exec_id: str | None = None
    # Carries ambient SDK context across the workflow process boundary.
    observability_context: dict[str, JsonValue] = Field(default_factory=dict)
