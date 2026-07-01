# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Literal, Required, TypedDict

from .._types import SequenceNotStr
from .application_agent_graph_input_param import ApplicationAgentGraphInputParam

__all__ = ["ApplicationAgentsServiceConfigurationParam"]


class ApplicationAgentsServiceConfigurationParam(TypedDict, total=False):
    params: Required[object]

    type: Required[Literal["WORKFLOW", "PLAN", "STATE_MACHINE"]]

    agent_service_errors: SequenceNotStr[str]
    """Errors that occurred when calling agent service"""

    graph: "AgentsServiceGraphDescriptorParam"
    """The graph of the agents service configuration"""

    inputs: Iterable[ApplicationAgentGraphInputParam]
    """The starting inputs that this agent configuration expects"""

    inputs_by_node: Dict[str, Iterable[ApplicationAgentGraphInputParam]]
    """The inputs that each node expects"""

    metadata: Dict[str, object]
    """User defined metadata about the application"""

    raw_configuration: str
    """Raw configuration entered by the user.

    May be invalid if variant is in draft mode.
    """


from .agents_service_graph_descriptor_param import AgentsServiceGraphDescriptorParam
