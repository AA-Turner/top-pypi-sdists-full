# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Integration tests for compare_ray_environments with real KubeRay clusters."""

import contextlib
import logging
import os
import time

import pytest
import ray

from geneva.cluster import K8sConfigMethod
from geneva.cluster.builder import KubeRayClusterBuilder, default_image
from geneva.db import Connection
from geneva.manifest import GenevaManifest
from geneva.runners.ray._mgr import _force_ray_cleanup
from geneva.runners.ray.compare_env import (
    compare_ray_environments,
    get_comparison_result,
)

_LOG = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def cluster_context(
    geneva_k8s_service_account: str,
    k8s_config_method: K8sConfigMethod,
    k8s_namespace: str,
    region: str,
    head_node_selector: dict,
    worker_node_selector: dict,
    k8s_cluster_name: str,
    session_db: Connection,
    slug: str | None,
) -> contextlib.AbstractContextManager:
    """Module-scoped fixture with pyarrow installed via pip on workers."""
    # Clean up any leftover Ray state from previous tests to avoid
    # "assert _internal_kv_initialized()" errors
    _force_ray_cleanup()

    cluster_name = f"compare-env-cluster-{slug}"
    manifest_name = f"compare-env-manifest-{slug}"
    img = default_image(arm=False)

    # Define cluster
    cluster_def = (
        KubeRayClusterBuilder.create(cluster_name)
        .namespace(k8s_namespace)
        .config_method(k8s_config_method)
        .aws_config(region=region, role_name="geneva-client-role")
        .portforwarding(True)
        .head_group(
            service_account=geneva_k8s_service_account,
            node_selector=head_node_selector,
            image=img,
        )
        .add_worker_group(
            KubeRayClusterBuilder.cpu_worker()
            .name("worker")
            .service_account(geneva_k8s_service_account)
            .node_selector(worker_node_selector)
            .image(img)
            .min_replicas(1)
            .build()
        )
        .build()
    )

    # Define manifest - avoid including local pyarrow (ARM) in py_modules.
    # This allows the test to run locally on an ARM driver
    manifest_def = (
        GenevaManifest.create_pip(manifest_name)
        .head_image(img)
        .worker_image(img)
        .upload_site_packages()
        .add_pip("pyarrow>=16.0.0")
        .add_pip("pylance>=6.0.0b1")
        .add_pip("lancedb>=0.31.0b9")
        .build()
    )

    try:
        session_db.define_cluster(cluster_name, cluster_def)
        session_db.define_manifest(manifest_name, manifest_def)

        _LOG.info(f"Starting compare-env cluster: {cluster_name}")
        with session_db.context(cluster=cluster_name, manifest=manifest_name):
            yield
    finally:
        with contextlib.suppress(Exception):
            session_db.delete_cluster(cluster_name)
        with contextlib.suppress(Exception):
            session_db.delete_manifest(manifest_name)


