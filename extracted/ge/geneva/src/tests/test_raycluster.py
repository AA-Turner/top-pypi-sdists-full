# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
from collections.abc import Generator
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any
from unittest.mock import Mock, patch

import pytest
import ray
import yaml

try:
    from geneva.constants import DEFAULT_K8S_NS
    from geneva.runners.ray import raycluster
    from geneva.runners.ray.raycluster import (
        _DEFAULT_LANCE_LOG,
        ClusterStatus,
        RayCluster,
        _HeadGroupSpec,
        _WorkerGroupSpec,
    )
except ImportError:
    pytest.skip("failed to import geneva.runners.ray", allow_module_level=True)

ClusterStatus = raycluster.ClusterStatus
RayCluster = raycluster.RayCluster
_DEFAULT_LANCE_LOG = raycluster._DEFAULT_LANCE_LOG
_HeadGroupSpec = raycluster._HeadGroupSpec
_WorkerGroupSpec = raycluster._WorkerGroupSpec

if TYPE_CHECKING:
    from geneva.runners.ray.kuberay import KuberaySummary

# Disable real k8s client init in attrs post_init for serialization tests
RayCluster.__attrs_post_init__ = lambda self: None


@pytest.fixture(autouse=True)
def ensure_ray_shutdown() -> Generator[None, None, None]:
    """Ensure Ray is shut down before and after each test"""
    if ray.is_initialized():
        ray.shutdown()
    yield
    if ray.is_initialized():
        ray.shutdown()


class DummyCM:
    def __init__(self, data: dict[str, str]) -> None:
        self.data = data


def test_env_vars_in_head_and_worker() -> None:
    """Test that env_vars can be set on both head and worker groups and
    appear in pod definition"""
    head = _HeadGroupSpec(
        env_vars={
            "GCS_REQUEST_CONNECTION_TIMEOUT_SECS": "300",
            "GCS_REQUEST_TIMEOUT_SECS": "600",
            "CUSTOM_VAR": "value",
        }
    )
    worker = _WorkerGroupSpec(
        env_vars={
            "GCS_REQUEST_CONNECTION_TIMEOUT_SECS": "300",
            "GCS_REQUEST_TIMEOUT_SECS": "600",
            "WORKER_VAR": "worker_value",
        }
    )

    cluster = RayCluster(
        name="test-env-vars", namespace="test", head_group=head, worker_groups=[worker]
    )

    # Check head group container env vars in the generated definition
    head_spec = cluster.definition["spec"]["headGroupSpec"]
    head_container = head_spec["template"]["spec"]["containers"][0]
    assert "env" in head_container
    head_env = {env["name"]: env["value"] for env in head_container["env"]}
    assert head_env["GCS_REQUEST_CONNECTION_TIMEOUT_SECS"] == "300"
    assert head_env["GCS_REQUEST_TIMEOUT_SECS"] == "600"
    assert head_env["CUSTOM_VAR"] == "value"
    # 3 custom env vars + 1 default (LANCE_LOG)
    assert len(head_env) == 4

    # Check worker group container env vars in the generated definition
    worker_spec = cluster.definition["spec"]["workerGroupSpecs"][0]
    worker_container = worker_spec["template"]["spec"]["containers"][0]
    assert "env" in worker_container
    worker_env = {env["name"]: env["value"] for env in worker_container["env"]}
    # Worker has 3 default env vars (RAY_memory_usage_threshold,
    # RAY_memory_monitor_refresh_ms, LANCE_LOG) plus the 3 custom ones
    assert worker_env["GCS_REQUEST_CONNECTION_TIMEOUT_SECS"] == "300"
    assert worker_env["GCS_REQUEST_TIMEOUT_SECS"] == "600"
    assert worker_env["WORKER_VAR"] == "worker_value"
    assert worker_env["RAY_memory_usage_threshold"] == "0.9"
    assert worker_env["RAY_memory_monitor_refresh_ms"] == "0"
    assert len(worker_env) == 6


def test_env_vars_empty() -> None:
    """Test that empty env_vars dict produces empty env list"""
    head = _HeadGroupSpec(env_vars={})
    worker = _WorkerGroupSpec(env_vars={})

    cluster = RayCluster(
        name="test-empty-env", namespace="test", head_group=head, worker_groups=[worker]
    )

    # Check head group has only default LANCE_LOG env var
    head_spec = cluster.definition["spec"]["headGroupSpec"]
    head_container = head_spec["template"]["spec"]["containers"][0]
    head_env = {env["name"]: env["value"] for env in head_container["env"]}
    assert head_env["LANCE_LOG"] == _DEFAULT_LANCE_LOG
    assert len(head_env) == 1

    # Check worker group has only default env vars
    worker_spec = cluster.definition["spec"]["workerGroupSpecs"][0]
    worker_container = worker_spec["template"]["spec"]["containers"][0]
    worker_env = {env["name"]: env["value"] for env in worker_container["env"]}
    assert worker_env["RAY_memory_usage_threshold"] == "0.9"
    assert worker_env["RAY_memory_monitor_refresh_ms"] == "0"
    assert worker_env["LANCE_LOG"] == _DEFAULT_LANCE_LOG
    assert len(worker_env) == 3


def test_default_lance_log_suppresses_engine_noise() -> None:
    """Default LANCE_LOG mutes LanceDB internals with no user audience."""
    # DataReplacement transaction warnings and the lance::events::* telemetry
    # are suppressed unconditionally, keeping the base info level.
    assert _DEFAULT_LANCE_LOG.startswith("info")
    assert "lance::dataset::transaction=error" in _DEFAULT_LANCE_LOG
    assert "lance::events=warn" in _DEFAULT_LANCE_LOG


def test_env_vars_serialization_to_config_map() -> None:
    """Test that env_vars are preserved in ConfigMap serialization"""
    head = _HeadGroupSpec(
        image="img",
        num_cpus=1,
        memory="4Gi",
        env_vars={"HEAD_VAR": "head_value"},
    )
    worker = _WorkerGroupSpec(
        image="img",
        num_cpus=2,
        memory="8Gi",
        env_vars={"WORKER_VAR": "worker_value"},
    )

    _ = RayCluster(
        name="test-env-serialization",
        namespace="ns",
        head_group=head,
        worker_groups=[worker],
    )


def test_cluster_status_get_status_happy_path() -> None:
    head = _HeadGroupSpec(image="test-img", num_cpus=1, memory="4Gi")
    worker = _WorkerGroupSpec(image="test-img", num_cpus=2, memory="8Gi")

    mock_ray_cluster = RayCluster(
        name="test-cluster",
        namespace="test-namespace",
        head_group=head,
        worker_groups=[worker],
    )

    mock_clients = Mock()
    mock_ray_cluster.clients = mock_clients

    mock_summary: KuberaySummary = {
        "phase": "Running",
        "phase_idx": 3,
        "pending": 0,
        "running": 3,
        "workers_ready": 2,
        "workers_ready_gpu": 1,
        "workers_ready_cpu": 1,
        "pods_gpu_running": 1,
        "pods_gpu_pending": 0,
        "pods_cpu_running": 2,
        "pods_cpu_pending": 0,
        "waits_top3": [],
        "pulling": 0,
        "total_pods": 3,
        "kr_state": "running",
        "kr_desired_workers": 2,
        "kr_available_workers": 2,
        "kr_scaling": "steady",
        "kr_last_condition": ("Ready", "True"),
        "nodes_gpu_ready": 1,
        "nodes_gpu_notready": 0,
        "nodes_cpu_ready": 1,
        "nodes_cpu_notready": 0,
    }

    cluster_status = ClusterStatus()
    cluster_status.namespace = "test-namespace"
    cluster_status.cluster_name = "test-cluster"
    cluster_status.ray_cluster = mock_ray_cluster

    # Mock the summarize_kuberay_status function
    with patch(
        "geneva.runners.ray.raycluster.summarize_kuberay_status"
    ) as mock_summarize:
        mock_summarize.return_value = mock_summary

        # Mock tqdm to avoid actual progress bar creation
        with patch("geneva.runners.ray.raycluster.tqdm") as mock_tqdm:
            mock_pbar = Mock()
            mock_tqdm.return_value = mock_pbar

            # Call get_status()
            cluster_status.get_status()

            # Verify summarize_kuberay_status was called with correct parameters
            mock_summarize.assert_called_once_with(
                mock_clients, "test-namespace", "test-cluster"
            )

            # Verify progress bars were created
            assert cluster_status.pbar_k8s is not None
            assert cluster_status.pbar_kuberay is not None

            # Verify progress bar refresh was called for both bars
            assert mock_pbar.refresh.call_count == 2  # Called for both k8s and kuberay

            # Verify that progress bar descriptions were set
            # The desc attribute should have been set
            assert hasattr(mock_pbar, "desc")

            # Verify that tqdm was called twice (once for k8s, once for kuberay)
            assert mock_tqdm.call_count == 2


