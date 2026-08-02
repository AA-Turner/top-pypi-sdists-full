# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from __future__ import annotations

import copy
import logging
import platform
import sys
from typing import TYPE_CHECKING

import ray

from geneva.cluster import GenevaClusterType, K8sConfigMethod
from geneva.constants import DEFAULT_K8S_NS

if TYPE_CHECKING:
    from typing import Self
from geneva.cluster.mgr import (
    GenevaCluster,
    HeadGroupConfig,
    KubeRayConfig,
    WorkerGroupConfig,
)
from geneva.utils.ray import (
    DEFAULT_MAX_WORKER_REPLICAS,
    GENEVA_RAY_CPU_NODE,
    GENEVA_RAY_GPU_NODE,
    GENEVA_RAY_HEAD_NODE,
    get_ray_image,
    size_to_bytes,
)

_LOG = logging.getLogger(__name__)

# Memory thresholds for validation (in bytes)
MEMORY_LARGE_THRESHOLD = 100 * (1000**3)  # 100 GB - likely exceeds node capacity
MEMORY_PER_CPU_THRESHOLD = 16 * (1024**3)  # 16 GiB per CPU - unusual ratio
MEMORY_GPU_MIN = 4 * (1024**3)  # 4 GiB minimum for GPU workers


# =============================================================================
# Type-Safe Builders
# =============================================================================


class _WorkerResourceMixin:
    """Shared resource configuration for KubeRay worker builders.

    This mixin provides common methods for configuring worker group resources
    like CPUs, memory, service accounts, and pod scheduling options.
    """

    def __init__(self) -> None:
        self._image: str | None = None  # None means use default
        self._num_cpus: int = 4
        self._memory: str = "8Gi"
        self._service_account: str = "geneva-service-account"
        self._node_selector: dict[str, str] = {}
        self._labels: dict[str, str] = {}
        self._tolerations: list[dict[str, str]] = []
        self._replicas: int = 1
        self._min_replicas: int = 0
        self._max_replicas: int = DEFAULT_MAX_WORKER_REPLICAS
        self._idle_timeout_seconds: int = 60
        self._env_vars: dict[str, str] = {}

    def image(self, image: str) -> Self:
        """Set the container image."""
        self._image = image
        return self  # type: ignore[return-value]

    def cpus(self, cpus: int) -> Self:
        """Set the number of CPUs."""
        self._num_cpus = cpus
        return self  # type: ignore[return-value]

    def memory(self, memory: str) -> Self:
        """Set the memory allocation (e.g., '8Gi', '16Gi')."""
        self._memory = memory
        return self  # type: ignore[return-value]

    def service_account(self, service_account: str) -> Self:
        """Set the Kubernetes service account."""
        self._service_account = service_account
        return self  # type: ignore[return-value]

    def node_selector(self, node_selector: dict[str, str]) -> Self:
        """Set the node selector for pod placement."""
        self._node_selector = node_selector.copy()
        return self  # type: ignore[return-value]

    def labels(self, labels: dict[str, str]) -> Self:
        """Set the pod labels."""
        self._labels = labels.copy()
        return self  # type: ignore[return-value]

    def tolerations(self, tolerations: list[dict[str, str]]) -> Self:
        """Set the pod tolerations."""
        self._tolerations = tolerations.copy()
        return self  # type: ignore[return-value]

    def replicas(self, replicas: int) -> Self:
        """Set the number of replicas."""
        self._replicas = replicas
        return self  # type: ignore[return-value]

    def min_replicas(self, min_replicas: int) -> Self:
        """Set the minimum number of replicas for autoscaling."""
        self._min_replicas = min_replicas
        return self  # type: ignore[return-value]

    def max_replicas(self, max_replicas: int) -> Self:
        """Set the maximum number of replicas for autoscaling."""
        self._max_replicas = max_replicas
        return self  # type: ignore[return-value]

    def idle_timeout_seconds(self, seconds: int) -> Self:
        """Set the idle timeout in seconds for autoscaling down workers."""
        self._idle_timeout_seconds = seconds
        return self  # type: ignore[return-value]

    def add_label(self, key: str, value: str) -> Self:
        """Add a single label."""
        self._labels[key] = value
        return self  # type: ignore[return-value]

    def add_toleration(
        self, key: str, operator: str = "Equal", value: str = "", effect: str = ""
    ) -> Self:
        """Add a single toleration."""
        toleration = {"key": key, "operator": operator}
        if value:
            toleration["value"] = value
        if effect:
            toleration["effect"] = effect
        self._tolerations.append(toleration)
        return self  # type: ignore[return-value]

    def env_vars(self, env_vars: dict[str, str]) -> Self:
        """Set environment variables for the worker containers.

        These are injected into the Kubernetes container spec alongside
        Geneva-managed env vars (workload identity, Ray config, etc.).
        """
        self._env_vars = env_vars.copy()
        return self  # type: ignore[return-value]

    def add_env_var(self, key: str, value: str) -> Self:
        """Add a single environment variable."""
        self._env_vars[key] = value
        return self  # type: ignore[return-value]


