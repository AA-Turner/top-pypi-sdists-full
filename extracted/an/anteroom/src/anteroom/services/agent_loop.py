"""Shared agentic loop for web and CLI chat interfaces."""

from __future__ import annotations

import asyncio
import json
import logging
import time
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any, AsyncGenerator

from .ai_service import AIService
from .compaction import (
    AGENT_LOOP_CONTENT_TEMPLATE,
    COMPACTION_MIN_MESSAGES,
    PROACTIVE_COMPACTION_MSG_THRESHOLD,
    PROACTIVE_COMPACTION_TOKEN_THRESHOLD,
    CompactionResult,
    collapse_old_tool_results_details,
    drop_old_turn_groups,
    logical_tail_boundary,
)
from .compaction import (
    compact_messages as _shared_compact_messages,
)
from .context_trust import wrap_untrusted
from .diagnostic_context import log_debug
from .microcompact import microcompact as _microcompact
from .token_budget import BudgetCheckResult, check_all_budgets
from .token_estimator import (
    RequestTokenBreakdown,
    count_message_tokens,
    estimate_request_tokens,
    request_breakdown_to_metadata,
)
from .tool_result_compact import compact_tool_output

logger = logging.getLogger(__name__)

# Per-turn skill policy, set when dequeuing a skill message or by the
# direct /skill-name REPL path.  Task-scoped via contextvars so
# concurrent web requests are isolated.
active_skill_policy: ContextVar[Any] = ContextVar("active_skill_policy", default=None)


@dataclass
class AgentEvent:
    kind: str
    data: dict[str, Any]


_DEFAULT_TOOL_OUTPUT_MAX_CHARS = 10_000
_DEFAULT_TOOL_TIMEOUT = 300  # 5 minutes hard cap per tool execution

# Proactive compaction thresholds live in the shared compaction module;
# re-exported here under their historical private names for compatibility
# with any external references.
_PROACTIVE_COMPACTION_MSG_THRESHOLD = PROACTIVE_COMPACTION_MSG_THRESHOLD
_PROACTIVE_COMPACTION_TOKEN_THRESHOLD = PROACTIVE_COMPACTION_TOKEN_THRESHOLD
_COMPACT_PRESERVED_TAIL_METADATA = "compact_preserved_tail"


def _humanize_tool_brief(tool_name: str, arguments: dict[str, Any]) -> str:
    """Produce a short human-readable summary for a tool call (#1366).

    Used in phase events sent to both CLI and web UI.
    """
    name_lower = tool_name.lower()
    if name_lower in ("file_read", "read_file"):
        path = arguments.get("path", arguments.get("file_path", ""))
        return f"Reading {path}" if path else "Reading file"
    if name_lower in ("file_write", "write_file"):
        path = arguments.get("path", arguments.get("file_path", ""))
        return f"Writing {path}" if path else "Writing file"
    if name_lower in ("file_edit", "edit_file"):
        path = arguments.get("path", arguments.get("file_path", ""))
        return f"Editing {path}" if path else "Editing file"
    if name_lower in ("grep", "search", "ripgrep"):
        pattern = arguments.get("pattern", arguments.get("query", ""))
        return f"Searching for '{pattern}'" if pattern else "Searching"
    if name_lower in ("glob", "glob_files", "find_files"):
        pattern = arguments.get("pattern", "")
        return f"Finding {pattern}" if pattern else "Finding files"
    if name_lower == "bash":
        cmd = arguments.get("command", "")
        if len(cmd) > 60:
            cmd = cmd[:57] + "..."
        return f"bash {cmd}" if cmd else "Running command"
    if name_lower == "run_agent":
        return "Running sub-agent"
    return tool_name


def _truncate_large_tool_outputs(
    messages: list[dict[str, Any]], max_chars: int = _DEFAULT_TOOL_OUTPUT_MAX_CHARS
) -> bool:
    """Truncate oversized tool result messages (reactive Strategy 1).

    Delegates to :func:`anteroom.services.microcompact.microcompact` with
    the ``oversized_tool_outputs`` strategy so proactive microcompact
    (#1266) and the reactive overflow ladder (#1415) share a single
    implementation. ``min_messages=1`` — the reactive caller has already
    verified the history exists and shouldn't be gated by the safety
    floor that guards proactive microcompact on nearly-empty histories.
    """
    result = _microcompact(
        messages,
        tool_output_max_chars=max_chars,
        min_messages=1,
        strategies=["oversized_tool_outputs"],
    )
    return result.success


def _compacted_history_state(messages: list[dict[str, Any]]) -> tuple[int, int]:
    """Return ``(prefix_len, preserved_tail_len)`` for a compacted history.

    Compacted histories start with ``metadata.compact_summary`` and may include
    a boundary marker with ``metadata.compact_boundary`` immediately after the
    summary.  The boundary marker records how many tail messages were preserved
    at compaction time; those retained messages should not immediately count as
    new history for the next proactive trigger.
    """
    if not messages:
        return 0, 0

    summary_metadata = messages[0].get("metadata") or {}
    if not summary_metadata.get("compact_summary"):
        return 0, 0

    prefix_len = 1
    preserved_tail_len = 0
    if len(messages) > 1:
        boundary_metadata = messages[1].get("metadata") or {}
        if boundary_metadata.get("compact_boundary"):
            prefix_len = 2
            raw_preserved = boundary_metadata.get("preserved_count", 0)
            if isinstance(raw_preserved, int):
                preserved_tail_len = max(0, raw_preserved)

    return prefix_len, preserved_tail_len


def _mark_compacted_tail(messages: list[dict[str, Any]]) -> None:
    """Mark preserved tail messages so future turns can count only new history."""
    prefix_len, _preserved_tail_len = _compacted_history_state(messages)
    if prefix_len == 0:
        return
    for msg in messages[prefix_len:]:
        metadata = dict(msg.get("metadata") or {})
        metadata[_COMPACT_PRESERVED_TAIL_METADATA] = True
        msg["metadata"] = metadata


