"""Pydantic shapes for the skills system.

Hard rules (SK-R*):
    * SK-R1 — ``SkillConfig`` carries ONLY visibility tiers + disabled. No
      priority, ordering, metadata, source-app. If you find yourself adding
      a field here, reread the plan.
    * SK-R10 — every id is a UUID. The string-form ``skill_id`` business
      key is NOT acceptable in ``SkillConfig`` — it's a UUID or it's wrong.
"""

from __future__ import annotations

from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SkillTier(str, Enum):
    """Per-agent visibility tier for a skill at request time."""

    INCLUDED = "included"  # full body in system prompt
    LISTED = "listed"  # name + description in system prompt
    DEFAULT = "default"  # not announced; searchable
    FORBIDDEN = "forbidden"  # hidden everywhere


# ---------------------------------------------------------------------------
# Wire-shape models
# ---------------------------------------------------------------------------


class SkillHint(BaseModel):
    """Minimal description the agent sees in ``skill_list`` / ``skill_search``."""

    model_config = ConfigDict(extra="forbid")

    id: UUID
    skill_id: str  # human-readable business key from skill.definition.skill_id
    label: str
    description: str
    skill_type: str
    category_path: list[str] = Field(default_factory=list)
    has_resources: bool = False
    has_allowed_tools: bool = False
    tier: SkillTier = SkillTier.DEFAULT


class SkillBody(BaseModel):
    """Full skill payload returned by ``skill_get``."""

    model_config = ConfigDict(extra="forbid")

    id: UUID
    skill_id: str
    label: str
    description: str
    skill_type: str
    body: str
    category_path: list[str] = Field(default_factory=list)
    allowed_tools: list[UUID] = Field(default_factory=list)
    trigger_patterns: list[str] = Field(default_factory=list)
    disable_auto_invocation: bool = False
    # DB truth: skill.definition.version is an INTEGER. This was `str | None`,
    # which made every skill_get ValidationError-out in resolve_skills_for_agent
    # — silently stripping ALL skills from every agent run that included one.
    version: int | None = None


class SkillConfig(BaseModel):
    """Per-agent visibility tiering. Loaded from ``agx_agent.skill_config``."""

    model_config = ConfigDict(extra="forbid")

    included: list[UUID] = Field(default_factory=list)
    listed: list[UUID] = Field(default_factory=list)
    forbidden: list[UUID] = Field(default_factory=list)
    disabled: bool = False

    @field_validator("included", "listed", "forbidden", mode="before")
    @classmethod
    def _coerce_uuid_list(cls, v: Any) -> Any:
        if v is None:
            return []
        if isinstance(v, list):
            # Tolerate string-form UUIDs coming from JSONB; reject anything else.
            out: list[UUID] = []
            for item in v:
                if isinstance(item, UUID):
                    out.append(item)
                elif isinstance(item, str):
                    out.append(UUID(item))
                else:
                    raise ValueError(
                        f"skill_config list items must be UUIDs or UUID strings; got {type(item).__name__}"
                    )
            return out
        raise ValueError("skill_config tier fields must be lists of UUIDs")

    def tier_for(self, skill_uuid: UUID) -> SkillTier:
        if skill_uuid in self.forbidden:
            return SkillTier.FORBIDDEN
        if skill_uuid in self.included:
            return SkillTier.INCLUDED
        if skill_uuid in self.listed:
            return SkillTier.LISTED
        return SkillTier.DEFAULT

    def is_forbidden(self, skill_uuid: UUID) -> bool:
        return skill_uuid in self.forbidden

    @classmethod
    def from_jsonb(cls, value: Any) -> SkillConfig:
        """Defensive parse of the ``agx_agent.skill_config`` JSONB blob."""
        if value is None or value == {} or value == "":
            return cls()
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            return cls.model_validate(value)
        raise TypeError(f"skill_config must be a dict or None; got {type(value).__name__}")


# ---------------------------------------------------------------------------
# Resolver output
# ---------------------------------------------------------------------------


class SkillPreamble(BaseModel):
    """Structured shape the preamble renderer consumes."""

    model_config = ConfigDict(extra="forbid")

    overview_lines: list[str] = Field(default_factory=list)
    listed_skills: list[SkillHint] = Field(default_factory=list)
    included_skills: list[SkillBody] = Field(default_factory=list)
    total_active_count: int = 0


class ResolvedSkills(BaseModel):
    """Full request-time resolution: preamble + tools to inject."""

    model_config = ConfigDict(extra="forbid")

    preamble: SkillPreamble
    tools_to_inject: list[UUID] = Field(default_factory=list)
    config: SkillConfig
    disabled: bool = False