class CpuWorkerBuilder(_WorkerResourceMixin):
    """Builder for CPU-only worker groups in KubeRay clusters.

    This builder does NOT have a gpus() method - use GpuWorkerBuilder for GPU workers.

    Examples
    --------

        worker = (
            CpuWorkerBuilder()
            .cpus(8)
            .memory("16Gi")
            .replicas(2)
            .build()
        )
    """

    def __init__(self) -> None:
        super().__init__()
        self._name: str | None = None
        self._node_selector = {GENEVA_RAY_CPU_NODE: "true"}

    def name(self, name: str) -> CpuWorkerBuilder:
        """Set the worker group name. Must be unique within the cluster."""
        self._name = name
        return self

    def build(self) -> WorkerGroupConfig:
        """Build the WorkerGroupConfig."""
        name = self._name or "cpu"
        image = self._image if self._image is not None else default_image(gpu=False)

        return WorkerGroupConfig(
            name=name,
            service_account=self._service_account,
            num_cpus=self._num_cpus,
            memory=self._memory,
            image=image,
            num_gpus=0,  # Always 0 for CPU workers
            node_selector=self._node_selector,
            labels=self._labels,
            tolerations=self._tolerations,
            replicas=self._replicas,
            min_replicas=self._min_replicas,
            max_replicas=self._max_replicas,
            idle_timeout_seconds=self._idle_timeout_seconds,
            env_vars=self._env_vars,
        )


class GpuWorkerBuilder(_WorkerResourceMixin):
    """Builder for GPU worker groups in KubeRay clusters.

    Includes validation:

    - Minimum 4GiB memory for GPU workers (raises ValueError)
    - Warning for memory > 100GB (may exceed node capacity)
    - Warning for high memory/CPU ratio (> 16 GiB/CPU)

    Examples
    --------

        worker = (
            GpuWorkerBuilder()
            .gpus(4)
            .cpus(8)
            .memory("64Gi")
            .build()
        )
    """

    def __init__(self) -> None:
        super().__init__()
        self._name: str | None = None
        self._num_gpus: int = 1
        self._memory = "16Gi"  # Higher default for GPU
        self._num_cpus = 8  # Higher default for GPU
        self._node_selector = {GENEVA_RAY_GPU_NODE: "true"}

    def name(self, name: str) -> GpuWorkerBuilder:
        """Set the worker group name. Must be unique within the cluster."""
        self._name = name
        return self

    def gpus(self, gpus: int) -> GpuWorkerBuilder:
        """Set the number of GPUs (must be >= 1)."""
        if gpus < 1:
            raise ValueError("GPU worker must have at least 1 GPU")
        self._num_gpus = gpus
        return self

    def build(self) -> WorkerGroupConfig:
        """Build the WorkerGroupConfig with memory validation."""
        memory_bytes = size_to_bytes(self._memory)

        # ERROR: GPU workers need minimum memory
        if memory_bytes < MEMORY_GPU_MIN:
            raise ValueError(
                f"GPU workers require at least 4GiB memory, got {self._memory}"
            )

        # WARNING: May exceed node capacity
        if memory_bytes > MEMORY_LARGE_THRESHOLD:
            _LOG.warning(
                f"Memory {self._memory} may exceed K8s node capacity. "
                f"Pods may stay Pending if no node can satisfy this request."
            )

        # WARNING: Unusual ratio
        if self._num_cpus > 0:
            ratio = memory_bytes / self._num_cpus
            if ratio > MEMORY_PER_CPU_THRESHOLD:
                _LOG.warning(
                    f"High memory/CPU ratio ({ratio / (1024**3):.1f} GiB/CPU). "
                    f"Verify nodes have sufficient memory."
                )

        name = self._name or "gpu"
        image = self._image if self._image is not None else default_image(gpu=True)

        return WorkerGroupConfig(
            name=name,
            service_account=self._service_account,
            num_cpus=self._num_cpus,
            memory=self._memory,
            image=image,
            num_gpus=self._num_gpus,
            node_selector=self._node_selector,
            labels=self._labels,
            tolerations=self._tolerations,
            replicas=self._replicas,
            min_replicas=self._min_replicas,
            max_replicas=self._max_replicas,
            idle_timeout_seconds=self._idle_timeout_seconds,
            env_vars=self._env_vars,
        )


