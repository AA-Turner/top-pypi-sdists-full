# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import attrs
import pytest

from geneva.cluster import GenevaCluster, GenevaClusterType
from geneva.cluster.builder import (
    CpuWorkerBuilder,
    ExternalRayClusterBuilder,
    GpuWorkerBuilder,
    KubeRayClusterBuilder,
    LocalRayClusterBuilder,
    default_image,
)
from geneva.constants import DEFAULT_K8S_NS
from geneva.utils.ray import GENEVA_RAY_CPU_NODE, GENEVA_RAY_GPU_NODE

# =============================================================================
# Type-Safe Builder Tests
# =============================================================================


class TestCpuWorkerBuilder:
    """Tests for CpuWorkerBuilder."""

    def test_no_gpus_method(self) -> None:
        """CpuWorkerBuilder should not have a gpus() method."""
        builder = KubeRayClusterBuilder.cpu_worker()
        assert not hasattr(builder, "gpus")

    def test_default_cpu_node_selector(self) -> None:
        """CpuWorkerBuilder should default to CPU node selector."""
        worker = KubeRayClusterBuilder.cpu_worker().build()
        assert worker.node_selector == {GENEVA_RAY_CPU_NODE: "true"}

    def test_num_gpus_always_zero(self) -> None:
        """CpuWorkerBuilder should always have num_gpus=0."""
        worker = KubeRayClusterBuilder.cpu_worker().cpus(8).memory("16Gi").build()
        assert worker.num_gpus == 0

    def test_default_name(self) -> None:
        """CpuWorkerBuilder should default to 'cpu' name."""
        worker = KubeRayClusterBuilder.cpu_worker().build()
        assert worker.name == "cpu"

    def test_custom_name(self) -> None:
        """CpuWorkerBuilder should accept custom name."""
        worker = KubeRayClusterBuilder.cpu_worker().name("data-workers").build()
        assert worker.name == "data-workers"

    def test_fluent_interface(self) -> None:
        """CpuWorkerBuilder should support fluent interface."""
        worker = (
            KubeRayClusterBuilder.cpu_worker()
            .name("cpu-pool")
            .cpus(16)
            .memory("32Gi")
            .replicas(4)
            .min_replicas(2)
            .max_replicas(8)
            .service_account("custom-sa")
            .labels({"pool": "cpu"})
            .build()
        )
        assert worker.name == "cpu-pool"
        assert worker.num_cpus == 16
        assert worker.memory == "32Gi"
        assert worker.replicas == 4
        assert worker.min_replicas == 2
        assert worker.max_replicas == 8
        assert worker.service_account == "custom-sa"
        assert worker.labels == {"pool": "cpu"}

    def test_idle_timeout_seconds(self) -> None:
        """CpuWorkerBuilder should set idle_timeout_seconds."""
        worker = KubeRayClusterBuilder.cpu_worker().idle_timeout_seconds(120).build()
        assert worker.idle_timeout_seconds == 120

    def test_idle_timeout_seconds_default(self) -> None:
        """CpuWorkerBuilder should default to 60 seconds idle timeout."""
        worker = KubeRayClusterBuilder.cpu_worker().build()
        assert worker.idle_timeout_seconds == 60

    def test_env_vars(self) -> None:
        """CpuWorkerBuilder should support env_vars."""
        worker = (
            KubeRayClusterBuilder.cpu_worker()
            .env_vars({"MY_VAR": "value", "OTHER": "123"})
            .build()
        )
        assert worker.env_vars == {"MY_VAR": "value", "OTHER": "123"}

    def test_env_vars_default_empty(self) -> None:
        """CpuWorkerBuilder env_vars should default to empty dict."""
        worker = KubeRayClusterBuilder.cpu_worker().build()
        assert worker.env_vars == {}

    def test_add_env_var(self) -> None:
        """CpuWorkerBuilder should support add_env_var."""
        worker = (
            KubeRayClusterBuilder.cpu_worker()
            .add_env_var("KEY1", "val1")
            .add_env_var("KEY2", "val2")
            .build()
        )
        assert worker.env_vars == {"KEY1": "val1", "KEY2": "val2"}

    def test_env_vars_copies_input(self) -> None:
        """env_vars() should copy the input dict to avoid mutation."""
        original = {"MY_VAR": "value"}
        worker = KubeRayClusterBuilder.cpu_worker().env_vars(original).build()
        original["MY_VAR"] = "changed"
        assert worker.env_vars == {"MY_VAR": "value"}


