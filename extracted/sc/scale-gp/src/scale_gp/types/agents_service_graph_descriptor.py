# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

from .._models import BaseModel
from .application_agent_graph_edge import ApplicationAgentGraphEdge

__all__ = ["AgentsServiceGraphDescriptor"]


class AgentsServiceGraphDescriptor(BaseModel):
    edges: List[ApplicationAgentGraphEdge]

    nodes: List["ApplicationAgentGraphNode"]


from .application_agent_graph_node import ApplicationAgentGraphNode
