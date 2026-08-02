# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Shared pytest fixtures for integ_tests, stress_tests, and e2e_tests.

This file contains common fixtures used across all test suites.
Test-suite-specific fixtures are kept in their respective conftest.py files.
"""

import contextlib
import logging
import random
import warnings

import kubernetes
import pytest

from geneva.cluster import K8sConfigMethod
from geneva.cluster.builder import KubeRayClusterBuilder, default_image
from geneva.constants import DEFAULT_K8S_NS
from geneva.runners.ray._mgr import ray_cluster
from geneva.runners.ray.raycluster import ExitMode
from geneva.utils import dt_now_utc

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# it's okay, we are in a test
warnings.filterwarnings(
    "ignore", "Using port forwarding for Ray cluster is not recommended for production"
)
_LOG = logging.getLogger(__name__)


# ============================================================================
# Common pytest options
# ============================================================================


def pytest_addoption(parser) -> None:
    """Add common command-line options for all test suites."""
    parser.addoption(
        "--csp",
        action="store",
        default="gcp",
        choices=["gcp", "aws", "azure"],
        help="CSP to deploy to for tests (e.g., 'gcp', 'aws', 'azure')",
    )
    parser.addoption(
        "--test-slug",
        action="store",
        default=None,
        help="Test slug to identify a test run. Typically used to "
        "cleanup external resources like rayclusters",
    )
    parser.addoption(
        "--bucket-path",
        action="store",
        default=None,
        help="Bucket path to use for test data (e.g., gs://bucket/path or s3://bucket/path)",
    )
    parser.addoption(
        "--manifest",
        action="store",
        default=None,
        help="Optional custom manifest",
    )
    parser.addoption(
        "--kube-context",
        action="store",
        default=None,
        help="Kubernetes context name to use (default: "
        "current context from kubeconfig)",
    )


# ============================================================================
# Common fixtures
# ============================================================================


@pytest.fixture(autouse=True, scope="session")
def geneva_k8s_service_account(csp: str) -> str:
    """
    A preconfigured service account for the test session.
    This service account should have all the permissions needed to run the tests.
    """
    return "geneva-service-account"


@pytest.fixture(autouse=True, scope="session")
def bucket_name(request, slug) -> str:
    csp = request.config.getoption("--csp")
    if csp == "gcp":
        return "lancedb-lancedb-dev-us-central1"
    elif csp == "aws":
        return "geneva-integ-test-devland-us-east-1"
    elif csp == "azure":
        # storage account must be set via AZURE_STORAGE_ACCOUNT_NAME env var
        return "lancedbdatasets"
    else:
        raise ValueError(f"Unsupported --csp arg: {csp}")


@pytest.fixture(autouse=True, scope="session")
def geneva_test_bucket(request, slug, bucket_name: str) -> str:
    """
    Test bucket path - can be overridden with --bucket-path or defaults based on CSP.

    Falls back to default paths for local development if --bucket-path is not provided.
    """
    bucket_path = request.config.getoption("--bucket-path")

    if not bucket_path:
        csp = request.config.getoption("--csp")
        if csp == "gcp":
            bucket_path = f"gs://{bucket_name}/{slug}/data"
        elif csp == "aws":
            bucket_path = f"s3://{bucket_name}/{slug}/data"
        elif csp == "azure":
            bucket_path = f"az://{bucket_name}/{slug}/data"
        else:
            raise ValueError(f"Unsupported --csp arg: {csp}")
        _LOG.info(f"Using default bucket path: {bucket_path}")
    else:
        _LOG.info(f"Using provided bucket path: {bucket_path}")

    return bucket_path


@pytest.fixture(scope="session")
def csp(request, geneva_test_bucket: str) -> str:
    """
    Cloud service provider (gcp or aws).

    Also sets up Geneva config overrides for checkpoint and upload paths
    based on geneva_test_bucket.
    """
    from geneva.config import override_config_kv

    csp = request.config.getoption("--csp")

    # Derive upload and checkpoint paths from the bucket path
    # If bucket path is: gs://bucket/slug/data
    # Then: gs://bucket/slug/data/zips and gs://bucket/slug/data/checkpoints
    override_config_kv(
        {
            "job.checkpoint.mode": "object_store",
            "job.checkpoint.object_store.path": f"{geneva_test_bucket}/checkpoints",
        }
    )

    return csp


@pytest.fixture(scope="session")
def manifest(request) -> str | None:
    """
    Optionally use a saved manifest instead of uploading new
    manifest
    """

    try:
        return request.config.getoption("--manifest")
    except ValueError:
        return None


@pytest.fixture(scope="session")
def slug(request) -> str | None:
    """Test slug for identifying test runs and cleanup."""
    return request.config.getoption("--test-slug") or str(random.randint(0, 10000))  # type: ignore[return-value]


@pytest.fixture(scope="session")
def region(csp) -> str:
    """Default region for the CSP."""
    if csp == "aws":
        return "us-east-1"
    elif csp == "azure":
        return "eastus"
    else:
        return "us-central1"


@pytest.fixture(scope="session", autouse=True)
def kube_context(request) -> str | None:
    """Kubernetes context name from --kube-context option.

    When provided, loads kubeconfig with the specified context name.
    If not provided, loads the default context from KUBECONFIG
    """
    from kubernetes.config.kube_config import list_kube_config_contexts

    ctx = request.config.getoption("--kube-context")
    _LOG.info(f"Using k8s context: {ctx or 'default'}")
    # Try to load kubernetes config - only needed for integration/stress/e2e tests
    # Unit tests don't need this, so it's okay if it fails
    with contextlib.suppress(kubernetes.config.config_exception.ConfigException):
        kubernetes.config.load_kube_config(
            context=ctx,
        )
        _, active = list_kube_config_contexts()
        _LOG.info(f"Active k8s context: {active}")
    return ctx


@pytest.fixture(scope="session")
def k8s_config_method(csp) -> K8sConfigMethod:
    """Kubernetes config method based on CSP."""
    if csp == "aws":
        return K8sConfigMethod.EKS_AUTH
    # GCP and Azure both use LOCAL (kubeconfig-based auth)
    return K8sConfigMethod.LOCAL


@pytest.fixture(scope="session")
def k8s_namespace(csp) -> str:
    """Kubernetes namespace for Ray clusters."""
    # only used for EKS auth currently
    return DEFAULT_K8S_NS


@pytest.fixture(scope="session")
def k8s_cluster_name(csp) -> str:
    """Kubernetes cluster name."""
    # only used for EKS auth currently
    return "lancedb"


@pytest.fixture(scope="session")
def head_node_selector(csp: str) -> dict:
    """Node selector for Ray head nodes."""
    return {"geneva.lancedb.com/ray-head": "true"}


@pytest.fixture(scope="session")
def worker_node_selector(csp: str) -> dict:
    """Node selector for Ray worker nodes (CPU)."""
    return {"geneva.lancedb.com/ray-worker-cpu": "true"}


@pytest.fixture(scope="session")
def num_gpus() -> int:
    """Number of GPUs required for tests (default: 0)."""
    return 0


@pytest.fixture(scope="module")
def standard_cluster(
    geneva_k8s_service_account: str,
    k8s_config_method: K8sConfigMethod,
    k8s_namespace: str,
    csp: str,
    region: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    k8s_cluster_name: str,
    slug: str | None,
) -> contextlib.AbstractContextManager:
    """Standard Ray cluster for integration and e2e tests.

    Module-scoped to allow tests in the same module to share a single cluster."""
    ray_cluster_name = "test-cluster"
    ray_cluster_name += f"-{dt_now_utc().strftime('%Y-%m-%d-%H-%M')}-{slug}"

    _LOG.info(f"creating ray cluster {ray_cluster_name}")

    # IMPORTANT: min_replicas must be ≥1 for worker groups with custom resources.
    #
    # Background: Workers with num_gpus=0 advertise a custom Ray resource via
    # rayStartParams (see raycluster.py:462-465). Each worker advertises
    # 100,000 units of the "cpu-only" custom resource to Ray.
    #
    # The Problem (Resource Discovery Bootstrapping):
    # 1. With min_replicas=0, cluster starts with zero workers
    # 2. Ray custom resources are only advertised by running workers
    # 3. When actors request cpu-only resources, Ray reports demand to autoscaler
    # 4. Kuberay autoscaler v2 cannot determine which worker group provides
    #    "cpu-only" resource because no workers are running to advertise it
    # 5. Autoscaler doesn't know which group to scale up → deadlock
    #
    # The Solution:
    # - min_replicas=1 ensures at least one worker is always running
    # - This worker advertises the cpu-only custom resource to Ray
    # - Autoscaler can now match resource demand to the correct worker group
    # - Additional workers scale up normally based on demand
    #
    # References:
    # - Ray custom resources: https://docs.ray.io/en/latest/ray-core/scheduling/resources.html
    # - Kuberay autoscaling: https://docs.ray.io/en/latest/cluster/kubernetes/user-guides/configuring-autoscaling.html
    # - Related issue: test_ray_add_column_pipeline_cpu_only_pool hung for 1.5+ hours
    #   when min_replicas=0, causing 10% of integration test failures

    # Build cluster using KubeRayClusterBuilder
    geneva_cluster = (
        KubeRayClusterBuilder.create(ray_cluster_name)
        .namespace(k8s_namespace)
        .config_method(k8s_config_method)
        .aws_config(region=region, role_name="geneva-client-role")
        .portforwarding(True)
        .head_group(
            cpus=1,
            memory="8Gi",
            service_account=geneva_k8s_service_account,
            node_selector=head_node_selector,
            image=default_image(arm=False),
        )
        .add_worker_group(
            KubeRayClusterBuilder.cpu_worker()
            .name("worker")
            .cpus(2)
            .memory("16Gi")
            .service_account(geneva_k8s_service_account)
            .node_selector(worker_node_selector)
            .image(default_image(arm=False))
            .min_replicas(1)  # Critical: must be ≥1 for custom resources
            .build()
        )
        .build()
    )

    # I guess we can't yet set *everything* using the builders, so still convert
    # it and use ray_cluster() here :-/
    rc = geneva_cluster.to_ray_cluster()
    rc.on_exit = ExitMode.DELETE
    rc.cluster_name = k8s_cluster_name

    return ray_cluster(
        ray_cluster=rc,
        use_portforwarding=True,
        skip_site_packages=False,
        extra_env={
            "RAY_BACKEND_LOG_LEVEL": "info",
            "RAY_LOG_TO_DRIVER": "1",
            "RAY_ENABLE_RECORD_ACTOR_TASK_LOGGING": "1",
            "RAY_RUNTIME_ENV_LOG_TO_DRIVER_ENABLED": "true",
        },
        log_to_driver=True,
        logging_level=logging.INFO,
    )


@pytest.fixture
def beefy_cluster(
    geneva_k8s_service_account: str,
    k8s_config_method: K8sConfigMethod,
    k8s_namespace: str,
    csp: str,
    region: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    k8s_cluster_name: str,
    slug: str | None,
    geneva_test_bucket: str,
) -> contextlib.AbstractContextManager:
    """Large Ray cluster for stress/e2e tests with high CPU/memory workers."""
    import geneva
    from geneva.manifest.mgr import ManifestConfigManager

    ray_cluster_name = "beefy-cluster"
    ray_cluster_name += f"-{dt_now_utc().strftime('%Y-%m-%d-%H-%M')}-{slug}"

    _LOG.info(f"creating beefy ray cluster {ray_cluster_name}")

    db = geneva.connect(geneva_test_bucket)
    ManifestConfigManager(db).get_table()
    uploader = db._default_manifest_uploader()
    img = default_image(arm=False)

    geneva_cluster = (
        KubeRayClusterBuilder.create(ray_cluster_name)
        .namespace(k8s_namespace)
        .config_method(k8s_config_method)
        .aws_config(region=region, role_name="geneva-client-role")
        .portforwarding(True)
        .head_group(
            cpus=1,
            memory="8Gi",
            service_account=geneva_k8s_service_account,
            node_selector=head_node_selector,
            image=img,
        )
        .add_worker_group(
            KubeRayClusterBuilder.cpu_worker()
            .name("worker")
            .cpus(14)
            .memory("56Gi")
            .service_account(geneva_k8s_service_account)
            .node_selector(worker_node_selector)
            .image(img)
            .min_replicas(0)
            .build()
        )
        .build()
    )

    rc = geneva_cluster.to_ray_cluster()
    rc.on_exit = ExitMode.DELETE
    rc.cluster_name = k8s_cluster_name

    return ray_cluster(
        ray_cluster=rc,
        use_portforwarding=True,
        skip_site_packages=False,
        uploader=uploader,
        extra_env={
            "LANCE_IO_THREADS": "4",
            "LANCE_PROCESS_IO_THREADS_LIMIT": "8",
        },
    )
