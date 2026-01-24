from enum import Enum

from pydantic import UUID4, BaseModel, Field, field_validator

from galileo_core.utils.name import ts_name

DEFAULT_PROJECT_NAME = "project"


class ProjectType(str, Enum):
    training_inference = "training_inference"
    prompt_evaluation = "prompt_evaluation"
    llm_monitor = "llm_monitor"
    protect = "protect"
    gen_ai = "gen_ai"


class CreateProjectRequest(BaseModel):
    name: str = Field(default=DEFAULT_PROJECT_NAME, validate_default=True)
    type: ProjectType

    @field_validator("name", mode="before")
    def generate_name(cls, value: str) -> str:
        if value == DEFAULT_PROJECT_NAME:
            value = ts_name(prefix=value)
        return value


class ProjectResponse(CreateProjectRequest):
    id: UUID4
