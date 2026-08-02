from __future__ import annotations

import hashlib
import logging
import random
from collections import Counter
from typing import TYPE_CHECKING, Any, Optional, TypedDict, cast

import attrs
import ray
from ray.util.state import list_actors

from geneva.config import ConfigBase
from geneva.constants import DEFAULT_K8S_NS

if TYPE_CHECKING:
    from kubernetes import client

    from geneva.runners.kuberay.client import KuberayClients

_LOG = logging.getLogger(__name__)

KUBERAY_API_GROUP = "ray.io"  # API group for KubeRay RayCluster CRD
KUBERAY_API_VERSION = "v1"  # CRD version
KUBERAY_API_GROUP_VERSION = f"{KUBERAY_API_GROUP}/{KUBERAY_API_VERSION}"
KUBERAY_JOB_API_KIND = "RayJob"
KUBERAY_JOB_API_NAME = "rayjobs"
KUBERAY_CLUSTER_PLURAL = "rayclusters"  # lowercase, plural form of the kind


@attrs.define
class KuberayConfig(ConfigBase):
    checkpoint_store: str = attrs.field()
    ray_version: str = attrs.field()
    namespace: str = attrs.field(default=DEFAULT_K8S_NS)
    worker_min_replicas: int = attrs.field(default=0)
    worker_max_replicas: int = attrs.field(default=10)

    @classmethod
    def name(cls) -> str:
        return "kuberay"


def generate_job_name(
    db_uri: str,
    table_name: str,
    column: str,
) -> str:
    db_name = db_uri.split("/")[-1]
    seed = random.randint(0, 1000000)
    job_name = f"ray-geneva-{db_name[:6]}-{table_name[6]}-{column[:6]}-{hashlib.md5(str(seed).encode()).hexdigest()[:6]}"  # noqa E501
    return job_name


def _ray_status() -> dict[str, Any]:
    """Check the status of the compute cluster
    Checks ray actors, ray and k8s to show progress
    """
    status: dict[str, Any] = {
        "cnt_ray_nodes": 0,
        "cnt_geneva_workers_active": 0,
        "cnt_geneva_workers_pending": 0,
    }

    try:
        # of machines in ray cluster
        nodes = ray.nodes()
        live_nodes = [n for n in nodes if n["Alive"]]
        status["cnt_ray_nodes"] = len(live_nodes)
    except Exception as e:
        # Best-effort status refresh; keep the traceback at debug (see below).
        _LOG.debug("Problem listing ray nodes", exc_info=True)
        status["ray_nodes_error"] = e

    try:
        # we want the ALIVE and PENDING_CREATION actors, but filter syntax does not
        # support OR.  instead we just exclude DEAD actors

        # Target the cluster this process is attached to. Without an explicit
        # address the state API auto-detects, which fails ("Found multiple active
        # Ray instances") when another local Ray cluster is also running.
        actors = list_actors(
            address=ray.get_runtime_context().gcs_address,
            filters=[("state", "!=", "DEAD"), ("class_name", "=", "ApplierActor")],
            limit=10000,
            detail=True,
            raise_on_missing_output=False,
        )
        live_applier_actors = [
            a.actor_id  # type: ignore[attr-defined]
            for a in actors
            if a.class_name == "ApplierActor" and a.state == "ALIVE"  # type: ignore[attr-defined]
        ]
        status["cnt_geneva_workers_active"] = len(live_applier_actors)

        pending_applier_actors = [
            a.actor_id  # type: ignore[attr-defined]
            for a in actors
            if a.class_name == "ApplierActor"  # type: ignore[attr-defined]
            and a.state in ("PENDING_CREATION", "DEPENDENCIES_UNREADY", "RESTARTING")  # type: ignore[attr-defined]
        ]
        status["cnt_geneva_workers_pending"] = len(pending_applier_actors)
    except Exception as e:
        # Best-effort status refresh; a failure just leaves the worker counts at
        # 0 for this tick. Keep the traceback at debug so it doesn't spam ERROR.
        _LOG.debug("Problem listing actors", exc_info=True)
        status["geneva_workers_error"] = e

    _LOG.debug(f"cluster status: {status}")
    return status


class PodStatus(TypedDict):
    name: str
    phase: str  # Pending | Running | Succeeded | Failed | Unknown
    ready: bool
    node_type: str | None  # head | worker | None (if unlabeled)
    node_name: str | None
    waiting_reasons: Counter[str]  # main containers
    init_waiting_reasons: Counter[str]  # init containers
    pulling_count: int  # total containers currently "Pulling..."
    gpu_requested: bool
    node_is_gpu: bool | None
    oom_evidence: Counter[str]


# Which extended resources count as "GPU"
_GPU_KEYS = ("nvidia.com/gpu", "amd.com/gpu", "intel.com/gpu")


