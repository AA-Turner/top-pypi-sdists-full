"""Backward-compatibility re-exports from matrx_connect.context.app_context."""

from matrx_connect.context.app_context import (
    AppContext,
    child_agent_context,
    clear_app_context,
    get_app_context,
    set_app_context,
    try_get_app_context,
)

__all__ = [
    "AppContext",
    "child_agent_context",
    "clear_app_context",
    "get_app_context",
    "set_app_context",
    "try_get_app_context",
]