class TestGpuWorkerBuilder:
    """Tests for GpuWorkerBuilder."""

    def test_default_gpu_node_selector(self) -> None:
        """GpuWorkerBuilder should default to GPU node selector."""
        worker = KubeRayClusterBuilder.gpu_worker().build()
        assert worker.node_selector == {GENEVA_RAY_GPU_NODE: "true"}

    def test_default_gpus(self) -> None:
        """GpuWorkerBuilder should default to 1 GPU."""
        worker = KubeRayClusterBuilder.gpu_worker().build()
        assert worker.num_gpus == 1

    def test_gpus_method(self) -> None:
        """GpuWorkerBuilder should allow setting GPU count."""
        worker = KubeRayClusterBuilder.gpu_worker(4).build()
        assert worker.num_gpus == 4

    def test_gpus_requires_positive(self) -> None:
        """GpuWorkerBuilder.gpus() should reject 0 or negative values."""
        with pytest.raises(ValueError, match="at least 1 GPU"):
            KubeRayClusterBuilder.gpu_worker(0)

    def test_minimum_memory_enforced(self) -> None:
        """GpuWorkerBuilder should reject memory < 4GiB."""
        with pytest.raises(ValueError, match="at least 4GiB memory"):
            KubeRayClusterBuilder.gpu_worker(1).memory("2Gi").build()

    def test_large_memory_warns(self, caplog) -> None:
        """GpuWorkerBuilder should warn for memory > 100GB."""
        import logging

        with caplog.at_level(logging.WARNING, logger="geneva.cluster.builder"):
            KubeRayClusterBuilder.gpu_worker(1).memory("120Gi").build()
        assert "may exceed K8s node capacity" in caplog.text

    def test_high_memory_cpu_ratio_warns(self, caplog) -> None:
        """GpuWorkerBuilder should warn for high memory/CPU ratio."""
        import logging

        with caplog.at_level(logging.WARNING, logger="geneva.cluster.builder"):
            KubeRayClusterBuilder.gpu_worker(1).cpus(1).memory("32Gi").build()
        assert "High memory/CPU ratio" in caplog.text

    def test_no_warning_for_reasonable_config(self, caplog) -> None:
        """GpuWorkerBuilder should not warn for reasonable config."""
        import logging

        with caplog.at_level(logging.WARNING, logger="geneva.cluster.builder"):
            KubeRayClusterBuilder.gpu_worker(2).cpus(8).memory("32Gi").build()
        # No warnings expected
        warning_messages = [
            rec.message for rec in caplog.records if rec.levelno == logging.WARNING
        ]
        assert len(warning_messages) == 0

    def test_auto_gpu_image(self) -> None:
        """GpuWorkerBuilder should use GPU image by default."""
        worker = KubeRayClusterBuilder.gpu_worker().build()
        assert worker.image == default_image(gpu=True)

    def test_default_name(self) -> None:
        """GpuWorkerBuilder should default to 'gpu' name."""
        worker = KubeRayClusterBuilder.gpu_worker().build()
        assert worker.name == "gpu"

    def test_higher_defaults(self) -> None:
        """GpuWorkerBuilder should have higher defaults than CPU."""
        worker = KubeRayClusterBuilder.gpu_worker().build()
        assert worker.num_cpus == 8  # Higher than CpuWorkerBuilder default of 4
        assert worker.memory == "16Gi"  # Higher than CpuWorkerBuilder default of 8Gi

    def test_gpu_worker_factory_with_gpus(self) -> None:
        """gpu_worker() should return builder with specified GPUs."""
        builder = KubeRayClusterBuilder.gpu_worker(gpus=4)
        worker = builder.build()
        assert worker.num_gpus == 4

    def test_idle_timeout_seconds(self) -> None:
        """GpuWorkerBuilder should set idle_timeout_seconds."""
        worker = KubeRayClusterBuilder.gpu_worker().idle_timeout_seconds(300).build()
        assert worker.idle_timeout_seconds == 300

    def test_idle_timeout_seconds_default(self) -> None:
        """GpuWorkerBuilder should default to 60 seconds idle timeout."""
        worker = KubeRayClusterBuilder.gpu_worker().build()
        assert worker.idle_timeout_seconds == 60

    def test_env_vars(self) -> None:
        """GpuWorkerBuilder should support env_vars."""
        worker = (
            KubeRayClusterBuilder.gpu_worker()
            .env_vars({"CUDA_VISIBLE_DEVICES": "0,1"})
            .build()
        )
        assert worker.env_vars == {"CUDA_VISIBLE_DEVICES": "0,1"}


