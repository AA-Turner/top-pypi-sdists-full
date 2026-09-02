from __future__ import annotations

import asyncio
import difflib
import json
import logging
import time
import traceback as tb
from collections.abc import Awaitable, Iterable
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

from matrx_utils import detached_task, vcprint
from pydantic import BaseModel

from ._db_log import db_log_event as _db_log
from ._debug_log import is_verbose as _debug_verbose
from ._debug_log import log_event as _debug_log
from .guardrails import GuardrailEngine
from .lifecycle import ToolLifecycleManager
from .logger import ToolExecutionLogger
from .models import ToolContext, ToolDefinition, ToolError, ToolResult, ToolType
from .registry import ToolRegistry
from .result_gate import apply_size_gate, tool_kind_label
from .streaming import ToolStreamManager

logger = logging.getLogger(__name__)

TOOL_INPUT_CONTRACT_DRIFT_KIND = "tool_input_contract_drift"
TOOL_OUTPUT_CONTRACT_DRIFT_KIND = "tool_output_contract_drift"
CONTEXT_PATCH_NO_MATCH_KIND = "context_patch_no_match"
TOOL_ARGUMENT_VALIDATION_FAILED_KIND = "tool_argument_validation_failed"
TOOL_EXECUTION_FAILED_KIND = "tool_execution_failed"
TOOL_RESULT_KIND_MISSING_KIND = "tool_result_kind_missing"
TOOL_RESULT_SIZE_UNMANAGED_KIND = "tool_result_size_unmanaged"


def _is_expected_domain_failure(*, tool_name: str, error_type: str) -> bool:
    """Return true for deliberate tool refusals that are not operational errors."""
    if error_type.lower() in {
        "auth_required",
        "invalid_arguments",
        "missing_context",
        "not_allowed",
        "not_found",
        "validation",
    }:
        return True
    return (tool_name, error_type) in {
        ("code_execute_python", "python_error"),
        ("context", "context_not_attached"),
        ("context_patch", "patch_no_match"),
        ("context", "context_create_disabled"),
        # The browser control plane returns this typed refusal when the caller's
        # session lost a lifecycle CAS or is already terminal.  It is actionable
        # tool feedback (reattach/navigate), not an executor implementation fault.
        ("cloud_browser", "run_state_conflict"),
        ("shell_execute", "exit_code"),
        ("shell_python", "exit_code"),
    }


async def _capture_context_patch_no_match(*, ctx: ToolContext) -> None:
    """Capture a failed optimistic context edit without retaining document text."""
    from matrx_connect.streaming.error_capture import capture_error

    exc = RuntimeError("Context patch could not find its requested anchor")
    await capture_error(
        exc,
        kind=CONTEXT_PATCH_NO_MATCH_KIND,
        request_id=ctx.request_id or None,
        user_id=ctx.user_id or None,
        conversation_id=ctx.conversation_id or None,
        route="tool_executor.context_patch",
        error_type="PatchNoMatch",
        context={"tool_name": "context_patch", "call_id": ctx.call_id, "retryable": True},
    )


async def _capture_tool_argument_validation_failed(
    *,
    ctx: ToolContext,
    tool_name: str,
) -> None:
    """Capture a rejected tool call without retaining model-supplied arguments."""
    from matrx_connect.streaming.error_capture import capture_error

    exc = RuntimeError(f"Tool arguments failed declared validation: {tool_name}")
    await capture_error(
        exc,
        kind=TOOL_ARGUMENT_VALIDATION_FAILED_KIND,
        request_id=ctx.request_id or None,
        user_id=ctx.user_id or None,
        conversation_id=ctx.conversation_id or None,
        route="tool_executor.argument_validation",
        error_type="ToolArgumentValidationError",
        context={"tool_name": tool_name, "call_id": ctx.call_id},
    )


async def _capture_tool_input_contract_drift(
    *,
    ctx: ToolContext,
    tool_name: str,
    input_kind: str,
    error_count: int,
) -> None:
    """Durably capture a shadow-contract mismatch without retaining tool input."""
    from matrx_connect.streaming.error_capture import capture_error

    exc = RuntimeError(
        f"Tool input disagreed with its Content IR contract: {tool_name} "
        f"({error_count} validation error(s))"
    )
    await capture_error(
        exc,
        kind=TOOL_INPUT_CONTRACT_DRIFT_KIND,
        request_id=ctx.request_id or None,
        user_id=ctx.user_id or None,
        conversation_id=ctx.conversation_id or None,
        route="tool_executor.content_ir_input",
        error_type="ToolInputContractDrift",
        context={
            "tool_name": tool_name,
            "input_kind": input_kind,
            "error_count": error_count,
        },
    )


async def _capture_tool_output_contract_drift(
    *,
    ctx: ToolContext,
    tool_name: str,
    output_kind: str,
    error_count: int,
) -> None:
    """Durably capture a successful result that violates its output contract."""
    from matrx_connect.streaming.error_capture import capture_error

    exc = RuntimeError(
        f"Tool output disagreed with its Content IR contract: {tool_name} "
        f"({error_count} validation error(s))"
    )
    await capture_error(
        exc,
        kind=TOOL_OUTPUT_CONTRACT_DRIFT_KIND,
        request_id=ctx.request_id or None,
        user_id=ctx.user_id or None,
        conversation_id=ctx.conversation_id or None,
        route="tool_executor.content_ir_output",
        error_type="ToolOutputContractDrift",
        context={
            "tool_name": tool_name,
            "output_kind": output_kind,
            "error_count": error_count,
        },
    )


async def _capture_tool_result_kind_missing(
    *, ctx: ToolContext, tool_name: str, output_kind: str
) -> None:
    """Capture a successful declared-kind result that omitted its discriminator."""
    from matrx_connect.streaming.error_capture import capture_error

    await capture_error(
        RuntimeError(f"Declared tool result kind was missing: {tool_name}"),
        kind=TOOL_RESULT_KIND_MISSING_KIND,
        request_id=ctx.request_id or None,
        user_id=ctx.user_id or None,
        conversation_id=ctx.conversation_id or None,
        route="tool_executor.content_ir_output",
        error_type="ToolResultKindMissing",
        context={"tool_name": tool_name, "output_kind": output_kind},
    )


async def _capture_tool_result_size_unmanaged(
    *, ctx: ToolContext, tool_name: str
) -> None:
    """Capture an owned tool that reached the universal blunt size gate."""
    from matrx_connect.streaming.error_capture import capture_error

    await capture_error(
        RuntimeError(f"Owned tool result exceeded its unmanaged size limit: {tool_name}"),
        kind=TOOL_RESULT_SIZE_UNMANAGED_KIND,
        request_id=ctx.request_id or None,
        user_id=ctx.user_id or None,
        conversation_id=ctx.conversation_id or None,
        route="tool_executor.result_gate",
        error_type="ToolResultSizeUnmanaged",
        context={"tool_name": tool_name, "call_id": ctx.call_id},
    )


async def _capture_tool_execution_failed(
    *, ctx: ToolContext, tool_name: str, error_type: str
) -> None:
    """Capture an unexpected failed tool result without retaining args or output."""
    from matrx_connect.streaming.error_capture import capture_error

    await capture_error(
        RuntimeError(f"Tool execution failed: {tool_name}"),
        kind=TOOL_EXECUTION_FAILED_KIND,
        request_id=ctx.request_id or None,
        user_id=ctx.user_id or None,
        conversation_id=ctx.conversation_id or None,
        route="tool_executor.execution",
        error_type=error_type,
        context={"tool_name": tool_name, "call_id": ctx.call_id},
    )


# ── Client-delegated tool timing — the canonical durable contract ──────────────
# These two numbers govern client delegation and are the SINGLE SOURCE OF TRUTH;
# no UI surface defines its own answer deadline. A delegated call's honest state
# is ``cx_tool_call.status='delegated'`` + ``cx_user_request.status='paused'`` —
# a user may sit in it for seconds, minutes, hours, or weeks, and the platform
# does NOT try to control that. The only role of a timeout here is far-future
# cleanup of genuinely-abandoned conversations; a late answer ALWAYS resumes
# (see ``submit_tool_results``' timeout_sweep supersession).
#
# DELEGATED_CALL_ABANDON_AFTER_SECONDS — the durable ledger TTL stamped on
#   ``cx_tool_call.expires_at``. The lifecycle sweep flips a row past this to a
#   timeout terminal state purely so an abandoned conversation doesn't keep a
#   'delegated' row outstanding forever. It is NOT a user-facing answer deadline.
#   Override per-tool via the ``tools.max_client_wait_seconds`` column when a
#   specific tool legitimately needs a tighter bound.
DELEGATED_CALL_ABANDON_AFTER_SECONDS: int = 30 * 24 * 60 * 60  # 30 days

# _DELEGATED_DISPATCH_TIMEOUT_SECONDS — pure HANG-backstop for the delegated
#   DISPATCH itself (queue the 'delegated' UPDATE + ``coordinator.finalize()`` +
#   ``tool_delegated`` emit). It returns in milliseconds normally and NEVER waits
#   for the user. It must sit comfortably ABOVE ``finalize()``'s own internal
#   worst case — ``finalize`` drains each in-flight commit serially at
#   ``_DRAIN_TIMEOUT_SECONDS`` (30s) plus a ``_COMMIT_HARD_DEADLINE_SECONDS``
#   (60s) current flush, so a slow-but-SUCCESSFUL finalize must not be killed
#   here (that would overwrite the durable 'delegated' row with an error and
#   reopen the delegation loop). 1h matches the prior known-good value; it only
#   ever fires if the emit/commit genuinely deadlocks. DECOUPLED from the
#   abandonment TTL so a long per-tool wait can never hold the request task open.
_DELEGATED_DISPATCH_TIMEOUT_SECONDS: float = 60.0 * 60.0  # 1 hour

# ── Unknown-tool hint bounds — always on, tune here (never a flag) ─────────────
# The db_hints pattern applied to tool names: a miss returns did-you-mean +
# a bounded option list, never an unbounded registry dump (context bloat).
UNKNOWN_TOOL_LIST_CAP = 25  # max tool names listed in the error message
_CONFIDENT_SUGGESTION_RATIO = 0.85  # difflib ratio for a "Retry with tool 'X'" action