def test_wait_for_tracked_jobs_skips_tracker_confirmation_after_failure() -> None:
    cluster = RayCluster(name="test-cluster", namespace="test")
    failed_ref = object()
    tracker = Mock()
    cluster._tracked_refs = [("job-1", failed_ref, tracker)]

    with (
        patch("geneva.runners.ray.raycluster.ray.is_initialized", return_value=True),
        patch(
            "geneva.runners.ray.raycluster.ray.wait", return_value=([failed_ref], [])
        ),
        patch(
            "geneva.runners.ray.raycluster.ray.get",
            side_effect=RuntimeError("worker failed"),
        ),
        patch.object(
            cluster,
            "_is_tracker_done",
            side_effect=AssertionError("tracker should not be queried"),
        ),
        patch("geneva.runners.ray.raycluster._LOG.info"),
        patch("geneva.runners.ray.raycluster._LOG.warning"),
    ):
        assert cluster._wait_for_tracked_jobs() is True


def test_env_vars_serialization_to_config_map_continued() -> None:
    """Test that env_vars are preserved in ConfigMap serialization - continuation"""
    head = _HeadGroupSpec(
        image="img",
        num_cpus=1,
        memory="4Gi",
        env_vars={"HEAD_VAR": "head_value"},
    )
    worker = _WorkerGroupSpec(
        image="img",
        num_cpus=2,
        memory="8Gi",
        env_vars={"WORKER_VAR": "worker_value"},
    )

    cluster = RayCluster(
        name="test-env-serialization",
        namespace="ns",
        head_group=head,
        worker_groups=[worker],
    )

    data = cluster.to_config_map()
    h = yaml.safe_load(data["head_group"])
    assert h["env_vars"] == {"HEAD_VAR": "head_value"}

    ws = yaml.safe_load(data["worker_groups"])
    assert ws[0]["env_vars"] == {"WORKER_VAR": "worker_value"}


def test_env_vars_deserialization_from_config_map(monkeypatch) -> None:
    """Test that env_vars are properly loaded from ConfigMap"""
    dummy_data = {
        "name": "env-vars-cluster",
        "head_group": yaml.dump(
            {
                "image": "ray:latest",
                "num_cpus": 2,
                "memory": "4Gi",
                "env_vars": {"HEAD_ENV": "head_val"},
            }
        ),
        "worker_groups": yaml.dump(
            [
                {
                    "image": "ray:latest",
                    "num_cpus": 4,
                    "memory": "8Gi",
                    "env_vars": {"WORKER_ENV": "worker_val"},
                }
            ]
        ),
    }
    cm = DummyCM(dummy_data)

    monkeypatch.setattr(
        "geneva.runners.kuberay.client.build_api_client",
        lambda *args: None,
    )

    class DummyCore:
        def read_namespaced_config_map(self, name: str, namespace: str) -> DummyCM:
            return cm

    monkeypatch.setattr(
        "geneva.runners.ray.raycluster.kubernetes.client.CoreV1Api",
        lambda api_client=None: DummyCore(),
    )

    cluster = RayCluster.from_config_map(
        "my-namespace", "my-k8s-cluster", "cm-name", "env-vars-cluster"
    )

    assert cluster.head_group.env_vars == {"HEAD_ENV": "head_val"}
    assert cluster.worker_groups[0].env_vars == {"WORKER_ENV": "worker_val"}


def test_extra_env_passed_to_init_ray(monkeypatch) -> None:
    """Test that extra_env parameter is passed through ray_cluster to init_ray

    This test verifies that extra_env variables are correctly passed through the
    ray_cluster context manager to init_ray, where they become part of Ray's
    runtime environment. These variables will be available in Ray worker processes
    when executing tasks/actors on both head and worker nodes.
    """

    import geneva.runners.ray._mgr as ray_mgr_mod

    ray_init_called = {}

    # Mock ray.init to capture the runtime_env
    def mock_ray_init(*args: Any, **kwargs: Any) -> None:
        ray_init_called["args"] = args
        ray_init_called["kwargs"] = kwargs

    monkeypatch.setattr("ray.init", mock_ray_init)
    monkeypatch.setattr("ray.shutdown", lambda: None)
    monkeypatch.setattr("ray.is_initialized", lambda: False)

    # Test with local ray cluster to avoid kubernetes dependencies
    extra_env_vars = {
        "GCS_REQUEST_CONNECTION_TIMEOUT_SECS": "300",
        "GCS_REQUEST_TIMEOUT_SECS": "600",
        "CUSTOM_ENV_VAR": "custom_value",
    }

    with ray_mgr_mod.ray_cluster(local=True, extra_env=extra_env_vars):
        pass

    # Verify ray.init was called with correct runtime_env
    assert "kwargs" in ray_init_called
    runtime_env = ray_init_called["kwargs"]["runtime_env"]

    # Check that extra_env variables are in the runtime_env
    assert "env_vars" in runtime_env
    env_vars = runtime_env["env_vars"]

    # Verify our custom env vars are present
    assert env_vars["GCS_REQUEST_CONNECTION_TIMEOUT_SECS"] == "300"
    assert env_vars["GCS_REQUEST_TIMEOUT_SECS"] == "600"
    assert env_vars["CUSTOM_ENV_VAR"] == "custom_value"

    # GENEVA_ZIPS should also be present (added by init_ray)
    assert "GENEVA_ZIPS" in env_vars


def test_init_ray_includes_zip_namespace(monkeypatch) -> None:
    import base64
    import json

    import geneva.runners.ray._mgr as ray_mgr_mod

    ray_init_called: dict[str, Any] = {}

    def mock_ray_init(*args: Any, **kwargs: Any) -> None:
        ray_init_called["args"] = args
        ray_init_called["kwargs"] = kwargs

    monkeypatch.setattr("ray.init", mock_ray_init)
    monkeypatch.setattr("ray.shutdown", lambda: None)
    monkeypatch.setattr("ray.is_initialized", lambda: False)

    zip_namespace = {
        "impl": "dir",
        "properties": {"root": "/example/db"},
        "table_id": ["__system", "geneva_manifests"],
    }

    with ray_mgr_mod.init_ray(
        addr="ray://test:10001",
        zips=[["/example/db/__system/geneva_manifests/_geneva_uploads/a.zip"]],
        zip_namespace=zip_namespace,
    ):
        pass

    env_vars = ray_init_called["kwargs"]["runtime_env"]["env_vars"]
    payload = json.loads(base64.b64decode(env_vars["GENEVA_ZIPS"]))
    assert payload["namespace"] == zip_namespace