class KubeRayClusterBuilder:
    """Type-safe builder for KubeRay clusters deployed on Kubernetes.

    Use this builder for clusters that will be deployed via KubeRay.
    For local development, use LocalRayClusterBuilder instead.

    Examples
    --------

        cluster = (
            KubeRayClusterBuilder.create("my-cluster")
            .namespace("ml-team")
            .add_worker_group(
                KubeRayClusterBuilder.gpu_worker(4)
                .memory("64Gi")
                .build()
            )
            .add_worker_group(
                KubeRayClusterBuilder.cpu_worker()
                .cpus(16)
                .memory("32Gi")
                .build()
            )
            .build()
        )
    """

    def __init__(self) -> None:
        self._name: str | None = None
        self._namespace: str = DEFAULT_K8S_NS
        self._config_method: K8sConfigMethod = K8sConfigMethod.LOCAL
        self._use_portforwarding: bool = True
        self._aws_region: str | None = None
        self._aws_role_name: str | None = None
        self._ray_init_kwargs: dict = {}
        self._worker_groups: list[WorkerGroupConfig] = []

        # Head group defaults
        self._head_image: str | None = None
        self._head_cpus: int = 4
        self._head_memory: str = "8Gi"
        self._head_gpus: int = 0
        self._head_service_account: str = "geneva-service-account"
        self._head_node_selector: dict[str, str] = {GENEVA_RAY_HEAD_NODE: "true"}
        self._head_labels: dict[str, str] = {}
        self._head_tolerations: list[dict[str, str]] = []
        self._head_env_vars: dict[str, str] = {}

    def name(self, name: str) -> KubeRayClusterBuilder:
        """Set the cluster name."""
        self._name = name
        return self

    def namespace(self, namespace: str) -> KubeRayClusterBuilder:
        """Set the Kubernetes namespace."""
        self._namespace = namespace
        return self

    def config_method(self, method: K8sConfigMethod) -> KubeRayClusterBuilder:
        """Set the Kubernetes config method."""
        self._config_method = method
        return self

    def portforwarding(self, enabled: bool = True) -> KubeRayClusterBuilder:
        """Enable or disable port forwarding."""
        self._use_portforwarding = enabled
        return self

    def aws_config(
        self, region: str | None = None, role_name: str | None = None
    ) -> KubeRayClusterBuilder:
        """Configure AWS settings."""
        self._aws_region = region
        self._aws_role_name = role_name
        return self

    def ray_init_kwargs(self, kwargs: dict) -> KubeRayClusterBuilder:
        """Set arbitrary kwargs to pass to ray.init() when starting the cluster,
        such as env vars.
        Examples
        --------

            .ray_init_kwargs({
                "runtime_env": {
                    "env_vars": {
                        "MY_VAR": "value",
                        "AWS_ACCESS_KEY_ID": os.environ["AWS_ACCESS_KEY_ID"]
                    },
                },
            })
        """
        self._ray_init_kwargs = copy.deepcopy(kwargs)
        return self

    def head_group(
        self,
        *,
        image: str | None = None,
        cpus: int | None = None,
        memory: str | None = None,
        gpus: int | None = None,
        service_account: str | None = None,
        node_selector: dict[str, str] | None = None,
        labels: dict[str, str] | None = None,
        tolerations: list[dict[str, str]] | None = None,
        env_vars: dict[str, str] | None = None,
    ) -> KubeRayClusterBuilder:
        """Configure the head group with optional parameters."""
        if image is not None:
            self._head_image = image
        if cpus is not None:
            self._head_cpus = cpus
        if memory is not None:
            self._head_memory = memory
        if gpus is not None:
            self._head_gpus = gpus
        if service_account is not None:
            self._head_service_account = service_account
        if node_selector is not None:
            self._head_node_selector = node_selector
        if labels is not None:
            self._head_labels = labels
        if tolerations is not None:
            self._head_tolerations = tolerations
        if env_vars is not None:
            self._head_env_vars = env_vars.copy()
        return self

    def add_worker_group(self, worker: WorkerGroupConfig) -> KubeRayClusterBuilder:
        """Add a worker group configuration."""
        self._worker_groups.append(worker)
        return self

    def build(self) -> GenevaCluster:
        """Build the GenevaCluster with the configured settings."""
        if self._name is None:
            raise ValueError("Cluster name is required. Use .name() to set it.")

        # Build head group config
        head_image = (
            self._head_image
            if self._head_image is not None
            else default_image(gpu=False)
        )
        head_group = HeadGroupConfig(
            service_account=self._head_service_account,
            num_cpus=self._head_cpus,
            memory=self._head_memory,
            image=head_image,
            num_gpus=self._head_gpus,
            node_selector=self._head_node_selector,
            labels=self._head_labels,
            tolerations=self._head_tolerations,
            env_vars=self._head_env_vars,
        )

        # Use worker group configs directly
        worker_groups = self._worker_groups.copy()

        # If no worker groups were explicitly added, add a default CPU worker
        if not worker_groups:
            worker_groups.append(
                WorkerGroupConfig(
                    name="cpu",
                    service_account=self._head_service_account,
                    num_cpus=4,
                    memory="8Gi",
                    image=default_image(gpu=False),
                    num_gpus=0,
                    node_selector={GENEVA_RAY_CPU_NODE: "true"},
                    labels={},
                    tolerations=[],
                )
            )

        # Ensure unique worker group names by appending index for duplicates
        seen_names: dict[str, int] = {}
        for wg in worker_groups:
            base_name = wg.name or ("gpu" if wg.num_gpus > 0 else "cpu")
            if base_name in seen_names:
                seen_names[base_name] += 1
                new_name = f"{base_name}-{seen_names[base_name]}"
                _LOG.warning(
                    f"Duplicate worker group name '{base_name}' detected. "
                    f"Renaming to '{new_name}' to ensure uniqueness."
                )
                wg.name = new_name
            else:
                seen_names[base_name] = 0
                wg.name = base_name

        kuberay_config = KubeRayConfig(
            namespace=self._namespace,
            head_group=head_group,
            worker_groups=worker_groups,
            config_method=self._config_method,
            use_portforwarding=self._use_portforwarding,
            aws_region=self._aws_region,
            aws_role_name=self._aws_role_name,
            ray_init_kwargs=self._ray_init_kwargs,
        )

        return GenevaCluster(
            cluster_type=GenevaClusterType.KUBE_RAY,
            name=self._name,
            ray_address=None,
            kuberay=kuberay_config,
        )

    @classmethod
    def create(cls, name: str) -> KubeRayClusterBuilder:
        """Create a new builder with the given cluster name."""
        return cls().name(name)

    @staticmethod
    def cpu_worker() -> CpuWorkerBuilder:
        """Create a CPU worker builder.

        CPU workers do not have a gpus() method - use gpu_worker() for GPU workers.

        Examples
        --------

            cluster = (
                KubeRayClusterBuilder.create("test")
                .add_worker_group(KubeRayClusterBuilder.cpu_worker().cpus(8).build())
                .build()
            )
        """
        return CpuWorkerBuilder()

    @staticmethod
    def gpu_worker(gpus: int = 1) -> GpuWorkerBuilder:
        """Create a GPU worker builder.

        GPU workers have memory validation:

        - Minimum 4GiB memory required (raises ValueError)
        - Warning for memory > 100GB (may exceed node capacity)

        Examples
        --------

            cluster = (
                KubeRayClusterBuilder.create("test")
                .add_worker_group(KubeRayClusterBuilder.gpu_worker(4).memory("64Gi").build())
                .build()
            )
        """
        return GpuWorkerBuilder().gpus(gpus)


