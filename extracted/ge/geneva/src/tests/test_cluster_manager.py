# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
from pathlib import Path

import pytest

from geneva import connect
from geneva.cluster import GenevaClusterType, K8sConfigMethod
from geneva.cluster.mgr import (
    GenevaCluster,
    HeadGroupConfig,
    KubeRayConfig,
    WorkerGroupConfig,
)
from geneva.constants import DEFAULT_K8S_NS


def test_define_and_list_cluster(tmp_path: Path) -> None:
    geneva = connect(tmp_path)

    tolerations = [
        {
            "key": "node.kubernetes.io/unreachable",
            "operator": "Exists",
            "effect": "NoExecute",
            "value": "1",
        },
        {
            "key": "node.kubernetes.io/disk-pressure",
            "operator": "Exists",
            "effect": "NoSchedule",
            "value": "2",
        },
    ]

    cluster_def = GenevaCluster(
        name="test",
        cluster_type=GenevaClusterType.KUBE_RAY,
        kuberay=KubeRayConfig(
            namespace=DEFAULT_K8S_NS,
            config_method=K8sConfigMethod.LOCAL,
            use_portforwarding=False,
            head_group=HeadGroupConfig(
                image="rayproject/ray:2.54.0-py312",
                service_account="test-service-account",
                num_cpus=2,
                memory="4Gi",
                node_selector={"foo": "bar"},
                labels={"foo": "bar", "baz": "fu"},
                tolerations=tolerations,
                num_gpus=0,
            ),
            worker_groups=[
                WorkerGroupConfig(
                    image="rayproject/ray:2.54.0-py312",
                    service_account="test-service-account",
                    num_cpus=2,
                    memory="4Gi",
                    node_selector={"foo": "bar"},
                    labels={"foo": "bar"},
                    tolerations=tolerations,
                    num_gpus=0,
                ),
                WorkerGroupConfig(
                    image="rayproject/ray:2.54.0-py312",
                    service_account="test-service-account",
                    num_cpus=2,
                    memory="4Gi",
                    node_selector={"foo": "bar"},
                    labels={"foo": "bar"},
                    tolerations=tolerations,
                    num_gpus=0,
                ),
            ],
        ),
    )

    # create
    geneva.define_cluster("test-cluster-1", cluster_def)
    c = geneva.list_clusters()[0]
    assert c.as_dict() == cluster_def.as_dict()
    assert c.kuberay.head_group.labels == {"foo": "bar", "baz": "fu"}

    # update
    cluster_def.kuberay.head_group.num_cpus = 3
    geneva.define_cluster("test-cluster-1", cluster_def)
    c = geneva.list_clusters()[0]
    assert c.as_dict() == cluster_def.as_dict()

    # delete
    geneva.delete_cluster("test-cluster-1")
    assert geneva.list_clusters() == []


def test_invalid_cluster_name_should_raise(tmp_path: Path) -> None:
    geneva = connect(tmp_path)

    name = "-this_name_doesnt_comply-with-rfc1123!@#"
    cluster_def = GenevaCluster(
        name=name,
        cluster_type=GenevaClusterType.KUBE_RAY,
        kuberay=KubeRayConfig(
            namespace=DEFAULT_K8S_NS,
            config_method=K8sConfigMethod.LOCAL,
            use_portforwarding=False,
            head_group=HeadGroupConfig(
                image="rayproject/ray:2.54.0-py312",
                service_account="test-service-account",
                num_cpus=2,
                memory="4Gi",
                node_selector={"foo": "bar"},
                labels={"foo": "bar", "baz": "fu"},
                tolerations=[],
                num_gpus=0,
            ),
            worker_groups=[
                WorkerGroupConfig(
                    image="rayproject/ray:2.54.0-py312",
                    service_account="test-service-account",
                    num_cpus=2,
                    memory="4Gi",
                    node_selector={"foo": "bar"},
                    labels={"foo": "bar"},
                    tolerations=[],
                    num_gpus=0,
                ),
            ],
        ),
    )
    geneva.define_cluster(name, cluster_def)

    with pytest.raises(
        ValueError,
        match="cluster name must comply with "
        "RFC 1123: lowercase letters, numbers, and "
        "hyphens only; must start and end with alphanumeric "
        f"character: {name}",
    ):
        geneva.context(cluster=name)


def test_context_not_found_should_raise(tmp_path: Path) -> None:
    geneva = connect(tmp_path)

    with pytest.raises(  # noqa: SIM117
        Exception,
        match="cluster definition 'i-dont-exist' not found. "
        "Create a new cluster with define_cluster()",
    ):
        with geneva.context(cluster="i-dont-exist", manifest={}):
            pass
