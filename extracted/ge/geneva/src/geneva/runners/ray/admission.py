# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""
Admission control for Geneva Ray jobs.

This module validates that cluster resources are sufficient before starting
a backfill job, preventing jobs from hanging indefinitely.
"""

from __future__ import annotations

import atexit
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeoutError
from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING, Any, TypeVar

import attrs
import ray
from kubernetes.utils import parse_quantity

from geneva._context import get_current_context
from geneva.config import ConfigBase, str_to_bool
from geneva.runners.ray.raycluster import RayCluster

if TYPE_CHECKING:
    from collections.abc import Callable

    from geneva.transformer import UDF

_LOG = logging.getLogger(__name__)


# =============================================================================
# Admission Control Configuration
# =============================================================================
@attrs.define
class AdmissionConfig(ConfigBase):
    """Configuration for admission control.

    Can be configured via:
    - Environment variables: GENEVA_ADMISSION__CHECK, GENEVA_ADMISSION__STRICT,
      GENEVA_ADMISSION__TIMEOUT (uses '__' double underscore separator)
    - pyproject.toml: [geneva.geneva_admission] section
    - Config files: .config/*.yaml, .config/*.json, .config/*.toml

    ``strict`` defaults to False: admission control reports insufficient
    resources as a warning and lets the job proceed. Set it to True (or pass
    ``_admission_strict=True``) to fail fast instead.
    """

    check: bool = attrs.field(default=True, converter=str_to_bool)
    strict: bool = attrs.field(default=False, converter=str_to_bool)
    timeout: float = attrs.field(default=3.0, converter=float)

    @classmethod
    def name(cls) -> str:
        return "geneva_admission"


# =============================================================================
# Timeout Configuration
# =============================================================================
# Shared executor for timeout-wrapped calls (avoids creating threads per call)
_TIMEOUT_EXECUTOR = ThreadPoolExecutor(max_workers=2, thread_name_prefix="admission-")
atexit.register(lambda: _TIMEOUT_EXECUTOR.shutdown(wait=False))

T = TypeVar("T")


def _call_with_timeout(
    func: Callable[[], T], timeout_secs: float | None = None
) -> T | None:
    """Call a function with a timeout, returning None on timeout or error.

    This is used to wrap Ray API calls that can hang indefinitely when the
    cluster is in a bad state (stale, partially initialized, etc.).

    Parameters
    ----------
    func : Callable
        The function to call (should take no arguments)
    timeout_secs : float, optional
        Timeout in seconds. If not specified, uses AdmissionConfig.timeout.

    Returns
    -------
    T | None
        The function result, or None if timeout/error occurred.
    """
    config = AdmissionConfig.get()
    timeout = timeout_secs if timeout_secs is not None else config.timeout
    future = _TIMEOUT_EXECUTOR.submit(func)
    try:
        return future.result(timeout=timeout)
    except FuturesTimeoutError:
        future.cancel()
        _LOG.warning(f"Admission control: {func.__name__}() timed out after {timeout}s")
        return None
    except Exception as e:
        _LOG.warning(f"Admission control: {func.__name__}() failed: {e}")
        return None


# =============================================================================
# Actor Resource Configuration
# =============================================================================


@attrs.define
class PipelineResourceConfig(ConfigBase):
    """Resource allocations for Geneva pipeline infrastructure actors.

    Can be configured via:
    - Environment variables: GENEVA_PIPELINE_RESOURCES__DRIVER_NUM_CPUS, etc.
      (uses '__' double underscore separator)
    - pyproject.toml: [geneva.geneva_pipeline_resources] section
    - Config files: .config/*.yaml, .config/*.json, .config/*.toml

    Note: Queue actors use 0 resources (no CPU/memory requirement).
    """

    driver_num_cpus: float = attrs.field(default=0.1, converter=float)
    jobtracker_num_cpus: float = attrs.field(default=0.1, converter=float)
    jobtracker_memory: int = attrs.field(
        default=128 * 1024 * 1024,
        converter=int,  # 128 MiB
    )
    fragment_writer_num_cpus: float = attrs.field(default=0.1, converter=float)
    fragment_writer_memory: int = attrs.field(
        default=1024 * 1024 * 1024,
        converter=int,  # 1 GiB
    )
    # GEN-631: how Ray places FragmentWriter actors across nodes.
    #   "spread" (default) -> best-effort one-writer-per-node; spreads write
    #     bandwidth and per-writer working set across pods instead of packing
    #     them onto the first node with capacity (which OOMs the pod and gates
    #     aggregate write throughput on a single NIC).
    #   "pack" -> Ray's default hybrid scheduler (the old behavior); useful for
    #     small writers / density-friendly UDFs.
    # Honors the short env var GENEVA_FRAGMENT_WRITER_SCHEDULING=pack|spread as
    # its default; the structured override
    # GENEVA_PIPELINE_RESOURCES__FRAGMENT_WRITER_SCHEDULING still takes priority.
    fragment_writer_scheduling: str = attrs.field(
        factory=lambda: (
            os.environ.get("GENEVA_FRAGMENT_WRITER_SCHEDULING", "spread")
            .strip()
            .lower()
        ),
        converter=lambda v: str(v).strip().lower(),
    )

    def __attrs_post_init__(self) -> None:
        # Validate scheduling mode once at construction so a misconfigured
        # value warns a single time per process rather than once per fragment.
        if self.fragment_writer_scheduling not in ("pack", "spread"):
            _LOG.warning(
                "Unknown fragment_writer_scheduling %r; using 'spread'. "
                "Valid values: 'pack', 'spread'.",
                self.fragment_writer_scheduling,
            )

    @classmethod
    def name(cls) -> str:
        return "geneva_pipeline_resources"

    def fragment_writer_scheduling_strategy(self) -> str | None:
        """Resolve the configured packing mode to a Ray ``scheduling_strategy``.

        Returns ``"SPREAD"`` for best-effort one-writer-per-node placement, or
        ``None`` (Ray's default hybrid scheduler, which packs) for ``"pack"``.
        Unknown values fall back to spread, the safe default.
        """
        if self.fragment_writer_scheduling == "pack":
            return None
        return "SPREAD"


def _get_resource_config() -> PipelineResourceConfig:
    return PipelineResourceConfig.get()


# Module-level constants for backward compatibility.
# These are evaluated at import time with default values.
# For runtime-configurable values, use PipelineResourceConfig.get() directly.
DRIVER_NUM_CPUS = 0.1
JOBTRACKER_NUM_CPUS = 0.1
JOBTRACKER_MEMORY = 128 * 1024 * 1024  # 128 MiB
FRAGMENT_WRITER_NUM_CPUS = 0.1
FRAGMENT_WRITER_MEMORY = 1024 * 1024 * 1024  # 1 GiB


class AdmissionDecision(Enum):
    """Result of admission control check."""

    ALLOW = auto()  # Resources available, proceed immediately
    ALLOW_WITH_WARNING = auto()  # Resources exist but busy, may wait
    REJECT = auto()  # Resources will never be available


class ResourcesUnavailableError(Exception):
    """Raised when job cannot run due to insufficient cluster resources."""


class ClusterKind(Enum):
    """Which kind of Ray cluster admission control is running against."""

    KUBERAY = auto()  # Geneva-managed KubeRay cluster (autoscaling known)
    LOCAL = auto()  # Local ray.init() cluster
    EXTERNAL = auto()  # Pre-existing cluster connected to by address


def _detect_cluster_kind() -> ClusterKind:
    """Classify the current Ray connection for admission messaging."""
    if _is_kuberay_cluster():
        return ClusterKind.KUBERAY

    from geneva._context import LocalRayContext

    if isinstance(get_current_context(), LocalRayContext):
        return ClusterKind.LOCAL
    return ClusterKind.EXTERNAL


def _cluster_advisory(kind: ClusterKind) -> str:
    """Explain what the admission check did and did not account for.

    Autoscaling is the main source of false rejections: on KubeRay we know the
    max scale capacity, on an external cluster we only see current capacity.
    """
    if kind is ClusterKind.KUBERAY:
        return (
            "This check accounts for the cluster's maximum autoscale capacity, "
            "so the job is unlikely to become schedulable by scaling up."
        )
    if kind is ClusterKind.EXTERNAL:
        return (
            "This check compares against the external cluster's current "
            "capacity and does not account for autoscaling. If the cluster can "
            "scale up, the job may still be schedulable."
        )
    return ""


def _warn_admission(prefix: str, message: str, kind: ClusterKind) -> None:
    """Log a non-strict admission rejection with cluster-specific context."""
    parts = [message, _cluster_advisory(kind)]
    parts.append("Proceeding anyway; set _admission_strict=True to fail fast.")
    _LOG.warning("%s: %s", prefix, " ".join(p for p in parts if p))


@dataclass
class JobResources:
    """Resources required for a backfill job."""

    # Applier resources (main workload)
    applier_cpus: float
    applier_gpus: float
    applier_memory: int

    # Worker-side overhead resources (JobTracker, writers, queues)
    overhead_cpus: float
    overhead_memory: int

    # Configuration
    concurrency: int
    udf_cpus: float
    udf_gpus: float
    udf_memory: int = 0

    @property
    def total_cpus(self) -> float:
        return self.applier_cpus + self.overhead_cpus

    @property
    def total_gpus(self) -> float:
        return self.applier_gpus

    @property
    def total_memory(self) -> int:
        return self.applier_memory + self.overhead_memory

    def __str__(self) -> str:
        return (
            f"JobResources(cpus={self.total_cpus:.1f}, gpus={self.total_gpus:.1f}, "
            f"memory={self.total_memory / 1e9:.1f}GB, concurrency={self.concurrency})"
        )


@dataclass
class NodeCapacity:
    """Resources available on a single node or worker group."""

    cpus: float = 0.0
    gpus: float = 0.0
    memory: int = 0

    def can_fit(self, udf_cpus: float, udf_gpus: float, udf_memory: int) -> bool:
        """Check if this node can fit a UDF with the given requirements."""
        # Only check dimensions that the UDF actually requires
        if udf_cpus > 0 and self.cpus < udf_cpus:
            return False
        if udf_gpus > 0 and self.gpus < udf_gpus:
            return False
        # Memory check
        return not (udf_memory > 0 and self.memory < udf_memory)


@dataclass
class ClusterResources:
    """Available cluster resources."""

    # Total capacity
    total_cpus: float
    total_gpus: float
    total_memory: int

    # Currently available
    available_cpus: float
    available_gpus: float
    available_memory: int

    # Cluster type
    is_kuberay: bool = False
    max_scale_cpus: float | None = None  # For KubeRay: resources at max scale
    max_scale_gpus: float | None = None
    max_scale_memory: int | None = None

    # Per-node capacities for checking UDF feasibility on heterogeneous clusters
    # Each entry represents the resources available on a single node or worker group
    node_capacities: list[NodeCapacity] | None = None

    # Max resources on any single node (legacy, for backward compatibility)
    max_node_cpus: float = 0.0
    max_node_gpus: float = 0.0
    max_node_memory: int = 0

    def any_node_can_fit(
        self, udf_cpus: float, udf_gpus: float, udf_memory: int
    ) -> bool:
        """Check if any node can fit a UDF with all the given requirements."""
        if not self.node_capacities:
            # Fallback to legacy max-per-node values when per-node list is unavailable.
            # Unlike can_fit() on real nodes (where 0 means "none"), here 0 means
            # "unknown/not tracked" — so only check dimensions with reported data.
            if (
                self.max_node_cpus == 0
                and self.max_node_gpus == 0
                and self.max_node_memory == 0
            ):
                return False
            if (
                udf_cpus > 0
                and self.max_node_cpus > 0
                and udf_cpus > self.max_node_cpus
            ):
                return False
            if (
                udf_gpus > 0
                and self.max_node_gpus > 0
                and udf_gpus > self.max_node_gpus
            ):
                return False
            return not (
                udf_memory > 0
                and self.max_node_memory > 0
                and udf_memory > self.max_node_memory
            )
        return any(
            node.can_fit(udf_cpus, udf_gpus, udf_memory)
            for node in self.node_capacities
        )

    def __str__(self) -> str:
        if self.is_kuberay:
            return (
                f"ClusterResources(kuberay, total={self.total_cpus:.1f}cpu/"
                f"{self.total_gpus:.1f}gpu, max_scale={self.max_scale_cpus:.1f}cpu/"
                f"{self.max_scale_gpus:.1f}gpu)"
            )
        return (
            f"ClusterResources(static, total={self.total_cpus:.1f}cpu/"
            f"{self.total_gpus:.1f}gpu, available={self.available_cpus:.1f}cpu/"
            f"{self.available_gpus:.1f}gpu)"
        )


def actor_cpu_thread_count(
    *,
    enable_gpu_pipelining: bool,
    pipelining_num_readers: int,
    has_preprocess: bool,
    intra_applier_concurrency: int,
) -> int:
    """Per-actor CPU multiplier — single source of truth shared by
    ``setup_actor`` and ``calculate_job_resources``. The two MUST agree
    or Ray's lease queue silently wedges on jobs admission accepted
    but actors can't claim.
    """
    if enable_gpu_pipelining:
        if has_preprocess:
            return 1 + int(pipelining_num_readers)
        return 1
    return intra_applier_concurrency


def calculate_job_resources(
    udf: UDF,
    concurrency: int = 8,
    intra_applier_concurrency: int = 1,
    *,
    enable_gpu_pipelining: bool = False,
    pipelining_num_readers: int = 8,
) -> JobResources:
    """
    Calculate total resources needed for a backfill job.

    Parameters
    ----------
    udf : UDF
        The UDF to execute (provides num_cpus, num_gpus, memory)
    concurrency : int
        Number of parallel applier actors
    intra_applier_concurrency : int
        Parallelism within each applier
    enable_gpu_pipelining : bool
        If True, account for in-actor reader/preprocess threads via
        ``actor_cpu_thread_count`` instead of ``intra_applier_concurrency``.
    pipelining_num_readers : int
        Preprocess pool size; only used when pipelining + ``preprocess()``.

    Returns
    -------
    JobResources
        Computed resource requirements
    """
    cpu_threads = actor_cpu_thread_count(
        enable_gpu_pipelining=enable_gpu_pipelining,
        pipelining_num_readers=pipelining_num_readers,
        has_preprocess=udf.has_preprocess(),
        intra_applier_concurrency=intra_applier_concurrency,
    )
    udf_cpus = (udf.num_cpus or 1.0) * cpu_threads
    udf_gpus = udf.num_gpus or 0.0
    udf_memory = (udf.memory or 0) * intra_applier_concurrency

    # Applier actors (main workload)
    applier_cpus = concurrency * udf_cpus
    applier_gpus = concurrency * udf_gpus
    applier_memory = concurrency * udf_memory

    # Worker-side overhead resources. The driver is pinned to the head pod,
    # so only the JobTracker and fragment writers consume worker CPU.
    rc = _get_resource_config()
    overhead_cpus = rc.jobtracker_num_cpus + concurrency * rc.fragment_writer_num_cpus
    overhead_memory = rc.jobtracker_memory + concurrency * rc.fragment_writer_memory

    return JobResources(
        applier_cpus=applier_cpus,
        applier_gpus=applier_gpus,
        applier_memory=applier_memory,
        overhead_cpus=overhead_cpus,
        overhead_memory=overhead_memory,
        concurrency=concurrency,
        udf_cpus=udf_cpus,
        udf_gpus=udf_gpus,
        udf_memory=udf_memory,
    )


def calculate_udtf_job_resources(
    udtf_num_cpus: float = 1.0,
    udtf_num_gpus: float = 0.0,
    udtf_memory: int = 0,
    concurrency: int = 8,
) -> JobResources:
    """Calculate total resources needed for a UDTF refresh job.

    Unlike regular backfill jobs, UDTF jobs have no fragment writers, and the
    driver is pinned to the head pod, so worker-side overhead is just the
    JobTracker.

    Parameters
    ----------
    udtf_num_cpus : float
        CPUs per UDTF actor (default 1.0)
    udtf_num_gpus : float
        GPUs per UDTF actor (default 0.0)
    udtf_memory : int
        Memory (bytes) per UDTF actor (default 0)
    concurrency : int
        Number of parallel UDTF actors

    Returns
    -------
    JobResources
        Computed resource requirements
    """
    applier_cpus = concurrency * udtf_num_cpus
    applier_gpus = concurrency * udtf_num_gpus
    applier_memory = concurrency * udtf_memory

    # No fragment writers for UDTF. The driver is pinned to the head pod, while
    # the JobTracker runs on workers and must be included in admission.
    rc = _get_resource_config()
    overhead_cpus = rc.jobtracker_num_cpus
    overhead_memory = rc.jobtracker_memory

    return JobResources(
        applier_cpus=applier_cpus,
        applier_gpus=applier_gpus,
        applier_memory=applier_memory,
        overhead_cpus=overhead_cpus,
        overhead_memory=overhead_memory,
        concurrency=concurrency,
        udf_cpus=udtf_num_cpus,
        udf_gpus=udtf_num_gpus,
        udf_memory=udtf_memory,
    )


def validate_udtf_admission(
    udtf_num_cpus: float = 1.0,
    udtf_num_gpus: float = 0.0,
    udtf_memory: int = 0,
    concurrency: int = 8,
    *,
    check: bool | None = None,
    strict: bool | None = None,
) -> None:
    """Validate cluster resources for a UDTF refresh job.

    Mirrors [`validate_admission`][validate_admission] but accepts raw resource values
    instead of a [`UDF`][UDF] object.

    Parameters
    ----------
    udtf_num_cpus, udtf_num_gpus, udtf_memory
        Per-actor resource requirements
    concurrency : int
        Number of parallel UDTF actors
    check : bool | None
        If True, run admission control. If False, skip. If None, use config.
    strict : bool | None
        If True, raise on rejection. If False, only log. If None, use
        AdmissionConfig.strict (default False: warn and proceed).

    Raises
    ------
    ResourcesUnavailableError
        If strict=True and resources are insufficient
    """
    config = AdmissionConfig.get()

    if check is None:
        check = config.check
    if not check:
        _LOG.debug("UDTF admission control disabled")
        return

    if not ray.is_initialized():
        _LOG.debug("UDTF admission control skipped: Ray not initialized")
        return

    if strict is None:
        strict = config.strict

    job_resources = calculate_udtf_job_resources(
        udtf_num_cpus, udtf_num_gpus, udtf_memory, concurrency
    )

    kind = _detect_cluster_kind()
    if kind is ClusterKind.KUBERAY:
        cluster_resources = get_kuberay_cluster_resources()
    else:
        cluster_resources = get_cluster_resources()

    if cluster_resources is None:
        if strict:
            raise ResourcesUnavailableError(
                "UDTF admission control could not query cluster resources "
                "(timeout or error). Cannot verify that cluster has sufficient "
                "resources for this job. Set _admission_strict=False to skip this "
                "check, or increase the timeout via GENEVA_ADMISSION__TIMEOUT."
            )
        _LOG.warning(
            "UDTF admission control skipped: could not query cluster resources"
        )
        return

    _LOG.debug("UDTF admission check: %s vs %s", job_resources, cluster_resources)

    decision, message = check_admission(job_resources, cluster_resources)

    if decision == AdmissionDecision.REJECT:
        if strict:
            raise ResourcesUnavailableError(message)
        else:
            _warn_admission("UDTF admission control", message, kind)
    elif decision == AdmissionDecision.ALLOW_WITH_WARNING:
        _LOG.warning("UDTF admission control: %s", message)
    else:
        _LOG.debug("UDTF admission control: %s", message)


def get_cluster_resources() -> ClusterResources | None:
    """
    Query current cluster resources from Ray.

    Returns
    -------
    ClusterResources | None
        Current cluster capacity and availability, or None if query timed out.
    """
    nodes_result = _call_with_timeout(ray.nodes)
    if nodes_result is None:
        return None

    nodes = [n for n in nodes_result if n.get("Alive")]

    total_cpus = sum(n["Resources"].get("CPU", 0) for n in nodes)
    total_gpus = sum(n["Resources"].get("GPU", 0) for n in nodes)
    total_memory = sum(n["Resources"].get("memory", 0) for n in nodes)

    # Collect per-node resources (excluding head node which has 0 CPUs)
    # This is used to check if a single UDF can fit on any node
    worker_nodes = [n for n in nodes if n["Resources"].get("CPU", 0) > 0]

    # Build list of node capacities for heterogeneous cluster support
    node_capacities = [
        NodeCapacity(
            cpus=n["Resources"].get("CPU", 0.0),
            gpus=n["Resources"].get("GPU", 0.0),
            memory=int(n["Resources"].get("memory", 0)),
        )
        for n in worker_nodes
    ]

    # Also compute max per-node for backward compatibility
    max_node_cpus = max((nc.cpus for nc in node_capacities), default=0.0)
    max_node_gpus = max((nc.gpus for nc in node_capacities), default=0.0)
    max_node_memory = max((nc.memory for nc in node_capacities), default=0)

    available = _call_with_timeout(ray.available_resources) or {}

    is_kuberay = _is_kuberay_cluster()

    return ClusterResources(
        total_cpus=total_cpus,
        total_gpus=total_gpus,
        total_memory=int(total_memory),
        available_cpus=available.get("CPU", 0),
        available_gpus=available.get("GPU", 0),
        available_memory=int(available.get("memory", 0)),
        is_kuberay=is_kuberay,
        node_capacities=node_capacities if node_capacities else None,
        max_node_cpus=max_node_cpus,
        max_node_gpus=max_node_gpus,
        max_node_memory=max_node_memory,
    )


def get_kuberay_cluster_resources(
    namespace: str | None = None,
    cluster_name: str | None = None,
) -> ClusterResources | None:
    """
    Query KubeRay cluster resources including max scale capacity.

    Parameters
    ----------
    namespace : str, optional
        Kubernetes namespace. Resolution order: parameter > Geneva context > "default"
    cluster_name : str, optional
        RayCluster name. Resolution order: parameter > Geneva context

    Returns
    -------
    ClusterResources | None
        Current and max-scale cluster capacity, or None if query timed out.
    """
    from geneva.runners.kuberay.client import KuberayClients

    # Get current resources from Ray
    base = get_cluster_resources()
    if base is None:
        return None
    base.is_kuberay = True

    # Priority: explicit params > Geneva context
    ctx = get_current_context()
    if ctx is not None:
        namespace = namespace or ctx.namespace
        cluster_name = cluster_name or ctx.name

    # Default namespace if not specified
    namespace = namespace or "default"

    if not cluster_name:
        _LOG.warning(
            "Cluster name not available (checked: parameter, Geneva context). "
            "Cannot query max scale capacity."
        )
        return None

    try:
        # Reuse clients from context if available (avoids recreating K8s API clients)
        clients = (
            ctx.clients
            if ctx is not None and isinstance(ctx, RayCluster)
            else KuberayClients()
        )
        cluster_obj = clients.custom_api.get_namespaced_custom_object(
            group="ray.io",
            version="v1",
            namespace=namespace,
            plural="rayclusters",
            name=cluster_name,
        )

        # Cast to dict since K8s API returns dynamic type
        cluster: dict[str, Any] = cluster_obj if isinstance(cluster_obj, dict) else {}
        spec: dict[str, Any] = cluster.get("spec", {})
        (
            max_cpus,
            max_gpus,
            max_memory,
            worker_group_capacities,
        ) = _parse_cluster_max_capacity(spec)

        base.max_scale_cpus = max_cpus
        base.max_scale_gpus = max_gpus
        base.max_scale_memory = max_memory

        # Merge worker group capacities with current node capacities
        # Use spec-based capacities since they define what the cluster CAN scale to
        if worker_group_capacities:
            base.node_capacities = worker_group_capacities
            # Also update legacy max values for backward compatibility
            base.max_node_cpus = max(nc.cpus for nc in worker_group_capacities)
            base.max_node_gpus = max(
                (nc.gpus for nc in worker_group_capacities), default=0.0
            )
            base.max_node_memory = max(nc.memory for nc in worker_group_capacities)

    except Exception as e:
        _LOG.warning(f"Failed to query KubeRay cluster capacity: {e}")
        return None

    return base


def _parse_cluster_max_capacity(
    spec: dict[str, Any],
) -> tuple[float, float, int, list[NodeCapacity]]:
    """Parse max capacity from RayCluster spec.

    Returns
    -------
    tuple
        (max_cpus, max_gpus, max_memory, worker_group_capacities)
        worker_group_capacities contains a NodeCapacity for each worker group type
    """
    max_cpus = 0.0
    max_gpus = 0.0
    max_memory = 0

    # Collect per-worker-group capacities for heterogeneous cluster support
    worker_group_capacities: list[NodeCapacity] = []

    # Head node resources
    head_spec = spec.get("headGroupSpec", {})
    head_res = _parse_ray_start_params(head_spec)
    max_cpus += head_res.get("CPU", 0)
    max_gpus += head_res.get("GPU", 0)
    max_memory += head_res.get("memory", 0)

    # Worker groups at max scale
    for wg in spec.get("workerGroupSpecs", []):
        max_replicas = wg.get("maxReplicas", wg.get("replicas", 1))
        wg_res = _parse_ray_start_params(wg)

        wg_cpus = wg_res.get("CPU", 0)
        wg_gpus = wg_res.get("GPU", 0)
        wg_memory = int(wg_res.get("memory", 0))

        max_cpus += max_replicas * wg_cpus
        max_gpus += max_replicas * wg_gpus
        max_memory += max_replicas * wg_memory

        # Store worker group capacity for per-node feasibility check
        if wg_cpus > 0 or wg_gpus > 0:  # Only include groups with compute resources
            worker_group_capacities.append(
                NodeCapacity(cpus=wg_cpus, gpus=wg_gpus, memory=wg_memory)
            )

    return (max_cpus, max_gpus, int(max_memory), worker_group_capacities)


def _parse_ray_start_params(group_spec: dict[str, Any]) -> dict[str, float]:
    """Extract resources from rayStartParams and container specs.

    Resources can be specified in two places in a KubeRay group spec:
    1. rayStartParams: Direct Ray resource flags (num-cpus, num-gpus)
    2. Container resources: K8s resource requests/limits (memory, GPU devices)
    """
    import contextlib

    resources: dict[str, float] = {}

    # Parse explicit Ray resource flags from rayStartParams
    params = group_spec.get("rayStartParams", {})

    if "num-cpus" in params:
        with contextlib.suppress(ValueError, TypeError):
            resources["CPU"] = float(params["num-cpus"])

    if "num-gpus" in params:
        with contextlib.suppress(ValueError, TypeError):
            resources["GPU"] = float(params["num-gpus"])

    # Parse container resources from the pod template spec
    # Structure: group_spec -> template -> spec -> containers[] -> resources
    template = group_spec.get("template", {})
    containers = template.get("spec", {}).get("containers", [])

    for container in containers:
        res = container.get("resources", {})

        # GPU devices are specified in limits (vendor-specific keys)
        limits = res.get("limits", {})
        for gpu_key in ("nvidia.com/gpu", "amd.com/gpu", "intel.com/gpu"):
            if gpu_key in limits:
                with contextlib.suppress(ValueError, TypeError):
                    resources["GPU"] = resources.get("GPU", 0) + float(limits[gpu_key])

        # Memory is typically specified in requests
        requests = res.get("requests", {})
        if "memory" in requests:
            mem = int(parse_quantity(requests["memory"]))
            resources["memory"] = resources.get("memory", 0) + mem

    return resources


def _is_kuberay_cluster() -> bool:
    """Check if connected to a Geneva-managed KubeRay cluster.

    Detection methods (in order of preference):
    1. Check for geneva_autoscaling custom resource in cluster resources
    2. Check for active Geneva context (RayCluster)
    """
    from geneva.utils.ray import GENEVA_AUTOSCALING_RESOURCE

    # Method 1: Check for Geneva autoscaling custom resource (definitive)
    if ray.is_initialized():
        resources = _call_with_timeout(ray.cluster_resources)
        if resources and GENEVA_AUTOSCALING_RESOURCE in resources:
            return True

    # Method 2: Check for active Geneva context
    ctx = get_current_context()
    # Make sure it's a RayCluster, not a LocalRayContext
    return ctx is not None and isinstance(ctx, RayCluster)


def check_admission(
    job_resources: JobResources,
    cluster_resources: ClusterResources,
) -> tuple[AdmissionDecision, str]:
    """
    Check if a job can run on the cluster.

    Parameters
    ----------
    job_resources : JobResources
        Resources required by the job
    cluster_resources : ClusterResources
        Available cluster resources

    Returns
    -------
    tuple[AdmissionDecision, str]
        Decision and explanation message
    """
    # For KubeRay, check against max scale capacity
    if cluster_resources.is_kuberay:
        return _check_kuberay_admission(job_resources, cluster_resources)

    return _check_static_admission(job_resources, cluster_resources)


def _check_static_admission(
    job: JobResources,
    cluster: ClusterResources,
) -> tuple[AdmissionDecision, str]:
    """Check admission for static Ray cluster."""

    # GPU job on CPU-only cluster
    if job.total_gpus > 0 and cluster.total_gpus == 0:
        return (
            AdmissionDecision.REJECT,
            f"Job requires {job.total_gpus:.1f} GPUs but cluster has none. "
            "Either remove GPU requirement from UDF (num_gpus=0) or add GPU nodes.",
        )

    # Check single UDF fits on at least one node (combined resource check)
    # This handles heterogeneous clusters correctly by checking if ANY single node
    # can satisfy ALL UDF requirements simultaneously
    if not cluster.any_node_can_fit(job.udf_cpus, job.udf_gpus, job.udf_memory):
        # Build a descriptive error message
        reqs = []
        if job.udf_cpus > 0:
            reqs.append(f"{job.udf_cpus:.1f} CPUs")
        if job.udf_gpus > 0:
            reqs.append(f"{job.udf_gpus:.1f} GPUs")
        if job.udf_memory > 0:
            reqs.append(f"{job.udf_memory / 1e9:.1f}GB memory")
        return (
            AdmissionDecision.REJECT,
            f"UDF requires {' + '.join(reqs)} but no single node can satisfy all "
            "requirements. Reduce UDF resource requirements or add nodes with "
            "sufficient combined resources.",
        )

    # More GPUs than cluster has
    if job.total_gpus > cluster.total_gpus:
        max_conc = int(cluster.total_gpus / job.udf_gpus) if job.udf_gpus else 0
        return (
            AdmissionDecision.REJECT,
            f"Job requires {job.total_gpus:.1f} GPUs but cluster only has "
            f"{cluster.total_gpus:.1f}. Reduce concurrency to {max_conc} or fewer.",
        )

    # More CPUs than cluster has
    if job.total_cpus > cluster.total_cpus:
        return (
            AdmissionDecision.REJECT,
            f"Job requires {job.total_cpus:.1f} CPUs but cluster only has "
            f"{cluster.total_cpus:.1f}. Reduce concurrency or UDF num_cpus.",
        )

    # More memory than cluster has
    if (
        job.total_memory > 0
        and cluster.total_memory > 0
        and job.total_memory > cluster.total_memory
    ):
        return (
            AdmissionDecision.REJECT,
            f"Job requires {job.total_memory / 1e9:.1f}GB memory but cluster "
            f"only has {cluster.total_memory / 1e9:.1f}GB. Reduce concurrency, "
            "reduce UDF memory, or add more nodes to the cluster.",
        )

    # Check available resources (warn if busy)
    warnings = []

    if job.total_gpus > 0 and job.total_gpus > cluster.available_gpus:
        warnings.append(
            f"needs {job.total_gpus:.1f} GPUs but only "
            f"{cluster.available_gpus:.1f} currently available"
        )

    if job.total_cpus > cluster.available_cpus:
        warnings.append(
            f"needs {job.total_cpus:.1f} CPUs but only "
            f"{cluster.available_cpus:.1f} currently available"
        )

    if warnings:
        return (
            AdmissionDecision.ALLOW_WITH_WARNING,
            "Job may wait for resources: " + "; ".join(warnings),
        )

    return (AdmissionDecision.ALLOW, "Resources available")


def _check_kuberay_admission(
    job: JobResources,
    cluster: ClusterResources,
) -> tuple[AdmissionDecision, str]:
    """Check admission for KubeRay cluster."""

    max_gpus = (
        cluster.max_scale_gpus
        if cluster.max_scale_gpus is not None
        else cluster.total_gpus
    )
    max_cpus = (
        cluster.max_scale_cpus
        if cluster.max_scale_cpus is not None
        else cluster.total_cpus
    )

    # GPU job on non-GPU cluster
    if job.total_gpus > 0 and max_gpus == 0:
        return (
            AdmissionDecision.REJECT,
            f"Job requires {job.total_gpus:.1f} GPUs but cluster has no GPU worker "
            "groups configured. Add a GPU worker group to the RayCluster spec.",
        )

    # Check single UDF fits on at least one worker group (combined resource check)
    # This handles heterogeneous clusters correctly by checking if ANY worker group
    # can satisfy ALL UDF requirements simultaneously
    if not cluster.any_node_can_fit(job.udf_cpus, job.udf_gpus, job.udf_memory):
        # Build a descriptive error message
        reqs = []
        if job.udf_cpus > 0:
            reqs.append(f"{job.udf_cpus:.1f} CPUs")
        if job.udf_gpus > 0:
            reqs.append(f"{job.udf_gpus:.1f} GPUs")
        if job.udf_memory > 0:
            reqs.append(f"{job.udf_memory / 1e9:.1f}GB memory")
        return (
            AdmissionDecision.REJECT,
            f"UDF requires {' + '.join(reqs)} but no worker group can satisfy all "
            "requirements. Reduce UDF resource requirements or configure worker "
            "nodes with sufficient combined resources.",
        )

    # More GPUs than max scale allows
    if job.total_gpus > max_gpus:
        max_concurrency = int(max_gpus / job.udf_gpus) if job.udf_gpus else 0
        return (
            AdmissionDecision.REJECT,
            f"Job requires {job.total_gpus:.1f} GPUs but cluster can only scale to "
            f"{max_gpus:.1f} GPUs (maxReplicas limit). Reduce concurrency to "
            f"{max_concurrency} or increase maxReplicas for GPU worker group.",
        )

    # More CPUs than max scale allows
    if job.total_cpus > max_cpus:
        return (
            AdmissionDecision.REJECT,
            f"Job requires {job.total_cpus:.1f} CPUs but cluster can only scale to "
            f"{max_cpus:.1f} CPUs. Reduce concurrency or increase maxReplicas.",
        )

    # More memory than max scale allows
    max_memory = (
        cluster.max_scale_memory
        if cluster.max_scale_memory is not None
        else cluster.total_memory
    )
    if job.total_memory > 0 and max_memory > 0 and job.total_memory > max_memory:
        return (
            AdmissionDecision.REJECT,
            f"Job requires {job.total_memory / 1e9:.1f}GB memory but cluster "
            f"can only scale to {max_memory / 1e9:.1f}GB. Reduce concurrency "
            "or increase maxReplicas.",
        )

    # Will need to scale up
    if job.total_gpus > cluster.total_gpus or job.total_cpus > cluster.total_cpus:
        return (
            AdmissionDecision.ALLOW_WITH_WARNING,
            "Cluster will need to scale up. Job may wait for nodes to provision.",
        )

    return (AdmissionDecision.ALLOW, "Resources available")


def validate_admission(
    udf: UDF,
    concurrency: int = 8,
    intra_applier_concurrency: int = 1,
    *,
    enable_gpu_pipelining: bool = False,
    pipelining_num_readers: int = 8,
    check: bool | None = None,
    strict: bool | None = None,
    kuberay_namespace: str | None = None,
    kuberay_cluster_name: str | None = None,
) -> None:
    """
    Validate that cluster has sufficient resources for a job.

    This is the main entry point for admission control.

    Parameters
    ----------
    udf : UDF
        The UDF to execute
    concurrency : int
        Number of parallel applier actors
    intra_applier_concurrency : int
        Parallelism within each applier
    enable_gpu_pipelining : bool
        If True, account for the extra reader/preprocess threads each
        actor spawns. See ``calculate_job_resources`` for details.
    pipelining_num_readers : int
        Preprocess pool size when GPU pipelining + ``udf.preprocess()``
        are both present.
    check : bool | None
        If True, run admission control. If False, skip. If None, use
        AdmissionConfig.check (configurable via GENEVA_ADMISSION__CHECK env var).
    strict : bool | None
        If True, raise exception on rejection. If False, only log warnings.
        If None, use AdmissionConfig.strict (default False, configurable via
        GENEVA_ADMISSION__STRICT env var).
    kuberay_namespace : str, optional
        Kubernetes namespace for KubeRay clusters
    kuberay_cluster_name : str, optional
        RayCluster name for KubeRay clusters

    Raises
    ------
    ResourcesUnavailableError
        If strict=True and resources are insufficient
    """
    config = AdmissionConfig.get()

    # Resolve check from config if None (API param takes precedence)
    if check is None:
        check = config.check

    if not check:
        _LOG.debug("Admission control disabled")
        return

    # Check if Ray is initialized
    if not ray.is_initialized():
        _LOG.debug("Admission control skipped: Ray not initialized")
        return

    # Resolve strict from config if None (API param takes precedence)
    if strict is None:
        strict = config.strict

    job_resources = calculate_job_resources(
        udf,
        concurrency,
        intra_applier_concurrency,
        enable_gpu_pipelining=enable_gpu_pipelining,
        pipelining_num_readers=pipelining_num_readers,
    )

    kind = _detect_cluster_kind()
    if kind is ClusterKind.KUBERAY:
        cluster_resources = get_kuberay_cluster_resources(
            namespace=kuberay_namespace,
            cluster_name=kuberay_cluster_name,
        )
    else:
        cluster_resources = get_cluster_resources()

    # Could not query cluster resources (timeout/error)
    if cluster_resources is None:
        if strict:
            raise ResourcesUnavailableError(
                "Admission control could not query cluster resources "
                "(timeout or error). Cannot verify that cluster has sufficient "
                "resources for this job. Set _admission_strict=False to skip "
                "this check, or increase the timeout via "
                "GENEVA_ADMISSION__TIMEOUT."
            )
        _LOG.warning("Admission control skipped: could not query cluster resources")
        return

    _LOG.debug(f"Admission check: {job_resources} vs {cluster_resources}")

    decision, message = check_admission(job_resources, cluster_resources)

    if decision == AdmissionDecision.REJECT:
        if strict:
            raise ResourcesUnavailableError(message)
        else:
            _warn_admission("Admission control", message, kind)
    elif decision == AdmissionDecision.ALLOW_WITH_WARNING:
        _LOG.warning(f"Admission control: {message}")
    else:
        _LOG.debug(f"Admission control: {message}")
