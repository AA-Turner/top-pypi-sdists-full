"""Run: one execution of a piece of work, its lifecycle status and how it relates to a parent run."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import AliasChoices, BaseModel, Field

from ..compat import StrEnum
from .records import Record


class RunStatus(StrEnum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CRASHED = "crashed"
    CANCELED = "canceled"
    # 0106: never owned (no heartbeat ever), so nothing is known to have failed. Terminal like 'crashed';
    # old clients get 'crashed' (app/runs/service.py presentable_run_status). DESIGN.md (run.py).
    UNTRACKED = "untracked"


class RunType(StrEnum):
    """What a run is, as its creator declares it (0495). Training and evaluation are phases inside a run, not types.
    RL presentation (RL workspace, Rollouts, Compute timeline, Trials) follows `RL`; DESIGN.md (run.py)."""

    GENERAL = "general"
    #: Rollouts in an environment scored by a reward: an RL trainer's run, or a Harbor agent eval.
    RL = "rl"


class ParentRelation(StrEnum):
    FORK = "fork"
    RESUME = "resume"
    RETRY = "retry"
    BRANCH = "branch"


class RunCounts(BaseModel):
    """Child-row tallies nested under RunOut.counts (dashboard contract)."""

    spans: int
    metrics: int
    artifacts: int


class Run(Record):
    """A run as every surface reads it: the field set of the frozen ingest response.

    Detail-only reads (slug, project, writer, mirror state) are added by the
    projections that serve them, never here, so the ingest response cannot grow.
    """

    id: UUID
    customer_id: str
    # None = a project-direct run (0054-0058). Required-nullable on purpose (no default): it stays in the
    # schema's `required` set, so the frozen ingest response reads "may be null", never "may be absent".
    experiment_id: UUID | None
    name: str
    status: RunStatus
    source: str
    external_id: str | None = None
    parent_run_id: UUID | None = None
    parent_relation: ParentRelation | None = None
    group_id: UUID | None = None
    config: dict = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    #: Headline scalars, one value each, no step axis (`{"final_exact_match": 0.336}`). Renamed from
    #: `summary`, still accepted on input (and emitted by the wire shapes for one release).
    summary_metrics: dict = Field(
        default_factory=dict,
        validation_alias=AliasChoices("summary_metrics", "summary"),
    )
    metadata: dict = Field(default_factory=dict)
    created_at: datetime
    started_at: datetime | None = None
    ended_at: datetime | None = None
    labeled_point_budget: int | None = None
    # Labeled-point consumption (0060 counter): folded from actually-inserted rows.
    labeled_point_count: int = 0
    counts: RunCounts | None = None
