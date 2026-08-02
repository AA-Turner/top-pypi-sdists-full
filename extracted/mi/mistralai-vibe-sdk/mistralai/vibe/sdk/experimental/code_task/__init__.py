"""Experimental package for code-task capability primitives.

The code-task subsystem lets sandboxed Python code request host tools, replay
previous tool outcomes, and pause execution while unresolved tool calls wait for
a client or orchestrator response. This package holds the current implementation
while the API remains experimental.
"""

from .handler import ToolCallHandler, ToolRejectedError
from .orchestrator import orchestrate
from .sandbox import run_python_code
from .types import (
    CodeResult,
    FunctionDef,
    PartialEvaluation,
    PendingTool,
    RejectedTool,
    ResolvedTool,
    RunCodeResult,
    ToolCallFunction,
    ToolDefinition,
    ToolState,
)

__all__ = [
    "CodeResult",
    "FunctionDef",
    "PartialEvaluation",
    "PendingTool",
    "RejectedTool",
    "ResolvedTool",
    "RunCodeResult",
    "ToolCallFunction",
    "ToolCallHandler",
    "ToolDefinition",
    "ToolRejectedError",
    "ToolState",
    "orchestrate",
    "run_python_code",
]
