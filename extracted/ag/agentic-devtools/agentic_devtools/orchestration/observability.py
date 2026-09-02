"""Public observability API for LangGraph workflow execution.

This module is the canonical integration surface for new LangGraph node
code. All observability for LangGraph workflows flows exclusively through
this API — node implementations MUST NOT call ``execution/tracing.py`` or
``tools/audit.py`` directly.

Re-exports 19 public symbols covering event dataclasses (``NodeExecutionEvent``,
``LLMCallEvent``, ``ToolCallEvent``, ``ObservabilityEvent``), error classification
(``ErrorClassification``, ``ErrorClassifier``), pricing helpers
(``build_pricing_table``, ``lookup_call_cost``), redaction (``Redactor``),
summary formatting (``SummaryStats``, ``format_run_summary``,
``format_summary_stats``, ``print_run_summary``), truncation
(``truncate_summary``), the JSONL writer (``EventWriter``), and the workflow run
context manager with its three record helpers (``WorkflowRun``,
``record_node_execution``, ``record_llm_call``, ``record_tool_call``).

Usage::

    from agentic_devtools.orchestration.observability import (
        WorkflowRun,
        record_node_execution,
        record_llm_call,
        record_tool_call,
        print_run_summary,
    )

    with WorkflowRun(state_dir=get_state_dir()) as run:
        record_node_execution(run, node_name="fetch", ...)
        record_llm_call(run, node_name="analyze", ...)
        record_tool_call(run, node_name="commit", ...)
    # Summary is printed automatically on context exit.
"""

from agentic_devtools.orchestration.observability_errors import (
    ErrorClassification,
    ErrorClassifier,
)
from agentic_devtools.orchestration.observability_events import (
    LLMCallEvent,
    NodeExecutionEvent,
    ObservabilityEvent,
    ToolCallEvent,
)
from agentic_devtools.orchestration.observability_pricing import (
    build_pricing_table,
    lookup_call_cost,
)
from agentic_devtools.orchestration.observability_redactor import Redactor
from agentic_devtools.orchestration.observability_run import (
    WorkflowRun,
    record_llm_call,
    record_node_execution,
    record_tool_call,
)
from agentic_devtools.orchestration.observability_summary import (
    SummaryStats,
    format_run_summary,
    format_summary_stats,
    print_run_summary,
)
from agentic_devtools.orchestration.observability_truncation import truncate_summary
from agentic_devtools.orchestration.observability_writer import EventWriter

__all__ = [
    "ErrorClassification",
    "ErrorClassifier",
    "EventWriter",
    "LLMCallEvent",
    "NodeExecutionEvent",
    "ObservabilityEvent",
    "Redactor",
    "SummaryStats",
    "ToolCallEvent",
    "WorkflowRun",
    "build_pricing_table",
    "format_run_summary",
    "format_summary_stats",
    "lookup_call_cost",
    "print_run_summary",
    "record_llm_call",
    "record_node_execution",
    "record_tool_call",
    "truncate_summary",
]
