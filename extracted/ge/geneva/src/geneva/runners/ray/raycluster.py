# ruff: noqa: F821

# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# For managing and launching KubeRay Cluster. (Should maybe be named kuberaycluster.py)

import abc
import contextlib
import enum
import functools
import getpass
import json
import logging
import platform
import re
import sys
import time
from collections import Counter
from collections.abc import Generator, Iterable, Iterator
from typing import TYPE_CHECKING, Any, Optional, TypeVar, cast

import attrs
import kubernetes
import kubernetes.client.exceptions
import ray
import yaml
from kubernetes import client

from geneva._context import (
    get_current_context,
)
from geneva._context import (
    set_current_context as _set_current_context,
)

if TYPE_CHECKING:
    from geneva.manifest.mgr import GenevaManifest

# do global config init
from geneva.cluster import K8sConfigMethod
from geneva.config import ConfigBase
from geneva.constants import DEFAULT_K8S_NS
from geneva.runners.kuberay.client import KuberayClients
from geneva.runners.ray.kuberay import (
    KuberaySummary,
    WorkerGroupBrief,
    summarize_kuberay_status,
)
from geneva.tqdm import (
    Colors,
    fmt,
    fmt_numeric,
    fmt_pending,
    fmt_status_badge,
    tqdm,
)
from geneva.utils import deep_merge
from geneva.utils.ray import (
    CPU_ONLY_NODE,
    DEFAULT_MAX_WORKER_REPLICAS,
    GENEVA_AUTOSCALING_RESOURCE,
    GENEVA_RAY_CPU_NODE,
    GENEVA_RAY_GPU_NODE,
    GENEVA_RAY_HEAD,
    GENEVA_RAY_HEAD_NODE,
    get_ray_image,
    size_to_bytes,
)

_LOG = logging.getLogger(__name__)

# Default LANCE_LOG level: ``info`` with two noise sources suppressed at every
# display verbosity (these are LanceDB query-engine internals with no user
# audience, not Geneva's own diagnostics):
#  - DataReplacement transaction warnings (``lance::dataset::transaction``)
#  - per-event telemetry (``lance::events::*`` "plan_run"/"loading" INFO lines)
_DEFAULT_LANCE_LOG = "info,lance::dataset::transaction=error,lance::events=warn"

# Env vars advertising the owning RayCluster inside its pods. The remote
# pipeline driver (head pod) uses them with in-cluster credentials to look up
# worker pod status (OOM evidence) when the client-side RayCluster context is
# not available in its process.
GENEVA_RAY_CLUSTER_NAME_ENV = "GENEVA_RAY_CLUSTER_NAME"
GENEVA_RAY_CLUSTER_NAMESPACE_ENV = "GENEVA_RAY_CLUSTER_NAMESPACE"

# Poll completion probes in a Ray-safe bounded slice. Slow probes retain their
# ObjectRef across slices instead of submitting duplicate actor calls.
_DEFAULT_JOB_TRACKER_PROBE_TIMEOUT_SECS = 5.0


class _HeadPodNotFoundError(RuntimeError):
    """No head pod is discoverable from the RayCluster status.

    Signals the one condition the kuberay 1.1 fallback in ``apply()`` exists
    to handle, so that unrelated ``RuntimeError``s raised while waiting for
    the head node are not swallowed by it.
    """


def _inject_cluster_identity_env(group_spec: dict, name: str, namespace: str) -> None:
    """Add cluster-identity env vars to every container in a group spec."""
    try:
        containers = group_spec["template"]["spec"]["containers"]
    except (KeyError, TypeError):
        return
    for container in containers:
        env = container.setdefault("env", [])
        existing = {e.get("name") for e in env if isinstance(e, dict)}
        for key, value in (
            (GENEVA_RAY_CLUSTER_NAME_ENV, name),
            (GENEVA_RAY_CLUSTER_NAMESPACE_ENV, namespace),
        ):
            if key not in existing:
                env.append({"name": key, "value": value})


@attrs.define
class _RayClusterConfig(ConfigBase):
    user: str = attrs.field(
        converter=attrs.converters.default_if_none(default=getpass.getuser())
    )

    namespace: str = attrs.field(
        converter=attrs.converters.default_if_none(default=DEFAULT_K8S_NS)
    )

    @classmethod
    def name(cls) -> str:
        return "raycluster"

    def cluster_name(self) -> str:
        if self.user:
            return self.user
        _LOG.info("Using the current OS user name as the cluster name")
        return getpass.getuser()


class _ValidationVisitable(abc.ABC):
    @abc.abstractmethod
    def _validate(self, visitor: "_ValidationVisitor") -> None:
        """
        Validate at cluster construction time if the definition is valid
        """


@attrs.define(kw_only=True, slots=False)
class _ResourceMixin:
    num_cpus: int = attrs.field(default=4, validator=attrs.validators.gt(0))
    memory: int = attrs.field(
        converter=size_to_bytes,
        default=8 * (1024**3),
        validator=attrs.validators.gt(0),
    )
    num_gpus: int = attrs.field(default=0, validator=attrs.validators.ge(0))

    arm: bool = attrs.field(default=platform.processor() in {"aarch64", "arm"})

    @property
    def _resources(self) -> dict:
        resource = {
            "requests": {
                "cpu": self.num_cpus,
                "memory": self.memory,
            },
            "limits": {
                "cpu": self.num_cpus,
                "memory": self.memory,
            },
        }

        if self.num_gpus:
            resource["requests"]["nvidia.com/gpu"] = self.num_gpus
            resource["limits"]["nvidia.com/gpu"] = self.num_gpus

        return resource


@attrs.define(kw_only=True, slots=False)
class _ServiceAccountMixin(_ValidationVisitable):
    service_account: str | None = attrs.field(default=None)

    @property
    def _service_account(self) -> dict[str, str] | None:
        if self.service_account is None:
            return None
        return {
            "serviceAccountName": self.service_account,
        }

    def _validate(self, visitor: "_ValidationVisitor") -> None:
        visitor.visit_service_account(self)


@attrs.define(kw_only=True, slots=False)
class _PriorityClassMixin(_ValidationVisitable):
    priority_class: str | None = attrs.field(default=None)

    @property
    def _priority_class(self) -> dict[str, str] | None:
        if self.priority_class is None:
            return None
        return {
            "priorityClassName": self.priority_class,
        }

    def _validate(self, visitor: "_ValidationVisitor") -> None:
        visitor.visit_priority_class(self)


@attrs.define(kw_only=True, slots=False)
class _RayVersionMixin:
    ray_version: str = attrs.field(init=False)
    """
    The version of Ray to use for the cluster. Auto detected from the Ray
    package version in the current environment.
    """

    @ray_version.default  # type: ignore[attr-defined]
    def _default_ray_version(self) -> str:
        return ray.__version__


@attrs.define(kw_only=True, slots=False)
class _PythonVersionMixin:
    python_version: str = attrs.field(init=False)
    """
    The major.minor version of Python to use for the cluster.
    Auto detected from the python version in the current environment.
    """

    @python_version.default  # type: ignore[attr-defined]
    def _default_python_version(self) -> str:
        return f"{sys.version_info.major}.{sys.version_info.minor}"


@attrs.define(kw_only=True, slots=False)
class _ImageMixin(_RayVersionMixin, _PythonVersionMixin, _ResourceMixin):
    # set a dummpy default so the generated __init__
    # gets the correct signature
    image: str = attrs.field()

    @image.default  # type: ignore[attr-defined]
    def _default_image(self) -> str:
        return get_ray_image(
            self.ray_version,
            self.python_version,
            gpu=self.num_gpus > 0,
            arm=self.arm,
        )

    def _validate(self, visitor: "_ValidationVisitor") -> None:
        visitor.visit_image(self)


