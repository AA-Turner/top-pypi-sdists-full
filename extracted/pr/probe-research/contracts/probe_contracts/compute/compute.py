"""Compute: the vocabularies the node daemon, the server and the SDK share (probe-node spec, P0).
Wire shapes live beside this file; the Go daemon mirrors them and is held to `vectors/`."""

from __future__ import annotations

from ..compat import StrEnum

#: How often a node daemon sends a state report, and how many missed reports make a node `silent`.
REPORT_INTERVAL_SECONDS = 15
SILENT_AFTER_MISSED_REPORTS = 3
#: A silent node with no other signal is `retired` (credential revoked, stints closed) after this.
RETIRE_AFTER_SECONDS = 24 * 3600
#: The metric step grid, shared with the SDK hardware rail (`sdk/hardware/grid.py` HW_STEP_SECONDS).
STEP_SECONDS = 60
#: The latest full report is kept on the node row for the live view; larger reports are refused. 256 KiB holds
#: ~750 occupants without points (conformance F-21; it was 64 KiB, ~190).
MAX_REPORT_BYTES = 256 * 1024
MAX_POINTS_PER_REPORT = 5_000
MAX_GPUS_PER_NODE = 64
MAX_OCCUPANTS_PER_GPU = 64
MAX_LABELS = 32
MAX_LABEL_CHARS = 256

#: Credential prefixes: an enrollment token joins nodes; a node credential is one node's own key.
ENROLLMENT_TOKEN_PREFIX = "probe_nodeenroll_"
NODE_CREDENTIAL_PREFIX = "probe_node_"

#: The only process environment keys a daemon may read and send. Everything else is dropped on the machine.
#: The session keys are the coding-agent harnesses' `session_env` (foundation/harness_registry/harnesses.json).
ENV_ALLOWLIST = frozenset(
    {
        "PROBE_RUN_ID",
        "PROBE_LAUNCH_ID",
        "SLURM_JOB_ID",
        #: A SkyPilot managed job's id (T5): its stint names it, and `probe compute job stop` refuses it.
        "SKYPILOT_MANAGED_JOB_ID",
        "RAY_JOB_ID",
        "TORCHELASTIC_RUN_ID",
        "CLAUDE_CODE_SESSION_ID",
        "CODEX_THREAD_ID",
        "PI_SESSION_ID",
        "PROBE_KIMI_SESSION_ID",
        "CURSOR_CONVERSATION_ID",
    }
)
#: Which allowlisted keys name a coding-agent session (an untracked occupant's owner).
AGENT_SESSION_ENV_KEYS = (
    "CLAUDE_CODE_SESSION_ID",
    "CODEX_THREAD_ID",
    "PI_SESSION_ID",
    "PROBE_KIMI_SESSION_ID",
    "CURSOR_CONVERSATION_ID",
)
#: The metric aggregations the server accepts (closed: one unknown value refuses the batch).
SERVER_AGGS = frozenset({"mean", "sum", "min", "max", "count"})


class InstallMode(StrEnum):
    """Where the daemon runs: a DaemonSet, a system service, or a wrapper inside a container."""

    CLUSTER = "cluster"
    HOST = "host"
    POD = "pod"
    #: A queue reader beside a scheduler (the SkyPilot API server's sidecar, T5): no GPUs, never a machine.
    QUEUE = "queue"


class Capacity(StrEnum):
    """Reserved long-term machines, or rented ones billed by the hour."""

    OWNED = "owned"
    BURST = "burst"


class Pricing(StrEnum):
    ON_DEMAND = "on_demand"
    SPOT = "spot"
    RESERVED = "reserved"
    OWNED = "owned"


class NodeKeySource(StrEnum):
    """Which identity rule produced the node key (spec: Identity)."""

    INSTANCE_ID = "instance_id"
    K8S_NODE = "k8s_node"
    MINTED = "minted"
    POD_UID = "pod_uid"


class NodeState(StrEnum):
    """Where a node is. `silent` after missed reports; `released` on a goodbye or a provider answer;
    `uninstalling` once an admin asked to remove Probe from it (its report ack carries the order)."""

    ACTIVE = "active"
    SILENT = "silent"
    RELEASED = "released"
    BILLING_UNATTENDED = "billing_unattended"
    UNKNOWN = "unknown"
    RETIRED = "retired"
    UNINSTALLING = "uninstalling"


class ClusterKind(StrEnum):
    KUBERNETES = "kubernetes"
    SLURM = "slurm"
    POOL = "pool"


class OccupantKind(StrEnum):
    """A process seen on the GPU, or a GPU the kubelet assigned to a pod (from P1)."""

    PROCESS = "process"
    ALLOCATION = "allocation"


class WorkloadKind(StrEnum):
    TRAINING = "training"
    INFERENCE = "inference"
    NOTEBOOK = "notebook"
    EVAL = "eval"
    UNTRACKED = "untracked"
    UNKNOWN = "unknown"


class MatchRule(StrEnum):
    """Which join rule tied an occupant to a run, strongest first (spec: Detecting jobs)."""

    ENVIRON = "environ"
    REGISTRY = "registry"
    GPU_UUID = "gpu_uuid"
    POD = "pod"
    CONTAINER = "container"
    SLURM = "slurm"
    NONE = "none"


class StintEndReason(StrEnum):
    EXITED = "exited"
    NODE_GONE = "node_gone"
    NODE_RELEASED = "node_released"
    #: The GPU fell off the bus (Xid 79): the daemon named it in `health.lost_gpus` (conformance F-18).
    GPU_LOST = "gpu_lost"