class TestKubeRayClusterBuilder:
    """Tests for KubeRayClusterBuilder."""

    def test_basic_creation(self) -> None:
        """KubeRayClusterBuilder should create a KUBE_RAY cluster."""
        cluster = KubeRayClusterBuilder.create("test").build()
        assert cluster.cluster_type == GenevaClusterType.KUBE_RAY
        assert cluster.name == "test"
        assert cluster.kuberay is not None

    def test_default_namespace(self) -> None:
        """KubeRayClusterBuilder should default to the lancedb namespace."""
        cluster = KubeRayClusterBuilder.create("test").build()
        assert cluster.kuberay.namespace == DEFAULT_K8S_NS

    def test_custom_namespace(self) -> None:
        """KubeRayClusterBuilder should accept custom namespace."""
        cluster = KubeRayClusterBuilder.create("test").namespace("ml-team").build()
        assert cluster.kuberay.namespace == "ml-team"

    def test_add_worker_group_cpu(self) -> None:
        """KubeRayClusterBuilder should add CPU workers via add_worker_group."""
        cluster = (
            KubeRayClusterBuilder.create("test")
            .add_worker_group(KubeRayClusterBuilder.cpu_worker().cpus(4).build())
            .build()
        )
        assert len(cluster.kuberay.worker_groups) == 1
        assert cluster.kuberay.worker_groups[0].num_gpus == 0
        assert cluster.kuberay.worker_groups[0].num_cpus == 4

    def test_add_worker_group_gpu(self) -> None:
        """KubeRayClusterBuilder should add GPU workers via add_worker_group."""
        cluster = (
            KubeRayClusterBuilder.create("test")
            .add_worker_group(
                KubeRayClusterBuilder.gpu_worker(2).memory("32Gi").build()
            )
            .build()
        )
        assert len(cluster.kuberay.worker_groups) == 1
        assert cluster.kuberay.worker_groups[0].num_gpus == 2
        assert cluster.kuberay.worker_groups[0].memory == "32Gi"

    def test_mixed_workers(self) -> None:
        """KubeRayClusterBuilder should support mixed CPU and GPU workers."""
        cluster = (
            KubeRayClusterBuilder.create("test")
            .add_worker_group(
                KubeRayClusterBuilder.cpu_worker().name("cpu-pool").cpus(8).build()
            )
            .add_worker_group(
                KubeRayClusterBuilder.gpu_worker(4).name("gpu-pool").build()
            )
            .build()
        )
        assert len(cluster.kuberay.worker_groups) == 2
        assert cluster.kuberay.worker_groups[0].name == "cpu-pool"
        assert cluster.kuberay.worker_groups[0].num_gpus == 0
        assert cluster.kuberay.worker_groups[1].name == "gpu-pool"
        assert cluster.kuberay.worker_groups[1].num_gpus == 4

    def test_add_worker_group_from_config(self) -> None:
        """KubeRayClusterBuilder should accept a hand-constructed WorkerGroupConfig."""
        from geneva.cluster.mgr import WorkerGroupConfig

        cfg = WorkerGroupConfig(
            service_account="custom-sa",
            num_cpus=4,
            memory="16Gi",
            image="rayproject/ray:2.54.0-py310",
            num_gpus=1,
            node_selector={"pool": "gpu"},
            labels={},
            tolerations=[],
            k8s_spec_override={"replicas": 8, "min_replicas": 8, "max_replicas": 8},
        )
        cluster = KubeRayClusterBuilder.create("test").add_worker_group(cfg).build()
        assert len(cluster.kuberay.worker_groups) == 1
        assert cluster.kuberay.worker_groups[0].num_gpus == 1
        assert cluster.kuberay.worker_groups[0].service_account == "custom-sa"
        assert cluster.kuberay.worker_groups[0].k8s_spec_override == {
            "replicas": 8,
            "min_replicas": 8,
            "max_replicas": 8,
        }

    def test_requires_name(self) -> None:
        """KubeRayClusterBuilder should require a name."""
        with pytest.raises(ValueError, match="Cluster name is required"):
            KubeRayClusterBuilder().build()

    def test_default_cpu_worker_if_none_added(self) -> None:
        """KubeRayClusterBuilder should add default CPU worker if none specified."""
        cluster = KubeRayClusterBuilder.create("test").build()
        assert len(cluster.kuberay.worker_groups) == 1
        assert cluster.kuberay.worker_groups[0].name == "cpu"
        assert cluster.kuberay.worker_groups[0].num_gpus == 0

    def test_aws_config(self) -> None:
        """KubeRayClusterBuilder should accept AWS config."""
        cluster = (
            KubeRayClusterBuilder.create("test")
            .aws_config(region="us-west-2", role_name="test-role")
            .build()
        )
        assert cluster.kuberay.aws_region == "us-west-2"
        assert cluster.kuberay.aws_role_name == "test-role"

    def test_portforwarding(self) -> None:
        """KubeRayClusterBuilder should configure port forwarding."""
        cluster = KubeRayClusterBuilder.create("test").portforwarding(False).build()
        assert cluster.kuberay.use_portforwarding is False

    def test_ray_init_kwargs(self) -> None:
        """KubeRayClusterBuilder should pass through ray_init_kwargs."""
        kwargs = {"runtime_env": {"pip": ["numpy"]}}
        cluster = KubeRayClusterBuilder.create("test").ray_init_kwargs(kwargs).build()
        assert cluster.kuberay.ray_init_kwargs == kwargs

    def test_head_group_env_vars(self) -> None:
        """head_group() should accept env_vars."""
        cluster = (
            KubeRayClusterBuilder.create("test")
            .head_group(
                env_vars={
                    "GENEVA_PIPELINE_STALL_TIMEOUT_S": "1800",
                    "GENEVA_RETRY_LANCE_ATTEMPTS": "12",
                },
            )
            .build()
        )
        assert cluster.kuberay.head_group.env_vars == {
            "GENEVA_PIPELINE_STALL_TIMEOUT_S": "1800",
            "GENEVA_RETRY_LANCE_ATTEMPTS": "12",
        }

    def test_head_group_env_vars_default_empty(self) -> None:
        """head_group env_vars should default to empty dict."""
        cluster = KubeRayClusterBuilder.create("test").build()
        assert cluster.kuberay.head_group.env_vars == {}

    def test_worker_env_vars_through_builder(self) -> None:
        """Worker env_vars should flow through add_worker_group."""
        cluster = (
            KubeRayClusterBuilder.create("test")
            .add_worker_group(
                KubeRayClusterBuilder.cpu_worker()
                .env_vars({"GENEVA_RETRY_LANCE_MAX_SECS": "180.0"})
                .build()
            )
            .build()
        )
        assert cluster.kuberay.worker_groups[0].env_vars == {
            "GENEVA_RETRY_LANCE_MAX_SECS": "180.0",
        }

    def test_head_and_worker_env_vars_independent(self) -> None:
        """Head and worker env_vars should be independent."""
        cluster = (
            KubeRayClusterBuilder.create("test")
            .head_group(env_vars={"HEAD_VAR": "head_value"})
            .add_worker_group(
                KubeRayClusterBuilder.cpu_worker()
                .env_vars({"WORKER_VAR": "worker_value"})
                .build()
            )
            .build()
        )
        assert cluster.kuberay.head_group.env_vars == {"HEAD_VAR": "head_value"}
        assert cluster.kuberay.worker_groups[0].env_vars == {
            "WORKER_VAR": "worker_value"
        }

    def test_cpu_worker_factory(self) -> None:
        """KubeRayClusterBuilder.cpu_worker() should return a CpuWorkerBuilder."""
        builder = KubeRayClusterBuilder.cpu_worker()
        assert isinstance(builder, CpuWorkerBuilder)
        worker = builder.cpus(8).memory("16Gi").build()
        assert worker.num_cpus == 8
        assert worker.memory == "16Gi"
        assert worker.num_gpus == 0

    def test_gpu_worker_factory(self) -> None:
        """KubeRayClusterBuilder.gpu_worker() should return a GpuWorkerBuilder."""
        builder = KubeRayClusterBuilder.gpu_worker(gpus=4)
        assert isinstance(builder, GpuWorkerBuilder)
        worker = builder.memory("64Gi").build()
        assert worker.num_gpus == 4
        assert worker.memory == "64Gi"


