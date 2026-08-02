# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
import pytest
import yaml

try:
    from geneva.cluster import K8sConfigMethod
    from geneva.runners.ray.raycluster import (
        RayCluster,
        _HeadGroupSpec,
        _WorkerGroupSpec,
    )
except ImportError:
    pytest.skip("failed to import geneva.runners.ray", allow_module_level=True)

# Disable real k8s client init in attrs post_init for serialization tests
RayCluster.__attrs_post_init__ = lambda self: None


class DummyCM:
    def __init__(self, data: dict[str, str]) -> None:
        self.data = data


def test_from_config_map(monkeypatch) -> None:
    dummy_data = {
        "name": "my-ray-cluster",
        "head_group": yaml.dump(
            {
                "image": "ray:latest",
                "service_account": "sa-head",
                "num_cpus": 3,
                "num_gpus": 0,
                "memory": "8Gi",
                "node_selector": {"geneva.lancedb.com/ray-head": "true"},
            }
        ),
        "worker_groups": yaml.dump(
            [
                {
                    "image": "ray:latest",
                    "service_account": "sa-worker",
                    "num_cpus": 2,
                    "num_gpus": 1,
                    "memory": "16Gi",
                    "replicas": 2,
                    "min_replicas": 1,
                    "max_replicas": 5,
                    "idle_timeout_seconds": 30,
                    "node_selector": {"geneva.lancedb.com/ray-worker-cpu": "true"},
                }
            ]
        ),
    }
    cm = DummyCM(dummy_data)

    # Stub build_api_client to avoid real K8s calls
    monkeypatch.setattr(
        "geneva.runners.kuberay.client.build_api_client",
        lambda *args: None,
    )

    # Stub CoreV1Api to return our dummy ConfigMap
    class DummyCore:
        def read_namespaced_config_map(self, name: str, namespace: str) -> DummyCM:
            assert name == "cm-name"
            assert namespace == "my-namespace"
            return cm

    monkeypatch.setattr(
        "geneva.runners.ray.raycluster.kubernetes.client.CoreV1Api",
        lambda api_client=None: DummyCore(),
    )

    cluster = RayCluster.from_config_map(
        "my-namespace", "my-k8s-cluster", "cm-name", "my-ray-cluster"
    )
    assert isinstance(cluster, RayCluster)
    assert cluster.name == "my-ray-cluster"
    assert cluster.namespace == "my-namespace"
    assert isinstance(cluster.head_group, _HeadGroupSpec)
    # head_group fields
    hg = cluster.head_group
    assert hg.num_cpus == 3
    assert hg.num_gpus == 0
    assert hg.memory == 8 * 1024**3
    assert hg.node_selector == {"geneva.lancedb.com/ray-head": "true"}
    assert hg.service_account == "sa-head"
    # worker_groups fields
    assert isinstance(cluster.worker_groups, list)
    assert len(cluster.worker_groups) == 1
    wg = cluster.worker_groups[0]
    assert wg.num_cpus == 2
    assert wg.num_gpus == 1
    assert wg.memory == 16 * 1024**3
    assert wg.replicas == 2
    assert wg.min_replicas == 1
    assert wg.max_replicas == 5
    assert wg.idle_timeout_seconds == 30
    assert wg.node_selector == {"geneva.lancedb.com/ray-worker-cpu": "true"}
    assert wg.service_account == "sa-worker"
    assert cluster.config_method == K8sConfigMethod.LOCAL


