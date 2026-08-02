# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Unit tests for k8s_spec_override functionality in GenevaCluster"""

from pathlib import Path

from geneva import connect
from geneva.cluster import GenevaClusterType, K8sConfigMethod
from geneva.cluster.mgr import (
    GenevaCluster,
    HeadGroupConfig,
    KubeRayConfig,
    WorkerGroupConfig,
)


def test_cluster_extra_params_basic(tmp_path: Path) -> None:
    """Test creating a cluster with k8s_spec_override in both head and worker groups"""
    geneva = connect(tmp_path)

    head_group = HeadGroupConfig(
        service_account="test-account",
        num_cpus=1,
        memory="4Gi",
        image="rayproject/ray:2.54.0-py310",
        node_selector={"test": "head"},
        labels={},
        tolerations=[],
        k8s_spec_override={
            "template": {
                "spec": {
                    "containers": [
                        {"env": [{"name": "HEAD_VAR", "value": "head_value"}]}
                    ],
                    "priorityClassName": "high-priority",
                }
            }
        },
    )

    worker_groups = [
        WorkerGroupConfig(
            service_account="test-account",
            num_cpus=2,
            memory="8Gi",
            image="rayproject/ray:2.54.0-py310",
            node_selector={"test": "worker"},
            labels={},
            tolerations=[],
            num_gpus=0,
            k8s_spec_override={
                "replicas": 2,
                "minReplicas": 1,
                "maxReplicas": 5,
                "template": {
                    "spec": {
                        "containers": [
                            {"env": [{"name": "WORKER_VAR", "value": "worker_value"}]}
                        ]
                    }
                },
            },
        ),
    ]

    kuberay_config = KubeRayConfig(
        namespace="test-namespace",
        head_group=head_group,
        worker_groups=worker_groups,
        config_method=K8sConfigMethod.LOCAL,
    )

    cluster = GenevaCluster(
        cluster_type=GenevaClusterType.KUBE_RAY,
        name="test-cluster-k8s-override",
        kuberay=kuberay_config,
    )

    # Create the cluster definition
    geneva.define_cluster("test-cluster-k8s-override", cluster)

    # Load it back
    loaded_cluster = geneva.list_clusters()[0]

    # Verify k8s_spec_override persisted
    assert (
        loaded_cluster.kuberay.head_group.k8s_spec_override["template"]["spec"][
            "priorityClassName"
        ]
        == "high-priority"
    )
    assert loaded_cluster.kuberay.worker_groups[0].k8s_spec_override["replicas"] == 2
    assert loaded_cluster.kuberay.worker_groups[0].k8s_spec_override["minReplicas"] == 1
    assert loaded_cluster.kuberay.worker_groups[0].k8s_spec_override["maxReplicas"] == 5

    # Clean up
    geneva.delete_cluster("test-cluster-k8s-override")


