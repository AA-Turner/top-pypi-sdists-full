"""Tool binding layer for LangGraph nodes.

Provides a unified interface for LangGraph nodes to call existing agdt
Python functions (Jira, Git, Azure DevOps, file operations) directly —
without spawning *agdt* CLI entry points as subprocesses. Some built-in
tools (e.g. git root detection, pytest) still use ``subprocess`` internally
for the underlying operations they wrap.

Public API::

    from agentic_devtools.orchestration.tools import (
        ConcreteToolRegistry,
        ToolDefinition,
        ToolExecutor,
        ToolResult,
        tool_definition,
        validate_inputs,
    )
"""

from .decorators import auto_discover, tool_definition
from .definition import ToolDefinition
from .executor import ToolExecutor
from .registry import ConcreteToolRegistry
from .result import ToolResult
from .validation import validate_inputs

__all__ = [
    "ConcreteToolRegistry",
    "ToolDefinition",
    "ToolExecutor",
    "ToolResult",
    "auto_discover",
    "tool_definition",
    "validate_inputs",
]
