"""
Pydantic request and response schemas for the scheduler HTTP API.

These mirror the package's internal models (``matrx_scheduler.models``)
but with API-friendly defaults and validation. They are decoupled from
the internal models so wire shapes can evolve independently from the
storage shape.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from matrx_scheduler.models import RunStatus, TriggerType


# ── Task ─────────────────────────────────────────────────────────────────


class AgentTaskCreate(BaseModel):
    """Child sch_agent_task row payload (used for kind=agent/tool)."""

    model_config = ConfigDict(extra="ignore")

    agent_id: str | None = None
    mandate_key: str | None = None
    prompt: str = ""
    variables: dict[str, Any] = Field(default_factory=dict)
    persistent_conversation_id: str | None = None
    auth_mode: Literal["ask", "auto"] = "ask"
    max_runtime_seconds: int = Field(default=600, ge=1, le=86400)
    max_concurrent: int = Field(default=1, ge=1, le=100)


class TriggerCreate(BaseModel):
    """Child sch_trigger row payload."""

    model_config = ConfigDict(extra="ignore")

    type: TriggerType
    config: dict[str, Any] = Field(default_factory=dict)
    enabled: bool = True


class TaskCreateRequest(BaseModel):
    """Create a new sch_task (plus optional agent_task and trigger)."""

    model_config = ConfigDict(extra="ignore")

    kind: str = Field(..., description="'agent', 'tool', or 'ping'")
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    queue: str = Field(default="default", max_length=50)
    surfaces: list[str] = Field(default_factory=lambda: ["any"])
    enabled: bool = True
    expires_at: datetime | None = None
    tags: list[str] = Field(default_factory=list)
    taxonomy_node_id: str | None = Field(
        default=None,
        description=(
            "Canonical platform.taxonomy_node identity. Required for kind='tool' so "
            "system work is attached to a Domain, Feature, or Sub-feature."
        ),
    )
    agent_task: AgentTaskCreate | None = None
    trigger: TriggerCreate | None = None
    force: bool = Field(
        default=False,
        description=(
            "Create even when an identical live schedule already exists. Default "
            "false: an identical create returns the EXISTING schedule instead of "
            "inserting a twin (see scheduler.duplicate_guard), so a double-click "
            "or a retried MCP call cannot produce two always-on schedules doing "
            "one job. Set true only when a second schedule is genuinely wanted."
        ),
    )


class TaskPatchRequest(BaseModel):
    """Update a subset of sch_task fields."""

    model_config = ConfigDict(extra="ignore")

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    queue: str | None = Field(default=None, max_length=50)
    surfaces: list[str] | None = None
    enabled: bool | None = None
    expires_at: datetime | None = None
    tags: list[str] | None = None


class TaskResponse(BaseModel):
    """Single sch_task row (plain, without children)."""

    model_config = ConfigDict(extra="ignore")

    id: str
    user_id: str
    kind: str
    title: str
    description: str | None = None
    queue: str
    surfaces: list[str]
    enabled: bool
    expires_at: datetime | None = None
    tags: list[str]
    taxonomy_node_id: str | None = None
    next_due_at: datetime | None = None
    last_run_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class AgentTaskResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    agent_id: str | None = None
    mandate_key: str | None = None
    prompt: str
    variables: dict[str, Any] = Field(default_factory=dict)
    persistent_conversation_id: str | None = None
    auth_mode: Literal["ask", "auto"] = "ask"
    max_runtime_seconds: int
    max_concurrent: int


class TriggerResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    task_id: str
    user_id: str
    type: TriggerType
    config: dict[str, Any] = Field(default_factory=dict)
    enabled: bool
    next_due_at: datetime | None = None
    last_fired_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class RunResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    task_id: str
    trigger_id: str | None = None
    user_id: str
    status: RunStatus
    surface: str | None = None
    queue: str | None = None
    output_ref: dict[str, Any] | None = None
    due_at: datetime
    claimed_at: datetime | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    result_summary: str | None = None
    error_message: str | None = None
    result_metadata: dict[str, Any] | None = None
    created_at: datetime | None = None


class TaskDetailResponse(BaseModel):
    """Task hydrated with agent_task, triggers, and recent runs."""

    model_config = ConfigDict(extra="ignore")

    task: TaskResponse
    agent_task: AgentTaskResponse | None = None
    triggers: list[TriggerResponse] = Field(default_factory=list)
    recent_runs: list[RunResponse] = Field(default_factory=list)
    deduplicated: bool = Field(
        default=False,
        description=(
            "True when a create returned an EXISTING identical schedule instead "
            "of inserting a new one. The response is a success (HTTP 200, not "
            "201) and `task` is the schedule that was already there — a client "
            "must not tell the user it created something new."
        ),
    )


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int


class DuplicateScheduleMember(BaseModel):
    """One schedule inside a duplicate group."""

    model_config = ConfigDict(extra="ignore")

    id: str
    title: str | None = None
    enabled: bool = True
    created_at: datetime | None = None
    is_original: bool = Field(
        default=False,
        description="True for the OLDEST schedule in the group -- the one that is not redundant.",
    )


class DuplicateScheduleGroup(BaseModel):
    """A set of the caller's schedules that all do the same work on the same trigger."""

    model_config = ConfigDict(extra="ignore")

    fingerprint: str
    members: list[DuplicateScheduleMember]
    redundant_count: int = Field(
        description="How many schedules in this group pay for work already being done."
    )
    enabled_count: int = Field(
        description=(
            "How many are still enabled. A group whose extras are all paused is "
            "resolved -- it costs nothing -- and should not be shown as a live problem."
        )
    )


