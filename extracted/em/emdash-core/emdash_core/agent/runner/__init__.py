"""Agent runner module for LLM-powered exploration.

This module provides the AgentRunner class and related utilities for running
LLM agents with tool access for code exploration.

The module is organized as follows:
- agent_runner.py: Main AgentRunner class
- context.py: Context estimation, compaction, and management
- plan.py: Plan approval/rejection functionality
- utils.py: JSON encoding and utility functions
"""

from .agent_runner import AgentRunner
from .factory import get_runner, create_hybrid_runner
from .utils import SafeJSONEncoder, summarize_tool_result
from .context import (
    estimate_context_tokens,
    get_context_breakdown,
    maybe_compact_context,
    compact_messages_with_llm,
    format_messages_for_summary,
    get_reranked_context,
    emit_context_frame,
)
from .plan import PlanMixin

__all__ = [
    # Main classes
    "AgentRunner",
    # Factory functions
    "get_runner",
    "create_hybrid_runner",
    # Utils
    "SafeJSONEncoder",
    "summarize_tool_result",
    # Context functions
    "estimate_context_tokens",
    "get_context_breakdown",
    "maybe_compact_context",
    "compact_messages_with_llm",
    "format_messages_for_summary",
    "get_reranked_context",
    "emit_context_frame",
    # Plan management
    "PlanMixin",
]
