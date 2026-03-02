"""Agent module for LLM-powered graph exploration.

This module provides tools and infrastructure for LLM agents to explore
and understand code graphs.

Imports are lazy to allow submodules (like subagent) to be imported
without requiring all dependencies (like kuzu).
"""


def __getattr__(name: str):
    """Lazy import to avoid loading kuzu when not needed."""
    if name == "AgentToolkit":
        from .toolkit import AgentToolkit
        return AgentToolkit
    elif name == "AgentSession":
        from .session import AgentSession
        return AgentSession
    elif name == "AgentRunner":
        from .runner import AgentRunner
        return AgentRunner
    elif name == "SafeJSONEncoder":
        from .runner import SafeJSONEncoder
        return SafeJSONEncoder
    elif name == "ToolResult":
        from .tools.base import ToolResult
        return ToolResult
    elif name == "ToolCategory":
        from .tools.base import ToolCategory
        return ToolCategory
    elif name == "OpenAgent":
        from .open import OpenAgent
        return OpenAgent
    elif name == "AgentFactory":
        from .factory import AgentFactory
        return AgentFactory
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "AgentToolkit",
    "AgentSession",
    "AgentRunner",
    "SafeJSONEncoder",
    "ToolResult",
    "ToolCategory",
    "OpenAgent",
    "AgentFactory",
]