class DuplicateScheduleResponse(BaseModel):
    groups: list[DuplicateScheduleGroup] = Field(default_factory=list)


# ── Triggers (standalone CRUD) ────────────────────────────────────────────


class TriggerCreateRequest(BaseModel):
    """Create a sch_trigger row attached to an existing task."""

    model_config = ConfigDict(extra="ignore")

    task_id: str
    type: TriggerType
    config: dict[str, Any] = Field(default_factory=dict)
    enabled: bool = True


class TriggerPatchRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    type: TriggerType | None = None
    config: dict[str, Any] | None = None
    enabled: bool | None = None


class TriggerListResponse(BaseModel):
    triggers: list[TriggerResponse]


# ── Runs ─────────────────────────────────────────────────────────────────


class RunListResponse(BaseModel):
    runs: list[RunResponse]


class RunNowResponse(BaseModel):
    run_id: str


# ── Cron + next-due ──────────────────────────────────────────────────────


class ValidateCronRequest(BaseModel):
    expression: str = Field(..., min_length=1, max_length=200)
    tz: str = Field(default="UTC", min_length=1, max_length=64)
    next_n: int = Field(default=5, ge=1, le=50)


class ValidateCronResponse(BaseModel):
    valid: bool
    error: str | None = None
    next_fires_utc: list[str] = Field(default_factory=list)


class PreviewFiresRequest(BaseModel):
    """Preview next-fire times for any trigger config, not just cron."""

    trigger_type: TriggerType
    config: dict[str, Any] = Field(default_factory=dict)
    n: int = Field(default=5, ge=1, le=50)


class PreviewFiresResponse(BaseModel):
    next_fires_utc: list[str] = Field(default_factory=list)
    event_driven: bool = False


class ComputeNextDueRequest(BaseModel):
    trigger_type: TriggerType
    config: dict[str, Any] = Field(default_factory=dict)


class ComputeNextDueResponse(BaseModel):
    next_due_at: str | None = None
    event_driven: bool


# ── Scanner status ──────────────────────────────────────────────────────


class ScannerStatusResponse(BaseModel):
    running: bool
    started_at: str | None = None
    last_tick_at: str | None = None
    last_tick_duration_ms: int | None = None
    last_tick_claimed: int = 0
    last_tick_expired_sweeps: int = 0
    last_tick_manual_claimed: int = 0
    total_runs_dispatched: int = 0
    in_flight_count: int = 0
    consecutive_errors: int = 0
    error_message: str | None = None


# ── Generic ─────────────────────────────────────────────────────────────


class DeletedResponse(BaseModel):
    deleted: bool
    soft: bool = True
