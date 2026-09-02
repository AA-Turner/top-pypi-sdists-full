"""Execution state schema for LangGraph node input/output contracts.

Carries only JSON-serialisable workflow data so node updates remain safe
to merge into graph state.
"""

from typing import TypedDict

from .types import JSONValue

NodeUpdateAlias = dict[str, JSONValue]
"""Convenience alias for the dict a node callable returns."""


class ExecutionState(TypedDict, total=False):
    """LangGraph node input/output state contract for ``execution/`` nodes.

    All fields are optional (``total=False``) because LangGraph uses
    last-writer-wins merging and nodes only return the keys they update.
    """

    status: str
    error: str | None
    retry_count: int