def test_env_vars_vs_extra_env(monkeypatch) -> None:
    """Test interaction between env_vars (in head spec) and extra_env

    This test demonstrates that:
    - env_vars in head/worker specs set Kubernetes container environment variables
    - extra_env in ray_cluster sets Ray runtime_env environment variables
    - When the same variable is set in both places, extra_env takes
      precedence in Ray tasks
    - extra_env is what gets passed to init_ray's runtime_env, not env_vars
      from specs
    """

    import geneva.runners.ray._mgr as ray_mgr_mod

    ray_init_called = {}

    # Mock ray.init to capture the runtime_env
    def mock_ray_init(*args: Any, **kwargs: Any) -> None:
        ray_init_called["args"] = args
        ray_init_called["kwargs"] = kwargs

    monkeypatch.setattr("ray.init", mock_ray_init)
    monkeypatch.setattr("ray.shutdown", lambda: None)
    monkeypatch.setattr("ray.is_initialized", lambda: False)

    # Create a RayCluster with env_vars in the head spec
    # These would normally go into the Kubernetes pod definition
    head = _HeadGroupSpec(
        env_vars={
            "SHARED_VAR": "from_head_spec",
            "HEAD_ONLY_VAR": "head_value",
        }
    )
    # Note: cluster object is not used, but demonstrates that env_vars
    # in head spec don't automatically flow to runtime_env
    _ = RayCluster(
        name="test-env-conflict",
        namespace="test",
        head_group=head,
        worker_groups=[],
    )

    # Now use ray_cluster with extra_env
    # These go into Ray's runtime_env
    extra_env_vars = {
        "SHARED_VAR": "from_extra_env",  # Overlaps with head spec
        "EXTRA_ONLY_VAR": "extra_value",  # Only in extra_env
    }

    # Note: We use local=True to avoid actually creating a k8s cluster
    # In a real scenario with a k8s cluster, both env_vars (in containers)
    # and extra_env (in Ray runtime_env) would be present
    with ray_mgr_mod.ray_cluster(local=True, extra_env=extra_env_vars):
        pass

    # Verify what ended up in the runtime_env
    assert "kwargs" in ray_init_called
    runtime_env = ray_init_called["kwargs"]["runtime_env"]
    assert "env_vars" in runtime_env
    env_vars = runtime_env["env_vars"]

    # Key insight: Only extra_env makes it to the runtime_env
    # The env_vars from head spec are NOT in the runtime_env
    # (they would only be in the Kubernetes pod definition)
    assert env_vars["SHARED_VAR"] == "from_extra_env"  # extra_env wins for Ray tasks
    assert env_vars["EXTRA_ONLY_VAR"] == "extra_value"
    assert "HEAD_ONLY_VAR" not in env_vars  # Not in runtime_env
    assert "GENEVA_ZIPS" in env_vars  # Always present


@pytest.mark.ray
def test_extra_env_available_in_ray_workers() -> None:
    """Test that extra_env variables are actually available in Ray worker processes

    This integration test starts a real local Ray cluster and verifies that
    environment variables passed via extra_env are accessible in Ray remote
    functions running on worker processes.
    """
    import os

    import ray

    import geneva.runners.ray._mgr as ray_mgr_mod

    # Define a remote function that checks environment variables
    @ray.remote
    def check_env_vars() -> dict[str, str | None]:
        """Remote function that runs in a Ray worker and checks env vars"""
        return {
            "GCS_REQUEST_CONNECTION_TIMEOUT_SECS": os.environ.get(
                "GCS_REQUEST_CONNECTION_TIMEOUT_SECS"
            ),
            "GCS_REQUEST_TIMEOUT_SECS": os.environ.get("GCS_REQUEST_TIMEOUT_SECS"),
            "CUSTOM_ENV_VAR": os.environ.get("CUSTOM_ENV_VAR"),
        }

    extra_env_vars = {
        "GCS_REQUEST_CONNECTION_TIMEOUT_SECS": "300",
        "GCS_REQUEST_TIMEOUT_SECS": "600",
        "CUSTOM_ENV_VAR": "custom_value",
    }

    # Use local Ray cluster to test
    with ray_mgr_mod.ray_cluster(local=True, extra_env=extra_env_vars):
        # Execute the remote function and get the result
        result = ray.get(check_env_vars.remote())

        # Verify all env vars are accessible in the worker
        assert result["GCS_REQUEST_CONNECTION_TIMEOUT_SECS"] == "300"
        assert result["GCS_REQUEST_TIMEOUT_SECS"] == "600"
        assert result["CUSTOM_ENV_VAR"] == "custom_value"


def test_ray_init_kwargs_passed_to_init_ray(monkeypatch) -> None:
    """Test that ray_init_kwargs parameter is passed through to ray.init()

    This test verifies that arbitrary kwargs passed via ray_init_kwargs are
    correctly threaded through ray_cluster -> init_ray -> ray.init().
    """

    import geneva.runners.ray._mgr as ray_mgr_mod

    ray_init_called = {}

    # Mock ray.init to capture all kwargs
    def mock_ray_init(*args: Any, **kwargs: Any) -> None:
        ray_init_called["args"] = args
        ray_init_called["kwargs"] = kwargs

    monkeypatch.setattr("ray.init", mock_ray_init)
    monkeypatch.setattr("ray.shutdown", lambda: None)
    monkeypatch.setattr("ray.is_initialized", lambda: False)

    # Test with custom runtime_env via ray_init_kwargs
    custom_runtime_env = {
        "conda": {
            "channels": ["conda-forge"],
            "dependencies": ["python=3.10", "ffmpeg"],
        },
        "config": {"eager_install": True},
    }

    ray_init_kwargs = {
        "runtime_env": custom_runtime_env,
        "namespace": "test-namespace",
        "ignore_reinit_error": True,
    }

    with ray_mgr_mod.ray_cluster(local=True, ray_init_kwargs=ray_init_kwargs):
        pass

    # Verify ray.init was called with our custom kwargs
    assert "kwargs" in ray_init_called
    kwargs = ray_init_called["kwargs"]

    # Check that ray_init_kwargs are present
    assert kwargs["namespace"] == "test-namespace"
    assert kwargs["ignore_reinit_error"] is True

    # Check that runtime_env was merged correctly
    runtime_env = kwargs["runtime_env"]
    assert "conda" in runtime_env
    assert runtime_env["conda"] == custom_runtime_env["conda"]
    assert runtime_env["config"] == custom_runtime_env["config"]

    # GENEVA_ZIPS should still be present in env_vars
    assert "env_vars" in runtime_env
    assert "GENEVA_ZIPS" in runtime_env["env_vars"]


def test_ray_init_kwargs_runtime_env_merge(monkeypatch) -> None:
    """Test that ray_init_kwargs runtime_env is properly merged with default runtime_env

    This test verifies that when ray_init_kwargs contains a runtime_env,
    it's properly merged with the default Geneva runtime_env, preserving
    both user settings and Geneva internals.
    """

    import geneva.runners.ray._mgr as ray_mgr_mod

    ray_init_called = {}

    def mock_ray_init(*args: Any, **kwargs: Any) -> None:
        ray_init_called["kwargs"] = kwargs

    monkeypatch.setattr("ray.init", mock_ray_init)
    monkeypatch.setattr("ray.shutdown", lambda: None)
    monkeypatch.setattr("ray.is_initialized", lambda: False)

    # Use both extra_env and ray_init_kwargs with runtime_env
    extra_env_vars = {
        "EXTRA_VAR": "extra_value",
    }

    ray_init_kwargs = {
        "runtime_env": {
            "env_vars": {
                "CUSTOM_VAR": "custom_value",
            },
            "pip": ["numpy==1.24.0"],
        }
    }

    with ray_mgr_mod.ray_cluster(
        local=True, extra_env=extra_env_vars, ray_init_kwargs=ray_init_kwargs
    ):
        pass

    runtime_env = ray_init_called["kwargs"]["runtime_env"]

    # Check that all env_vars are merged
    assert "GENEVA_ZIPS" in runtime_env["env_vars"]  # Default from Geneva
    assert runtime_env["env_vars"]["EXTRA_VAR"] == "extra_value"  # From extra_env
    assert (
        runtime_env["env_vars"]["CUSTOM_VAR"] == "custom_value"
    )  # From ray_init_kwargs

    # Local mode: Geneva's pin is not added; only user's packages from
    # ray_init_kwargs remain
    assert runtime_env["pip"] == ["numpy==1.24.0"]


