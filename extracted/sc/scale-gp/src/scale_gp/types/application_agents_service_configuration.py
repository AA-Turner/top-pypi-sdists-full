# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .application_agent_graph_input import ApplicationAgentGraphInput

__all__ = ["ApplicationAgentsServiceConfiguration"]


class ApplicationAgentsServiceConfiguration(BaseModel):
    params: object

    type: Literal["WORKFLOW", "PLAN", "STATE_MACHINE"]

    agent_service_errors: Optional[List[str]] = None
    """Errors that occurred when calling agent service"""

    graph: Optional["AgentsServiceGraphDescriptor"] = None
    """The graph of the agents service configuration"""

    inputs: Optional[List[ApplicationAgentGraphInput]] = None
    """The starting inputs that this agent configuration expects"""

    inputs_by_node: Optional[Dict[str, List[ApplicationAgentGraphInput]]] = None
    """The inputs that each node expects"""

    metadata: Optional[Dict[str, object]] = None
    """User defined metadata about the application"""

    raw_configuration: Optional[str] = None
    """Raw configuration entered by the user.

    May be invalid if variant is in draft mode.
    """


from .agents_service_graph_descriptor import AgentsServiceGraphDescriptor