def _qty_gt_zero(q: Any) -> bool:
    try:
        # K8s quantities for extended resources are ints (e.g. "1")
        return int(q) > 0
    except Exception:
        return False


def _container_wants_gpu(c: client.V1Container) -> bool:
    from kubernetes import client

    r = c.resources or client.V1ResourceRequirements()
    for d in (r.limits or {}), (r.requests or {}):
        for k in _GPU_KEYS:
            if k in d and _qty_gt_zero(d[k]):
                return True
    return False


def _pod_requests_gpu(pod: client.V1Pod) -> bool:
    spec = pod.spec
    if not spec:
        return False
    for c in spec.init_containers or []:
        if _container_wants_gpu(c):
            return True
    return any(_container_wants_gpu(c) for c in spec.containers or [])


def _terminated_oom_evidence(terminated: Any, state_name: str) -> Counter[str]:
    evidence: Counter[str] = Counter()
    if terminated is None:
        return evidence

    if getattr(terminated, "reason", None) == "OOMKilled":
        evidence[f"{state_name}.reason=OOMKilled"] += 1
    message = getattr(terminated, "message", None) or ""
    if "memory cgroup out of memory" in message.lower():
        evidence[f"{state_name}.message=memory cgroup out of memory"] += 1
    return evidence


def _container_oom_evidence(container_status: Any) -> Counter[str]:
    evidence: Counter[str] = Counter()
    for state_name in ("state", "last_state"):
        state = getattr(container_status, state_name, None)
        evidence.update(
            _terminated_oom_evidence(
                getattr(state, "terminated", None),
                state_name,
            )
        )
    return evidence


def _node_is_gpu(
    clients: KuberayClients, node_name: str, cache: dict[str, bool]
) -> bool:
    if node_name in cache:
        return cache[node_name]
    try:
        n: client.V1Node = cast("client.V1Node", clients.core_api.read_node(node_name))
        if n.status is None:
            has_gpu = False
        else:
            alloc = n.status.allocatable or {}
            has_gpu = any(_qty_gt_zero(alloc.get(k)) for k in _GPU_KEYS)
    except Exception:
        has_gpu = False
    cache[node_name] = has_gpu
    return has_gpu


def k8s_status(
    clients: KuberayClients,
    namespace: str = DEFAULT_K8S_NS,
    *,
    cluster_name: str | None = None,
) -> list[PodStatus]:
    # List all pods in the namespace, scoped to the RayCluster when provided.
    selector = f"ray.io/cluster={cluster_name}" if cluster_name is not None else None
    pods = clients.core_api.list_namespaced_pod(namespace, label_selector=selector)

    # Filter Ray pods by label (adjust depending on your RayCluster setup)
    ray_pods = [
        pod
        for pod in pods.items
        if pod.metadata
        and pod.metadata.labels
        and "ray.io/node-type" in pod.metadata.labels
        and (
            cluster_name is None
            or pod.metadata.labels.get("ray.io/cluster") == cluster_name
        )
    ]

    # Summarize pod phases and conditions
    node_gpu_cache: dict[str, bool] = {}
    out: list[PodStatus] = []
    for pod in ray_pods:
        phase: str = pod.status.phase or "Unknown"
        conds: list[client.V1PodCondition] = pod.status.conditions or []
        cond_map = {c.type: c.status for c in conds}

        waiting: Counter[str] = Counter()
        init_waiting: Counter[str] = Counter()
        oom_evidence: Counter[str] = Counter()
        pulling_count = 0

        # Init containers
        for cs in pod.status.init_container_statuses or []:
            oom_evidence.update(_container_oom_evidence(cs))
            st = cs.state
            if st and st.waiting:
                reason = st.waiting.reason or "Waiting"
                init_waiting[reason] += 1
                if reason.lower().startswith("pull"):
                    pulling_count += 1

        # Main containers
        for cs in pod.status.container_statuses or []:
            oom_evidence.update(_container_oom_evidence(cs))
            st = cs.state
            if st and st.waiting:
                reason = st.waiting.reason or "Waiting"
                waiting[reason] += 1
                if reason.lower().startswith("pull"):
                    pulling_count += 1

        node_name = pod.spec.node_name if pod.spec else None
        node_is_gpu = (
            _node_is_gpu(clients, node_name, node_gpu_cache) if node_name else None
        )

        out.append(
            PodStatus(
                name=pod.metadata.name,
                phase=phase,
                ready=(cond_map.get("Ready") == "True"),
                node_type=pod.metadata.labels.get("ray.io/node-type"),
                node_name=pod.spec.node_name if pod.spec else None,
                waiting_reasons=waiting,
                init_waiting_reasons=init_waiting,
                pulling_count=pulling_count,
                gpu_requested=_pod_requests_gpu(pod),
                node_is_gpu=node_is_gpu,
                oom_evidence=oom_evidence,
            )
        )
    return out