class TestLocalRayClusterBuilder:
    """Tests for LocalRayClusterBuilder."""

    def test_no_worker_methods(self) -> None:
        """LocalRayClusterBuilder should not have worker configuration methods."""
        builder = LocalRayClusterBuilder()
        assert not hasattr(builder, "add_worker_group")
        assert not hasattr(builder, "memory")
        assert not hasattr(builder, "cpus")
        assert not hasattr(builder, "namespace")

    def test_builds_local_ray_cluster(self) -> None:
        """LocalRayClusterBuilder should create a LOCAL_RAY cluster."""
        cluster = LocalRayClusterBuilder.create("local-test").build()
        assert cluster.cluster_type == GenevaClusterType.LOCAL_RAY
        assert cluster.name == "local-test"
        assert cluster.kuberay is None

    def test_requires_name(self) -> None:
        """LocalRayClusterBuilder should require a name."""
        with pytest.raises(ValueError, match="Cluster name is required"):
            LocalRayClusterBuilder().build()


class TestExternalRayClusterBuilder:
    """Tests for ExternalRayClusterBuilder."""

    def test_no_worker_methods(self) -> None:
        """ExternalRayClusterBuilder should not have worker configuration methods."""
        builder = ExternalRayClusterBuilder()
        assert not hasattr(builder, "add_worker_group")
        assert not hasattr(builder, "memory")
        assert not hasattr(builder, "cpus")

    def test_requires_ray_address(self) -> None:
        """ExternalRayClusterBuilder should require ray_address."""
        with pytest.raises(ValueError, match="ray_address is required"):
            ExternalRayClusterBuilder.create("ext").build()

    def test_with_ray_address(self) -> None:
        """ExternalRayClusterBuilder should create EXTERNAL_RAY cluster."""
        cluster = (
            ExternalRayClusterBuilder.create("ext")
            .ray_address("ray://host:10001")
            .build()
        )
        assert cluster.cluster_type == GenevaClusterType.EXTERNAL_RAY
        assert cluster.name == "ext"
        assert cluster.ray_address == "ray://host:10001"
        assert cluster.kuberay is None

    def test_create_with_address(self) -> None:
        """ExternalRayClusterBuilder.create() should accept ray_address."""
        cluster = ExternalRayClusterBuilder.create(
            "ext", ray_address="ray://host:10001"
        ).build()
        assert cluster.ray_address == "ray://host:10001"

    def test_requires_name(self) -> None:
        """ExternalRayClusterBuilder should require a name."""
        with pytest.raises(ValueError, match="Cluster name is required"):
            ExternalRayClusterBuilder().ray_address("ray://host:10001").build()

    def test_ray_init_kwargs(self) -> None:
        """ExternalRayClusterBuilder should pass through ray_init_kwargs."""
        kwargs = {
            "runtime_env": {
                "env_vars": {"MY_VAR": "value", "AWS_ACCESS_KEY_ID": "test"}
            },
            "namespace": "test-namespace",
        }
        cluster = (
            ExternalRayClusterBuilder.create("ext")
            .ray_address("ray://host:10001")
            .ray_init_kwargs(kwargs)
            .build()
        )
        assert cluster.ray_init_kwargs == kwargs
        assert cluster.cluster_type == GenevaClusterType.EXTERNAL_RAY
        assert cluster.ray_address == "ray://host:10001"

    def test_ray_init_kwargs_defaults_to_empty(self) -> None:
        """ExternalRayClusterBuilder should default ray_init_kwargs to empty dict."""
        cluster = (
            ExternalRayClusterBuilder.create("ext")
            .ray_address("ray://host:10001")
            .build()
        )
        assert cluster.ray_init_kwargs == {}