@attrs.define(kw_only=True, slots=False)
class _MountsMixin:
    volumes: dict[str, dict] = attrs.field(default={})
    """
    Volumes to attach to the worker Pod.

    The key is the name of the volume and the value is the volume specification.
    """

    mounts: list[tuple[str, str]] = attrs.field(default=[])
    """
    The list of mounts to attach to the worker containers.
    """

    @mounts.validator  # type: ignore[attr-defined]
    def _validate_mounts(self, attribute: str, value: list[tuple[str, str]]) -> None:
        paths = set()
        for name, path in value:
            if name not in self.volumes:
                raise ValueError(f"Volume {name} not found in volumes")
            paths.add(path)

        if len(paths) != len(value):
            dups = [
                item
                for item, count in Counter(path for _, path in value).items()
                if count > 1
            ]
            raise ValueError(f"Duplicate mount paths: {dups}")

    @property
    def mounts_definition(self) -> list[dict[str, str]]:
        return [{"name": volume, "mountPath": path} for volume, path in self.mounts]

    @property
    def volume_definition(self) -> list[dict[str, str]]:
        return [{"name": volume, **config} for volume, config in self.volumes.items()]


class _PodSpec(
    _ImageMixin,
    _ResourceMixin,
    _MountsMixin,
    _ServiceAccountMixin,
    _PriorityClassMixin,
    _ValidationVisitable,
):
    def _validate(self, visitor: "_ValidationVisitor") -> None:
        visitor.visit_service_account(self)
        visitor.visit_priority_class(self)
        visitor.visit_image(self)


@attrs.define(kw_only=True)
class _HeadGroupSpec(_PodSpec):
    node_selector: dict[str, str] = attrs.field(default={"_PLACEHOLDER": "true"})
    labels: dict[str, str] = attrs.field(factory=dict)
    tolerations: list[dict[str, str]] = attrs.field(factory=list)

    env_vars: dict[str, str] = attrs.field(factory=dict)
    """
    Additional environment variables to set in the head container.
    """

    k8s_spec_override: dict[str, Any] | None = attrs.field(default=None)
    """
    Arbitrary Kubernetes spec overrides. Deep-merged into the generated K8s spec.
    """

    def __attrs_post_init__(self) -> None:
        if self.node_selector == {"_PLACEHOLDER": "true"}:
            self.node_selector = {GENEVA_RAY_HEAD_NODE: "true"}

    @property
    def _ports(self) -> list[dict]:
        return [
            {
                "containerPort": 10001,
                "name": "client",
                "protocol": "TCP",
            },
            {
                "containerPort": 8265,
                "name": "dashboard",
                "protocol": "TCP",
            },
            {
                "containerPort": 6379,
                "name": "gsc-server",
                "protocol": "TCP",
            },
        ]

    @property
    def definition(self) -> dict:
        definition = {
            "rayStartParams": {
                # do not schedule tasks onto the head node this prevents cluster
                # crashes due to other tasks killing the head node
                "num-cpus": "0",
                # Custom resources advertised by the head pod:
                #   GENEVA_AUTOSCALING_RESOURCE: identifies Geneva-managed
                #     autoscaling clusters (admission control reads it via
                #     ``ray.cluster_resources()``).
                #   GENEVA_RAY_HEAD: head-only marker that pipeline drivers
                #     use to pin placement here -- combined with their
                #     ``num_cpus=0`` so they bypass the ``num-cpus=0``
                #     task-blocking above while still being constrained to
                #     the head.
                "resources": json.dumps(
                    json.dumps(
                        {
                            GENEVA_AUTOSCALING_RESOURCE: 1,
                            GENEVA_RAY_HEAD: 1,
                        }
                    )
                ),
            },
            "template": {
                "metadata": {
                    "labels": {
                        # Azure Workload Identity: required for pods to receive
                        # federated credentials via the workload identity webhook
                        "azure.workload.identity/use": "true",
                        **self.labels,
                    },
                },
                "spec": {
                    **(self._priority_class or {}),
                    **(self._service_account or {}),
                    "containers": [
                        {
                            "name": "ray-head",
                            "image": self.image,
                            "imagePullPolicy": "IfNotPresent",
                            "resources": self._resources,
                            "ports": self._ports,
                            "volumeMounts": self.mounts_definition,
                            "env": [
                                {"name": k, "value": v}
                                for k, v in {
                                    # Defaults (user env_vars override these)
                                    "LANCE_LOG": _DEFAULT_LANCE_LOG,
                                    **self.env_vars,
                                }.items()
                            ],
                        }
                    ],
                    "volumes": self.volume_definition,
                    "nodeSelector": self.node_selector,
                    "tolerations": self.tolerations,
                },
            },
        }

        # Deep merge k8s_spec_override if present
        if self.k8s_spec_override is not None:
            definition = deep_merge(definition, self.k8s_spec_override)

        return definition


