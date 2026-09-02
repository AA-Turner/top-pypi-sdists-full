"""Replicated handle_tool_calls integration point.

This module shows exactly how the new tool system plugs into the existing
``execute_until_complete`` loop in ``ai/executor.py``.

When rolling out, the single change needed in ``ai/executor.py`` is to:
  1. Import from this module
  2. Replace the current ``handle_tool_calls`` call with ``handle_tool_calls_v2``
  3. Feature-flag it for gradual rollout

This file is self-contained — it can be tested independently.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from matrx_utils import vcprint

from matrx_ai.config.usage_config import TokenUsage

from .executor import ToolExecutor
from .guardrails import GuardrailEngine
from .lifecycle import ToolLifecycleManager
from .logger import ToolExecutionLogger
from .models import ToolContext, ToolError, ToolResult
from .registry import ToolRegistry

logger = logging.getLogger(__name__)


def _resolve_call_tool_def(name: str):
    """The ToolDefinition a raw model call would dispatch to, or None. Projected
    (per-request) definitions take precedence over the global registry — the
    same order the executor resolves at dispatch."""
    if not name:
        return None
    try:
        from matrx_ai.tools.agent_projection import lookup_projected_tool

        projected = lookup_projected_tool(name)
        if projected is not None:
            return projected
        return ToolRegistry.get_instance().get(name)
    except Exception:  # noqa: BLE001 — policy detection must never break dispatch
        return None


def _is_handoff_call(name: str) -> bool:
    """Whether a raw model call targets a handoff-flagged agent tool."""
    return bool(getattr(_resolve_call_tool_def(name), "handoff_terminal", False))


# Module-level singleton — initialized once at app startup
_executor: ToolExecutor | None = None


def get_executor() -> ToolExecutor:
    global _executor
    if _executor is None:
        registry = ToolRegistry.get_instance()
        if not registry.loaded:
            vcprint(
                "[Tool System] Creating executor but registry was never initialized. "
                "Did initialize_tool_system() run at startup?",
                color="red",
            )
        elif registry.count == 0:
            vcprint(
                "[Tool System] Creating executor but registry has 0 tools loaded.",
                color="red",
            )
        _executor = ToolExecutor(
            registry=registry,
            guardrails=GuardrailEngine(),
            execution_logger=ToolExecutionLogger(),
            lifecycle=ToolLifecycleManager.get_instance(),
        )
    return _executor


async def initialize_tool_system() -> int:
    """Call once at app startup to load tools from the database (async).

    Returns the total number of tools registered (DB rows + bundled
    catalogs that ship in code, e.g. browser-dom).
    """
    registry = ToolRegistry.get_instance()
    count = await registry.load_from_database()

    if count == 0:
        vcprint(
            "[Tool System] WARNING: 0 tools loaded from database. "
            "Tool calls will fail. Check tool.definition rows / is_active flags (or the host tool_source).",
            color="red",
        )
    else:
        vcprint(f"[Tools] Loaded {count} tools", color="green")

    # Initialize the per-process tool-debug log path so it's ready for the
    # session. _debug_log prints the single canonical discovery line to
    # stderr on creation — no duplicate announcement here.
    try:
        from matrx_ai.tools._debug_log import log_path

        log_path()
    except Exception:
        pass

    # Register every tool that ships in code rather than the DB. Browser-dom
    # tools live in the Chrome-extension catalog (matrx_ai.capabilities.
    # browser_dom_catalog.json) — they can't be loaded by load_from_database
    # because they have no DB rows, but they're standard registered tools
    # at runtime: the executor finds them via the registry like any other
    # built-in.
    catalog_count = _register_bundled_catalogs()
    if catalog_count:
        vcprint(
            f"[Tool System] +{catalog_count} bundled-catalog tools registered "
            f"(total registry: {count + catalog_count})",
            color="green",
        )

    get_executor()

    lifecycle = ToolLifecycleManager.get_instance()
    lifecycle.start_background_sweep()

    return count + catalog_count


def initialize_tool_system_sync() -> int:
    """Call once at app startup to load tools from the database (sync).

    Use this when the caller does not have an active event loop
    (e.g. module-level code in asgi.py).
    """
    registry = ToolRegistry.get_instance()
    count = registry.load_from_database_sync()

    if count == 0:
        vcprint(
            "[Tool System] WARNING: 0 tools loaded from database. "
            "Tool calls will fail. Check tool.definition rows / is_active flags (or the host tool_source).",
            color="red",
        )
    else:
        vcprint(
            f"[Tools] Loaded {count} tools (sync)",
            color="green",
        )

    catalog_count = _register_bundled_catalogs()
    if catalog_count:
        vcprint(
            f"[Tool System] +{catalog_count} bundled-catalog tools registered "
            f"(total registry: {count + catalog_count})",
            color="green",
        )

    get_executor()

    return count + catalog_count


def _register_bundled_catalogs() -> int:
    """Register tools that ship as Python-bundled catalogs (no DB rows).

    Historical no-op as of migration 0022 — the browser-dom tools now live
    in the ``tool.definition`` DB table (plain names; the only
    colon-namespaced rows today are the ``bundle:list_*`` listers) and are
    loaded by ``load_from_database``. Inline-spec dispatch for any
    genuinely-ad-hoc third-party client tools is handled by Step 1's
    ``ensure_registered`` hook in the merge primitive.

    Kept as a stub so the call site in ``initialize_tool_system{,_sync}``
    doesn't need to change; future capability bundles that legitimately
    cannot live in the DB (none today) would re-add their helpers here.
    """
    return 0


async def handle_tool_calls_v2(
    tool_calls_raw: list[dict[str, Any]],
    *,
    iteration: int,
    recursion_depth: int = 0,
    cost_budget_remaining: float | None = None,
    client_tools: frozenset[str] | None = None,
    allowed_tools: frozenset[str] | None = None,
    message_id: str | None = None,
) -> tuple[list[dict[str, Any]], list[TokenUsage], list[str]]:
    """Execute tool calls using the current ExecutionContext.

    All user/emitter/project context is read from the ContextVar.

    Parameters
    ----------
    client_tools:
        Frozenset of tool names to delegate to the connected client instead of
        executing server-side. When a tool is in this set the executor emits a
        ``tool_delegated`` event and suspends until the client POSTs results back
        via ``POST /conversations/{id}/tool_results``.
    allowed_tools:
        Frozenset of tool names that were actually sent to the model in the
        current iteration's API call.  When provided, any tool call whose name
        is NOT in this set is rejected before execution — the model cannot invoke
        tools it was never given.  ``None`` means no restriction (open set).

    Returns
    -------
    (content_results, child_token_usages, pending_call_ids)
        - content_results: list of dicts matching ToolResultContent fields, for
          the COMPLETED calls only. Pending client-delegated calls are excluded —
          they produced no result yet (the turn suspends; see
          docs/tool_delegation/DELEGATION_LOOP_BUGS.md).
        - child_token_usages: list of TokenUsage objects from child agent executions
        - pending_call_ids: call_ids that were delegated to the client and are
          awaiting a POST /tool_results. Non-empty means the orchestrator must
          end the turn and let /resume continue once the client answers.
    """
    executor = get_executor()

    lifecycle = ToolLifecycleManager.get_instance()
    if not lifecycle.sweep_running:
        lifecycle.start_background_sweep()

    ctx = ToolContext(
        call_id="",
        tool_name="",
        iteration=iteration,
        message_id=message_id,
        recursion_depth=recursion_depth,
        cost_budget_remaining=cost_budget_remaining,
    )

    # ── Handoff batch policy — enforced BEFORE dispatch ─────────────────────
    # execute_batch runs everything concurrently; a post-hoc rejection cannot
    # un-stream or un-spend an already-run handoff agent. Exactly ONE handoff
    # per response, and never alongside a client-delegated call (the suspend
    # and the terminal exit cannot both own the turn). Violating handoff calls
    # are converted to error tool_results WITHOUT running the target.
    blocked_handoff_content: list[dict[str, Any]] = []
    dispatchable = tool_calls_raw
    handoff_calls = [c for c in tool_calls_raw if _is_handoff_call(c.get("name", ""))]
    if handoff_calls:
        # Live-parsed call names are WIRE spellings (ns__tool) while
        # client_tools holds internal names (ns:tool) — compare in wire form
        # (to_wire_name is idempotent on plain names) or colon-named delegated
        # tools silently share a batch with a handoff.
        delegated_in_batch = False
        if client_tools:
            from matrx_ai.config.wire_names import to_wire_name

            client_wire_names = {to_wire_name(n) for n in client_tools}
            delegated_in_batch = any(
                to_wire_name(c.get("name", "")) in client_wire_names for c in tool_calls_raw
            )
        policy_error: str | None = None
        if len(handoff_calls) > 1:
            policy_error = (
                "Handoff policy: call exactly ONE handoff tool per response — "
                "this batch contained several, none were run. Pick one and call it alone."
            )
        elif delegated_in_batch:
            policy_error = (
                "Handoff policy: a handoff cannot share a turn with a "
                "client-delegated tool call — the handoff was not run. Resolve "
                "the client tool first, then call the handoff alone."
            )
        if policy_error:
            blocked_ids = {id(c) for c in handoff_calls}
            dispatchable = [c for c in tool_calls_raw if id(c) not in blocked_ids]
            blocked_handoff_content = [
                {
                    "tool_use_id": c.get("call_id", ""),
                    "call_id": c.get("call_id", ""),
                    "name": c.get("name", ""),
                    "content": f"TOOL BLOCKED [handoff_policy]: {policy_error}",
                    "is_error": True,
                    "error": {
                        "error_type": "handoff_policy",
                        "message": policy_error,
                        "is_retryable": True,
                        "suggested_action": ("Call one handoff, alone, in its own turn."),
                    },
                }
                for c in handoff_calls
            ]
            # A blocked call still needs its durable cx_tool_call row: the
            # next-turn rebuild draws tool_results ONLY from terminal rows —
            # without one, the pointer block empties, the tool_use orphans,
            # and sanitize silently drops the pair (the model never learns the
            # policy error). Same two-phase logging the executor runs.
            for c in handoff_calls:
                try:
                    blocked_def = _resolve_call_tool_def(c.get("name", ""))
                    if blocked_def is None:
                        continue
                    call_ctx = ctx.model_copy(
                        update={
                            "call_id": c.get("call_id", ""),
                            "tool_name": c.get("name", ""),
                        }
                    )
                    blocked_result = ToolResult(
                        success=False,
                        error=ToolError(
                            error_type="handoff_policy",
                            message=policy_error,
                            is_retryable=True,
                            suggested_action="Call one handoff, alone, in its own turn.",
                        ),
                        started_at=time.time(),
                        completed_at=time.time(),
                        tool_name=c.get("name", ""),
                        call_id=c.get("call_id", ""),
                    )
                    row_id = await executor.execution_logger.log_started(
                        call_ctx,
                        blocked_def,
                        c.get("arguments") or {},
                        exposed_name=c.get("name", ""),
                    )
                    await executor.execution_logger.log_completed(row_id, blocked_result, [])
                except Exception as exc:  # noqa: BLE001 — best-effort audit
                    logger.warning("blocked-handoff row logging failed: %s", exc)

    content_results, full_results = await executor.execute_batch(
        dispatchable, ctx, client_tools=client_tools, allowed_tools=allowed_tools
    )

    all_child_usages: list[TokenUsage] = []
    completed_content: list[dict[str, Any]] = []
    pending_call_ids: list[str] = []
    auto_stub_keys: list[str] = []
    handoff_outcome = None
    for content_dict, result in zip(content_results, full_results):
        all_child_usages.extend(result.child_usages)
        if result.delegated_pending:
            pending_call_ids.append(result.call_id)
        else:
            completed_content.append(content_dict)
        # Serve-once value reads: the key is stamped/stubbed only AFTER the
        # next provider response consumes this result (the orchestrator's
        # turn-directive drain) — never here at completion.
        if result.auto_stub and result.value_ref_key:
            auto_stub_keys.append(result.value_ref_key)
        # Terminal handoff (the pre-dispatch policy guarantees at most one).
        if result.handoff_final and result.handoff is not None:
            handoff_outcome = result.handoff

    completed_content.extend(blocked_handoff_content)

    return (
        completed_content,
        all_child_usages,
        pending_call_ids,
        auto_stub_keys,
        handoff_outcome,
    )


async def cleanup_conversation(conversation_id: str) -> None:
    """Call when a conversation ends to clean up resources."""
    lifecycle = ToolLifecycleManager.get_instance()
    await lifecycle.cleanup_conversation(conversation_id)

    guardrails = get_executor().guardrails
    guardrails.clear_conversation(conversation_id)