def _node_ready_split_for(
    clients: KuberayClients, pod_statuses: list[PodStatus]
) -> tuple[int, int, int, int]:
    """
    Returns (gpu_ready, gpu_notready, cpu_ready, cpu_notready)
    for nodes that host any of the provided pods.
    """
    nodes_seen: dict[str, bool] = {}  # node_name -> is_gpu
    ready_map: dict[str, bool] = {}  # node_name -> Ready True/False

    # collect unique node names from these pods
    node_names = {s["node_name"] for s in pod_statuses if s["node_name"]}

    # read node objects once
    for name in node_names:
        try:
            n: client.V1Node = cast("client.V1Node", clients.core_api.read_node(name))
            if n.status is None:
                is_ready = False
                is_gpu = False
            else:
                conds = {c.type: c.status for c in (n.status.conditions or [])}
                is_ready = conds.get("Ready") == "True"
                alloc = n.status.allocatable or {}
                is_gpu = any(_qty_gt_zero(alloc.get(k)) for k in _GPU_KEYS)
            nodes_seen[name] = is_gpu
            ready_map[name] = is_ready
        except Exception:  # noqa PERF203
            # if we can’t read, treat as not ready & cpu
            nodes_seen[name] = False
            ready_map[name] = False

    gpu_ready = gpu_notready = cpu_ready = cpu_notready = 0
    for name, is_gpu in nodes_seen.items():
        if ready_map.get(name, False):
            if is_gpu:
                gpu_ready += 1
            else:
                cpu_ready += 1
        else:
            if is_gpu:
                gpu_notready += 1
            else:
                cpu_notready += 1
    return gpu_ready, gpu_notready, cpu_ready, cpu_notready


def kuberay_cluster_status(
    clients: KuberayClients, namespace: str, name: str
) -> Optional[dict[str, Any]]:
    try:
        obj = clients.custom_api.get_namespaced_custom_object(
            group="ray.io",
            version="v1",
            namespace=namespace,
            plural="rayclusters",
            name=name,
        )
        return obj.get("status") if obj else None  # type: ignore[attr-defined]
    except Exception as e:
        _LOG.debug(f"error getting kuberay status: {e}")
        return None


class WorkerGroupBrief(TypedDict):
    name: str
    desired: int
    ready: int


class KuberaySummary(TypedDict):
    phase: (
        str  # "nodes-provisioning" | "pods-creating" | "cluster-cold" | "cluster-warm"
    )
    phase_idx: int  # monotonically increasing index for your progress bar
    pending: int
    running: int
    workers_ready: int
    waits_top3: list[tuple[str, int]]
    pulling: int
    total_pods: int

    # kuberay
    kr_state: str | None
    kr_desired_workers: int | None
    kr_available_workers: int | None
    kr_last_update: str | None
    kr_scaling: str | None  # "up" | "down" | "steady" | None
    kr_groups: list[WorkerGroupBrief]  # per workger-group ready/desired
    kr_last_condition: tuple[str, str] | None  # reason, type if present

    # pod splits
    pods_gpu_running: int
    pods_gpu_pending: int
    pods_cpu_running: int
    pods_cpu_pending: int
    workers_ready_gpu: int
    workers_ready_cpu: int

    # node splits (only nodes hosting this cluster’s pods)
    nodes_gpu_ready: int
    nodes_gpu_notready: int
    nodes_cpu_ready: int
    nodes_cpu_notready: int


def _get_int(d: dict[str, Any], *keys: str) -> Optional[int]:
    for k in keys:
        v = d.get(k)
        if isinstance(v, int):
            return v
    return None


def _parse_worker_groups(status: dict[str, Any]) -> list[WorkerGroupBrief]:
    out: list[WorkerGroupBrief] = []
    # Newer KubeRay surfaces workerGroupStatuses; older embeds in spec/status
    # differently
    wgs = status.get("workerGroupStatuses") or []
    for item in wgs:
        name = item.get("groupName") or item.get("name") or "worker"
        desired = _get_int(item, "desiredReplicas", "replicas", "desired") or 0
        ready = _get_int(item, "readyReplicas", "availableReplicas", "ready") or 0
        out.append(WorkerGroupBrief(name=name, desired=desired, ready=ready))
    return out


def _parse_scaling(status: dict[str, Any]) -> Optional[str]:
    # Heuristic: desired vs available (or ready) tells the story
    desired = _get_int(status, "desiredWorkerReplicas", "desiredWorkerCount")
    avail = _get_int(status, "availableWorkerReplicas", "availableWorkerCount")
    if desired is None or avail is None:
        return None
    if desired > avail:
        return "up"
    if desired < avail:
        return "down"
    return "steady"