def test_cluster_extra_params_to_ray_cluster(tmp_path: Path) -> None:
    """Test that k8s_spec_override is properly passed to RayCluster"""
    geneva = connect(tmp_path)

    head_group = HeadGroupConfig(
        service_account="test-account",
        num_cpus=1,
        memory="4Gi",
        image="rayproject/ray:2.54.0-py310",
        node_selector={"test": "head"},
        labels={},
        tolerations=[],
        k8s_spec_override={
            "template": {
                "spec": {"securityContext": {"runAsNonRoot": True, "fsGroup": 1000}}
            }
        },
    )

    worker_groups = [
        WorkerGroupConfig(
            service_account="test-account",
            num_cpus=2,
            memory="8Gi",
            image="rayproject/ray:2.54.0-py310",
            node_selector={"test": "worker"},
            labels={},
            tolerations=[],
            num_gpus=0,
            k8s_spec_override={
                "replicas": 3,
                "minReplicas": 1,
                "maxReplicas": 10,
                "template": {
                    "spec": {
                        "initContainers": [{"name": "init", "image": "busybox:1.35"}]
                    }
                },
            },
        ),
    ]

    kuberay_config = KubeRayConfig(
        namespace="test-namespace",
        head_group=head_group,
        worker_groups=worker_groups,
        config_method=K8sConfigMethod.LOCAL,
    )

    cluster = GenevaCluster(
        cluster_type=GenevaClusterType.KUBE_RAY,
        name="test-to-ray-cluster",
        kuberay=kuberay_config,
    )

    geneva.define_cluster("test-to-ray-cluster", cluster)
    loaded_cluster = geneva.list_clusters()[0]

    # Convert to RayCluster
    ray_cluster = loaded_cluster.to_ray_cluster()

    # Verify head group has k8s_spec_override
    assert ray_cluster.head_group.k8s_spec_override is not None
    assert (
        ray_cluster.head_group.k8s_spec_override["template"]["spec"]["securityContext"][
            "runAsNonRoot"
        ]
        is True
    )

    # Verify worker group has k8s_spec_override
    assert len(ray_cluster.worker_groups) == 1
    worker = ray_cluster.worker_groups[0]
    assert worker.k8s_spec_override is not None
    assert worker.k8s_spec_override["replicas"] == 3
    assert worker.k8s_spec_override["minReplicas"] == 1
    assert worker.k8s_spec_override["maxReplicas"] == 10
    assert (
        worker.k8s_spec_override["template"]["spec"]["initContainers"][0]["name"]
        == "init"
    )

    # Clean up
    geneva.delete_cluster("test-to-ray-cluster")


def test_cluster_without_extra_params(tmp_path: Path) -> None:
    """Test backward compatibility: clusters without k8s_spec_override work fine"""
    geneva = connect(tmp_path)

    head_group = HeadGroupConfig(
        service_account="test-account",
        num_cpus=1,
        memory="4Gi",
        image="rayproject/ray:2.54.0-py310",
        node_selector={"test": "head"},
        labels={},
        tolerations=[],
        # No k8s_spec_override - should default to None
    )

    worker_groups = [
        WorkerGroupConfig(
            service_account="test-account",
            num_cpus=2,
            memory="8Gi",
            image="rayproject/ray:2.54.0-py310",
            node_selector={"test": "worker"},
            labels={},
            tolerations=[],
            num_gpus=0,
            # No k8s_spec_override - should default to None
        ),
    ]

    kuberay_config = KubeRayConfig(
        namespace="test-namespace",
        head_group=head_group,
        worker_groups=worker_groups,
        config_method=K8sConfigMethod.LOCAL,
    )

    cluster = GenevaCluster(
        cluster_type=GenevaClusterType.KUBE_RAY,
        name="test-no-k8s-override",
        kuberay=kuberay_config,
    )

    geneva.define_cluster("test-no-k8s-override", cluster)
    loaded_cluster = geneva.list_clusters()[0]

    # Verify k8s_spec_override defaults to None
    assert loaded_cluster.kuberay.head_group.k8s_spec_override is None
    assert loaded_cluster.kuberay.worker_groups[0].k8s_spec_override is None

    # Should convert to RayCluster without errors
    ray_cluster = loaded_cluster.to_ray_cluster()
    assert ray_cluster.head_group.k8s_spec_override is None
    assert ray_cluster.worker_groups[0].k8s_spec_override is None

    # Clean up
    geneva.delete_cluster("test-no-k8s-override")


