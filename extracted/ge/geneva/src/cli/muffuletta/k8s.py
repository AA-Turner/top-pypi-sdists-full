# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Kubernetes client and port-forward utilities."""

import atexit
import contextlib
import socket
import subprocess
import time
from collections.abc import Generator
from contextlib import contextmanager
from datetime import datetime

from .models import RayCluster
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from rich.console import Console

from geneva.constants import DEFAULT_K8S_NS

console = Console(stderr=True)

CONSOLE_API_SERVICE = "geneva-console-api"
CONSOLE_API_PORT = 8000

# Global to track current context
_current_context: str | None = None


class KubernetesError(Exception):
    """Kubernetes-related error."""


def load_kubeconfig(context: str | None = None) -> str:
    """
    Load kubeconfig from default location.

    Args:
        context: Optional context name to use. If None, uses current context.

    Returns:
        The name of the context being used.
    """
    global _current_context

    try:
        contexts, active_context = config.list_kube_config_contexts()

        if context:
            # Verify the context exists
            context_names = [c["name"] for c in contexts]
            if context not in context_names:
                available = ", ".join(context_names)
                raise KubernetesError(
                    f"Context '{context}' not found. Available: {available}"
                )
            config.load_kube_config(context=context)
            _current_context = context
        else:
            config.load_kube_config()
            _current_context = active_context["name"]

        return _current_context

    except config.ConfigException as e:
        raise KubernetesError(
            f"Failed to load kubeconfig. Ensure ~/.kube/config exists and is valid: {e}"
        ) from e


def get_current_context() -> str | None:
    """Get the current context name."""
    return _current_context


def get_context() -> str:
    """Get the current context name, loading kubeconfig if needed."""
    global _current_context
    if _current_context is None:
        load_kubeconfig()
    return _current_context


def get_namespace() -> str:
    """Get current namespace from kubeconfig context."""
    try:
        _, active_context = config.list_kube_config_contexts()
        return active_context.get("context", {}).get("namespace", DEFAULT_K8S_NS)
    except Exception:
        return DEFAULT_K8S_NS


def get_console_api_service_target(
    namespace: str | None = None,
    context: str | None = None,
) -> tuple[str, str, str]:
    """
    Get the service target for the geneva-console-api.

    Args:
        namespace: Kubernetes namespace
        context: Kubernetes context name

    Returns:
        Tuple of (service_target, namespace, context_name)
    """
    ctx = load_kubeconfig(context)
    ns = namespace or get_namespace()
    return f"svc/{CONSOLE_API_SERVICE}", ns, ctx


