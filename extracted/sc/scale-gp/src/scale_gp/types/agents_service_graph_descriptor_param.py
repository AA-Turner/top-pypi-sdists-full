# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from .application_agent_graph_edge_param import ApplicationAgentGraphEdgeParam

__all__ = ["AgentsServiceGraphDescriptorParam"]


class AgentsServiceGraphDescriptorParam(TypedDict, total=False):
    edges: Required[Iterable[ApplicationAgentGraphEdgeParam]]

    nodes: Required[Iterable["ApplicationAgentGraphNodeParam"]]


from .application_agent_graph_node_param import ApplicationAgentGraphNodeParam
