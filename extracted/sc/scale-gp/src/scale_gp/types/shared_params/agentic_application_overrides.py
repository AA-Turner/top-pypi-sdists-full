# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Required, TypedDict

__all__ = ["AgenticApplicationOverrides", "InitialState", "PartialTrace"]


class InitialState(TypedDict, total=False):
    current_node: Required[str]

    state: Required[Dict[str, object]]


class PartialTrace(TypedDict, total=False):
    duration_ms: Required[int]

    node_id: Required[str]

    operation_input: Required[str]

    operation_output: Required[str]

    operation_type: Required[str]

    start_timestamp: Required[str]

    workflow_id: Required[str]

    operation_metadata: Dict[str, object]


class AgenticApplicationOverrides(TypedDict, total=False):
    """Execution override options for agentic applications"""

    concurrent: bool

    initial_state: InitialState

    partial_trace: Iterable[PartialTrace]

    return_span: bool

    use_channels: bool