@attrs.define(kw_only=True)
class _WorkerGroupSpec(_PodSpec):
    """
    A worker group specification for a Ray cluster.
    """

    name: str = attrs.field(default="worker")

    @name.validator  # type: ignore[attr-defined]
    def _validate_name(self, attribute: str, value: str) -> None:
        if not value:
            raise ValueError("name cannot be empty")

        if not re.match(r"^[a-zA-Z0-9\-]+$", value):
            raise ValueError(
                f"name must only contain alphanumeric characters and dashes: {value}"
            )

    node_selector: dict[str, str] = attrs.field(default={"_PLACEHOLDER": "true"})

    labels: dict[str, str] = attrs.field(factory=dict)

    tolerations: list[dict[str, str]] = attrs.field(factory=list)

    replicas: int = attrs.field(
        default=1,
        validator=attrs.validators.ge(0),
    )

    # Note on validator ordering: Although replicas is defined before min_replicas
    # and max_replicas, attrs initializes ALL field values before running validators.
    # This means self.min_replicas and self.max_replicas are available when this
    # validator runs. See: https://www.attrs.org/en/stable/init.html#validators
    @replicas.validator  # type: ignore[attr-defined]
    def _validate_replicas(self, attribute: str, value: int) -> None:
        if value < self.min_replicas:
            raise ValueError(
                f"replicas ({value}) must be >= min_replicas ({self.min_replicas})"
            )
        if value > self.max_replicas:
            raise ValueError(
                f"replicas ({value}) must be <= max_replicas ({self.max_replicas})"
            )

    idle_timeout_seconds: int = attrs.field(
        default=60,
        validator=attrs.validators.ge(0),
    )

    min_replicas: int = attrs.field(
        default=0,
        validator=attrs.validators.ge(0),
    )
    max_replicas: int = attrs.field(
        default=DEFAULT_MAX_WORKER_REPLICAS,
    )

    env_vars: dict[str, str] = attrs.field(factory=dict)
    """
    Additional environment variables to set in the worker containers.
    """

    k8s_spec_override: dict[str, Any] | None = attrs.field(default=None)
    """
    Arbitrary Kubernetes spec overrides. Deep-merged into the generated K8s spec.
    """

    @max_replicas.validator  # type: ignore[attr-defined]
    def _validate_max_replicas(self, attribute: str, value: int) -> None:
        if value == 0:
            raise ValueError("max_replicas must be greater than 0")

        if value < self.min_replicas:
            raise ValueError(
                f"max_replicas ({value}) must be greater than or",
                f" equal to min_replicas ({self.min_replicas})",
            )

    def __attrs_post_init__(self) -> None:
        if self.node_selector == {"_PLACEHOLDER": "true"}:
            if self.num_gpus > 0:
                self.node_selector = {GENEVA_RAY_GPU_NODE: "true"}
            else:
                self.node_selector = {GENEVA_RAY_CPU_NODE: "true"}

    @property
    def _start_params(self) -> dict:
        params = {
            "num-cpus": str(self.num_cpus),
            "num-gpus": str(self.num_gpus),
        }

        # add a special resource for CPU only nodes
        # so that actors can be forced to run on CPU only nodes
        # in practice it looks like this
        # actor.options(num_cpus=1) can be scheduled on
        # * CPU only nodes, or
        # * GPU nodes with >= 1 CPU
        #
        # however, it is usually wasteful to schedule cpu-only actors
        # on GPU nodes. This allows us to force them to run on CPU only nodes
        if self.num_gpus == 0:
            # this param needs to be a JSON-string of a JSON-string
            # https://docs.ray.io/en/latest/ray-core/scheduling/resources.html#codecell3
            params["resources"] = json.dumps(json.dumps({CPU_ONLY_NODE: 10**5}))

        return params

    @property
    def definition(self) -> dict:
        definition = {
            "groupName": self.name,
            "replicas": self.replicas,
            "minReplicas": self.min_replicas,
            "maxReplicas": self.max_replicas,
            "idleTimeoutSeconds": self.idle_timeout_seconds,
            "rayStartParams": self._start_params,
            "template": {
                "metadata": {
                    "labels": {
                        # Azure Workload Identity: required for pods to receive
                        # federated credentials via the workload identity webhook
                        "azure.workload.identity/use": "true",
                        **self.labels,
                    },
                },
                "spec": {
                    **(self._priority_class or {}),
                    **(self._service_account or {}),
                    "containers": [
                        {
                            "name": "ray-worker",
                            "image": self.image,
                            "imagePullPolicy": "IfNotPresent",
                            "resources": self._resources,
                            "volumeMounts": self.mounts_definition,
                            "livenessProbe": {
                                "exec": {
                                    "command": [
                                        "bash",
                                        "-c",
                                        "wget --tries 1 -T 2 -q -O- "
                                        "http://localhost:52365/api/"
                                        "local_raylet_healthz | grep success",
                                    ],
                                },
                                "failureThreshold": 200,  # default: 120
                                "initialDelaySeconds": 30,
                                "periodSeconds": 30,  # default: 10
                                "successThreshold": 1,
                                "timeoutSeconds": 10,  # default: 2
                            },
                            "readinessProbe": {
                                "exec": {
                                    "command": [
                                        "bash",
                                        "-c",
                                        "wget --tries 1 -T 2 -q -O- "
                                        "http://localhost:52365/api/"
                                        "local_raylet_healthz | grep success",
                                    ],
                                },
                                "failureThreshold": 60,  # default: 10
                                "initialDelaySeconds": 30,  # default: 10
                                "periodSeconds": 10,  # default: 5
                                "successThreshold": 1,
                                "timeoutSeconds": 10,  # default: 2
                            },
                            "env": [
                                {"name": k, "value": v}
                                for k, v in {
                                    # Defaults (user env_vars override these)
                                    "RAY_memory_usage_threshold": "0.9",
                                    "RAY_memory_monitor_refresh_ms": "0",
                                    "LANCE_LOG": _DEFAULT_LANCE_LOG,
                                    **self.env_vars,
                                }.items()
                            ],
                        }
                    ],
                    "volumes": self.volume_definition,
                    "nodeSelector": self.node_selector,
                    "tolerations": self.tolerations,
                },
            },
        }

        # Deep merge k8s_spec_override if present
        if self.k8s_spec_override is not None:
            definition = deep_merge(definition, self.k8s_spec_override)

        return definition


class ExitMode(enum.Enum):
    """
    Behavior on context manager exit.
    RETAIN_ON_FAILURE will wait for all tracked async jobs to finish,
        then retain the cluster if any job failed, the context body
        raised an exception, or wait_timeout was reached; otherwise
        delete. If wait_timeout is set and exceeded, this is treated
        as a failure and the cluster is retained.
    DELETE will wait for all tracked async jobs to reach a terminal
        state (DONE or FAILED), then delete the RayCluster. If
        wait_timeout is set and exceeded, the cluster is deleted even
        if jobs are still running.
    RETAIN will always retain the RayCluster.
    """

    RETAIN_ON_FAILURE = "retain_on_failure"
    DELETE = "delete"
    RETAIN = "retain"