def find_free_port() -> int:
    """Find a free port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@contextmanager
def port_forward(
    target: str,
    namespace: str,
    context: str | None = None,
    remote_port: int = CONSOLE_API_PORT,
    local_port: int | None = None,
) -> Generator[int, None, None]:
    """
    Create a port-forward to the specified Kubernetes resource.

    Args:
        target: Kubernetes resource to forward to (e.g. "svc/geneva-console-api")
        namespace: Kubernetes namespace
        context: Kubernetes context name
        remote_port: Port on the resource to forward
        local_port: Local port to use (auto-assigned if None)

    Yields:
        The local port number
    """
    if local_port is None:
        local_port = find_free_port()

    cmd = [
        "kubectl",
        "port-forward",
        target,
        f"{local_port}:{remote_port}",
        "-n",
        namespace,
    ]

    if context:
        cmd.extend(["--context", context])

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Register cleanup
    def cleanup() -> None:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()

    atexit.register(cleanup)

    # Wait for port-forward to be ready
    max_retries = 30
    for _ in range(max_retries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect(("localhost", local_port))
                break
        except (TimeoutError, OSError):
            if proc.poll() is not None:
                stderr = proc.stderr.read().decode() if proc.stderr else ""
                raise KubernetesError(f"Port-forward process died: {stderr}") from None
            time.sleep(0.2)
    else:
        proc.terminate()
        raise KubernetesError(
            f"Port-forward failed to become ready after {max_retries} retries"
        )

    try:
        yield local_port
    finally:
        cleanup()
        atexit.unregister(cleanup)


def list_ray_clusters(
    namespace: str | None = None,
    context: str | None = None,
) -> tuple[list[RayCluster], str]:
    """
    List RayClusters using the Kubernetes API.

    Args:
        namespace: Kubernetes namespace (uses current context namespace if None)
        context: Kubernetes context name

    Returns:
        Tuple of (list of RayCluster objects, context_name)
    """
    ctx = load_kubeconfig(context)
    custom_api = client.CustomObjectsApi()
    ns = namespace or get_namespace()

    try:
        result = custom_api.list_namespaced_custom_object(
            group="ray.io",
            version="v1",
            namespace=ns,
            plural="rayclusters",
        )
    except ApiException as e:
        if e.status == 404:
            raise KubernetesError(
                "RayCluster CRD not found. Is KubeRay operator installed?"
            ) from e
        raise KubernetesError(f"Failed to list RayClusters: {e.reason}") from e

    clusters = []
    for item in result.get("items", []):
        metadata = item.get("metadata", {})
        status = item.get("status", {})

        created_at = None
        if creation_ts := metadata.get("creationTimestamp"):
            with contextlib.suppress(ValueError):
                created_at = datetime.fromisoformat(creation_ts.replace("Z", "+00:00"))

        clusters.append(
            RayCluster(
                name=metadata.get("name", ""),
                namespace=metadata.get("namespace", ns),
                status=status.get("state", "Unknown"),
                head_pod=status.get("head", {}).get("podName"),
                worker_replicas=status.get("availableWorkerReplicas"),
                created_at=created_at,
            )
        )

    return clusters, ctx


def get_ray_cluster(
    name: str,
    namespace: str | None = None,
    context: str | None = None,
) -> tuple[RayCluster, str]:
    """
    Get a single RayCluster by name.

    Args:
        name: Name of the RayCluster
        namespace: Kubernetes namespace (uses current context namespace if None)
        context: Kubernetes context name

    Returns:
        Tuple of (RayCluster object, context_name)
    """
    ctx = load_kubeconfig(context)
    custom_api = client.CustomObjectsApi()
    ns = namespace or get_namespace()

    try:
        item = custom_api.get_namespaced_custom_object(
            group="ray.io",
            version="v1",
            namespace=ns,
            plural="rayclusters",
            name=name,
        )
    except ApiException as e:
        if e.status == 404:
            raise KubernetesError(
                f"RayCluster '{name}' not found in namespace '{ns}'"
            ) from e
        raise KubernetesError(f"Failed to get RayCluster '{name}': {e.reason}") from e

    metadata = item.get("metadata", {})
    status = item.get("status", {})

    created_at = None
    if creation_ts := metadata.get("creationTimestamp"):
        with contextlib.suppress(ValueError):
            created_at = datetime.fromisoformat(creation_ts.replace("Z", "+00:00"))

    cluster = RayCluster(
        name=metadata.get("name", ""),
        namespace=metadata.get("namespace", ns),
        status=status.get("state", "Unknown"),
        head_pod=status.get("head", {}).get("podName"),
        worker_replicas=status.get("availableWorkerReplicas"),
        created_at=created_at,
    )

    return cluster, ctx


def stream_pod_logs(
    pod_name: str,
    namespace: str | None = None,
    context: str | None = None,
    container: str | None = None,
    follow: bool = True,
    tail_lines: int | None = None,
) -> Generator[str, None, None]:
    """
    Stream logs from a pod.

    Args:
        pod_name: Name of the pod
        namespace: Kubernetes namespace
        context: Kubernetes context name
        container: Container name (optional)
        follow: Whether to follow/stream logs
        tail_lines: Number of lines to tail from the end

    Yields:
        Log lines as they come in
    """
    load_kubeconfig(context)
    v1 = client.CoreV1Api()
    ns = namespace or get_namespace()

    try:
        # Use watch for streaming
        for line in v1.read_namespaced_pod_log(
            name=pod_name,
            namespace=ns,
            container=container,
            follow=follow,
            tail_lines=tail_lines,
            _preload_content=False,
        ).stream():
            yield line.decode("utf-8").rstrip("\n")
    except ApiException as e:
        raise KubernetesError(
            f"Failed to stream logs from pod '{pod_name}': {e.reason}"
        ) from e


def get_job_pods(
    job_id: str,
    namespace: str | None = None,
    context: str | None = None,
) -> list[str]:
    """
    Get pod names associated with a Geneva job.

    Args:
        job_id: Geneva job ID
        namespace: Kubernetes namespace
        context: Kubernetes context name

    Returns:
        List of pod names
    """
    load_kubeconfig(context)
    v1 = client.CoreV1Api()
    ns = namespace or get_namespace()

    try:
        # Try to find pods with job label
        pods = v1.list_namespaced_pod(
            namespace=ns,
            label_selector=f"geneva.lancedb.com/job-id={job_id}",
        )

        if pods.items:
            return [pod.metadata.name for pod in pods.items]

        # Fallback: search by ray cluster name
        pods = v1.list_namespaced_pod(
            namespace=ns,
            label_selector=f"ray.io/cluster={job_id}",
        )

        return [pod.metadata.name for pod in pods.items]

    except ApiException as e:
        raise KubernetesError(
            f"Failed to list pods for job '{job_id}': {e.reason}"
        ) from e