def test_to_config_map(monkeypatch) -> None:
    # Create simple head and worker specs
    head = _HeadGroupSpec(
        image="img",
        service_account="sa-h",
        num_cpus=1,
        num_gpus=0,
        memory="4Gi",
        node_selector={"h": "v"},
    )
    w1 = _WorkerGroupSpec(
        image="img",
        service_account="sa-w1",
        num_cpus=2,
        num_gpus=1,
        memory="8Gi",
        replicas=1,
        min_replicas=0,
        max_replicas=3,
        idle_timeout_seconds=15,
        node_selector={"w1": "v1"},
    )
    w2 = _WorkerGroupSpec(
        image="img",
        service_account="sa-w2",
        num_cpus=3,
        num_gpus=0,
        memory="16Gi",
        replicas=2,
        min_replicas=1,
        max_replicas=4,
        idle_timeout_seconds=30,
        node_selector={"w2": "v2"},
    )

    cluster = RayCluster(name="c1", namespace="ns", head_group=head, worker_groups=[w1])
    data = cluster.to_config_map()
    assert data["name"] == "c1"
    h = yaml.safe_load(data["head_group"])
    assert h["image"] == head.image
    assert h["service_account"] == head.service_account
    assert h["num_cpus"] == head.num_cpus
    assert h["num_gpus"] == head.num_gpus
    assert h["memory"] == head.memory
    assert h["node_selector"] == head.node_selector
    ws1 = yaml.safe_load(data["worker_groups"])
    assert isinstance(ws1, list)
    assert len(ws1) == 1
    wdict = ws1[0]
    assert wdict["image"] == w1.image
    assert wdict["service_account"] == w1.service_account
    assert wdict["num_cpus"] == w1.num_cpus
    assert wdict["num_gpus"] == w1.num_gpus
    assert wdict["replicas"] == w1.replicas
    assert wdict["min_replicas"] == w1.min_replicas
    assert wdict["max_replicas"] == w1.max_replicas
    assert wdict["idle_timeout_seconds"] == w1.idle_timeout_seconds
    assert wdict["memory"] == w1.memory
    assert wdict["node_selector"] == w1.node_selector

    # Multiple worker groups
    cluster2 = RayCluster(
        name="c2", namespace="ns", head_group=head, worker_groups=[w1, w2]
    )
    data2 = cluster2.to_config_map()
    ws = yaml.safe_load(data2["worker_groups"])
    assert isinstance(ws, list)
    assert len(ws) == 2
    for idx, wspec in enumerate([w1, w2]):
        entry = ws[idx]
        assert entry["image"] == wspec.image
        assert entry["service_account"] == wspec.service_account
        assert entry["num_cpus"] == wspec.num_cpus
        assert entry["num_gpus"] == wspec.num_gpus
        assert entry["replicas"] == wspec.replicas
        assert entry["min_replicas"] == wspec.min_replicas
        assert entry["max_replicas"] == wspec.max_replicas
        assert entry["idle_timeout_seconds"] == wspec.idle_timeout_seconds
        assert entry["memory"] == wspec.memory
        assert entry["node_selector"] == wspec.node_selector
    assert "worker_group" not in data2


def test_config_map_round_trip(monkeypatch) -> None:
    head = _HeadGroupSpec(
        image="i",
        service_account="sa-h",
        num_cpus=1,
        num_gpus=0,
        memory="2Gi",
        node_selector={"nh": "nv"},
    )
    w = _WorkerGroupSpec(
        image="i",
        service_account="sa-w",
        num_cpus=2,
        num_gpus=1,
        memory="4Gi",
        replicas=1,
        min_replicas=0,
        max_replicas=2,
        idle_timeout_seconds=20,
        node_selector={"wn": "wv"},
    )
    orig = RayCluster(
        name="orig",
        namespace="ns",
        head_group=head,
        worker_groups=[w],
        config_method=K8sConfigMethod.LOCAL,
        region="rgn",
        role_name="roleX",
    )
    data = orig.to_config_map()
    cm = DummyCM(data)

    # Stub K8s client to return our dummy ConfigMap
    monkeypatch.setattr(
        "geneva.runners.kuberay.client.build_api_client",
        lambda *args: None,
    )

    class DummyCoreRT:
        def read_namespaced_config_map(self, name: str, namespace: str) -> DummyCM:
            return cm

    monkeypatch.setattr(
        "geneva.runners.ray.raycluster.kubernetes.client.CoreV1Api",
        lambda api_client=None: DummyCoreRT(),
    )

    loaded = RayCluster.from_config_map(
        orig.namespace,
        "my-k8s-cluster",
        "cm-name",
        orig.name,
        config_method=orig.config_method,
        aws_region=orig.region,
        aws_role_name=orig.role_name,
    )
    assert loaded.name == orig.name
    assert loaded.namespace == orig.namespace
    assert loaded.config_method == orig.config_method
    assert loaded.region == orig.region
    assert loaded.role_name == orig.role_name
    # Check head_group resources and selector
    assert loaded.head_group.num_cpus == orig.head_group.num_cpus
    assert loaded.head_group.num_gpus == orig.head_group.num_gpus
    assert loaded.head_group.memory == orig.head_group.memory
    assert loaded.head_group.node_selector == orig.head_group.node_selector
    assert loaded.head_group.service_account == orig.head_group.service_account
    # Check worker_groups resources and selectors
    assert len(loaded.worker_groups) == len(orig.worker_groups)
    lw = loaded.worker_groups[0]
    ow = orig.worker_groups[0]
    assert lw.num_cpus == ow.num_cpus
    assert lw.num_gpus == ow.num_gpus
    assert lw.memory == ow.memory
    assert lw.replicas == ow.replicas
    assert lw.min_replicas == ow.min_replicas
    assert lw.max_replicas == ow.max_replicas
    assert lw.idle_timeout_seconds == ow.idle_timeout_seconds
    assert lw.node_selector == ow.node_selector
    assert lw.service_account == ow.service_account
