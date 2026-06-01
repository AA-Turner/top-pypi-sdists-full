import re
import uuid
from datetime import timedelta
from enum import StrEnum
from typing import Any, Dict, List

from pydantic import BaseModel, Field, field_serializer, field_validator

from .handlers import QueryDefinition, SignalDefinition, UpdateDefinition
from .schedule import ScheduleDefinition

WORKFLOW_NAME_MAX_LENGTH = 128
WORKFLOW_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")


class WorkflowType(StrEnum):
    CODE = "code"


class WorkflowCodeDefinition(BaseModel):
    input_schema: Dict[str, Any] = Field(
        description="Input schema of the workflow's run method",
        json_schema_extra={"additionalProperties": True},
    )  # note change to Dict[str, Any] which is closer to real Json type.
    output_schema: Dict[str, Any] | None = Field(
        default=None,
        description="Output schema of the workflow's run method",
        json_schema_extra={"additionalProperties": True},
    )
    signals: List[SignalDefinition] = Field(default_factory=list, description="Signal handlers defined by the workflow")
    queries: List[QueryDefinition] = Field(default_factory=list, description="Query handlers defined by the workflow")
    updates: List[UpdateDefinition] = Field(default_factory=list, description="Update handlers defined by the workflow")
    enforce_determinism: bool = Field(
        default=False, description="Whether the workflow enforces deterministic execution"
    )
    execution_timeout: timedelta = Field(
        default=timedelta(hours=1),
        description="Maximum total execution time including retries and continue-as-new",
    )
    plugin_metadata: Dict[str, Any] | None = Field(
        default=None,
        description="Plugin-specific metadata (e.g. connector declarations)",
    )

    @field_serializer("execution_timeout")
    def serialize_execution_timeout(self, v: timedelta) -> float:
        # Serialize as seconds so model_dump() produces a JSON-serializable float.
        # Pydantic coerces the float back to timedelta on deserialization.
        return v.total_seconds()


class WorkflowSpec(WorkflowCodeDefinition):
    name: str = Field(description="Name of the workflow", max_length=WORKFLOW_NAME_MAX_LENGTH)
    display_name: str | None = Field(default=None, description="Display name of the workflow")
    description: str | None = Field(default=None, description="Description of the workflow")
    is_technical: bool = Field(default=False, description="Whether the workflow is technical (e.g. SDK-managed)")
    on_behalf_of: bool = Field(
        default=False,
        description="Whether the workflow must run associated to a user's identity",
    )
    schedules: List[ScheduleDefinition] = Field(default_factory=list, description="Schedules defined by the workflow")

    @field_validator("name")
    @classmethod
    def validate_workflow_name(cls, v: str) -> str:
        """Validate workflow name is URI-compliant.

        Rules:
        - Can only contain alphanumeric characters, hyphens (-), and underscores (_)
        - Maximum length of 128 characters (enforced via Field max_length)
        """
        if not v:
            raise ValueError("Workflow name cannot be empty")
        if not WORKFLOW_NAME_PATTERN.match(v):
            raise ValueError(
                "Workflow name is invalid. "
                "Names can only contain alphanumeric characters, hyphens (-), and underscores (_)."
            )
        return v


class WorkflowSpecWithTaskQueue(WorkflowSpec):
    task_queue: str = Field(description="Task queue name for the workflow")


class Workflow(BaseModel):
    id: uuid.UUID = Field(description="Unique identifier of the workflow")
    name: str = Field(description="Name of the workflow")
    display_name: str = Field(description="Display name of the workflow")
    type: WorkflowType = Field(description="Type of the workflow")
    description: str | None = Field(default=None, description="Description of the workflow")
    customer_id: uuid.UUID = Field(description="Customer ID of the workflow")
    workspace_id: uuid.UUID = Field(description="Workspace ID of the workflow")
    shared_namespace: str | None = Field(
        default=None, description="Reserved namespace for shared workflows (e.g., 'shared:my-shared-workflow')"
    )
    available_in_chat_assistant: bool = Field(
        default=False, description="Whether the workflow is available in chat assistant"
    )
    is_technical: bool = Field(default=False, description="Whether the workflow is technical (e.g. SDK-managed)")
    on_behalf_of: bool = Field(
        default=False,
        description="Whether the workflow must run associated to a user's identity",
    )
    archived: bool = Field(default=False, description="Whether the workflow is archived")


class WorkflowRegistration(BaseModel):
    id: uuid.UUID = Field(description="Unique identifier of the workflow registration")
    deployment_id: uuid.UUID | None = Field(default=None, description="Deployment ID this registration belongs to")
    task_queue: str | None = Field(
        default=None,
        deprecated=True,
        description="Deprecated. Use deployment_id instead. Will be removed in a future release.",
    )
    definition: WorkflowCodeDefinition
    workflow_id: uuid.UUID = Field(description="Workflow ID of the workflow")
    workflow: Workflow | None = Field(default=None, description="Workflow of the workflow registration")
    compatible_with_chat_assistant: bool = Field(
        default=False, description="Whether the workflow is compatible with chat assistant"
    )