class LocalRayClusterBuilder:
    """Builder for local Ray clusters.

    Resources are managed by the local Ray runtime, so this builder
    does NOT have memory(), cpus(), or worker configuration methods.

    Examples
    --------

        cluster = LocalRayClusterBuilder.create("local-dev").build()
    """

    def __init__(self) -> None:
        self._name: str | None = None

    def name(self, name: str) -> LocalRayClusterBuilder:
        """Set the cluster name."""
        self._name = name
        return self

    def build(self) -> GenevaCluster:
        """Build the GenevaCluster for local Ray."""
        if self._name is None:
            raise ValueError("Cluster name is required. Use .name() to set it.")

        return GenevaCluster(
            cluster_type=GenevaClusterType.LOCAL_RAY,
            name=self._name,
            ray_address=None,
            kuberay=None,
        )

    @classmethod
    def create(cls, name: str) -> LocalRayClusterBuilder:
        """Create a new builder with the given cluster name."""
        return cls().name(name)


class ExternalRayClusterBuilder:
    """Builder for connecting to an existing external Ray cluster.

    This builder requires a ray_address to be set.
    Does NOT have memory(), cpus(), or worker configuration methods.

    Examples
    --------

        cluster = (
            ExternalRayClusterBuilder.create("remote")
            .ray_address("ray://10.0.0.1:10001")
            .build()
        )
    """

    def __init__(self) -> None:
        self._name: str | None = None
        self._ray_address: str | None = None
        self._ray_init_kwargs: dict = {}

    def name(self, name: str) -> ExternalRayClusterBuilder:
        """Set the cluster name."""
        self._name = name
        return self

    def ray_address(self, addr: str) -> ExternalRayClusterBuilder:
        """Set the Ray address (required). e.g., 'ray://host:port'"""
        self._ray_address = addr
        return self

    def ray_init_kwargs(self, kwargs: dict) -> ExternalRayClusterBuilder:
        """Set kwargs passed to ray.init() when connecting (e.g. env_vars).
        For example:

            .ray_init_kwargs({
                "runtime_env": {
                    "env_vars": {
                        "MY_VAR": "value",
                        "AWS_ACCESS_KEY_ID": os.environ["AWS_ACCESS_KEY_ID"]
                    },
                },
            })
        """
        self._ray_init_kwargs = copy.deepcopy(kwargs)
        return self

    def build(self) -> GenevaCluster:
        """Build the GenevaCluster for external Ray."""
        if self._name is None:
            raise ValueError("Cluster name is required. Use .name() to set it.")
        if self._ray_address is None:
            raise ValueError("ray_address is required for external clusters")

        return GenevaCluster(
            cluster_type=GenevaClusterType.EXTERNAL_RAY,
            name=self._name,
            ray_address=self._ray_address,
            kuberay=None,
            ray_init_kwargs=self._ray_init_kwargs,
        )

    @classmethod
    def create(
        cls, name: str, ray_address: str | None = None
    ) -> ExternalRayClusterBuilder:
        """Create a new builder with the given cluster name and optional ray_address."""
        builder = cls().name(name)
        if ray_address is not None:
            builder = builder.ray_address(ray_address)
        return builder


def default_image(
    gpu: bool = False, arm: bool = platform.processor() in {"aarch64", "arm"}
) -> str:
    """Get the default Ray image"""
    ray_version = ray.__version__
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"

    return get_ray_image(
        ray_version,
        python_version,
        gpu=gpu,
        arm=arm,
    )