def test_raycluster_ray_init_kwargs_attribute() -> None:
    """Test that RayCluster properly stores ray_init_kwargs"""
    head = _HeadGroupSpec(image="test-img", num_cpus=1, memory="4Gi")
    worker = _WorkerGroupSpec(image="test-img", num_cpus=2, memory="8Gi")

    ray_init_kwargs = {
        "runtime_env": {
            "conda": {"dependencies": ["python=3.10"]},
        },
        "namespace": "my-namespace",
    }

    cluster = RayCluster(
        name="test-cluster",
        namespace="test-ns",
        head_group=head,
        worker_groups=[worker],
        ray_init_kwargs=ray_init_kwargs,
    )

    assert cluster.ray_init_kwargs == ray_init_kwargs
    assert cluster.ray_init_kwargs["namespace"] == "my-namespace"


def test_geneva_cluster_ray_init_kwargs() -> None:
    """Test that GenevaCluster properly stores and converts ray_init_kwargs"""
    from geneva.cluster import GenevaClusterType, K8sConfigMethod
    from geneva.cluster.mgr import GenevaCluster, HeadGroupConfig, KubeRayConfig

    ray_init_kwargs = {
        "runtime_env": {
            "pip": ["numpy"],
        },
        "namespace": "test-ns",
    }

    head_config = HeadGroupConfig(
        service_account="test-sa",
        num_cpus=2,
        memory="4Gi",
        image="rayproject/ray:latest",
        node_selector={},
        labels={},
        tolerations=[],
    )

    kuberay_config = KubeRayConfig(
        namespace=DEFAULT_K8S_NS,
        head_group=head_config,
        worker_groups=[],
        config_method=K8sConfigMethod.LOCAL,
        ray_init_kwargs=ray_init_kwargs,
    )

    cluster = GenevaCluster(
        cluster_type=GenevaClusterType.KUBE_RAY,
        name="test-cluster",
        kuberay=kuberay_config,
    )

    # Verify ray_init_kwargs are stored
    assert cluster.kuberay.ray_init_kwargs == ray_init_kwargs

    # Verify conversion to RayCluster preserves ray_init_kwargs
    ray_cluster = cluster.to_ray_cluster()
    assert ray_cluster.ray_init_kwargs == ray_init_kwargs


def test_external_cluster_ray_init_kwargs() -> None:
    """Test that ExternalRayCluster properly stores ray_init_kwargs"""
    from geneva.cluster import GenevaCluster, GenevaClusterType

    ray_init_kwargs = {
        "runtime_env": {
            "env_vars": {"MY_VAR": "value", "AWS_ACCESS_KEY_ID": "test"},
        },
        "namespace": "test-ns",
    }

    cluster = GenevaCluster(
        cluster_type=GenevaClusterType.EXTERNAL_RAY,
        name="external-cluster",
        ray_address="ray://host:10001",
        ray_init_kwargs=ray_init_kwargs,
    )

    # Verify ray_init_kwargs are stored at cluster level (not in kuberay)
    assert cluster.ray_init_kwargs == ray_init_kwargs
    assert cluster.kuberay is None
    assert cluster.cluster_type == GenevaClusterType.EXTERNAL_RAY


def test_conda_pip_conflict(monkeypatch) -> None:
    """Test handling when both conda and pip are specified

    According to Ray documentation, conda and pip cannot be specified simultaneously.
    This test verifies the behavior when both are present.
    """
    import geneva.runners.ray._mgr as ray_mgr_mod

    ray_init_called = {}

    def mock_ray_init(*args: Any, **kwargs: Any) -> None:
        ray_init_called["kwargs"] = kwargs

    monkeypatch.setattr("ray.init", mock_ray_init)
    monkeypatch.setattr("ray.shutdown", lambda: None)
    monkeypatch.setattr("ray.is_initialized", lambda: False)

    # Geneva sets pip via parameter, user sets conda via ray_init_kwargs
    pip_packages = ["numpy==1.24.0"]
    ray_init_kwargs = {
        "runtime_env": {
            "conda": {
                "channels": ["conda-forge"],
                "dependencies": ["python=3.10", "ffmpeg"],
            }
        }
    }

    with ray_mgr_mod.ray_cluster(
        local=True, pip=pip_packages, ray_init_kwargs=ray_init_kwargs
    ):
        pass

    runtime_env = ray_init_called["kwargs"]["runtime_env"]

    # Local mode: pip is not set (workers share the driver's environment).
    # Only conda from ray_init_kwargs is present.
    assert "pip" not in runtime_env
    assert "conda" in runtime_env


def test_conda_overrides_pip_in_ray_init_kwargs(monkeypatch) -> None:
    """Test that conda in ray_init_kwargs can override pip at the same level

    If user specifies both pip via parameter AND conda in ray_init_kwargs,
    they can also override by putting pip in ray_init_kwargs.
    """
    import geneva.runners.ray._mgr as ray_mgr_mod

    ray_init_called = {}

    def mock_ray_init(*args: Any, **kwargs: Any) -> None:
        ray_init_called["kwargs"] = kwargs

    monkeypatch.setattr("ray.init", mock_ray_init)
    monkeypatch.setattr("ray.shutdown", lambda: None)
    monkeypatch.setattr("ray.is_initialized", lambda: False)

    # User can override pip by passing pip: None in ray_init_kwargs
    pip_packages = ["numpy==1.24.0"]
    ray_init_kwargs = {
        "runtime_env": {
            "pip": None,  # Explicitly clear pip
            "conda": {
                "channels": ["conda-forge"],
                "dependencies": ["python=3.10", "ffmpeg"],
            },
        }
    }

    with ray_mgr_mod.ray_cluster(
        local=True, pip=pip_packages, ray_init_kwargs=ray_init_kwargs
    ):
        pass

    runtime_env = ray_init_called["kwargs"]["runtime_env"]

    # pip should be None, conda should be present
    assert runtime_env.get("pip") is None
    assert "conda" in runtime_env


def test_container_runtime_env(monkeypatch) -> None:
    """Test that container in runtime_env is passed through correctly

    According to Ray docs, container works alone or only with config/env_vars.
    """
    import geneva.runners.ray._mgr as ray_mgr_mod

    ray_init_called = {}

    def mock_ray_init(*args: Any, **kwargs: Any) -> None:
        ray_init_called["kwargs"] = kwargs

    monkeypatch.setattr("ray.init", mock_ray_init)
    monkeypatch.setattr("ray.shutdown", lambda: None)
    monkeypatch.setattr("ray.is_initialized", lambda: False)

    ray_init_kwargs = {
        "runtime_env": {
            "container": {
                "image": "anyscale/ray:latest",
                "run_options": ["--cap-add=SYS_PTRACE"],
            },
        }
    }

    with ray_mgr_mod.ray_cluster(local=True, ray_init_kwargs=ray_init_kwargs):
        pass

    runtime_env = ray_init_called["kwargs"]["runtime_env"]

    # Container should be present
    assert "container" in runtime_env
    assert runtime_env["container"]["image"] == "anyscale/ray:latest"
    # env_vars (GENEVA_ZIPS) should still be there
    assert "env_vars" in runtime_env
    assert "GENEVA_ZIPS" in runtime_env["env_vars"]


