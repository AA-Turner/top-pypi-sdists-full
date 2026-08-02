# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import pytest

from geneva.cluster import K8sConfigMethod
from geneva.constants import DEFAULT_K8S_NS
from geneva.runners.ray.raycluster import RayCluster, _HeadGroupSpec, _WorkerGroupSpec


def test_service_account_does_not_exist(
    k8s_config_method: K8sConfigMethod,
    head_node_selector: dict,
    worker_node_selector: dict,
) -> None:
    cluster = RayCluster(
        name="not-used",
        namespace=DEFAULT_K8S_NS,
        config_method=k8s_config_method,
        # allocate at least a single worker so the test runs faster
        # that we save time on waiting for the actor to start
        head_group=_HeadGroupSpec(node_selector=head_node_selector),  # type: ignore[call-arg]
        worker_groups=[
            _WorkerGroupSpec(  # type: ignore[call-arg]
                name="worker",
                min_replicas=1,
                service_account="does-not-exist",
                node_selector=worker_node_selector,
            )
        ],
    )
    with pytest.raises(
        ValueError, match="Service account does-not-exist does not exist"
    ):
        cluster._validate()


@pytest.mark.skip("requires RBAC permissions beyond what we require for Geneva users")
def test_service_account_not_enough_permission(
    k8s_temp_service_account: str,
    k8s_config_method: K8sConfigMethod,
    head_node_selector: dict,
    worker_node_selector: dict,
) -> None:
    # with strict access review, we should get an error about lack of permission
    cluster = RayCluster(
        name="not-used",
        namespace=DEFAULT_K8S_NS,
        config_method=k8s_config_method,
        # allocate at least a single worker so the test runs faster
        # that we save time on waiting for the actor to start
        head_group=_HeadGroupSpec(node_selector=head_node_selector),  # type: ignore[call-arg]
        worker_groups=[
            _WorkerGroupSpec(  # type: ignore[call-arg]
                name="worker",
                min_replicas=1,
                service_account=k8s_temp_service_account,
                node_selector=worker_node_selector,
            )
        ],
        strict_access_review=True,
    )
    with pytest.raises(
        ValueError,
        match=f"Service account {k8s_temp_service_account} does not"
        " have the required permission:",
    ):
        cluster._validate()

    # with strict access review disabled, we should still get the same
    # error because we have permission to create local subject access
    # review and the service account does not have enough permission
    cluster = RayCluster(
        name="not-used",
        namespace=DEFAULT_K8S_NS,
        config_method=k8s_config_method,
        # allocate at least a single worker so the test runs faster
        # that we save time on waiting for the actor to start
        head_group=_HeadGroupSpec(node_selector=head_node_selector),  # type: ignore[call-arg]
        worker_groups=[
            _WorkerGroupSpec(  # type: ignore[call-arg]
                name="worker",
                min_replicas=1,
                service_account=k8s_temp_service_account,
                node_selector=worker_node_selector,
            )
        ],
        strict_access_review=False,
    )
    with pytest.raises(
        ValueError,
        match=f"Service account {k8s_temp_service_account} does not"
        " have the required permission:",
    ):
        cluster._validate()


def test_service_account_is_valid(
    geneva_k8s_service_account: str,
    k8s_config_method: K8sConfigMethod,
    head_node_selector: dict,
    worker_node_selector: dict,
) -> None:
    cluster = RayCluster(
        name="not-used",
        namespace=DEFAULT_K8S_NS,
        config_method=k8s_config_method,
        # allocate at least a single worker so the test runs faster
        # that we save time on waiting for the actor to start
        head_group=_HeadGroupSpec(node_selector=head_node_selector),  # type: ignore[call-arg]
        worker_groups=[
            _WorkerGroupSpec(  # type: ignore[call-arg]
                name="worker",
                min_replicas=1,
                service_account=geneva_k8s_service_account,
                node_selector=worker_node_selector,
            )
        ],
    )
    cluster._validate()
