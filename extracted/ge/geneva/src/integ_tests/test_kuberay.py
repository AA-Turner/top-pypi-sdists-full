# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
import logging
import time

from geneva.cluster import K8sConfigMethod
from geneva.runners.kuberay.client import KuberayClients

_LOG = logging.getLogger(__name__)


def test_eks_token_expiry(
    k8s_config_method: K8sConfigMethod,
    k8s_namespace: str,
    region: str,
    k8s_cluster_name: str,
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        "geneva.eks.TOKEN_EXPIRATION_S",
        5,
    )
    try:
        clients = KuberayClients(
            k8s_config_method, region, k8s_cluster_name, "geneva-client-role"
        )
        for _ in range(10):
            clients.core_api.list_namespaced_pod(k8s_namespace)
            time.sleep(0.2)
    finally:
        monkeypatch.setattr(
            "geneva.eks.TOKEN_EXPIRATION_S",
            1800,
        )