def test_init_ray_connection_error_retries_and_raises(monkeypatch) -> None:
    """Test that init_ray retries on ConnectionError and raises RuntimeError after
    exhausting retries.

    This test verifies that:
    1. init_ray retries when ray.init() raises ConnectionError
    2. After exhausting retries, it raises RuntimeError with helpful message
    3. The retry count matches RAY_INIT_MAX_RETRIES
    """
    import geneva.runners.ray._mgr as ray_mgr_mod

    # Set max retries to a small number for fast testing
    monkeypatch.setattr(ray_mgr_mod, "RAY_INIT_MAX_RETRIES", 3)

    call_count = 0

    def mock_ray_init_raises_connection_error(*args: Any, **kwargs: Any) -> None:
        nonlocal call_count
        call_count += 1
        raise ConnectionError("Failed to connect to Ray head")

    monkeypatch.setattr("ray.init", mock_ray_init_raises_connection_error)
    monkeypatch.setattr("ray.shutdown", lambda: None)
    monkeypatch.setattr("ray.is_initialized", lambda: False)

    # Create a mock cluster for the error message
    mock_cluster = Mock()
    mock_cluster.name = "test-cluster"
    mock_cluster.namespace = "test-namespace"
    mock_cluster.definition = {"name": "test-cluster"}

    with (
        pytest.raises(RuntimeError) as exc_info,
        ray_mgr_mod.init_ray(
            addr="ray://test:10001",
            zips=[],
            cluster=mock_cluster,
        ),
    ):
        pass

    # Verify the exact error message format
    error_msg = str(exc_info.value)
    assert (
        error_msg
        == "Geneva was unable to connect to the Ray head. The Ray head probably "
        "failed to start. Please ensure the head image matches the node "
        "architecture. Ray cluster: {'name': 'test-cluster'}"
    )

    # Verify the original ConnectionError is chained
    assert exc_info.value.__cause__ is not None
    assert isinstance(exc_info.value.__cause__, ConnectionError)

    # Verify ray.init was called the expected number of times (initial + retries)
    assert call_count == 3  # RAY_INIT_MAX_RETRIES


def test_init_ray_connection_error_succeeds_after_retry(monkeypatch) -> None:
    """Test that init_ray succeeds when ray.init() works after initial failures.

    This test verifies that transient ConnectionErrors are handled correctly
    and the context manager yields successfully when ray.init() eventually succeeds.
    """
    import geneva.runners.ray._mgr as ray_mgr_mod

    monkeypatch.setattr(ray_mgr_mod, "RAY_INIT_MAX_RETRIES", 5)

    call_count = 0
    ray_initialized = False

    def mock_ray_init_fails_then_succeeds(*args: Any, **kwargs: Any) -> None:
        nonlocal call_count, ray_initialized
        call_count += 1
        if call_count < 3:
            raise ConnectionError("Transient connection failure")
        # Success on 3rd attempt
        ray_initialized = True

    def mock_is_initialized() -> bool:
        return ray_initialized

    monkeypatch.setattr("ray.init", mock_ray_init_fails_then_succeeds)
    monkeypatch.setattr("ray.shutdown", lambda: None)
    monkeypatch.setattr("ray.is_initialized", mock_is_initialized)

    entered_context = False
    with ray_mgr_mod.init_ray(
        addr="ray://test:10001",
        zips=[],
        cluster=None,
    ):
        entered_context = True

    assert entered_context, "Context manager should have yielded successfully"
    assert call_count == 3, "ray.init should have been called 3 times"


# --- Replica Constraint Validation Tests ---


def test_worker_group_replicas_less_than_min_replicas_raises() -> None:
    """Test that replicas < min_replicas raises ValueError."""
    with pytest.raises(
        ValueError, match=r"replicas \(1\) must be >= min_replicas \(2\)"
    ):
        _WorkerGroupSpec(
            image="test-img",
            num_cpus=2,
            memory="8Gi",
            replicas=1,
            min_replicas=2,
            max_replicas=5,
        )


def test_worker_group_replicas_greater_than_max_replicas_raises() -> None:
    """Test that replicas > max_replicas raises ValueError."""
    with pytest.raises(
        ValueError, match=r"replicas \(10\) must be <= max_replicas \(5\)"
    ):
        _WorkerGroupSpec(
            image="test-img",
            num_cpus=2,
            memory="8Gi",
            replicas=10,
            min_replicas=1,
            max_replicas=5,
        )


def test_worker_group_replicas_equal_to_min_replicas_valid() -> None:
    """Test that replicas == min_replicas is valid."""
    worker = _WorkerGroupSpec(
        image="test-img",
        num_cpus=2,
        memory="8Gi",
        replicas=2,
        min_replicas=2,
        max_replicas=5,
    )
    assert worker.replicas == 2
    assert worker.min_replicas == 2


def test_worker_group_replicas_equal_to_max_replicas_valid() -> None:
    """Test that replicas == max_replicas is valid."""
    worker = _WorkerGroupSpec(
        image="test-img",
        num_cpus=2,
        memory="8Gi",
        replicas=5,
        min_replicas=1,
        max_replicas=5,
    )
    assert worker.replicas == 5
    assert worker.max_replicas == 5


def test_worker_group_replicas_between_min_and_max_valid() -> None:
    """Test that min_replicas < replicas < max_replicas is valid."""
    worker = _WorkerGroupSpec(
        image="test-img",
        num_cpus=2,
        memory="8Gi",
        replicas=3,
        min_replicas=1,
        max_replicas=5,
    )
    assert worker.replicas == 3
    assert worker.min_replicas == 1
    assert worker.max_replicas == 5


def test_worker_group_replicas_all_equal_valid() -> None:
    """Test that replicas == min_replicas == max_replicas is valid (fixed size)."""
    worker = _WorkerGroupSpec(
        image="test-img",
        num_cpus=2,
        memory="8Gi",
        replicas=3,
        min_replicas=3,
        max_replicas=3,
    )
    assert worker.replicas == 3
    assert worker.min_replicas == 3
    assert worker.max_replicas == 3


def test_worker_group_replicas_validator_order() -> None:
    """Test that replicas validator can access min/max_replicas.

    This test proves that attrs validators run AFTER all fields are initialized,
    so the replicas validator can safely reference min_replicas and max_replicas
    even though they are defined later in the class. This is documented behavior:
    https://www.attrs.org/en/stable/init.html#validators
    """
    # This should work: replicas=5 is valid for min=1, max=10
    # The validator references min_replicas and max_replicas which are defined
    # AFTER replicas in the _WorkerGroupSpec class
    worker = _WorkerGroupSpec(
        image="test-img",
        num_cpus=2,
        memory="8Gi",
        replicas=5,
        min_replicas=1,
        max_replicas=10,
    )
    assert worker.replicas == 5
    assert worker.min_replicas == 1
    assert worker.max_replicas == 10

    # Also verify validation still fails correctly
    with pytest.raises(ValueError, match="replicas.*must be >= min_replicas"):
        _WorkerGroupSpec(
            image="test-img",
            num_cpus=2,
            memory="8Gi",
            replicas=0,  # Less than min_replicas
            min_replicas=1,
            max_replicas=10,
        )