async def _await_must_complete(
    operation: Awaitable[ToolResult],
    *,
    timeout_seconds: float,
    stream: ToolStreamManager,
    tool_name: str,
) -> tuple[ToolResult, asyncio.CancelledError | None]:
    task = asyncio.create_task(operation, name=f"must_complete_tool:{tool_name}")
    cancellation: asyncio.CancelledError | None = None
    try:
        result = await asyncio.wait_for(
            asyncio.shield(task),
            timeout=timeout_seconds,
        )
        return result, None
    except TimeoutError:
        vcprint(
            f"[ToolExecutor] Tool '{tool_name}' crossed its {timeout_seconds:.0f}s "
            "soft timeout, but must_complete=True — waiting for the real result. "
            "The execution was NOT cancelled and MUST NOT be retried.",
            color="yellow",
        )
        detached_task(
            stream.progress(
                "Still running — this paid operation will continue until the "
                "provider returns a terminal result.",
                data={
                    "soft_timeout_seconds": timeout_seconds,
                    "must_complete": True,
                    "retry_allowed": False,
                },
            ),
            name=f"must_complete_progress:{tool_name}",
        )
    except asyncio.CancelledError as exc:
        if task.done():
            return task.result(), None
        cancellation = exc
        vcprint(
            f"[ToolExecutor] Cancellation reached must-complete tool '{tool_name}'. "
            "Finishing the in-flight operation before propagating cancellation.",
            color="yellow",
        )

    while True:
        try:
            result = await asyncio.shield(task)
            return result, cancellation
        except asyncio.CancelledError as exc:
            if task.done():
                return task.result(), cancellation
            cancellation = cancellation or exc
            vcprint(
                f"[ToolExecutor] Repeated cancellation ignored while must-complete "
                f"tool '{tool_name}' is still in flight.",
                color="red",
            )


def build_unknown_tool_hint(
    called: str,
    *,
    vocabulary: Iterable[str],
    active_tools: Iterable[str] | None = None,
    cap: int = UNKNOWN_TOOL_LIST_CAP,
) -> tuple[str, str]:
    """Build ``(message, suggested_action)`` for an unregistered tool name.

    Fuzzy-matches ``called`` against every internal name in ``vocabulary`` AND
    its wire spelling (``:`` → ``__`` — the model may only ever have seen wire
    names), mapping matches back to internal names. Lists ``active_tools``
    (bounded, closest-first) so the model has a real vocabulary to pick from.
    Pure function — unit-testable without an executor.
    """
    from matrx_utils import did_you_mean, format_options

    from matrx_ai.config.wire_names import to_wire_name

    # wire/internal spelling → internal name (identity for colon-free names).
    spelling_to_internal: dict[str, str] = {}
    for name in vocabulary:
        spelling_to_internal.setdefault(name, name)
        spelling_to_internal.setdefault(to_wire_name(name), name)

    matched_spellings = did_you_mean(called, spelling_to_internal.keys())
    # Present suggestions in WIRE form — that is the spelling the model saw
    # declared and the only one it should call (wire-name seam rules).
    suggestions: list[str] = []
    for spelling in matched_spellings:
        wire = to_wire_name(spelling_to_internal[spelling])
        if wire not in suggestions:
            suggestions.append(wire)

    lines = [f"Tool '{called}' is not registered."]
    confident: str | None = None
    if suggestions:
        if len(suggestions) == 1:
            lines.append(f"Did you mean '{suggestions[0]}'?")
        else:
            lines.append(f"Did you mean one of: {format_options(suggestions, 5)}?")
        top_ratio = difflib.SequenceMatcher(None, called, suggestions[0]).ratio()
        if len(suggestions) == 1 or top_ratio >= _CONFIDENT_SUGGESTION_RATIO:
            confident = suggestions[0]

    active = sorted({to_wire_name(n) for n in active_tools}) if active_tools is not None else []
    if active:
        # Closest-first so a truncated list still leads with the likely target.
        active.sort(
            key=lambda n: difflib.SequenceMatcher(None, called, n).ratio(),
            reverse=True,
        )
        lines.append(f"Available tools: {format_options(active, cap)}.")

    if confident:
        action = f"Retry with tool '{confident}'."
    elif active:
        action = "Pick a tool from the available list and retry with its exact name."
    else:
        action = "Check the tool name and try again. Use a valid tool from the available set."
    return " ".join(lines), action


async def warn_member_depth_exhausted(
    ctx: ToolContext, tool_def: ToolDefinition, tool_name: str
) -> None:
    """Emit a loud `member_depth_exhausted` warning for a depth-refused agent tool.

    D-39: a projected member refused at recursion depth is TRUNCATED DELEGATION —
    the calling orchestrator answers WITHOUT this member and may quietly absorb
    the refusal ToolResult. That result is the model's signal; this warning is
    the HUMAN's, so the truncation is never silent on the wire. Additive only —
    a failure to emit never breaks the run (it screams to the console instead).
    """
    try:
        emitter = ctx.emitter
        if emitter is None:
            return
        from matrx_connect.context.events import WarningPayload

        await emitter.send_warning(
            WarningPayload(
                code="member_depth_exhausted",
                system_message=(
                    f"Projected agent tool '{tool_name}' (agent "
                    f"{tool_def.prompt_id}) refused: agent-nesting depth "
                    f"{ctx.recursion_depth} has reached its ceiling of "
                    f"{tool_def.max_recursion_depth}."
                ),
                user_message=(
                    "A team member couldn't be called because the delegation "
                    f"chain is already {ctx.recursion_depth} levels deep "
                    f"(limit {tool_def.max_recursion_depth}). The answer may "
                    "be missing that member's contribution."
                ),
                level="medium",
                recoverable=True,
                metadata={
                    "tool_name": tool_name,
                    "agent_id": tool_def.prompt_id,
                    "depth": ctx.recursion_depth,
                    "ceiling": tool_def.max_recursion_depth,
                },
            )
        )
    except Exception as warn_exc:
        vcprint(
            f"[executor] member_depth_exhausted warning failed to emit: {warn_exc}",
            color="red",
        )


