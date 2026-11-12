from typing import List, Optional

from anyscale._private.sdk import sdk_command
from anyscale.gpus.commands import _RESOURCE_ARG_DOCSTRINGS
from anyscale.node._private.node_sdk import DEFAULT_MAX_ITEMS, PrivateNodeSDK
from anyscale.node.models import Node, NodeList


_NODE_SDK_SINGLETON_KEY = "node_sdk"

_GET_EXAMPLE = """
import anyscale

node = anyscale.node.get("7aeb8674…", job_id="prodjob_abc123")
print(node.status, node.node_ip, node.instance_type)
print(node.resources, node.labels)
"""

_GET_ARG_DOCSTRINGS = {
    "node_id": "The Ray node ID (hex), as `anyscale node list` and the Nodes tab show it.",
    # The node's cluster: exactly one of these, the same four the GPU commands take.
    **_RESOURCE_ARG_DOCSTRINGS,
    "ray_session": "Name of the Ray session to read the node from. None means the newest "
    "of the cluster's recent sessions that has the node.",
}

_LIST_EXAMPLE = """
import anyscale

page = anyscale.node.list(service_id="service2_abc123", states=["ALIVE"], max_items=50)
print(f"{len(page.results)} of {page.total} nodes")
for node in page.results:
    print(node.node_id, node.name, node.status, node.instance_type)
"""

_LIST_ARG_DOCSTRINGS = {
    # The cluster whose nodes to list: exactly one of these, as for `get`.
    **_RESOURCE_ARG_DOCSTRINGS,
    "ray_session": "Name of a Ray session: only its nodes. None means the nodes of the "
    "cluster's recent sessions, newest session first.",
    "text_filter": "Case-insensitive substring to match in the node ID, name, IP, labels or "
    "resources. No regex.",
    "states": "Only nodes in these states: ALIVE, DEAD or PENDING (case-insensitive). None "
    "means every state.",
    "max_items": "How many nodes to return at most (default 10). `total` in the result says "
    "how many match.",
}


@sdk_command(
    _NODE_SDK_SINGLETON_KEY,
    PrivateNodeSDK,
    doc_py_example=_GET_EXAMPLE,
    arg_docstrings=_GET_ARG_DOCSTRINGS,
)
def get(  # noqa: PLR0913
    node_id: str,
    *,
    cluster_id: Optional[str] = None,
    workspace_id: Optional[str] = None,
    job_id: Optional[str] = None,
    service_id: Optional[str] = None,
    ray_session: Optional[str] = None,
    _private_sdk: Optional[PrivateNodeSDK] = None,
) -> Node:
    """Get one node of a cluster, workspace, job or service: state, IPs, instance type,
    resources and labels.

    Needs Ray 2.50.0 or newer; on an older version the node is not found.
    """
    return _private_sdk.get(  # type: ignore
        node_id,
        cluster_id=cluster_id,
        workspace_id=workspace_id,
        job_id=job_id,
        service_id=service_id,
        ray_session=ray_session,
    )


@sdk_command(
    _NODE_SDK_SINGLETON_KEY,
    PrivateNodeSDK,
    doc_py_example=_LIST_EXAMPLE,
    arg_docstrings=_LIST_ARG_DOCSTRINGS,
)
def list(  # noqa: A001, PLR0913
    *,
    cluster_id: Optional[str] = None,
    workspace_id: Optional[str] = None,
    job_id: Optional[str] = None,
    service_id: Optional[str] = None,
    ray_session: Optional[str] = None,
    text_filter: Optional[str] = None,
    states: Optional[List[str]] = None,
    max_items: int = DEFAULT_MAX_ITEMS,
    _private_sdk: Optional[PrivateNodeSDK] = None,
) -> NodeList:
    """List the nodes of a cluster, workspace, job or service, newest Ray session first,
    with optional filters.

    Needs Ray 2.50.0 or newer; on an older version the list is empty.
    """
    return _private_sdk.list(  # type: ignore
        cluster_id=cluster_id,
        workspace_id=workspace_id,
        job_id=job_id,
        service_id=service_id,
        ray_session=ray_session,
        text_filter=text_filter,
        states=states,
        max_items=max_items,
    )