@attrs.define(kw_only=True)
class RayCluster(_RayVersionMixin, _ValidationVisitable):
    """
    A Ray cluster specification.

    This is also a context manager for managing a Ray cluster.
    This context manager will apply the Ray cluster definition to the
    Kubernetes cluster when entering the context and delete the Ray
    cluster from the Kubernetes cluster when exiting the context.

    When entering the context, ray.init will be called with the address of the
    Ray cluster head node. When exiting the context, ray.shutdown will be
    called to shutdown the Ray cluster.

    Examples
    --------
        >>> from geneva.runners.ray.raycluster import RayCluster
        >>> head_group = _HeadGroupSpec(image="rayproject/ray:latest")
        >>> worker_group = _WorkerGroupSpec(name="worker", image="rayproject/ray")
        >>> with RayCluster(
        ...     name="test-cluster",
        ...     head_group=head_group,
        ...     worker_groups=[worker_group],
        ... ):
        ...     print("Ray cluster is running")
        Ray cluster is running
    """

    name: str = attrs.field()
    """
    The name of the Ray cluster. This name is used for deduplication of Ray
    clusters in the Kubernetes cluster. When a Ray cluster with the same name
    already exists, we will not create a new one.

    Must comply with RFC 1123 DNS naming conventions:
    - 63 characters or less
    - lowercase letters, numbers, and hyphens only
    - must start and end with an alphanumeric character

    TODO: add a recreate=True option to force the recreation of the cluster.
    """

    @name.validator  # type: ignore[attr-defined]
    def _validate_name(self, attribute: str, value: str) -> None:
        """Validate that the cluster name complies with RFC 1123 for
        Kubernetes domain validation"""
        if not value:
            raise ValueError("cluster name cannot be empty")
        if len(value) > 63:
            raise ValueError(f"cluster name must be 63 characters or less: {value}")
        # RFC 1123 pattern: lowercase letters, numbers, and hyphens
        # Must start and end with alphanumeric character
        if not re.match(r"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?$", value):
            raise ValueError(
                "cluster name must comply with RFC 1123: "
                "lowercase letters, numbers, and hyphens only; "
                f"must start and end with alphanumeric character: {value}"
            )

    @name.default  # type: ignore[attr-defined]
    def _default_name(self) -> str:
        config = _RayClusterConfig.get()
        user_name = config.user.lower()  # Ensure lowercase for RFC 1123 compliance
        # Replace any invalid characters with hyphens
        user_name = re.sub(r"[^a-z0-9\-]", "-", user_name)
        # Ensure it starts and ends with alphanumeric
        user_name = re.sub(r"^-+|-+$", "", user_name)
        # Ensure it's not empty after cleanup
        if not user_name:
            user_name = "user"
        # Ensure the final name doesn't exceed 63 characters
        prefix = "geneva-"
        max_user_length = 63 - len(prefix)
        if len(user_name) > max_user_length:
            user_name = user_name[:max_user_length]
            # Ensure it doesn't end with a hyphen after truncation
            user_name = re.sub(r"-+$", "", user_name)
            # Ensure it's not empty after truncation
            if not user_name:
                user_name = "user"
        return f"{prefix}{user_name}"

    namespace: str = attrs.field()
    """
    The namespace of the Ray cluster. This is the namespace in which the Ray
    cluster will be created in the Kubernetes cluster.
    """

    @namespace.default  # type: ignore[attr-defined]
    def _default_namespace(self) -> str:
        config = _RayClusterConfig.get()
        return config.namespace

    head_group: _HeadGroupSpec = attrs.field(factory=_HeadGroupSpec)  # type: ignore[arg-type]
    """
    The head group specification for the Ray cluster.
    """

    worker_groups: list[_WorkerGroupSpec] = attrs.field(
        factory=lambda: [_WorkerGroupSpec()]  # type: ignore[misc]
    )
    """
    The worker group specifications for the Ray cluster.
    """

    strict_access_review: bool = attrs.field(
        default=False,
    )
    """
    Fail the access review for the service account if any errors occur.
    e.g. if we don't have permission to create local subject access reviews
    """

    config_method: K8sConfigMethod = attrs.field(default=K8sConfigMethod.LOCAL)
    """
    Method to retrieve kubeconfig
    """

    region: str = attrs.field(
        default=None,
    )
    """
    Optional cloud region where the cluster is located
    """

    cluster_name: str = attrs.field(
        default=None,
    )
    """
    Optional k8s cluster name, required for EKS auth
    """

    role_name: str = attrs.field(
        default=None,
    )
    """
    Optional IAM role name, required for EKS auth. This can be a role name or
    a role ARN. If a role name is provided, it is assumed the role is in the
    current account.
    """

    on_exit: ExitMode = attrs.field(
        default=ExitMode.DELETE,
    )
    """
    Context manager behavior on exit. By default, the RayCluster will
    wait for all running jobs to complete before deleting.
    """

    manifest: "GenevaManifest | None" = attrs.field(
        default=None,
        init=False,
    )
    """
    Optional manifest defining the code and dependencies for this cluster.
    Set by the context manager when entering.
    """

    wait_timeout: float | None = attrs.field(
        default=None,
    )
    """
    Internal/experimental. Maximum seconds to wait for tracked jobs
    during context exit. Used as a safety valve to prevent indefinite
    blocking if a job hangs. None (default) means wait indefinitely.
    Applies when on_exit is DELETE or RETAIN_ON_FAILURE.
    """

    _tracked_refs: list = attrs.field(factory=list, init=False)
    """
    List of (job_id, ObjectRef, JobTracker) tuples registered during the context.
    Used by _wait_for_tracked_jobs to block until all async jobs complete.
    """

    _jobs_had_failures: bool = attrs.field(default=False, init=False)
    """
    Cached result from _wait_for_tracked_jobs(). True if any tracked job
    failed. Set by the _mgr.py early-wait call (while Ray is still up) so
    that __exit__ can use it after Ray has been shut down.
    """

    ray_init_kwargs: dict[str, Any] = attrs.field(
        factory=dict,
    )
    """
    Arbitrary kwargs to pass to ray.init() when starting the cluster.
    This allows passing any ray.init() parameter like runtime_env, etc.
    """

    @classmethod
    def from_config_map(
        cls,
        k8s_namespace: str,
        k8s_cluster_name: str,
        config_map_name: str,
        name: str,
        *,
        config_method: K8sConfigMethod = K8sConfigMethod.LOCAL,
        aws_region: str | None = None,
        aws_role_name: str | None = None,
    ) -> "RayCluster":
        """
        Create a RayCluster from an existing Kubernetes ConfigMap.

        Parameters
        ----------
            k8s_namespace
                Namespace of the ConfigMap.
            k8s_cluster_name
                Name of the Kubernetes cluster
            config_map_name
                Name of the ConfigMap to load the RayCluster spec from.
            name
                Name of the RayCluster to create
            config_method
                Optional Method to retrieve kubeconfig.
            aws_region
                Cloud region for EKS auth.
            aws_role_name
                IAM role name for EKS auth.
        """
        clients = KuberayClients(
            config_method=config_method,
            region=aws_region,
            role_name=aws_role_name,
            cluster_name=k8s_cluster_name,
        )

        cm = clients.core_api.read_namespaced_config_map(
            name=config_map_name, namespace=k8s_namespace
        )
        data = cm.data or {}  # type: ignore[attr-defined]

        _LOG.debug(f"loaded config map {config_map_name}: {data}")

        config_kwargs: dict[str, Any] = {}
        for key, value in data.items():
            try:
                config_kwargs[key] = yaml.safe_load(value)
            except Exception:  # noqa: PERF203
                config_kwargs[key] = value

        try:
            config_kwargs["name"] = name
            config_kwargs["namespace"] = k8s_namespace
            config_kwargs["config_method"] = config_method
            config_kwargs["region"] = aws_region
            config_kwargs["role_name"] = aws_role_name
            config_kwargs["head_group"] = _HeadGroupSpec(  # type: ignore[call-arg]
                **config_kwargs.get("head_group")  # type: ignore[arg-type]
            )
            config_kwargs["worker_groups"] = [
                _WorkerGroupSpec(**w) for w in config_kwargs["worker_groups"]
            ]
            res = cls(**config_kwargs)
        except Exception as e:
            _LOG.error(f"error parsing ConfigMap data for {config_map_name}", e)
            raise Exception(
                f"unable to parse ConfigMap data for {config_map_name}: {str(e)}"
            ) from e

        return res

    def to_config_map(self) -> dict[str, str]:
        """
        Serialize this RayCluster into a dict of YAML strings suitable for
        storing in a Kubernetes ConfigMap.data field.
        Keys include 'name', 'head_group', and 'worker_groups'.
        """
        data: dict[str, str] = {}
        data["name"] = self.name
        head_dict = attrs.asdict(self.head_group)
        # remove internal attrs
        for key in ("ray_version", "python_version"):
            head_dict.pop(key, None)
        data["head_group"] = yaml.safe_dump(head_dict, sort_keys=False)
        wgs: list[dict[str, Any]] = []
        for w in self.worker_groups:
            wd = attrs.asdict(w)
            for key in ("ray_version", "python_version"):
                wd.pop(key, None)
            wgs.append(wd)
        data["worker_groups"] = yaml.safe_dump(wgs, sort_keys=False)
        return data

    def __attrs_post_init__(self) -> None:
        self.clients = KuberayClients(
            config_method=self.config_method,
            region=self.region,
            cluster_name=self.cluster_name,
            role_name=self.role_name,
        )

    @property
    def _autoscaler_options(self) -> dict:
        """
        The autoscaler options for the Ray cluster.
        """
        # TODO: allow customization of the autoscaler options
        return {
            "version": "v2",
            "enableInTreeAutoscaling": True,
            "env": [{"name": "RAY_enable_autoscaler_v2", "value": "1"}],
            "envFrom": [],
            "idleTimeoutSeconds": 60,
            "imagePullPolicy": "IfNotPresent",
            "resources": {
                "requests": {
                    "cpu": "1",
                    "memory": "1Gi",
                },
                "limits": {
                    "cpu": "1",
                    "memory": "1Gi",
                },
            },
            "upscalingMode": "Default",
        }

    @property
    def spec(self) -> dict:
        """
        The Ray cluster specification.

        This can be used as part of RayJob for configuring the Ray cluster.
        """
        head_spec = self.head_group.definition
        worker_specs = [worker.definition for worker in self.worker_groups]
        for group_spec in (head_spec, *worker_specs):
            _inject_cluster_identity_env(group_spec, self.name, self.namespace)
        return {
            "enableInTreeAutoscaling": True,
            "autoscalerOptions": self._autoscaler_options,
            "rayVersion": self.ray_version,
            "headGroupSpec": head_spec,
            "workerGroupSpecs": worker_specs,
        }

    @property
    def definition(self) -> dict:
        """
        The Ray cluster definition.

        This is the full definition of the Ray cluster, including the name and
        autoscaler options. This can be used to create the Ray cluster in the
        Kubernetes cluster via a CRD.
        """
        return {
            "apiVersion": "ray.io/v1",
            "kind": "RayCluster",
            "metadata": {
                "name": self.name,
                "namespace": self.namespace,
            },
            "spec": self.spec,
        }

    def _has_existing_cluster(self) -> bool:
        try:
            self.clients.custom_api.get_namespaced_custom_object(
                group="ray.io",
                version="v1",
                namespace=self.namespace,
                plural="rayclusters",
                name=self.name,
            )
        except kubernetes.client.exceptions.ApiException as e:
            if e.status == 404:
                return False
            raise e
        return True

    def _wait_for_cluster(self, timeout_s: float = 300.0) -> Any:
        """Wait for the Ray cluster to be ready.

        Parameters
        ----------
            timeout_s
                Maximum time to wait in seconds. Default 300s (5 minutes).

        Returns
        -------
            The cluster status dict.

        Raises
        ------
            TimeoutError
                If the cluster is not ready within timeout_s.
        """
        start = time.time()
        while True:
            elapsed = time.time() - start
            if elapsed > timeout_s:
                raise TimeoutError(
                    f"Timed out waiting for Ray cluster '{self.name}' to be ready "
                    f"after {timeout_s:.0f}s"
                )

            result = self.clients.custom_api.get_namespaced_custom_object(
                group="ray.io",
                version="v1",
                namespace=self.namespace,
                plural="rayclusters",
                name=self.name,
            )
            assert isinstance(result, dict)

            if "status" not in result:
                _LOG.debug("Waiting for the Ray cluster to be ready")
                time.sleep(1)
                continue

            status = result["status"]
            assert isinstance(status, dict)

            if "head" not in status:
                _LOG.debug("Waiting for the head node to be ready")
                time.sleep(1)
                continue

            head = status["head"]
            assert isinstance(head, dict)

            if "podIP" not in head:
                _LOG.debug("Waiting for the head node IP address")
                time.sleep(1)
                continue

            _LOG.debug("Ray cluster is ready")
            return result

    def _wait_for_head_node(self, pod_name: str, timeout_s: float = 600.0) -> Any:
        """Wait for the head node pod to be running.

        Parameters
        ----------
            pod_name
                The name of the head node pod.
            timeout_s
                Maximum time to wait in seconds. Default 600s (10 minutes).

        Returns
        -------
            The V1Pod object.

        Raises
        ------
            TimeoutError
                If the pod is not running within timeout_s.
            RuntimeError
                If a container is in CrashLoopBackOff, terminated, etc.
        """
        start = time.time()
        while True:
            elapsed = time.time() - start
            if elapsed > timeout_s:
                raise TimeoutError(
                    f"Timed out waiting for head pod '{pod_name}' to be running "
                    f"after {timeout_s:.0f}s"
                )

            pod: client.V1Pod = cast(
                "client.V1Pod",
                self.clients.core_api.read_namespaced_pod(
                    name=pod_name, namespace=self.namespace
                ),
            )
            if pod.status is None or pod.status.phase != "Running":
                _LOG.debug("Waiting for the head node to be running")
                time.sleep(1)
                continue

            # Pod phase is Running, but check container-level health
            _check_head_container_health(pod)

            # Wait for all containers to be ready
            all_ready = all(
                cs.ready
                for cs in (pod.status.container_statuses or [])
                if cs is not None
            )
            if not all_ready:
                _LOG.debug("Waiting for all head node containers to be ready")
                time.sleep(1)
                continue

            _LOG.debug("Head node is running")
            return pod

    def _get_podname(self, cluster: dict[str, Any] | None = None) -> str:
        """Get the head node pod name from cluster status.

        Parameters
        ----------
            cluster
                Optional pre-fetched cluster status dict. If None, will
                     call _wait_for_cluster() to fetch it.
        """
        if cluster is None:
            cluster = self._wait_for_cluster()
        assert isinstance(cluster, dict)
        _LOG.debug(f"cluster status: {cluster['status']}")

        # kuberay 1.2+
        pod_name = cluster.get("status", {}).get("head", {}).get("podName")
        if pod_name:
            return pod_name

        # kuberay 1.1 version.
        label_selector = f"ray.io/cluster={self.name},ray.io/node-type=head"
        pods = self.clients.core_api.list_namespaced_pod(
            namespace=self.namespace,
            label_selector=label_selector,
        )

        for pod in pods.items:
            if pod.status.phase == "Running":
                return pod.metadata.name
        raise _HeadPodNotFoundError(
            f"Failed to find head node pod for cluster {self.name}"
        )

    @property
    def head_node_pod(self) -> Any:
        """Get the head node pod, waiting for it to be ready."""
        cluster = self._wait_for_cluster()  # Single wait call
        pod_name = self._get_podname(cluster)  # Reuse the result
        return self._wait_for_head_node(pod_name)

    @property
    def ui_pod(self) -> Optional[Any]:
        label_selector = "geneva.lancedb.com/console-ui=true"
        pods = self.clients.core_api.list_namespaced_pod(
            namespace=self.namespace,
            label_selector=label_selector,
        )
        for pod in pods.items:
            if pod.status.phase == "Running":
                return pod
        _LOG.debug("could not locate console-ui pod")
        return None

    def apply(self) -> str:
        """
        Apply the Ray cluster definition to the Kubernetes cluster.

        returns the ip address of the head node
        """
        self._validate()

        if self._has_existing_cluster():
            _LOG.info(
                "Ray cluster already exists, patching instead of creating a new one."
                " This means existing nodes will not update until they are recreated."
                " Use recreate=True to force recreation."
            )
            self.clients.custom_api.patch_namespaced_custom_object(
                group="ray.io",
                version="v1",
                namespace=self.namespace,
                plural="rayclusters",
                name=self.name,
                body=self.definition,
            )
        else:
            self.clients.custom_api.create_namespaced_custom_object(
                group="ray.io",
                version="v1",
                namespace=self.namespace,
                plural="rayclusters",
                body=self.definition,
            )

        try:
            pod = self.head_node_pod

            return pod.status.pod_ip
        except (_HeadPodNotFoundError, KeyError, AttributeError):
            # Only an unexpected status shape falls back. Everything else
            # names a real problem the fallback would mask: a TimeoutError
            # means the cluster never came up, and the RuntimeError from
            # _check_head_container_health carries the CrashLoopBackOff /
            # OOM diagnostic for a head pod that already has an IP -- which
            # the fallback would happily return as a success.
            _LOG.warning("Falling back to kuberay 1.1 cluster status")
            # kuberay 1.1 version of cluster['status'].  kuberay 1.2+ has
            # cluster['status']['head']['podName'] which is used to look up
            # the head node's ip
            """
            {
                ...
                "head": {"podIP": "10.104.5.6", "serviceIP": "34.118.237.31"},
                ...
                "state": "ready",
            }
            """
            timeout_s = 300.0
            start = time.time()
            while True:
                elapsed = time.time() - start
                if elapsed > timeout_s:
                    raise TimeoutError(
                        f"Timed out waiting for kuberay 1.1 head node IP "
                        f"after {timeout_s:.0f}s"
                    ) from None

                cluster = self._wait_for_cluster()
                _LOG.debug(f"cluster status waiting for head: {cluster['status']}")
                head_ip = cluster["status"]["head"].get("podIP")
                if head_ip is None:
                    _LOG.info(
                        "waiting for kuberay 1.1 head node to be ready but"
                        f" no IP: {head_ip}"
                    )
                    time.sleep(1)
                    continue
                _LOG.info(f"kuberay 1.1 head node is running @ {head_ip}")
                return head_ip

    def delete(self) -> None:
        """
        Delete the Ray cluster from the Kubernetes cluster.
        """
        try:
            if not self._has_existing_cluster():
                _LOG.warning("No kuberay cluster to shutdown")
                return
            self.clients.custom_api.delete_namespaced_custom_object(
                group="ray.io",
                version="v1",
                namespace=self.namespace,
                plural="rayclusters",
                name=self.name,
            )
        except kubernetes.client.exceptions.ApiException as e:
            if e.status == 404:
                _LOG.info(
                    f"{self.cluster_name}: Ray cluster does not exist, "
                    f"nothing to delete"
                )
                return
            _LOG.exception(f"{self.cluster_name}: Failed to delete Ray cluster")
            raise e
        except Exception as e:
            _LOG.exception(f"{self.cluster_name}: Failed to delete Ray cluster")
            raise e

    @staticmethod
    def _poll_tracker_done(
        tracker: Any,
        probe_ref: Any = None,
        *,
        timeout: float = _DEFAULT_JOB_TRACKER_PROBE_TIMEOUT_SECS,
    ) -> tuple[bool | None, Any | None]:
        """Poll one single-flight JobTracker completion probe.

        Returns ``(None, ref)`` while the existing probe is still running,
        ``(True, None)`` only when the actor explicitly reports completion,
        and ``(False, None)`` when a completed probe reports not-done or fails.
        """
        try:
            if probe_ref is None:
                probe_ref = tracker.is_job_done.remote()
            ready, _ = ray.wait([probe_ref], timeout=timeout)
            if not ready:
                return None, probe_ref
            return bool(ray.get(ready[0])), None
        except Exception:
            _LOG.warning(
                "JobTracker unreachable; treating as not-yet-done (will retry)",
                exc_info=True,
            )
            return False, None

    def register_tracked_job(
        self, job_id: str, obj_ref: ray.ObjectRef, job_tracker: Any = None
    ) -> None:
        """Register a job so _wait_for_tracked_jobs can await it.

        Stores the ObjectRef (for ``ray.wait``) and optionally the
        JobTracker actor handle (for ``is_job_done`` confirmation).
        """
        self._tracked_refs.append((job_id, obj_ref, job_tracker))

    def _wait_for_tracked_jobs(self, poll_interval: float = 5.0) -> bool:
        """Block until all tracked jobs complete.

        Uses a two-phase approach:
        1. ``ray.wait`` on ObjectRefs to detect when each remote task
           finishes (success or failure).
        2. Poll each job's ``JobTracker.is_job_done()`` to confirm the
           actor has recorded completion (final DB save, etc.).

        ObjectRefs are registered at job submission time via
        ``register_tracked_job``, so there are no race conditions with
        actor discovery.

        Respects ``self.wait_timeout`` — if set, the wait is abandoned after
        that many seconds. For DELETE, the cluster is then deleted. For
        RETAIN_ON_FAILURE, a timeout is treated as a failure and the
        cluster is retained (since jobs may still be running).

        Called automatically when on_exit is DELETE or RETAIN_ON_FAILURE.

        Returns True if any tracked job failed.
        """
        if not self._tracked_refs:
            _LOG.info(f"{self.name}: no tracked jobs, skipping wait")
            return False

        if not ray.is_initialized():
            _LOG.debug(f"{self.name}: Ray not initialized, skipping wait")
            return False

        deadline = (
            time.monotonic() + self.wait_timeout
            if self.wait_timeout is not None
            else None
        )

        # Phase 1: wait for ObjectRefs to resolve
        ref_to_job: dict[ray.ObjectRef, str] = {
            ref: jid for jid, ref, _tracker in self._tracked_refs
        }
        refs = list(ref_to_job.keys())

        _LOG.info(
            f"{self.name}: waiting for {len(refs)} tracked job(s)..."
            + (f" (timeout={self.wait_timeout}s)" if self.wait_timeout else "")
        )

        has_failures = False
        while refs:
            if deadline is not None and time.monotonic() > deadline:
                _LOG.warning(
                    f"{self.name}: timed out after {self.wait_timeout}s "
                    f"waiting for jobs; {len(refs)} still running"
                )
                # Timeout with pending jobs is treated as failure — we
                # can't confirm those jobs succeeded.
                return True

            ready, refs = ray.wait(refs, num_returns=len(refs), timeout=poll_interval)
            for r in ready:
                try:
                    ray.get(r)
                    _LOG.info(
                        f"{self.name}: job {ref_to_job[r]} completed successfully"
                    )
                except Exception:  # noqa: PERF203 — each ref needs independent failure tracking
                    has_failures = True
                    _LOG.warning(
                        f"{self.name}: job {ref_to_job[r]} failed", exc_info=True
                    )

            if refs:
                _LOG.info(f"{self.name}: {len(refs)} job(s) still running...")

        if has_failures:
            _LOG.info(
                f"{self.name}: skipping JobTracker confirmation because "
                "tracked jobs failed"
            )
            return True

        # Phase 2: confirm JobTrackers report done
        trackers = [
            (jid, tracker)
            for jid, _ref, tracker in self._tracked_refs
            if tracker is not None
        ]
        if trackers:
            _LOG.info(
                f"{self.name}: confirming {len(trackers)} JobTracker(s) report done..."
            )
            # Per-tracker consecutive-failure counter.  If a tracker is
            # unreachable (actor dead, OOMKilled, node lost) for this many
            # polls in a row, we give up on confirming it and report the
            # job as failed.  This prevents an infinite spin when
            # wait_timeout is None (the default) and the tracker actor is
            # genuinely gone.
            max_consecutive_failures = 6
            failure_counts: dict[str, int] = {jid: 0 for jid, _tracker in trackers}
            pending = [(jid, tracker, None) for jid, tracker in trackers]
            while pending:
                if deadline is not None and time.monotonic() > deadline:
                    _LOG.warning(
                        f"{self.name}: timed out waiting for "
                        f"JobTracker confirmation; {len(pending)} remaining"
                    )
                    return True

                still_pending = []
                has_inflight_probe = False
                for jid, tracker, probe_ref in pending:
                    probe_timeout = _DEFAULT_JOB_TRACKER_PROBE_TIMEOUT_SECS
                    if deadline is not None:
                        remaining = deadline - time.monotonic()
                        if remaining <= 0:
                            _LOG.warning(
                                f"{self.name}: timed out waiting for "
                                "JobTracker confirmation"
                            )
                            return True
                        probe_timeout = min(probe_timeout, remaining)

                    done, probe_ref = self._poll_tracker_done(
                        tracker,
                        probe_ref,
                        timeout=probe_timeout,
                    )
                    if done is True:
                        _LOG.info(f"{self.name}: JobTracker {jid} confirmed done")
                        failure_counts[jid] = 0
                    elif done is None:
                        has_inflight_probe = True
                        still_pending.append((jid, tracker, probe_ref))
                    else:
                        failure_counts[jid] += 1
                        if failure_counts[jid] >= max_consecutive_failures:
                            _LOG.error(
                                f"{self.name}: JobTracker {jid} unreachable "
                                f"for {max_consecutive_failures} consecutive "
                                "probes; treating job as "
                                "FAILED rather than assuming success"
                            )
                            has_failures = True
                            # Drop this tracker from pending — don't keep
                            # polling a dead actor.
                            continue
                        still_pending.append((jid, tracker, None))
                pending = still_pending
                if pending:
                    if has_inflight_probe:
                        _LOG.info(
                            f"{self.name}: {len(pending)} JobTracker probe(s) "
                            "still running"
                        )
                    else:
                        sleep_secs = poll_interval
                        if deadline is not None:
                            sleep_secs = min(
                                sleep_secs,
                                max(0.0, deadline - time.monotonic()),
                            )
                        _LOG.info(
                            f"{self.name}: {len(pending)} JobTracker(s) "
                            f"not yet done, waiting {sleep_secs}s..."
                        )
                        if sleep_secs > 0:
                            time.sleep(sleep_secs)

        _LOG.info(f"{self.name}: all tracked jobs completed")
        return has_failures

    def __enter__(self) -> str:
        _LOG.info(f"{self.name}: Starting Ray cluster")

        _set_current_context(self)
        try:
            return self.apply()
        except BaseException:
            _set_current_context(None)
            raise

    def __exit__(self, exc_type=None, exc_value=None, traceback=None) -> None:
        _set_current_context(None)

        success = exc_type is None

        if self.on_exit == ExitMode.RETAIN_ON_FAILURE:
            # _wait_for_tracked_jobs() is called earlier in _mgr.py while
            # Ray is still up; by this point Ray may be shut down. Use the
            # cached result, falling back to a direct call if __exit__ is
            # invoked without the _mgr.py wrapper (e.g. bare context manager).
            has_failures = self._jobs_had_failures or self._wait_for_tracked_jobs()
            if has_failures or not success:
                _LOG.info(f"{self.name}: retaining RayCluster due to failure")
            else:
                _LOG.info(f"{self.name}: deleting RayCluster (all jobs succeeded)")
                self.delete()
        elif self.on_exit == ExitMode.DELETE:
            self._wait_for_tracked_jobs()
            _LOG.info(f"{self.name}: deleting RayCluster (jobs completed)")
            self.delete()
        elif self.on_exit == ExitMode.RETAIN:
            _LOG.info(f"{self.name}: retaining RayCluster due to ExitMode.RETAIN")
        else:
            raise Exception(f"unsupported exit_mode: {self.on_exit}")

    def _validate(self, visitor=None) -> None:
        if visitor is None:
            visitor = _ValidationVisitor()
        with (
            visitor.with_namespace(self.namespace),
            visitor.with_cluster_name(self.name),
            visitor.with_strict_access_review(self.strict_access_review),
            visitor.with_core_api(self.clients.core_api),
            visitor.with_auth_api(self.clients.auth_api),
            visitor.with_scheduling_api(self.clients.scheduling_api),
        ):
            self.head_group._validate(visitor)
            for worker in self.worker_groups:
                worker._validate(visitor)


