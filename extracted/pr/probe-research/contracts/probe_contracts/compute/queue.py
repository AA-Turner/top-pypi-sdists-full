"""Queue report: the jobs a node daemon sees in its cluster's scheduler queue (D23 Pending)."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..compat import StrEnum
from .compute import ENV_ALLOWLIST

#: A queue report names at most this many jobs; only jobs carrying an allowlisted run key are sent.
MAX_QUEUED_JOBS = 1_000
#: How often a daemon reads its queue and sends what it saw.
QUEUE_INTERVAL_SECONDS = 30


class SchedulerKind(StrEnum):
    """The scheduler whose queue a report reads. Each has one variant in `app/compute/queues/schedulers/`."""

    SLURM = "slurm"
    KUBERNETES = "kubernetes"
    SKYPILOT = "skypilot"


class QueuedJob(BaseModel):
    """One job as its scheduler lists it. `state` is the scheduler's own word (`PENDING`, `Pending`,
    `CANCELLED`); the server's variant for that scheduler reads it, so a new word needs no daemon release."""

    model_config = ConfigDict(extra="forbid")

    job_id: str = Field(min_length=1, max_length=128)
    state: str = Field(min_length=1, max_length=64)
    #: Why it waits, as the scheduler says (`Resources`, `Priority`, `Unschedulable`).
    reason: str | None = Field(default=None, max_length=256)
    submitted_at: datetime | None = None
    #: The job's launch environment, allowlisted keys only: `PROBE_RUN_ID` names its run.
    env: dict[str, str] = Field(default_factory=dict)

    @field_validator("env")
    @classmethod
    def check_env_allowlisted(cls, value: dict[str, str]) -> dict[str, str]:
        unknown = sorted(set(value) - ENV_ALLOWLIST)
        if unknown:
            raise ValueError(f"environment keys outside the allowlist: {unknown}")
        return value


class QueueReportIn(BaseModel):
    """`POST /v1/nodes/{node_id}/queue`, by the node credential: every job of one scheduler that names a
    run, waiting or just ended. A job absent from a report is not evidence of anything."""

    model_config = ConfigDict(extra="forbid")

    scheduler: SchedulerKind
    sent_at: datetime
    jobs: list[QueuedJob] = Field(default_factory=list, max_length=MAX_QUEUED_JOBS)


class QueueReportAck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    #: Jobs whose run this team has (the rest named no run, or one the server does not know).
    linked: int
    #: Runs this report made `pending`, and runs it ended `canceled`.
    pending: int
    canceled: int
    #: Jobs the server could not read (an over-long id, an env key outside the allowlist) and left out; the
    #: rest of the report still counts.
    skipped: int = 0
