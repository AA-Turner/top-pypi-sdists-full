from enum import Enum
from typing import Optional, Union

from pydantic import UUID4, BaseModel, Field, ValidationInfo, field_validator

from galileo_core.schemas.protect.ruleset import RulesetsMixin


class StageType(str, Enum):
    local = "local"
    central = "central"


class Stage(BaseModel):
    name: str = Field(description="Name of the stage. Must be unique within the project.")
    project_id: UUID4 = Field(description="ID of the project to which this stage belongs.")
    description: Optional[str] = Field(
        description="Optional human-readable description of the goals of this guardrail.",
        default=None,
    )
    type: StageType = Field(description="Type of the stage.", default=StageType.local)
    paused: bool = Field(
        description="Whether the action is enabled. If False, the action will not be applied.",
        default=False,
    )


class StageWithRulesets(Stage, RulesetsMixin):
    @field_validator("type", mode="before")
    def validate_type(cls, value: Union[StageType, str], info: ValidationInfo) -> StageType:
        stage_type = StageType(value)
        rulesets = info.data.get("prioritized_rulesets") or info.data.get("rulesets") or []
        if value == StageType.local and len(rulesets) > 0:
            raise ValueError("Local stages cannot include ruleset definitions during creation.")
        return stage_type


class CreateStage(Stage):
    created_by: UUID4


class StageDB(CreateStage):
    id: UUID4
    version: Union[int, None] = None
