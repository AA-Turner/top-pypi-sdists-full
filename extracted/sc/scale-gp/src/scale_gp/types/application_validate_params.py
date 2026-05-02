# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr
from .application_edge_param import ApplicationEdgeParam
from .application_node_param import ApplicationNodeParam
from .shared_params.agentic_application_overrides import AgenticApplicationOverrides

__all__ = ["ApplicationValidateParams", "Overrides", "OverridesUnionMember1OverridesUnionMember1Item"]


class ApplicationValidateParams(TypedDict, total=False):
    edges: Required[Iterable[ApplicationEdgeParam]]
    """List of edges in the application graph"""

    nodes: Required[Iterable[ApplicationNodeParam]]
    """List of nodes in the application graph"""

    version: Required[Literal["V0"]]
    """Version of the application schema"""

    overrides: Overrides
    """Optional overrides for the application"""


class OverridesUnionMember1OverridesUnionMember1Item(TypedDict, total=False):
    artifact_ids_filter: SequenceNotStr[str]

    artifact_name_regex: SequenceNotStr[str]

    type: Literal["knowledge_base_schema"]


Overrides: TypeAlias = Union[AgenticApplicationOverrides, Dict[str, OverridesUnionMember1OverridesUnionMember1Item]]
