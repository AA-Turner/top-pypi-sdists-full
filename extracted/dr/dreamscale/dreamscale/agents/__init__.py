"""Managed LLM robot runs with local safety, measured receipts and durable journals.

Use run_yam for a configured YAM, or run/arun with your own RobotAdapter.
Action-chunk policy inference remains available through dreamscale.connect.
"""

from dreamscale_transport.llm import (
    Effort,
    Observation,
    RobotProfile,
    Speed,
    ToolCall,
    ToolReceipt,
    ToolSpec,
    TurnResult,
)

from .api import RunResult, arun, run, run_yam
from .runner import ExecutionInterrupted, RobotAdapter

__all__ = [
    "Effort",
    "ExecutionInterrupted",
    "Observation",
    "RobotAdapter",
    "RobotProfile",
    "RunResult",
    "Speed",
    "ToolCall",
    "ToolReceipt",
    "ToolSpec",
    "TurnResult",
    "arun",
    "run",
    "run_yam",
]
