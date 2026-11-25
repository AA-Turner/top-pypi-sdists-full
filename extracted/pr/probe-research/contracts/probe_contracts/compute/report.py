"""Node report: the full state of one machine every 15 s (GPUs, who is on them, metric windows)."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated

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
    #: GPUs (and their MIG slices) the daemon saw that NVML no longer answers for: fallen off the bus, Xid 79.
    #: Their stints end `gpu_lost` instead of `exited` (conformance F-18).
    lost_gpus: list[Annotated[str, Field(min_length=4, max_length=128)]] = Field(
        default_factory=list, max_length=MAX_GPUS_PER_NODE
    )


#: NodeActivity.signals caps (experiment: agent-monitoring-spec 2a).
MAX_ACTIVITY_SIGNALS = 16
MAX_ACTIVITY_SIGNAL_CHARS = 160


class NodeActivity(BaseModel):
    """Machine-level use beyond GPU processes (experiment, agent-monitoring-spec 2a): a node whose GPUs are
    empty is idle capacity only when all of this is quiet. Rates are over the last report interval;
    `cpu_busy_percent` is None on a daemon's first report."""

    model_config = ConfigDict(extra="forbid")

    cpu_busy_percent: float | None = Field(default=None, ge=0, le=100)
    #: Logged-in users (utmp) or sshd session processes, whichever is larger.
    interactive_sessions: int = Field(default=0, ge=0)
    tmux_servers: int = Field(default=0, ge=0)
    #: Jupyter/IPython (and IJulia, IRkernel) kernels.
    notebook_kernels: int = Field(default=0, ge=0)
    #: rsync/scp/rclone/aws/gsutil/curl/wget/... processes moving more than 64 KB/s.
    transfers: int = Field(default=0, ge=0)
    #: Probe SDK writes not yet delivered on this machine; None when no outbox was found.
    outbox_pending: int | None = Field(default=None, ge=0)
    #: Human-readable evidence ("ssh session: ubuntu@pts/0 (pid 812)"), at most 16.
    signals: list[str] = Field(default_factory=list, max_length=MAX_ACTIVITY_SIGNALS)

    @field_validator("signals")
    @classmethod
    def check_signal_length(cls, value: list[str]) -> list[str]:
        if any(len(s) > MAX_ACTIVITY_SIGNAL_CHARS for s in value):
            raise ValueError(f"each signal is at most {MAX_ACTIVITY_SIGNAL_CHARS} characters")
        return value


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
    #: Experiment (agent-monitoring-spec 2a): absent from daemons that do not read it.
    activity: NodeActivity | None = None


#: The largest spin-down scan a node may attach to an idle alert (`POST /v1/nodes/{id}/idle-scan`).
MAX_IDLE_SCAN_BYTES = 256 * 1024


class IdleScanRequest(BaseModel):
    """The ack asks the node to run `probe-node spindown-scan` once (read-only) and attach the result to this
    idle alert. Sent once, on the ack of the report that fired the alert; an older daemon ignores it."""

    model_config = ConfigDict(extra="forbid")

    alert_id: int = Field(ge=1)


class IdleScanIn(BaseModel):
    """A node's answer to `IdleScanRequest`: the JSON of `probe-node spindown-scan --json`."""

    model_config = ConfigDict(extra="forbid")

    alert_id: int = Field(ge=1)
    scan: dict


class IdleScanAck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    alert_id: int
    at_risk: bool


class UninstallOrder(BaseModel):
    """What an admin's uninstall asks beyond removing probe-node itself. Sent with `node_state = uninstalling`;
    the daemon runs its own fixed uninstall code, never a command from the server."""

    model_config = ConfigDict(extra="forbid")

    #: Also remove SkyPilot itself, not only Probe's policy, plugin and sidecar (A21): its queue may hold jobs.
    include_skypilot: bool = False
    #: The whole cluster is being removed: a DaemonSet may delete its own release. False (one machine of it):
    #: the pod only empties its state dir and stops reporting.
    whole_cluster: bool = False


class NodeReportAck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    accepted_seq: int
    server_time: datetime
    min_daemon_version: str
    node_state: NodeState
    #: Present only when this report fired an idle alert whose team's action wants the machine's scan.
    idle_scan: IdleScanRequest | None = None
    #: Present only while `node_state` is `uninstalling`: the report was not stored.
    uninstall: UninstallOrder | None = None


#: The longest error a node may attach to its "uninstalled" answer.
MAX_UNINSTALL_ERROR_CHARS = 1024


class NodeUninstalledIn(BaseModel):
    """`POST /v1/nodes/{node_id}/uninstalled`: the node removed Probe and is about to stop. `error` names what
    it could not remove (the rest is gone); its credential is revoked either way."""

    model_config = ConfigDict(extra="forbid")

    error: str | None = Field(default=None, max_length=MAX_UNINSTALL_ERROR_CHARS)


class NodeUninstalledAck(BaseModel):
    model_config = ConfigDict(extra="forbid")

    node_state: NodeState
