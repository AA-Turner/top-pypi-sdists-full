"""Skill models for SDK agents."""

from pydantic import BaseModel, Field, JsonValue, field_validator


class SkillDefinition(BaseModel):
    """Reusable instruction set discoverable by an agent and loaded on demand."""

    name: str = Field(
        min_length=1,
        max_length=64,
        pattern=r"^[a-z0-9]+(-[a-z0-9]+)*$",
        description=(
            "Skill identifier. Lowercase letters, numbers, and hyphens only."
            " Must not start or end with a hyphen."
        ),
    )
    description: str = Field(
        min_length=1,
        max_length=1024,
        description="What this skill does and when to use it.",
    )
    content: str = Field(description="The skill body content.")
    license: str | None = Field(
        default=None,
        description="License name or reference to a bundled license file.",
    )
    compatibility: str | None = Field(
        default=None,
        max_length=500,
        description="Environment requirements for the skill.",
    )
    metadata: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="Additional metadata for SDK consumers.",
    )
    allowed_tools: list[str] = Field(
        default_factory=list,
        validation_alias="allowed-tools",
        description="Pre-approved tools the skill may use.",
    )

    model_config = {
        "extra": "forbid",
        "validate_by_name": True,
        "validate_by_alias": True,
    }

    @field_validator("allowed_tools", mode="before")
    @classmethod
    def _parse_allowed_tools(cls, value: str | list[str] | None) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return value.split()
        return list(value)
