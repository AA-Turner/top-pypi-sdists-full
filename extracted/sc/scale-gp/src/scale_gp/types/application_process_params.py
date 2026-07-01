# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr
from .application_edge_param import ApplicationEdgeParam
from .application_node_param import ApplicationNodeParam
from .shared_params.agentic_application_overrides import AgenticApplicationOverrides

__all__ = ["ApplicationProcessParams", "History", "Overrides", "OverridesUnionMember1OverridesUnionMember1Item"]


class ApplicationProcessParams(TypedDict, total=False):
    edges: Required[Iterable[ApplicationEdgeParam]]
    """List of edges in the application graph"""

    inputs: Required[Dict[str, Dict[str, object]]]
    """Input data for the application. You must provide inputs for each input node"""

    nodes: Required[Iterable[ApplicationNodeParam]]
    """List of nodes in the application graph"""

    version: Required[Literal["V0"]]
    """Version of the application schema"""

    history: Iterable[History]
    """History of the application"""

    operation_metadata: Dict[str, object]
    """
    Arbitrary user-defined metadata that can be attached to the process operations
    and will be registered in the interaction.
    """

    overrides: Overrides
    """Optional overrides for the application"""

    stream: bool
    """Control to have streaming of the endpoint.

    If the last node before the output is a completion node, you can set this to
    true to get the output as soon as the completion node has a token
    """


class History(TypedDict, total=False):
    request: Required[str]
    """Request inputs"""

    response: Required[str]
    """Response outputs"""

    session_data: Dict[str, object]
    """Session data corresponding to the request response pair"""


class OverridesUnionMember1OverridesUnionMember1Item(TypedDict, total=False):
    artifact_ids_filter: SequenceNotStr[str]

    artifact_name_regex: SequenceNotStr[str]

    type: Literal["knowledge_base_schema"]


Overrides: TypeAlias = Union[AgenticApplicationOverrides, Dict[str, OverridesUnionMember1OverridesUnionMember1Item]]
