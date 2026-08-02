"""Enumerate EKS clusters and their managed node groups via the ``aws eks`` CLI."""

from dataclasses import dataclass, field

from .awscli import run_aws_json
from .spot_evictions import cluster_to_env


@dataclass
class NodeGroup:
    """A managed node group's authoritative config, from ``describe-nodegroup``."""

    cluster: str
    name: str
    capacity_type: str  # "SPOT" | "ON_DEMAND"
    instance_types: list[str] = field(default_factory=list)
    desired: int = 0
    ami_type: str = ""

    @property
    def env(self) -> str:
        return cluster_to_env(self.cluster)

    @property
    def is_spot(self) -> bool:
        return self.capacity_type.upper() == "SPOT"


def list_clusters(region: str, *, profile: str = "") -> list[str]:
    """Return the names of all EKS clusters in ``region``."""
    payload = run_aws_json(["eks", "list-clusters", "--region", region], profile=profile)
    clusters: list[str] = payload.get("clusters", [])
    return clusters


def list_nodegroups(region: str, cluster: str, *, profile: str = "") -> list[str]:
    """Return the managed node group names of ``cluster``."""
    payload = run_aws_json(
        ["eks", "list-nodegroups", "--region", region, "--cluster-name", cluster],
        profile=profile,
    )
    names: list[str] = payload.get("nodegroups", [])
    return names


def describe_nodegroup(region: str, cluster: str, name: str, *, profile: str = "") -> NodeGroup:
    """Return the config of one managed node group."""
    payload = run_aws_json(
        ["eks", "describe-nodegroup", "--region", region, "--cluster-name", cluster, "--nodegroup-name", name],
        profile=profile,
    )
    ng = payload.get("nodegroup", {})
    scaling = ng.get("scalingConfig") or {}
    return NodeGroup(
        cluster=cluster,
        name=name,
        capacity_type=ng.get("capacityType", "") or "",
        instance_types=list(ng.get("instanceTypes") or []),
        desired=int(scaling.get("desiredSize", 0) or 0),
        ami_type=ng.get("amiType", "") or "",
    )


def discover_nodegroups(region: str, *, profile: str = "") -> list[NodeGroup]:
    """Enumerate every managed node group across every cluster in ``region``."""
    out: list[NodeGroup] = []
    for cluster in list_clusters(region, profile=profile):
        for name in list_nodegroups(region, cluster, profile=profile):
            out.append(describe_nodegroup(region, cluster, name, profile=profile))
    return out