class TestEnvVarsE2E:
    """Tests for env_vars flowing through config to K8s pod specs."""

    def test_env_vars_flow_to_head_pod_spec(self) -> None:
        """Env vars set on head_group should appear in K8s head pod definition."""
        from geneva.runners.ray.raycluster import _HeadGroupSpec

        cluster = (
            KubeRayClusterBuilder.create("test")
            .head_group(env_vars={"MY_VAR": "my_value"})
            .build()
        )
        head_cfg = cluster.kuberay.head_group
        spec = _HeadGroupSpec(**attrs.asdict(head_cfg))
        head_def = spec.definition
        containers = head_def["template"]["spec"]["containers"]
        env_list = containers[0]["env"]
        env_dict = {e["name"]: e["value"] for e in env_list}
        assert env_dict["MY_VAR"] == "my_value"

    def test_env_vars_flow_to_worker_pod_spec(self) -> None:
        """Env vars set on worker builder should appear in K8s worker pod definition."""
        from geneva.runners.ray.raycluster import _WorkerGroupSpec

        cluster = (
            KubeRayClusterBuilder.create("test")
            .add_worker_group(
                KubeRayClusterBuilder.cpu_worker()
                .env_vars({"WORKER_VAR": "worker_val"})
                .build()
            )
            .build()
        )
        wg_cfg = cluster.kuberay.worker_groups[0]
        spec = _WorkerGroupSpec(**attrs.asdict(wg_cfg))
        worker_def = spec.definition
        containers = worker_def["template"]["spec"]["containers"]
        env_list = containers[0]["env"]
        env_dict = {e["name"]: e["value"] for e in env_list}
        assert env_dict["WORKER_VAR"] == "worker_val"

    def test_env_vars_coexist_with_defaults(self) -> None:
        """Custom env vars coexist with defaults; no duplicate names in the env list."""
        from geneva.runners.ray.raycluster import _WorkerGroupSpec

        cluster = (
            KubeRayClusterBuilder.create("test")
            .add_worker_group(
                KubeRayClusterBuilder.cpu_worker()
                .env_vars({"CUSTOM_VAR": "custom_val"})
                .build()
            )
            .build()
        )
        wg_cfg = cluster.kuberay.worker_groups[0]
        spec = _WorkerGroupSpec(**attrs.asdict(wg_cfg))
        worker_def = spec.definition
        containers = worker_def["template"]["spec"]["containers"]
        env_list = containers[0]["env"]
        env_names = [e["name"] for e in env_list]
        # Default env vars should still be present
        assert "RAY_memory_usage_threshold" in env_names
        assert "CUSTOM_VAR" in env_names
        # No duplicate env var names
        assert len(env_names) == len(set(env_names))

    def test_env_vars_override_defaults(self) -> None:
        """User env vars override Geneva defaults when keys collide."""
        from geneva.runners.ray.raycluster import _WorkerGroupSpec

        cluster = (
            KubeRayClusterBuilder.create("test")
            .add_worker_group(
                KubeRayClusterBuilder.cpu_worker()
                .env_vars({"LANCE_LOG": "debug"})
                .build()
            )
            .build()
        )
        wg_cfg = cluster.kuberay.worker_groups[0]
        spec = _WorkerGroupSpec(**attrs.asdict(wg_cfg))
        worker_def = spec.definition
        containers = worker_def["template"]["spec"]["containers"]
        env_list = containers[0]["env"]
        env_dict = {e["name"]: e["value"] for e in env_list}
        # User value wins over the default
        assert env_dict["LANCE_LOG"] == "debug"
        # No duplicate env var names
        env_names = [e["name"] for e in env_list]
        assert len(env_names) == len(set(env_names))