class ToolExecutor:
    """The single entry point for all tool executions.

    Replaces:
      - tool_registry.execute_tool_call()
      - tool_registry.execute_tool()
      - All thin wrapper functions in mcp_server/tools/

    Every tool — local, external MCP, agent — goes through the same pipeline:
      1. Resolve tool definition from registry
      2. Build ToolContext
      3. Validate arguments
      4. Check guardrails
      5. Stream "started" to client
      6. Execute (dispatch by tool type)
      7. Stream "completed" or "error" to client
      8. Log execution (fire-and-forget)
      9. Persist output if flagged
      10. Return result
    """

    def __init__(
        self,
        registry: ToolRegistry,
        guardrails: GuardrailEngine | None = None,
        execution_logger: ToolExecutionLogger | None = None,
        lifecycle: ToolLifecycleManager | None = None,
    ):
        self.registry = registry
        self.guardrails = guardrails or GuardrailEngine()
        self.execution_logger = execution_logger or ToolExecutionLogger()
        self.lifecycle = lifecycle or ToolLifecycleManager.get_instance()

    # ------------------------------------------------------------------
    # Context builder
    # ------------------------------------------------------------------

    @staticmethod
    def build_context(
        *,
        call_id: str,
        tool_name: str,
        iteration: int = 0,
        recursion_depth: int = 0,
        cost_budget_remaining: float | None = None,
        calls_remaining: int | None = None,
    ) -> ToolContext:
        return ToolContext(
            call_id=call_id,
            tool_name=tool_name,
            iteration=iteration,
            recursion_depth=recursion_depth,
            cost_budget_remaining=cost_budget_remaining,
            calls_remaining_this_conversation=calls_remaining,
        )

    # ------------------------------------------------------------------
    # Inbound wire-name normalization
    # ------------------------------------------------------------------

    def _normalize_called_name(self, called: str) -> str:
        """Map a model-called (wire) tool name back to its internal name.

        Providers reject ':' in tool names, so colon-namespaced internal
        names (``bundle:list_supabase``) are declared to the model in wire
        form (``bundle__list_supabase`` — see ``matrx_ai.config.wire_names``).
        This reverses that transform for dispatch.

        A name that resolves as-is (projected tool, alias-map entry, or
        registry hit) is returned unchanged — direct identity always wins,
        so plain names containing ``__`` can never be corrupted. Only when
        direct resolution fails do we look for an internal name whose wire
        form matches what the model said.
        """
        from matrx_ai.config.wire_names import WIRE_SEP, resolve_wire_name
        from matrx_ai.tools.agent_projection import lookup_projected_tool
        from matrx_ai.tools.tool_aliases import get_alias_map, lookup_canonical

        if WIRE_SEP not in called:
            return called
        if (
            lookup_projected_tool(called) is not None
            or lookup_canonical(called) is not None
            or self.registry.get(called) is not None
        ):
            return called
        matched = resolve_wire_name(called, get_alias_map().keys())
        if matched is None:
            matched = resolve_wire_name(called, self.registry.list_tool_names())
        return matched if matched is not None else called

    # ------------------------------------------------------------------
    # Pre-dispatch rejection recorder
    # ------------------------------------------------------------------

    async def _record_rejected(
        self,
        ctx: ToolContext,
        *,
        tool_name: str,
        arguments: dict[str, Any],
        result: ToolResult,
        tool_type: str = "local",
        canonical_name: str | None = None,
    ) -> None:
        """Persist a terminal cx_tool_call row for a call rejected before
        dispatch. Best-effort — telemetry must never block dispatch, so a
        failure here is logged inside the logger and swallowed here."""
        try:
            await self.execution_logger.log_rejected(
                ctx,
                tool_name=tool_name,
                arguments=arguments,
                result=result,
                tool_type=tool_type,
                canonical_name=canonical_name,
            )
        except Exception as exc:
            vcprint(
                f"[ToolExecutor] Failed to record rejected tool call "
                f"'{tool_name}' ({getattr(result.error, 'error_type', '?')}): {exc}",
                color="red",
            )

    async def _reject_invalid_arguments(
        self,
        *,
        ctx: ToolContext,
        tool_name: str,
        as_called: str,
        canonical_name: str,
        tool_def: ToolDefinition,
        arguments: dict[str, Any],
        msg: str,
        dispatch_kind: str,
        started_at: float,
    ) -> tuple[dict[str, Any], ToolResult]:
        """Terminal reject for a pre-dispatch argument-validation failure —
        error_type='invalid_arguments' (fault_domain model_error), recorded to
        both trace sinks with the full args (forensics: 'what did the model
        actually send?') and streamed to the client."""
        await _capture_tool_argument_validation_failed(
            ctx=ctx,
            tool_name=canonical_name,
        )
        result = ToolResult(
            success=False,
            error=ToolError(
                error_type="invalid_arguments",
                message=f"Invalid arguments for '{tool_name}': {msg}",
                suggested_action=(
                    "Re-read the tool's input schema and call it again with "
                    "exactly the documented arguments (no extra keys)."
                ),
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name=tool_name,
            call_id=ctx.call_id,
        )
        _conv_full = getattr(ctx, "conversation_id", None)
        try:
            _args_str = json.dumps(arguments, default=str)
        except Exception:
            _args_str = str(arguments)
        _debug_log(
            "FAIL",
            tool=tool_name,
            kind=dispatch_kind,
            ms=int((time.time() - started_at) * 1000),
            args=_args_str,
            err_type="invalid_arguments",
            err_msg=msg,
            conv=(_conv_full or "")[:8],
            call=ctx.call_id,
        )
        detached_task(
            _db_log(
                "FAIL",
                tool_name=tool_name,
                kind=dispatch_kind,
                args=arguments,
                err_type="invalid_arguments",
                err_msg=msg,
                conversation_id=_conv_full,
                call_id=ctx.call_id,
                user_id=getattr(ctx, "user_id", None),
            ),
            name="tool_db_log_invalid_args",
        )
        result.compute_duration()
        await self._record_rejected(
            ctx,
            tool_name=as_called,
            arguments=arguments,
            result=result,
            tool_type=tool_def.tool_type.value,
            canonical_name=canonical_name,
        )
        stream = ToolStreamManager(ctx.emitter, ctx.call_id, tool_name)
        await stream.error(
            f"Invalid arguments for '{tool_name}': {msg}",
            error_type="invalid_arguments",
        )
        return result.to_tool_result_content(), result

    # ------------------------------------------------------------------
    # Completion-log persistence (coordinator-aware)
    # ------------------------------------------------------------------

    async def _persist_tool_outcome(self, coro: Any, *, coordinator: Any, name: str) -> None:
        """Persist a tool-completion log write (log_completed / log_error).

        WHEN A REQUEST COORDINATOR IS PRESENT (the in-request path) the write
        is a purely IN-MEMORY ``coordinator.queue()`` (Session.defer_update) —
        it does NO database I/O. So we run it INLINE and synchronously, which
        deterministically lands the UPDATE in the coordinator's current Session
        BEFORE the tool returns to the loop. It then coalesces with the row's
        INSERT and flushes at the turn barrier exactly like any normal tool.

        This replaces a fire-and-forget ``detached_task``. That detached write
        raced the request's final drain + ``seal()``: for a child-agent-forking
        tool (``agent_call``) — whose ``child_agent_context`` force-finalizes the
        parent coordinator (``pre_fan_out``) and thereby splits the row's INSERT
        off from its UPDATE into separate flush cycles — the late, untracked
        completion write landed AFTER ``seal()`` as a one-shot that request
        teardown never ran. The row stayed ``status='running'`` and the watchdog
        later flipped it to ``error`` (the observed 2026-06-20 agent_call bug).
        The detached_task was only ever needed to keep a REAL DB write off the
        parent's transaction connection — but with a coordinator there is no DB
        write here, just an in-memory defer, so the isolation is moot.

        WITH NO COORDINATOR (a true out-of-request background dispatch) the write
        IS a real DB UPDATE (``update_item_fields``) that must run in a fresh
        contextvars Context so it doesn't dispatch onto a parent transaction
        connection. ``detached_task`` provides that isolation, but the task is
        awaited: a short-lived CLI must not exit after a successful tool result
        while its ledger row is still ``running``.
        """
        if coordinator is not None:
            try:
                await coro
            except Exception as exc:  # noqa: BLE001 — telemetry must never break dispatch
                vcprint(
                    f"[ToolExecutor] inline completion-log write failed: "
                    f"{type(exc).__name__}: {exc}",
                    color="red",
                )
        else:
            try:
                await detached_task(coro, name=name)
            except Exception as exc:  # noqa: BLE001 — telemetry must never break dispatch
                vcprint(
                    f"[ToolExecutor] isolated completion-log write failed: "
                    f"{type(exc).__name__}: {exc}",
                    color="red",
                )

    # ------------------------------------------------------------------
    # Single execution
    # ------------------------------------------------------------------

    async def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        ctx: ToolContext,
        client_tools: frozenset[str] | None = None,
        allowed_tools: frozenset[str] | None = None,
    ) -> tuple[dict[str, Any], ToolResult]:
        """Execute a single tool call through the full pipeline.

        Two-phase logging:
          1. INSERT cx_tool_call with status='running' immediately
          2. UPDATE with output/error when done

        Parameters
        ----------
        allowed_tools:
            When provided, the tool_name must be in this set or execution is
            rejected.  ``None`` means no restriction.  Resolved from the tools
            that were actually sent to the model in the current API call.

        Returns ``(tool_result_content_dict, full_result)``.
        """
        started_at = time.time()

        # --- Wire-name normalization (inbound seam) ---
        # Providers reject ':' in tool names, so declarations go out in wire
        # form (':' → '__', see matrx_ai.config.wire_names) and the model
        # calls the wire name (e.g. 'bundle__list_supabase'). Reverse the
        # transform ONCE, here, so the allowlist, alias map, registry lookup,
        # guardrails and persistence all operate on the internal name. The
        # as-called (wire) spelling is preserved for the trace columns.
        as_called = tool_name
        tool_name = self._normalize_called_name(tool_name)
        if tool_name != as_called:
            vcprint(
                f"[ToolExecutor] wire-name normalized: {as_called!r} → {tool_name!r}",
                color="cyan",
            )
            # Handlers read ctx.tool_name (e.g. the bundle lister parses its
            # bundle from it) — it must carry the internal name.
            ctx = ctx.model_copy(update={"tool_name": tool_name})

        # --- Allowlist guard ---
        # Reject any tool the model was not explicitly given in this request.
        # This prevents the model from invoking arbitrary registered tools by
        # guessing their names (accidental or adversarial).
        if (
            allowed_tools is not None
            and tool_name not in allowed_tools
            and as_called not in allowed_tools
        ):
            vcprint(
                {
                    "tool_name": tool_name,
                    "call_id": ctx.call_id,
                    "allowed_tools": sorted(allowed_tools),
                },
                f"[ToolExecutor] Tool '{tool_name}' was not in the allowed set for this request",
                color="yellow",
            )
            result = ToolResult(
                success=False,
                error=ToolError(
                    error_type="not_allowed",
                    message=(
                        f"Tool '{tool_name}' was not provided to the model for this request "
                        "and cannot be executed."
                    ),
                    suggested_action="Only call tools that were listed in your available tools.",
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_name,
                call_id=ctx.call_id,
            )
            result.compute_duration()
            await self._record_rejected(
                ctx,
                tool_name=as_called,
                arguments=arguments,
                result=result,
                canonical_name=tool_name,
            )
            stream = ToolStreamManager(ctx.emitter, ctx.call_id, tool_name)
            await stream.error(
                f"Tool '{tool_name}' is not in the allowed set for this request.",
                error_type="not_allowed",
            )
            return result.to_tool_result_content(), result

        # --- Resolve tool ---
        # Lookup precedence (Step 2 of the redesign):
        #   1. Projected agent tools — synthetic ``custom_tool_N`` definitions
        #      live on AppContext.metadata['projected_agent_tools'] and never
        #      have a real DB row. Highest priority so concurrent requests
        #      don't collide on the same opaque name.
        #   2. tool_aliases map — bundle aliasing exposes a canonical tool
        #      under a bundle-prefixed name (e.g. 'cool_stuff:scrape_page' →
        #      'scraper:scrape_page'). Resolve through the map, then fetch
        #      the canonical from the registry.
        #   3. Direct registry lookup — back-compat for code paths that haven't
        #      populated the alias map, plus the identity case where exposed
        #      name equals canonical.
        from matrx_ai.tools.agent_projection import lookup_projected_tool
        from matrx_ai.tools.tool_aliases import lookup_canonical

        tool_def = lookup_projected_tool(tool_name)
        canonical_name: str = tool_name
        if tool_def is None:
            aliased = lookup_canonical(tool_name)
            if aliased is not None and aliased != tool_name:
                canonical_name = aliased
            tool_def = self.registry.get(canonical_name)
        if tool_def is None:
            vcprint(
                {
                    "tool_name": tool_name,
                    "call_id": ctx.call_id,
                    "registry_loaded": self.registry.loaded,
                    "registry_count": self.registry.count,
                    "available_tools": self.registry.list_tool_names()[:20],
                },
                f"[ToolExecutor] Tool '{tool_name}' not found in registry",
                color="red",
            )
            hint_message, hint_action = self._unknown_tool_hint(tool_name, allowed_tools)
            result = self._unknown_tool_result(
                tool_name,
                ctx.call_id,
                started_at,
                message=hint_message,
                suggested_action=hint_action,
            )
            result.compute_duration()
            await self._record_rejected(
                ctx,
                tool_name=as_called,
                arguments=arguments,
                result=result,
                canonical_name=tool_name,
            )
            stream = ToolStreamManager(ctx.emitter, ctx.call_id, tool_name)
            await stream.error(hint_message, error_type="not_found")
            return result.to_tool_result_content(), result

        # --- Pre-flight: viable executor check ---
        # Detects tools that have no live executor for the current request
        # context — the bug class where an agent has a tool whose only
        # client surface isn't connected, AND the server-side fallback
        # function_path is empty (handler not yet implemented). Without
        # this check the dispatch would either silently run on the wrong
        # executor (the original incident) or fail with a generic import
        # error mid-run.
        is_delegated_pre = bool(client_tools and tool_name in client_tools)
        # Captured for the single OK/FAIL line emitted at completion —
        # cheaper than re-deriving from client_tools at result time.
        _dispatch_kind = "DELEGATE" if is_delegated_pre else "SERVER"

        # Schema-proven discriminator alias recovery runs before the durable
        # tool row and delegated event are written, so every client receives
        # the canonical shape. This is generic (not a `user`-tool special
        # case): it fires only when the published type.enum accepts the value
        # and the schema does not own an `action` field. Loud on every fire.
        from matrx_ai.tools._dispatch_util import recover_action_type_alias

        _alias_recovered = recover_action_type_alias(arguments, tool_def.parameters)
        if _alias_recovered is not None:
            arguments = _alias_recovered
            logger.warning(
                "[ToolExecutor] recovered discriminator alias action→type for tool %r",
                tool_name,
            )
            vcprint(
                f"[ToolExecutor] RECOVERED {tool_name}: `action` was accepted as "
                "the schema-proven `type` alias.",
                color="yellow",
            )
            _debug_log(
                "ALIAS_RECOVERED",
                tool=tool_name,
                alias="action_to_type",
                conv=(getattr(ctx, "conversation_id", None) or "")[:8],
                call=ctx.call_id,
            )
            detached_task(
                _db_log(
                    "ALIAS_RECOVERED",
                    tool_name=tool_name,
                    kind=_dispatch_kind,
                    args=arguments,
                    conversation_id=getattr(ctx, "conversation_id", None),
                    call_id=ctx.call_id,
                    user_id=getattr(ctx, "user_id", None),
                    metadata={"alias": "action_to_type"},
                ),
                name="tool_db_log_alias_recovered",
            )

        # --- Admin-only gate (defense-in-depth, the hard runtime boundary) ---
        # A tool marked admin_only (e.g. the cross-user `sql` tool) must NEVER execute
        # for a non-admin caller, no matter how it entered the toolset. The injection
        # funnel filters these out for non-admins, but this backstop guarantees it even
        # if a misconfigured agent or a path that bypasses the funnel slips one through.
        if getattr(tool_def, "admin_only", False):
            from matrx_connect import get_app_context

            try:
                _is_admin = bool(getattr(get_app_context(), "is_admin", False))
            except Exception:
                _is_admin = False
            if not _is_admin:
                _admin_msg = (
                    f"Tool '{tool_name}' is admin-only and cannot be run by a non-admin caller."
                )
                result = ToolResult(
                    success=False,
                    error=ToolError(error_type="admin_only", message=_admin_msg),
                    started_at=started_at,
                    completed_at=time.time(),
                    tool_name=tool_name,
                    call_id=ctx.call_id,
                )
                _conv_full = getattr(ctx, "conversation_id", None)
                _debug_log(
                    "FAIL",
                    tool=tool_name,
                    kind=_dispatch_kind,
                    ms=int((time.time() - started_at) * 1000),
                    err_type="admin_only",
                    err_msg="non-admin caller",
                    conv=(_conv_full or "")[:8],
                    call=ctx.call_id,
                )
                detached_task(
                    _db_log(
                        "FAIL",
                        tool_name=tool_name,
                        kind=_dispatch_kind,
                        args=arguments,
                        err_type="admin_only",
                        err_msg="non-admin caller",
                        conversation_id=_conv_full,
                        call_id=ctx.call_id,
                        user_id=getattr(ctx, "user_id", None),
                    ),
                    name="tool_db_log_admin_only",
                )
                result.compute_duration()
                await self._record_rejected(
                    ctx,
                    tool_name=as_called,
                    arguments=arguments,
                    result=result,
                    tool_type=tool_def.tool_type.value,
                    canonical_name=canonical_name,
                )
                stream = ToolStreamManager(ctx.emitter, ctx.call_id, tool_name)
                await stream.error(_admin_msg, error_type="admin_only")
                return result.to_tool_result_content(), result

        # --- Pre-flight: validate arguments against the declared schema ---
        # When a tool declares a Pydantic args model in code
        # (matrx_ai.tools.declared, populated by @tool / the generated
        # declarations), validate the model-supplied arguments BEFORE dispatch.
        # A failure here is the MODEL's fault — wrong / extra / missing /
        # mistyped args — and is reported as error_type="invalid_arguments"
        # (fault_domain "model_error"), cleanly distinct from a tool body that
        # throws (a "tool_defect"). Only server-executed, validate-enabled
        # declared tools are checked; client-delegated tools validate on the
        # client, and tools without a declared model are left untouched.
        coerced_fields: list[str] = []
        inferred_discriminator: tuple[str, str] | None = None
        if not is_delegated_pre:
            from matrx_ai.tools._dispatch_util import (
                coerce_stringified_containers,
                format_args_error,
                infer_missing_discriminator,
                remove_flattened_variant_extras,
            )
            from matrx_ai.tools.declared import get_effective_declared

            _declared = get_effective_declared(canonical_name)
            if _declared is not None and _declared.validate:
                # ── Missing action/command inference (before validate) ───────
                # A rejected call still costs a full provider turn. When the
                # discriminator is omitted but variant-unique fields uniquely
                # identify the action, fill it in. Loud on every fire.
                _infer = infer_missing_discriminator(arguments or {}, _declared.args_model)
                if _infer.kind == "inferred" and _infer.args is not None:
                    arguments = _infer.args
                    inferred_discriminator = (
                        _infer.discriminator or "action",
                        _infer.tag or "",
                    )
                    _disc_f, _disc_t = inferred_discriminator
                    logger.warning(
                        "[ToolExecutor] inferred missing %s=%r for tool %r "
                        "from variant-unique fields",
                        _disc_f,
                        _disc_t,
                        tool_name,
                    )
                    vcprint(
                        f"[ToolExecutor] INFERRED {tool_name}: missing "
                        f"{_disc_f}={_disc_t!r} recovered from supplied fields.",
                        color="yellow",
                    )
                    _debug_log(
                        "INFERRED",
                        tool=tool_name,
                        field=_disc_f,
                        tag=_disc_t,
                        conv=(getattr(ctx, "conversation_id", None) or "")[:8],
                        call=ctx.call_id,
                    )
                    detached_task(
                        _db_log(
                            "INFERRED",
                            tool_name=tool_name,
                            kind=_dispatch_kind,
                            args=arguments,
                            conversation_id=getattr(ctx, "conversation_id", None),
                            call_id=ctx.call_id,
                            user_id=getattr(ctx, "user_id", None),
                            metadata={
                                "inferred_discriminator": _disc_f,
                                "inferred_tag": _disc_t,
                            },
                        ),
                        name="tool_db_log_inferred",
                    )

                try:
                    _declared.args_model.model_validate(arguments or {})
                except Exception as _ve:
                    # ── Flattened dispatcher-schema recovery ──────────────
                    # Provider schemas expose the superset of dispatcher
                    # fields, while the selected Pydantic action correctly
                    # forbids fields owned by another variant. Remove only
                    # those provably cross-variant extras, revalidate once,
                    # and scream in every trace sink when recovery fires.
                    _healed = False
                    _variant_recovery = remove_flattened_variant_extras(
                        arguments or {},
                        _declared.args_model,
                        _ve,
                    )
                    if _variant_recovery is not None:
                        _cand_args, _removed_fields = _variant_recovery
                        try:
                            _declared.args_model.model_validate(_cand_args)
                            _healed = True
                        except Exception:
                            _healed = False
                        if _healed:
                            arguments = _cand_args
                            _fields_str = ", ".join(_removed_fields)
                            logger.warning(
                                "[ToolExecutor] removed flattened-schema "
                                "variant field(s) for tool %r: %s",
                                tool_name,
                                _fields_str,
                            )
                            vcprint(
                                f"[ToolExecutor] VARIANT-RECOVERED {tool_name}: "
                                f"removed field(s) [{_fields_str}] advertised "
                                "by another action and re-validated OK.",
                                color="yellow",
                            )
                            _debug_log(
                                "VARIANT_RECOVERED",
                                tool=tool_name,
                                fields=_fields_str,
                                conv=(getattr(ctx, "conversation_id", None) or "")[:8],
                                call=ctx.call_id,
                            )
                            detached_task(
                                _db_log(
                                    "VARIANT_RECOVERED",
                                    tool_name=tool_name,
                                    kind=_dispatch_kind,
                                    args=arguments,
                                    conversation_id=getattr(ctx, "conversation_id", None),
                                    call_id=ctx.call_id,
                                    user_id=getattr(ctx, "user_id", None),
                                    metadata={"removed_variant_fields": _removed_fields},
                                ),
                                name="tool_db_log_variant_recovered",
                            )

                    # ── Stringified-JSON auto-coercion (one pass) ─────────────
                    # The dominant arg-shape failure: the model sent a JSON
                    # STRING where a dict/list is required (8x-in-one-conversation
                    # class). Nothing has executed yet, so decoding the string
                    # and re-validating once is an encoding fix, not a semantic
                    # guess. Loud on every fire — the model gets a notice on the
                    # result, both trace sinks record a COERCED event.
                    _coerce = (
                        None if _healed else coerce_stringified_containers(arguments or {}, _ve)
                    )
                    if _coerce is not None:
                        _cand_args, _cand_fields = _coerce
                        # After decoding containers, retry discriminator
                        # inference once (e.g. requests='[...]' then action=batch).
                        _infer2 = infer_missing_discriminator(_cand_args, _declared.args_model)
                        if _infer2.kind == "inferred" and _infer2.args is not None:
                            _cand_args = _infer2.args
                            if inferred_discriminator is None:
                                inferred_discriminator = (
                                    _infer2.discriminator or "action",
                                    _infer2.tag or "",
                                )
                        try:
                            _declared.args_model.model_validate(_cand_args)
                            _healed = True
                        except Exception:
                            _healed = False
                        if _healed:
                            arguments = _cand_args
                            coerced_fields = _cand_fields
                            _fields_str = ", ".join(coerced_fields)
                            logger.warning(
                                "[ToolExecutor] auto-coerced JSON-string arg(s) "
                                "for tool %r: %s (model sent a JSON-encoded "
                                "string where a dict/list is required)",
                                tool_name,
                                _fields_str,
                            )
                            vcprint(
                                f"[ToolExecutor] COERCED {tool_name}: field(s) "
                                f"[{_fields_str}] were JSON-encoded strings — "
                                f"decoded to native containers and re-validated OK.",
                                color="yellow",
                            )
                            _debug_log(
                                "COERCED",
                                tool=tool_name,
                                fields=_fields_str,
                                conv=(getattr(ctx, "conversation_id", None) or "")[:8],
                                call=ctx.call_id,
                            )
                            detached_task(
                                _db_log(
                                    "COERCED",
                                    tool_name=tool_name,
                                    kind=_dispatch_kind,
                                    args=arguments,
                                    conversation_id=getattr(ctx, "conversation_id", None),
                                    call_id=ctx.call_id,
                                    user_id=getattr(ctx, "user_id", None),
                                    metadata={"coerced_fields": coerced_fields},
                                ),
                                name="tool_db_log_coerced",
                            )
                    if not _healed:
                        # Prefer the action-menu error over Pydantic's
                        # "Unable to extract tag using discriminator …".
                        if _infer.kind in ("ambiguous", "uninferable") and _infer.error:
                            _msg = _infer.error[:800]
                        else:
                            _retry_infer = infer_missing_discriminator(
                                arguments or {}, _declared.args_model
                            )
                            if (
                                _retry_infer.kind in ("ambiguous", "uninferable")
                                and _retry_infer.error
                            ):
                                _msg = _retry_infer.error[:800]
                            else:
                                _msg = format_args_error(_ve)[:800]
                        return await self._reject_invalid_arguments(
                            ctx=ctx,
                            tool_name=tool_name,
                            as_called=as_called,
                            canonical_name=canonical_name,
                            tool_def=tool_def,
                            arguments=arguments,
                            msg=_msg,
                            dispatch_kind=_dispatch_kind,
                            started_at=started_at,
                        )

        if (
            tool_def.tool_type == ToolType.LOCAL
            and not is_delegated_pre
            and not (tool_def.function_path or "").strip()
            and tool_def._callable is None
            and not self._has_external_handler(tool_def)
        ):
            _debug_log(
                "NO_EXECUTOR",
                tool=tool_name,
                canonical=canonical_name,
                reason="LOCAL+empty_fn+not_delegated",
                call_id=ctx.call_id,
            )
            vcprint(
                {
                    "tool_name": tool_name,
                    "canonical_name": canonical_name,
                    "call_id": ctx.call_id,
                    "client_tools": sorted(client_tools or []),
                    "tool_type": tool_def.tool_type.value,
                },
                f"[ToolExecutor] Tool '{tool_name}' has no viable executor "
                f"for this request — not delegated to a live client surface "
                f"AND no server-side function_path is configured.",
                color="red",
            )
            result = ToolResult(
                success=False,
                error=ToolError(
                    error_type="no_viable_executor",
                    message=(
                        f"Tool {tool_name!r} (canonical {canonical_name!r}) "
                        f"has no executor available for this request. The "
                        f"client surface that runs this tool isn't active "
                        f"in the request envelope, and no server-side "
                        f"fallback handler is configured."
                    ),
                    suggested_action=(
                        "Either run from a client that supports this tool, "
                        "or implement the server-side handler."
                    ),
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_name,
                call_id=ctx.call_id,
            )
            result.compute_duration()
            await self._record_rejected(
                ctx,
                tool_name=as_called,
                arguments=arguments,
                result=result,
                tool_type=tool_def.tool_type.value,
                canonical_name=canonical_name,
            )
            stream = ToolStreamManager(ctx.emitter, ctx.call_id, tool_name)
            await stream.error(
                f"Tool '{tool_name}' has no viable executor for this request.",
                error_type="no_viable_executor",
            )
            return result.to_tool_result_content(), result

        # Content IR shadow input check. This runs only after wire-name and
        # alias resolution plus all safe argument coercions, against the same
        # normalized schema sent to providers. It never blocks dispatch.
        from matrx_graph.content_ir.model import kind_of
        from matrx_graph.contract_kinds import check_schema
        from matrx_graph.kinds import check_against_kind

        from matrx_ai.tools.kinds import result_kind_slug

        input_contract, output_contract = tool_def.content_ir_contracts()
        input_kind_verdict = check_schema(arguments, input_contract.json_schema)
        if input_kind_verdict.errors:
            logger.error(
                "[Content IR] tool input drift for %s (%s): %s",
                canonical_name,
                input_contract.kind,
                input_kind_verdict.errors,
            )
            await _capture_tool_input_contract_drift(
                ctx=ctx,
                tool_name=canonical_name,
                input_kind=input_contract.kind,
                error_count=len(input_kind_verdict.errors),
            )

        # --- Phase 1: log attempt (fire-and-forget INSERT) ---
        from matrx_ai.tools.execution_authorization import evaluate_tool_authorization

        authorization = await evaluate_tool_authorization(tool_def, arguments, ctx)
        if authorization.requires_confirmation:
            client_tools = frozenset({*(client_tools or frozenset()), tool_name})
            is_delegated_pre = True
            _dispatch_kind = "DELEGATE"

        # ``as_called`` is the literal (wire) name the model used;
        # ``tool_def.name`` is the *canonical* identity. Pass both so the
        # logger records each in its own column (analytics defaults to
        # canonical; trace UIs can show what the model actually called it).
        row_id = await self.execution_logger.log_started(
            ctx,
            tool_def,
            arguments,
            exposed_name=as_called,
            authorization_metadata=authorization.metadata or None,
        )

        stream = ToolStreamManager(ctx.emitter, ctx.call_id, tool_name)

        # --- Guardrails ---
        guardrail_result = await self.guardrails.check(tool_name, arguments, ctx, tool_def)
        if guardrail_result.blocked:
            error_result = ToolResult(
                success=False,
                error=ToolError(
                    error_type=guardrail_result.error_type,
                    message=guardrail_result.reason or "Blocked by guardrail",
                    suggested_action=guardrail_result.suggested_action,
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_name,
                call_id=ctx.call_id,
            )
            error_result.compute_duration()
            await stream.error(guardrail_result.reason or "Blocked", guardrail_result.error_type)
            if (
                guardrail_result.error_type == "recursion_depth"
                and tool_def.tool_type == ToolType.AGENT
            ):
                await warn_member_depth_exhausted(ctx, tool_def, tool_name)
            self.execution_logger.prepare_metadata(error_result)
            events = stream.get_events_for_persistence()
            # Phase F: detached_task so this log write doesn't inherit the
            # request's transaction connection (would cause asyncpg
            # InterfaceError when the parent flush is mid-statement). Capture
            # the coordinator in the live context and hand it through so the
            # UPDATE is queued onto the INSERT's Session instead of racing it
            # as a context-less direct write (see _update_row).
            from matrx_ai.persistence.queue_helpers import get_coordinator as _get_coord

            _gr_coord = _get_coord()
            await self._persist_tool_outcome(
                self.execution_logger.log_error(
                    row_id, error_result, events, coordinator=_gr_coord
                ),
                coordinator=_gr_coord,
                name="tool_log_error_guardrail",
            )
            return error_result.to_tool_result_content(), error_result

        self.guardrails.record_call(tool_name, arguments, ctx)

        # --- Stream started (with full arguments — non-negotiable) ---
        user_message = tool_def.format_user_message(arguments)
        await stream.started(user_message, arguments=arguments)

        # Touch lifecycle
        self.lifecycle.touch(ctx.conversation_id)

        # --- Execute ---
        # Client-delegated tools follow a different cancellation contract:
        # their row is the durable ledger entry for "awaiting client POST",
        # so an SSE disconnect MUST leave the row in 'delegated' (not flip
        # it to 'error/abandoned') so a later POST or the expiry sweep can
        # resolve it. The delegated dispatch RETURNS IMMEDIATELY — it commits
        # the ledger row + emits ``tool_delegated`` and then suspends; it never
        # blocks on the user. So its timeout only guards that commit/emit and is
        # deliberately SHORT and decoupled from the user's answer window, which
        # is durable (cx_tool_call.expires_at + /resume), not a held request task.
        is_delegated = bool(client_tools and tool_name in client_tools)
        dispatch_timeout = (
            _DELEGATED_DISPATCH_TIMEOUT_SECONDS if is_delegated else tool_def.timeout_seconds
        )
        cancellation_after_completion: asyncio.CancelledError | None = None
        try:
            dispatch = self._dispatch(
                tool_def,
                arguments,
                ctx,
                stream,
                client_tools,
                row_id,
                authorization_metadata=authorization.metadata or None,
            )
            if tool_def.must_complete and not is_delegated:
                result, cancellation_after_completion = await _await_must_complete(
                    dispatch,
                    timeout_seconds=dispatch_timeout,
                    stream=stream,
                    tool_name=tool_name,
                )
            else:
                result = await asyncio.wait_for(
                    dispatch,
                    timeout=dispatch_timeout,
                )
        except asyncio.CancelledError:
            # Server-side tools: flip 'running' → 'error/abandoned' synchronously
            # (shielded) to avoid orphan rows. Client-delegated tools: LEAVE the
            # row alone — status='delegated' is durable and expected to outlive
            # the request.
            if row_id and not is_delegated:
                try:
                    # Cancellation cleanup runs under ``shield()``, which may
                    # execute in a copied context after request teardown has
                    # begun. Carry the coordinator explicitly, just like the
                    # normal completion funnel, so the terminal UPDATE cannot
                    # miss the deferred INSERT or strand a running row.
                    from matrx_ai.persistence.queue_helpers import (
                        get_coordinator as _get_cancel_coord,
                    )

                    _cancel_coord = _get_cancel_coord()
                    await asyncio.shield(
                        self.execution_logger.log_abandoned(
                            row_id,
                            reason="client_disconnected",
                            error_message=(
                                f"Tool '{tool_name}' was abandoned — the request "
                                "was cancelled (client disconnected) before the "
                                "tool finished."
                            ),
                            execution_events=stream.get_events_for_persistence(),
                            coordinator=_cancel_coord,
                        )
                    )
                except Exception as cleanup_exc:
                    vcprint(
                        f"[ToolExecutor] Failed to mark row abandoned on cancel: {cleanup_exc}",
                        color="red",
                    )
            raise
        except TimeoutError:
            result = ToolResult(
                success=False,
                error=ToolError(
                    error_type="timeout",
                    message=f"Tool '{tool_name}' timed out after {dispatch_timeout:.0f}s",
                    is_retryable=True,
                    suggested_action="Try with simpler parameters or break the task into smaller parts.",
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_name,
                call_id=ctx.call_id,
            )
        except Exception as exc:
            result = ToolResult(
                success=False,
                error=ToolError(
                    error_type="execution",
                    message=str(exc),
                    traceback=tb.format_exc(),
                    is_retryable=False,
                    suggested_action="Check the error details and try with different parameters.",
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_name,
                call_id=ctx.call_id,
            )

        result.compute_duration()

        result.input_kind = input_contract.kind
        result.input_kind_version = input_contract.version
        result.input_kind_checked = input_kind_verdict.checked
        result.input_kind_errors = input_kind_verdict.errors

        # --- Client-delegated suspension: record DELEGATED, skip OK/FAIL ---
        # A delegated call produced no result here — it suspended. The cx_tool_call
        # row is already 'delegated' (set in _execute_delegated) and is the
        # durable ledger for the client's POST /tool_results + /resume. Running
        # the completed/error stream events or log_completed/log_error below would
        # overwrite that 'delegated' status and emit a misleading OK/FAIL trace —
        # skip those. (docs/tool_delegation/DELEGATION_LOOP_BUGS.md)
        #
        # But the DISPATCH itself must still reach both trace sinks: before
        # 2026-08-12 this early return skipped ALL logging, so delegated tools
        # (executor matrx-user — apply_surface_write, war_room_*, matrx-local
        # tools) left ZERO rows in chat.tool_trace and were invisible to
        # /admin/debug-traces. The completion is recorded by the /tool_results
        # resolver (aidream/services/ai_execution/tool_results.py) as OK/FAIL
        # with kind=DELEGATE when the client posts the result back.
        if result.delegated_pending:
            try:
                _dl_conv_id = ctx.conversation_id or None
            except Exception:
                _dl_conv_id = None
            try:
                _dl_user_id: str | None = ctx.user_id or None
            except Exception:
                _dl_user_id = None
            _debug_log(
                "DELEGATED",
                tool=tool_name,
                kind=_dispatch_kind,
                conv=(_dl_conv_id or "")[:8],
                call=ctx.call_id,
            )
            detached_task(
                _db_log(
                    "DELEGATED",
                    tool_name=tool_name,
                    kind=_dispatch_kind,
                    args=arguments,
                    conversation_id=_dl_conv_id,
                    call_id=ctx.call_id,
                    user_id=_dl_user_id,
                    metadata={"disposition": "suspended_for_client"},
                ),
                name="tool_db_log_delegated",
            )
            return result.to_tool_result_content(), result

        # --- Defense-in-depth: embedded-error-envelope detection ---
        # Some legacy tools (and any new ones written under the same
        # anti-pattern) return ``ToolResult(success=True, output={"success":
        # False, "error": "..."})`` — the outer flag says OK but the
        # payload says the underlying operation failed. The Pydantic
        # validator on ToolResult.output catches the str()-ed-dict variant;
        # this catches the native-dict variant. When detected, flip the
        # ToolResult to a structured failure BEFORE downstream consumers
        # (stream.error, log_error, _debug_log FAIL) read it, so all three
        # telemetry sinks record the truth instead of the outer lie.
        if (
            result.success
            and isinstance(result.output, dict)
            and result.output.get("success") is False
        ):
            embedded_err = (
                result.output.get("error")
                or result.output.get("message")
                or "Tool returned success=False inside its output payload."
            )
            result.success = False
            result.error = ToolError(
                error_type="embedded_error_envelope",
                message=str(embedded_err),
                is_retryable=False,
                suggested_action=(
                    "The tool wrapped a failure as a success envelope. "
                    "Inspect the original output and fix the tool to "
                    "raise or return ToolResult(success=False, ...) directly."
                ),
            )

        # --- Content IR: the tool's RESULT kind (KINDS_EVERYWHERE_PLAN §10d-C) ---
        # Two different things, and conflating them is what kept tools opaque:
        #
        #   * the GENERATED CONTRACT (`tool_io_<name>_<digest>_output`, derived
        #     from the row's hand-written `output_schema`) is an ABI fingerprint
        #     — it detects DRIFT. It is not an identity, it renders nowhere, and
        #     it is nobody's declaration.
        #   * the CURATED KIND is the result's identity, and — exactly as
        #     everywhere else in the platform — the payload SAYS SO ITSELF via
        #     its `__kind` field. A tool declares its result kind by RETURNING a
        #     KindModel; there is no second registry and no new column.
        #
        # So the payload's own declaration wins, verified against the live
        # catalog just like a workflow node's (scheduler.py runtime propagation:
        # "output kind = the kind of what actually flowed"). A payload lying
        # about itself screams exactly like author drift; a payload carrying no
        # `__kind` changes nothing and the generated contract still governs.
        # Both schemas describe the JSON wire value, never an in-memory
        # Pydantic object. Keep one serialization seam for the curated kind
        # check and the generated output-contract drift check. Passing a
        # BaseModel directly to ``check_schema`` makes every valid kinded tool
        # result look like a non-object and creates a false drift row.
        serialized_output = (
            result.output.model_dump(mode="json")
            if isinstance(result.output, BaseModel)
            else result.output
        )
        curated_kind = kind_of(serialized_output)
        if curated_kind == "json":
            # 'json' is a format word, never an identity — the same refusal the
            # scheduler makes when adopting a kind from a payload.
            curated_kind = None
        if curated_kind is not None:
            # Validate the SERIALIZED form: a tool may hand back the KindModel
            # itself, and the registered schema describes the wire shape.
            kind_check = await check_against_kind(serialized_output, curated_kind)
            result.output_kind = curated_kind
            result.output_kind_version = kind_check.kind_version
            result.output_kind_checked = kind_check.checked
            result.output_kind_errors = list(kind_check.errors)
            if kind_check.errors:
                logger.error(
                    "[Content IR] tool result violates its self-described kind for %s (%s): %s",
                    canonical_name,
                    curated_kind,
                    kind_check.errors,
                )
            elif not kind_check.checked:
                logger.warning(
                    "[Content IR] tool result kind check SKIPPED for %s (%s): %s "
                    "— a skipped check is never a pass.",
                    canonical_name,
                    curated_kind,
                    kind_check.degraded_reason.value
                    if kind_check.degraded_reason is not None
                    else "unknown",
                )

        # Failed tools have no successful output to validate. Their ToolError
        # is the contract; checking ``None`` against the success schema creates
        # a second false drift event that hides the actual failure.
        if result.success and output_contract is not None:
            output_kind_verdict = check_schema(serialized_output, output_contract.json_schema)
            if curated_kind is None:
                result.output_kind = output_contract.kind
                result.output_kind_version = output_contract.version
                result.output_kind_checked = output_kind_verdict.checked
                result.output_kind_errors = output_kind_verdict.errors
            if output_kind_verdict.errors:
                logger.error(
                    "[Content IR] tool output drift for %s (%s): %s",
                    canonical_name,
                    output_contract.kind,
                    output_kind_verdict.errors,
                )
                await _capture_tool_output_contract_drift(
                    ctx=ctx,
                    tool_name=canonical_name,
                    output_kind=output_contract.kind,
                    error_count=len(output_kind_verdict.errors),
                )

        # The RUNTIME half of the reconciled tool measure (§10g GAP 3). A tool
        # listed in ``TOOL_RESULT_KINDS`` has a stored ``output_schema`` derived
        # from that model, so every reader that never runs the tool has been
        # told what comes back. If the implementation stops returning the model
        # — a branch nobody converted, a dict slipped in on an error path — that
        # promise is silently false. Scream instead: same loud-but-open posture
        # as everywhere else, the call still succeeds.
        declared_slug = result_kind_slug(canonical_name)
        if result.success and declared_slug is not None and curated_kind != declared_slug:
            logger.error(
                "[Content IR] DECLARED tool result kind missing for %s: expected "
                "%r from the returned KindModel, payload carries %r. The stored "
                "output_schema promises a shape this branch does not return — "
                "convert the branch (matrx_ai/tools/kinds/__init__.py names the "
                "declaration) or remove the declaration.",
                canonical_name,
                declared_slug,
                curated_kind,
            )
            result.output_kind_errors = [
                *result.output_kind_errors,
                f"declared result kind {declared_slug!r} not carried by the payload",
            ]
            await _capture_tool_result_kind_missing(
                ctx=ctx,
                tool_name=canonical_name,
                output_kind=declared_slug,
            )

        # --- Surface the arg-coercion / inference notice to the MODEL ---
        # When the pre-flight healed JSON-string args or inferred a missing
        # action/command, the model must LEARN the correct shape, not just get
        # away with it: inject a notice key into a dict output so it rides the
        # tool result into context. Non-dict outputs fall back to the log +
        # COERCED/INFERRED trace events only.
        if coerced_fields and isinstance(result.output, dict):
            result.output.setdefault(
                "arg_coercion_notice",
                (
                    f"NOTICE: argument(s) {', '.join(repr(f) for f in coerced_fields)} "
                    "were sent as JSON-encoded strings; the server decoded them to "
                    "native JSON this time. Next call, pass the raw JSON "
                    "object/array itself — not a quoted string."
                ),
            )
        if inferred_discriminator and isinstance(result.output, dict):
            _idf, _idt = inferred_discriminator
            result.output.setdefault(
                "arg_inference_notice",
                (
                    f"NOTICE: {_idf!r} was omitted; inferred {_idf}={_idt!r} from "
                    f"the other fields. Next call, set {_idf}={_idt!r} explicitly."
                ),
            )

        # --- Contract repair: failure with no structured error ---
        # If a tool returns success=False but leaves ToolResult.error unset,
        # we used to surface a useless "Unknown error" to the model, the FE,
        # and all three telemetry sinks. Synthesise an error from result.output
        # instead so the failure detail is always visible — and stamp it with a
        # dedicated error_type so the tool author can find and fix the leak.
        if not result.success and result.error is None:
            try:
                output_preview = json.dumps(result.output, default=str)[:4000]
            except Exception:
                output_preview = str(result.output)[:4000]
            result.error = ToolError(
                error_type="missing_error_field",
                message=(
                    f"Tool {tool_name!r} returned success=False but did not "
                    f"populate ToolResult.error. Synthesised from output: "
                    f"{output_preview}"
                ),
                is_retryable=False,
                suggested_action=(
                    "Fix the tool to populate ToolResult.error when returning "
                    "success=False. Per-item failure details (if any) are in "
                    "the message above and in the original output payload."
                ),
            )

        if (
            not result.success
            and canonical_name == "context_patch"
            and result.error is not None
            and result.error.error_type == "patch_no_match"
        ):
            await _capture_context_patch_no_match(ctx=ctx)

        # Normalize result metadata before the completion event snapshots the
        # output.  ToolStreamManager stores a validated copy, so mutating the
        # ToolResult afterward cannot repair NUL bytes already captured in
        # execution_events.
        self.execution_logger.prepare_metadata(result)

        # --- Stream completed / error (with full result — non-negotiable) ---
        if result.success:
            await stream.completed("Done", result=result)
        else:
            await stream.error(result.error.message, result.error.error_type)

        # --- Phase 2: log result (fire-and-forget UPDATE) ---
        events = stream.get_events_for_persistence()
        events.append(
            {
                "event": "content_ir_contract",
                "input": {
                    "kind": result.input_kind,
                    "version": result.input_kind_version,
                    "checked": result.input_kind_checked,
                    "errors": result.input_kind_errors,
                },
                "output": {
                    "kind": result.output_kind,
                    "version": result.output_kind_version,
                    "checked": result.output_kind_checked,
                    "errors": result.output_kind_errors,
                },
            }
        )
        # Capture the request-scoped WriteCoordinator NOW, while we are still in
        # the live request context. detached_task runs the completion write in a
        # FRESH contextvars Context (to isolate the asyncpg connection), which
        # also hides the coordinator ContextVar — without this hand-off the
        # UPDATE would fall back to a direct DB write that races the row's
        # deferred INSERT and gets silently lost (the status='error'+success=true
        # phantom-row bug). Passing the object in keeps the UPDATE on the same
        # Session as the INSERT, ordered after it. None outside a request scope.
        from matrx_ai.persistence.queue_helpers import get_coordinator as _get_coord

        _log_coord = _get_coord()
        # In-request: queue the UPDATE INLINE onto the coordinator (in-memory,
        # no DB I/O) so it deterministically coalesces with the row's INSERT and
        # flushes at the turn barrier. Out-of-request: detached_task isolates the
        # real DB write. See _persist_tool_outcome for the full rationale (this
        # is the fix for agent_call's lost completion write → watchdog phantom).
        if result.success:
            await self._persist_tool_outcome(
                self.execution_logger.log_completed(row_id, result, events, coordinator=_log_coord),
                coordinator=_log_coord,
                name="tool_log_completed",
            )
        else:
            await self._persist_tool_outcome(
                self.execution_logger.log_error(row_id, result, events, coordinator=_log_coord),
                coordinator=_log_coord,
                name="tool_log_error",
            )

        if cancellation_after_completion is not None:
            vcprint(
                f"[ToolExecutor] Must-complete tool '{tool_name}' reached a terminal "
                "result and its outcome was persisted; propagating the deferred "
                "request cancellation now.",
                color="yellow",
            )
            raise cancellation_after_completion

        # User-id capture for the DB sink. ctx.user_id is a property that
        # reads from AppContext and may raise when called outside a request;
        # swallow so telemetry never blocks dispatch.
        try:
            _trace_user_id: str | None = ctx.user_id or None
        except Exception:
            _trace_user_id = None
        # ctx.conversation_id also reads AppContext and RAISES out of request — wrap
        # it identically (the size gate now depends on this for the overflow key).
        try:
            _trace_conv_id_full = ctx.conversation_id or None
        except Exception:
            _trace_conv_id_full = None

        if result.success:
            # Verbose mode (MATRX_TOOL_DEBUG_VERBOSE=1) adds args + a
            # truncated result preview to OK events. Use this when chasing
            # a silent-success bug — the trace file grows much faster, but
            # you get forensic detail without joining cx_tool_call.
            verbose_extra: dict[str, Any] = {}
            if _debug_verbose():
                try:
                    verbose_extra["args"] = json.dumps(arguments, default=str)
                except Exception:
                    verbose_extra["args"] = str(arguments)
                if result.output is not None:
                    try:
                        verbose_extra["result"] = json.dumps(result.output, default=str)
                    except Exception:
                        verbose_extra["result"] = str(result.output)
            _debug_log(
                "OK",
                tool=tool_name,
                kind=_dispatch_kind,
                ms=result.duration_ms,
                conv=(_trace_conv_id_full or "")[:8],
                call=ctx.call_id,
                **verbose_extra,
            )
            # DB sink — always retain the bounded result preview. Downstream
            # review/audit consumers must be able to fact-check successful
            # calls; _db_log caps the serialized value at 4 KiB.
            detached_task(
                _db_log(
                    "OK",
                    tool_name=tool_name,
                    kind=_dispatch_kind,
                    duration_ms=result.duration_ms,
                    args=arguments,
                    result_preview=result.output,
                    conversation_id=_trace_conv_id_full,
                    call_id=ctx.call_id,
                    user_id=_trace_user_id,
                ),
                name="tool_db_log_OK",
            )
        else:
            # Failures get the full forensic detail: args (truncated),
            # error type, error message. This is the data the operator
            # actually needs to triage — don't make them join against
            # the DB to find it.
            try:
                args_blob = json.dumps(arguments, default=str)
            except Exception:
                args_blob = str(arguments)
            _err_type = result.error.error_type if result.error else "unknown"
            _err_msg = result.error.message if result.error else "no error message"
            _err_tb = result.error.traceback if result.error else None
            _expected_domain_failure = _is_expected_domain_failure(
                tool_name=canonical_name,
                error_type=_err_type,
            )
            if not _expected_domain_failure:
                await _capture_tool_execution_failed(
                    ctx=ctx,
                    tool_name=canonical_name,
                    error_type=_err_type,
                )

            # SCREAM. A tool failure is a REAL failure and it goes to the
            # console, always — the two sinks below are durable but SILENT
            # (a file under .matrx-debug/ and a chat.tool_trace row), so for
            # years a tool could fail every single call and the terminal
            # showed nothing but a happy stream. Whoever is watching the
            # server MUST see this without opening a log file or a DB.
            #
            # The traceback is printed when we have one. We often DON'T,
            # because the tool caught its own exception and stringified it
            # (`message=f"... {exc}"`) — that destroys the stack before it can
            # ever reach here. That is a defect in the tool, not here; the
            # `no traceback` line below names it so the tool gets fixed.
            vcprint(
                "\n"
                "╔══════════════════════════════════════════════════════════════════╗\n"
                "║  TOOL CALL FAILED                                                ║\n"
                "╚══════════════════════════════════════════════════════════════════╝\n"
                f"  tool:       {tool_name}  (kind={_dispatch_kind}, {result.duration_ms}ms)\n"
                f"  error_type: {_err_type}\n"
                f"  message:    {_err_msg}\n"
                f"  conv:       {_trace_conv_id_full or '-'}\n"
                f"  call_id:    {ctx.call_id}\n"
                f"  args:       {args_blob[:2000]}\n"
                + (
                    f"  traceback:\n{_err_tb}"
                    if _err_tb
                    else (
                        "  traceback:  <not applicable — expected domain conflict; "
                        "handled by the tool's expected-domain-failure contract.>"
                        if _expected_domain_failure
                        else "  traceback:  <none — the tool swallowed its exception and "
                        f"stringified it. Fix '{tool_name}' to let the exception reach the "
                        "executor, or set ToolError.traceback.>"
                    )
                ),
                color="yellow" if _expected_domain_failure else "red",
            )

            _debug_log(
                "FAIL",
                tool=tool_name,
                kind=_dispatch_kind,
                ms=result.duration_ms,
                args=args_blob,
                err_type=_err_type,
                err_msg=_err_msg,
                tb=_err_tb,
                conv=(_trace_conv_id_full or "")[:8],
                call=ctx.call_id,
            )
            detached_task(
                _db_log(
                    "FAIL",
                    tool_name=tool_name,
                    kind=_dispatch_kind,
                    duration_ms=result.duration_ms,
                    args=arguments,
                    err_type=_err_type,
                    err_msg=_err_msg,
                    # No schema change needed — chat.tool_trace.metadata is jsonb.
                    # Without this the durable row recorded the error MESSAGE but
                    # threw the stack away, so /admin/debug-traces could tell you
                    # THAT a tool broke but never WHERE.
                    metadata={"traceback": _err_tb} if _err_tb else None,
                    conversation_id=_trace_conv_id_full,
                    call_id=ctx.call_id,
                    user_id=_trace_user_id,
                ),
                name="tool_db_log_FAIL",
            )

        # --- Layer 1: universal tool-result size gate (source-aware, graceful) ---
        # Cap what the model SEES from this result so a runaway payload (the 1.8 MB
        # note dump) can't be re-billed on every loop iteration. A tool that
        # self-managed (output_self_capped) is trusted; everything else over the
        # soft cap is truncated-with-notice, its full payload cached for
        # fetch_tool_result, and the firing recorded (a defect for tools we own, an
        # expected event for external/MCP). Runs on EVERY output-carrying result —
        # the single convergence point all tool kinds reach.
        content_dict = result.to_tool_result_content()
        _tool_kind = tool_kind_label(tool_def.tool_type)
        content_dict, _gate_truncated = apply_size_gate(
            content_dict,
            output_self_capped=result.output_self_capped,
            tool_name=tool_name,
            tool_kind=_tool_kind,
            conversation_id=_trace_conv_id_full,
            user_id=_trace_user_id,
        )
        if _gate_truncated:
            if _tool_kind in ("native", "agent"):
                await _capture_tool_result_size_unmanaged(ctx=ctx, tool_name=tool_name)
            # Inject-on-truncation: make fetch_tool_result available on the NEXT
            # turn so the notice's promise ("call fetch_tool_result …") is real,
            # without bloating the default toolset. Idempotent — the merge dedups
            # by name, so repeated truncations don't pile up. Best-effort.
            try:
                ctx.queue_tool_changes(add=[{"kind": "registered", "name": "fetch_tool_result"}])
            except Exception as inj_exc:  # noqa: BLE001 — injection must never break dispatch
                vcprint(
                    f"[ToolExecutor] fetch_tool_result injection failed: {inj_exc}",
                    color="yellow",
                )
        return content_dict, result

    # ------------------------------------------------------------------
    # Batch execution
    # ------------------------------------------------------------------

    async def execute_batch(
        self,
        tool_calls: list[dict[str, Any]],
        ctx_base: ToolContext,
        client_tools: frozenset[str] | None = None,
        allowed_tools: frozenset[str] | None = None,
    ) -> tuple[list[dict[str, Any]], list[ToolResult]]:
        """Execute multiple tool calls concurrently.

        Each item in ``tool_calls`` must have:
          - ``name``: tool name
          - ``arguments``: dict of arguments
          - ``call_id`` or ``id``: the tool call id
        """
        tasks = []
        child_contexts: list[ToolContext] = []
        for tc in tool_calls:
            name = tc.get("name", "")
            arguments = tc.get("arguments", {})
            call_id = tc.get("call_id") or tc.get("id") or str(uuid4())

            child_ctx = ctx_base.model_copy(
                update={
                    "call_id": call_id,
                    "tool_name": name,
                }
            )
            child_contexts.append(child_ctx)
            tasks.append(self.execute(name, arguments, child_ctx, client_tools, allowed_tools))

        raw_results = await asyncio.gather(*tasks, return_exceptions=True)

        content_results: list[dict[str, Any]] = []
        full_results: list[ToolResult] = []

        for idx, r in enumerate(raw_results):
            if isinstance(r, Exception):
                tc = tool_calls[idx]
                child_ctx = child_contexts[idx]
                call_id = child_ctx.call_id
                tool_name_str = tc.get("name", "")
                error_traceback = "".join(tb.format_exception(type(r), r, r.__traceback__))
                err_result = ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="unhandled",
                        message=str(r),
                        traceback=error_traceback,
                    ),
                    started_at=time.time(),
                    completed_at=time.time(),
                    tool_name=tool_name_str,
                    call_id=call_id,
                )
                # Stream the unhandled exception as a tool_error so the client
                # knows this specific call failed rather than seeing silence.
                stream = ToolStreamManager(ctx_base.emitter, call_id, tool_name_str)
                await stream.error(str(r), error_type="unhandled")
                self.execution_logger.prepare_metadata(err_result)
                row_id = self.execution_logger.row_id_for_call(child_ctx)
                if row_id:
                    from matrx_ai.persistence.queue_helpers import (
                        get_coordinator as _get_coord,
                    )

                    coordinator = _get_coord()
                    await self._persist_tool_outcome(
                        self.execution_logger.log_error(
                            row_id,
                            err_result,
                            stream.get_events_for_persistence(),
                            coordinator=coordinator,
                        ),
                        coordinator=coordinator,
                        name="tool_log_unhandled_error",
                    )
                content_results.append(err_result.to_tool_result_content())
                full_results.append(err_result)
            else:
                content_dict, full_result = r
                content_results.append(content_dict)
                full_results.append(full_result)

        return content_results, full_results

    # ------------------------------------------------------------------
    # Dispatch
    # ------------------------------------------------------------------

    async def _dispatch(
        self,
        tool_def: ToolDefinition,
        args: dict[str, Any],
        ctx: ToolContext,
        stream: ToolStreamManager,
        client_tools: frozenset[str] | None = None,
        row_id: str = "",
        authorization_metadata: dict[str, Any] | None = None,
    ) -> ToolResult:
        # Client-delegated tools take priority over all other dispatch paths.
        # The tool is NOT executed server-side; instead a tool_delegated event is
        # emitted over the SSE stream and the executor suspends until the client
        # POSTs the result back.
        if client_tools and tool_def.name in client_tools:
            return await self._execute_delegated(
                tool_def,
                args,
                ctx,
                row_id,
                authorization_metadata=authorization_metadata,
            )

        match tool_def.tool_type:
            case ToolType.LOCAL:
                # Host-executor precedence, dispatch-time layer: a LOCAL def
                # with no execution path of its own (no callable, no
                # function_path — e.g. a server/DB row for a tool the HOST
                # executes) routes to the host's registered external handler
                # when one exists, instead of dying in _execute_local. The
                # registry's load-time flip is the first layer; this one
                # catches defs that arrived after handlers were registered
                # (cache-bust reloads, late loads).
                if (
                    tool_def._callable is None
                    and not (tool_def.function_path or "").strip()
                    and self._has_external_handler(tool_def)
                ):
                    return await self._execute_external_handler(tool_def, args, ctx)
                return await self._execute_local(tool_def, args, ctx, stream)
            case ToolType.EXTERNAL_MCP:
                return await self._execute_external_mcp(tool_def, args, ctx)
            case ToolType.AGENT:
                return await self._execute_agent(tool_def, args, ctx)
            case ToolType.EXTERNAL_HANDLER:
                return await self._execute_external_handler(tool_def, args, ctx)
            case _:
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="configuration",
                        message=f"Unknown tool type: {tool_def.tool_type}",
                    ),
                    started_at=time.time(),
                    completed_at=time.time(),
                    tool_name=tool_def.name,
                    call_id=ctx.call_id,
                )

    async def _execute_delegated(
        self,
        tool_def: ToolDefinition,
        args: dict[str, Any],
        ctx: ToolContext,
        row_id: str = "",
        authorization_metadata: dict[str, Any] | None = None,
    ) -> ToolResult:
        """Delegate a tool call to the connected client — a SUSPENSION POINT.

        Delegation does NOT block the loop. We (1) flip the cx_tool_call row to
        ``status='delegated'`` (the durable ledger entry) and (2) emit a
        ``tool_delegated`` event over the stream, then return a *pending* result
        immediately. The orchestrator detects ``delegated_pending`` and ends the
        turn. The client executes the tool and POSTs the result to
        ``POST /conversations/{id}/tool_results``; once no delegated rows remain,
        ``POST /conversations/{id}/resume`` reconstructs the conversation (now
        with the tool result) and continues the loop.

        This replaced an in-memory ``ClientToolWaiter.wait_for_result`` blocking
        await that (a) wasn't reliably blocking and (b) fed an empty result into
        the loop when it returned, causing the runaway tool-call loop. Full
        history: docs/tool_delegation/DELEGATION_LOOP_BUGS.md.
        """
        from matrx_ai.context.events import ToolEventPayload

        started_at = time.time()

        wait_seconds = int(tool_def.max_client_wait_seconds or DELEGATED_CALL_ABANDON_AFTER_SECONDS)
        expires_at = datetime.now(UTC) + timedelta(seconds=wait_seconds)

        # ── Durability checkpoint — TWO-STEP, NON-NEGOTIABLE ──────────────
        # (1) Queue the UPDATE that flips cx_tool_call to 'delegated' and stamps
        #     expires_at. Combined with the queued INSERT from log_started(),
        #     this is the FULL durable ledger entry the client will look up.
        # (2) `coordinator.finalize(...)` — synchronously flush + drain all
        #     in-flight commits so the row is ON DISK before we emit the
        #     `tool_delegated` event below.
        #
        # WITHOUT (2) the client's POST /tool_results racing this same row's
        # commit will return 404 and the conversation is stuck (the client has
        # no retry). The persistence contract names this as one of the three
        # deliberate blocking points: "the pre-suspend commit before a client-
        # delegated tool" (see CLAUDE.md, packages/matrx-ai/.../persistence
        # skill, and docs/tool_delegation/DELEGATION_LOOP_BUGS.md).
        #
        # We finalize OUTSIDE the emit so a PersistenceBarrierError aborts the
        # delegation entirely — better to fail loudly than to tell the client
        # "go ahead" without a durable ledger to recover against.
        # Desktop targeting is scoped to tools actually bound to the
        # matrx-local executor — a selected desktop target must never capture
        # browser-executed delegated tools (war_room_*, widget_*, ui-first):
        # their results would fail the /tool_results submission-binding check
        # (the browser sends no instance_id) → 404 → wedged turn, while the
        # desktop claims calls it cannot execute.
        is_desktop_bound = any(
            b == "matrx-local" or b.startswith("matrx-local.")
            for b in self.registry.bindings_for_tool(tool_def.name)
        )
        await self.execution_logger.log_delegated(
            row_id, expires_at=expires_at, allow_desktop_target=is_desktop_bound
        )

        from matrx_ai.persistence.queue_helpers import get_coordinator

        _coord = get_coordinator()
        if _coord is not None:
            await _coord.finalize(reason="pre_client_delegation_commit")

        emitter = ctx.emitter
        if emitter is not None:
            target_instance_id = (
                self.execution_logger._desktop_target_instance_id() if is_desktop_bound else None
            )
            event_data: dict[str, Any] = {"arguments": args}
            if authorization_metadata:
                event_data["execution_authorization"] = authorization_metadata
            if target_instance_id:
                event_data["target_instance_id"] = target_instance_id
            await emitter.send_tool_event(
                ToolEventPayload(
                    event="tool_delegated",
                    call_id=ctx.call_id,
                    tool_name=tool_def.name,
                    message=f"Delegating {tool_def.name} to client",
                    show_spinner=True,
                    data=event_data,
                )
            )

        # Pending marker — NOT a result. success=False keeps it out of any
        # success path; delegated_pending is the real signal. The caller
        # (execute) returns this without logging so the 'delegated' row stands.
        return ToolResult(
            success=False,
            delegated_pending=True,
            tool_name=tool_def.name,
            call_id=ctx.call_id,
            started_at=started_at,
            completed_at=time.time(),
        )

    async def _execute_local(
        self,
        tool_def: ToolDefinition,
        args: dict[str, Any],
        ctx: ToolContext,
        stream: ToolStreamManager,
    ) -> ToolResult:
        func = tool_def._callable
        if func is None:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="configuration",
                    message=f"No callable resolved for local tool '{tool_def.name}'",
                ),
                started_at=time.time(),
                completed_at=time.time(),
                tool_name=tool_def.name,
                call_id=ctx.call_id,
            )

        started_at = time.time()
        raw_result = await func(args, ctx)

        if isinstance(raw_result, ToolResult):
            raw_result.started_at = raw_result.started_at or started_at
            raw_result.completed_at = raw_result.completed_at or time.time()
            raw_result.tool_name = raw_result.tool_name or tool_def.name
            raw_result.call_id = raw_result.call_id or ctx.call_id
            return raw_result

        # Legacy compatibility: dict with "status" / "result"
        if isinstance(raw_result, dict):
            is_error = raw_result.get("status") == "error"
            return ToolResult(
                success=not is_error,
                output=(
                    raw_result.get("result")
                    if not is_error
                    else raw_result.get("error", raw_result.get("result"))
                ),
                error=ToolError(
                    error_type="execution",
                    message=str(raw_result.get("error", raw_result.get("result", ""))),
                )
                if is_error
                else None,
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_def.name,
                call_id=ctx.call_id,
            )

        return ToolResult(
            success=True,
            output=raw_result,
            started_at=started_at,
            completed_at=time.time(),
            tool_name=tool_def.name,
            call_id=ctx.call_id,
        )

    async def _execute_external_mcp(
        self,
        tool_def: ToolDefinition,
        args: dict[str, Any],
        ctx: ToolContext,
    ) -> ToolResult:
        from .external_mcp import ExternalMCPClient

        # Host-injected per-user MCP auth (the ``mcp_auth_resolver`` seam —
        # ``async (server_slug, user_id) -> dict | None``). The host resolves
        # the user's stored connection credentials (vault-backed in aidream)
        # just in time; matrx-ai never persists or decrypts them. Canonical
        # tool names are ``mcp.<slug>.<local>``.
        if tool_def.mcp_server_auth is None and tool_def.name.startswith("mcp."):
            from matrx_ai._ext import get_ext, has_ext

            if has_ext("mcp_auth_resolver"):
                parts = tool_def.name.split(".", 2)
                if len(parts) == 3 and parts[1]:
                    try:
                        auth = await get_ext("mcp_auth_resolver")(parts[1], ctx.user_id)
                    except Exception:
                        logger.exception(
                            "mcp_auth_resolver failed for %s — calling unauthenticated",
                            tool_def.name,
                        )
                        auth = None
                    if auth is not None:
                        # The host may resolve a per-user scoped endpoint along
                        # with Vault-backed auth. Remove the reserved metadata
                        # before auth headers are built and use it only as the
                        # remote URL for this invocation.
                        resolved_auth = dict(auth)
                        endpoint = resolved_auth.pop("__matrx_mcp_endpoint_url", None)
                        updates: dict[str, Any] = {"mcp_server_auth": resolved_auth}
                        if isinstance(endpoint, str) and endpoint:
                            updates["mcp_server_url"] = endpoint
                        tool_def = tool_def.model_copy(update=updates)

        client = ExternalMCPClient(timeout=tool_def.timeout_seconds)
        return await client.call_tool(tool_def, args, ctx)

    async def _execute_agent(
        self,
        tool_def: ToolDefinition,
        args: dict[str, Any],
        ctx: ToolContext,
    ) -> ToolResult:
        from .agent_tool import execute_agent_tool

        child_ctx = ctx.model_copy(
            update={
                "recursion_depth": ctx.recursion_depth + 1,
            }
        )
        return await execute_agent_tool(tool_def, args, child_ctx)

    async def _execute_external_handler(
        self,
        tool_def: ToolDefinition,
        args: dict[str, Any],
        ctx: ToolContext,
    ) -> ToolResult:
        """Dispatch a tool call to an async handler registered by a host application.

        The handler is resolved from ``ExternalHandlerRegistry`` using a two-tier
        lookup: exact tool-name match first, then app-level (source_kind) fallback.
        If no handler is registered, a structured error is returned to the model.
        """
        from .external_handlers import invoke_external_handler

        child_ctx = ctx.model_copy(update={"tool_name": tool_def.name})
        return await invoke_external_handler(
            tool_name=tool_def.name,
            source_kind=tool_def.source_kind,
            args=args,
            ctx=child_ctx,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _has_external_handler(tool_def: ToolDefinition) -> bool:
        """Whether the host registered an external handler that can run this
        tool (exact name match, or an app-level handler for its source_kind)."""
        from .external_handlers import ExternalHandlerRegistry

        return ExternalHandlerRegistry.get_instance().has_handler(
            tool_def.name, tool_def.source_kind
        )

    def _unknown_tool_hint(
        self,
        tool_name: str,
        allowed_tools: frozenset[str] | None,
    ) -> tuple[str, str]:
        """(message, suggested_action) for an unknown tool name — did-you-mean
        over the full name vocabulary plus a bounded, closest-first list of the
        tools that are actually active for this request. Best-effort: any
        failure degrades to the plain not-registered message."""
        try:
            from matrx_ai.tools.agent_projection import list_projected_tool_names
            from matrx_ai.tools.tool_aliases import get_alias_map

            vocabulary: set[str] = set(self.registry.list_tool_names())
            vocabulary.update(get_alias_map().keys())
            vocabulary.update(list_projected_tool_names())
            active = allowed_tools if allowed_tools is not None else vocabulary
            return build_unknown_tool_hint(tool_name, vocabulary=vocabulary, active_tools=active)
        except Exception as exc:  # noqa: BLE001 — a hint must never mask the error
            vcprint(
                f"[ToolExecutor] unknown-tool hint construction failed: {exc}",
                color="yellow",
            )
            return (
                f"Tool '{tool_name}' is not registered.",
                "Check the tool name and try again. Use a valid tool from the available set.",
            )

    @staticmethod
    def _unknown_tool_result(
        tool_name: str,
        call_id: str,
        started_at: float,
        *,
        message: str | None = None,
        suggested_action: str | None = None,
    ) -> ToolResult:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="not_found",
                message=message or f"Tool '{tool_name}' is not registered.",
                suggested_action=suggested_action
                or "Check the tool name and try again. Use a valid tool from the available set.",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name=tool_name,
            call_id=call_id,
        )

    # _persist_output is no longer needed — persist_key and output are stored
    # directly in the cx_tool_call row via the unified logger.log() call.
