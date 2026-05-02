# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Required, TypedDict

from .application_edge_param import ApplicationEdgeParam
from .application_node_param import ApplicationNodeParam

__all__ = ["ApplicationConfigurationParam"]


class ApplicationConfigurationParam(TypedDict, total=False):
    edges: Required[Iterable[ApplicationEdgeParam]]

    nodes: Required[Iterable[ApplicationNodeParam]]

    metadata: Dict[str, object]
    """User defined metadata about the application"""
