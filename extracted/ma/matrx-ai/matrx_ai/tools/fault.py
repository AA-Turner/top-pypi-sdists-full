"""Fault-domain classification for tool failures.

Every tool failure is one of four kinds. The distinction the platform cares
about most is the first two: *who is at fault when a tool call fails?*

* ``model_error`` — the **model** is at fault. It passed arguments the tool's
  schema rejects (wrong/extra/missing/typed-wrong), called a tool that wasn't in
  its allowed set, hallucinated a tool name, or looped. The tool *definition* is
  fine; the caller misused it. Fixing this means better prompting / schemas, not
  tool code.
* ``tool_defect`` — **our tool** is at fault. The implementation threw, returned
  a malformed envelope, has no viable executor, or tripped one of our own
  internal validation gates. This is an engineering bug in the tool definition
  or implementation and should be fixed in code.
* ``infra`` — the **environment** is at fault: timeouts, DB/transport errors,
  external handler / MCP connectivity. Transient or operational.
* ``user`` — **policy / authorization**: the user lacks permission, or a
  per-conversation / cost budget was hit. Working as designed.

This single mapping lives here so the file sink, the DB trace sink, and the
``cx_tool_call`` row all classify identically — and so the admin dashboard can
split "the model keeps getting this wrong" from "this tool is broken" with one
field instead of a pile of error-string heuristics.
"""
from __future__ import annotations

MODEL_ERROR = "model_error"
TOOL_DEFECT = "tool_defect"
INFRA = "infra"
USER = "user"
OK = "ok"

# Maps the executor's ``error_type`` strings to a fault domain. Anything not
# listed defaults to ``tool_defect`` — an unknown failure shape is, until proven
# otherwise, treated as our bug so it gets attention rather than being silently
# blamed on the model.
_FAULT_BY_ERROR_TYPE: dict[str, str] = {
    # ── model's fault ──
    "invalid_arguments": MODEL_ERROR,   # NEW: pre-dispatch arg-model validation failed
    "not_allowed": MODEL_ERROR,         # called a tool not in its allowed set
    "not_found": MODEL_ERROR,           # hallucinated a tool name
    "unknown_category": MODEL_ERROR,    # bad enum/category argument
    "duplicate": MODEL_ERROR,           # loop guard: identical repeated call
    "loop_detected": MODEL_ERROR,
    "rate_limit": MODEL_ERROR,
    # ── our tool's fault ──
    "no_viable_executor": TOOL_DEFECT,  # LOCAL tool with no function_path wired
    "no_handler": TOOL_DEFECT,
    "embedded_error_envelope": TOOL_DEFECT,
    "missing_error_field": TOOL_DEFECT,
    "matrx_validation_gate": TOOL_DEFECT,
    "configuration": TOOL_DEFECT,
    "execution": TOOL_DEFECT,           # unhandled exception inside the tool body
    "client_tool_error": TOOL_DEFECT,
    "batch_all_failed": TOOL_DEFECT,
    "batch_partial_failure": TOOL_DEFECT,
    # ── environment's fault ──
    "timeout": INFRA,
    "database": INFRA,
    "external_handler_error": INFRA,
    "mcp_error": INFRA,
    "abandoned": INFRA,                 # client disconnect / cancellation
    # ── policy / user ──
    "permission": USER,
    "conversation_limit": USER,
    "cost_budget": USER,
}

# Valid values for the DB CHECK constraint / admin filters.
FAULT_DOMAINS = (OK, MODEL_ERROR, TOOL_DEFECT, INFRA, USER)


def classify_fault(error_type: str | None, *, success: bool = False) -> str:
    """Return the fault domain for a tool result.

    Args:
        error_type: the executor's ``error_type`` / trace ``err_type`` (may be None).
        success: when True, the call succeeded → ``ok``.
    """
    if success:
        return OK
    if not error_type:
        return TOOL_DEFECT
    return _FAULT_BY_ERROR_TYPE.get(error_type, TOOL_DEFECT)