def test_cluster_multiple_worker_groups_with_different_extra_params(
    tmp_path: Path,
) -> None:
    """Test multiple worker groups each with different k8s_spec_override"""
    geneva = connect(tmp_path)

    head_group = HeadGroupConfig(
        service_account="test-account",
        num_cpus=1,
        memory="4Gi",
        image="rayproject/ray:2.54.0-py310",
        node_selector={"test": "head"},
        labels={},
        tolerations=[],
    )

    worker_groups = [
        WorkerGroupConfig(
            service_account="test-account",
            num_cpus=2,
            memory="8Gi",
            image="rayproject/ray:2.54.0-py310",
            node_selector={"test": "cpu"},
            labels={},
            tolerations=[],
            num_gpus=0,
            k8s_spec_override={
                "replicas": 2,
                "minReplicas": 1,
                "maxReplicas": 5,
            },
        ),
        WorkerGroupConfig(
            service_account="test-account",
            num_cpus=4,
            memory="16Gi",
            image="rayproject/ray:2.54.0-py310-gpu",
            node_selector={"test": "gpu"},
            labels={},
            tolerations=[],
            num_gpus=1,
            k8s_spec_override={
                "replicas": 1,
                "minReplicas": 0,
                "maxReplicas": 3,
                "scaleStrategy": {"workersToDelete": []},
            },
        ),
    ]

    kuberay_config = KubeRayConfig(
        namespace="test-namespace",
        head_group=head_group,
        worker_groups=worker_groups,
        config_method=K8sConfigMethod.LOCAL,
    )

    cluster = GenevaCluster(
        cluster_type=GenevaClusterType.KUBE_RAY,
        name="test-multi-workers",
        kuberay=kuberay_config,
    )

    geneva.define_cluster("test-multi-workers", cluster)
    loaded_cluster = geneva.list_clusters()[0]

    # Convert to RayCluster
    ray_cluster = loaded_cluster.to_ray_cluster()

    # Verify CPU worker group has k8s_spec_override
    cpu_worker = ray_cluster.worker_groups[0]
    assert cpu_worker.k8s_spec_override is not None
    assert cpu_worker.k8s_spec_override["replicas"] == 2
    assert cpu_worker.k8s_spec_override["minReplicas"] == 1
    assert cpu_worker.k8s_spec_override["maxReplicas"] == 5

    # Verify GPU worker group has k8s_spec_override
    gpu_worker = ray_cluster.worker_groups[1]
    assert gpu_worker.k8s_spec_override is not None
    assert gpu_worker.k8s_spec_override["replicas"] == 1
    assert gpu_worker.k8s_spec_override["minReplicas"] == 0
    assert gpu_worker.k8s_spec_override["maxReplicas"] == 3
    assert "scaleStrategy" in gpu_worker.k8s_spec_override

    # Clean up
    geneva.delete_cluster("test-multi-workers")


def test_cluster_extra_params_update(tmp_path: Path) -> None:
    """Test updating a cluster's k8s_spec_override"""
    geneva = connect(tmp_path)

    head_group = HeadGroupConfig(
        service_account="test-account",
        num_cpus=1,
        memory="4Gi",
        image="rayproject/ray:2.54.0-py310",
        node_selector={"test": "head"},
        labels={},
        tolerations=[],
        k8s_spec_override={
            "template": {
                "spec": {"containers": [{"env": [{"name": "VERSION", "value": "v1"}]}]}
            }
        },
    )

    worker_groups = [
        WorkerGroupConfig(
            service_account="test-account",
            num_cpus=2,
            memory="8Gi",
            image="rayproject/ray:2.54.0-py310",
            node_selector={"test": "worker"},
            labels={},
            tolerations=[],
            k8s_spec_override={
                "replicas": 2,
                "maxReplicas": 5,
            },
        ),
    ]

    kuberay_config = KubeRayConfig(
        namespace="test-namespace",
        head_group=head_group,
        worker_groups=worker_groups,
        config_method=K8sConfigMethod.LOCAL,
    )

    cluster = GenevaCluster(
        cluster_type=GenevaClusterType.KUBE_RAY,
        name="test-update",
        kuberay=kuberay_config,
    )

    # Create initial cluster
    geneva.define_cluster("test-update", cluster)
    loaded = geneva.list_clusters()[0]
    assert (
        loaded.kuberay.head_group.k8s_spec_override["template"]["spec"]["containers"][
            0
        ]["env"][0]["value"]
        == "v1"
    )
    assert loaded.kuberay.worker_groups[0].k8s_spec_override["maxReplicas"] == 5

    # Update k8s_spec_override
    head_group.k8s_spec_override = {
        "template": {
            "spec": {
                "containers": [
                    {
                        "env": [
                            {"name": "VERSION", "value": "v2"},
                            {"name": "NEW_VAR", "value": "new"},
                        ]
                    }
                ]
            }
        }
    }
    worker_groups[0].k8s_spec_override = {
        "replicas": 3,
        "maxReplicas": 10,
        "minReplicas": 1,
    }

    updated_cluster = GenevaCluster(
        cluster_type=GenevaClusterType.KUBE_RAY,
        name="test-update",
        kuberay=KubeRayConfig(
            namespace="test-namespace",
            head_group=head_group,
            worker_groups=worker_groups,
            config_method=K8sConfigMethod.LOCAL,
        ),
    )

    geneva.define_cluster("test-update", updated_cluster)
    loaded = geneva.list_clusters()[0]

    # Verify updates
    env_vars = loaded.kuberay.head_group.k8s_spec_override["template"]["spec"][
        "containers"
    ][0]["env"]
    assert len(env_vars) == 2
    assert env_vars[0]["value"] == "v2"
    assert env_vars[1]["name"] == "NEW_VAR"

    assert loaded.kuberay.worker_groups[0].k8s_spec_override == {
        "replicas": 3,
        "maxReplicas": 10,
        "minReplicas": 1,
    }

    # Clean up
    geneva.delete_cluster("test-update")


