"""Pydantic response models for the Synkro enterprise API."""

from datetime import datetime

from pydantic import BaseModel, Field


class Project(BaseModel):
    id: str
    slug: str
    name: str
    provider: str | None = None
    is_active: bool = True
    gateway_url: str | None = None
    created_at: datetime | None = None


class ProjectStatus(BaseModel):
    project_id: str
    slug: str
    name: str
    is_active: bool
    has_api_key: bool
    has_policy: bool
    rule_count: int
    is_ready: bool
    violations_total: int
    violations_24h: int


class Policy(BaseModel):
    id: str
    name: str
    policy_text: str
    rules: list[dict] = Field(default_factory=list)
    rule_count: int = 0
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


class PolicyCreateResult(BaseModel):
    ok: bool
    policy_id: str
    status: str = "ready"
    event_id: str | None = None
    rules: list[dict] = Field(default_factory=list)
    rule_count: int = 0
    model: str | None = None
    timing_ms: int | None = None


class LangSmithConnection(BaseModel):
    connected: bool
    id: str | None = None
    base_url: str | None = None
    status: str | None = None
    project_count: int = 0
    created_at: datetime | None = None


class DatasetCreateResult(BaseModel):
    dataset_id: str
    example_count: int
