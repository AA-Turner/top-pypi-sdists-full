"""LangGraph control-flow signal detection.

LangGraph raises a few exception classes to move execution between graph
boundaries or pause for human input. They are not runtime failures and should
not be emitted as error spans.
"""

from __future__ import annotations

from typing import Any

_CONTROL_FLOW_NAMES = frozenset({"GraphInterrupt", "ParentCommand"})


def is_control_flow_signal(error: BaseException | None) -> bool:
    """Return True for LangGraph non-failure control-flow exceptions."""
    if error is None:
        return False
    if is_control_flow_error_type(type(error).__name__):
        return True
    return _is_langgraph_control_flow_instance(error)


def is_control_flow_error_type(error_type: Any) -> bool:
    """Return True when an error_type field names a LangGraph control signal."""
    return isinstance(error_type, str) and error_type in _CONTROL_FLOW_NAMES


def _is_langgraph_control_flow_instance(error: BaseException) -> bool:
    try:
        from langgraph.errors import GraphInterrupt, ParentCommand
    except ImportError:
        return False
    return isinstance(error, (GraphInterrupt, ParentCommand))
