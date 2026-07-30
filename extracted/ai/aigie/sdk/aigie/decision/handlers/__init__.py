"""Per-verb handlers for RemediationStep dispatch.

Each handler module owns its verb(s) — dispatch logic plus the advertised
``VerbSpec`` (name, description, param_schema) — as a ``BINDINGS`` list. This
package aggregates them into ``DEFAULT_BINDINGS``, the single source of truth the
executor wires into its registry + advertised capabilities.
"""

from __future__ import annotations

from aigie.decision.handlers.correct_tool_call import BINDINGS as _correct_tool_call_bindings
from aigie.decision.handlers.correct_tool_call import CorrectToolCallHandler
from aigie.decision.handlers.no_op import BINDINGS as _no_op_bindings
from aigie.decision.handlers.no_op import NoOpHandler
from aigie.decision.handlers.prompt import BINDINGS as _prompt_bindings
from aigie.decision.handlers.prompt import PromptHandler
from aigie.decision.handlers.reduce_context import BINDINGS as _reduce_context_bindings
from aigie.decision.handlers.reduce_context import ReduceContextHandler
from aigie.decision.handlers.report_only import BINDINGS as _report_only_bindings
from aigie.decision.handlers.report_only import ReportOnlyHandler
from aigie.decision.handlers.retry import BINDINGS as _retry_bindings
from aigie.decision.handlers.retry import RetryHandler
from aigie.decision.steps import VerbBinding

DEFAULT_BINDINGS: list[VerbBinding] = [
    *_no_op_bindings,
    *_retry_bindings,
    *_prompt_bindings,
    *_reduce_context_bindings,
    *_correct_tool_call_bindings,
    *_report_only_bindings,
]

__all__ = [
    "DEFAULT_BINDINGS",
    "CorrectToolCallHandler",
    "NoOpHandler",
    "PromptHandler",
    "ReduceContextHandler",
    "ReportOnlyHandler",
    "RetryHandler",
]