def _last_condition(status: dict[str, Any]) -> Optional[tuple[str, str]]:
    # Surfaces *some* operator condition, if present
    conds = status.get("conditions") or []
    if not isinstance(conds, list) or not conds:
        return None
    last = conds[-1]
    reason = str(last.get("reason") or "?")
    typ = str(last.get("type") or "?")
    return (reason, typ)


def summarize_k8s(
    clients: KuberayClients,
    statuses: list[PodStatus],
    cluster_name: str,
    namespace: str = DEFAULT_K8S_NS,
) -> KuberaySummary:
    phases = Counter(s["phase"] for s in statuses)
    waits = Counter()
    pulling = 0
    workers_ready = 0
    workers_ready_gpu = 0
    workers_ready_cpu = 0
    pods_gpu_running = pods_gpu_pending = 0
    pods_cpu_running = pods_cpu_pending = 0

    for s in statuses:
        waits.update(s["waiting_reasons"])
        waits.update(s["init_waiting_reasons"])
        pulling += s["pulling_count"]
        if s["node_type"] == "worker" and s["phase"] == "Running" and s["ready"]:
            workers_ready += 1
            if s.get("gpu_requested"):
                workers_ready_gpu += 1
            else:
                workers_ready_cpu += 1

        # pod splits by GPU/CPU and phase
        is_gpu = bool(s.get("gpu_requested"))
        if s["phase"] == "Running":
            if is_gpu:
                pods_gpu_running += 1
            else:
                pods_cpu_running += 1
        elif s["phase"] == "Pending":
            if is_gpu:
                pods_gpu_pending += 1
            else:
                pods_cpu_pending += 1

    # Phase selection focused on “cold start” (= no workers ready yet)
    if phases["Pending"] > 0 and any(
        k.lower().startswith(("unschedulable", "waiting")) for k in waits
    ):
        phase, phase_idx = "nodes-provisioning", 1
    elif pulling > 0 or any(k.lower().startswith("containercreating") for k in waits):
        phase, phase_idx = "pods-creating", 2
    elif workers_ready == 0:
        phase, phase_idx = "cluster-cold", 3
    else:
        phase, phase_idx = "cluster-warm", 4

    kr_status = kuberay_cluster_status(clients, namespace, cluster_name)
    if kr_status is None:
        _LOG.warning(
            f"Could not fetch KubeRay status for {namespace}/{cluster_name}..."
        )
        kr_status = {}

    desired = _get_int(kr_status, "desiredWorkerReplicas", "desiredWorkerCount")
    avail = _get_int(kr_status, "availableWorkerReplicas", "availableWorkerCount")
    groups = _parse_worker_groups(kr_status)
    scaling = _parse_scaling(kr_status)
    last_cond = _last_condition(kr_status)

    # Node readiness split (only nodes hosting our Ray pods)
    nodes_gpu_ready, nodes_gpu_notready, nodes_cpu_ready, nodes_cpu_notready = (
        _node_ready_split_for(clients, statuses)
    )

    def _int_or_none(v: Any) -> int | None:
        return int(v) if isinstance(v, int) else None

    return KuberaySummary(
        phase=phase,
        phase_idx=phase_idx,
        pending=phases.get("Pending", 0),
        running=phases.get("Running", 0),
        workers_ready=workers_ready,
        waits_top3=waits.most_common(3),
        pulling=pulling,
        total_pods=len(statuses),
        kr_state=kr_status.get("state"),
        kr_desired_workers=_int_or_none(desired),
        kr_available_workers=_int_or_none(avail),
        kr_last_update=kr_status.get("lastUpdateTime"),
        kr_scaling=scaling,
        kr_groups=groups,
        kr_last_condition=last_cond,
        # NEW pod splits
        pods_gpu_running=pods_gpu_running,
        pods_gpu_pending=pods_gpu_pending,
        pods_cpu_running=pods_cpu_running,
        pods_cpu_pending=pods_cpu_pending,
        workers_ready_gpu=workers_ready_gpu,
        workers_ready_cpu=workers_ready_cpu,
        # NEW node splits
        nodes_gpu_ready=nodes_gpu_ready,
        nodes_gpu_notready=nodes_gpu_notready,
        nodes_cpu_ready=nodes_cpu_ready,
        nodes_cpu_notready=nodes_cpu_notready,
    )


def summarize_kuberay_status(
    clients: KuberayClients, namespace: str | None, cluster_name: str | None
) -> KuberaySummary:
    if namespace is None:
        namespace = DEFAULT_K8S_NS
    if cluster_name is None:
        raise ValueError("cluster_name is required")
    k8s_statuses = k8s_status(clients, namespace=namespace, cluster_name=cluster_name)
    k8s_summary = summarize_k8s(
        clients, k8s_statuses, cluster_name=cluster_name, namespace=namespace
    )
    return k8s_summary
