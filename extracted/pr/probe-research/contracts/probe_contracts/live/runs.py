"""The `data` of the `run.*` notices (rl-next W54). A notice says what changed; the run's routes hold the rest."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from .samples import MAX_NOTICE_TEXT

#: Metric keys one `run.metrics` notice names at most (`is_cut` says there were more).
MAX_METRIC_KEYS = 32
#: The one interval `run.metrics` coalesces over: at most one notice per run per this many seconds per apply pod.
METRICS_EVERY_SECONDS = 5.0


class RunStatusData(BaseModel):
    """`run.status`: the run's status changed (running, completed, failed, crashed, canceled, untracked)."""

    status: str
    #: Why, when the writer said (`writer_gone`, `stale`, `never_started`, a reopen's `reopened`).
    reason: str | None = Field(default=None, max_length=MAX_NOTICE_TEXT)


class RunMetricsData(BaseModel):
    """`run.metrics`: new points landed, up to `last_step`. Coalesced: read the points from the metric routes."""

    keys: list[str] = Field(default_factory=list, max_length=MAX_METRIC_KEYS)
    last_step: int | None = None
    #: More keys landed than `keys` names.
    is_cut: bool = False


class RunAlertData(BaseModel):
    """`run.alert`: an alert the run's agents get (`run_alerts.kind`: crashed, still_running, flagged_then_stopped,
    token_expiring, samples_hung, ...), with the finding it leads with when it has one."""

    kind: str
    #: The leading finding's kind (`loss_spike`), when the alert is about findings.
    key: str | None = None
    value: float | None = None
    text: str = Field(default="", max_length=MAX_NOTICE_TEXT)


class RunFindingData(BaseModel):
    """`run.finding`: a detector found something new on the run (`progress_stalled`, `writer_lost`, `nan_inf`, ...)."""

    kind: str
    #: The series it is about (`loss`), when one.
    key: str | None = None
    #: The finding's score.
    value: float | None = None
    severity: str
    step: int | None = None


class RunCheckpointData(BaseModel):
    """`run.checkpoint`: a checkpoint save was recorded on the run."""

    name: str
    step: int | None = None
    artifact_id: UUID


class RunArtifactData(BaseModel):
    """`run.artifact`: a file (not a checkpoint) was recorded on the run."""

    name: str
    kind: str
    artifact_id: UUID
