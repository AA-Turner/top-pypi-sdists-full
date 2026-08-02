# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for admission control."""

from unittest.mock import MagicMock, patch

import lance
import pyarrow as pa
import pytest

from geneva._context import LocalRayContext
from geneva.runners.ray.admission import (
    AdmissionDecision,
    ClusterResources,
    JobResources,
    NodeCapacity,
    PipelineResourceConfig,
    ResourcesUnavailableError,
    _check_kuberay_admission,
    _check_static_admission,
    _is_kuberay_cluster,
    calculate_job_resources,
    check_admission,
    validate_admission,
)
from geneva.runners.ray.raycluster import RayCluster
from geneva.transformer import UDF
from geneva.utils.ray import GENEVA_AUTOSCALING_RESOURCE


def make_udf(
    num_cpus: float = 1.0,
    num_gpus: float = 0.0,
    memory: int | None = None,
) -> UDF:
    """Create a simple UDF for testing."""

    def identity(x: str) -> str:
        return x

    return UDF(
        func=identity,
        num_cpus=num_cpus,
        num_gpus=num_gpus,
        memory=memory,
        data_type=pa.string(),
    )


class TestCalculateJobResources:
    """Tests for calculate_job_resources."""

    def test_cpu_only_udf(self) -> None:
        udf = make_udf(num_cpus=1.0, num_gpus=0.0)
        resources = calculate_job_resources(udf, concurrency=4)

        assert resources.applier_cpus == 4.0
        assert resources.applier_gpus == 0.0
        assert resources.concurrency == 4
        assert resources.udf_cpus == 1.0
        assert resources.udf_gpus == 0.0
        # Overhead includes driver (0.1), jobtracker (0.1), and writers (0.1 each)
        # Note: queues use 0 CPU and 0 memory
        assert resources.overhead_cpus == pytest.approx(0.6)

    def test_gpu_udf(self) -> None:
        udf = make_udf(num_cpus=1.0, num_gpus=1.0)
        resources = calculate_job_resources(udf, concurrency=8)

        assert resources.applier_cpus == 8.0
        assert resources.applier_gpus == 8.0
        assert resources.total_gpus == 8.0
        assert resources.udf_gpus == 1.0

    def test_fractional_gpu(self) -> None:
        udf = make_udf(num_cpus=0.5, num_gpus=0.5)
        resources = calculate_job_resources(udf, concurrency=4)

        assert resources.applier_cpus == 2.0
        assert resources.applier_gpus == 2.0
        assert resources.total_gpus == 2.0

    def test_intra_applier_concurrency(self) -> None:
        udf = make_udf(num_cpus=1.0)
        resources = calculate_job_resources(
            udf, concurrency=4, intra_applier_concurrency=2
        )

        assert resources.applier_cpus == 8.0
        assert resources.udf_cpus == 2.0

    def test_with_memory(self) -> None:
        udf = make_udf(num_cpus=1.0, memory=1024 * 1024 * 1024)
        resources = calculate_job_resources(udf, concurrency=4)

        assert resources.applier_memory == 4 * 1024 * 1024 * 1024

    def test_string_representation(self) -> None:
        udf = make_udf(num_cpus=2.0, num_gpus=1.0)
        resources = calculate_job_resources(udf, concurrency=4)

        s = str(resources)
        assert "cpus=" in s
        assert "gpus=" in s
        assert "concurrency=4" in s

    def test_gpu_pipelining_no_preprocess_reserves_one_thread(self) -> None:
        """Pipelining without preprocess() runs only reader + GPU loop.

        Regression: actor used to reserve 1 + pipelining_num_readers
        CPUs unconditionally, leaving K-1 idle on UDFs without
        preprocess (e.g. ``OpenClipEmbedFromTensor`` over a cached RGB
        column).
        """
        udf = make_udf(num_cpus=1.0)
        resources = calculate_job_resources(
            udf,
            concurrency=4,
            enable_gpu_pipelining=True,
            pipelining_num_readers=8,
        )

        assert resources.udf_cpus == 1.0
        assert resources.applier_cpus == 4.0

    def test_gpu_pipelining_with_preprocess_reserves_pool(self) -> None:
        """Pipelining + preprocess() reserves 1 + K reader/preprocess threads."""

        class _WithPreprocess:
            def preprocess(self, batch: pa.RecordBatch) -> pa.RecordBatch:
                return batch

            def __call__(self, x: str) -> str:
                return x

        udf = UDF(
            func=_WithPreprocess(),
            num_cpus=1.0,
            num_gpus=0.0,
            data_type=pa.string(),
        )
        resources = calculate_job_resources(
            udf,
            concurrency=4,
            enable_gpu_pipelining=True,
            pipelining_num_readers=8,
        )

        # 1 reader + 8 preprocess workers per actor, 4 actors.
        assert resources.udf_cpus == 9.0
        assert resources.applier_cpus == 36.0