_FATAL_WAITING_REASONS = frozenset(
    {
        "CrashLoopBackOff",
        "CreateContainerError",
        "CreateContainerConfigError",
        "RunContainerError",
    }
)


def _check_head_container_health(pod: client.V1Pod) -> None:
    """Raise RuntimeError if any container in the head pod is crashed or OOM-killed."""
    for cs in pod.status.container_statuses or []:  # type: ignore[union-attr]
        state = cs.state
        if state is None:
            continue

        # Container is in a crash loop or similar fatal waiting state
        if state.waiting and state.waiting.reason in _FATAL_WAITING_REASONS:
            diag = _head_pod_diagnostics(cs)
            raise RuntimeError(
                f"Head node container '{cs.name}' is in {state.waiting.reason}. "
                f"{diag}"
                "If the container is OOM-killed, increase memory via "
                "head_group(memory=...) in your RayCluster config."
            )

        # Container already terminated (exited)
        if state.terminated:
            diag = _head_pod_diagnostics(cs)
            raise RuntimeError(
                f"Head node container '{cs.name}' terminated with "
                f"reason={state.terminated.reason}, "
                f"exit_code={state.terminated.exit_code}. "
                f"{diag}"
                "If the container is OOM-killed, increase memory via "
                "head_group(memory=...) in your RayCluster config."
            )


