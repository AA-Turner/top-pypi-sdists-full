from datetime import datetime, timezone
from typing import List, Optional

from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale._private.workload.cluster_id import resolve_cluster_id
from anyscale.client.openapi_client.models import ClusterDashboardNode
from anyscale.node.models import Node, NodeList, NodeStatus


# The backend's own page size when none is sent.
DEFAULT_MAX_ITEMS = 10


class PrivateNodeSDK(BaseSDK):
    def get(  # noqa: PLR0913
        self,
        node_id: str,
        *,
        cluster_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        job_id: Optional[str] = None,
        service_id: Optional[str] = None,
        ray_session: Optional[str] = None,
    ) -> Node:
        """One node by Ray node id.

        The node's cluster is named by exactly one of the four IDs; see resolve_cluster_id.
        With no `ray_session` the backend looks through the cluster's recent Ray
        sessions, newest first, and returns the first one that has the node.
        """
        resolved = resolve_cluster_id(
            self.client,
            cluster_id=cluster_id,
            workspace_id=workspace_id,
            job_id=job_id,
            service_id=service_id,
        )
        raw = self.client.get_cluster_node(
            cluster_id=resolved, node_id=node_id, session_name=ray_session
        )
        return _to_node(raw)

    def list(  # noqa: A003, PLR0913
        self,
        *,
        cluster_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        job_id: Optional[str] = None,
        service_id: Optional[str] = None,
        ray_session: Optional[str] = None,
        text_filter: Optional[str] = None,
        states: Optional[List[str]] = None,
        max_items: int = DEFAULT_MAX_ITEMS,
    ) -> NodeList:
        """The first `max_items` nodes of the cluster matching the filters, plus the total.

        The cluster is named by exactly one of the four IDs; see resolve_cluster_id. Then
        one request: the backend filters and sorts the whole list (newest Ray session
        first, head node first, alive first) and returns the first page.
        """
        if isinstance(max_items, bool) or not isinstance(max_items, int) or max_items < 1:
            raise ValueError("max_items must be a positive int.")
        resolved = resolve_cluster_id(
            self.client,
            cluster_id=cluster_id,
            workspace_id=workspace_id,
            job_id=job_id,
            service_id=service_id,
        )
        raw = self.client.list_cluster_nodes(
            cluster_id=resolved,
            session_name=ray_session,
            text_filter=text_filter,
            states_filter=[NodeStatus.validate(state).value for state in states]
            if states
            else None,
            page=1,
            page_size=max_items,
        )
        results = [_to_node(node) for node in raw.results or []]
        total = (
            raw.metadata.total if raw.metadata and raw.metadata.total is not None else len(results)
        )
        return NodeList(results=results, total=total)


def _to_node(raw: ClusterDashboardNode) -> Node:
    return Node(
        node_id=raw.node_id,
        node_ip=raw.node_ip,
        name=raw.name,
        status=NodeStatus.validate(str(raw.status)),
        is_head_node=bool(raw.is_head_node),
        resources=dict(raw.resources or {}),
        labels=dict(raw.labels or {}),
        instance_type=raw.instance_type,
        start_time=_from_epoch_ms(raw.start_time_ms),
        end_time=_from_epoch_ms(raw.end_time_ms),
        ray_session_name=raw.ray_session_name,
    )


def _from_epoch_ms(value: Optional[int]) -> Optional[datetime]:
    # The API sends epoch milliseconds; the model carries a UTC datetime, like every
    # other SDK model (the GPU models do the same with epoch seconds).
    if value is None:
        return None
    return datetime.fromtimestamp(value / 1000, tz=timezone.utc)
