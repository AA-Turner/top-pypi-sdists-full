# SPDX-FileCopyrightText: 2026 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Skill request model — input to the dispatch_engine skill dispatch node."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ModelSkillRequest(BaseModel):
    """Input to the dispatch_engine skill dispatch node."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    skill_name: str = Field(
        ..., min_length=1, description="Human-readable skill identifier"
    )
    skill_path: str = Field(..., description="Path to the skill's SKILL.md file")
    args: dict[str, str] = Field(
        default_factory=dict,
        description="Argument pairs; empty/true → bare flag, else --flag value",
    )
    dry_run: bool = Field(
        default=False,
        description="If true, return a dry_run placeholder instead of live dispatch",
    )

    @field_validator("skill_name")
    @classmethod
    def _validate_skill_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("skill_name must not be blank or whitespace-only")
        return value

    @field_validator("skill_path")
    @classmethod
    def _validate_skill_path(cls, value: str) -> str:
        if not value:
            raise ValueError("skill_path must not be empty")
        if not value.endswith("SKILL.md"):
            raise ValueError(f"skill_path must end with 'SKILL.md', got: {value!r}")
        return value


__all__ = ["ModelSkillRequest"]