def _head_pod_diagnostics(cs: client.V1ContainerStatus) -> str:
    """Extract last termination details from a container status."""
    parts: list[str] = []
    last = cs.last_state
    if last and last.terminated:
        t = last.terminated
        parts.append(f"Last terminated: reason={t.reason}, exit_code={t.exit_code}.")
    restart_count = cs.restart_count
    if restart_count and restart_count > 0:
        parts.append(f"Restart count: {restart_count}.")
    if parts:
        return " ".join(parts) + " "
    return ""


def _can_i(
    *,
    auth_api: kubernetes.client.AuthorizationV1Api,
    namespace: str,
    sa: str,
    verb: str,
    resource: str,
    name: str,
    group: str | None = None,
) -> bool:
    """
    Check if the service account has permission to perform the action
    """
    res: client.V1LocalSubjectAccessReview = cast(
        "client.V1LocalSubjectAccessReview",
        auth_api.create_namespaced_local_subject_access_review(
            namespace=namespace,
            body={
                "apiVersion": "authorization.k8s.io/v1",
                "kind": "LocalSubjectAccessReview",
                "spec": {
                    "user": f"system:serviceaccount:{namespace}:{sa}",
                    "resourceAttributes": {
                        "namespace": namespace,
                        "verb": verb,
                        "resource": resource,
                        "name": name,
                        **({"group": group} if group else {}),
                    },
                },
            },
        ),
    )

    return res.status.allowed if res.status else False


