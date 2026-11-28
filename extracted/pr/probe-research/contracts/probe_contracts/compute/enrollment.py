"""Enrollment: a node joins with an enrollment token and leaves with its own node credential."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ..compat import StrEnum
from .compute import (
    MAX_GPUS_PER_NODE,
    MAX_LABELS,
    Capacity,
    ClusterKind,
    InstallMode,
    NodeKeySource,
    Pricing,
)


class EnrollmentTokenKind(StrEnum):
    """How often an enrollment token enrolls (control/099). Named at every mint: neither is a silent default."""

    #: One machine, at most 2 h, enrolls once; then only the node it made may enroll again, with its credential.
    SINGLE_USE = "single_use"
    #: Many enrollments until it expires (a Helm DaemonSet, pod and container jobs, the SkyPilot reporters).
    REUSABLE = "reusable"


class ClusterEvidence(BaseModel):
    """What the machine knows about the cluster it belongs to (kube-system UID, SLURM ClusterName, a pool label)."""

    model_config = ConfigDict(extra="forbid")

    key: str = Field(min_length=1, max_length=256)
    kind: ClusterKind
    name: str | None = Field(default=None, max_length=256)


class GpuInventory(BaseModel):
    """One physical GPU or MIG slice, keyed by its UUID (globally unique, burned into the hardware)."""

    model_config = ConfigDict(extra="forbid")

    uuid: str = Field(min_length=4, max_length=128)
    index: int = Field(ge=0)
    model: str = Field(max_length=128)
    memory_bytes: int = Field(ge=0)
    mig_parent_uuid: str | None = Field(default=None, max_length=128)
    mig_profile: str | None = Field(default=None, max_length=64)
    #: NVML family name: ampere, hopper, blackwell, rubin; "arch-<n>" for values newer than the daemon knows.
    architecture: str | None = Field(default=None, max_length=32)
    #: The NVLink domain (NVML GPU fabric info). On GB200/GB300 NVL72 it spans the nodes of one rack.
    fabric_cluster_uuid: str | None = Field(default=None, max_length=64)
    #: NVML's clique id is a uint32, so it can exceed a signed 32-bit integer.
    fabric_clique_id: int | None = Field(default=None, ge=0, le=2**32 - 1)


class NodeInventory(BaseModel):
    """Machine facts that change rarely; resent only when they change."""

    model_config = ConfigDict(extra="forbid")

    driver_version: str | None = None
    cuda_driver_version: str | None = None
    cpu_count: int | None = None
    memory_bytes: int | None = None
    os: str | None = None
    kernel: str | None = None
    #: GPU UUID pairs joined by NVLink, as "uuidA|uuidB".
    nvlink_pairs: list[str] = Field(default_factory=list)


class EnrollIn(BaseModel):
    """`POST /v1/nodes/enroll`, authorized by an enrollment token (Authorization: Bearer probe_nodeenroll_...)."""

    model_config = ConfigDict(extra="forbid")

    node_key: str = Field(min_length=1, max_length=256)
    node_key_source: NodeKeySource
    install_mode: InstallMode
    hostname: str = Field(max_length=255)
    daemon_version: str = Field(max_length=64)
    capacity: Capacity | None = None
    provider: str | None = Field(default=None, max_length=64)
    instance_id: str | None = Field(default=None, max_length=128)
    instance_type: str | None = Field(default=None, max_length=128)
    region: str | None = Field(default=None, max_length=64)
    zone: str | None = Field(default=None, max_length=64)
    pricing: Pricing | None = None
    cluster: ClusterEvidence | None = None
    gpus: list[GpuInventory] = Field(default_factory=list, max_length=MAX_GPUS_PER_NODE)
    inventory: NodeInventory = Field(default_factory=NodeInventory)
    #: Hashed with the team salt on the machine: system UUID, InfiniBand GUIDs, NIC MACs, GPU serials.
    identity_evidence: dict[str, str] = Field(default_factory=dict)
    labels: dict[str, str] = Field(default_factory=dict, max_length=MAX_LABELS)


class EnrollOut(BaseModel):
    """The node's id and its own credential (shown once), plus what the server expects of it."""

    model_config = ConfigDict(extra="forbid")

    node_id: UUID
    node_credential: str
    report_interval_seconds: int
    min_daemon_version: str
    server_time: datetime
    #: The team salt for hashing identity evidence on this machine.
    evidence_salt: str