class TestTlsSetup:
    """Tests for secure Ray TLS setup."""

    def test_needs_tls_setup_returns_false_for_none_addr(self) -> None:
        """Test that None address returns False."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        assert ray_mgr_mod._needs_tls_setup(None, None) is False

    def test_needs_tls_setup_returns_false_for_non_ray_addr(self) -> None:
        """Test that non-ray:// addresses return False."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        assert ray_mgr_mod._needs_tls_setup("localhost:10001", None) is False
        assert ray_mgr_mod._needs_tls_setup("http://host:443", None) is False

    def test_needs_tls_setup_returns_true_for_port_443(self) -> None:
        """Test that ray:// addresses on port 443 return True."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        assert ray_mgr_mod._needs_tls_setup("ray://host:443", None) is True
        assert (
            ray_mgr_mod._needs_tls_setup("ray://my-cluster.example.com:443", None)
            is True
        )

    def test_needs_tls_setup_returns_false_for_other_ports(self) -> None:
        """Test that ray:// addresses on non-443 ports return False."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        assert ray_mgr_mod._needs_tls_setup("ray://host:10001", None) is False
        assert ray_mgr_mod._needs_tls_setup("ray://host:8080", None) is False

    def test_needs_tls_setup_with_env_var(self, monkeypatch: Any) -> None:
        """Test that GENEVA_RAY_CLIENT_SECURE env var enables secure mode."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        for val in ["1", "true", "yes", "TRUE", "Yes"]:
            monkeypatch.setenv("GENEVA_RAY_CLIENT_SECURE", val)
            assert ray_mgr_mod._needs_tls_setup("ray://host:10001", None) is True

        for val in ["0", "false", "no", ""]:
            monkeypatch.setenv("GENEVA_RAY_CLIENT_SECURE", val)
            assert ray_mgr_mod._needs_tls_setup("ray://host:10001", None) is False

    def test_needs_tls_setup_with_kwargs(self) -> None:
        """Test that TLS-related Geneva kwargs enable TLS setup."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        assert (
            ray_mgr_mod._needs_tls_setup(
                "ray://host:10001", {"_geneva_secure_client": True}
            )
            is True
        )
        assert (
            ray_mgr_mod._needs_tls_setup(
                "ray://host:10001", {"_geneva_tls_ca_cert": "ca.pem"}
            )
            is True
        )
        assert (
            ray_mgr_mod._needs_tls_setup(
                "ray://host:10001", {"_geneva_secure_client": False}
            )
            is False
        )
        assert (
            ray_mgr_mod._needs_tls_setup("ray://host:10001", {"other_kwarg": "value"})
            is False
        )

    def test_needs_tls_setup_accepts_any_non_none_ca_cert_value(self) -> None:
        """Test that TLS setup is triggered for any explicit CA-cert config."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        assert (
            ray_mgr_mod._needs_tls_setup(
                "ray://host:10001", {"_geneva_tls_ca_cert": True}
            )
            is True
        )

    def test_setup_tls_and_init_uses_existing_credentials(
        self, monkeypatch: Any
    ) -> None:
        """Test that TLS setup passes sanitized kwargs through to ray.init."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        captured_args: dict[str, Any] = {}

        def mock_ray_init(*args: Any, **kwargs: Any) -> None:
            captured_args["args"] = args
            captured_args["kwargs"] = kwargs

        def fail_import_grpc() -> None:
            raise AssertionError("grpc should not be imported")

        monkeypatch.setattr(
            ray_mgr_mod,
            "_import_grpc",
            fail_import_grpc,
        )
        monkeypatch.setattr("ray.init", mock_ray_init)

        init_kwargs = {
            "address": "ray://my-host:443",
            "runtime_env": {"env_vars": {"FOO": "bar"}},
            "namespace": "test-ns",
            "_metadata": [("key", "value")],
            "_credentials": "mock-creds",
            "_geneva_secure_client": True,
            "log_to_driver": True,
        }

        ray_mgr_mod._setup_tls_and_init("ray://my-host:443", init_kwargs)

        assert captured_args["args"] == ()
        assert captured_args["kwargs"]["address"] == "ray://my-host:443"
        assert captured_args["kwargs"]["namespace"] == "test-ns"
        assert captured_args["kwargs"]["_metadata"] == [("key", "value")]
        assert captured_args["kwargs"]["_credentials"] == "mock-creds"
        assert captured_args["kwargs"]["log_to_driver"] is True
        assert "_geneva_secure_client" not in captured_args["kwargs"]

    def test_setup_tls_and_init_warns_when_ca_cert_overrides_credentials(
        self, monkeypatch: Any, tmp_path: Any, caplog: Any
    ) -> None:
        """Test that CA cert precedence over explicit credentials is logged."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        ca_cert_path = tmp_path / "ca.pem"
        ca_cert_path.write_bytes(b"test-ca-bytes")

        monkeypatch.setattr(
            ray_mgr_mod,
            "_import_grpc",
            lambda: SimpleNamespace(
                ssl_channel_credentials=lambda root_certificates=None: "generated-creds"
            ),
        )
        monkeypatch.setattr("ray.init", lambda **kwargs: None)

        with caplog.at_level("WARNING"):
            ray_mgr_mod._setup_tls_and_init(
                "ray://my-host:443",
                {
                    "address": "ray://my-host:443",
                    "_geneva_tls_ca_cert": str(ca_cert_path),
                    "_credentials": "existing-creds",
                },
            )

        assert "Both _geneva_tls_ca_cert and _credentials were provided" in caplog.text

    def test_setup_tls_and_init_builds_credentials_from_ca_cert(
        self, monkeypatch: Any, tmp_path: Any
    ) -> None:
        """Test that TLS setup can build channel credentials from a CA cert file."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        grpc_captured: dict[str, Any] = {}
        ray_init_captured: dict[str, Any] = {}
        ca_cert_path = tmp_path / "ca.pem"
        ca_cert_path.write_bytes(b"test-ca-bytes")

        def mock_ssl_channel_credentials(
            root_certificates: bytes | None = None,
        ) -> str:
            grpc_captured["root_certificates"] = root_certificates
            return "generated-creds"

        monkeypatch.setattr(
            ray_mgr_mod,
            "_import_grpc",
            lambda: SimpleNamespace(
                ssl_channel_credentials=mock_ssl_channel_credentials
            ),
        )

        def mock_ray_init(**kwargs: Any) -> None:
            ray_init_captured.update(kwargs)

        monkeypatch.setattr("ray.init", mock_ray_init)

        init_kwargs = {
            "address": "ray://my-host:443",
            "runtime_env": {
                "env_vars": {"FOO": "bar"},
                "py_modules": ["/path/to/module"],
                "pip": ["numpy"],
            },
            "_geneva_tls_ca_cert": str(ca_cert_path),
        }

        ray_mgr_mod._setup_tls_and_init("ray://my-host:443", init_kwargs)

        runtime_env = ray_init_captured["runtime_env"]
        assert runtime_env["env_vars"] == {"FOO": "bar"}
        assert runtime_env["pip"] == ["numpy"]
        assert runtime_env["py_modules"] == ["/path/to/module"]
        assert ray_init_captured["_credentials"] == "generated-creds"
        assert grpc_captured["root_certificates"] == b"test-ca-bytes"
        assert "_geneva_tls_ca_cert" not in ray_init_captured

    def test_setup_tls_and_init_uses_system_trust_store(self, monkeypatch: Any) -> None:
        """Test that TLS setup falls back to the system trust store."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        grpc_captured: dict[str, Any] = {}
        ray_init_captured: dict[str, Any] = {}

        def mock_ssl_channel_credentials(
            root_certificates: bytes | None = None,
        ) -> str:
            grpc_captured["root_certificates"] = root_certificates
            return "system-creds"

        monkeypatch.setattr(
            ray_mgr_mod,
            "_import_grpc",
            lambda: SimpleNamespace(
                ssl_channel_credentials=mock_ssl_channel_credentials
            ),
        )

        def mock_ray_init(**kwargs: Any) -> None:
            ray_init_captured.update(kwargs)

        monkeypatch.setattr("ray.init", mock_ray_init)

        ray_mgr_mod._setup_tls_and_init(
            "ray://my-host:443",
            {
                "address": "ray://my-host:443",
                "runtime_env": {"env_vars": {"FOO": "bar"}},
            },
        )

        assert grpc_captured["root_certificates"] is None
        assert ray_init_captured["_credentials"] == "system-creds"

    def test_setup_tls_and_init_raises_clear_error_for_missing_ca_cert(
        self, monkeypatch: Any
    ) -> None:
        """Test that missing CA cert paths raise a clear error."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        monkeypatch.setattr("ray.init", lambda **kwargs: None)

        with pytest.raises(ValueError, match="Failed to read CA cert file"):
            ray_mgr_mod._setup_tls_and_init(
                "ray://my-host:443",
                {
                    "address": "ray://my-host:443",
                    "_geneva_tls_ca_cert": "missing-ca.pem",
                },
            )

    def test_setup_tls_and_init_rejects_non_string_ca_cert(
        self, monkeypatch: Any
    ) -> None:
        """Test that non-string CA cert config raises a clear error."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        monkeypatch.setattr("ray.init", lambda **kwargs: None)

        with pytest.raises(ValueError, match="file path string"):
            ray_mgr_mod._setup_tls_and_init(
                "ray://my-host:443",
                {
                    "address": "ray://my-host:443",
                    "_geneva_tls_ca_cert": True,
                },
            )

    def test_normalize_tls_ca_cert_path(self) -> None:
        """Test CA cert path normalization behavior."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        assert ray_mgr_mod._normalize_tls_ca_cert_path(None) is None
        assert ray_mgr_mod._normalize_tls_ca_cert_path("ca.pem") == "ca.pem"

        with pytest.raises(ValueError, match="non-empty file path string"):
            ray_mgr_mod._normalize_tls_ca_cert_path("")

        with pytest.raises(ValueError, match="file path string"):
            ray_mgr_mod._normalize_tls_ca_cert_path(True)

    def test_setup_tls_and_init_rejects_mismatched_addr(self) -> None:
        """Test that TLS setup validates the logged and actual addresses match."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        with pytest.raises(ValueError, match="Mismatched Ray TLS init addresses"):
            ray_mgr_mod._setup_tls_and_init(
                "ray://my-host:443",
                {"address": "ray://other-host:443", "_credentials": "mock-creds"},
            )

    def test_init_ray_rejects_mismatched_ray_init_kwargs_address(
        self, monkeypatch: Any
    ) -> None:
        """Test that init_ray rejects address overrides in ray_init_kwargs."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        monkeypatch.setattr(ray_mgr_mod, "RAY_INIT_MAX_RETRIES", 1)
        monkeypatch.setattr("ray.shutdown", lambda: None)
        monkeypatch.setattr("ray.is_initialized", lambda: False)
        monkeypatch.setattr("ray.init", lambda **kwargs: None)

        with (
            pytest.raises(ValueError, match=r"ray_init_kwargs\['address'\]"),
            ray_mgr_mod.init_ray(
                addr="ray://my-host:443",
                zips=[],
                ray_init_kwargs={"address": "ray://other-host:443"},
            ),
        ):
            pass

    def test_init_ray_uses_tls_setup_for_port_443(self, monkeypatch: Any) -> None:
        """Test that init_ray routes port 443 endpoints through TLS setup."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        monkeypatch.setattr(ray_mgr_mod, "RAY_INIT_MAX_RETRIES", 1)

        tls_setup_called = False
        ray_init_called = False

        def mock_tls_setup(addr: str, init_kwargs: dict) -> None:
            nonlocal tls_setup_called
            tls_setup_called = True

        def mock_ray_init(*args: Any, **kwargs: Any) -> None:
            nonlocal ray_init_called
            ray_init_called = True

        monkeypatch.setattr(ray_mgr_mod, "_setup_tls_and_init", mock_tls_setup)
        monkeypatch.setattr("ray.init", mock_ray_init)
        monkeypatch.setattr("ray.shutdown", lambda: None)
        monkeypatch.setattr("ray.is_initialized", lambda: False)

        with ray_mgr_mod.init_ray(addr="ray://host:443", zips=[]):
            pass

        assert tls_setup_called is True
        assert ray_init_called is False

    def test_init_ray_uses_tls_setup_for_ca_cert(self, monkeypatch: Any) -> None:
        """Test that a CA cert forces TLS setup even on non-443 ports."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        monkeypatch.setattr(ray_mgr_mod, "RAY_INIT_MAX_RETRIES", 1)

        tls_setup_called = False
        ray_init_called = False

        def mock_tls_setup(addr: str, init_kwargs: dict) -> None:
            nonlocal tls_setup_called
            tls_setup_called = True

        def mock_ray_init(*args: Any, **kwargs: Any) -> None:
            nonlocal ray_init_called
            ray_init_called = True

        monkeypatch.setattr(ray_mgr_mod, "_setup_tls_and_init", mock_tls_setup)
        monkeypatch.setattr("ray.init", mock_ray_init)
        monkeypatch.setattr("ray.shutdown", lambda: None)
        monkeypatch.setattr("ray.is_initialized", lambda: False)

        with ray_mgr_mod.init_ray(
            addr="ray://host:10001",
            zips=[],
            ray_init_kwargs={"_geneva_tls_ca_cert": "ca.pem"},
        ):
            pass

        assert tls_setup_called is True
        assert ray_init_called is False

    def test_init_ray_uses_ray_init_for_standard_port(self, monkeypatch: Any) -> None:
        """Test that init_ray uses plain ray.init for standard ports."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        monkeypatch.setattr(ray_mgr_mod, "RAY_INIT_MAX_RETRIES", 1)

        tls_setup_called = False
        ray_init_called = False

        def mock_tls_setup(addr: str, init_kwargs: dict) -> None:
            nonlocal tls_setup_called
            tls_setup_called = True

        def mock_ray_init(*args: Any, **kwargs: Any) -> None:
            nonlocal ray_init_called
            ray_init_called = True

        monkeypatch.setattr(ray_mgr_mod, "_setup_tls_and_init", mock_tls_setup)
        monkeypatch.setattr("ray.init", mock_ray_init)
        monkeypatch.setattr("ray.shutdown", lambda: None)
        monkeypatch.setattr("ray.is_initialized", lambda: False)

        with ray_mgr_mod.init_ray(addr="ray://host:10001", zips=[]):
            pass

        assert tls_setup_called is False
        assert ray_init_called is True


# =============================================================================
# Tests for automatic Geneva dependency injection
# =============================================================================


class TestInjectGenevaDeps:
    """Tests for automatic geneva pip injection in init_ray and ray_cluster."""

    def _make_ray_init_mock(self) -> tuple[dict, Any]:
        """Return (captured, mock_fn) for intercepting ray.init calls."""
        captured: dict = {}

        def mock_ray_init(*args: Any, **kwargs: Any) -> None:
            captured["args"] = args
            captured["kwargs"] = kwargs

        return captured, mock_ray_init

    def _geneva_pin(self) -> str:
        import geneva

        return f"geneva=={geneva.__version__}"

    def test_init_ray_adds_geneva_by_default(self, monkeypatch: Any) -> None:
        """When no deps are specified, geneva is added as the first pip entry."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        captured, mock_ray_init = self._make_ray_init_mock()
        monkeypatch.setattr("ray.init", mock_ray_init)
        monkeypatch.setattr("ray.shutdown", lambda: None)
        monkeypatch.setattr("ray.is_initialized", lambda: False)

        with ray_mgr_mod.init_ray(addr=None, zips=[]):
            pass

        runtime_env = captured["kwargs"]["runtime_env"]
        assert "pip" in runtime_env
        pip_list = runtime_env["pip"]
        assert isinstance(pip_list, list)
        assert pip_list[0] == self._geneva_pin()

    def test_init_ray_prepends_geneva_before_user_packages(
        self, monkeypatch: Any
    ) -> None:
        """geneva pin is first; user packages follow so they can override versions."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        captured, mock_ray_init = self._make_ray_init_mock()
        monkeypatch.setattr("ray.init", mock_ray_init)
        monkeypatch.setattr("ray.shutdown", lambda: None)
        monkeypatch.setattr("ray.is_initialized", lambda: False)

        user_pip = ["numpy==1.24.0", "pandas"]
        with ray_mgr_mod.init_ray(addr=None, zips=[], pip=user_pip):
            pass

        runtime_env = captured["kwargs"]["runtime_env"]
        pip_list = runtime_env["pip"]
        assert pip_list == [self._geneva_pin(), "numpy==1.24.0", "pandas"]

    def test_init_ray_inlines_requirements_path_with_geneva(
        self, monkeypatch: Any, tmp_path: Any
    ) -> None:
        """requirements_path is inlined as a list with the geneva pin prepended."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        captured, mock_ray_init = self._make_ray_init_mock()
        monkeypatch.setattr("ray.init", mock_ray_init)
        monkeypatch.setattr("ray.shutdown", lambda: None)
        monkeypatch.setattr("ray.is_initialized", lambda: False)

        req_file = tmp_path / "requirements.txt"
        req_file.write_text("numpy==1.24.0\n# a comment\npandas\n\n")

        with ray_mgr_mod.init_ray(addr=None, zips=[], requirements_path=str(req_file)):
            pass

        pip_list = captured["kwargs"]["runtime_env"]["pip"]
        assert isinstance(pip_list, list)
        assert pip_list == [self._geneva_pin(), "numpy==1.24.0", "pandas"]

    def test_ray_cluster_adds_geneva(self, monkeypatch: Any) -> None:
        """Local ray_cluster does not set pip — workers share the driver's
        environment."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        captured, mock_ray_init = self._make_ray_init_mock()
        monkeypatch.setattr("ray.init", mock_ray_init)
        monkeypatch.setattr("ray.shutdown", lambda: None)
        monkeypatch.setattr("ray.is_initialized", lambda: False)

        with ray_mgr_mod.ray_cluster(local=True):
            pass

        runtime_env = captured["kwargs"]["runtime_env"]
        assert "pip" not in runtime_env

    def test_ray_cluster_with_manifest_adds_geneva_before_user_pip(
        self, monkeypatch: Any
    ) -> None:
        """Local ray_cluster does not set pip even when manifest specifies pip
        packages."""
        import geneva.runners.ray._mgr as ray_mgr_mod
        from geneva.manifest.mgr import GenevaManifest

        captured, mock_ray_init = self._make_ray_init_mock()
        monkeypatch.setattr("ray.init", mock_ray_init)
        monkeypatch.setattr("ray.shutdown", lambda: None)
        monkeypatch.setattr("ray.is_initialized", lambda: False)

        manifest = GenevaManifest(name="test", pip=["user-pkg"])

        with ray_mgr_mod.ray_cluster(local=True, manifest=manifest):
            pass

        runtime_env = captured["kwargs"]["runtime_env"]
        assert "pip" not in runtime_env

    def test_ray_init_kwargs_pip_merges_with_geneva_pin(self, monkeypatch: Any) -> None:
        """pip in ray_init_kwargs.runtime_env is merged after Geneva's pin."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        captured, mock_ray_init = self._make_ray_init_mock()
        monkeypatch.setattr("ray.init", mock_ray_init)
        monkeypatch.setattr("ray.shutdown", lambda: None)
        monkeypatch.setattr("ray.is_initialized", lambda: False)

        with ray_mgr_mod.init_ray(
            addr=None,
            zips=[],
            ray_init_kwargs={"runtime_env": {"pip": ["custom==1.0"]}},
        ):
            pass

        pip_list = captured["kwargs"]["runtime_env"]["pip"]
        assert pip_list == [self._geneva_pin(), "custom==1.0"]

    def test_ray_init_kwargs_pip_string_path_wins(self, monkeypatch: Any) -> None:
        """A requirements-path string in ray_init_kwargs.runtime_env.pip wins
        over the assembled list rather than being unpacked character-by-character."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        captured, mock_ray_init = self._make_ray_init_mock()
        monkeypatch.setattr("ray.init", mock_ray_init)
        monkeypatch.setattr("ray.shutdown", lambda: None)
        monkeypatch.setattr("ray.is_initialized", lambda: False)

        req_path = "/path/to/requirements.txt"
        with ray_mgr_mod.init_ray(
            addr=None,
            zips=[],
            ray_init_kwargs={"runtime_env": {"pip": req_path}},
        ):
            pass

        pip_value = captured["kwargs"]["runtime_env"]["pip"]
        assert pip_value == req_path

    def test_ray_init_kwargs_pip_none_clears_pip(self, monkeypatch: Any) -> None:
        """pip=None in ray_init_kwargs.runtime_env clears the assembled pip list,
        e.g. when switching to conda via ray_init_kwargs."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        captured, mock_ray_init = self._make_ray_init_mock()
        monkeypatch.setattr("ray.init", mock_ray_init)
        monkeypatch.setattr("ray.shutdown", lambda: None)
        monkeypatch.setattr("ray.is_initialized", lambda: False)

        with ray_mgr_mod.init_ray(
            addr=None,
            zips=[],
            ray_init_kwargs={"runtime_env": {"pip": None}},
        ):
            pass

        runtime_env = captured["kwargs"]["runtime_env"]
        assert "pip" not in runtime_env

    def test_requirements_path_with_include_directive_raises(
        self, monkeypatch: Any, tmp_path: Any
    ) -> None:
        """-r include directives raise ValueError; workers can't access local files."""
        import pytest

        import geneva.runners.ray._mgr as ray_mgr_mod

        monkeypatch.setattr("ray.init", lambda *a, **kw: None)
        monkeypatch.setattr("ray.shutdown", lambda: None)
        monkeypatch.setattr("ray.is_initialized", lambda: False)

        req_file = tmp_path / "requirements.txt"
        req_file.write_text("numpy==1.24.0\n-r other.txt\npandas\n")

        with (
            pytest.raises(ValueError, match="-r include"),
            ray_mgr_mod.init_ray(addr=None, zips=[], requirements_path=str(req_file)),
        ):
            pass

    @pytest.mark.parametrize(
        "directive",
        [
            "-r other.txt",
            "-rother.txt",
            "--requirement other.txt",
            "--requirement=other.txt",
        ],
    )
    def test_requirements_path_include_directive_forms_all_raise(
        self, monkeypatch: Any, tmp_path: Any, directive: str
    ) -> None:
        """All pip -r / --requirement syntaxes are caught, with or without a space."""
        import pytest

        import geneva.runners.ray._mgr as ray_mgr_mod

        monkeypatch.setattr("ray.init", lambda *a, **kw: None)
        monkeypatch.setattr("ray.shutdown", lambda: None)
        monkeypatch.setattr("ray.is_initialized", lambda: False)

        req_file = tmp_path / "requirements.txt"
        req_file.write_text(f"numpy==1.24.0\n{directive}\npandas\n")

        with (
            pytest.raises(ValueError, match="-r include"),
            ray_mgr_mod.init_ray(addr=None, zips=[], requirements_path=str(req_file)),
        ):
            pass

    def test_conda_env_skips_geneva_pin(self, monkeypatch: Any) -> None:
        """When conda manages the environment, no geneva pip pin is injected."""
        import geneva.runners.ray._mgr as ray_mgr_mod

        captured, mock_ray_init = self._make_ray_init_mock()
        monkeypatch.setattr("ray.init", mock_ray_init)
        monkeypatch.setattr("ray.shutdown", lambda: None)
        monkeypatch.setattr("ray.is_initialized", lambda: False)

        with ray_mgr_mod.init_ray(
            addr=None,
            zips=[],
            conda={"dependencies": ["python=3.10", "numpy"]},
        ):
            pass

        runtime_env = captured["kwargs"]["runtime_env"]
        assert "pip" not in runtime_env
        assert "conda" in runtime_env
