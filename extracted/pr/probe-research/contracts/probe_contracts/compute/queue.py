"""Queue report: the jobs a node daemon sees in its cluster's scheduler queue (D23 Pending)."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ..compat import StrEnum
from .compute import ENV_ALLOWLIST
from .enrollment import ClusterEvidence

#: A queue report names at most this many jobs; only jobs carrying an allowlisted run key are sent.
MAX_QUEUED_JOBS = 1_000
#: How often a daemon reads its queue and sends what it saw.
QUEUE_INTERVAL_SECONDS = 30
#: A machine list (T7) names at most this many machines, this many per page: a page of the longest allowed
#: fields stays under MAX_REPORT_BYTES. A daemon resends its scheduler's list this often.
MAX_LISTED_MACHINES = 10_000
MACHINES_PER_PAGE = 100
MAX_MACHINE_PAGES = MAX_LISTED_MACHINES // MACHINES_PER_PAGE
MACHINE_LIST_INTERVAL_SECONDS = 600


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


class ListedMachine(BaseModel):
    """One machine as its scheduler lists it (a Kubernetes node, a Slurm node): a machine Probe expects
    before probe-node reports from it. Spot and burst machines are never listed."""

    model_config = ConfigDict(extra="forbid")

    #: The scheduler's name for it (the Kubernetes node name, the Slurm NodeName).
    name: str = Field(min_length=1, max_length=253)
    #: The provider's instance id when the scheduler knows it (the last part of a Kubernetes providerID).
    instance_id: str | None = Field(default=None, max_length=128)
    gpu_count: int | None = Field(default=None, ge=0, le=1024)
    gpu_model: str | None = Field(default=None, max_length=128)


class MachineList(BaseModel):
    """One page of a scheduler's whole machine list (T7). The pages of one listing share `listing_id`; once
    every page has landed, the cluster's machines the listing did not name are marked gone (never deleted)."""

    model_config = ConfigDict(extra="forbid")

    listing_id: str = Field(min_length=1, max_length=64)
    page: int = Field(ge=0)
    page_count: int = Field(ge=1, le=MAX_MACHINE_PAGES)
    #: Machines in the whole listing, every page together.
    total: int = Field(ge=0, le=MAX_LISTED_MACHINES)
    machines: list[ListedMachine] = Field(default_factory=list, max_length=MACHINES_PER_PAGE)
    #: Whose machines these are. None on a queue report: the reporting node's own cluster. `probe compute
    #: connect` always names it; SkyPilot's reader (T5) names each SkyPilot cluster it started here.
    cluster: ClusterEvidence | None = None

    @model_validator(mode="after")
    def check_page_in_range(self) -> MachineList:
        if self.page >= self.page_count:
            raise ValueError("page must be below page_count")
        return self


class QueueReportIn(BaseModel):
    """`POST /v1/nodes/{node_id}/queue`, by the node credential: every job of one scheduler that names a
    run, waiting or just ended. A job absent from a report is not evidence of anything. A daemon that can
    list its scheduler's machines sends them as `machine_list` pages (with no jobs) every
    MACHINE_LIST_INTERVAL_SECONDS."""

    model_config = ConfigDict(extra="forbid")

    scheduler: SchedulerKind
    sent_at: datetime
    jobs: list[QueuedJob] = Field(default_factory=list, max_length=MAX_QUEUED_JOBS)
    machine_list: MachineList | None = None


class SubmittedJobIn(BaseModel):
    """`POST /v1/runs/{run_id}/queue-jobs`, by a SkyPilot API server's `runs:submit` key (its plugin's
    `managed_job_submitted` hook, T4): the queue job id a run's job was given, recorded waiting."""

    model_config = ConfigDict(extra="forbid")

    scheduler: SchedulerKind
    job_id: str = Field(min_length=1, max_length=128)


class QueueReportAck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    #: Jobs whose run this team has (the rest named no run, or one the server does not know).
    linked: int
    #: Runs this report made `pending`, and runs it ended `canceled`.
    pending: int
    canceled: int
    #: Runs it ended `failed`: their job failed in the queue before the run attached (A17, T5).
    failed: int = 0
    #: Jobs the server could not read (an over-long id, an env key outside the allowlist) and left out; the
    #: rest of the report still counts.
    skipped: int = 0
    #: Machines this report's `machine_list` page saved, and expected machines it marked gone.
    machines_listed: int = 0
    machines_gone: int = 0