class TestGenevaClusterFactories:
    """Tests for GenevaCluster static factory methods."""

    def test_kuberay_factory(self) -> None:
        """GenevaCluster.create_kuberay() should return KubeRayClusterBuilder."""
        builder = GenevaCluster.create_kuberay("test")
        assert isinstance(builder, KubeRayClusterBuilder)
        cluster = builder.build()
        assert cluster.cluster_type == GenevaClusterType.KUBE_RAY
        assert cluster.name == "test"

    def test_local_factory(self) -> None:
        """GenevaCluster.create_local() should return LocalRayClusterBuilder."""
        builder = GenevaCluster.create_local("test")
        assert isinstance(builder, LocalRayClusterBuilder)
        cluster = builder.build()
        assert cluster.cluster_type == GenevaClusterType.LOCAL_RAY

    def test_external_factory(self) -> None:
        """GenevaCluster.create_external() should return ExternalRayClusterBuilder."""
        builder = GenevaCluster.create_external("test", "ray://host:10001")
        assert isinstance(builder, ExternalRayClusterBuilder)
        cluster = builder.build()
        assert cluster.cluster_type == GenevaClusterType.EXTERNAL_RAY
        assert cluster.ray_address == "ray://host:10001"

    def test_full_workflow_with_factories(self) -> None:
        """Test complete workflow using factory methods."""
        cluster = (
            GenevaCluster.create_kuberay("my-cluster")
            .namespace("ml-team")
            .add_worker_group(
                KubeRayClusterBuilder.cpu_worker().cpus(8).memory("16Gi").build()
            )
            .add_worker_group(
                KubeRayClusterBuilder.gpu_worker(gpus=4).memory("64Gi").build()
            )
            .build()
        )

        assert cluster.name == "my-cluster"
        assert cluster.kuberay.namespace == "ml-team"
        assert len(cluster.kuberay.worker_groups) == 2

        cpu_worker = cluster.kuberay.worker_groups[0]
        assert cpu_worker.num_cpus == 8
        assert cpu_worker.num_gpus == 0

        gpu_worker = cluster.kuberay.worker_groups[1]
        assert gpu_worker.num_gpus == 4
        assert gpu_worker.memory == "64Gi"