class TestActorCpuThreadCount:
    """The single source of truth shared by setup_actor and admission."""

    def test_no_pipelining_uses_intra_applier_concurrency(self) -> None:
        from geneva.runners.ray.admission import actor_cpu_thread_count

        assert (
            actor_cpu_thread_count(
                enable_gpu_pipelining=False,
                pipelining_num_readers=8,
                has_preprocess=False,
                intra_applier_concurrency=4,
            )
            == 4
        )

    def test_pipelining_with_preprocess(self) -> None:
        from geneva.runners.ray.admission import actor_cpu_thread_count

        assert (
            actor_cpu_thread_count(
                enable_gpu_pipelining=True,
                pipelining_num_readers=8,
                has_preprocess=True,
                intra_applier_concurrency=1,
            )
            == 9
        )

    def test_pipelining_without_preprocess_does_not_pay_for_pool(self) -> None:
        from geneva.runners.ray.admission import actor_cpu_thread_count

        assert (
            actor_cpu_thread_count(
                enable_gpu_pipelining=True,
                pipelining_num_readers=8,
                has_preprocess=False,
                intra_applier_concurrency=1,
            )
            == 1
        )


class TestFragmentWriterScheduling:
    """GEN-631: FragmentWriter placement defaults to SPREAD across nodes."""

    @pytest.fixture(autouse=True)
    def _clear_scheduling_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Keep the default-resolution tests hermetic if a developer has the
        # env var exported in their shell.
        monkeypatch.delenv("GENEVA_FRAGMENT_WRITER_SCHEDULING", raising=False)

    def test_default_is_spread(self) -> None:
        rc = PipelineResourceConfig()
        assert rc.fragment_writer_scheduling == "spread"
        assert rc.fragment_writer_scheduling_strategy() == "SPREAD"

    def test_pack_maps_to_ray_default(self) -> None:
        # "pack" -> None lets Ray use its default (packing) hybrid scheduler.
        rc = PipelineResourceConfig(fragment_writer_scheduling="pack")
        assert rc.fragment_writer_scheduling_strategy() is None

    def test_value_is_normalized(self) -> None:
        rc = PipelineResourceConfig(fragment_writer_scheduling="  PACK  ")
        assert rc.fragment_writer_scheduling == "pack"
        assert rc.fragment_writer_scheduling_strategy() is None

    def test_unknown_falls_back_to_spread(self) -> None:
        rc = PipelineResourceConfig(fragment_writer_scheduling="bogus")
        assert rc.fragment_writer_scheduling_strategy() == "SPREAD"

    def test_short_env_var_default(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GENEVA_FRAGMENT_WRITER_SCHEDULING", "pack")
        rc = PipelineResourceConfig()
        assert rc.fragment_writer_scheduling == "pack"
        assert rc.fragment_writer_scheduling_strategy() is None


class TestCheckStaticAdmission:
    """Tests for static cluster admission."""

    def test_allow_sufficient_resources(self) -> None:
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=0.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=1024 * 1024 * 128,
            concurrency=4,
            udf_cpus=1.0,
            udf_gpus=0.0,
        )
        cluster = ClusterResources(
            total_cpus=16.0,
            total_gpus=0.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=12.0,
            available_gpus=0.0,
            available_memory=24 * 1024 * 1024 * 1024,
            node_capacities=[
                NodeCapacity(cpus=8.0, gpus=0.0, memory=16 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=8.0, gpus=0.0, memory=16 * 1024 * 1024 * 1024),
            ],
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.ALLOW
        assert "available" in message.lower()

    def test_reject_gpu_on_cpu_cluster(self) -> None:
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=4.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=4,
            udf_cpus=1.0,
            udf_gpus=1.0,
        )
        cluster = ClusterResources(
            total_cpus=16.0,
            total_gpus=0.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=12.0,
            available_gpus=0.0,
            available_memory=24 * 1024 * 1024 * 1024,
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "GPUs but cluster has none" in message

    def test_reject_more_gpus_than_available(self) -> None:
        job = JobResources(
            applier_cpus=8.0,
            applier_gpus=8.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=8,
            udf_cpus=1.0,
            udf_gpus=1.0,
        )
        cluster = ClusterResources(
            total_cpus=16.0,
            total_gpus=4.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=12.0,
            available_gpus=4.0,
            available_memory=24 * 1024 * 1024 * 1024,
            node_capacities=[
                NodeCapacity(cpus=4.0, gpus=1.0, memory=8 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=1.0, memory=8 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=1.0, memory=8 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=1.0, memory=8 * 1024 * 1024 * 1024),
            ],
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "Reduce concurrency to 4" in message

    def test_reject_more_cpus_than_available(self) -> None:
        job = JobResources(
            applier_cpus=16.0,
            applier_gpus=0.0,
            applier_memory=0,
            overhead_cpus=4.0,
            overhead_memory=0,
            concurrency=16,
            udf_cpus=1.0,
            udf_gpus=0.0,
        )
        cluster = ClusterResources(
            total_cpus=8.0,
            total_gpus=0.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=8.0,
            available_gpus=0.0,
            available_memory=24 * 1024 * 1024 * 1024,
            node_capacities=[
                NodeCapacity(cpus=4.0, gpus=0.0, memory=16 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=16 * 1024 * 1024 * 1024),
            ],
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "CPUs but cluster only has" in message

    def test_warn_resources_busy(self) -> None:
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=0.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=4,
            udf_cpus=1.0,
            udf_gpus=0.0,
        )
        cluster = ClusterResources(
            total_cpus=16.0,
            total_gpus=0.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=2.0,
            available_gpus=0.0,
            available_memory=24 * 1024 * 1024 * 1024,
            node_capacities=[
                NodeCapacity(cpus=8.0, gpus=0.0, memory=16 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=8.0, gpus=0.0, memory=16 * 1024 * 1024 * 1024),
            ],
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.ALLOW_WITH_WARNING
        assert "currently available" in message

    def test_reject_udf_cpus_exceed_node(self) -> None:
        """Test that UDF requiring more CPUs than any node has is rejected."""
        # UDF needs 8 CPUs but largest node only has 4 CPUs
        job = JobResources(
            applier_cpus=8.0,
            applier_gpus=0.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=1,
            udf_cpus=8.0,
            udf_gpus=0.0,
        )
        # 5 nodes × 4 CPUs = 20 CPUs total, but max per node is 4
        cluster = ClusterResources(
            total_cpus=20.0,
            total_gpus=0.0,
            total_memory=20 * 1024 * 1024 * 1024,
            available_cpus=20.0,
            available_gpus=0.0,
            available_memory=20 * 1024 * 1024 * 1024,
            node_capacities=[
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
            ],
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "no single node can satisfy" in message

    def test_reject_udf_memory_exceeds_node(self) -> None:
        """Test that UDF requiring more memory than any node has is rejected."""
        # UDF needs 8GB but largest node only has 4GB
        job = JobResources(
            applier_cpus=1.0,
            applier_gpus=0.0,
            applier_memory=8 * 1024 * 1024 * 1024,
            overhead_cpus=0.2,
            overhead_memory=0,
            concurrency=1,
            udf_cpus=1.0,
            udf_gpus=0.0,
            udf_memory=8 * 1024 * 1024 * 1024,
        )
        # 5 nodes × 4GB = 20GB total, but max per node is 4GB
        cluster = ClusterResources(
            total_cpus=20.0,
            total_gpus=0.0,
            total_memory=20 * 1024 * 1024 * 1024,
            available_cpus=20.0,
            available_gpus=0.0,
            available_memory=20 * 1024 * 1024 * 1024,
            node_capacities=[
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
            ],
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "no single node can satisfy" in message

    def test_reject_heterogeneous_nodes_no_combined_fit(self) -> None:
        """Test that heterogeneous nodes are correctly validated.

        Scenario: 4GB/8CPU nodes + 8GB/4CPU nodes, UDF needs 8GB + 8CPU.
        No single node can satisfy both requirements even though the cluster
        has enough total resources and each requirement is individually met.
        """
        job = JobResources(
            applier_cpus=8.0,
            applier_gpus=0.0,
            applier_memory=8 * 1024 * 1024 * 1024,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=1,
            udf_cpus=8.0,
            udf_gpus=0.0,
            udf_memory=8 * 1024 * 1024 * 1024,
        )
        # Heterogeneous cluster:
        # - Node A: 8 CPUs, 4GB memory (can't fit 8GB memory requirement)
        # - Node B: 4 CPUs, 8GB memory (can't fit 8 CPU requirement)
        cluster = ClusterResources(
            total_cpus=12.0,  # 8 + 4
            total_gpus=0.0,
            total_memory=12 * 1024 * 1024 * 1024,  # 4 + 8
            available_cpus=12.0,
            available_gpus=0.0,
            available_memory=12 * 1024 * 1024 * 1024,
            node_capacities=[
                NodeCapacity(cpus=8.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=8 * 1024 * 1024 * 1024),
            ],
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "no single node can satisfy" in message
        assert "8.0 CPUs" in message
        assert "memory" in message  # Memory value depends on GiB to GB conversion

    def test_reject_udf_gpus_exceed_node_via_legacy_max(self) -> None:
        """Test rejection when node_capacities is empty but max_node values are set.

        This covers the case where per-node capacity list is unavailable (e.g.,
        KubeRay API query failed with no workers running), but we still have
        legacy max-per-node values from a prior query.
        """
        # UDF needs 60 GPUs but max node has 8 GPUs
        job = JobResources(
            applier_cpus=100.0,
            applier_gpus=6000.0,
            applier_memory=0,
            overhead_cpus=10.0,
            overhead_memory=0,
            concurrency=100,
            udf_cpus=1.0,
            udf_gpus=60.0,
        )
        # Cluster has lots of total GPUs but no single node has 60
        cluster = ClusterResources(
            total_cpus=800.0,
            total_gpus=8000.0,
            total_memory=800 * 1024 * 1024 * 1024,
            available_cpus=800.0,
            available_gpus=8000.0,
            available_memory=800 * 1024 * 1024 * 1024,
            node_capacities=None,  # No per-node info available
            max_node_cpus=8.0,
            max_node_gpus=8.0,
            max_node_memory=64 * 1024 * 1024 * 1024,
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "no single node can satisfy" in message

    def test_reject_total_memory_exceeds_cluster(self) -> None:
        """Test that jobs requiring more total memory than cluster has are rejected."""
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=0.0,
            applier_memory=100 * 1024 * 1024 * 1024,  # 100 GB
            overhead_cpus=1.0,
            overhead_memory=10 * 1024 * 1024 * 1024,  # 10 GB
            concurrency=4,
            udf_cpus=1.0,
            udf_gpus=0.0,
            udf_memory=25 * 1024 * 1024 * 1024,
        )
        cluster = ClusterResources(
            total_cpus=16.0,
            total_gpus=0.0,
            total_memory=32 * 1024 * 1024 * 1024,  # 32 GB
            available_cpus=16.0,
            available_gpus=0.0,
            available_memory=32 * 1024 * 1024 * 1024,
            node_capacities=[
                NodeCapacity(cpus=8.0, gpus=0.0, memory=32 * 1024 * 1024 * 1024),
            ],
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "memory" in message.lower()

    def test_reject_no_per_node_info(self) -> None:
        """Test that UDFs are rejected when no per-node info is available."""
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=0.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=4,
            udf_cpus=1.0,
            udf_gpus=0.0,
        )
        cluster = ClusterResources(
            total_cpus=16.0,
            total_gpus=0.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=12.0,
            available_gpus=0.0,
            available_memory=24 * 1024 * 1024 * 1024,
            node_capacities=None,
            max_node_cpus=0.0,
            max_node_gpus=0.0,
            max_node_memory=0,
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "no single node" in message

    def test_allow_legacy_fallback_partial_info(self) -> None:
        """Test that legacy fallback works when only some dimensions have data.

        CPU-only clusters may not track per-node memory (max_node_memory=0).
        The fallback should only check dimensions with reported data, so a UDF
        requesting memory should NOT be rejected just because memory isn't tracked.
        """
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=0.0,
            applier_memory=4 * 1024 * 1024 * 1024,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=4,
            udf_cpus=1.0,
            udf_gpus=0.0,
            udf_memory=1024 * 1024 * 1024,  # 1GB
        )
        cluster = ClusterResources(
            total_cpus=16.0,
            total_gpus=0.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=12.0,
            available_gpus=0.0,
            available_memory=24 * 1024 * 1024 * 1024,
            node_capacities=None,
            max_node_cpus=8.0,
            max_node_gpus=0.0,
            max_node_memory=0,  # Memory not tracked per-node
        )

        decision, message = _check_static_admission(job, cluster)

        # Should ALLOW — UDF fits within per-node CPUs and memory isn't tracked
        assert decision == AdmissionDecision.ALLOW

    def test_allow_heterogeneous_nodes_with_fit(self) -> None:
        """Test that heterogeneous nodes allow jobs when one node can fit."""
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=0.0,
            applier_memory=4 * 1024 * 1024 * 1024,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=1,
            udf_cpus=4.0,
            udf_gpus=0.0,
            udf_memory=4 * 1024 * 1024 * 1024,
        )
        # Heterogeneous cluster with one node that can fit:
        # - Node A: 8 CPUs, 4GB memory (can fit 4 CPU + 4GB)
        # - Node B: 4 CPUs, 8GB memory (can also fit 4 CPU + 4GB)
        cluster = ClusterResources(
            total_cpus=12.0,
            total_gpus=0.0,
            total_memory=12 * 1024 * 1024 * 1024,
            available_cpus=12.0,
            available_gpus=0.0,
            available_memory=12 * 1024 * 1024 * 1024,
            node_capacities=[
                NodeCapacity(cpus=8.0, gpus=0.0, memory=4 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=4.0, gpus=0.0, memory=8 * 1024 * 1024 * 1024),
            ],
        )

        decision, message = _check_static_admission(job, cluster)

        assert decision == AdmissionDecision.ALLOW


class TestCheckKuberayAdmission:
    """Tests for KubeRay cluster admission."""

    def test_allow_within_max_scale(self) -> None:
        job = JobResources(
            applier_cpus=8.0,
            applier_gpus=8.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=8,
            udf_cpus=1.0,
            udf_gpus=1.0,
        )
        cluster = ClusterResources(
            total_cpus=4.0,
            total_gpus=4.0,
            total_memory=16 * 1024 * 1024 * 1024,
            available_cpus=4.0,
            available_gpus=4.0,
            available_memory=16 * 1024 * 1024 * 1024,
            is_kuberay=True,
            max_scale_cpus=32.0,
            max_scale_gpus=16.0,
            max_scale_memory=128 * 1024 * 1024 * 1024,
            node_capacities=[
                NodeCapacity(cpus=4.0, gpus=1.0, memory=16 * 1024 * 1024 * 1024),
            ],
        )

        decision, message = _check_kuberay_admission(job, cluster)

        assert decision == AdmissionDecision.ALLOW_WITH_WARNING
        assert "scale up" in message

    def test_reject_gpu_on_non_gpu_cluster(self) -> None:
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=4.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=4,
            udf_cpus=1.0,
            udf_gpus=1.0,
        )
        cluster = ClusterResources(
            total_cpus=16.0,
            total_gpus=0.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=16.0,
            available_gpus=0.0,
            available_memory=32 * 1024 * 1024 * 1024,
            is_kuberay=True,
            max_scale_cpus=64.0,
            max_scale_gpus=0.0,
            max_scale_memory=256 * 1024 * 1024 * 1024,
        )

        decision, message = _check_kuberay_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "no GPU worker groups" in message

    def test_reject_exceeds_max_scale(self) -> None:
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=16.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=16,
            udf_cpus=0.25,
            udf_gpus=1.0,
        )
        cluster = ClusterResources(
            total_cpus=8.0,
            total_gpus=4.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=8.0,
            available_gpus=4.0,
            available_memory=32 * 1024 * 1024 * 1024,
            is_kuberay=True,
            max_scale_cpus=64.0,
            max_scale_gpus=8.0,
            max_scale_memory=256 * 1024 * 1024 * 1024,
            node_capacities=[
                NodeCapacity(cpus=4.0, gpus=1.0, memory=16 * 1024 * 1024 * 1024),
            ],
        )

        decision, message = _check_kuberay_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "maxReplicas" in message

    def test_reject_udf_gpus_exceed_node_no_capacities(self) -> None:
        """Test rejection when UDF needs more GPUs than any worker group.

        Covers the scenario where node_capacities is None (e.g., KubeRay API
        failed) but legacy max_node values are available.
        """
        # UDF needs 60 GPUs, cluster has lots of total GPUs at max scale
        job = JobResources(
            applier_cpus=100.0,
            applier_gpus=6000.0,
            applier_memory=0,
            overhead_cpus=10.0,
            overhead_memory=0,
            concurrency=100,
            udf_cpus=1.0,
            udf_gpus=60.0,
        )
        cluster = ClusterResources(
            total_cpus=800.0,
            total_gpus=800.0,
            total_memory=800 * 1024 * 1024 * 1024,
            available_cpus=800.0,
            available_gpus=800.0,
            available_memory=800 * 1024 * 1024 * 1024,
            is_kuberay=True,
            max_scale_cpus=8000.0,
            max_scale_gpus=8000.0,
            max_scale_memory=8000 * 1024 * 1024 * 1024,
            node_capacities=None,  # KubeRay API failed
            max_node_cpus=8.0,
            max_node_gpus=8.0,
            max_node_memory=64 * 1024 * 1024 * 1024,
        )

        decision, message = _check_kuberay_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "no worker group can satisfy" in message

    def test_reject_total_memory_exceeds_max_scale(self) -> None:
        """Test that jobs requiring more memory than max scale are rejected."""
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=0.0,
            applier_memory=500 * 1024 * 1024 * 1024,
            overhead_cpus=1.0,
            overhead_memory=10 * 1024 * 1024 * 1024,
            concurrency=4,
            udf_cpus=1.0,
            udf_gpus=0.0,
            udf_memory=125 * 1024 * 1024 * 1024,
        )
        cluster = ClusterResources(
            total_cpus=16.0,
            total_gpus=0.0,
            total_memory=64 * 1024 * 1024 * 1024,
            available_cpus=16.0,
            available_gpus=0.0,
            available_memory=64 * 1024 * 1024 * 1024,
            is_kuberay=True,
            max_scale_cpus=64.0,
            max_scale_gpus=0.0,
            max_scale_memory=256 * 1024 * 1024 * 1024,
            node_capacities=[
                NodeCapacity(cpus=16.0, gpus=0.0, memory=256 * 1024 * 1024 * 1024),
            ],
        )

        decision, message = _check_kuberay_admission(job, cluster)

        assert decision == AdmissionDecision.REJECT
        assert "memory" in message.lower()


class TestCheckAdmission:
    """Tests for the main check_admission function."""

    def test_routes_to_static_check(self) -> None:
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=0.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=4,
            udf_cpus=1.0,
            udf_gpus=0.0,
        )
        cluster = ClusterResources(
            total_cpus=16.0,
            total_gpus=0.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=12.0,
            available_gpus=0.0,
            available_memory=24 * 1024 * 1024 * 1024,
            is_kuberay=False,
            node_capacities=[
                NodeCapacity(cpus=8.0, gpus=0.0, memory=16 * 1024 * 1024 * 1024),
                NodeCapacity(cpus=8.0, gpus=0.0, memory=16 * 1024 * 1024 * 1024),
            ],
        )

        decision, _ = check_admission(job, cluster)
        assert decision == AdmissionDecision.ALLOW

    def test_routes_to_kuberay_check(self) -> None:
        job = JobResources(
            applier_cpus=4.0,
            applier_gpus=4.0,
            applier_memory=0,
            overhead_cpus=1.0,
            overhead_memory=0,
            concurrency=4,
            udf_cpus=1.0,
            udf_gpus=1.0,
        )
        cluster = ClusterResources(
            total_cpus=8.0,
            total_gpus=0.0,
            total_memory=32 * 1024 * 1024 * 1024,
            available_cpus=8.0,
            available_gpus=0.0,
            available_memory=32 * 1024 * 1024 * 1024,
            is_kuberay=True,
            max_scale_cpus=32.0,
            max_scale_gpus=0.0,
            max_scale_memory=128 * 1024 * 1024 * 1024,
        )

        decision, message = check_admission(job, cluster)
        assert decision == AdmissionDecision.REJECT
        assert "GPU" in message


class TestValidateAdmissionResourceQueryFailure:
    """Tests for validate_admission when cluster resources can't be queried."""

    def test_strict_mode_raises_when_static_cluster_unavailable(self) -> None:
        """In strict mode, raise if static cluster resources can't be queried.

        If ray.nodes() times out, we have no data to validate against, so
        the job should be rejected rather than allowed to hang.
        """
        udf = make_udf(num_gpus=60.0)

        with (
            patch("geneva.runners.ray.admission.ray.is_initialized", return_value=True),
            patch(
                "geneva.runners.ray.admission._is_kuberay_cluster", return_value=False
            ),
            patch(
                "geneva.runners.ray.admission.get_cluster_resources", return_value=None
            ),
            pytest.raises(ResourcesUnavailableError, match="could not query"),
        ):
            validate_admission(udf, concurrency=100, check=True, strict=True)

    def test_non_strict_mode_skips_when_resources_unavailable(self) -> None:
        """In non-strict mode, warn and allow if resources can't be queried."""
        udf = make_udf(num_gpus=60.0)

        with (
            patch("geneva.runners.ray.admission.ray.is_initialized", return_value=True),
            patch(
                "geneva.runners.ray.admission._is_kuberay_cluster", return_value=False
            ),
            patch(
                "geneva.runners.ray.admission.get_cluster_resources", return_value=None
            ),
        ):
            # Should not raise — non-strict mode skips gracefully
            validate_admission(udf, concurrency=100, check=True, strict=False)

    def test_strict_mode_raises_when_kuberay_api_fails(self) -> None:
        """In strict mode, raise if KubeRay K8s API query fails.

        get_kuberay_cluster_resources returns None on K8s API failure,
        which should be treated the same as any other resource query failure.
        """
        udf = make_udf(num_gpus=60.0)

        with (
            patch("geneva.runners.ray.admission.ray.is_initialized", return_value=True),
            patch(
                "geneva.runners.ray.admission._is_kuberay_cluster", return_value=True
            ),
            patch(
                "geneva.runners.ray.admission.get_kuberay_cluster_resources",
                return_value=None,
            ),
            pytest.raises(ResourcesUnavailableError, match="could not query"),
        ):
            validate_admission(udf, concurrency=100, check=True, strict=True)


class TestIsKuberayCluster:
    """Tests for _is_kuberay_cluster detection."""

    def test_detects_geneva_autoscaling_resource(self) -> None:
        """Test detection via geneva_autoscaling resource."""
        with (
            patch("geneva.runners.ray.admission.ray.is_initialized", return_value=True),
            patch(
                "geneva.runners.ray.admission.ray.cluster_resources",
                return_value={GENEVA_AUTOSCALING_RESOURCE: 1.0, "CPU": 8.0},
            ),
        ):
            assert _is_kuberay_cluster() is True

    def test_not_kuberay_without_resource(self) -> None:
        """Test that cluster is not detected as KubeRay without the resource."""
        with (
            patch("geneva.runners.ray.admission.ray.is_initialized", return_value=True),
            patch(
                "geneva.runners.ray.admission.ray.cluster_resources",
                return_value={"CPU": 8.0, "GPU": 4.0},
            ),
            patch(
                "geneva.runners.ray.admission.get_current_context", return_value=None
            ),
        ):
            assert _is_kuberay_cluster() is False

    def test_fallback_to_context(self) -> None:
        """Test fallback to Geneva context when Ray resource check fails."""
        mock_ctx = MagicMock(spec=RayCluster)
        mock_ctx.namespace = "test-ns"
        mock_ctx.name = "test-cluster"

        with (
            patch(
                "geneva.runners.ray.admission.ray.is_initialized", return_value=False
            ),
            patch(
                "geneva.runners.ray.admission.get_current_context",
                return_value=mock_ctx,
            ),
        ):
            assert _is_kuberay_cluster() is True

    def test_not_kuberay_without_context(self) -> None:
        """Test that cluster is not detected as KubeRay without context."""
        with (
            patch(
                "geneva.runners.ray.admission.ray.is_initialized", return_value=False
            ),
            patch(
                "geneva.runners.ray.admission.get_current_context", return_value=None
            ),
        ):
            assert _is_kuberay_cluster() is False

    def test_local_ray_context_returns_false(self) -> None:
        """Test that LocalRayContext (local Ray cluster) is not detected as KubeRay."""
        with (
            patch(
                "geneva.runners.ray.admission.get_current_context",
                return_value=LocalRayContext(),
            ),
        ):
            assert _is_kuberay_cluster() is False


@pytest.mark.ray
class TestBackfillAdmissionControlIntegration:
    """Integration tests for admission control with real Ray cluster.

    These tests verify that backfill_async properly rejects jobs with excessive
    resource requirements WITHOUT explicitly setting _admission_check=True.

    This is a regression test for a bug where admission control was only invoked
    if _admission_check was explicitly set (it defaulted to None which is falsy).
    """

    @pytest.fixture(autouse=True)
    def ray_cluster(self) -> None:
        """Start a local Ray cluster for each test."""
        import ray

        ray.shutdown()
        ray.init()
        yield
        ray.shutdown()

    @pytest.fixture
    def db(self, tmp_path) -> None:
        """Create a test database with a simple table."""
        import geneva

        # Create a simple table with one column
        tbl_path = tmp_path / "test.lance"
        lance.write_dataset(pa.table({"a": [1, 2, 3]}), tbl_path)
        db = geneva.connect(str(tmp_path))
        yield db
        db.close()

    def test_backfill_rejects_excessive_gpu_without_explicit_flag(self, db) -> None:
        """Backfill with UDF requiring 1000 GPUs fails without _admission_check.

        This is the key regression test - before the fix, this would NOT raise
        because admission control was not invoked when _admission_check=None.
        """

        from geneva import udf
        from geneva.runners.ray.admission import ResourcesUnavailableError

        @udf(data_type=pa.int32(), num_gpus=1000)
        def excessive_gpu_udf(a: int) -> int:
            return a * 2

        tbl = db.open_table("test")
        tbl.add_columns({"b": excessive_gpu_udf})

        # Key: we do NOT pass _admission_check=True here
        # Before the fix, this would hang instead of failing fast
        with pytest.raises(ResourcesUnavailableError) as exc_info:
            tbl.backfill_async("b")

        assert "GPU" in str(exc_info.value)

    def test_backfill_rejects_excessive_cpu_without_explicit_flag(self, db) -> None:
        """Backfill with UDF requiring 10000 CPUs fails without _admission_check."""

        from geneva import udf
        from geneva.runners.ray.admission import ResourcesUnavailableError

        @udf(data_type=pa.int32(), num_cpus=10000)
        def excessive_cpu_udf(a: int) -> int:
            return a * 2

        tbl = db.open_table("test")
        tbl.add_columns({"b": excessive_cpu_udf})

        with pytest.raises(ResourcesUnavailableError) as exc_info:
            tbl.backfill_async("b")

        assert "CPU" in str(exc_info.value)

    def test_backfill_rejects_excessive_memory_without_explicit_flag(self, db) -> None:
        """Backfill with UDF requiring 1PB memory fails without _admission_check."""
        from geneva import udf
        from geneva.runners.ray.admission import ResourcesUnavailableError

        # Request 1 petabyte of memory per UDF instance
        one_petabyte = 1024**5

        @udf(data_type=pa.int32(), memory=one_petabyte)
        def excessive_memory_udf(a: int) -> int:
            return a * 2

        tbl = db.open_table("test")
        tbl.add_columns({"b": excessive_memory_udf})

        with pytest.raises(ResourcesUnavailableError) as exc_info:
            tbl.backfill_async("b")

        assert "memory" in str(exc_info.value).lower()

    def test_backfill_can_disable_admission_check(self, db) -> None:
        """Verify _admission_check=False bypasses validation.

        With admission check disabled, backfill_async should return a future
        without raising ResourcesUnavailableError, even though the job would
        eventually fail when Ray can't schedule the actors.
        """
        from geneva import udf

        @udf(data_type=pa.int32(), num_gpus=1000)
        def excessive_gpu_udf(a: int) -> int:
            return a * 2

        tbl = db.open_table("test")
        tbl.add_columns({"b": excessive_gpu_udf})

        # With _admission_check=False, no ResourcesUnavailableError should be raised
        # We just verify the call doesn't raise - we don't wait for completion
        fut = tbl.backfill_async("b", _admission_check=False)
        # If we get here without ResourcesUnavailableError, admission was bypassed
        assert fut is not None, "backfill_async should return a future"
        # Don't wait for completion - job will hang forever waiting for 1000 GPUs

    def test_backfill_with_admission_control_local_ray(self, db) -> None:
        """Backfill with _admission_check=True works in local_ray_context (static
        admission).

        Uses static admission (no KubeRay), so _is_kuberay_cluster() is False and
        admission doesn't query cluster resources. Verifies the path completes
        successfully.
        """
        from geneva import udf

        @udf(data_type=pa.int32())
        def plus_one(a: int) -> int:
            return a + 1

        tbl = db.open_table("test")
        tbl.add_columns({"b": plus_one})
        with db.local_ray_context():
            tbl.backfill(
                "b", _admission_check=True, _admission_strict=True, concurrency=2
            )
        result = tbl.to_arrow()
        assert result.column("b").to_pylist() == [2, 3, 4]


class TestPipelineResourceConfig:
    """Tests for PipelineResourceConfig."""

    def test_default_values(self) -> None:
        config = PipelineResourceConfig()
        assert config.driver_num_cpus == 0.1
        assert config.jobtracker_num_cpus == 0.1
        assert config.jobtracker_memory == 128 * 1024 * 1024
        assert config.fragment_writer_num_cpus == 0.1
        assert config.fragment_writer_memory == 1024 * 1024 * 1024

    def test_custom_values(self) -> None:
        config = PipelineResourceConfig(
            driver_num_cpus=0.2,
            jobtracker_num_cpus=0.5,
            jobtracker_memory=256 * 1024 * 1024,
            fragment_writer_num_cpus=0.3,
            fragment_writer_memory=2 * 1024 * 1024 * 1024,
        )
        assert config.driver_num_cpus == 0.2
        assert config.jobtracker_num_cpus == 0.5
        assert config.jobtracker_memory == 256 * 1024 * 1024
        assert config.fragment_writer_num_cpus == 0.3
        assert config.fragment_writer_memory == 2 * 1024 * 1024 * 1024

    def test_type_conversion(self) -> None:
        config = PipelineResourceConfig(
            driver_num_cpus="0.5",
            jobtracker_memory="268435456",
        )
        assert config.driver_num_cpus == 0.5
        assert isinstance(config.driver_num_cpus, float)
        assert config.jobtracker_memory == 268435456
        assert isinstance(config.jobtracker_memory, int)

    def test_config_name(self) -> None:
        assert PipelineResourceConfig.name() == "geneva_pipeline_resources"

    def test_env_var_override(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Clear the lru_cache so env vars are picked up
        PipelineResourceConfig.get.cache_clear()
        monkeypatch.setenv("GENEVA_PIPELINE_RESOURCES__DRIVER_NUM_CPUS", "0.5")
        monkeypatch.setenv("GENEVA_PIPELINE_RESOURCES__JOBTRACKER_MEMORY", "268435456")
        try:
            config = PipelineResourceConfig.get()
            assert config.driver_num_cpus == 0.5
            assert config.jobtracker_memory == 268435456
        finally:
            PipelineResourceConfig.get.cache_clear()

    def test_calculate_job_resources_uses_config(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Verify calculate_job_resources uses PipelineResourceConfig values."""
        PipelineResourceConfig.get.cache_clear()
        monkeypatch.setenv("GENEVA_PIPELINE_RESOURCES__DRIVER_NUM_CPUS", "0.2")
        monkeypatch.setenv("GENEVA_PIPELINE_RESOURCES__JOBTRACKER_NUM_CPUS", "0.3")
        monkeypatch.setenv("GENEVA_PIPELINE_RESOURCES__FRAGMENT_WRITER_NUM_CPUS", "0.4")
        try:
            udf = make_udf(num_cpus=1.0)
            resources = calculate_job_resources(udf, concurrency=2)
            # overhead_cpus = driver(0.2) + jobtracker(0.3) + 2*writer(0.4) = 1.3
            assert resources.overhead_cpus == pytest.approx(1.3)
        finally:
            PipelineResourceConfig.get.cache_clear()
