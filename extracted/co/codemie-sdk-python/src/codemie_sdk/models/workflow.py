"""Workflow models."""

from datetime import datetime
from enum import StrEnum, Enum

from pydantic import BaseModel, ConfigDict, Field

from codemie_sdk.models.common import User, TokensUsage


class WorkflowMode(StrEnum):
    """Available workflow modes."""

    SEQUENTIAL = "Sequential"
    AUTONOMOUS = "Autonomous"


class WorkflowCreateRequest(BaseModel):
    """Request model for workflow creation."""

    model_config = ConfigDict(populate_by_name=True)

    project: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    description: str | None = None
    yaml_config: str = Field(..., min_length=1)
    mode: WorkflowMode = WorkflowMode.SEQUENTIAL
    shared: bool = False
    icon_url: str | None = None


class WorkflowUpdateRequest(BaseModel):
    """Request model for workflow updates."""

    model_config = ConfigDict(populate_by_name=True)
    project: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    yaml_config: str = Field(..., min_length=1)
    mode: WorkflowMode | None = None
    shared: bool | None = None
    icon_url: str | None = None


class Workflow(BaseModel):
    """Workflow template model."""

    def __getitem__(self, key):
        return getattr(self, key)

    model_config = ConfigDict(populate_by_name=True)

    id: str | None = None
    project: str
    name: str
    description: str | None = None
    yaml_config: str | None = None
    mode: WorkflowMode = WorkflowMode.SEQUENTIAL
    shared: bool = False
    icon_url: str | None = None
    created_date: datetime | None = Field(None, alias="date")
    update_date: datetime | None = Field(None)
    created_by: User | None = None
    display_name: str | None = None
    required_variables: list[str] = Field(default_factory=list)


class ExecutionStatus(str, Enum):
    IN_PROGRESS = "In Progress"
    NOT_STARTED = "Not Started"
    INTERRUPTED = "Interrupted"
    FAILED = "Failed"
    SUCCEEDED = "Succeeded"
    ABORTED = "Aborted"


class WorkflowExecution(BaseModel):
    """Model representing a workflow execution."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    execution_id: str
    workflow_id: str
    status: ExecutionStatus = Field(alias="overall_status")
    created_date: datetime = Field(alias="date")
    prompt: str
    updated_date: datetime | None = Field(alias="update_date")
    created_by: User
    conversation_id: str | None = None
    tokens_usage: TokensUsage | None = None


class WorkflowEvaluationRequest(BaseModel):
    """Model for workflow evaluation request."""

    model_config = ConfigDict(extra="ignore")

    dataset_id: str = Field(description="ID of the dataset to use for evaluation")
    experiment_name: str = Field(description="Name of the evaluation experiment")
    max_concurrency: int = Field(
        default=1, ge=1, le=5, description="Maximum number of concurrent evaluations"
    )


class WorkflowGeneratorRequest(BaseModel):
    """Request model for generating a workflow from a natural language description.

    Maps to the backend's ``WorkflowGeneratorRequest``
    (``src/codemie/rest_api/models/workflow_generator.py``), where the wire field
    for the natural language description is ``text`` (not ``nl_query`` — that name
    is only used internally as the service-layer parameter).
    """

    text: str = Field(..., min_length=1)
    llm_model: str | None = None
    persist: bool = False
    guardrail_ids: list[str] | None = None


class WorkflowGeneratedState(BaseModel):
    """A single generated state (node) inside a generated workflow config."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    assistant_id: str | None = None
    tool_id: str | None = None
    custom_node_id: str | None = None
    task: str | None = None
    next: dict | None = None


class WorkflowGeneratedAssistant(BaseModel):
    """A single generated assistant reference inside a generated workflow config."""

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    assistant_id: str | None = None


class WorkflowGeneratorConfig(BaseModel):
    """The generated workflow configuration returned by the generator.

    Mirrors the backend's ``CreateWorkflowRequest`` shape
    (``src/codemie/core/workflow_models/workflow_models.py``). Uses
    ``extra="allow"`` since the backend model carries additional fields (e.g.
    ``guardrail_assignments``) that are not required for test assertions.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    name: str
    description: str | None = None
    project: str | None = None
    mode: WorkflowMode = WorkflowMode.SEQUENTIAL
    yaml_config: str | None = None
    shared: bool = True
    assistants: list[WorkflowGeneratedAssistant] = Field(default_factory=list)
    tools: list[dict] = Field(default_factory=list)
    states: list[WorkflowGeneratedState] = Field(default_factory=list)
    supervisor_prompt: str | None = ""
    meta_config: str | None = None


class WorkflowGeneratorResponse(BaseModel):
    """Response model for ``POST /v1/workflows/generate``."""

    model_config = ConfigDict(populate_by_name=True)

    workflow_config: WorkflowGeneratorConfig
    workflow_id: str | None = None
