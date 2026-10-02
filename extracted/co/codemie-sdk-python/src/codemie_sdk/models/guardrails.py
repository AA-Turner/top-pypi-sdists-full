"""Models for guardrail assignments."""

from pydantic import BaseModel, ConfigDict, Field


class GuardrailAssignmentSetting(BaseModel):
    """Model for guardrail assignment settings."""

    model_config = ConfigDict(extra="ignore")

    mode: str = Field(..., description="Assignment mode (e.g., 'all', 'specific')")
    source: str = Field(..., description="Source type (e.g., 'input', 'output')")


class GuardrailAssignmentEntity(BaseModel):
    """Model for guardrail assignment to specific entities."""

    model_config = ConfigDict(extra="ignore")

    settings: list[GuardrailAssignmentSetting] = Field(
        default_factory=list, description="List of assignment settings"
    )
    items: list[str] = Field(
        default_factory=list, description="List of specific entity IDs"
    )


class GuardrailAssignmentRequest(BaseModel):
    """Request model for assigning guardrails to entities."""

    model_config = ConfigDict(extra="ignore")

    project: GuardrailAssignmentEntity = Field(
        default_factory=lambda: GuardrailAssignmentEntity(settings=[], items=[]),
        description="Project-level assignments",
    )
    assistants: GuardrailAssignmentEntity = Field(
        default_factory=lambda: GuardrailAssignmentEntity(settings=[], items=[]),
        description="Assistant-level assignments",
    )
    workflows: GuardrailAssignmentEntity = Field(
        default_factory=lambda: GuardrailAssignmentEntity(settings=[], items=[]),
        description="Workflow-level assignments",
    )
    datasources: GuardrailAssignmentEntity = Field(
        default_factory=lambda: GuardrailAssignmentEntity(settings=[], items=[]),
        description="Datasource-level assignments",
    )


class GuardrailAssignmentResponse(BaseModel):
    """Response model for guardrail assignment."""

    model_config = ConfigDict(extra="ignore")

    success: int = Field(..., description="Count of successful assignments")
    failed: int = Field(..., description="Count of failed assignments")
    errors: list[str] = Field(
        default_factory=list, description="List of error messages"
    )