def test_cluster_extra_params_with_placeholder_node_selector(tmp_path: Path) -> None:
    """Test that placeholder node selectors work with k8s_spec_override"""
    geneva = connect(tmp_path)

    head_group = HeadGroupConfig(
        service_account="test-account",
        num_cpus=1,
        memory="4Gi",
        image="rayproject/ray:2.54.0-py310",
        node_selector={"_PLACEHOLDER": "true"},  # Use placeholder
        labels={},
        tolerations=[],
        k8s_spec_override={
            "template": {"spec": {"priorityClassName": "high-priority"}}
        },
    )

    worker_groups = [
        WorkerGroupConfig(
            service_account="test-account",
            num_cpus=2,
            memory="8Gi",
            image="rayproject/ray:2.54.0-py310",
            node_selector={"_PLACEHOLDER": "true"},  # Use placeholder
            labels={},
            tolerations=[],
            num_gpus=1,  # GPU worker
            k8s_spec_override={
                "replicas": 1,
                "maxReplicas": 3,
            },
        ),
    ]

    kuberay_config = KubeRayConfig(
        namespace="test-namespace",
        head_group=head_group,
        worker_groups=worker_groups,
        config_method=K8sConfigMethod.LOCAL,
    )

    cluster = GenevaCluster(
        cluster_type=GenevaClusterType.KUBE_RAY,
        name="test-placeholder",
        kuberay=kuberay_config,
    )

    geneva.define_cluster("test-placeholder", cluster)
    loaded_cluster = geneva.list_clusters()[0]

    # Convert to RayCluster - placeholder replaced, k8s_spec_override preserved
    ray_cluster = loaded_cluster.to_ray_cluster()

    # Verify head group got defaults and k8s_spec_override
    assert ray_cluster.head_group.node_selector == {
        "geneva.lancedb.com/ray-head": "true"
    }
    assert ray_cluster.head_group.k8s_spec_override is not None
    assert (
        ray_cluster.head_group.k8s_spec_override["template"]["spec"][
            "priorityClassName"
        ]
        == "high-priority"
    )

    # Verify worker got GPU node selector and k8s_spec_override
    worker = ray_cluster.worker_groups[0]
    assert worker.node_selector == {"geneva.lancedb.com/ray-worker-gpu": "true"}
    assert worker.k8s_spec_override is not None
    assert worker.k8s_spec_override["replicas"] == 1
    assert worker.k8s_spec_override["maxReplicas"] == 3

    # Clean up
    geneva.delete_cluster("test-placeholder")