# todo: https://linear.app/lancedb/issue/GEN-330/enable-test-compare-env-integ-tests
@pytest.mark.skip("flaky in CI and does not run on MacOS")
class TestCompareEnvOnCluster:
    """Integration tests for compare_ray_environments on a real KubeRay cluster.

    All tests in this class share a single cluster context to avoid the overhead
    of creating/destroying clusters for each test.
    """

    def test_basic_comparison(self, cluster_context) -> None:
        """Test comparison against a real KubeRay cluster."""
        result = compare_ray_environments()

        # Verify result structure
        assert "local" in result
        assert "remote" in result
        assert "env_diffs" in result
        assert "pkg_diffs" in result

        # Should detect some differences between local and cluster
        env_diffs = result["env_diffs"]
        pkg_diffs = result["pkg_diffs"]

        _LOG.info(
            f"Real cluster comparison: {len(pkg_diffs['version_mismatch'])} "
            "package mismatches"
        )
        _LOG.info(
            f"Real cluster comparison: {len(env_diffs['diffs'])} env var differences"
        )
        _LOG.info(f"Packages only in remote: {len(pkg_diffs['only_remote'])}")
        _LOG.info(f"Packages only in local: {len(pkg_diffs['only_local'])}")

        # Cluster workers should have Ray
        assert "ray" in result["remote"]["packages"]

        # Log some interesting differences
        for key in env_diffs["only_remote"][:5]:  # First 5 remote-only vars
            _LOG.info(f"Remote-only env var: {key}")

    def test_runtime_env_detection(self, cluster_context) -> None:
        """Test that runtime_env differences are detected on real cluster."""

        # Create a remote function with custom runtime_env
        @ray.remote(runtime_env={"pip": ["emoji==2.15.0"]})
        def get_emoji_version() -> str:
            import emoji

            return emoji.__version__

        # Run it to ensure runtime_env is created
        version = ray.get(get_emoji_version.remote())
        _LOG.info(f"Remote emoji version: {version}")
        assert version == "2.15.0"

        # Compare environments
        result = get_comparison_result()

        # Log the differences
        pkg_diffs = result["pkg_diffs"]
        _LOG.info(
            f"With runtime_env: {len(pkg_diffs['version_mismatch'])} package mismatches"
        )

    def test_performance(self, cluster_context) -> None:
        """Ensure comparison completes in reasonable time on real cluster."""
        start = time.time()
        result = get_comparison_result()
        duration = time.time() - start

        _LOG.info(f"Comparison completed in {duration:.2f} seconds")

        # Should complete within 300 seconds even on real cluster
        assert duration < 300, f"Comparison took too long: {duration:.2f}s"

        # Verify we got results
        assert len(result["local"]["packages"]) > 0
        assert len(result["remote"]["packages"]) > 0

    def test_ray_env_vars(self, cluster_context) -> None:
        """Test detection of cluster-specific RAY environment variables."""
        result = get_comparison_result(env_prefix="RAY")

        env_diffs = result["env_diffs"]

        # Cluster workers should have RAY-prefixed env vars
        ray_vars_in_remote = [
            k for k in env_diffs["only_remote"] if k.startswith("RAY")
        ]
        _LOG.info(f"RAY env vars only in cluster: {len(ray_vars_in_remote)}")

        # Log some cluster-specific vars
        for var in ray_vars_in_remote[:10]:
            _LOG.info(f"  {var}")

        # Should have at least some RAY-specific vars in cluster
        assert len(ray_vars_in_remote) > 0

    def test_kubernetes_env_detection(self, cluster_context) -> None:
        """Test that Kubernetes-related env vars are detected in cluster."""
        result = get_comparison_result(env_prefix="KUBERNETES")

        env_diffs = result["env_diffs"]

        # Cluster should have KUBERNETES env vars (if running in K8s)
        k8s_vars = [k for k in env_diffs["only_remote"] if k.startswith("KUBERNETES")]

        if k8s_vars:
            _LOG.info(f"Found {len(k8s_vars)} Kubernetes env vars in cluster")
            for var in k8s_vars:
                _LOG.info(f"  {var}")
        else:
            _LOG.info("No Kubernetes env vars detected (cluster may not be in K8s)")

    def test_sys_path_comparison(self, cluster_context) -> None:
        """Test sys.path comparison on real cluster."""
        result = get_comparison_result()

        sys_path_diffs = result["sys_path_diffs"]

        _LOG.info(
            f"Cluster sys.path: {sys_path_diffs['local_count']} local, "
            f"{sys_path_diffs['remote_count']} remote, "
            f"{sys_path_diffs['intersection_count']} shared"
        )

        # Should have different paths between local and cluster
        assert len(sys_path_diffs["only_remote"]) > 0

        # Log some cluster-specific paths
        for path in sys_path_diffs["only_remote"][:5]:
            _LOG.info(f"  Remote-only path: {path}")

    def test_python_version_info(self, cluster_context) -> None:
        """Test that Python version info is captured correctly on cluster."""
        result = get_comparison_result()

        local_py = result["local"]["python"]
        remote_py = result["remote"]["python"]

        _LOG.info(f"Local Python: {local_py['version']}")
        _LOG.info(f"Remote Python: {remote_py['version']}")
        _LOG.info(f"Local executable: {local_py['executable']}")
        _LOG.info(f"Remote executable: {remote_py['executable']}")

        # Both should be Python 3.x
        assert local_py["version"].startswith("3.")
        assert remote_py["version"].startswith("3.")

        # Executables will likely be different paths
        _LOG.info(
            f"Executable paths differ: "
            f"{local_py['executable'] != remote_py['executable']}"
        )

    def test_local_only_env_vars(self, cluster_context) -> None:
        """Test that local-only environment variables are detected on real cluster."""
        # Set a unique environment variable locally
        os.environ["GENEVA_TEST_VAR"] = "local_value"

        try:
            result = get_comparison_result(env_prefix="GENEVA")

            env_diffs = result["env_diffs"]

            # GENEVA_TEST_VAR should be in only_local (cluster workers won't have it)
            assert "GENEVA_TEST_VAR" in env_diffs["only_local"]
            _LOG.info(
                f"Local-only env vars with GENEVA prefix: {env_diffs['only_local']}"
            )
        finally:
            # Cleanup
            del os.environ["GENEVA_TEST_VAR"]