@attrs.define
class _ValidationVisitor:
    cluster_name: str | None = attrs.field(init=False, default=None)
    namespace: str | None = attrs.field(init=False, default=None)
    strict_access_review: bool = attrs.field(init=False, default=False)
    core_api: kubernetes.client.CoreV1Api | None = attrs.field(init=False, default=None)
    auth_api: kubernetes.client.AuthorizationV1Api | None = attrs.field(
        init=False, default=None
    )
    scheduling_api: kubernetes.client.SchedulingV1Api | None = attrs.field(
        init=False, default=None
    )

    @contextlib.contextmanager
    def with_namespace(self, namespace: str) -> Generator[None, None, None]:
        old = self.namespace
        self.namespace = namespace
        yield
        self.namespace = old

    @contextlib.contextmanager
    def with_cluster_name(self, cluster_name: str) -> Generator[None, None, None]:
        old = self.cluster_name
        self.cluster_name = cluster_name
        yield
        self.cluster_name = old

    @contextlib.contextmanager
    def with_strict_access_review(self, value: bool) -> Generator[None, None, None]:
        old = self.strict_access_review
        self.strict_access_review = value
        yield
        self.strict_access_review = old

    @contextlib.contextmanager
    def with_core_api(self, value) -> Generator[None, None, None]:
        old = self.core_api
        self.core_api = value
        yield
        self.core_api = old

    @contextlib.contextmanager
    def with_auth_api(self, value) -> Generator[None, None, None]:
        old = self.auth_api
        self.auth_api = value
        yield
        self.auth_api = old

    @contextlib.contextmanager
    def with_scheduling_api(self, value) -> Generator[None, None, None]:
        old = self.scheduling_api
        self.scheduling_api = value
        yield
        self.scheduling_api = old

    def _check_sa_access(self, sa: _ServiceAccountMixin) -> None:
        if sa.service_account is None:
            return
        assert self.auth_api is not None, "auth_api must be set"
        assert self.namespace is not None, "namespace must be set"
        # list all the role bindings on the service account
        # and check we have the correct permissions
        permissions_needed = [
            {
                "verb": "get",
                "resource": "pods",
                "name": "*",
            },
            {
                "verb": "list",
                "resource": "pods",
                "name": "*",
            },
            {
                "verb": "watch",
                "resource": "pods",
                "name": "*",
            },
            {
                "verb": "get",
                "resource": "rayclusters",
                "name": self.cluster_name,
                "group": "ray.io",
            },
            {
                "verb": "patch",
                "resource": "rayclusters",
                "name": self.cluster_name,
                "group": "ray.io",
            },
        ]
        checker = functools.partial(
            _can_i,
            auth_api=self.auth_api,
            namespace=self.namespace,
            sa=sa.service_account,
        )
        passed = True
        error_str = ""
        for perm in permissions_needed:
            if not checker(**perm):
                error_str += (
                    f"Service account {sa.service_account} does not have the "
                    f"required permission: {perm['verb']} {perm['resource']}"
                )
                passed = False
        if not passed:
            raise ValueError(error_str)

    def visit_service_account(self, sa: _ServiceAccountMixin) -> None:
        if sa.service_account is None:
            return

        assert self.core_api is not None, "core_api must be set"
        assert self.namespace is not None, "namespace must be set"

        # validate the service account exists
        try:
            service_account = cast(
                "client.V1ServiceAccount",
                self.core_api.read_namespaced_service_account(
                    name=sa.service_account, namespace=self.namespace
                ),
            )
        except kubernetes.client.exceptions.ApiException as e:
            if e.status == 404:
                raise ValueError(
                    f"Service account {sa.service_account} does not exist"
                ) from e
            raise e

        try:
            self._check_sa_access(sa)
        except ValueError:
            raise
        except Exception:
            if self.strict_access_review:
                raise
            _LOG.warn(
                "Skipping access review for service account %s due to exception",
                sa.service_account,
            )

        if (
            service_account.metadata is None
            or service_account.metadata.annotations is None
        ):
            raise ValueError(
                f"Service account {sa.service_account} does not have any annotations"
            )

        # TODO: need different modes of permission check here
        annotations = (
            service_account.metadata.annotations if service_account.metadata else {}
        )
        if (
            "iam.gke.io/gcp-service-account" not in annotations
            and "azure.workload.identity/client-id" not in annotations
            and "eks.amazonaws.com/role-arn" not in annotations
        ):
            raise ValueError(
                f"Service account {sa.service_account} does not have a "
                f"cloud service account or role"
            )

    def visit_priority_class(self, pri: _PriorityClassMixin) -> None:
        if pri.priority_class is None:
            return

        assert self.scheduling_api is not None, "scheduling_api must be set"

        # validate the priority class exists
        try:
            self.scheduling_api.read_priority_class(name=pri.priority_class)
        except kubernetes.client.exceptions.ApiException as e:
            if e.status == 404:
                raise ValueError(
                    f"Priority class {pri.priority_class} does not exist"
                ) from e
            raise e

    def visit_image(self, img: _ImageMixin) -> None:
        local_arch = platform.processor()

        # note: 1) this may not work for custom Ray images.
        # 2) Ray multi-platform images do not contain the arch suffix, but we don't
        # need to warn in that case
        is_img_arm = "aarch64" in img.image
        is_local_arm = local_arch in {"aarch64", "arm"}

        # log a warning if the image architecture differs from the
        # local CPU architecture
        if is_img_arm != is_local_arm:
            _LOG.debug(
                f"Ray image architecture does not match current architecture. "
                f"This may result in dependency errors on workers. Please ensure "
                f"the job manifest is using the same CPU architecture as the Ray "
                f"image. Ray image: {img.image} Current architecture: {local_arch}"
            )

    def visit_head_node(self, _: _HeadGroupSpec) -> None:
        pass

    def visit_worker_node(self, _: _WorkerGroupSpec) -> None:
        pass


