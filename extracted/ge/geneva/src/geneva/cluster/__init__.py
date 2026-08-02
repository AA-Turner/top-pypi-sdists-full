# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from geneva.cluster.mgr import GenevaCluster


class GenevaClusterType(Enum):
    """Type of Geneva Cluster"""

    KUBE_RAY = "KUBE_RAY"
    LOCAL_RAY = "LOCAL_RAY"
    EXTERNAL_RAY = "EXTERNAL_RAY"


class K8sConfigMethod(Enum):
    """Method for retrieving kubernetes config:

    - LOCAL: Load the kube config from the local environment.
    - EKS_AUTH: Load the kube config from AWS EKS service (requires AWS credentials).
    - IN_CLUSTER: Load the kube config when running inside a pod in the cluster.
    """

    EKS_AUTH = "EKS_AUTH"
    IN_CLUSTER = "IN_CLUSTER"
    LOCAL = "LOCAL"


def __getattr__(name: str) -> type[Any]:
    """Lazy import GenevaCluster to avoid circular imports.

    Allows: from geneva.cluster import GenevaCluster
    """
    if name == "GenevaCluster":
        from geneva.cluster.mgr import GenevaCluster

        return GenevaCluster
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["GenevaClusterType", "K8sConfigMethod", "GenevaCluster"]
