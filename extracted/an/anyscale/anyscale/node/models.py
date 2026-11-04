"""Models for `anyscale node get` and `anyscale.node.*`.

A node record comes from the cluster dashboard: the Ray node lifecycle events the
control plane ingests for a cluster, so a node that is already dead still resolves.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar, Dict, List, Optional

from anyscale._private.models import ModelBase, ModelEnum


class NodeStatus(ModelEnum):
    """The lifecycle state of a node, as Ray last reported it."""

    ALIVE = "ALIVE"
    DEAD = "DEAD"
    PENDING = "PENDING"

    __docstrings__: ClassVar[Dict[str, str]] = {
        ALIVE: "The node is up and part of the Ray cluster.",
        DEAD: "The node left the Ray cluster: terminated, preempted or failed.",
        PENDING: "The node is being provisioned and has not joined the Ray cluster yet.",
    }


@dataclass(frozen=True)
class Node(ModelBase):
    """One node of a cluster, as the cluster dashboard reports it."""

    __doc_py_example__ = """\
import anyscale

node = anyscale.node.get(cluster_id="ses_abc123", node_id="7aeb8674…")
print(node.status, node.node_ip, node.instance_type, node.resources)
"""

    node_id: str = field(metadata={"docstring": "The Ray node ID (hex)."})
    node_ip: str = field(metadata={"docstring": "IP of the node."})
    name: str = field(metadata={"docstring": "Display name of the node, e.g. head-node."})
    status: NodeStatus = field(metadata={"docstring": "Lifecycle state; see NodeStatus."})
    is_head_node: bool = field(metadata={"docstring": "Whether this is the head node."})
    resources: Dict[str, float] = field(
        default_factory=dict,
        metadata={"docstring": 'Ray resources of the node, e.g. {"CPU": 8, "GPU": 1}.'},
    )
    labels: Dict[str, str] = field(
        default_factory=dict, metadata={"docstring": "Ray node labels."}
    )
    instance_type: Optional[str] = field(
        default=None, metadata={"docstring": "Cloud instance type of the node."}
    )
    start_time: Optional[datetime] = field(
        default=None,
        metadata={
            "docstring": "When the node started, as a timezone-aware UTC datetime. The API "
            "sends this as epoch milliseconds (start_time_ms)."
        },
    )
    end_time: Optional[datetime] = field(
        default=None,
        metadata={
            "docstring": "When the node died, as a timezone-aware UTC datetime; None while "
            "it is alive. The API sends this as epoch milliseconds (end_time_ms)."
        },
    )
    ray_session_name: Optional[str] = field(
        default=None, metadata={"docstring": "The Ray session the node belongs to."}
    )

    def _validate_node_id(self, node_id: str):
        if not isinstance(node_id, str) or not node_id:
            raise ValueError("node_id must be a non-empty string.")

    def _validate_node_ip(self, node_ip: str):
        if not isinstance(node_ip, str):
            raise TypeError("node_ip must be a string.")

    def _validate_name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("name must be a string.")

    def _validate_status(self, status: NodeStatus) -> NodeStatus:
        return NodeStatus.validate(status)

    def _validate_is_head_node(self, is_head_node: bool):
        if not isinstance(is_head_node, bool):
            raise TypeError("is_head_node must be a bool.")

    def _validate_resources(self, resources: Dict[str, float]):
        if not isinstance(resources, dict) or not all(
            isinstance(key, str)
            and isinstance(value, (int, float))
            and not isinstance(value, bool)
            for key, value in resources.items()
        ):
            raise TypeError("resources must be a dict of str to number.")

    def _validate_labels(self, labels: Dict[str, str]):
        if not isinstance(labels, dict) or not all(
            isinstance(key, str) and isinstance(value, str) for key, value in labels.items()
        ):
            raise TypeError("labels must be a dict of str to str.")

    def _validate_instance_type(self, instance_type: Optional[str]):
        if instance_type is not None and not isinstance(instance_type, str):
            raise TypeError("instance_type must be a string or None.")

    def _validate_start_time(self, start_time: Optional[datetime]):
        if start_time is not None and not isinstance(start_time, datetime):
            raise TypeError("start_time must be a datetime or None.")

    def _validate_end_time(self, end_time: Optional[datetime]):
        if end_time is not None and not isinstance(end_time, datetime):
            raise TypeError("end_time must be a datetime or None.")

    def _validate_ray_session_name(self, ray_session_name: Optional[str]):
        if ray_session_name is not None and not isinstance(ray_session_name, str):
            raise TypeError("ray_session_name must be a string or None.")


@dataclass(frozen=True)
class NodeList(ModelBase):
    """One page of a cluster's nodes, and how many nodes match in total."""

    __doc_py_example__ = """\
import anyscale

page = anyscale.node.list(cluster_id="ses_abc123", states=["DEAD"], max_items=50)
print(f"{len(page.results)} of {page.total}")
for node in page.results:
    print(node.node_id, node.status, node.end_time)
"""

    results: List[Node] = field(
        metadata={"docstring": "The nodes, newest Ray session first; see Node."}
    )
    total: int = field(
        metadata={
            "docstring": "How many nodes match the filters, which can be more than "
            "len(results) when max_items cut the list short."
        }
    )

    def _validate_results(self, results: List[Node]):
        if not isinstance(results, list) or not all(isinstance(node, Node) for node in results):
            raise TypeError("results must be a list of Node.")

    def _validate_total(self, total: int):
        if isinstance(total, bool) or not isinstance(total, int) or total < 0:
            raise ValueError("total must be a non-negative int.")
