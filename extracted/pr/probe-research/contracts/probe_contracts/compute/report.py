"""Node report: the full state of one machine every 15 s (GPUs, who is on them, metric windows)."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .compute import (
    ENV_ALLOWLIST,
    MAX_GPUS_PER_NODE,
    MAX_OCCUPANTS_PER_GPU,
    MAX_POINTS_PER_REPORT,
    SERVER_AGGS,
    NodeState,
)
from .enrollment import GpuInventory, NodeInventory


class OccupantEvidence(BaseModel):
    """One process on a GPU and everything the machine knows about it. Sent whole every report."""

    model_config = ConfigDict(extra="forbid")

    pid: int = Field(ge=1)
    #: Process start time in clock ticks since boot (/proc/<pid>/stat field 22): pid + this = process identity.
    proc_start_ticks: int = Field(ge=0)
    exe: str = Field(max_length=255)
    container_id: str | None = Field(default=None, max_length=128)
    pod_uid: str | None = Field(default=None, max_length=64)
    slurm_job_id: str | None = Field(default=None, max_length=64)
    pidns: int | None = None
    #: Run id from the SDK watcher registry file for this pid (same pid namespace only).
    registry_run_id: str | None = Field(default=None, max_length=128)
    env: dict[str, str] = Field(default_factory=dict)
    #: False when /proc/<pid>/environ could not be read, so an empty `env` means "unknown", not "no keys".
    is_env_readable: bool = True
    gpu_memory_bytes: int | None = Field(default=None, ge=0)
    sm_utilization_percent: float | None = Field(default=None, ge=0, le=100)

    @field_validator("env")
    @classmethod
    def check_env_allowlisted(cls, value: dict[str, str]) -> dict[str, str]:
        unknown = sorted(set(value) - ENV_ALLOWLIST)
        if unknown:
            raise ValueError(f"environment keys outside the allowlist: {unknown}")
        return value


class GpuReport(BaseModel):
    """One GPU's current state and its occupants (many at once is normal: sharing)."""

    model_config = ConfigDict(extra="forbid")

    uuid: str = Field(min_length=4, max_length=128)
    utilization_percent: float | None = Field(default=None, ge=0, le=100)
    memory_used_bytes: int | None = Field(default=None, ge=0)
    power_watts: float | None = Field(default=None, ge=0)
    temperature_c: float | None = None
    occupants: list[OccupantEvidence] = Field(default_factory=list, max_length=MAX_OCCUPANTS_PER_GPU)


class NodeMetricPoint(BaseModel):
    """One 60 s window of one series. Same keys, grid and aggregations as the SDK hardware rail."""

    model_config = ConfigDict(extra="forbid")

    key: str = Field(min_length=1, max_length=256)
    #: Empty for node-level series (CPU, memory, disk, network).
    gpu_uuid: str = Field(default="", max_length=128)
    dims: dict[str, str] = Field(default_factory=dict, max_length=8)
    step_index: int = Field(ge=0)
    value: float
    agg: str

    @field_validator("agg")
    @classmethod
    def check_agg_known(cls, value: str) -> str:
        if value not in SERVER_AGGS:
            raise ValueError(f"agg must be one of {sorted(SERVER_AGGS)}")
        return value


class DaemonHealth(BaseModel):
    model_config = ConfigDict(extra="forbid")

    cpu_percent: float | None = None
    rss_bytes: int | None = None
    dropped_points: int = 0
    open_breakers: list[str] = Field(default_factory=list)


class NodeReportIn(BaseModel):
    """`POST /v1/nodes/{node_id}/report`, authorized by the node credential."""

    model_config = ConfigDict(extra="forbid")

    seq: int = Field(ge=0)
    sent_at: datetime
    boot_id: str | None = Field(default=None, max_length=64)
    #: The goodbye: the daemon received SIGTERM and is exiting (spec: Knowing when a machine is really gone).
    is_stopping: bool = False
    stop_reason: str | None = Field(default=None, max_length=256)
    #: Pod mode's goodbye only: how the wrapped job ended, its exit status or the signal that killed it.
    #: Host and cluster mode are not the job's parent and never send these (unknown, not success).
    job_exit_code: int | None = Field(default=None, ge=0, le=255)
    job_exit_signal: str | None = Field(default=None, min_length=1, max_length=16)
    gpus: list[GpuReport] = Field(default_factory=list, max_length=MAX_GPUS_PER_NODE)
    points: list[NodeMetricPoint] = Field(default_factory=list, max_length=MAX_POINTS_PER_REPORT)
    #: Present only when the GPU list or machine facts changed since the last report.
    gpu_inventory: list[GpuInventory] | None = None
    inventory: NodeInventory | None = None
    health: DaemonHealth = Field(default_factory=DaemonHealth)


class NodeReportAck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    accepted_seq: int
    server_time: datetime
    min_daemon_version: str
    node_state: NodeState
