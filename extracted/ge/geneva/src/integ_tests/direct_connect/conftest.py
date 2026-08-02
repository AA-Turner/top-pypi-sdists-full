# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Direct-connect integration test fixtures.

This file provides fixtures for testing Geneva's ability to connect to
pre-existing Ray clusters without managing cluster lifecycle.

Architecture: Hybrid Mode
- Kuberay provisions a cluster once per test session (for CI convenience)
- Port forwarding provides network access to the cluster
- Geneva connects via address parameter (simulating direct connect pattern)
- Tests run against the shared cluster
- Cleanup happens after entire session completes

This mimics the customer pattern where:
1. DevOps provisions a Ray cluster via kuberay (or other means)
2. Geneva application code connects to it as an external resource
3. Geneva does NOT manage cluster lifecycle (no create/delete)

Note: While we use port forwarding for CI access, the key difference from
standard tests is that the cluster lifecycle is managed separately from
the Ray connection - tests use init_ray(addr=...) directly rather than
the ray_cluster() context manager that provisions clusters.
"""

import logging
from collections.abc import Generator

import pytest
from tenacity import (
    retry,
    stop_after_delay,
    wait_fixed,
)

import geneva
from geneva.cluster import GenevaCluster, K8sConfigMethod
from geneva.cluster.builder import KubeRayClusterBuilder, default_image
from geneva.manifest import GenevaManifest
from geneva.runners.ray._portforward import PortForward
from geneva.runners.ray.raycluster import (
    ExitMode,
    RayCluster,
)
from geneva.utils import dt_now_utc

_LOG = logging.getLogger(__name__)


class _WorkersNotReadyError(Exception):
    """Raised when workers are not yet ready, triggering a retry."""


def _wait_for_workers(
    cluster: "RayCluster",
    expected_workers: int,
    timeout_s: float = 600.0,
) -> None:
    """Wait for all workers to be ready before proceeding with tests.

    Args:
        cluster: The RayCluster to wait on
        expected_workers: Number of workers expected to be ready
        timeout_s: Maximum time to wait in seconds. Default 10 minutes.

    Raises:
        TimeoutError: If workers are not ready within timeout.
    """

    @retry(
        stop=stop_after_delay(timeout_s),
        wait=wait_fixed(5),
        reraise=True,
    )
    def _check_workers() -> None:
        result = cluster.clients.custom_api.get_namespaced_custom_object(
            group="ray.io",
            version="v1",
            namespace=cluster.namespace,
            plural="rayclusters",
            name=cluster.name,
        )
        status = result.get("status", {})
        # KubeRay reports availableWorkerReplicas when workers are ready
        available = status.get("availableWorkerReplicas", 0)
        desired = status.get("desiredWorkerReplicas", expected_workers)

        if available >= expected_workers:
            _LOG.info(
                f"All {available} workers are ready "
                f"(desired: {desired}, expected: {expected_workers})"
            )
            return

        _LOG.info(f"Waiting for workers: {available}/{expected_workers} ready")
        raise _WorkersNotReadyError()

    try:
        _check_workers()
    except _WorkersNotReadyError:
        raise TimeoutError(
            f"Timed out waiting for {expected_workers} workers to be ready "
            f"after {timeout_s:.0f}s"
        ) from None


@pytest.fixture(scope="session")
def direct_connect_default_manifest(slug: str) -> GenevaManifest:
    """Full manifest with pip dependencies for direct-connect tests.

    Direct-connect tests require runtime dependencies to be installed
    on the remote cluster since we connect to a pre-existing cluster.
    """
    manifest_name = "direct-connect-manifest"
    if slug:
        manifest_name += f"-{slug}"

    return (
        GenevaManifest.create_pip(manifest_name)
        # always use x86 images even if running tests on arm64
        # all of our integ test environments use x86
        .head_image(default_image(arm=False))
        .worker_image(default_image(arm=False))
        .add_pip("pyarrow>=16.0.0")
        # Geneva requires lance/pylance/lancedb for data operations
        .add_pip("pylance>=6.0.0b1")
        .add_pip("lancedb>=0.31.0b9")
        .add_pip("lance-namespace>=0.2.1")
        # Geneva runtime dependencies needed by workers
        .add_pip("more-itertools")
        .add_pip("tenacity")
        .add_pip("attrs>=23,<25")
        .add_pip("cloudpickle")
        .add_pip("yarl")
        .add_pip("tqdm")
        .add_pip("emoji")
        .add_pip("overrides")
        .add_pip("toml")
        .add_pip("multiprocess")
        # kubernetes is imported at module level by raycluster.py/kuberay.py
        # even though workers don't need k8s functionality
        .add_pip("kubernetes")
        .add_pip("requests-oauthlib")  # kubernetes dependency
        .add_pip("google-auth")  # kubernetes dependency for GCP
        .build()
    )


@pytest.fixture(scope="session")
def direct_connect_session_manifest(
    geneva_test_bucket: str,
    direct_connect_default_manifest: GenevaManifest,
    manifest: str | None,  # optional custom manifest via --manifest
) -> Generator[str, None, None]:
    """Upload and save direct-connect manifest per-session and return the name.

    Cleans up after test session ends.
    """
    # use custom manifest name if passed to tests with --manifest arg
    if manifest:
        yield manifest
    else:
        db = geneva.connect(geneva_test_bucket)

        # package and upload the manifest
        db.define_manifest(
            direct_connect_default_manifest.name,
            direct_connect_default_manifest,
        )

        yield direct_connect_default_manifest.name
        db.delete_manifest(direct_connect_default_manifest.name)


@pytest.fixture(scope="session")
def direct_connect_ray_cluster(
    geneva_k8s_service_account: str,
    k8s_config_method: K8sConfigMethod,
    k8s_namespace: str,
    csp: str,
    region: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    k8s_cluster_name: str,
    slug: str | None,
) -> Generator[RayCluster, None, None]:
    """
    Session-scoped Ray cluster for direct-connect tests.

    Provisions a kuberay cluster once for the entire test session.
    The cluster is kept alive during all tests and deleted on session teardown.

    Unlike standard integration test fixtures that create/delete clusters per test,
    this fixture provisions once and reuses - mimicking how customers deploy.
    """
    ray_cluster_name = f"direct-connect-{dt_now_utc().strftime('%Y-%m-%d-%H-%M')}"
    if slug:
        ray_cluster_name += f"-{slug}"

    _LOG.info(
        f"Provisioning session Ray cluster for direct-connect tests: {ray_cluster_name}"
    )

    # Fixed-size worker pool: 4 workers with no autoscaling.
    # Setting min_replicas == max_replicas disables autoscaling.
    num_workers = 4
    img = default_image(arm=False)
    gc = (
        GenevaCluster.create_kuberay(ray_cluster_name)
        .namespace(k8s_namespace)
        .config_method(k8s_config_method)
        .aws_config(region, "geneva-client-role")
        .head_group(
            image=img,
            node_selector=head_node_selector,
            service_account=geneva_k8s_service_account,
        )
        .add_worker_group(
            KubeRayClusterBuilder.cpu_worker()
            .image(img)
            .replicas(num_workers)
            .min_replicas(num_workers)
            .max_replicas(num_workers)
            .node_selector(worker_node_selector)
            .service_account(geneva_k8s_service_account)
            .build()
        )
        .build()
    )

    cluster = gc.to_ray_cluster()

    # Keep cluster alive during session
    cluster.on_exit = ExitMode.RETAIN

    # Provision the cluster and get head IP
    head_ip = cluster.apply()
    _LOG.info(f"Session cluster provisioned with head IP: {head_ip}")

    # Wait for all workers to be ready before proceeding with tests.
    # This ensures admission control sees the full cluster capacity.
    _wait_for_workers(cluster, expected_workers=num_workers)

    yield cluster

    # Cleanup after entire session
    _LOG.info(f"Cleaning up session Ray cluster: {ray_cluster_name}")
    cluster.delete()


@pytest.fixture(scope="session")
def direct_connect_port_forward(
    direct_connect_ray_cluster: RayCluster,
) -> Generator[PortForward, None, None]:
    """
    Session-scoped port forward to the Ray head node.

    Sets up port forwarding once for the entire test session.
    This provides network access to the cluster from CI environments.
    """
    _LOG.info("Setting up port forwarding to Ray head node")
    pf = PortForward.to_head_node(direct_connect_ray_cluster)

    with pf:
        _LOG.info(f"Port forwarding established on localhost:{pf.local_port}")
        yield pf

    _LOG.info("Port forwarding closed")


@pytest.fixture(scope="session")
def direct_connect_ray_address(direct_connect_port_forward: PortForward) -> str:
    """
    Ray address for direct connection via port forward.

    Returns a ray:// URI pointing to the port-forwarded local port.
    """
    ray_addr = f"ray://localhost:{direct_connect_port_forward.local_port}"
    _LOG.info(f"Direct connect address: {ray_addr}")
    return ray_addr


@pytest.fixture(scope="session")
def direct_connect_manifest(
    geneva_test_bucket: str,
    direct_connect_session_manifest: str,
) -> GenevaManifest:
    """
    Load the direct-connect manifest for tests.

    Uses the direct_connect_session_manifest fixture which has all
    pip dependencies needed for direct-connect mode.
    """
    from geneva.manifest.mgr import ManifestConfigManager

    db = geneva.connect(geneva_test_bucket)
    # Initialize manifest manager (it's lazily created)
    manifest_manager = ManifestConfigManager(db)
    manifest_def = manifest_manager.load(direct_connect_session_manifest)
    if manifest_def is None:
        raise RuntimeError(
            f"Direct-connect manifest '{direct_connect_session_manifest}' not found"
        )
    return manifest_def


@pytest.fixture
def direct_connect_context(
    geneva_test_bucket: str,
    direct_connect_ray_address: str,
    direct_connect_session_manifest: str,
) -> Generator[None, None, None]:
    """
    Context manager for tests using direct connect to session cluster.

    Unlike standard_cluster, this:
    1. Connects to existing cluster (no provisioning)
    2. Does NOT manage cluster lifecycle
    3. Uses init_ray(addr=...) directly, via db.context()

    This is the primary fixture tests should use. It simulates the customer
    pattern of connecting to a pre-existing Ray cluster.
    """
    _LOG.info(f"Connecting to Ray cluster at {direct_connect_ray_address}")

    db = geneva.connect(geneva_test_bucket)

    # Direct connect mode to "external" cluster
    ext_name = "direct-connect-external"
    ext_cluster = GenevaCluster.create_external(
        ext_name, direct_connect_ray_address
    ).build()
    db.define_cluster(ext_name, ext_cluster)

    with db.context(cluster=ext_name, manifest=direct_connect_session_manifest):
        _LOG.info("Direct connect Ray context established")
        yield

    _LOG.info("Direct connect Ray context closed")