T = TypeVar("T")


def ray_tqdm(iterable: Iterable[T], job_tracker, metric: str) -> Iterator[T]:
    for item in iterable:
        job_tracker.increment.remote(metric, 1)
        yield item
    job_tracker.mark_done.remote(metric)


def _fmt_groups(groups: list[WorkerGroupBrief]) -> str:
    if not groups:
        return ""
    parts = [f"{g['name']} {g['ready']}/{g['desired']}" for g in groups]
    return " | " + ", ".join(parts)


@attrs.define
class ClusterStatus:
    cluster_name: Optional[str] = attrs.field(default=None, init=False)
    namespace: Optional[str] = attrs.field(default=None, init=False)
    ray_cluster: Optional[RayCluster] = attrs.field(default=None, init=False)
    pbar_k8s = attrs.field(default=None, init=False)
    pbar_kuberay = attrs.field(default=None, init=False)

    def _ensure_ctx(self) -> None:
        if self.namespace and self.cluster_name:
            return
        rc = get_current_context()
        # "isinstance(RayCluster)" making sure it's not a LocalRayContext
        if rc is not None and isinstance(rc, RayCluster):
            # pull from active RayCluster context
            self.namespace = self.namespace or rc.namespace
            self.cluster_name = self.cluster_name or rc.name
            self.ray_cluster = rc
        # if still missing, fall back to your previous inference helpers
        if not self.namespace or not self.cluster_name:
            ns, cn = (None, None)
            self.namespace = self.namespace or ns
            self.cluster_name = self.cluster_name or cn

    def _update_k8s_pbar(self, s: KuberaySummary) -> None:
        k8s_desc = (
            f"{fmt('k8s', Colors.BRIGHT_MAGENTA, bold=True)} "
            f"{fmt(self.namespace or '', Colors.BRIGHT_CYAN)}: "
            f"{fmt_status_badge(s['phase'])} "
            f"({fmt('gpu/cpu nodes ready ', Colors.CYAN, bold=True)}"
            f"{fmt_numeric(s['workers_ready_gpu'])}/"
            f"{fmt_numeric(s['workers_ready_cpu'])}) "
            f"│ {fmt('pods running/pending/total', Colors.CYAN, bold=True)} "
            f"{fmt_numeric(s['running'], total=s['total_pods'])}/"
            f"{fmt_pending(s['pending'])}/"
            f"{fmt_numeric(s['total_pods'])} "
            f"({fmt('gpu', Colors.CYAN, bold=True)} "
            f"{fmt_numeric(s['pods_gpu_running'])}/"
            f"{fmt_pending(s['pods_gpu_pending'])} "
            f"{fmt('cpu', Colors.CYAN, bold=True)} "
            f"{fmt_numeric(s['pods_cpu_running'])}/"
            f"{fmt_pending(s['pods_cpu_pending'])}) "
        )

        if self.pbar_k8s is None:
            # no progress bar, just text)
            self.pbar_k8s = tqdm(total=0, bar_format="{desc} {bar:0}[{elapsed}]")

        self.pbar_k8s.desc = k8s_desc
        self.pbar_k8s.refresh()

    def _update_kuberay_pbar(self, s: KuberaySummary) -> None:
        scale_glyph_map = {
            "up": fmt("↑", Colors.BRIGHT_GREEN, bold=True),
            "down": fmt("↓", Colors.BRIGHT_RED, bold=True),
            "steady": fmt("→", Colors.BRIGHT_BLUE, bold=True),
        }
        scale_glyph = scale_glyph_map.get(s.get("kr_scaling") or "", "")

        # Format condition status
        cond = s.get("kr_last_condition")
        cond_str = f" {fmt(f'({cond[0]}/{cond[1]})', Colors.DIM)}" if cond else ""

        available_desired = fmt_numeric(
            s.get("kr_available_workers"), s.get("kr_desired_workers")
        )
        kr_desc = (
            f"{fmt('kuberay', Colors.BRIGHT_MAGENTA, bold=True)} "
            f"{fmt(self.cluster_name or '', Colors.BRIGHT_CYAN)}: "
            f"{fmt_status_badge(s.get('kr_state') or '')}{cond_str} "
            f"{scale_glyph} "
            f"│ {fmt('ray workers available/desired', Colors.CYAN, bold=True)} "
            f"{available_desired}/"
            f"{fmt_numeric(s.get('kr_desired_workers'))} "
            f"({fmt('gpu ready/pend', Colors.CYAN, bold=True)} "
            f"{fmt_numeric(s['nodes_gpu_ready'])}/"
            f"{fmt_pending(s['nodes_gpu_notready'])} "
            f"{fmt('cpu ready/pend', Colors.CYAN, bold=True)} "
            f"{fmt_numeric(s['nodes_cpu_ready'])}/"
            f"{fmt_pending(s['nodes_cpu_notready'])})"
        )

        if self.pbar_kuberay is None:
            self.pbar_kuberay = tqdm(total=0, bar_format="{desc} {bar:0}[{elapsed}]")

        self.pbar_kuberay.desc = kr_desc
        self.pbar_kuberay.refresh()

    def get_status(self) -> None:
        try:
            self._ensure_ctx()
            if not self.namespace or not self.cluster_name or not self.ray_cluster:
                return  # nothing we can do

            s = summarize_kuberay_status(
                self.ray_cluster.clients, self.namespace, self.cluster_name
            )
            if s is None:
                return  # cluster not found

            # k8s lane
            self._update_k8s_pbar(s)

            # kuberay lane
            self._update_kuberay_pbar(s)

        except Exception:
            _LOG.info("failed to get k8s node status")
            _LOG.debug("k8s exception:", exc_info=True)
            # do nothing

    def close(self) -> None:
        if self.pbar_kuberay is not None:
            self.pbar_kuberay.close()
            self.pbar_kuberay = None
        if self.pbar_k8s is not None:
            self.pbar_k8s.close()
            self.pbar_k8s = None