def _new_history_since_compaction(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return messages appended after the existing compacted prefix/tail."""
    prefix_len, preserved_tail_len = _compacted_history_state(messages)
    if prefix_len == 0:
        return messages
    tail = messages[prefix_len:]
    if any((msg.get("metadata") or {}).get(_COMPACT_PRESERVED_TAIL_METADATA) for msg in tail):
        new_start = 0
        while new_start < len(tail):
            metadata = tail[new_start].get("metadata") or {}
            if metadata.get(_COMPACT_PRESERVED_TAIL_METADATA):
                new_start += 1
                continue
            if tail[new_start].get("role") == "tool" and new_start > 0:
                new_start += 1
                continue
            break
        return tail[new_start:]
    return tail[preserved_tail_len:]


def _proactive_compaction_phase(
    messages: list[dict[str, Any]],
    *,
    request_breakdown: RequestTokenBreakdown,
    summary_trigger_msg_count: int,
    summary_trigger_token_count: int,
) -> dict[str, Any] | None:
    """Build proactive compaction phase metadata, or ``None`` if not needed."""
    token_hit = request_breakdown.total >= summary_trigger_token_count
    message_hit = len(messages) >= summary_trigger_msg_count
    if not token_hit and not message_hit:
        return None

    from .token_estimator import count_message_tokens

    prefix_len, _preserved_tail_len = _compacted_history_state(messages)
    if prefix_len:
        new_history = _new_history_since_compaction(messages)
        new_token_estimate = count_message_tokens(new_history)
        new_token_hit = new_token_estimate >= summary_trigger_token_count
        new_message_hit = len(new_history) >= summary_trigger_msg_count
        if not new_token_hit and not new_message_hit:
            logger.debug(
                "Skipping proactive compaction for already compacted history: "
                "new_messages=%d threshold=%d new_tokens~%d threshold=%d",
                len(new_history),
                summary_trigger_msg_count,
                new_token_estimate,
                summary_trigger_token_count,
            )
            return None

        token_hit = new_token_hit
        message_hit = new_message_hit
        message_count = len(new_history)
    else:
        message_count = len(messages)

    reasons: list[str] = []
    if token_hit:
        reasons.append("token_threshold")
    if message_hit:
        reasons.append("message_count")

    reason = "token_and_message_threshold" if len(reasons) == 2 else reasons[0]
    return {
        "phase": "compacting",
        "reason": reason,
        "reasons": reasons,
        **request_breakdown_to_metadata(
            request_breakdown,
            token_threshold=summary_trigger_token_count,
        ),
        "message_count": message_count,
        "message_threshold": summary_trigger_msg_count,
    }


def _coerce_tool_arguments(raw_arguments: Any) -> dict[str, Any]:
    """Normalize tool-call arguments to a dict."""
    if isinstance(raw_arguments, dict):
        return raw_arguments
    if isinstance(raw_arguments, str) and raw_arguments:
        try:
            parsed = json.loads(raw_arguments)
        except (json.JSONDecodeError, ValueError):
            return {}
        if isinstance(parsed, dict):
            return parsed
    return {}


async def _compact_messages(
    ai_service: AIService,
    messages: list[dict[str, Any]],
    *,
    preserve_tail: int = 0,
    db: Any | None = None,
    conversation_id: str | None = None,
    rehydrate: bool = True,
    rehydrate_max_files: int = 20,
    rehydrate_max_errors: int = 5,
    summary_max_completion_tokens: int = 1000,
    summary_retry_max_attempts: int = 3,
    summary_retry_drop_groups: int = 2,
    cancel_event: asyncio.Event | None = None,
) -> bool:
    """Summarize conversation history to reduce context size. Returns True on success.

    Thin wrapper around :func:`services.compaction.compact_messages` that
    preserves the historical ``bool`` return used by this module's loop
    control.  When *preserve_tail* is 0 (default) the output shape is
    identical to the legacy behaviour: one summary message replaces the
    entire history.  When *preserve_tail* > 0, boundary-based compaction
    summarises only the older portion and keeps the trailing messages
    intact — see :func:`services.compaction._find_tail_boundary` for the
    walk-back rules.

    When *db* and *conversation_id* are provided, the compacted shape is
    also persisted to SQLite via
    :func:`services.compaction.persist_compacted_messages`.  This is the
    path used by live conversations so the compacted form survives
    ``/resume`` and web reload.
    """
    # Pre-compute the persisted tail IDs from the same logical boundary that
    # will mutate the runtime list below. Runtime and SQLite represent tool
    # turns differently, so this must map by logical turn group rather than
    # re-running the boundary algorithm over stored rows.
    tail_message_ids: list[str] = []
    tail_mapping_aligned = True
    tail_mapping_reason: str | None = None
    if db is not None and conversation_id is not None and preserve_tail > 0:
        try:
            from . import storage as _storage

            stored_rows = _storage.list_messages(db, conversation_id)
            boundary = logical_tail_boundary(messages, stored_rows, preserve_tail)
            tail_message_ids = boundary.tail_message_ids
            tail_mapping_aligned = boundary.aligned
            tail_mapping_reason = boundary.reason
        except Exception:
            tail_mapping_aligned = False
            tail_mapping_reason = "tail_mapping_exception"
            logger.warning(
                "Failed to compute stored tail IDs for persistence; compaction will run in-memory only",
                exc_info=True,
            )

    result = await _compact_messages_result(
        ai_service,
        messages,
        preserve_tail=preserve_tail,
        db=db,
        conversation_id=conversation_id,
        tail_message_ids=tail_message_ids,
        tail_mapping_aligned=tail_mapping_aligned,
        tail_mapping_reason=tail_mapping_reason,
        rehydrate=rehydrate,
        rehydrate_max_files=rehydrate_max_files,
        rehydrate_max_errors=rehydrate_max_errors,
        summary_max_completion_tokens=summary_max_completion_tokens,
        summary_retry_max_attempts=summary_retry_max_attempts,
        summary_retry_drop_groups=summary_retry_drop_groups,
        cancel_event=cancel_event,
    )
    return result.success


async def _compact_messages_result(
    ai_service: AIService,
    messages: list[dict[str, Any]],
    *,
    preserve_tail: int = 0,
    db: Any | None = None,
    conversation_id: str | None = None,
    tail_message_ids: list[str] | None = None,
    tail_mapping_aligned: bool = True,
    tail_mapping_reason: str | None = None,
    rehydrate: bool = True,
    rehydrate_max_files: int = 20,
    rehydrate_max_errors: int = 5,
    summary_max_completion_tokens: int = 1000,
    summary_retry_max_attempts: int = 3,
    summary_retry_drop_groups: int = 2,
    cancel_event: asyncio.Event | None = None,
) -> CompactionResult:
    """Summarize conversation history and return result metadata."""
    if tail_message_ids is None:
        tail_message_ids = []
        if db is not None and conversation_id is not None and preserve_tail > 0:
            try:
                from . import storage as _storage
                from .compaction import _find_tail_boundary

                stored_rows = _storage.list_messages(db, conversation_id)
                stored_split = _find_tail_boundary(stored_rows, preserve_tail)
                if stored_split > 0:
                    tail_message_ids = [r["id"] for r in stored_rows[stored_split:]]
            except Exception:
                tail_mapping_aligned = False
                tail_mapping_reason = "tail_mapping_exception"
                logger.warning(
                    "Failed to compute stored tail IDs for persistence; compaction will run in-memory only",
                    exc_info=True,
                )

    result = await _shared_compact_messages(
        ai_service,
        messages,
        role="user",
        content_template=AGENT_LOOP_CONTENT_TEMPLATE,
        preserve_tail=preserve_tail,
        rehydrate=rehydrate,
        rehydrate_max_files=rehydrate_max_files,
        rehydrate_max_errors=rehydrate_max_errors,
        summary_max_completion_tokens=summary_max_completion_tokens,
        summary_retry_max_attempts=summary_retry_max_attempts,
        summary_retry_drop_groups=summary_retry_drop_groups,
        cancel_event=cancel_event,
    )

    if result.success:
        _mark_compacted_tail(messages)

    if result.success and db is not None and conversation_id is not None and tail_mapping_aligned:
        try:
            from . import storage as _storage
            from .compaction import persist_compacted_messages

            summary_msg = messages[0] if messages else None
            boundary_msg = (
                messages[1] if len(messages) > 1 and messages[1].get("metadata", {}).get("compact_boundary") else None
            )
            if summary_msg is not None:
                persist_compacted_messages(
                    db,
                    conversation_id,
                    summary_msg=summary_msg,
                    boundary_msg=boundary_msg,
                    tail_message_ids=tail_message_ids or [],
                )
                for msg_id in tail_message_ids or []:
                    _storage.merge_message_metadata(
                        db,
                        msg_id,
                        {_COMPACT_PRESERVED_TAIL_METADATA: True},
                    )
        except Exception:
            logger.warning(
                "Failed to persist compacted conversation; in-memory form is intact",
                exc_info=True,
            )
    elif result.success and db is not None and conversation_id is not None:
        logger.warning(
            "Skipping compacted conversation persistence because runtime/storage tail mapping failed: %s",
            tail_mapping_reason or "unknown",
        )

    return result


async def _execute_tool(
    tc: dict[str, Any],
    tool_executor: Any,
    cancel_event: asyncio.Event | None,
    timeout: float = _DEFAULT_TOOL_TIMEOUT,
) -> tuple[dict[str, Any], dict[str, Any], str]:
    """Execute a single tool call, returning (tool_call, result, status).

    A hard timeout prevents any single tool (including MCP tools) from
    hanging the entire agent loop indefinitely.
    """
    tool_args = {**_coerce_tool_arguments(tc.get("arguments")), "_tool_call_id": tc["id"]}
    if tc["function_name"] == "run_agent":
        # Internal-only association key for web subagent progress (#1460).
        # This is injected at execution time so it never leaks back into the
        # assistant-visible tool-call transcript or persisted tool input.
        tool_args = {**tool_args, "_parent_tool_call_id": tc["id"]}
    try:
        if cancel_event:
            cancel_task = asyncio.create_task(cancel_event.wait())
            exec_task = asyncio.create_task(tool_executor(tc["function_name"], tool_args))
            timeout_task = asyncio.create_task(asyncio.sleep(timeout))
            done, pending = await asyncio.wait(
                {cancel_task, exec_task, timeout_task}, return_when=asyncio.FIRST_COMPLETED
            )
            for p in pending:
                p.cancel()
                try:
                    await asyncio.wait_for(p, timeout=0.5)
                except (asyncio.CancelledError, asyncio.TimeoutError):
                    pass
            if exec_task in done:
                return tc, exec_task.result(), "success"
            if timeout_task in done:
                tool_name = tc["function_name"]
                logger.warning("Tool '%s' timed out after %ds", tool_name, timeout)
                return tc, {"error": f"Tool execution timed out after {int(timeout)}s"}, "timeout"
            return tc, {"error": "Cancelled by user"}, "cancelled"
        else:
            result = await asyncio.wait_for(tool_executor(tc["function_name"], tool_args), timeout=timeout)
            return tc, result, "success"
    except asyncio.TimeoutError:
        tool_name = tc["function_name"]
        logger.warning("Tool '%s' timed out after %ds", tool_name, timeout)
        return tc, {"error": f"Tool execution timed out after {int(timeout)}s"}, "timeout"
    except Exception as e:
        return tc, {"error": str(e)}, "error"


_NARRATION_PROMPT = (
    "Briefly summarize your progress in 1-2 sentences: what have you found or done so far, "
    "and what are you doing next? Then continue your work."
)


async def run_agent_loop(
    ai_service: AIService,
    messages: list[dict[str, Any]],
    tool_executor: Any,
    tools_openai: list[dict[str, Any]] | None,
    cancel_event: asyncio.Event | None = None,
    extra_system_prompt: str | None = None,
    max_iterations: int = 50,
    message_queue: asyncio.Queue[dict[str, Any]] | None = None,
    narration_cadence: int = 0,
    tool_output_max_chars: int = _DEFAULT_TOOL_OUTPUT_MAX_CHARS,
    auto_plan_threshold: int = 0,
    budget_config: Any | None = None,
    get_token_totals: Any | None = None,
    dlp_scanner: Any | None = None,
    injection_detector: Any | None = None,
    output_filter: Any | None = None,
    max_consecutive_text_only: int = 3,
    max_line_repeats: int = 5,
    serialize_tools: bool = False,
    pause_signal: asyncio.Event | None = None,
    injection_queue: asyncio.Queue[dict[str, Any]] | None = None,
    compact_preserve_tail: int = 0,
    compact_rehydrate: bool = True,
    compact_rehydrate_max_files: int = 20,
    compact_rehydrate_max_errors: int = 5,
    microcompact_enabled: bool = True,
    historical_tool_collapse_enabled: bool = True,
    historical_tool_collapse_trigger_token_count: int = 80_000,
    historical_tool_collapse_keep_recent_groups: int = 6,
    historical_tool_collapse_compact_chars: int = 1_000,
    summary_trigger_msg_count: int = PROACTIVE_COMPACTION_MSG_THRESHOLD,
    summary_trigger_token_count: int = PROACTIVE_COMPACTION_TOKEN_THRESHOLD,
    reactive_max_attempts: int = 4,
    summary_max_completion_tokens: int = 1000,
    summary_retry_max_attempts: int = 3,
    summary_retry_drop_groups: int = 2,
    db: Any | None = None,
    conversation_id: str | None = None,
) -> AsyncGenerator[AgentEvent, None]:
    """Run the agentic tool-call loop, yielding events.

    tool_executor must be an async callable: (tool_name, arguments) -> dict
    budget_config: BudgetConfig dataclass (or None to disable).
    get_token_totals: async callable() -> (conversation_total, daily_total)
    """
    iteration = 0
    context_recovery_attempts = 0
    # Staged reactive overflow recovery (#1415): up to N strategies run in
    # sequence per recovery attempt — truncate oversized tool outputs,
    # collapse historical tool results, drop older turn groups, and finally
    # full LLM compaction.  ``reactive_max_attempts`` (default 4) gives
    # each strategy a chance before the loop gives up. Config-driven since
    # #1266 via ``CompactionConfig.reactive_max_attempts``.
    max_context_recoveries = reactive_max_attempts
    total_tool_calls = 0
    auto_plan_suggested = False
    request_tokens = 0  # tokens accumulated in this run_agent_loop invocation
    consecutive_text_only = 0

    _loop_start = time.monotonic()

    while iteration < max_iterations:
        iteration += 1
        _iter_start = time.monotonic()
        tool_calls_pending: list[dict[str, Any]] = []
        assistant_content = ""
        got_context_error = False
        logger.debug(
            "agent_loop iteration=%d messages=%d tools=%d elapsed=%.1fs",
            iteration,
            len(messages),
            len(tools_openai) if tools_openai else 0,
            _iter_start - _loop_start,
        )

        # Budget enforcement: check before each API call
        if budget_config and budget_config.enabled and get_token_totals:
            try:
                conv_total, daily_total = await get_token_totals()
            except Exception:
                logger.warning("Failed to fetch token totals for budget check", exc_info=True)
                conv_total, daily_total = 0, 0

            status = check_all_budgets(
                request_tokens=request_tokens,
                conversation_tokens=conv_total,
                daily_tokens=daily_total,
                max_per_request=budget_config.max_tokens_per_request,
                max_per_conversation=budget_config.max_tokens_per_conversation,
                max_per_day=budget_config.max_tokens_per_day,
                warn_threshold_percent=budget_config.warn_threshold_percent,
            )
            if status is not None:
                if status.result == BudgetCheckResult.EXCEEDED:
                    if budget_config.action_on_exceed == "block":
                        yield AgentEvent(
                            kind="error",
                            data={
                                "message": (
                                    f"Token budget exceeded ({status.label}): {status.used:,} / {status.limit:,} tokens"
                                ),
                                "code": "budget_exceeded",
                                "retryable": False,
                                "budget_label": status.label,
                                "budget_used": status.used,
                                "budget_limit": status.limit,
                            },
                        )
                        return
                    else:
                        yield AgentEvent(
                            kind="budget_warning",
                            data={
                                "message": (
                                    f"Token budget exceeded ({status.label}): "
                                    f"{status.used:,} / {status.limit:,} tokens (warn mode)"
                                ),
                                "label": status.label,
                                "used": status.used,
                                "limit": status.limit,
                                "percent": status.percent,
                            },
                        )
                elif status.result == BudgetCheckResult.WARNING:
                    yield AgentEvent(
                        kind="budget_warning",
                        data={
                            "message": (
                                f"Approaching {status.label} token budget: "
                                f"{status.used:,} / {status.limit:,} tokens "
                                f"({status.percent:.0f}%)"
                            ),
                            "label": status.label,
                            "used": status.used,
                            "limit": status.limit,
                            "percent": status.percent,
                        },
                    )

        # Proactive microcompact (#1266): cheap, deterministic, in-memory
        # sweep that runs every turn before the summary-trigger check. In
        # Phase 1 it trims any oversized tool results across the full
        # history (same strategy as reactive Strategy 1; single source of
        # truth via ``services.microcompact``). In-memory only — no SQLite
        # writes, no LLM call.
        if microcompact_enabled:
            _mc = _microcompact(
                messages,
                tool_output_max_chars=tool_output_max_chars,
                min_messages=COMPACTION_MIN_MESSAGES,
                strategies=["oversized_tool_outputs"],
            )
            if _mc.success:
                logger.info(
                    "Proactive microcompact applied: strategies=%s bytes_saved=%d",
                    _mc.strategies_applied,
                    _mc.bytes_saved,
                )
                yield AgentEvent(
                    kind="token",
                    data={"content": "\n\n*Trimmed oversized tool outputs to stay within context limits...*\n\n"},
                )

        # Proactive compaction: compact before hitting the API context limit (#1339).
        # Token and message-count thresholds are independent triggers, and the
        # phase payload below tells UIs which threshold fired.
        # Thresholds are config-driven since #1266.
        _ai_config = getattr(ai_service, "config", None)
        _raw_system_prompt = getattr(_ai_config, "system_prompt", "") if _ai_config is not None else ""
        _system_prompt = _raw_system_prompt if isinstance(_raw_system_prompt, str) else ""
        _loop_request_breakdown = estimate_request_tokens(
            messages=messages,
            system_prompt=_system_prompt,
            extra_system_prompt=extra_system_prompt or "",
            tool_schemas=tools_openai,
        )
        if microcompact_enabled and historical_tool_collapse_enabled:
            _historical_mc = _microcompact(
                messages,
                tool_output_max_chars=tool_output_max_chars,
                min_messages=COMPACTION_MIN_MESSAGES,
                strategies=["historical_tool_results"],
                historical_tool_collapse_enabled=historical_tool_collapse_enabled,
                estimated_tokens=_loop_request_breakdown.total,
                historical_tool_collapse_trigger_token_count=historical_tool_collapse_trigger_token_count,
                historical_tool_collapse_keep_recent_groups=historical_tool_collapse_keep_recent_groups,
                historical_tool_collapse_compact_chars=historical_tool_collapse_compact_chars,
            )
            if _historical_mc.success:
                detail = _historical_mc.metadata.get("historical_tool_results", {})
                logger.info(
                    "Proactive historical tool-result collapse applied: modified=%d bytes_saved=%d",
                    detail.get("modified_count", 0),
                    _historical_mc.bytes_saved,
                )
                phase_data = {
                    "phase": "compacting",
                    "reason": "historical_tool_results",
                    "reasons": ["historical_tool_results"],
                    "strategy": "historical_tool_results",
                    "bytes_saved": _historical_mc.bytes_saved,
                    "modified_count": detail.get("modified_count", 0),
                    "keep_recent_groups": detail.get(
                        "keep_recent_groups",
                        historical_tool_collapse_keep_recent_groups,
                    ),
                    "compact_chars": detail.get("compact_chars", historical_tool_collapse_compact_chars),
                    "estimated_tokens": detail.get("estimated_tokens", _loop_request_breakdown.total),
                    "token_threshold": historical_tool_collapse_trigger_token_count,
                }
                yield AgentEvent(kind="phase", data=phase_data)
                yield AgentEvent(
                    kind="token",
                    data={"content": "\n\n*Collapsed older tool results to reduce context pressure...*\n\n"},
                )
                yield AgentEvent(
                    kind="compaction",
                    data={
                        **phase_data,
                        "new_message_count": len(messages),
                        "in_memory_only": True,
                        "no_op": False,
                    },
                )
                _loop_request_breakdown = estimate_request_tokens(
                    messages=messages,
                    system_prompt=_system_prompt,
                    extra_system_prompt=extra_system_prompt or "",
                    tool_schemas=tools_openai,
                )
        _compaction_phase = _proactive_compaction_phase(
            messages,
            request_breakdown=_loop_request_breakdown,
            summary_trigger_msg_count=summary_trigger_msg_count,
            summary_trigger_token_count=summary_trigger_token_count,
        )
        if _compaction_phase is not None:
            logger.info(
                "Proactive compaction triggered: reason=%s ~%d tokens, %d messages "
                "(thresholds: %d tokens, %d messages)",
                _compaction_phase["reason"],
                _compaction_phase["estimated_tokens"],
                _compaction_phase["message_count"],
                summary_trigger_token_count,
                summary_trigger_msg_count,
            )
            yield AgentEvent(kind="thinking", data={})
            yield AgentEvent(kind="phase", data=_compaction_phase)
            _compact_result = await _compact_messages_result(
                ai_service,
                messages,
                preserve_tail=compact_preserve_tail,
                db=db,
                conversation_id=conversation_id,
                rehydrate=compact_rehydrate,
                rehydrate_max_files=compact_rehydrate_max_files,
                rehydrate_max_errors=compact_rehydrate_max_errors,
                summary_max_completion_tokens=summary_max_completion_tokens,
                summary_retry_max_attempts=summary_retry_max_attempts,
                summary_retry_drop_groups=summary_retry_drop_groups,
                cancel_event=cancel_event,
            )
            if _compact_result.retries:
                yield AgentEvent(
                    kind="phase",
                    data={
                        "phase": "compacting",
                        "reason": "compaction_prompt_too_long",
                        "attempt": _compact_result.attempts,
                        "max_attempts": summary_retry_max_attempts,
                        "dropped_messages": _compact_result.reduced_message_count,
                    },
                )
                yield AgentEvent(
                    kind="token",
                    data={
                        "content": (
                            "\n\n*Compaction summary prompt was too long — dropped older safe turns and retried...*\n\n"
                        )
                    },
                )
            if _compact_result.success:
                yield AgentEvent(
                    kind="compaction",
                    data={
                        "new_message_count": len(messages),
                        "reason": _compaction_phase["reason"],
                        "estimated_tokens": _compaction_phase["estimated_tokens"],
                        "message_tokens": _compaction_phase["message_tokens"],
                        "system_prompt_tokens": _compaction_phase["system_prompt_tokens"],
                        "tool_schema_tokens": _compaction_phase["tool_schema_tokens"],
                        "token_threshold": summary_trigger_token_count,
                        "message_count": _compaction_phase["message_count"],
                        "message_threshold": summary_trigger_msg_count,
                        "attempts": _compact_result.attempts,
                        "retries": _compact_result.retries,
                        "dropped_messages": _compact_result.reduced_message_count,
                        "messages_compacted": max(0, _compact_result.original_count - len(messages)),
                        "tail_preserved": max(0, len(messages) - 1),
                        "preserve_tail": compact_preserve_tail,
                        "in_memory_only": False,
                        "no_op": False,
                    },
                )
            elif _compact_result.failure_code:
                yield AgentEvent(
                    kind="error",
                    data={
                        "message": (
                            "Compaction failed while reducing conversation history. "
                            "Original history was left unchanged."
                        ),
                        "code": _compact_result.failure_code,
                        "retryable": _compact_result.failure_code == "context_length_exceeded",
                        "attempts": _compact_result.attempts,
                        "dropped_messages": _compact_result.reduced_message_count,
                    },
                )
                return

        # Per-iteration injection checkpoint (#889): drain mid-run
        # workflow inputs from `injection_queue` BEFORE the next LLM call.
        # Separate from `message_queue` (loop-continuation queue at `done`).
        if injection_queue is not None:
            _drained: list[dict[str, Any]] = []
            while True:
                try:
                    _drained.append(injection_queue.get_nowait())
                except asyncio.QueueEmpty:
                    break
            for _idx, _msg in enumerate(_drained, 1):
                # Strip internal metadata before adding to LLM messages
                _clean = {k: v for k, v in _msg.items() if not k.startswith("_")}
                messages.append(_clean)
                yield AgentEvent(
                    kind="queued_message",
                    data={
                        **_msg,
                        "position": _idx,
                        "queue_depth": injection_queue.qsize() + len(_drained) - _idx,
                    },
                )

        yield AgentEvent(kind="thinking", data={})

        _dlp_blocked = False
        _line_repeat_detected = False
        _line_buf = ""  # accumulates partial lines for inline repeat detection
        _prev_line = ""
        _line_run = 0
        _ai_call_start = time.monotonic()
        _first_token_logged = False
        _first_response_elapsed: float | None = None
        log_debug(
            logger,
            "agent_loop.ai_call.start",
            lifecycle="start",
            phase="ai_call",
            iteration=iteration,
            message_count=len(messages),
            tool_count=len(tools_openai or []),
        )
        async for event in ai_service.stream_chat(
            messages,
            tools=tools_openai,
            cancel_event=cancel_event,
            extra_system_prompt=extra_system_prompt,
        ):
            etype = event["event"]
            if not _first_token_logged and etype in ("token", "tool_call"):
                log_debug(
                    logger,
                    "agent_loop.ai_call.success",
                    lifecycle="success",
                    phase="first_response",
                    iteration=iteration,
                    response_type=etype,
                    _started_at=_ai_call_start,
                )
                _first_response_elapsed = time.monotonic() - _ai_call_start
                _first_token_logged = True
            if etype == "token":
                chunk = event["data"]["content"]
                # Per-chunk DLP: redact inline, block breaks stream.
                # Warn is deferred to the final assembled-text scan to
                # avoid duplicate events (per-chunk + final).
                if dlp_scanner is not None and dlp_scanner.enabled and dlp_scanner.scan_output:
                    chunk, dlp_result = dlp_scanner.apply(chunk, "output")
                    if dlp_result.matched and dlp_result.action == "block":
                        yield AgentEvent(
                            kind="dlp_blocked",
                            data={"direction": "output", "matches": [m.rule_name for m in dlp_result.matches]},
                        )
                        _dlp_blocked = True
                        break
                # Per-chunk output filter: custom pattern block (leak detection
                # requires full text and runs post-stream).
                if output_filter is not None and output_filter.enabled:
                    chunk_result = output_filter.scan_patterns_only(chunk)
                    if chunk_result.matched and chunk_result.action == "block":
                        yield AgentEvent(
                            kind="output_filter_blocked",
                            data={"matches": [m.rule_name for m in chunk_result.matches]},
                        )
                        _dlp_blocked = True  # reuse flag to skip final scan
                        break
                assistant_content += chunk
                _token_data: dict[str, Any] = {"content": chunk, "iteration": iteration}
                if _first_response_elapsed is not None:
                    _token_data["first_response_elapsed_seconds"] = _first_response_elapsed
                yield AgentEvent(kind="token", data=_token_data)
                # Inline line repetition detection: check as lines complete
                if max_line_repeats > 0:
                    _line_buf += chunk
                    while "\n" in _line_buf:
                        line, _line_buf = _line_buf.split("\n", 1)
                        stripped = line.strip()
                        if stripped:
                            if stripped == _prev_line:
                                _line_run += 1
                            else:
                                _prev_line = stripped
                                _line_run = 1
                            if _line_run >= max_line_repeats:
                                _line_repeat_detected = True
                                break
                    if _line_repeat_detected:
                        break
            elif etype == "tool_call":
                tool_calls_pending.append(event["data"])
                yield AgentEvent(
                    kind="tool_call_start",
                    data={
                        "id": event["data"]["id"],
                        "tool_name": event["data"]["function_name"],
                        "arguments": event["data"]["arguments"],
                        "iteration": iteration,
                        "first_response_elapsed_seconds": _first_response_elapsed,
                        "timeout_seconds": _DEFAULT_TOOL_TIMEOUT,
                    },
                )
            elif etype == "tool_call_args_delta":
                yield AgentEvent(kind="tool_call_args_delta", data={**event["data"], "iteration": iteration})
            elif etype == "phase":
                yield AgentEvent(kind="phase", data={**event["data"], "iteration": iteration})
            elif etype == "retrying":
                yield AgentEvent(kind="retrying", data={**event["data"], "iteration": iteration})
            elif etype == "usage":
                request_tokens += event["data"].get("total_tokens", 0)
                yield AgentEvent(kind="usage", data=event["data"])
            elif etype == "error":
                if (
                    event["data"].get("code") == "context_length_exceeded"
                    and context_recovery_attempts < max_context_recoveries
                ):
                    got_context_error = True
                    break
                yield AgentEvent(kind="error", data={**event["data"], "iteration": iteration})
                return
            elif etype == "done":
                break

        if _dlp_blocked:
            return

        # Inline repetition detection may have broken us out of the stream early.
        # Only act on it for text-only responses (tool call responses often have
        # repeated patterns in arguments and shouldn't be penalised).
        if _line_repeat_detected and not tool_calls_pending:
            yield AgentEvent(
                kind="error",
                data={
                    "message": (
                        f"Repetitive output detected: same line repeated {_line_run} times "
                        "during streaming. Stopping degenerate LLM output."
                    )
                },
            )
            return
        _line_repeat_detected = False  # Reset for tool-call responses

        if got_context_error:
            context_recovery_attempts += 1
            iteration -= 1  # don't count the failed attempt

            # Staged reactive overflow recovery (#1415).  Each strategy is
            # tried in order; the first that reports progress wins and the
            # loop retries.  Cheaper strategies fire first so the
            # conversation is preserved as much as possible — full LLM
            # compaction is the last resort.

            _recovery_message_count = len(messages)
            _recovery_tokens = count_message_tokens(messages)

            # Strategy 1: truncate oversized tool outputs (existing).
            if _truncate_large_tool_outputs(messages, max_chars=tool_output_max_chars):
                yield AgentEvent(
                    kind="compaction",
                    data={
                        "reason": "context_error_recovery",
                        "strategy": "truncate_large_tool_outputs",
                        "message_count": _recovery_message_count,
                        "new_message_count": len(messages),
                        "estimated_tokens": _recovery_tokens,
                        "attempts": context_recovery_attempts,
                        "max_attempts": max_context_recoveries,
                        "in_memory_only": True,
                        "no_op": False,
                    },
                )
                yield AgentEvent(
                    kind="token",
                    data={
                        "content": (
                            "\n\n*Context limit reached — tool output was too large. "
                            "Truncated and retrying with smaller scope...*\n\n"
                        )
                    },
                )
                continue

            # Strategy 2 (#1415): collapse all historical tool results to
            # a compact form regardless of current size.  Turn-group aware
            # — never splits an assistant+tool_calls from its tool results.
            _collapse_result = collapse_old_tool_results_details(messages, keep_recent_groups=2, compact_chars=200)
            if _collapse_result.success:
                yield AgentEvent(
                    kind="compaction",
                    data={
                        "reason": "context_error_recovery",
                        "strategy": "collapse_historical_tool_results",
                        "message_count": _recovery_message_count,
                        "new_message_count": len(messages),
                        "estimated_tokens": _recovery_tokens,
                        "attempts": context_recovery_attempts,
                        "max_attempts": max_context_recoveries,
                        "modified_count": _collapse_result.modified_count,
                        "bytes_saved": _collapse_result.bytes_saved,
                        "keep_recent_groups": _collapse_result.keep_recent_groups,
                        "compact_chars": _collapse_result.compact_chars,
                        "in_memory_only": True,
                        "no_op": False,
                    },
                )
                yield AgentEvent(
                    kind="token",
                    data={
                        "content": ("\n\n*Context limit reached — collapsed historical tool results, retrying...*\n\n")
                    },
                )
                continue

            # Strategy 3 (#1415): drop older turn groups with a
            # deterministic summary (no LLM call).  Produces the same
            # message shape as compact_messages() so downstream consumers
            # (#1414 rehydration, transcript renderers) treat it uniformly.
            _before_drop_count = len(messages)
            if drop_old_turn_groups(messages, keep_recent_groups=4):
                yield AgentEvent(
                    kind="compaction",
                    data={
                        "reason": "context_error_recovery",
                        "strategy": "drop_old_turn_groups",
                        "message_count": _before_drop_count,
                        "new_message_count": len(messages),
                        "estimated_tokens": _recovery_tokens,
                        "attempts": context_recovery_attempts,
                        "max_attempts": max_context_recoveries,
                        "messages_compacted": max(0, _before_drop_count - len(messages)),
                        "tail_preserved": max(0, len(messages) - 1),
                        "in_memory_only": True,
                        "no_op": False,
                    },
                )
                yield AgentEvent(
                    kind="token",
                    data={
                        "content": ("\n\n*Context limit reached — dropped older conversation turns, retrying...*\n\n")
                    },
                )
                continue

            # Strategy 4: full LLM compaction (last resort).
            yield AgentEvent(
                kind="phase",
                data={
                    "phase": "compacting",
                    "reason": "context_error_recovery",
                    "reasons": ["context_error_recovery"],
                    "strategy": "llm_summary",
                    "attempts": context_recovery_attempts,
                    "max_attempts": max_context_recoveries,
                    "message_count": len(messages),
                    "estimated_tokens": count_message_tokens(messages),
                },
            )
            yield AgentEvent(
                kind="token",
                data={"content": "\n\n*Context limit reached — compacting conversation and retrying...*\n\n"},
            )
            _compact_result = await _compact_messages_result(
                ai_service,
                messages,
                preserve_tail=compact_preserve_tail,
                db=db,
                conversation_id=conversation_id,
                rehydrate=compact_rehydrate,
                rehydrate_max_files=compact_rehydrate_max_files,
                rehydrate_max_errors=compact_rehydrate_max_errors,
                summary_max_completion_tokens=summary_max_completion_tokens,
                summary_retry_max_attempts=summary_retry_max_attempts,
                summary_retry_drop_groups=summary_retry_drop_groups,
                cancel_event=cancel_event,
            )
            if _compact_result.retries:
                yield AgentEvent(
                    kind="phase",
                    data={
                        "phase": "compacting",
                        "reason": "compaction_prompt_too_long",
                        "attempt": _compact_result.attempts,
                        "max_attempts": summary_retry_max_attempts,
                        "dropped_messages": _compact_result.reduced_message_count,
                    },
                )
                yield AgentEvent(
                    kind="token",
                    data={
                        "content": (
                            "\n\n*Compaction summary prompt was too long — dropped older safe turns and retried...*\n\n"
                        )
                    },
                )
            if _compact_result.success:
                yield AgentEvent(
                    kind="compaction",
                    data={
                        "reason": "context_error_recovery",
                        "strategy": "llm_summary",
                        "estimated_tokens": _compact_result.original_tokens,
                        "message_count": _compact_result.original_count,
                        "new_message_count": len(messages),
                        "attempts": _compact_result.attempts,
                        "retries": _compact_result.retries,
                        "dropped_messages": _compact_result.reduced_message_count,
                        "messages_compacted": max(0, _compact_result.original_count - len(messages)),
                        "tail_preserved": max(0, len(messages) - 1),
                        "preserve_tail": compact_preserve_tail,
                        "in_memory_only": False,
                        "no_op": False,
                    },
                )
                continue

            # Cancel fired during Strategy 4's LLM summary (#1266 senior
            # review): AIService.complete() returns None both on genuine
            # failure AND on cancel. Without this check, a user Escape
            # during recovery falls through to the "recovery failed"
            # error — which is wrong; the user cancelled, not the
            # strategy. Distinguish the two via cancel_event before
            # surfacing the terminal error.
            if cancel_event is not None and cancel_event.is_set():
                yield AgentEvent(kind="cancelled", data={"reason": "user_cancel_during_recovery"})
                return

            yield AgentEvent(
                kind="error",
                data={
                    "message": (
                        "Conversation too long for model context window. "
                        "Recovery failed after all strategies. "
                        "Original history was left unchanged. Please start a new conversation."
                    ),
                    "code": _compact_result.failure_code or "context_recovery_failed",
                    "attempts": _compact_result.attempts,
                    "dropped_messages": _compact_result.reduced_message_count,
                },
            )
            return

        if not tool_calls_pending:
            consecutive_text_only += 1
            if max_consecutive_text_only > 0 and consecutive_text_only > max_consecutive_text_only:
                yield AgentEvent(
                    kind="error",
                    data={
                        "message": (
                            f"Agent produced {consecutive_text_only} consecutive text-only responses "
                            "without tool calls. Stopping to prevent runaway loop."
                        )
                    },
                )
                return
            if max_line_repeats > 0 and assistant_content:
                lines = [ln.strip() for ln in assistant_content.splitlines() if ln.strip()]
                if lines:
                    max_run = 1
                    current_run = 1
                    for i in range(1, len(lines)):
                        if lines[i] == lines[i - 1]:
                            current_run += 1
                            if current_run > max_run:
                                max_run = current_run
                        else:
                            current_run = 1
                    if max_run >= max_line_repeats:
                        yield AgentEvent(
                            kind="error",
                            data={
                                "message": (
                                    f"Repetitive output detected: same line repeated {max_run} times "
                                    "in a single response. Stopping degenerate LLM output."
                                )
                            },
                        )
                        return
            if assistant_content:
                # Final DLP scan on complete assembled text (catches patterns split across chunks)
                if dlp_scanner is not None and dlp_scanner.enabled and dlp_scanner.scan_output:
                    assistant_content, dlp_final = dlp_scanner.apply(assistant_content, "output")
                    if dlp_final.matched and dlp_final.action == "block":
                        yield AgentEvent(
                            kind="dlp_blocked",
                            data={"direction": "output", "matches": [m.rule_name for m in dlp_final.matches]},
                        )
                        return
                    if dlp_final.matched and dlp_final.action == "warn":
                        yield AgentEvent(
                            kind="dlp_warning",
                            data={"direction": "output", "matches": [m.rule_name for m in dlp_final.matches]},
                        )
                # Output content filter scan (system prompt leak + custom patterns)
                if output_filter is not None and output_filter.enabled:
                    assistant_content, of_result = output_filter.apply(assistant_content)
                    if of_result.matched and of_result.action == "block":
                        yield AgentEvent(
                            kind="output_filter_blocked",
                            data={"matches": [m.rule_name for m in of_result.matches]},
                        )
                        return
                    if of_result.matched and of_result.action == "warn":
                        yield AgentEvent(
                            kind="output_filter_warning",
                            data={"matches": [m.rule_name for m in of_result.matches]},
                        )
                yield AgentEvent(kind="assistant_message", data={"content": assistant_content, "iteration": iteration})
            # Append the final assistant response to the conversation history so
            # subsequent turns (including queued messages) see the complete context.
            # Tool-call iterations already append to messages above; this covers
            # the final no-tool-call response that was previously missing.
            if assistant_content:
                messages.append({"role": "assistant", "content": assistant_content})
            yield AgentEvent(kind="done", data={"stop_reason": "completed", "iteration": iteration})

            # Clear skill policy from the completed turn before checking
            # the queue — prevents leaking into a non-skill follow-up.
            active_skill_policy.set(None)

            # Check message queue for follow-up messages
            if message_queue is not None:
                try:
                    queued_msg = message_queue.get_nowait()
                    _turn_policy = queued_msg.pop("_skill_policy", None)
                    active_skill_policy.set(_turn_policy)
                    queue_depth = message_queue.qsize()
                    messages.append(queued_msg)
                    yield AgentEvent(
                        kind="queued_message",
                        data={**queued_msg, "position": 1, "queue_depth": queue_depth},
                    )
                    continue
                except asyncio.QueueEmpty:
                    pass
            return

        # Final DLP scan on complete assistant text before storage (tool-call turn)
        if dlp_scanner is not None and dlp_scanner.enabled and dlp_scanner.scan_output and assistant_content:
            assistant_content, _ = dlp_scanner.apply(assistant_content, "output")
        # Output filter scan on tool-call turn text
        if output_filter is not None and output_filter.enabled and assistant_content:
            assistant_content, of_result = output_filter.apply(assistant_content)
            if of_result.matched and of_result.action == "block":
                yield AgentEvent(
                    kind="output_filter_blocked",
                    data={"matches": [m.rule_name for m in of_result.matches]},
                )
                return
            if of_result.matched and of_result.action in ("warn", "redact"):
                yield AgentEvent(
                    kind="output_filter_warning",
                    data={"matches": [m.rule_name for m in of_result.matches]},
                )

        # Save assistant message with tool calls into message history
        log_debug(
            logger,
            "agent_loop.ai_stream.success",
            lifecycle="success",
            phase="ai_stream",
            iteration=iteration,
            tool_calls=len(tool_calls_pending),
            assistant_chars=len(assistant_content),
            _started_at=_ai_call_start,
        )
        yield AgentEvent(kind="assistant_message", data={"content": assistant_content, "iteration": iteration})
        messages.append(
            {
                "role": "assistant",
                "content": assistant_content,
                "tool_calls": [
                    {
                        "id": tc["id"],
                        "type": "function",
                        "function": {
                            "name": tc["function_name"],
                            "arguments": json.dumps(tc["arguments"]),
                        },
                    }
                    for tc in tool_calls_pending
                ],
            }
        )

        # Emit tool_exec phase event for UI indicators (#1366)
        tool_names = [tc["function_name"] for tc in tool_calls_pending]
        yield AgentEvent(
            kind="phase",
            data={
                "phase": "tool_exec",
                "tool_count": len(tool_calls_pending),
                "tool_names": tool_names,
                "tool_summaries": [
                    _humanize_tool_brief(tc["function_name"], tc.get("arguments", {})) for tc in tool_calls_pending
                ],
                "iteration": iteration,
            },
        )

        # Execute tool calls in parallel
        _tools_start = time.monotonic()
        log_debug(
            logger,
            "agent_loop.tool_exec.start",
            lifecycle="start",
            phase="tool_exec",
            iteration=iteration,
            tool_count=len(tool_calls_pending),
            tool_names=tool_names,
        )
        _end_turn_requested = False  # (#1311) background task turn-yield
        if cancel_event and cancel_event.is_set():
            for tc in tool_calls_pending:
                cancelled_result = {"error": "Cancelled by user"}
                yield AgentEvent(
                    kind="tool_call_end",
                    data={
                        "id": tc["id"],
                        "tool_name": tc["function_name"],
                        "output": cancelled_result,
                        "status": "cancelled",
                        "iteration": iteration,
                        "execution_elapsed_seconds": time.monotonic() - _tools_start,
                        "timeout_seconds": _DEFAULT_TOOL_TIMEOUT,
                    },
                )
                messages.append({"role": "tool", "tool_call_id": tc["id"], "content": json.dumps(cancelled_result)})
        elif serialize_tools:
            # Serialized tool execution for workflow engine.
            # Tools execute one at a time so the pause signal can be checked
            # between each tool call. If the signal is set (by a workflow
            # approval callback), the loop exits BEFORE appending the paused
            # tool's result to messages — the paused result never enters
            # LLM-visible history. The assistant message and any earlier
            # successful tool results ARE in messages (appended before this
            # block). Full step isolation is handled by the workflow engine
            # (Phase 3) via session isolation per step.
            for tc in tool_calls_pending:
                tc, result, tool_status = await _execute_tool(tc, tool_executor, cancel_event)

                # Check pause signal BEFORE processing this tool's result.
                if pause_signal and pause_signal.is_set():
                    yield AgentEvent(
                        kind="workflow_pause",
                        data={
                            "tool_call_id": tc["id"],
                            "tool_name": tc["function_name"],
                            "tool_args": tc.get("arguments", {}),
                            "reason": "approval_required",
                            "iteration": iteration,
                        },
                    )
                    return

                yield AgentEvent(
                    kind="tool_call_end",
                    data={
                        "id": tc["id"],
                        "tool_name": tc["function_name"],
                        "output": result,
                        "status": tool_status,
                        "iteration": iteration,
                        "execution_elapsed_seconds": time.monotonic() - _tools_start,
                        "timeout_seconds": _DEFAULT_TOOL_TIMEOUT,
                    },
                )
                internal_keys = {
                    "_approval_decision",
                    "_old_content",
                    "_new_content",
                    "_context_trust",
                    "_context_origin",
                    "_end_turn",
                }
                if isinstance(result, dict):
                    if result.get("_end_turn"):
                        _end_turn_requested = True
                    if injection_detector is not None and injection_detector.enabled:
                        _tool_text = "\n".join(
                            v for k, v in result.items() if isinstance(v, str) and not k.startswith("_")
                        )
                        if _tool_text:
                            _inj_verdict = injection_detector.scan_tool_output(tc["function_name"], _tool_text)
                            if _inj_verdict.detected:
                                yield AgentEvent(
                                    kind="injection_detected",
                                    data={
                                        "tool_name": tc["function_name"],
                                        "technique": _inj_verdict.technique,
                                        "confidence": _inj_verdict.confidence,
                                        "detail": _inj_verdict.detail,
                                        "action": injection_detector.action,
                                    },
                                )
                                if injection_detector.action == "block":
                                    result = {
                                        "error": "Tool output blocked: prompt injection detected",
                                        "safety_blocked": True,
                                        "_approval_decision": "injection_blocked",
                                    }
                    context_trust = result.get("_context_trust")
                    if context_trust == "untrusted":
                        origin = result.get("_context_origin", "unknown")
                        for key in ("content", "result"):
                            if key in result and isinstance(result[key], str):
                                result[key] = wrap_untrusted(result[key], origin, "tool-result")
                                break
                    llm_result = {k: v for k, v in result.items() if k not in internal_keys}
                else:
                    llm_result = result
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "content": compact_tool_output(llm_result, max_chars=tool_output_max_chars),
                    }
                )
            total_tool_calls += len(tool_calls_pending)
            consecutive_text_only = 0
            log_debug(
                logger,
                "agent_loop.tool_exec.success",
                lifecycle="success",
                phase="tool_exec",
                iteration=iteration,
                tool_count=len(tool_calls_pending),
                execution_mode="serialized",
                _started_at=_tools_start,
            )
        else:
            # Parallel tool execution (default — existing behavior, untouched)
            tasks = [asyncio.create_task(_execute_tool(tc, tool_executor, cancel_event)) for tc in tool_calls_pending]
            for coro in asyncio.as_completed(tasks):
                tc, result, tool_status = await coro
                yield AgentEvent(
                    kind="tool_call_end",
                    data={
                        "id": tc["id"],
                        "tool_name": tc["function_name"],
                        "output": result,
                        "status": tool_status,
                        "iteration": iteration,
                        "execution_elapsed_seconds": time.monotonic() - _tools_start,
                        "timeout_seconds": _DEFAULT_TOOL_TIMEOUT,
                    },
                )
                # Strip internal metadata before sending to the LLM
                # _approval_decision: safety gate audit field
                # _old_content/_new_content: large strings for diff rendering only
                # _context_trust/_context_origin: trust classification metadata
                # _end_turn: background task turn-yield signal (#1311)
                internal_keys = {
                    "_approval_decision",
                    "_old_content",
                    "_new_content",
                    "_context_trust",
                    "_context_origin",
                    "_end_turn",
                }
                if isinstance(result, dict):
                    if result.get("_end_turn"):
                        _end_turn_requested = True
                    # Scan untrusted tool output for prompt injection
                    if injection_detector is not None and injection_detector.enabled:
                        # Collect all string values from the result (covers content,
                        # result, stdout, stderr, text — any tool output shape)
                        _tool_text = "\n".join(
                            v for k, v in result.items() if isinstance(v, str) and not k.startswith("_")
                        )
                        if _tool_text:
                            _inj_verdict = injection_detector.scan_tool_output(tc["function_name"], _tool_text)
                            if _inj_verdict.detected:
                                yield AgentEvent(
                                    kind="injection_detected",
                                    data={
                                        "tool_name": tc["function_name"],
                                        "technique": _inj_verdict.technique,
                                        "confidence": _inj_verdict.confidence,
                                        "detail": _inj_verdict.detail,
                                        "action": injection_detector.action,
                                    },
                                )
                                if injection_detector.action == "block":
                                    result = {
                                        "error": "Tool output blocked: prompt injection detected",
                                        "safety_blocked": True,
                                        "_approval_decision": "injection_blocked",
                                    }
                    # Wrap untrusted tool results in a defensive envelope
                    context_trust = result.get("_context_trust")
                    if context_trust == "untrusted":
                        origin = result.get("_context_origin", "unknown")
                        for key in ("content", "result"):
                            if key in result and isinstance(result[key], str):
                                result[key] = wrap_untrusted(result[key], origin, "tool-result")
                                break
                    llm_result = {k: v for k, v in result.items() if k not in internal_keys}
                else:
                    llm_result = result
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "content": compact_tool_output(llm_result, max_chars=tool_output_max_chars),
                    }
                )
            total_tool_calls += len(tool_calls_pending)
            consecutive_text_only = 0
            log_debug(
                logger,
                "agent_loop.tool_exec.success",
                lifecycle="success",
                phase="tool_exec",
                iteration=iteration,
                tool_count=len(tool_calls_pending),
                execution_mode="parallel",
                _started_at=_tools_start,
            )

        if cancel_event and cancel_event.is_set():
            yield AgentEvent(kind="done", data={"stop_reason": "cancelled", "iteration": iteration})
            return

        # Background task turn-yield (#1311): if any tool result had
        # _end_turn, emit done and break to the queue checkpoint instead
        # of calling the LLM again.
        if _end_turn_requested:
            log_debug(
                logger,
                "agent_loop.queue.skip",
                lifecycle="skip",
                phase="queue_checkpoint",
                reason="yielded_to_queue",
                iteration=iteration,
            )
            active_skill_policy.set(None)
            yield AgentEvent(kind="done", data={"stop_reason": "yielded_to_queue", "iteration": iteration})
            if message_queue is not None:
                try:
                    queued_msg = message_queue.get_nowait()
                    _turn_policy = queued_msg.pop("_skill_policy", None)
                    active_skill_policy.set(_turn_policy)
                    queue_depth = message_queue.qsize()
                    messages.append(queued_msg)
                    yield AgentEvent(
                        kind="queued_message",
                        data={**queued_msg, "position": 1, "queue_depth": queue_depth},
                    )
                    _end_turn_requested = False
                    continue
                except asyncio.QueueEmpty:
                    pass
            return

        # Auto-plan suggestion: one-shot event when tool calls cross the threshold.
        if (
            auto_plan_threshold > 0
            and not auto_plan_suggested
            and total_tool_calls >= auto_plan_threshold
            and not (cancel_event and cancel_event.is_set())
        ):
            auto_plan_suggested = True
            yield AgentEvent(kind="auto_plan_suggest", data={"tool_calls": total_tool_calls, "iteration": iteration})

        # Enforce narration cadence: inject an ephemeral prompt to force a progress update.
        # The injected message is removed from history immediately after the narration response
        # so it does not pollute the conversation context for subsequent tool calls.
        if (
            narration_cadence > 0
            and total_tool_calls > 0
            and total_tool_calls % narration_cadence == 0
            and not (cancel_event and cancel_event.is_set())
        ):
            yield AgentEvent(kind="thinking", data={})
            narration_idx = len(messages)
            messages.append({"role": "user", "content": _NARRATION_PROMPT})
            try:
                async for event in ai_service.stream_chat(
                    messages,
                    cancel_event=cancel_event,
                    extra_system_prompt=extra_system_prompt,
                ):
                    if event["event"] == "token":
                        yield AgentEvent(kind="token", data={**event["data"], "iteration": iteration})
                    elif event["event"] in ("done", "error"):
                        break
            except Exception:
                logger.exception("Narration request failed; continuing without update")
            finally:
                # Remove by index — safer than content equality if stream_chat mutated messages
                if len(messages) > narration_idx:
                    messages.pop(narration_idx)

        assistant_content = ""

    yield AgentEvent(
        kind="error",
        data={
            "message": f"Max iterations ({max_iterations}) reached",
            "code": "max_iterations",
            "iteration": iteration,
        },
    )
