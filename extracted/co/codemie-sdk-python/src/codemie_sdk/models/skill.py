"""Models for skill-related data structures."""

from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .common import User


class SkillVisibility(str, Enum):
    """Skill visibility options."""

    PROJECT = "project"
    PRIVATE = "private"
    PUBLIC = "public"


class SkillCategory(BaseModel):
    """Skill category model."""

    model_config = ConfigDict(extra="ignore")

    value: str  # Category value (e.g., "development", "testing")
    label: str  # Human-readable label (e.g., "Development", "Testing")
    description: str | None = None


class SkillBase(BaseModel):
    """Base skill model."""

    model_config = ConfigDict(extra="ignore")

    id: str
    name: str
    description: str
    project: str
    display_name: str | None = None
    visibility: SkillVisibility
    categories: list[str] = Field(default_factory=list)
    created_date: datetime = Field(alias="createdDate")
    enabled_builtin_subagents: list[str] = Field(default_factory=list)


class SkillListResponse(SkillBase):
    """Skill list item response."""

    created_by: User | None = Field(None, alias="created_by")
    updated_date: datetime | None = Field(None, alias="updatedDate")
    is_attached: bool | None = Field(None, alias="is_attached")
    reactions_count: int | None = Field(None, alias="reactionsCount")
    assistants_count: int | None = Field(None, alias="assistantsCount")


class SkillDetailResponse(SkillListResponse):
    """Full skill details response."""

    content: str
    slug: str | None = None
    icon_url: str | None = Field(None, alias="iconUrl")


class SkillCreateRequest(BaseModel):
    """Request to create a skill."""

    name: str
    description: str
    content: str
    project: str
    visibility: SkillVisibility | None = SkillVisibility.PROJECT
    categories: list[str] | None = Field(default_factory=list)
    enabled_builtin_subagents: list[str] | None = None


class SkillUpdateRequest(BaseModel):
    """Request to update a skill."""

    name: str | None = None
    description: str | None = None
    content: str | None = None
    project: str | None = None
    visibility: SkillVisibility | None = None
    categories: list[str] | None = None
    enabled_builtin_subagents: list[str] | None = None


class SkillImportRequest(BaseModel):
    """Request to import a skill from .md file."""

    file_content: str
    filename: str
    project: str
    visibility: SkillVisibility | None = SkillVisibility.PROJECT


class SkillAttachRequest(BaseModel):
    """Request to attach skill to assistant."""

    skill_id: str


class SkillBulkAttachRequest(BaseModel):
    """Request to bulk attach skill to assistants."""

    assistant_ids: list[str]


class SkillListPaginatedResponse(BaseModel):
    """Paginated list of skills."""

    model_config = ConfigDict(extra="ignore")

    skills: list[SkillListResponse]
    page: int
    per_page: int = Field(alias="perPage")
    total: int
    pages: int


class SkillReactionResponse(BaseModel):
    """Skill reaction response."""

    model_config = ConfigDict(extra="ignore")

    resource_id: str = Field(alias="resourceId")
    reaction: str
    reaction_at: str = Field(alias="reactionAt")
    resource_type: str | None = Field(None, alias="resourceType")


class SkillPagination(BaseModel):
    """Shared pagination envelope for skills statistics endpoints."""

    model_config = ConfigDict(extra="ignore")

    page: int
    per_page: int
    total: int
    pages: int


class SkillEventRequest(BaseModel):
    """Request body for POST /v1/skills/events."""

    session_id: str
    command: Literal["add", "update", "remove", "list", "find"]
    status: Literal["started", "completed", "failed"]
    scope: Literal["global", "project", "unknown"] | None = None
    error_code: str | None = None
    agent_selection_mode: (
        Literal["explicit", "auto_detected", "prompted", "upstream"] | None
    ) = None
    target_agents: list[str] | None = None
    source: str | None = None
    skill_name: str | None = None
    skill_slug: str | None = None
    skill_id: str | None = None
    agent: str = "codemie-skills"
    agent_version: str | None = None
    repository: str | None = None
    branch: str | None = None
    project: str | None = None
    attributes: dict[str, Any] | None = None


class SkillEventItem(BaseModel):
    """Single row from the raw event log."""

    model_config = ConfigDict(extra="ignore")

    skill_slug: str | None = None
    source: str | None = None
    target_agents: list[str] = Field(default_factory=list)
    date: datetime
    command: str
    user_id: str


class SkillEventsPaginatedResponse(BaseModel):
    """Paginated response from GET /v1/skills/events."""

    model_config = ConfigDict(extra="ignore")

    data: list[SkillEventItem]
    pagination: SkillPagination


class SkillStatsItem(BaseModel):
    """Per-skill aggregated stats item."""

    model_config = ConfigDict(extra="ignore")

    skill_slug: str | None = None
    installs: int
    removals: int
    by_agent: dict[str, int] = Field(default_factory=dict)


class SkillStatsPaginatedResponse(BaseModel):
    """Paginated response from GET /v1/skills/events/stats."""

    model_config = ConfigDict(extra="ignore")

    data: list[SkillStatsItem]
    pagination: SkillPagination


class SingleSkillStatsResponse(BaseModel):
    """Response from GET /v1/skills/events/{slug}/stats."""

    model_config = ConfigDict(extra="ignore")

    installs: int
    removals: int
    by_agent: dict[str, int] = Field(default_factory=dict)


class SkillConfigResponse(BaseModel):
    """Response model for GET /v1/skills/config."""

    model_config = ConfigDict(extra="ignore")

    max_content_length: int
    min_content_length: int
