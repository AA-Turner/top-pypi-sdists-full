from __future__ import annotations

import asyncio
import inspect
import time
import traceback
from typing import TYPE_CHECKING, Any, Literal
from uuid import uuid4

import rich
from matrx_connect.chat_timing import chat_timing_mark
from matrx_connect.context.app_context import set_app_context
from matrx_connect.context.error_buffer import buffer_error_events
from matrx_connect.context.events import InfoPayload, ProviderRetryPayload, WarningPayload
from matrx_connect.request_controls import RequestControlRegistry
from matrx_connect.reservations import get_tracker
from matrx_utils import vcprint

from matrx_ai.config import (
    TextContent,
    ThinkingContent,
    TokenUsage,
    ToolCallContent,
    ToolResultContent,
    UnifiedConfig,
    UnifiedMessage,
    UnifiedResponse,
)
from matrx_ai.context.app_context import get_app_context
from matrx_ai.db import (
    ensure_conversation_exists,
    ensure_user_request_exists,
    update_user_request_status,
)
from matrx_ai.db.message_positions import APPEND_MESSAGE_POSITION
from matrx_ai.db.persistence import persist_completed_request
from matrx_ai.ops.issue_capture import capture_issue
from matrx_ai.orchestrator.execution_state import (
    ExecutionState,
    ExecutionStateSnapshot,
    clear_execution_state,
    set_execution_state,
)
from matrx_ai.orchestrator.loop_guard import LoopHealth, evaluate_loop_health
from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest
from matrx_ai.orchestrator.tracking import TimingUsage, ToolCallUsage
from matrx_ai.providers.errors import RetryableError, classify_provider_error
from matrx_ai.providers.snapshot_redactors import (
    DEFAULT_SNAPSHOT_REDACTORS,
    apply_redactors,
)
from matrx_ai.tools.handle_tool_calls import handle_tool_calls_v2

from .recovery_logic import handle_finish_reason

if TYPE_CHECKING:
    from matrx_ai.providers import UnifiedAIClient

# Appended to a partial assistant message when a run is interrupted mid-stream,
# so both the user and the model see exactly what happened (the turn was cut off
# before completion). Kept short and self-explanatory.
_INTERRUPT_MARKER = "\n\n[⚠️ Response interrupted by the user before completion.]"

LOCAL_DEBUG = False
PROVIDER_OVERLOAD_RETRY_DELAYS: tuple[float, ...] = (2.0, 5.0, 10.0, 30.0, 60.0)


def _is_valid_uuid_str(value: str | None) -> bool:
    """True only for a non-empty string that parses as a UUID.

    Guards the conversation-resolution contract: "" and None both mean
    "no conversation supplied" → the caller gets a freshly assigned UUID.
    """
    if not value:
        return False
    from uuid import UUID

    try:
        UUID(str(value))
    except (ValueError, AttributeError, TypeError):
        return False
    return True


def _retry_schedule(error_info: RetryableError) -> tuple[float, ...] | None:
    if error_info.retry_schedule:
        return tuple(float(delay) for delay in error_info.retry_schedule)
    raw_schedule = error_info.details.get("retry_schedule") if error_info.details else None
    if isinstance(raw_schedule, list | tuple):
        delays: list[float] = []
        for value in raw_schedule:
            if isinstance(value, int | float) and value >= 0:
                delays.append(float(value))
        return tuple(delays) if delays else None
    return None


def _max_retries_for_error(error_info: RetryableError, default_max: int) -> int:
    schedule = _retry_schedule(error_info)
    if schedule:
        return max(default_max, len(schedule))
    return default_max


def _provider_name_for_event(error_info: RetryableError, fallback: str) -> str:
    detail_provider = error_info.details.get("provider") if error_info.details else None
    if isinstance(detail_provider, str) and detail_provider:
        return detail_provider
    return fallback or "unknown"


async def _emit_provider_retry(
    *,
    exec_ctx: Any,
    current_request: AIMatrixRequest,
    error_info: RetryableError,
    provider: str,
    iteration: int,
    failed_attempt: int,
    max_retries: int,
    state: Literal["scheduled", "retrying_now", "cancelled", "suspended", "recovered"],
    retry_delay: float | None = None,
    retry_at: float | None = None,
    next_attempt: int | None = None,
) -> None:
    emitter = exec_ctx.emitter
    # THE ``retrying`` MOMENT (SPEC §5.1) — every provider retry in the
    # platform passes through this one function, so the phase is announced
    # here and nowhere else. Deliberately BEFORE the send_provider_retry
    # capability check below: an emitter that does not implement the rich
    # retry payload (the workflow emitter is one) must still show the run as
    # retrying rather than as frozen mid-token.
    from matrx_ai.orchestrator.step_phase import emit_step_phase

    if state in ("scheduled", "retrying_now"):
        await emit_step_phase("retrying", emitter)
    send_provider_retry = getattr(emitter, "send_provider_retry", None)
    if send_provider_retry is None:
        return
    request_id = current_request.request_id or getattr(exec_ctx, "request_id", None)
    actions = {}
    if request_id:
        actions = {
            "cancel": f"/ai/cancel/{request_id}",
            "retry_now": f"/ai/retry-now/{request_id}",
        }
    await send_provider_retry(
        ProviderRetryPayload(
            state=state,
            provider=_provider_name_for_event(error_info, provider),
            error_type=error_info.error_type,
            message=error_info.message,
            user_message=error_info.user_message,
            status_code=error_info.status_code,
            model=current_request.config.model,
            request_id=request_id,
            conversation_id=current_request.conversation_id
            or getattr(exec_ctx, "conversation_id", None),
            iteration=iteration,
            failed_attempt=failed_attempt,
            next_attempt=next_attempt,
            max_retries=max_retries,
            retry_delay=retry_delay,
            retry_at=retry_at,
            discard_partial_output=state == "scheduled",
            schedule=list(_retry_schedule(error_info) or ()),
            can_cancel=True,
            can_retry_now=state == "scheduled",
            actions=actions,
        )
    )


async def _wait_for_retry_or_control(request_id: str | None, delay: float) -> str:
    if not request_id or delay <= 0:
        return "elapsed"
    registry = RequestControlRegistry.get_instance()
    deadline = time.monotonic() + delay
    while True:
        if registry.is_cancelled(request_id):
            return "cancelled"
        if await registry.consume_retry_now(request_id):
            return "retry_now"
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return "elapsed"
        await asyncio.sleep(min(0.25, remaining))


def _is_request_cancelled(request_id: str | None) -> bool:
    if not request_id:
        return False
    return RequestControlRegistry.get_instance().is_cancelled(request_id)


def _is_request_interrupted(request_id: str | None) -> bool:
    if not request_id:
        return False
    return RequestControlRegistry.get_instance().is_interrupted(request_id)


def _hide_interrupted_tail(messages: list, fence: int) -> int:
    """INTERRUPT (stop-and-fork) tail hiding — the three-send-modes ruling.

    Everything appended after the last clean boundary is work the user stopped
    mid-flight: it persists (the provider call was billed in full — costs are
    KEPT) but hidden from both the user's transcript and every future model
    call: ``is_visible_to_user=False`` + ``is_visible_to_model=False``, stamped
    on the message metadata (the persist layer lifts both into their
    cx_message columns) AND as the in-memory attribute (`MessageList.sanitize`
    backstop). The whole assistant/tool tail hides as one unit so a
    ``tool_use`` is never split from its ``tool_result``. USER-role messages
    in the window (steered inbox deliveries) stay visible — the user wrote
    them; the next run answers them.
    """
    hidden = 0
    for msg in messages[max(fence, 0):]:
        role = str(getattr(msg, "role", "")).lower()
        if role.endswith("user"):
            continue
        try:
            msg.is_visible_to_model = False
        except Exception:  # noqa: BLE001 — attribute stamp is the backstop, not the contract
            pass
        meta = dict(getattr(msg, "metadata", None) or {})
        meta["is_visible_to_user"] = False
        meta["is_visible_to_model"] = False
        msg.metadata = meta
        hidden += 1
    return hidden


async def _spine_stop_reason() -> str | None:
    """Poll the host-injected runtime-spine control check (durable cross-process
    cancel / tree dollar budget / deadline / per-quantity limit). None to proceed;
    a short human reason when the tree must stop. The SECOND cancellation layer
    behind the in-process RequestControlRegistry — it reaches a loop the registry
    can't (another process/worker). Best-effort: unconfigured or a hook blip →
    None (allow), never raises."""
    try:
        from matrx_ai._ext import get_spine_control_check

        check = get_spine_control_check()
        if check is None:
            return None
        return await check()
    except Exception as exc:  # noqa: BLE001 — control polling must never break the loop
        vcprint(f"[Executor] spine control check failed (allowing): {exc}", color="yellow")
        return None


def _spine_meter_call(usage) -> None:
    """Hand one billed provider call's usage to the host-injected spine meter hook
    (detached write inside the hook — zero hot-path cost). Best-effort, never raises."""
    try:
        from matrx_ai._ext import get_spine_call_meter

        meter = get_spine_call_meter()
        if meter is not None:
            meter(usage)
    except Exception as exc:  # noqa: BLE001 — metering must never break the loop
        vcprint(f"[Executor] spine call meter failed (harmless): {exc}", color="yellow")


def _strip_ephemeral_for_storage(config: UnifiedConfig) -> None:
    """Remove transient deferred-context content from a config before persistence.

    Two pieces of state are attached on every turn by ``apply_context_objects``:
    the ephemeral manifest block on the last user message, and the Tier 1
    condensed block on ``SystemInstruction``. Both are re-attached fresh next
    turn, so they must not survive into ``cx_message`` / ``cx_conversation``.
    Idempotent — safe to call when nothing is attached.
    """
    from matrx_ai.instructions.core import SystemInstruction

    config.messages.detach_ephemeral_from_last_user()
    # The first turn's context block is part of the system prompt that becomes
    # the durable conversation prefix.  Later turns never receive a system
    # block (the host places fresh context on the user message instead).
    if config.system_prompt_frozen and isinstance(config.system_instruction, SystemInstruction):
        config.system_instruction.clear_context_block()


# ============================================================================
# PUBLIC ENTRY POINT
# ============================================================================


async def execute_ai_request(
    config: UnifiedConfig,
    max_iterations: int = 100,
    max_retries_per_iteration: int = 2,
    metadata: dict[str, Any] | None = None,
    *,
    conversation_id: str | None = None,
    store: bool | None = None,
) -> CompletedRequest:
    """The single entry point for all AI execution.

    Reads everything it needs from AppContext (set by AuthMiddleware for API
    calls, or by create_test_app_context() for local scripts):
        user_id, conversation_id, request_id, emitter, debug, parent_conversation_id

    Creates AIMatrixRequest internally — callers never construct it directly.
    Works identically whether called from:
        - An API route task function (_run_ai)
        - Agent.execute()
        - A sub-agent fork (fork_for_child_agent sets a new conversation_id)
        - An internal/workflow node (llm_to_pydantic, graph actions)
        - A local test script

    Conversation + persistence contract (identical to the API's
    ``resolve_conversation`` — see aidream/api/utils/conversation_gate_utils.py):
        - ``conversation_id`` / ``store`` passed here OVERRIDE the context. This
          is how an internal/workflow caller "tells us what it wants" exactly
          like an API request body does. When omitted, the context's values
          (or their defaults) apply.
        - Supply an id → we use it. Omit it → we ASSIGN a fresh UUID. The
          effective conversation_id is ALWAYS a valid UUID, never "" or None —
          so a cx_* FK column can never again receive an empty string.
        - ``store=True`` (default) → the conversation/request/message rows are
          persisted. ``store=False`` → ephemeral: a real UUID is still assigned
          (so stream events + the X-Conversation-ID header are accurate) but NO
          rows are written.
        The resolved values are written back onto the AppContext so every
        downstream reader (execute_until_complete, the conversation gate,
        persist_completed_request) sees one consistent, valid identity.

    Sub-agent tracking:
        There is exactly ONE cx_user_request per user action. Sub-agents
        inherit the parent's request_id via fork_for_child_agent(), so their
        cx_request rows link to the same cx_user_request. Cost aggregation
        is automatic — persist_completed_request() sums all cx_request rows
        sharing a user_request_id. Sub-agents have parent_conversation_id
        set by fork_for_child_agent() for hierarchical queries.
    """
    ctx = get_app_context()

    request_id = ctx.request_id if ctx.request_id else str(uuid4())

    # ── Resolve the conversation + persistence intent ONCE, here, for EVERY
    # caller — internal or API. Explicit args win, then the context, then the
    # default. The effective conversation_id is always a valid UUID (assigned
    # when absent), mirroring resolve_conversation's default "generate a new
    # conversation" behaviour. See the contract in the docstring above.
    effective_store = ctx.store if store is None else store
    _candidate_conv = conversation_id or ctx.conversation_id
    effective_conversation_id = (
        _candidate_conv if _is_valid_uuid_str(_candidate_conv) else str(uuid4())
    )

    # Normalize the live context so downstream reads are consistent. Mirrors
    # the API router's ctx.with_overrides(...) + set_app_context(...) step.
    if effective_conversation_id != ctx.conversation_id or effective_store != ctx.store:
        ctx = ctx.with_overrides(
            conversation_id=effective_conversation_id,
            store=effective_store,
        )
        set_app_context(ctx)

    request = AIMatrixRequest(
        conversation_id=effective_conversation_id,
        config=config,
        debug=ctx.debug,
        request_id=request_id,
        organization_id=ctx.organization_id,
        parent_conversation_id=ctx.parent_conversation_id,
        # The request context carries server-owned execution metadata such as
        # the resume claim token. Preserve it unless the caller explicitly
        # supplies a metadata object; final cx_user_request persistence is
        # derived from AIMatrixRequest.metadata.
        metadata=dict(ctx.metadata) if metadata is None else metadata,
    )
    from matrx_ai.providers import UnifiedAIClient

    return await execute_until_complete(
        request,
        UnifiedAIClient(),
        max_iterations,
        max_retries_per_iteration,
    )


def _build_skipped_tool_results(
    response: UnifiedResponse,
    health: LoopHealth,
    current_request: AIMatrixRequest,
) -> list[ToolResultContent]:
    """For every pending tool_use in ``response``, emit a matched, skipped
    ``ToolResultContent`` so the conversation log stays internally consistent.

    Anthropic specifically rejects subsequent turns when a prior assistant
    ``tool_use`` block has no paired ``tool_result``. By inserting synthetic
    skipped results we keep the conversation resumable on every provider —
    a follow-up "please continue" turn just works, with the model seeing
    explicit context that the tool calls were skipped, not silently dropped.
    """
    pending: list[ToolCallContent] = []
    for msg in response.messages:
        for content in msg.content:
            if isinstance(content, ToolCallContent):
                pending.append(content)

    if not pending:
        return []

    # Only synthesize skipped results for tool_use blocks that are NOT ALREADY
    # paired with a real ToolResultContent in the conversation. By the time the
    # loop-guard / max-iterations exit runs, the normal flow has already called
    # add_response() with this response's REAL tool_results — so re-adding the
    # whole response here is what double-persisted the final turn (the 17/18 ==
    # 19/20 duplicate). We pair-check and emit nothing when everything is
    # already resolved, which is the common case for both exit sites.
    paired: set[str] = set()
    for msg in current_request.config.messages.to_list():
        for content in getattr(msg, "content", None) or []:
            if isinstance(content, ToolResultContent):
                _tid = getattr(content, "tool_use_id", None) or getattr(content, "call_id", None)
                if _tid:
                    paired.add(_tid)

    unpaired = [tc for tc in pending if tc.id not in paired]
    if not unpaired:
        return []

    skip_text = (
        f"Skipped — loop guard paused execution. {health.reason}. Awaiting user input to resume."
    )
    return [
        ToolResultContent(
            tool_use_id=tc.id,
            call_id=tc.id,
            name=tc.name,
            content=skip_text,
            is_error=True,
        )
        for tc in unpaired
    ]


async def _exit_with_loop_guard(
    *,
    exec_ctx: Any,
    state: ExecutionState,
    current_request: AIMatrixRequest,
    response: UnifiedResponse,
    health: LoopHealth,
    iteration: int,
    trigger_position: int,
    pre_execution_message_count: int,
    debug: bool,
    status: Literal["paused_loop_guard", "max_iterations_exceeded"],
    code: str,
    user_message: str,
    extra_metadata: dict[str, Any] | None = None,
) -> CompletedRequest:
    """Graceful exit shared by the loop guard and the max-iterations backstop.

    Mirrors the truncated/stop pattern: emits ``send_phase("complete")`` and a
    ``WarningPayload`` (not error) so the FE leaves any in-progress indicator,
    inserts skipped tool_results to keep the conversation resumable, and
    persists with a status string the persistence layer recognizes.

    The assistant ``response`` is ALREADY in ``current_request`` (the normal
    flow called add_response() before this exit ran), so we must NOT re-add it
    — doing so double-persisted the final turn. We only append a tool-role
    message carrying skipped results for any tool_use that is still UNPAIRED,
    purely to keep the conversation resumable on strict providers.
    """
    skipped = _build_skipped_tool_results(response, health, current_request)
    if skipped:
        from matrx_ai.config import UnifiedMessage

        current_request.config.messages.append(UnifiedMessage(role="tool", content=skipped))

    metadata: dict[str, Any] = {
        "status": status,
        "loop_health": {
            "verdict": health.verdict,
            "reason": health.reason,
            "total_calls": health.total_calls,
            "window_size": health.window_size,
            "failures_in_window": health.failures_in_window,
            "successes_in_window": health.successes_in_window,
        },
        "iteration": iteration,
    }
    if extra_metadata:
        metadata.update(extra_metadata)

    await exec_ctx.emitter.send_phase("complete")
    await exec_ctx.emitter.send_warning(
        WarningPayload(
            code=code,
            system_message=f"Loop exit ({status}): {health.reason}",
            user_message=user_message,
            level="medium",
            recoverable=True,
            metadata=metadata,
        )
    )
    await exec_ctx.emitter.send_info(
        InfoPayload(
            code="iteration_done",
            system_message=f"Execution paused: {status}",
            user_message="",
            metadata={"iteration": iteration, "will_continue": False, "status": status},
        )
    )

    return await _finalize_and_persist(
        current_request=current_request,
        iteration=iteration,
        final_response=response,
        metadata=metadata,
        trigger_position=trigger_position,
        pre_execution_message_count=pre_execution_message_count,
        debug=debug,
        state=state,
    )


async def _suspend_for_delegation(
    *,
    exec_ctx: Any,
    state: ExecutionState,
    current_request: AIMatrixRequest,
    response: UnifiedResponse,
    iteration: int,
    pending_call_ids: list[str],
    trigger_position: int,
    pre_execution_message_count: int,
    debug: bool,
) -> CompletedRequest:
    """End the turn cleanly because one or more tool calls were delegated to the
    client and are awaiting a result.

    This is NOT a failure and NOT an abandonment. The assistant message and any
    completed server-tool results for this turn were committed durably by the
    caller's barrier; the delegated ``cx_tool_call`` rows are ``status='delegated'``
    (the durable ledger). We finalize the request so it leaves the ``running``
    state (no watchdog false-abandon) and return — control is now with the
    client. The client POSTs results to ``POST /conversations/{id}/tool_results``
    and, once no delegated rows remain, ``POST /conversations/{id}/resume``
    reconstructs the conversation and continues the loop.

    Unlike the loop-guard exit we do NOT insert synthetic skipped tool_results:
    the calls are legitimately pending and will be paired with real results by
    the time /resume rebuilds the conversation. See
    docs/tool_delegation/DELEGATION_LOOP_BUGS.md.
    """
    metadata: dict[str, Any] = {
        "status": "suspended_awaiting_client",
        "pending_call_ids": pending_call_ids,
        "iteration": iteration,
    }

    await exec_ctx.emitter.send_phase("complete")
    await exec_ctx.emitter.send_info(
        InfoPayload(
            code="suspended_awaiting_client",
            system_message=(
                f"Turn suspended — {len(pending_call_ids)} tool call(s) delegated to "
                "the client; awaiting POST /tool_results + /resume."
            ),
            user_message="",
            metadata={
                "iteration": iteration,
                "will_continue": False,
                "status": "suspended_awaiting_client",
                "pending_call_ids": pending_call_ids,
            },
        )
    )

    return await _finalize_and_persist(
        current_request=current_request,
        iteration=iteration,
        final_response=response,
        metadata=metadata,
        trigger_position=trigger_position,
        pre_execution_message_count=pre_execution_message_count,
        debug=debug,
        state=state,
    )


def _resolve_allowed_tools(config: UnifiedConfig) -> frozenset[str] | None:
    """Return the set of tool names that were actually sent to the model.

    Resolution happens against the live registry so that any tools injected
    just before the API call (structured-input CRUD tools, dynamic category
    injections, etc.) are automatically included.

    Returns ``None`` when no tools were configured for this request, which
    signals the executor to skip the allowlist check entirely.
    """
    if not config.tools:
        return None

    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    allowed: set[str] = set()

    for name_or_id in config.tools:
        resolved = registry._resolve_tool_name(name_or_id)
        if resolved:
            allowed.add(resolved)
        else:
            # Unresolved entry — keep it as-is so the guard never silently
            # blocks a tool that failed to load but whose name the model knows.
            allowed.add(name_or_id)

    # custom_tools are always allowed — they are explicitly added by the caller
    # for this specific request (inline definitions, never in the global registry).
    for ct in config.custom_tools:
        if hasattr(ct, "name") and ct.name:
            allowed.add(ct.name)

    return frozenset(allowed) if allowed else None


def _cache_prefix_tool_names(config: Any) -> tuple[str, ...]:
    """Order-preserving signature of the tools that form the cacheable prefix.

    Feeds the prompt-cache guard's Layer-1 drift check: an add/remove/reorder of
    tools mid-loop busts the provider cache prefix, so the guard needs to see the
    exact tool identity+order sent each round. Names only (not full schemas) —
    enough to catch the drift patterns that actually occur, cheap to compute.
    """
    names: list[str] = []
    for t in getattr(config, "tools", None) or []:
        names.append(str(t))
    for t in getattr(config, "custom_tools", None) or []:
        names.append(str(getattr(t, "name", t)))
    return tuple(names)


def _response_has_tool_calls(response: UnifiedResponse) -> bool:
    """Return True if the response contains at least one tool call.

    Used to decide — immediately after the provider API returns — whether
    another iteration will run.  When False, we know this is the final
    response and the UI must transition out of the "Planning next steps…"
    state instead of being told another step is coming.
    """
    messages = response.messages
    if isinstance(messages, UnifiedMessage):
        messages = [messages]
    for message in messages:
        for content in message.content:
            if isinstance(content, ToolCallContent):
                return True
    return False


def _terminal_response_problem(
    response: UnifiedResponse,
) -> tuple[str, str] | None:
    """Classify a tool-less response that has no user-visible output.

    Provider protocols may report ``finish_reason=stop`` even when the model
    emitted reasoning only. That is not a completed assistant turn: the UI
    intentionally hides reasoning, so accepting it as success makes the agent
    appear to stop without an error.

    Any non-reasoning, non-tool content block counts as visible output. Text
    must contain at least one non-whitespace character.
    """
    if _response_has_tool_calls(response):
        return None
    messages = response.messages
    if isinstance(messages, UnifiedMessage):
        messages = [messages]

    saw_pseudo_tool_syntax = False
    for message in messages:
        for content in message.content:
            if isinstance(content, ThinkingContent):
                thought = content.text or ""
                if "<tool_call" in thought or "<function=" in thought:
                    saw_pseudo_tool_syntax = True
                continue
            if isinstance(content, ToolResultContent):
                continue
            if isinstance(content, TextContent):
                if content.text.strip():
                    return None
                continue
            # Media, code-execution, and other typed result blocks are
            # user-visible even when there is no accompanying text.
            return None

    if saw_pseudo_tool_syntax:
        return (
            "unparsed_tool_call",
            "The model attempted a tool call in an unsupported format and did "
            "not produce an answer. Please retry or use another model.",
        )
    return (
        "empty_assistant_response",
        "The model ended without producing a visible answer. Please retry or "
        "use another model.",
    )


def _response_has_client_delegated_call(
    response: UnifiedResponse,
    client_tools: frozenset[str] | None,
) -> bool:
    """True if the response contains a tool_call whose name is in ``client_tools``.

    Drives the mid-loop assistant-message flush: we only need to checkpoint the
    cx_message row when this iteration is about to hand control to the client
    and suspend (potentially indefinitely). Pure server-side iterations rely on
    end-of-loop persistence as before.

    Names are compared in WIRE form: a live-parsed ``ToolCallContent.name`` is
    the provider-plane spelling (``ns__tool``) while ``client_tools`` holds
    internal names (``ns:tool``) — comparing raw spellings silently skips this
    checkpoint for any colon-named delegated tool (the executor still delegates
    correctly, but the assistant message would not be durable before the
    suspend). ``to_wire_name`` is idempotent, so plain names compare unchanged.
    """
    if not client_tools:
        return False
    from matrx_ai.config.wire_names import to_wire_name

    client_wire_names = {to_wire_name(n) for n in client_tools}
    messages = response.messages
    if isinstance(messages, UnifiedMessage):
        messages = [messages]
    for message in messages:
        for content in message.content:
            if (
                isinstance(content, ToolCallContent)
                and to_wire_name(content.name) in client_wire_names
            ):
                return True
    return False


def _response_has_live_client_delegated_call(response: UnifiedResponse) -> bool:
    """Check delegation against the current turn's live AppContext.

    Dynamic tool mutations replace the request AppContext between iterations.
    The executor's original ``exec_ctx`` remains useful for stable run identity,
    but its ``client_tools`` snapshot is stale after that drain. The durability
    checkpoint must use the live routing set or it can miss the newly delegated
    call immediately before the loop suspends for a client result.
    """
    ctx = get_app_context()
    client_tools_list = getattr(ctx, "client_tools", None) or []
    client_tools = frozenset(client_tools_list) if client_tools_list else None
    return _response_has_client_delegated_call(response, client_tools)


async def _flush_assistant_message_mid_loop(
    *,
    response: UnifiedResponse,
    current_request: AIMatrixRequest,
    exec_ctx: Any,
    reserved_messages: dict[int, str],
    parent_refs: dict[str, str],
    trigger_position: int | None = None,
    state: ExecutionState | None = None,
) -> str | None:
    """Durability checkpoint before a client-delegated tool call suspends the loop.

    Writes (or updates a reservation for) the assistant cx_message row containing
    this iteration's tool_calls, so that a subsequent server restart / SSE drop
    still leaves a fully reconstructable conversation. Returns the message_id
    used, or None if the flush was skipped (store=False, empty response).

    ALSO flushes the user trigger message reservation in the same operation when
    it is still uncommitted (the reservation INSERT-from-executor-init wrote
    ``status='pending'`` + ``content=[]``; without an UPDATE here it would stay
    that way and the watchdog would sweep it to ``status='abandoned'`` at the
    300s SLA — the exact bug live conversation
    ``e6954332-622e-4f82-af93-fda58d019100`` exhibited).  The two updates ride
    the SAME coordinator.finalize() the caller fires below, so both rows land
    durably before ``tool_delegated`` emits.

    The position is derived from ``current_request.config.messages`` BEFORE
    ``AIMatrixRequest.add_response`` has run — so it matches the position this
    assistant message will occupy in msg_list at end-of-loop persistence. That
    alignment lets ``persist_completed_request`` find our reserved id and UPDATE
    (not double-insert) the row when the loop eventually completes.
    """
    if not getattr(exec_ctx, "store", True):
        return None
    # System runs persist no cx_message rows — nothing to checkpoint mid-loop.
    if getattr(exec_ctx, "system_run", False):
        return None

    messages = response.messages
    if isinstance(messages, UnifiedMessage):
        messages = [messages]
    if not messages:
        return None

    content_blocks: list[dict[str, Any]] = []
    for msg in messages:
        if msg.is_ephemeral_only():
            continue
        storage = msg.to_storage_dict()
        if storage.get("content"):
            content_blocks.extend(storage["content"])

    position = len(current_request.config.messages.to_list())
    reserved_id = reserved_messages.get(position) or reserved_messages.get(str(position))
    tracker = get_tracker()

    # Lazy import to break the matrx_ai.persistence ↔ matrx_ai.orchestrator
    # circular import (queue_helpers needs execution_state, which is reached
    # through the orchestrator package __init__).
    from matrx_ai.persistence.queue_helpers import (
        queue_message_create,
        queue_message_update,
    )

    # ── USER TRIGGER MESSAGE: flush BEFORE the assistant so a delegate
    #    suspend can't strand it as a 'pending' reservation with empty
    #    content. The mid-loop assistant flush below advances
    #    state.committed_position past the user's position; without this
    #    block, the per-turn barrier's high-water mark filter (write_from =
    #    since_position + 1) excludes the user message from the UPDATE pass
    #    in persist_completed_request, leaving it forever as the empty
    #    reservation. Idempotent: only fires when the user message is still
    #    uncommitted (committed_position < trigger_position) and a
    #    reservation exists at trigger_position. (Live evidence: conversation
    #    e6954332-622e-4f82-af93-fda58d019100, message
    #    5fcaa7c0-aca8-4161-9106-5dbc7bd10183 — status='abandoned',
    #    content_blocks=0. Persistence contract — CLAUDE.md.)
    if (
        trigger_position is not None
        and state is not None
        and trigger_position >= 0
        and state.committed_position < trigger_position
    ):
        try:
            trigger_msg = current_request.config.messages.to_list()[trigger_position]
        except (IndexError, AttributeError):
            trigger_msg = None
        # Pre-existing messages (rebuilt from the DB — they carry their real
        # cx_message.id) and non-user trigger slots (a /resume run's trigger
        # is the rebuilt tool/assistant tail) are already durable. Flushing
        # them here used to INSERT a duplicate row at an occupied position.
        if trigger_msg is not None and getattr(trigger_msg, "id", None):
            trigger_msg = None
        if trigger_msg is not None:
            _t_role = getattr(trigger_msg, "role", None)
            _t_role_str = _t_role.value if hasattr(_t_role, "value") else _t_role
            if _t_role_str != "user":
                trigger_msg = None
        if trigger_msg is not None and trigger_msg.is_ephemeral_only():
            trigger_msg = None
        if trigger_msg is not None:
            user_reserved_id = reserved_messages.get(trigger_position) or reserved_messages.get(
                str(trigger_position)
            )
            try:
                user_storage = trigger_msg.to_storage_dict()
                user_role = user_storage.get("role", "user")
                if hasattr(user_role, "value"):
                    user_role = user_role.value
                user_content = user_storage.get("content", [])
                # This mid-loop flush bypasses persist_completed_request, so it
                # must itself lift the per-turn call-record keys (model_context /
                # tools_on_call) out of the stamped metadata into their columns —
                # otherwise a delegated-tool turn loses the call record. Lazy
                # import avoids the matrx_ai.db ↔ orchestrator import cycle.
                from matrx_ai.db.persistence import lift_promoted_message_columns

                _clean_meta, _promoted = lift_promoted_message_columns(user_storage.get("metadata"))
                _extra = dict(_promoted)
                if _clean_meta:
                    _extra["metadata"] = _clean_meta
                if user_reserved_id:
                    queue_message_update(
                        user_reserved_id,
                        role=user_role,
                        status="active",
                        content=user_content,
                        **_extra,
                    )
                else:
                    # No reservation existed — INSERT now. The end-of-loop
                    # persist_completed_request skips this position because the
                    # high-water mark is about to advance past it.
                    new_user_id = str(uuid4())
                    queue_message_create(
                        id=new_user_id,
                        conversation_id=exec_ctx.conversation_id,
                        role=user_role,
                        position=APPEND_MESSAGE_POSITION,
                        status="active",
                        content=user_content,
                        created_by=exec_ctx.user_id or None,
                        **_extra,
                    )
                    reserved_messages[trigger_position] = new_user_id
            except Exception as exc:
                vcprint(
                    f"[Executor] Mid-loop user trigger flush failed (non-fatal — "
                    f"the end-of-loop persist still tries): {exc}",
                    color="yellow",
                )

    try:
        if reserved_id:
            # Mid-loop transition for a row already INSERTed as a reservation
            # at iteration start. Coalesces with that INSERT in the flush —
            # exactly one cx_message INSERT lands per row.
            queue_message_update(
                reserved_id,
                status="active",
                content=content_blocks,
            )
            return reserved_id

        message_id = str(uuid4())
        # Mid-loop INSERT for a path that didn't reserve at iteration start
        # (client-delegated tool case). Idempotent absorption is no longer
        # needed because the coordinator coalesces duplicates at flush time
        # — but we keep the structure consistent in case a non-coordinator
        # path ever creates the row first.
        queue_message_create(
            id=message_id,
            conversation_id=exec_ctx.conversation_id,
            role="assistant",
            position=APPEND_MESSAGE_POSITION,
            status="active",
            content=content_blocks,
            created_by=exec_ctx.user_id or None,
        )
        reserved_messages[position] = message_id
        try:
            await tracker.reserve(
                emitter=exec_ctx.emitter,
                db_project="matrx",
                table="message",
                parent_refs=parent_refs,
                metadata={
                    "role": "assistant",
                    "position": position,
                    "position_kind": "logical_index",
                    "source": "mid_loop_flush",
                },
                record_id=message_id,
            )
        except Exception:
            pass
        return message_id
    except Exception as exc:
        vcprint(
            f"[Executor] Mid-loop assistant message flush failed: {exc}",
            color="yellow",
        )
        return None


async def handle_tool_calls(
    response: UnifiedResponse,
    request: AIMatrixRequest,
    iteration: int,
    message_id: str | None = None,
) -> tuple[list | None, ToolCallUsage | None, list[TokenUsage], list[str], list[str], Any]:
    """Handle tool calls from the response using Tool System V2.

    Returns (tool_results, tool_call_usage, child_token_usages,
    pending_call_ids, auto_stub_keys, handoff_outcome). auto_stub_keys are
    value-store keys whose serve-once results must be stubbed AFTER the next
    provider response consumes them (the turn-directive drain). handoff_outcome
    (a HandoffOutcome, at most one — the batch policy pre-blocks extras) means
    the loop must EXIT terminally, delivering the child's answer as the
    conversation's own response.
    child_token_usages contains TokenUsage objects from any child agent
    executions triggered by the tool calls. pending_call_ids holds call_ids that
    were delegated to the client and have no result yet — when non-empty the
    orchestrator must end the turn (suspend) instead of looping; the client's
    POST /tool_results + /resume continues it. See
    docs/tool_delegation/DELEGATION_LOOP_BUGS.md.
    """
    tool_calls = []
    messages = response.messages
    if isinstance(messages, UnifiedMessage):
        messages = [messages]

    for message in messages:
        for content in message.content:
            if isinstance(content, ToolCallContent):
                tool_calls.append(content)

    if not tool_calls:
        return None, None, [], [], [], None

    raw_calls = [
        {
            "name": tc.name,
            "arguments": tc.arguments,
            "call_id": tc.id,
        }
        for tc in tool_calls
    ]

    # Read client_tools from AppContext — populated by the agent/conversation router
    # when the caller supplied a client_tools list in the request body.
    ctx = get_app_context()
    client_tools_list = getattr(ctx, "client_tools", [])
    client_tools = frozenset(client_tools_list) if client_tools_list else None

    # Build the allowlist from what was actually sent to the model in this
    # iteration.  Resolved at call-time so any tools injected just before the
    # API call (CRUD tools, dynamic category injections, etc.) are included.
    allowed_tools = _resolve_allowed_tools(request.config)

    vcprint(tool_calls, "[AI REQUESTS HANDLE TOOL CALLS] Tool Calls", color="blue")
    vcprint(raw_calls, "[AI REQUESTS HANDLE TOOL CALLS] Raw Calls", color="blue")
    if client_tools:
        vcprint(
            list(client_tools),
            "[AI REQUESTS HANDLE TOOL CALLS] Client-delegated tools",
            color="cyan",
        )
    # Tree-wide dollar budget: dollars left for this user request's whole tree
    # (parent + every sub-agent share request_id). None when disabled/unknown,
    # which the guardrail reads as "no budget", never as "exhausted".
    from matrx_ai.orchestrator.cost_budget import remaining_budget

    cost_budget_remaining = remaining_budget(request.request_id)

    # Agent-nesting depth: a child agent's loop runs this same function, so
    # without reading the forked context's depth every ToolContext is built at
    # depth 0 and the ToolType.AGENT max_recursion_depth guardrail can never
    # fire (the pre-2026-07 unbounded-nesting defect).
    from matrx_ai.tools.models import read_agent_depth

    (
        content_results,
        child_token_usages,
        pending_call_ids,
        auto_stub_keys,
        handoff_outcome,
    ) = await handle_tool_calls_v2(
        raw_calls,
        iteration=iteration,
        cost_budget_remaining=cost_budget_remaining,
        client_tools=client_tools,
        allowed_tools=allowed_tools,
        message_id=message_id,
        recursion_depth=read_agent_depth(getattr(ctx, "metadata", None)),
    )

    results = [
        ToolResultContent(**{k: v for k, v in cr.items() if k != "error"}) for cr in content_results
    ]

    # vcprint(
    #     content_results,
    #     "[AI REQUESTS HANDLE TOOL CALLS] Content Results",
    #     color="yellow",
    # )
    tool_call_details = _tool_call_details_from_content(
        content_results,
        raw_calls=raw_calls,
    )

    tool_call_usage = ToolCallUsage(
        iteration=iteration,
        tool_calls_count=len(tool_calls),
        tool_calls_details=tool_call_details,
    )

    vcprint(
        tool_call_usage,
        "[AI REQUESTS HANDLE TOOL CALLS] Tool Call Usage",
        color="blue",
    )

    return (
        results,
        tool_call_usage,
        child_token_usages,
        pending_call_ids,
        auto_stub_keys,
        handoff_outcome,
    )


# ============================================================================
# INTERNAL HELPERS
# ============================================================================


def _assistant_text_from_response(response: UnifiedResponse | None) -> str:
    """All assistant-authored text in this turn's response (joined) — the ONLY
    text the turn-directive handler is allowed to scan (position invariant:
    a directive fence executes solely from the CURRENT turn's model output,
    never from history, user, or tool content)."""
    if response is None:
        return ""
    messages = response.messages
    if isinstance(messages, UnifiedMessage):
        messages = [messages]
    parts: list[str] = []
    for message in messages or []:
        for content in getattr(message, "content", None) or []:
            text = getattr(content, "text", None)
            if isinstance(text, str) and text:
                parts.append(text)
    return "\n".join(parts)


async def _apply_turn_directives(
    response: UnifiedResponse | None,
    current_request,
    *,
    auto_stub_keys: list[str] | None = None,
) -> None:
    """Host seam: hand THIS turn's model-authored text (+ the live config) to the
    injected turn-directive handler — the non-blocking inline-marker channel
    (e.g. a context_groom fence the model emits mid-prose without spending a
    tool call) plus the just-consumed serve-once value keys. Runs before the
    per-turn barrier so the handler's queued writes ride the same commit.
    Best-effort: never breaks the turn. The handler is invoked whenever it is
    configured (it also drains host-side pending state, e.g. a groom tool call
    queued earlier in this turn) — its no-work path must stay cheap."""
    try:
        from matrx_ai._ext import get_turn_directive_handler

        handler = get_turn_directive_handler()
    except Exception:  # noqa: BLE001 — optional seam
        return
    if handler is None:
        return
    turn_text = _assistant_text_from_response(response)
    try:
        await handler(
            turn_text=turn_text,
            config=current_request.config,
            auto_stub_keys=list(auto_stub_keys or []),
        )
    except Exception as exc:  # noqa: BLE001
        vcprint(
            f"[executor] turn directive handler failed (ignored): {type(exc).__name__}: {exc}",
            color="yellow",
        )


def _required_member_gate(
    current_request: AIMatrixRequest,
    state: "ExecutionState | None",
) -> tuple[str, Any, bool]:
    """Evaluate the designated-member predicate (C-26) at a finishing exit.

    Returns ``(action, report, is_workflow_step)`` where action is one of
    ``proceed | force | pause | fail`` (see
    ``matrx_ai.orchestrator.required_members.decide_required_member_action``).
    Pure read: stamped declaration + projection map off the active AppContext
    metadata, successful calls off ``tool_call_history``, enforceability off
    the run's own active toolset (``config.tools``) so an inherited
    declaration inside a child agent's loop never fires.
    """
    if state is None:
        return "proceed", None, False
    from matrx_connect.context.app_context import try_get_app_context

    from matrx_ai.orchestrator.required_members import (
        decide_required_member_action,
        evaluate_required_members,
    )

    ctx = try_get_app_context()
    metadata = getattr(ctx, "metadata", None) if ctx is not None else None
    report = evaluate_required_members(
        metadata,
        current_request.tool_call_history,
        active_tool_names=[
            t for t in (current_request.config.tools or []) if isinstance(t, str)
        ],
    )
    is_workflow = (
        str(getattr(ctx, "origin_class", "") or "") == "workflow" if ctx is not None else False
    )
    action = decide_required_member_action(
        report,
        already_intervened=state.required_member_intervened,
        loop_guard_intervened=state.loop_guard_intervened,
        is_workflow_step=is_workflow,
    )
    return action, report, is_workflow


async def _finalize_handoff(
    *,
    handoff_outcome: Any,
    current_request: AIMatrixRequest,
    iteration: int,
    response: UnifiedResponse,
    trigger_position: int,
    pre_execution_message_count: int,
    debug: bool,
    state: ExecutionState | None,
    exec_ctx: Any,
) -> CompletedRequest | None:
    """The terminal handoff exit (Pattern 1) — the non-suspending sibling of
    _suspend_for_delegation.

    Appends the child's final text as a SYNTHETIC assistant message in the
    caller's conversation (attributed to the child via the promoted agent_id
    column; provenance in metadata.handoff), hides the tool plumbing rows from
    the USER view (the model keeps them — that is the in-context lesson),
    commits stub + response under ONE barrier, drains the turn-boundary inbox
    (a queued user message ⇒ return None and the loop continues on top of the
    delivered answer), then finalizes 'completed' with the caller's
    structured-output parse skipped — the delivered response is the child's.
    """
    from uuid import uuid4

    config = current_request.config

    # Hide the plumbing from the USER view (model keeps everything): the tool
    # message just appended, and the textless assistant message(s) of THIS
    # response (translators may split tool_calls and text into separate
    # messages). The window is bounded to exactly what this turn contributed —
    # response messages + one tool message — never reaching into a previous
    # turn; a user message is a hard stop; the first assistant WITH text stays
    # visible (the preamble — one coherent voice).
    _turn_window = len(getattr(response, "messages", None) or []) + 1
    for msg in reversed(config.messages[-_turn_window:]):
        role = str(getattr(getattr(msg, "role", None), "value", getattr(msg, "role", None)) or "")
        if role == "user":
            break
        if role == "tool":
            msg.metadata["is_visible_to_user"] = False
        elif role == "assistant":
            has_text = any(
                isinstance(getattr(block, "text", None), str) and block.text.strip()
                for block in (msg.content or [])
            )
            if has_text:
                break
            msg.metadata["is_visible_to_user"] = False

    # The synthetic response row — the conversation's own answer. Pre-set id so
    # the client learns the durable anchor BEFORE persist (rebind).
    synthetic_id = str(uuid4())
    synthetic_metadata: dict[str, Any] = {
        "handoff": {
            "source_call_id": None,
            "child_conversation_id": handoff_outcome.child_conversation_id,
            "child_execution_id": handoff_outcome.child_execution_id,
            "agent_version_id": handoff_outcome.agent_version_id,
            "model_id": handoff_outcome.model_id,
            "value_ref_key": handoff_outcome.value_ref_key,
        }
    }
    if handoff_outcome.agent_id:
        synthetic_metadata["agent_id"] = handoff_outcome.agent_id
    synthetic_message = UnifiedMessage(
        role="assistant",
        content=[TextContent(text=handoff_outcome.final_text)],
        id=synthetic_id,
        metadata=synthetic_metadata,
    )
    synthetic_response = UnifiedResponse(messages=[synthetic_message])
    updated_request = AIMatrixRequest.add_response(
        original_request=current_request,
        response=synthetic_response,
        tool_results=None,
    )
    if state is not None:
        state.current_request = updated_request
    synthetic_position = len(updated_request.config.messages) - 1

    # Register the synthetic row on the SAME reservation channel every other
    # message uses: state.reserved_message_ids keys persistence's UPDATE to
    # this UUID, and the queued 'pending' INSERT coalesces with that UPDATE
    # into one durable row. Persistence honors NO other id source — an id
    # riding only on UnifiedMessage.id is discarded loudly (that leak is how
    # a provider "msg_*" id once became a cx_message PK).
    if state is not None:
        state.reserved_message_ids[synthetic_position] = synthetic_id
    # The pending INSERT is only queued when the registration above happened —
    # without state, persistence can't find the reservation and would mint its
    # own UUID, stranding this row as an orphaned 'pending' placeholder.
    if state is not None and getattr(exec_ctx, "store", True):
        from matrx_ai.persistence.queue_helpers import (
            get_coordinator,
            queue_message_create,
        )

        if get_coordinator() is not None:
            queue_message_create(
                id=synthetic_id,
                conversation_id=exec_ctx.conversation_id,
                role="assistant",
                position=APPEND_MESSAGE_POSITION,
                status="pending",
                content=[],
                created_by=exec_ctx.user_id or None,
            )

    # Announce the durable anchor on the existing reservation channel so the
    # FE rebinds its live bubble from the loop-start placeholder to this row.
    try:
        from matrx_connect.reservations import get_tracker

        await get_tracker().reserve(
            emitter=exec_ctx.emitter,
            db_project="matrx",
            table="message",
            parent_refs={"conversation_id": exec_ctx.conversation_id},
            metadata={
                "role": "assistant",
                "position": synthetic_position,
                "position_kind": "logical_index",
                "handoff": True,
                "agent_id": handoff_outcome.agent_id,
            },
            record_id=synthetic_id,
        )
    except Exception as exc:  # noqa: BLE001 — announce is best-effort
        vcprint(f"[handoff] reservation announce failed (ignored): {exc}", color="yellow")

    # ONE barrier for the whole handoff turn: tool_use + stub + the response.
    await _persist_turn_and_commit(
        current_request=updated_request,
        iteration=iteration,
        final_response=synthetic_response,
        trigger_position=trigger_position,
        pre_execution_message_count=pre_execution_message_count,
        debug=debug,
        state=state,
    )

    # B's answer is durable — clear the SHARED emitter's per-turn buffer so a
    # late cancel/fatal path can never harvest the same text again as an
    # "interrupt partial" (the double-persist shape).
    try:
        _reset = getattr(exec_ctx.emitter, "reset_turn_text", None)
        if _reset is not None:
            _reset()
    except Exception:  # noqa: BLE001 — best-effort hygiene
        pass

    # This batch's serve-once value reads were NEVER consumed by a provider
    # response (the loop exits terminally) — dropping the keys keeps the
    # content intact, per the consumption-time contract.
    if state is not None:
        state.pending_auto_stub_keys = []

    # The 'queue anytime' guarantee survives the terminal exit: a user message
    # queued during the handoff drains here — B's answer is already durable, so
    # the loop continues and the caller answers the NEW input on top of it.
    try:
        from matrx_ai.tools.dynamic_drain import drain_pending_injections

        _n_before = len(updated_request.config.messages)
        await drain_pending_injections(
            updated_request.config, exec_ctx, include_turn_end=True
        )
        if len(updated_request.config.messages) > _n_before:
            await exec_ctx.emitter.send_info(
                InfoPayload(
                    code="inbox_continue",
                    system_message=(
                        "Queued message(s) drained after the handoff delivered — "
                        "continuing to answer them."
                    ),
                    user_message="",
                    metadata={"iteration": iteration, "will_continue": True},
                )
            )
            return None
    except Exception as exc:  # noqa: BLE001 — a drain hiccup must not undo delivery
        vcprint(f"[handoff] inbox drain failed (ignored): {exc}", color="yellow")

    # ── REQUIRED-MEMBER GATE, handoff exit (C-26, D-38) ──────────────────
    # A successful handoff ends the caller's loop by design — the child's
    # answer already streamed and just committed, so no corrective turn is
    # possible here. What the gate guarantees instead: a handoff exit can
    # NEVER bypass the requirement and record a clean 'completed'. If a
    # required member was never successfully called (the handoff call itself
    # counts — history already includes this turn), the run finalizes with
    # the distinct skipped status (chat) or as a loud failure (workflow step).
    _handoff_meta: dict[str, Any] = {
        "finish_reason": "handoff",
        "handoff_agent_id": handoff_outcome.agent_id,
        "handoff_message_id": synthetic_id,
    }
    if state is not None:
        from matrx_connect.context.app_context import try_get_app_context as _try_ctx_rm

        from matrx_ai.orchestrator.required_members import (
            REQUIRED_MEMBER_ERROR_TYPE,
            REQUIRED_MEMBER_SKIPPED_STATUS,
            evaluate_required_members,
        )

        _rm_ctx = _try_ctx_rm()
        _rm_report = evaluate_required_members(
            getattr(_rm_ctx, "metadata", None) if _rm_ctx is not None else None,
            updated_request.tool_call_history,
            active_tool_names=[
                t for t in (updated_request.config.tools or []) if isinstance(t, str)
            ],
        )
        if not _rm_report.satisfied:
            _rm_missing = ", ".join(m.display for m in _rm_report.missing)
            _rm_is_workflow = (
                str(getattr(_rm_ctx, "origin_class", "") or "") == "workflow"
                if _rm_ctx is not None
                else False
            )
            _handoff_meta["required_members_missing"] = [
                {"agent_id": m.agent_id, "role_title": m.role_title}
                for m in _rm_report.missing
            ]
            if _rm_is_workflow:
                _rm_msg = (
                    f"This Orchestra requires member(s) [{_rm_missing}] to be "
                    f"successfully consulted before the orchestrator finishes, "
                    f"and it handed off without them. The workflow step fails."
                )
                _handoff_meta["status"] = "failed"
                _handoff_meta["error"] = _rm_msg
                _handoff_meta["error_type"] = REQUIRED_MEMBER_ERROR_TYPE
                vcprint(
                    f"🛑 Required-member gate (handoff exit): {_rm_msg}",
                    "[HANDOFF] Required Member Gate",
                    color="red",
                )
                await exec_ctx.emitter.send_error(
                    error_type=REQUIRED_MEMBER_ERROR_TYPE,
                    message=_rm_msg,
                    user_message=_rm_msg,
                )
            else:
                _handoff_meta["status"] = REQUIRED_MEMBER_SKIPPED_STATUS
                vcprint(
                    f"⚠️  Required-member gate (handoff exit): handoff delivered "
                    f"without required member(s) [{_rm_missing}] — recording "
                    f"'{REQUIRED_MEMBER_SKIPPED_STATUS}', never a clean 'completed'.",
                    "[HANDOFF] Required Member Gate",
                    color="yellow",
                )
                await exec_ctx.emitter.send_warning(
                    WarningPayload(
                        code="required_member_skipped",
                        system_message=(
                            f"Handoff delivered without required member(s) "
                            f"[{_rm_missing}] having been successfully called — "
                            f"run recorded as {REQUIRED_MEMBER_SKIPPED_STATUS}."
                        ),
                        user_message=(
                            "The orchestrator answered without consulting a required "
                            "team member, so this run is not marked complete."
                        ),
                        level="medium",
                        recoverable=True,
                        metadata={
                            "missing_members": _handoff_meta["required_members_missing"],
                            "iteration": iteration,
                        },
                    )
                )

    return await _finalize_and_persist(
        current_request=updated_request,
        iteration=iteration,
        final_response=synthetic_response,
        metadata=_handoff_meta,
        trigger_position=trigger_position,
        pre_execution_message_count=pre_execution_message_count,
        debug=debug,
        state=state,
        skip_structured_output=True,
    )


def _tool_definition_snapshot(name: str) -> dict[str, Any] | None:
    """Description + parameters the agent was given for ``name``, or None."""
    if not name:
        return None
    try:
        from matrx_ai.tools.handle_tool_calls import _resolve_call_tool_def

        tool_def = _resolve_call_tool_def(name)
    except Exception:  # noqa: BLE001 — enrichment must never break the loop
        return None
    if tool_def is None:
        return None
    snapshot: dict[str, Any] = {
        "name": getattr(tool_def, "name", name),
        "description": getattr(tool_def, "description", "") or "",
        "parameters": getattr(tool_def, "parameters", None) or {},
    }
    tool_id = getattr(tool_def, "tool_id", None)
    if tool_id:
        snapshot["tool_id"] = tool_id
    return snapshot


def _tool_call_details_from_content(
    content_results: list[dict[str, Any]],
    *,
    raw_calls: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Per-call usage details, built from each content result ITSELF (it carries
    name/call_id) — never by positional indexing into the raw model calls:
    content_results holds COMPLETED calls only (delegated ones are excluded), so
    on a mixed batch a positional zip mis-attributes every detail after the
    first delegated call (the pre-2026-07 defect).

    Failed calls are enriched with arguments, the structured error, the exact
    agent-facing error string, and a snapshot of the tool definition — so
    cx_request.tool_calls_details is enough to diagnose a failure without
    joining chat.tool_call.
    """
    args_by_call_id: dict[str, Any] = {}
    for call in raw_calls or []:
        cid = str(call.get("call_id") or call.get("id") or "")
        if cid:
            args_by_call_id[cid] = call.get("arguments") or {}

    details: list[dict[str, Any]] = []
    for cr in content_results:
        call_id = str(cr.get("call_id") or cr.get("tool_use_id") or "")
        name = str(cr.get("name") or "")
        success = not bool(cr.get("is_error", False))
        entry: dict[str, Any] = {
            "name": name,
            "id": call_id,
            "call_id": call_id,
            "success": success,
        }
        if not success:
            entry["arguments"] = args_by_call_id.get(call_id, {})
            agent_error = cr.get("content")
            if agent_error is not None and not isinstance(agent_error, str):
                try:
                    import json as _json

                    agent_error = (
                        _json.dumps(agent_error)
                        if isinstance(agent_error, dict | list)
                        else str(agent_error)
                    )
                except Exception:  # noqa: BLE001
                    agent_error = str(agent_error)
            entry["agent_error"] = agent_error
            structured = cr.get("error")
            if isinstance(structured, dict):
                entry["error"] = structured
            elif isinstance(agent_error, str) and agent_error:
                entry["error"] = {"message": agent_error}
            else:
                entry["error"] = {"message": "Unknown error"}
            definition = _tool_definition_snapshot(name)
            if definition is not None:
                entry["definition"] = definition
        details.append(entry)
    return details


def _partial_response_from_emitter(exec_ctx: Any) -> UnifiedResponse:
    """Build an assistant turn from the text streamed during THIS model call.

    Used by the terminal error paths: when a provider raises MID-STREAM (e.g. a
    safety block after some tokens), the exception is raised before the response
    is assembled, so the partial text only exists in the emitter's per-turn
    buffer (reset before every provider call). This recovers it so the partial
    answer the user already saw is persisted instead of lost. Returns an empty
    response when there is no partial text (pre-call failures). Never raises.
    """
    text = ""
    try:
        getter = getattr(getattr(exec_ctx, "emitter", None), "get_turn_text", None)
        if getter is not None:
            text = getter() or ""
    except Exception:
        text = ""
    if text.strip():
        return UnifiedResponse(
            messages=[UnifiedMessage(role="assistant", content=[TextContent(text=text)])]
        )
    return UnifiedResponse(messages=[])


def _append_partial_response(
    current_request: AIMatrixRequest,
    api_response: UnifiedResponse,
    state: ExecutionState | None,
) -> AIMatrixRequest:
    """Append a non-success response's content as a normal assistant turn.

    The ``truncated`` / ``stop`` exit paths return BEFORE the loop's normal
    ``add_response()`` call, so any text the model streamed before it was cut
    off / blocked would otherwise never be appended to ``config.messages`` and
    would be lost from persistence. This mirrors the normal append so the
    existing finalize path writes the partial turn to ``cx_message`` at its
    natural position. Best-effort — never raises (a persistence helper must
    never break the request it is trying to save).
    """
    try:
        if not getattr(api_response, "messages", None):
            return current_request
        if state is not None:
            for partial_message in api_response.messages:
                partial_role = getattr(partial_message, "role", None)
                partial_role_value = (
                    partial_role.value if hasattr(partial_role, "value") else partial_role
                )
                if partial_role_value == "assistant":
                    partial_message.metadata = {
                        **(partial_message.metadata or {}),
                        "provider_iteration": state.iteration,
                    }
        updated = AIMatrixRequest.add_response(
            original_request=current_request,
            response=api_response,
            tool_results=None,
        )
        if state is not None:
            state.current_request = updated
        return updated
    except Exception as _err:
        vcprint(
            f"[execute_until_complete] partial-content add_response failed: {_err}",
            color="yellow",
        )
        return current_request


def _record_billed_usage_on_failure(
    current_request: AIMatrixRequest,
    exc: BaseException | None,
    *,
    iteration: int | None = None,
    provider_attempt: int | None = None,
) -> None:
    """Record provider-billed usage from one failing/cancelling provider call.

    A provider bills us the instant a call starts; the charge stands even when
    the call fails or is cancelled mid-flight. The provider stamps the billed
    ``TokenUsage`` onto the exception (``attach_billed_usage``); we harvest it
    here and append it to the request's ``usage_history`` so the failed turn's
    cx_request row carries real cost instead of $0 (the cost-tracking gap where
    mid-flight rejections were billed but recorded as $0). Provider-agnostic:
    any provider that attaches gets recorded. Best-effort — never raises.

    This runs as soon as each provider attempt fails, not only when the retry
    loop gives up. The exception is marked after harvest so terminal finalizers
    can call this defensively without double-counting the same paid attempt.
    """
    try:
        from matrx_ai.providers.errors import get_billed_usage

        if exc is None or getattr(exc, "_matrx_billed_usage_recorded", False):
            return
        billed = get_billed_usage(exc)
        if billed is None:
            return
        setattr(exc, "_matrx_billed_usage_recorded", True)
        if iteration is not None:
            billed.metadata["iteration"] = iteration
        if provider_attempt is not None:
            billed.metadata["provider_attempt"] = provider_attempt
        billed.metadata["attempt_outcome"] = "failed"
        current_request.add_usage(billed)
        try:
            from matrx_ai.orchestrator.cost_budget import record_tree_cost

            record_tree_cost(current_request.request_id, billed.calculate_cost())
        except Exception:
            pass
        _spine_meter_call(billed)  # billed-on-failure spend reaches the tree too
        vcprint(
            {
                "request_id": current_request.request_id,
                "conversation_id": current_request.conversation_id,
                "iteration": iteration,
                "provider_attempt": provider_attempt,
                "input_tokens": getattr(billed, "input_tokens", None),
                "output_tokens": getattr(billed, "output_tokens", None),
            },
            "[execute_until_complete] Recorded billed failed attempt",
            color="yellow",
        )
    except Exception as _err:
        vcprint(
            f"[execute_until_complete] billed-usage harvest failed "
            f"(non-fatal, cost may under-record): {_err}",
            color="yellow",
        )


async def _finalize_and_persist(
    current_request: AIMatrixRequest,
    iteration: int,
    final_response: UnifiedResponse,
    metadata: dict[str, Any],
    trigger_position: int,
    pre_execution_message_count: int,
    conversation_id: str | None = None,
    debug: bool = False,
    state: ExecutionState | None = None,
    skip_structured_output: bool = False,
) -> CompletedRequest:
    """Build a CompletedRequest and persist it to the database.

    Every exit path from execute_until_complete() MUST call this function.
    This guarantees that no API call, no matter how it was triggered
    (route, test, agent-to-agent, internal service), is ever lost.

    The cx_conversation row already exists (created by the conversation
    gate at request entry time).  Persistence only updates it.

    Persistence is non-blocking to the caller: errors are logged
    but never propagated. The CompletedRequest is always returned.
    """
    post_count = len(current_request.config.messages)
    has_new_messages = post_count > pre_execution_message_count

    # Fetch-if-not-fetched: guarantee the DB pricing lookup is loaded BEFORE
    # accessing total_usage below (it aggregates per-model cost synchronously).
    # Without this, the first run in any non-server entry point (scripts, tests,
    # workers) computes cost against a cold cache and emits a false
    # "pricing not found" warning. See config/usage_config.ensure_pricing_lookup.
    from matrx_ai.config.usage_config import ensure_pricing_lookup

    await ensure_pricing_lookup()

    completed = CompletedRequest(
        request=current_request,
        total_usage=current_request.total_usage,
        timing_stats=current_request.timing_stats,
        tool_call_stats=current_request.tool_call_stats,
        iterations=iteration,
        final_response=final_response,
        metadata=metadata,
        trigger_message_position=trigger_position,
        result_start_position=pre_execution_message_count if has_new_messages else None,
        result_end_position=post_count - 1 if has_new_messages else None,
    )

    conv_id = conversation_id or current_request.conversation_id or None
    req_id = current_request.request_id or None

    # On failure paths, record the OUTCOME on the unit-of-work row
    # (cx_user_request), immediately, so the DB reflects the failure even if
    # full persistence below fails.
    #
    # The conversation status is a LIFECYCLE field (active|archived) — NOT a
    # per-request outcome. Writing 'error' here violated
    # cx_conversation_status_check (active|archived only), which aborted the
    # commit transaction and poisoned every sibling write (the 2026-05-23 /
    # 2026-05-24 user-message-loss incident). The failure belongs on
    # cx_user_request.status='failed' + error, where get_conversation_data
    # surfaces it via incomplete_requests. The conversation stays 'active'.
    # See docs/persistence/STATUS_AND_ERROR_FIELDS.md.
    if metadata.get("status") == "failed":
        if req_id:
            await update_user_request_status(
                req_id,
                "failed",
                error=metadata.get("error"),
            )

    # Turn-directive scan for the FINAL response (the no-tool-calls exit never
    # passes the mid-loop scan): a groom fence in the model's closing text still
    # applies, and the last batch's serve-once keys drain here too — the final
    # response consumed them. On a FAILED finalize the model may never have
    # seen those results, so auto-stubs are skipped (fence grooms still apply).
    # A handoff finalize (skip_structured_output=True) passes final_response=
    # the CHILD's text — never scan it as the CALLER's turn-authored directives
    # (a groom fence the child wrote grooms ITS conversation, already applied
    # by the child's own finalize); the handler still runs so tool-queued
    # grooms from the caller's turn drain.
    _final_auto_stubs: list[str] = []
    if state is not None and metadata.get("status") != "failed":
        _final_auto_stubs = list(state.pending_auto_stub_keys or [])
        state.pending_auto_stub_keys = []
    await _apply_turn_directives(
        None if skip_structured_output else final_response,
        current_request,
        auto_stub_keys=_final_auto_stubs,
    )

    # Strip keep_fresh structured input blocks from the last user message before
    # persisting. These blocks are re-fetched on every turn so we never store
    # stale resolved content in the DB. The block's structural definition
    # (type, IDs, keep_fresh=True) is preserved via to_storage_dict() so the
    # next turn knows to re-fetch them.
    completed.request.config.messages.strip_keep_fresh_from_last_user()

    # Strip the deferred-context ephemeral block from the last user message and
    # the injected Tier 1 context block from the system instruction. Both are
    # re-attached fresh on every turn by apply_context_objects() — we never
    # want stale or duplicated context surviving in the DB.
    _strip_ephemeral_for_storage(completed.request.config)

    # Persist the request-level rollup, then COMMIT synchronously at the
    # barrier. Per the persistence contract (CLAUDE.md): a failed commit is
    # NOT "non-fatal" — it STOPS THE REQUEST. We do not swallow it. The
    # per-turn barriers already committed each turn's messages/cost; this final
    # pass writes the cx_user_request rollup (is_final=True) and commits it.
    # PersistenceBarrierError propagates to the streaming handler, which emits
    # fatal_error to the client and records system_error. (The cancel path
    # wraps this call in its own shielded, watchdog-backstopped handler.)
    await persist_completed_request(
        completed,
        conversation_id=conv_id,
        debug=debug,
        state=state,
        since_position=state.committed_position if state is not None else None,
        since_iteration=state.committed_iteration if state is not None else None,
        is_final=True,
    )
    from matrx_ai.persistence.queue_helpers import get_coordinator as _get_coord

    _coord = _get_coord()
    if _coord is not None:
        await _coord.finalize(reason="request_final_commit")

    # Authoritative cost rollup. After this owner's final commit, every
    # cx_request row sharing user_request_id is durable — the parent's turns AND
    # every sub-agent's (child coordinators committed on join). Re-SUM them into
    # cx_user_request so the one-user-click total reflects the whole tree, never
    # just the last finalize's contribution (the in-memory last-write-wins
    # clobber). Owner-only: a sub-agent (parent_request_id set) skips this — only
    # the request owner sees the complete set of rows. Idempotent + non-fatal.
    from matrx_connect import try_get_app_context as _try_ctx_for_rollup

    _rollup_ctx = _try_ctx_for_rollup()
    _is_request_owner = _rollup_ctx is None or not getattr(_rollup_ctx, "parent_request_id", None)
    if _is_request_owner and req_id and _is_valid_uuid_str(req_id):
        from matrx_ai.db.persistence import apply_authoritative_user_request_rollup

        await apply_authoritative_user_request_rollup(req_id)

        # The whole tree is durable and rolled up — drop its tree-wide dollar
        # budget accumulator so the process-local map can't grow without bound.
        # Owner-only: a sub-agent must NOT release the shared accumulator while
        # siblings may still be spending against it.
        from matrx_ai.orchestrator.cost_budget import release_tree_budget

        release_tree_budget(req_id)

    if state is not None:
        state.persisted = True
        if completed.result_end_position is not None:
            state.committed_position = max(state.committed_position, completed.result_end_position)

    # Single chokepoint for STRUCTURED_OUTPUT emission. Every exit path from
    # the orchestrator passes through here, so any execution whose config
    # carries a json_schema response_format envelope produces exactly one
    # structured_output event — regardless of which route, agent, or sub-
    # agent triggered the run. Never raises; emission errors degrade silently.
    # A terminal handoff SKIPS both: the delivered response is the CHILD's
    # (whose own run already parsed its schema and dispatched its directives) —
    # parsing it against the CALLER's schema would be wrong on both sides.
    if not skip_structured_output:
        parsed_output = await _emit_structured_output_if_schema(completed)

        # Same chokepoint, the durable side-effect seam: if a host dispatcher is
        # configured and the parsed output is an object, hand it over so an
        # apply-envelope can be applied (e.g. create a project tree) before the
        # stream closes. Awaited (so it has the last word) but never fatal.
        await _apply_output_directive_if_present(parsed_output)

    return completed


async def _persist_turn_and_commit(
    *,
    current_request: AIMatrixRequest,
    iteration: int,
    final_response: UnifiedResponse,
    trigger_position: int,
    pre_execution_message_count: int,
    debug: bool,
    state: ExecutionState,
) -> None:
    """Per-turn commit barrier — durably commit THIS turn's new rows.

    Called at the end of every iteration (and before a client-delegated tool
    suspends). Persists only the cx_message / cx_request rows produced ABOVE
    the high-water-mark (``state.committed_position`` / ``committed_iteration``),
    then COMMITS them synchronously via ``coordinator.finalize()`` — which
    RAISES ``PersistenceBarrierError`` on failure. On success it advances the
    cursors so the next barrier starts above what is now durable.

    This is the heart of the persistence contract (CLAUDE.md): each turn is
    durable the moment its data is complete, and a failed commit STOPS the run
    rather than silently losing data. A mid-run crash/kill therefore loses at
    most the single in-flight turn, never the whole conversation.
    """
    post_count = len(current_request.config.messages)
    # Nothing new beyond what a prior barrier already committed.
    if post_count - 1 <= state.committed_position:
        return

    # Fetch-if-not-fetched: ensure the DB pricing lookup is loaded before the
    # total_usage cost aggregation runs (see ensure_pricing_lookup docstring).
    from matrx_ai.config.usage_config import ensure_pricing_lookup

    await ensure_pricing_lookup()

    completed = CompletedRequest(
        request=current_request,
        total_usage=current_request.total_usage,
        timing_stats=current_request.timing_stats,
        tool_call_stats=current_request.tool_call_stats,
        iterations=iteration,
        final_response=final_response,
        metadata={"finish_reason": getattr(final_response, "finish_reason", None)},
        trigger_message_position=trigger_position,
        result_start_position=pre_execution_message_count,
        result_end_position=post_count - 1,
    )
    conv_id = current_request.conversation_id or None

    # Queue ONLY this turn's new rows (scoped by the high-water-mark), then
    # commit them in one transaction. is_final=False skips the request-level
    # cx_user_request rollup — that is derived once on the final commit (and on
    # cancel), and is always recomputable from the per-iteration cx_request rows.
    from matrx_ai.persistence.queue_helpers import get_coordinator

    coord = get_coordinator()

    # 1. QUEUE this turn's new rows into the current Session FIRST. If the prior
    #    turn's commit turns out to have failed (detected in step 2), this turn's
    #    just-streamed data is already in the Session, so the degrade-drain
    #    secures it instead of losing it. (Persistence contract — CLAUDE.md.)
    await persist_completed_request(
        completed,
        conversation_id=conv_id,
        debug=debug,
        state=state,
        since_position=state.committed_position,
        since_iteration=state.committed_iteration,
        is_final=False,
    )

    # 2. ACCOUNTABILITY: confirm the PRIOR turn's fired commit actually landed
    #    before firing another on top of it. A prior failure or overdue commit
    #    blows up here → the except handler degrade-drains (securing THIS turn's
    #    queued data) then surfaces fatal_error. The "turn 27 failed ⇒ turn 28
    #    stops" guarantee.
    if coord is not None:
        await coord.check_pending()

    # 3. FIRE this turn's commit (non-blocking) and roll a fresh Session. It runs
    #    on its own DB connection and overlaps the next model call; the NEXT
    #    turn's check_pending verifies it landed. A queue-time drop blows up now.
    #
    #    BACKPRESSURE FIRST: background commits are capped process-wide (pool
    #    budget). Under legitimate fan-out — N parallel agent invocations in one
    #    workflow super-step, each its own Coordinator — that budget is
    #    momentarily full while healthy ms-scale commits drain. WAIT for a slot
    #    (bounded) instead of failing a healthy request; if the wait expires the
    #    commits truly are not draining and commit_async raises the barrier
    #    error, unchanged. Nothing proceeds unconfirmed either way.
    if coord is not None:
        await coord.acquire_commit_slot()
        coord.commit_async(reason=f"turn_{iteration}_commit")

    # Advance the high-water-mark optimistically — we fired the commit; the next
    # barrier's check_pending verifies it landed (and stops the run if it didn't).
    state.committed_position = post_count - 1
    state.committed_iteration = max(state.committed_iteration, iteration)


async def _degrade_and_secure(*, reason: str) -> list[str]:
    """DATA FIRST on any anomaly — synchronously flush the cache and drain all
    in-flight commits BEFORE error-handling or unwinding. The instant something
    is wrong, speed stops mattering; zero data loss is the only priority. The
    fast-path write-behind switches OFF here. Best-effort: never raises (failures
    are captured to system_write_failure). Returns failure descriptions. See the
    degrade-to-synchronous rule in CLAUDE.md."""
    from matrx_ai.persistence.queue_helpers import get_coordinator

    coord = get_coordinator()
    if coord is None:
        return []
    try:
        return await coord.drain_and_confirm(reason=reason)
    except Exception as exc:  # noqa: BLE001 — the panic flush must never crash the unwind
        vcprint(
            f"[execute_until_complete] degrade drain raised unexpectedly: "
            f"{type(exc).__name__}: {exc}. Watchdog backstop.",
            color="red",
        )
        return [f"degrade_drain:{type(exc).__name__}:{exc}"]


async def _emit_structured_output_if_schema(completed: CompletedRequest) -> Any:
    """Parse the final assistant text against config.response_format and emit.

    Fires only when ``response_format`` is the OpenAI ``json_schema`` envelope
    (``{type: "json_schema", json_schema: {...}}``). Other shapes (``json_object``,
    None, etc.) skip emission — they're not contracts the frontend can render.

    Returns the parsed structured-output object on success (so the caller can
    feed it to the output-apply dispatcher without re-parsing), else ``None``.
    """
    try:
        rf = getattr(completed.request.config, "response_format", None)
        if not isinstance(rf, dict) or rf.get("type") != "json_schema":
            return None

        envelope = rf.get("json_schema")
        if not isinstance(envelope, dict):
            return None

        schema = envelope.get("schema") if isinstance(envelope.get("schema"), dict) else envelope
        if not isinstance(schema, dict):
            return None

        from matrx_connect import try_get_app_context
        from matrx_connect.context.events import StructuredOutputPayload

        from matrx_ai.agents.output import parse_agent_output

        ctx = try_get_app_context()
        emitter = getattr(ctx, "emitter", None) if ctx else None
        # THE ``finalizing`` MOMENT (SPEC §5.1) — the tokens have stopped and
        # the answer is being parsed and validated against its schema. On a big
        # structured answer this is seconds of dead air right where the user is
        # most likely to think the run hung, so it is announced before the
        # parse, independent of whether this emitter can carry the rich
        # structured-output payload below.
        from matrx_ai.orchestrator.step_phase import emit_step_phase

        await emit_step_phase("finalizing", emitter)
        if emitter is None or not hasattr(emitter, "send_structured_output"):
            return None

        final_text = completed.request.config.get_last_output() or ""
        extraction = parse_agent_output(final_text, envelope)
        contract_meta = (
            (ctx.metadata or {}).get("structured_output_content_ir", {})
            if isinstance(getattr(ctx, "metadata", None), dict)
            else {}
        )
        contract_kind = (
            contract_meta.get("kind") if isinstance(contract_meta, dict) else None
        )
        kind_errors = (
            [] if extraction.success else [extraction.reason or "schema mismatch"]
        ) if contract_kind else []
        payload = StructuredOutputPayload(
            schema_name=envelope.get("name") if isinstance(envelope.get("name"), str) else None,
            json_schema=schema,
            data=extraction.data if extraction.success else None,
            success=extraction.success,
            reason=extraction.reason,
            match_count=len(extraction.all_matches),
            agent_name=getattr(ctx, "agent_id", None),
            operation_id=getattr(ctx, "operation_id", None) or None,
            kind=contract_kind,
            kind_version=(
                contract_meta.get("version") if isinstance(contract_meta, dict) else None
            ),
            kind_checked=contract_kind is not None,
            kind_errors=kind_errors,
        )
        await emitter.send_structured_output(payload)
        return extraction.data if extraction.success else None
    except Exception as exc:
        vcprint(
            f"[Orchestrator] structured_output emission failed: {exc}",
            color="yellow",
        )
        return None


async def _apply_output_directive_if_present(parsed: Any) -> None:
    """Hand a parsed structured output to the host's output-apply dispatcher.

    The structured-output → durable side-effect seam. Fires only when (a) a
    dispatcher is configured via ``matrx_ai.configure(matrx_directives_dispatcher=…)``
    and (b) the parsed output is a non-empty object. matrx-ai stays agnostic:
    it does NOT know the reserved apply key — the host dispatcher owns the
    early-return and the directive registry.

    Awaited so the side effect lands before the stream closes (it "has the last
    word"), but NEVER raises: a dispatch failure must not turn a delivered AI
    response into a failed request. The host already reports its own failures
    to the client as warnings; this try/except is the backstop.
    """
    try:
        if not isinstance(parsed, dict) or not parsed:
            return

        from matrx_ai._ext import get_matrx_directives_dispatcher

        dispatcher = get_matrx_directives_dispatcher()
        if dispatcher is None:
            return

        from matrx_connect import try_get_app_context

        ctx = try_get_app_context()
        if ctx is None:
            return

        await dispatcher(parsed=parsed, ctx=ctx)
    except Exception as exc:
        vcprint(
            f"[Orchestrator] output-apply dispatch failed (non-fatal): {type(exc).__name__}: {exc}",
            color="yellow",
        )


# ============================================================================
# CONVERSATION LABELING — fires once per new conversation, from any call path
# ============================================================================


def _schedule_labeling_if_new(exec_ctx: Any, config: UnifiedConfig) -> None:
    """Schedule labeling for new conversations only.

    Called immediately after ensure_conversation_exists() inside
    execute_until_complete(), which means it covers every possible
    call path: API routes, direct test scripts, sub-agents, internal
    services — anything that ultimately calls execute_ai_request().

    Labeling only needs the initial user input, so it fires before
    the AI runs. We skip it when:
      - conversation_id or user_id is missing
      - the conversation already has messages from prior turns (continuation)
    """
    try:
        from matrx_ai.agents.services.conversation_labeler import schedule_conversation_labeling
        from matrx_ai.config.message_config import MessageList

        if not exec_ctx.store:
            return
        # System runs are throwaway machine transcripts — never title them
        # (and never spend another LLM call doing it).
        if getattr(exec_ctx, "system_run", False):
            return

        # Client host: the labeler writes its title through the cx_ ORM
        # tables (cxm), which don't exist here. Titling is the host's job
        # until the ConversationStore protocol grows a set_title seam.
        from matrx_ai.client_host import get_conversation_store

        if get_conversation_store() is not None:
            return

        conversation_id = exec_ctx.conversation_id
        user_id = exec_ctx.user_id

        if not conversation_id or not user_id:
            return

        # Skip labeler for sub-agent (child) conversations — internal scratch
        # threads that must not be titled. The labeler is fire-and-forget and
        # can race the child's queued conversation INSERT. conversation_type is
        # the durable source of truth (any non-standard type is internal);
        # is_internal_agent / parent_conversation_id remain as belt-and-suspenders.
        from matrx_ai.agents.conversation_type import is_internal_conversation

        if is_internal_conversation(exec_ctx):
            return
        if getattr(exec_ctx, "parent_conversation_id", None):
            return

        raw_messages = config.messages
        if not raw_messages:
            return

        # Only label on the first turn — if there are already more than a couple
        # of messages (user + assistant from a prior turn), this is a continuation.
        if len(raw_messages) > 3:
            return

        if isinstance(raw_messages, MessageList):
            messages: list[dict] = raw_messages.to_dict_list()
        else:
            messages = [m if isinstance(m, dict) else m for m in raw_messages]

        agent_name: str | None = exec_ctx.metadata.get("agent_name") or None
        agent_description: str | None = exec_ctx.metadata.get("agent_description") or None

        user_prompt: str | None = None
        user_variables: dict | None = None
        if agent_name:
            # Project picklist envelopes to their public label so the title generator never
            # sees the reference dict (and could never see the secret description either,
            # which only ever exists in the wire clone).
            user_variables = _project_picklist_labels(exec_ctx.initial_variables) or None
            for msg in reversed(messages):
                if isinstance(msg, dict) and msg.get("role") == "user":
                    content = msg.get("content", "")
                    user_prompt = content if isinstance(content, str) else str(content)
                    break

        schedule_conversation_labeling(
            conversation_id=conversation_id,
            user_id=user_id,
            messages=messages,
            agent_name=agent_name,
            agent_description=agent_description,
            user_variables=user_variables,
            user_prompt=user_prompt,
        )

        # Phase B — universal auto-ingest seam. The host (aidream) injects a
        # post-finalize hook via matrx_ai.configure(post_finalize_hook=...).
        # We invoke it best-effort, next to the labeler, mirroring the same
        # fire-and-forget discipline. matrx-ai never imports aidream — the
        # hook is opaque. The host implementation schedules its own
        # detached_task and returns immediately, so this never blocks the
        # orchestrator. Sub-agent conversations are already short-circuited
        # above (parent_conversation_id guard), so the hook only sees
        # user-visible threads.
        try:
            from matrx_ai._ext import get_post_finalize_hook

            hook = get_post_finalize_hook()
            if hook is not None:
                organization_id = getattr(
                    exec_ctx, "organization_id", None
                ) or exec_ctx.metadata.get("organization_id")
                hook(
                    conversation_id=conversation_id,
                    user_id=user_id,
                    organization_id=organization_id,
                    messages=messages,
                    is_continuation=len(raw_messages) > 3,
                )
        except Exception as hook_exc:
            vcprint(
                f"[Executor] post_finalize_hook failed (non-fatal): {hook_exc}",
                color="yellow",
            )
    except Exception as exc:
        vcprint(
            f"[Executor] Failed to schedule labeling (non-fatal): {exc}",
            color="yellow",
        )


def _project_picklist_labels(variables: dict | None) -> dict | None:
    """Return a copy of ``variables`` with any picklist reference envelope replaced by its
    public label (single) or comma-joined labels (multi-select). Plain values pass through.
    Used so the conversation labeler renders human text, never the reference dict."""
    if not variables:
        return variables
    from matrx_ai.config.picklist_runtime import is_picklist_ref

    out: dict = {}
    for name, value in variables.items():
        if is_picklist_ref(value):
            out[name] = value.get("label") or ""
        elif isinstance(value, list) and any(is_picklist_ref(v) for v in value):
            out[name] = ", ".join(
                (v.get("label") or "") if is_picklist_ref(v) else ("" if v is None else str(v))
                for v in value
            )
        else:
            out[name] = value
    return out


# ============================================================================
# REQUEST SNAPSHOT (always-on; AppContext.snapshot is a per-request override)
# ============================================================================


def _json_safe(value: Any) -> Any:
    """Best-effort coercion of arbitrary provider payload values into
    JSON-serializable structures so they can be written to a jsonb column.

    Never raises — any value that cannot be coerced falls back to its
    ``repr()``. This is a debugging/audit artifact, not production data, so
    approximate fidelity is acceptable.
    """
    if value is None or isinstance(value, str | int | float | bool):
        return value
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, list | tuple | set | frozenset):
        return [_json_safe(v) for v in value]
    # Pydantic v2 models
    if hasattr(value, "model_dump"):
        try:
            return _json_safe(value.model_dump(mode="python"))
        except Exception:
            pass
    # Matrx config objects
    if hasattr(value, "to_dict"):
        try:
            return _json_safe(value.to_dict())
        except Exception:
            pass
    # Dataclasses.
    #
    # NOT dataclasses.asdict(): it deep-copies every leaf, so ONE un-copyable
    # value anywhere inside (a provider SDK object parked in TokenUsage's
    # raw_usage, say) raises and drops the WHOLE object through to repr()
    # below. That is not hypothetical — it is how 2,049 of 5,473 production
    # response snapshots (37.4%) came to store `usage` as the string
    # "TokenUsage(input_tokens=9443, ...)" instead of an object, losing all 14
    # fields of a billing-relevant audit record.
    #
    # Walking the fields ourselves keeps the recursion under _json_safe's own
    # per-value fallbacks, so an un-copyable leaf degrades to repr() AT THE
    # LEAF and every sibling field survives as structure.
    try:
        import dataclasses as _dc

        if _dc.is_dataclass(value) and not isinstance(value, type):
            return {f.name: _json_safe(getattr(value, f.name, None)) for f in _dc.fields(value)}
    except Exception:
        pass
    # Bytes — record size only, not contents
    if isinstance(value, bytes | bytearray | memoryview):
        return f"<{type(value).__name__} len={len(bytes(value))}>"
    try:
        return repr(value)
    except Exception:
        return f"<unrepresentable {type(value).__name__}>"


# ── CAPTURE DEFAULT (a CAPS constant, NEVER an env var) ──────────────────
# Snapshot capture is ALWAYS-ON: every persisted orchestrator iteration writes
# its exact provider request/response to ``chat.request_snapshot`` unless the
# request explicitly opts out. That is the whole point — a snapshot is the
# input half of replay, and a capture you have to remember to ask for is a
# regression case you don't have (measured 2026-08-15: podcast runs, the
# highest-value multi-stage pipeline we own, had never opted in).
#
# It is a constant, not an env var, for the reason the root CLAUDE.md gives:
# a behaviour flag that is unset on one server fails SILENTLY there — capture
# would simply be dead in production with nothing broken and nothing logged.
# Changing this takes a code push, which is the point. Same rule as the CAPS
# in aidream/services/snapshot_retention/types.py, which is what makes this
# flip affordable (180-day retention + pin-on-reference) and observable
# (durable capture-failure counter + assist chip above threshold).
#
# Per-request ``ctx.snapshot`` remains an OVERRIDE, now tri-state:
#   None  → this default (ON)
#   True  → force ON, and additionally arm the wire-level outbound capture
#           stream events (``providers/outbound_capture.py``) for debugging
#   False → explicit opt-out; this request writes no snapshot
# Ephemeral runs (``store=False``) never write, independent of any of the
# above — that is a hard invariant, not a volume knob
# (tests/test_request_snapshot_store_gate.py).
REQUEST_SNAPSHOT_CAPTURE_DEFAULT: bool = True


def _request_snapshot_enabled(exec_ctx: Any) -> bool:
    """Should THIS request's successful iterations write a snapshot?

    Layer 1 of the store gate (layer 2 is inside ``_write_request_snapshot``,
    which is what the forcing-function test pins). Both are independently
    sufficient; this one also saves the payload-copy work on ephemeral runs.
    """
    if not getattr(exec_ctx, "store", True):
        return False
    explicit = getattr(exec_ctx, "snapshot", None)
    if explicit is not None:
        return bool(explicit)
    return REQUEST_SNAPSHOT_CAPTURE_DEFAULT


# The durable identity of a capture failure. Snapshot capture is best-effort by
# design (it must NEVER perturb a live request), which means a broken capture
# path produces exactly zero user-visible symptoms while replay, hindsight and
# the regression suite quietly lose their inputs. So every swallowed failure
# also lands one ``system_error`` row under this kind — that row IS the counter
# the alarm reads. Import this constant rather than re-typing the string: the
# consumer (aidream/services/snapshot_retention/capture_health.py) counts rows
# by it, and a typo on either side means an alarm that can never fire.
REQUEST_SNAPSHOT_CAPTURE_FAILURE_KIND = "request_snapshot_capture_failure"
TERMINAL_PROVIDER_FAILURE_KIND = "provider_request_failed"
MESSAGE_SANITIZATION_FAILURE_KIND = "message_sanitization_failed"
PROVIDER_USAGE_MISSING_KIND = "provider_usage_missing"
TRUNCATED_RESPONSE_KIND = "provider_response_truncated"


async def _capture_missing_provider_usage(
    *, exec_ctx: Any, current_request: AIMatrixRequest, provider: str, iteration: int
) -> None:
    """Capture a successful provider call that returned no billable usage."""
    from matrx_connect.streaming.error_capture import capture_error

    exc = RuntimeError("Successful provider response did not include usage data")
    await capture_error(
        exc,
        kind=PROVIDER_USAGE_MISSING_KIND,
        request_id=current_request.request_id or getattr(exec_ctx, "request_id", None),
        user_id=getattr(exec_ctx, "user_id", None),
        conversation_id=current_request.conversation_id
        or getattr(exec_ctx, "conversation_id", None),
        route="orchestrator/provider_response",
        error_type=type(exc).__name__,
        payload={"provider": provider, "model": current_request.config.model, "iteration": iteration},
    )


async def _capture_truncated_response(
    *, exec_ctx: Any, current_request: AIMatrixRequest, iteration: int
) -> None:
    """Record a user-visible token-limit truncation without retaining content."""
    from matrx_connect.streaming.error_capture import capture_error

    model = current_request.config.model or "unknown model"
    exc = RuntimeError(f"Model {model!r} reached its output token limit")
    await capture_error(
        exc,
        kind=TRUNCATED_RESPONSE_KIND,
        request_id=current_request.request_id or getattr(exec_ctx, "request_id", None),
        user_id=getattr(exec_ctx, "user_id", None),
        conversation_id=current_request.conversation_id
        or getattr(exec_ctx, "conversation_id", None),
        route="orchestrator/provider_response",
        error_type="truncated_response",
        payload={
            "model": model,
            "max_output_tokens": current_request.config.max_output_tokens,
            "iteration": iteration,
        },
    )


async def _capture_terminal_provider_failure(
    exc: BaseException,
    *,
    exec_ctx: Any,
    current_request: AIMatrixRequest,
    error_info: RetryableError,
    provider: str,
    iteration: int,
    retry_attempt: int,
) -> None:
    """Put a terminal provider exception in the structured repair queue."""
    from matrx_connect.streaming.error_capture import capture_error

    # A sanitation refusal happens before the SDK call. Give it its own repair
    # class instead of laundering it into a provider outage.
    kind = (
        MESSAGE_SANITIZATION_FAILURE_KIND
        if error_info.error_type == "message_sanitization_error"
        else TERMINAL_PROVIDER_FAILURE_KIND
    )
    await capture_error(
        exc,
        kind=kind,
        request_id=current_request.request_id or getattr(exec_ctx, "request_id", None),
        user_id=getattr(exec_ctx, "user_id", None),
        conversation_id=current_request.conversation_id
        or getattr(exec_ctx, "conversation_id", None),
        route="orchestrator/provider_request",
        error_type=error_info.error_type,
        payload={
            "provider": _provider_name_for_event(error_info, provider),
            "model": current_request.config.model,
            "status_code": error_info.status_code,
            "iteration": iteration,
            "retry_attempt": retry_attempt,
        },
    )


async def _record_snapshot_capture_failure(exc: BaseException, context: dict[str, Any]) -> None:
    """Durably count one swallowed snapshot-capture failure. Never raises.

    Await the host-injected ``record_error`` seam (the same seam
    picklist_runtime uses) so the already-detached snapshot task cannot finish
    before its failure record does. With no host configured this is a no-op and
    capture stays exactly as best-effort as before.
    """
    try:
        from matrx_ai._ext import get_ext  # local import to avoid import cycles

        record_error = get_ext("record_error")
    except Exception:
        record_error = None
    if record_error is None:
        return
    try:
        result = record_error(
            exc,
            kind=REQUEST_SNAPSHOT_CAPTURE_FAILURE_KIND,
            error_type=f"{type(exc).__module__}.{type(exc).__qualname__}",
            error_text=f"request_snapshot capture failed: {exc or type(exc).__name__}",
            route="request_snapshot_capture",
            payload=context,
        )
        if inspect.isawaitable(result):
            await result
    except Exception:
        # Counting a failure must never become a second failure.
        pass


async def _write_request_snapshot(
    *,
    exec_ctx: Any,
    iteration: int,
    api_response: UnifiedResponse | None,
    request_payload: Any,
    unified_payload: Any,
    trigger_position: int,
    first_assistant_position: int,
    state_snapshot: ExecutionStateSnapshot,
    error_payload: Any = None,
    provider: str | None = None,
    model: str | None = None,
) -> None:
    """Persistence of the full provider request/response for one iteration.

    On the SUCCESS path this is fire-and-forget and gated by
    ``_request_snapshot_enabled`` (always-on default + per-request
    opt-out; see ``REQUEST_SNAPSHOT_CAPTURE_DEFAULT``). On the
    PROVIDER-CALL-FAILURE path (``api_response is None`` + ``error_payload``
    set) the caller invokes it UNCONDITIONALLY — a failed request's payload is
    always worth persisting. Ephemeral runs (``exec_ctx.store=False``) NEVER
    write: no conversation/user_request parent is created, so a snapshot INSERT
    is a permanent ``request_snapshot_conversation_id_fkey`` orphan. Never
    raises — snapshotting is best-effort and must not affect the live request.

    Two payload columns are written:
      * ``request_payload`` — the provider-translated SDK-ready dict captured
        by the provider's ``capture_request_payload`` just before the SDK call.
        This is what literally hits the wire.
      * ``unified_payload`` — the matrx-canonical ``AIMatrixRequest.to_dict()``
        captured immediately before ``client.execute()``. Same logical moment,
        different representation: tools as IDs/specs, messages as UnifiedMessage,
        ``system_instruction`` as a string. Easier to read and diff than the
        provider shape.

    Both go through the same redactor pipeline.

    ``state_snapshot`` is a frozen copy of ``ExecutionState`` taken at task-
    creation time so this background coroutine never reads dicts the main
    loop is still mutating.
    """
    try:
        # Ephemeral (store=False): no cx_conversation / cx_user_request is ever
        # created — writing a snapshot would FK-fail forever and spam replay.
        if not getattr(exec_ctx, "store", True):
            return
        if not request_payload and not unified_payload and not error_payload:
            return

        cx_request_id = state_snapshot.reserved_request_ids.get(iteration)
        trigger_message_id = state_snapshot.reserved_message_ids.get(trigger_position)
        response_message_id = state_snapshot.reserved_message_ids.get(first_assistant_position)

        model_name = model or state_snapshot.last_model or None
        provider_name = provider or ""
        # Best signal we have for provider — explicit arg (both call sites pass
        # it now), else api_response metadata. The metadata keys are the
        # PROVIDER's own vocabulary: nobody stamps a bare "provider"/"model",
        # they stamp ``matrx_model_name`` / ``provider_model_name``. Reading
        # only the bare keys is why 2,004 of the first 2,600 captured rows
        # (2026-04-22 → 2026-08-16) recorded provider='unknown', model=NULL —
        # a snapshot that cannot say which model produced it is a weak replay
        # input, and always-on capture made that the default for all traffic.
        if api_response is not None and (not provider_name or not model_name):
            try:
                meta = api_response.metadata or {}
                if not provider_name:
                    provider_name = str(meta.get("provider", "") or "")
                if not model_name:
                    model_name = (
                        meta.get("model")
                        or meta.get("matrx_model_name")
                        or meta.get("provider_model_name")
                    )
            except Exception:
                pass
        # Last resort — the catalog knows the vendor for a model id. This runs
        # in the background snapshot task, never on the request's hot path.
        if not provider_name and model_name:
            provider_name = await _catalog_vendor_for_model(str(model_name))

        # Step 1 — coerce payloads into JSON-safe Python values.
        # This only touches types (dataclass → dict, bytes → placeholder,
        # Pydantic → dict); it does NOT shorten strings or drop keys.
        safe_request = _json_safe(request_payload) if request_payload else None
        safe_unified = _json_safe(unified_payload) if unified_payload else None
        # response_payload = the model response on success, or the structured
        # ERROR on the provider-call-failure path (api_response is None then).
        if api_response is not None:
            safe_response = _json_safe(api_response.to_dict())
        elif error_payload is not None:
            safe_response = _json_safe(error_payload)
        else:
            safe_response = None

        # Step 2 — apply the explicit redactor pipeline. This is the ONE
        # place where the snapshot writer is allowed to modify the payload
        # before persistence. Every redactor in DEFAULT_SNAPSHOT_REDACTORS:
        #   - has a single, clearly-named transformation
        #   - leaves an inline marker identifying what it changed and why
        #   - never adds, removes, reorders, or retypes keys
        # See matrx_ai.providers.snapshot_redactors for the guarantees.
        if safe_request is not None:
            safe_request = apply_redactors(safe_request, DEFAULT_SNAPSHOT_REDACTORS)
        if safe_unified is not None:
            safe_unified = apply_redactors(safe_unified, DEFAULT_SNAPSHOT_REDACTORS)
        if safe_response is not None:
            safe_response = apply_redactors(safe_response, DEFAULT_SNAPSHOT_REDACTORS)

        payload_dict = {
            "conversation_id": exec_ctx.conversation_id,
            "user_request_id": exec_ctx.request_id or None,
            "cx_request_id": cx_request_id,
            "iteration": iteration,
            "trigger_message_id": trigger_message_id,
            "response_message_id": response_message_id,
            "provider": provider_name or "unknown",
            "model": model_name,
            # request_payload is NOT NULL on the table; provider-shape is
            # the original primary column. Fall back to {} only if a caller
            # somehow passed unified-only, which shouldn't happen in practice.
            "request_payload": safe_request if safe_request is not None else {},
            "unified_payload": safe_unified,
            "response_payload": safe_response,
            # Tenant identity is part of the snapshot row, not a database
            # default. AIMatrixRequest carries host additions in metadata,
            # while a few typed host contexts expose the field directly.
            "organization_id": (
                getattr(exec_ctx, "organization_id", None)
                or getattr(exec_ctx, "metadata", {}).get("organization_id")
                or None
            ),
            # ── THE CONFIG HALF OF A REPLAYABLE INPUT (C-16) ──────────────
            # WHICH VERSION OF THE UNIT produced this call. Without it, a
            # replay weeks later cannot tell a candidate change apart from an
            # edit made to the agent/workflow in the meantime — the payload
            # would be exact and the conclusion still wrong. Capture time is
            # the ONLY moment this is knowable, which is why it is stamped
            # here and not resolved later.
            #
            # Both read straight off the ambient context (no extra DB work on
            # a background write path): `agent_version_id` already travels on
            # every agent run; `workflow_definition_version_id` is stamped once
            # per workflow run by the scheduler and inherited by every fork.
            #
            # NULL is HONEST, never "missing": a call made outside any agent
            # has no agent version, and a run started from a FLOATING
            # definition pins no workflow version row.
            "agent_definition_version": getattr(exec_ctx, "agent_version_id", None) or None,
            "workflow_definition_version": (
                getattr(exec_ctx, "workflow_definition_version_id", None) or None
            ),
        }

        # cx_request_snapshot is an append-only audit log, never UPDATE'd.
        # In a request lane: route through the WriteCoordinator so it lands in
        # the same single transactional flush as the cx_request row it shadows.
        #
        # OUT OF LANE — a mandated agent / NamedAgent.run inside a background
        # pipeline (podcast stages, detached resume tasks, queue workers) has
        # NO RequestLane, so the queue helper would log+DROP this write. That
        # is exactly how every podcast/mandated run captured ZERO snapshots
        # while always-on capture (D-33) reported healthy (measured 2026-08-17:
        # runs 6c2f768f + 34e2d7f4, 15 child conversations, 0 rows, 0 failure
        # alarms — the write was never attempted). On those paths the parent
        # conversation/user_request rows were committed SYNCHRONOUSLY by the
        # gate before the provider call (see conversation_gate's durable-scope
        # memo), so a direct one-shot insert here is FK-safe. A failure lands
        # in the outer except → _record_snapshot_capture_failure, the durable
        # counter the capture-health alarm reads.
        from matrx_ai.persistence.queue_helpers import (
            get_coordinator,
            queue_request_snapshot_create,
        )

        snapshot_id = str(uuid4())
        snapshot_fields = dict(payload_dict)
        snap_conv_id = snapshot_fields.pop("conversation_id")
        snap_ur_id = snapshot_fields.pop("user_request_id") or ""
        if get_coordinator() is not None:
            queue_request_snapshot_create(
                id=snapshot_id,
                user_request_id=snap_ur_id,
                conversation_id=snap_conv_id,
                **snapshot_fields,
            )
        else:
            from matrx_ai.client_host import get_conversation_store

            if get_conversation_store() is not None:
                # CLIENT host — chat.request_snapshot is a server table this
                # process cannot reach; snapshots are a server-side concern.
                return
            from matrx_orm import (
                COORDINATOR_BYPASS_ACKNOWLEDGEMENT,
                Session,
                allow_direct_coordinator_write,
            )

            from matrx_ai.db.cx_managers import cxm

            direct_fields = dict(snapshot_fields)
            # Mirror the queue path's org stamp; the empty-string sentinel is a
            # queue-dependency artifact — a direct insert uses honest NULL.
            org_id = direct_fields.get("organization_id")
            if org_id:
                direct_fields.setdefault("organization_id", org_id)
            creator = getattr(exec_ctx, "user_id", None)
            if creator:
                direct_fields.setdefault("created_by", creator)
            with allow_direct_coordinator_write(
                cxm.request_snapshot.model,
                reason=(
                    "out-of-lane snapshot capture after the durable parent gate; "
                    "there is no request Coordinator to own this append-only audit row"
                ),
                acknowledgement=COORDINATOR_BYPASS_ACKNOWLEDGEMENT,
            ):
                async with Session() as session:
                    await cxm.request_snapshot.model.create(
                        id=snapshot_id,
                        conversation_id=snap_conv_id,
                        user_request_id=snap_ur_id or None,
                        **direct_fields,
                    )
                report = await session.flush(reason="request_snapshot_capture")
                if report.error is not None:
                    raise RuntimeError(report.error)
    except Exception as exc:
        failure_context = {
            "request_id": getattr(exec_ctx, "request_id", None),
            "conversation_id": getattr(exec_ctx, "conversation_id", None),
            "iteration": iteration,
            "exception_type": f"{type(exc).__module__}.{type(exc).__qualname__}",
            "message": str(exc) or type(exc).__name__,
        }
        vcprint(
            failure_context,
            "[Executor] Snapshot write failed",
            color="red",
            log_level="ERROR",
        )
        await _record_snapshot_capture_failure(exc, {**failure_context, "path": "success"})


async def _catalog_vendor_for(config: Any) -> str:
    """The API vendor for this request's model, from the RESOLVED CATALOG
    (``ResolvedCallProfile.vendor`` == ``ai.endpoint.vendor``) — the same
    routing identity dispatch used. Feeds ``classify_provider_error`` (whose
    classifier keys ARE the vendor vocabulary) and telemetry.

    NEVER guesses from the model-name string — the old substring heuristic
    ("llama" → cerebras, no xai/replicate/together branch) mis-classified any
    model whose id didn't happen to carry a vendor token. Returns "unknown"
    only when the ref doesn't resolve at all (e.g. the failure IS an unknown
    model — the catalog raised before any provider was chosen)."""
    model = getattr(config, "matrx_model_name", None) or getattr(config, "model", None)
    if not model:
        return "unknown"
    return await _catalog_vendor_for_model(model)


async def _catalog_vendor_for_model(model: str) -> str:
    """The model-id twin of ``_catalog_vendor_for`` — same catalog, same
    contract, for callers that hold the id rather than the config (the
    snapshot writer). Never raises; "unknown" when the ref won't resolve."""
    if not model:
        return "unknown"
    try:
        from matrx_ai.catalog.resolve import resolve_call_profile

        profile = await resolve_call_profile(model)
        return profile.vendor
    except Exception:
        return "unknown"


def _error_to_response_payload(error: BaseException) -> dict[str, Any]:
    """Serialize a provider-call exception into a structured response_payload.

    Captures the classified ``error_info`` (RetryableError) when the provider
    attached one, plus the raw exception identity, so cx_request_snapshot's
    ``response_payload`` holds the exact failure alongside the exact payload.
    """
    payload: dict[str, Any] = {
        "outcome": "error",
        "exception_type": f"{type(error).__module__}.{type(error).__name__}",
        "exception_repr": repr(error)[:8000],
    }
    info = getattr(error, "error_info", None)
    if info is not None:
        payload["error_info"] = {
            "error_type": getattr(info, "error_type", None),
            "message": getattr(info, "message", None),
            "user_message": getattr(info, "user_message", None),
            "status_code": getattr(info, "status_code", None),
            "is_retryable": getattr(info, "is_retryable", None),
            "details": getattr(info, "details", None),
        }
    return payload


async def _write_request_snapshot_on_failure(
    *,
    exec_ctx: Any,
    iteration: int,
    current_request: AIMatrixRequest,
    state: ExecutionState,
    error: BaseException,
    trigger_position: int,
    first_assistant_position: int,
) -> None:
    """THE PROVIDER-CALL-FAILURE BOUNDARY WRITER.

    Persists a cx_request_snapshot capturing the EXACT payload that the
    provider rejected (``state.snapshot_payload`` — the SDK-ready wire dict
    stamped by the provider's ``capture_request_payload`` just before the SDK
    call), the matrx-canonical ``unified_payload``, and the structured error.

    BOUNDARY CONTRACT — read this before moving the call site:
      * This is invoked from EXACTLY ONE place: wrapped tightly around
        ``await client.execute(current_request)``. Any exception raised by
        that call — and ONLY that call — lands here.
      * It runs on failure whenever the run persists (``exec_ctx.store``) —
        NOT gated by ``ctx.snapshot`` / ``REQUEST_SNAPSHOT_CAPTURE_DEFAULT``.
        A failed request's payload is always recorded when there is a parent
        row to attach to; ephemeral runs (``store=False``) skip — no
        conversation is created, so a snapshot would be a permanent FK
        orphan. The per-request override governs only the success path.
      * It is awaited (not fire-and-forget): the snapshot is QUEUED into the
        request's WriteCoordinator and lands in the same final commit barrier
        as the rest of this turn — durable, per the "degrade to synchronous on
        error" doctrine.
      * It never raises — capture must not perturb the failure it is recording;
        the original exception is always re-raised by the caller afterwards.

    OUT OF SCOPE (these do NOT write here — they have their own homes):
      * Failures BEFORE the provider call (config assembly / payload build).
      * Failures AFTER a successful response (parsing, finish-reason handling,
        tool dispatch → cx_tool_call, persistence → system_write_failure).
      * The stream-level crash capture → system_error.
    """
    try:
        snap_payload = state.snapshot_payload
        state.snapshot_payload = None
        try:
            unified_snap = current_request.to_dict()
        except Exception:
            unified_snap = None
        model = getattr(current_request.config, "model", None)
        provider = await _catalog_vendor_for(current_request.config)
        await _write_request_snapshot(
            exec_ctx=exec_ctx,
            iteration=iteration,
            api_response=None,
            request_payload=snap_payload,
            unified_payload=unified_snap,
            trigger_position=trigger_position,
            first_assistant_position=first_assistant_position,
            state_snapshot=state.snapshot(),
            error_payload=_error_to_response_payload(error),
            provider=provider,
            model=model,
        )
    except Exception as exc:
        # Capturing the failure must never mask or replace the failure itself.
        failure_context = {
            "request_id": current_request.request_id,
            "conversation_id": current_request.conversation_id,
            "iteration": iteration,
            "exception_type": f"{type(exc).__module__}.{type(exc).__qualname__}",
            "message": str(exc) or type(exc).__name__,
        }
        vcprint(
            failure_context,
            "[Executor] Failure-path snapshot write failed",
            color="red",
            log_level="ERROR",
        )
        await _record_snapshot_capture_failure(
            exc, {**failure_context, "path": "provider_failure"}
        )


# ============================================================================
# MAIN EXECUTION FUNCTIONS
# ============================================================================


async def execute_until_complete(
    initial_request: AIMatrixRequest,
    client: UnifiedAIClient,
    max_iterations: int = 100,
    max_retries_per_iteration: int = 2,
) -> CompletedRequest:
    """
    Execute AI request autonomously, handling tool calls until completion.

    Args:
        initial_request: The initial request to execute
        client: The unified AI client
        max_iterations: Maximum number of iterations before giving up

    Returns:
        CompletedRequest with full conversation history, usage, and final response

    Raises:
        RuntimeError: If max iterations exceeded or execution fails
    """
    exec_ctx = get_app_context()

    # Per-execution mutable scratch lives here, NOT on AppContext.metadata.
    # The ContextVar set below is task-local; concurrent executors (parallel
    # workflow agents, sub-agents) each get their own instance via the
    # asyncio task ContextVar fork — no cross-task aliasing possible.
    state = ExecutionState()
    state_token = set_execution_state(state)
    try:
        return await _execute_until_complete_inner(
            exec_ctx=exec_ctx,
            state=state,
            initial_request=initial_request,
            client=client,
            max_iterations=max_iterations,
            max_retries_per_iteration=max_retries_per_iteration,
        )
    except asyncio.CancelledError as _cancel_exc:
        # ────────────────────────────────────────────────────────────────
        # CLOSE THE LOOP. This is the entire reason this system exists.
        #
        # A client disconnect (page refresh on localhost, network drop) or a
        # server shutdown cancels this task mid-stream. CancelledError does
        # NOT inherit from Exception, so it bypasses every ``except Exception``
        # in the inner loop and the persist step never runs — losing the cost
        # data even though the provider already billed us and we received the
        # token usage. That is the original incident, verbatim.
        #
        # Here we shield-persist the in-flight request using the cost/usage
        # accumulated on state.current_request, BEFORE re-raising. The persist
        # queues the cx_request / cx_user_request / cx_message rows onto the
        # request's WriteCoordinator; the lane's drain finalizer then flushes
        # them in one transaction (it runs even on cancel). asyncio.shield
        # keeps the persist alive if another cancellation arrives.
        #
        # Idempotent: state.persisted guards against a normal completion that
        # raced the cancel, and the coordinator coalesces per-row regardless.
        if state.current_request is not None and not state.persisted:
            # Record any provider-billed usage from the in-flight call that the
            # cancellation interrupted. The provider stamps billed usage onto the
            # CancelledError it propagates (when it managed to observe a terminal
            # usage block before the cancel landed); harvest it so the cancelled
            # row carries real cost, not $0. (The original incident: a paid call
            # billed during cancel/disconnect recorded as an error with no cost.)
            _record_billed_usage_on_failure(
                state.current_request,
                _cancel_exc,
                iteration=state.iteration or None,
            )
            from matrx_ai.providers.errors import get_completed_response

            _completed_response = get_completed_response(_cancel_exc)
            # Capture the partial assistant text streamed up to the interrupt and
            # save it as a real (truncated) assistant turn with a marker — so a
            # deliberate "stop and redirect" keeps what the model already said,
            # and the next run reloads it as ordinary history. The emitter is the
            # provider-agnostic chokepoint every chunk flows through.
            _partial_text = ""
            try:
                _get_turn = getattr(exec_ctx.emitter, "get_turn_text", None)
                if _get_turn is not None:
                    _partial_text = _get_turn() or ""
            except Exception:
                _partial_text = ""

            _interrupt_final_resp = (
                _completed_response
                if isinstance(_completed_response, UnifiedResponse)
                else UnifiedResponse(messages=[])
            )
            if _interrupt_final_resp.messages:
                try:
                    state.current_request = AIMatrixRequest.add_response(
                        original_request=state.current_request,
                        response=_interrupt_final_resp,
                        tool_results=None,
                    )
                except Exception as _add_err:
                    vcprint(
                        "[execute_until_complete] completed-response capture "
                        f"add_response failed: {_add_err}",
                        color="red",
                    )
                    _interrupt_final_resp = UnifiedResponse(messages=[])
            elif _partial_text.strip():
                _partial_msg = UnifiedMessage(
                    role="assistant",
                    content=[TextContent(text=_partial_text + _INTERRUPT_MARKER)],
                )
                _interrupt_final_resp = UnifiedResponse(messages=[_partial_msg])
                try:
                    # Append it exactly like a normal turn so the existing
                    # end-of-run persistence writes it into cx_message at its
                    # natural position (no special-casing).
                    state.current_request = AIMatrixRequest.add_response(
                        original_request=state.current_request,
                        response=_interrupt_final_resp,
                        tool_results=None,
                    )
                except Exception as _add_err:
                    vcprint(
                        f"[execute_until_complete] partial-capture add_response failed: {_add_err}",
                        color="yellow",
                    )
                    _interrupt_final_resp = UnifiedResponse(messages=[])

            try:
                await asyncio.shield(
                    _finalize_and_persist(
                        current_request=state.current_request,
                        iteration=state.iteration,
                        final_response=_interrupt_final_resp,
                        metadata={
                            "status": "cancelled",
                            "interrupted": True,
                            "partial_assistant_captured": bool(_partial_text.strip()),
                            "provider_completed_after_cancellation": bool(
                                _completed_response
                            ),
                            "error": (
                                "Request cancelled mid-stream (client "
                                "disconnect or server shutdown). Persisted the "
                                "completed provider response when available, "
                                "otherwise the partial assistant turn, plus "
                                "cost/usage accumulated through cancellation."
                            ),
                            "cancelled_iteration": state.iteration,
                        },
                        trigger_position=state.trigger_position,
                        pre_execution_message_count=state.pre_execution_message_count,
                        debug=False,
                        state=state,
                    )
                )
                vcprint(
                    "[execute_until_complete] Cancelled mid-stream — "
                    "shield-persisted in-flight cost/usage before re-raising.",
                    color="yellow",
                )
            except Exception as persist_err:
                # The persist itself must never swallow the cancellation or
                # crash the unwind. Worst case the watchdog backstops the row.
                vcprint(
                    f"[execute_until_complete] cancel-path persist failed: "
                    f"{type(persist_err).__name__}: {persist_err}. "
                    f"Watchdog is the backstop.",
                    color="red",
                )
        raise
    finally:
        clear_execution_state(state_token)


async def _execute_until_complete_inner(
    *,
    exec_ctx: Any,
    state: ExecutionState,
    initial_request: AIMatrixRequest,
    client: UnifiedAIClient,
    max_iterations: int,
    max_retries_per_iteration: int,
) -> CompletedRequest:
    current_request = initial_request
    iteration = 0
    response: UnifiedResponse | None = None
    debug = current_request.debug
    if LOCAL_DEBUG:
        debug = True

    # A stored request id is a UUID foreign key on every chat persistence row.
    # The conversation gate deliberately refuses to create an invalid parent,
    # so continuing into a paid provider call would guarantee that the later
    # chat.request INSERT is stranded in system_write_failure. Refuse at the
    # execution boundary instead. Ephemeral test/tool runs remain available by
    # declaring store=False explicitly.
    persistence_request_id = current_request.request_id or exec_ctx.request_id
    if (
        exec_ctx.store
        and persistence_request_id
        and not _is_valid_uuid_str(persistence_request_id)
    ):
        raise ValueError(
            "Stored AI executions require a UUID request_id; "
            "use store=False for synthetic or ephemeral execution contexts"
        )

    if debug:
        vcprint(debug, "[DEBUG EXECUTE UNTIL COMPLETE] Current Debug Setting", color="yellow")
        await exec_ctx.emitter.send_info(
            InfoPayload(
                code="debug_mode_active",
                system_message="Debug mode is enabled for this request",
                user_message="Debug mode is active — verbose execution details will be included in status updates.",
                metadata={"debug": True},
            )
        )

    # Ephemeral runs (store=False) assign a real UUID but write NOTHING — no
    # cx_conversation, no cx_user_request, no cx_message/cx_request. Creating
    # the conversation row here would FK-anchor rows the rest of the persist
    # path is told to skip. This mirrors the API's skip_persistence path.
    if exec_ctx.store:
        await ensure_conversation_exists(
            conversation_id=exec_ctx.conversation_id,
            user_id=exec_ctx.user_id,
            parent_conversation_id=exec_ctx.parent_conversation_id,
        )

    chat_timing_mark("execute_inner_entry", "execute_until_complete_inner entry")

    _schedule_labeling_if_new(exec_ctx, current_request.config)

    # The cx_user_request row should already exist — boundary layers call
    # ensure_user_request_exists() before reaching here.  If it's missing we
    # create it now so execution is never blocked by a missing boundary call.
    # A warning is logged so the gap can be found and fixed in the calling code.
    _request_id = current_request.request_id or exec_ctx.request_id
    if _request_id and exec_ctx.store:
        # `ensure_user_request_exists()` is idempotent (per-request_id lock,
        # silent no-op if the row already exists), so it's the canonical
        # entry point — boundaries (API routes, batch scripts, workflows)
        # MAY call it explicitly when they want to populate richer metadata
        # before execution starts, but they don't have to. The platform
        # self-heals and that's the contract.
        #
        # A cx_user_request is ONE backend API call (one user action), keyed
        # solely by request_id with NO conversation. One request_id may span
        # many conversations (batch) and each conversation's cx_request rows
        # carry their own conversation_id — that IS the request↔conversation
        # bridge. Sub-agents inherit the parent's request_id by design; this
        # is now a plain no-op (the row already exists), not a special case.
        await ensure_user_request_exists(
            request_id=_request_id,
            user_id=exec_ctx.user_id,
        )
    chat_timing_mark("user_request_inner", "ensure_user_request_exists (executor) complete")

    # Track message positions for cx_user_request
    pre_execution_message_count = len(current_request.config.messages)
    # The trigger is the last user message before execution (position is 0-based)
    trigger_position = pre_execution_message_count - 1 if pre_execution_message_count > 0 else 0

    # Record the persist context on the owned state so the OUTER
    # ``execute_until_complete`` can shield-persist on a mid-stream cancel
    # (client disconnect / shutdown). Without this, CancelledError sails past
    # every ``except Exception`` (it doesn't inherit from Exception) and the
    # accumulated cost is lost — the exact bug this whole system exists to kill.
    state.current_request = current_request
    state.trigger_position = trigger_position
    state.pre_execution_message_count = pre_execution_message_count
    # Messages already persisted (loaded from the DB) at execution start carry
    # their real cx_message.id. Persistence skips re-INSERTing these so a retry
    # (which reloads existing messages into config.messages) can't duplicate the
    # user message. New messages this turn have id=None until reserved/created.
    #
    # A DB-loaded message carries BOTH id AND position (from_cx_message stamps
    # position); a freshly-added message has position=None (the same signal
    # context_trim uses). Requiring position too means a client that sends a NEW
    # message with a self-assigned id can't accidentally mark it "already
    # persisted" and get it SILENTLY skipped (a data-loss shape). Only genuinely
    # DB-loaded rows (id + position) are treated as pre-existing.
    state.pre_existing_message_ids = {
        m.id
        for m in current_request.config.messages
        if getattr(m, "id", None) and getattr(m, "position", None) is not None
    }
    # Initialize the commit high-water-mark just below the trigger so the first
    # per-turn barrier writes the trigger message onward. (Persistence contract.)
    state.committed_position = trigger_position - 1
    state.committed_iteration = 0

    # Reserve cx_message rows for the user trigger and first assistant response.
    # These IDs are announced to the frontend immediately so the client can
    # attach streaming content to known record anchors.
    tracker = get_tracker()
    _parent_refs = {
        "conversation_id": exec_ctx.conversation_id,
        "user_request_id": _request_id or "",
    }

    reserved_messages: dict[int, str] = {}
    first_assistant_position = pre_execution_message_count

    # Lazy import — break cycle with matrx_ai.persistence ↔ orchestrator.
    from matrx_ai.persistence.queue_helpers import get_coordinator, queue_message_create

    # Message-row RESERVATION is a streaming-only optimization: it pre-announces
    # cx_message IDs to the frontend so it can anchor streaming content. It only
    # works when a coordinator (i.e. a streaming lane) is active — without one,
    # the queue calls below would be SILENTLY DROPPED, leaving reserved IDs that
    # name rows that never got inserted. In that out-of-request / background
    # scope (scheduler, content-processing pipeline, internal agent runs) we skip
    # reservation entirely; persist_completed_request CREATEs the messages
    # directly via the cxm fallback instead. ``get_coordinator()`` lazily creates
    # the coordinator when a lane exists, so the streaming path is unaffected.
    # System runs (cost-only persistence) write no cx_message rows at all, so
    # reserving message ids would announce rows that will never exist.
    if (
        exec_ctx.store
        and not getattr(exec_ctx, "system_run", False)
        and get_coordinator() is not None
    ):
        # Reserve user and assistant message rows via the WriteCoordinator.
        # These were previously blocking pre-API INSERTs; they are now fire-
        # and-forget queue calls. The reservation tracker announces the IDs
        # to the client immediately (no DB round-trip needed for that), and
        # the coordinator coalesces the INSERT with the later UPDATE-to-
        # 'active' from persist_completed_request into a single INSERT at
        # flush time.
        #
        # USER MESSAGE — the trigger content is FULLY KNOWN at reservation
        # time (the user already typed it). Serialize the real content into
        # the INSERT with status='active' instead of an empty 'pending'
        # placeholder, so the row is durable from the first coordinator
        # flush. This structurally kills the 2026-05-28 user-message-loss
        # class: the client-delegated suspend path runs
        # ``_flush_assistant_message_mid_loop`` (commits the assistant row)
        # and then advances ``state.committed_position`` past the user's
        # position via the ``max(..., _assistant_pos)`` at the precommit
        # site. That made the subsequent ``_persist_turn_and_commit``
        # early-return (``post_count - 1 <= state.committed_position``)
        # without ever UPDATEing the user row from its empty placeholder —
        # the row then aged off to ``status='abandoned'`` with
        # ``content_blocks=0`` while the model had clearly already received
        # the user's input. By carrying the real content on the reservation
        # INSERT, the user message is correct even if the downstream UPDATE
        # never runs. A later UPDATE from ``persist_completed_request``
        # writes the same fields and coalesces cleanly.
        # ``TextContent.to_storage_dict`` always emits the lease's pristine
        # user text (never the ephemeral context block), so the manifest that
        # ``apply_context_objects`` may have attached upstream cannot leak.
        # The user reservation only applies to a NEW user trigger this turn.
        # On a /resume run the message at trigger_position is a REBUILT row
        # from the DB (role='tool' after a delegated suspend, or a persisted
        # user message carrying its real cx_message.id) — reserving here used
        # to unconditionally INSERT an empty role='user' status='pending'
        # placeholder at an already-occupied position. Every resume left one
        # of those rows behind, aging off to status='abandoned' (live
        # evidence: conversation 417e64ce-74ff-4fcd-b976-df1f0df56671,
        # positions 24-27, 2026-06-09).
        _trigger_user_content: list[Any] = []
        _trigger_user_status: str = "pending"
        # Empty message list (internal callers) keeps the legacy empty/pending
        # reservation so later code that appends a user message can finalize
        # the row via UPDATE.
        _reserve_user_row = pre_execution_message_count == 0
        if pre_execution_message_count > 0 and 0 <= trigger_position < pre_execution_message_count:
            _trigger_msg = current_request.config.messages[trigger_position]
            _trigger_role = getattr(_trigger_msg, "role", None)
            _trigger_role_str = (
                _trigger_role.value if hasattr(_trigger_role, "value") else _trigger_role
            )
            if _trigger_role_str == "user" and not getattr(_trigger_msg, "id", None):
                if not _trigger_msg.is_ephemeral_only():
                    _reserve_user_row = True
                    _trigger_storage = _trigger_msg.to_storage_dict()
                    _trigger_user_content = _trigger_storage.get("content") or []
                    # Only flip to 'active' when we actually have content blocks
                    # to write. An empty list would leave the row equivalent to
                    # the legacy placeholder; let the downstream UPDATE finalize
                    # it in that (unexpected) case.
                    if _trigger_user_content:
                        _trigger_user_status = "active"

        if _reserve_user_row:
            user_msg_id = str(uuid4())
            queue_message_create(
                id=user_msg_id,
                conversation_id=exec_ctx.conversation_id,
                role="user",
                position=APPEND_MESSAGE_POSITION,
                status=_trigger_user_status,
                content=_trigger_user_content,
                created_by=exec_ctx.user_id or None,
            )
            reserved_messages[trigger_position] = user_msg_id
            try:
                await tracker.reserve(
                    emitter=exec_ctx.emitter,
                    db_project="matrx",
                    table="message",
                    parent_refs=_parent_refs,
                    metadata={
                        "role": "user",
                        "position": trigger_position,
                        "position_kind": "logical_index",
                    },
                    record_id=user_msg_id,
                )
            except Exception as exc:
                vcprint(
                    f"[Executor] Failed to announce user message reservation: {exc}", color="yellow"
                )

        assistant_msg_id = str(uuid4())
        queue_message_create(
            id=assistant_msg_id,
            conversation_id=exec_ctx.conversation_id,
            role="assistant",
            position=APPEND_MESSAGE_POSITION,
            status="pending",
            content=[],
            created_by=exec_ctx.user_id or None,
        )
        reserved_messages[first_assistant_position] = assistant_msg_id
        try:
            await tracker.reserve(
                emitter=exec_ctx.emitter,
                db_project="matrx",
                table="message",
                parent_refs=_parent_refs,
                metadata={
                    "role": "assistant",
                    "position": first_assistant_position,
                    "position_kind": "logical_index",
                },
                record_id=assistant_msg_id,
            )
        except Exception as exc:
            vcprint(
                f"[Executor] Failed to announce assistant message reservation: {exc}",
                color="yellow",
            )

    # Hand the reserved-message map to the executor's owned state.
    # ``state.reserved_request_ids`` starts empty and is populated below as
    # each iteration generates its cx_request UUID.
    state.reserved_message_ids = reserved_messages

    chat_timing_mark("reservations_complete", "message reservations complete")

    # Bind the barrier exception locally (lazy import avoids the persistence ↔
    # orchestrator module-load cycle) so the loop's generic ``except Exception``
    # can re-raise it instead of swallowing it into the soft error path.
    from matrx_ai.persistence.coordinator import PersistenceBarrierError

    # INTERRUPT fence — the message count at the last CLEAN boundary (a poll
    # that passed with no stop signal). When an interrupt-mode cancel fires,
    # everything appended since this fence is the abandoned tail the user
    # stopped mid-flight: it persists (costs are kept) but HIDDEN — both
    # is_visible_to_user=False and is_visible_to_model=False — as one
    # pairing-safe unit (the whole tail hides together, so a tool_use is
    # never split from its tool_result). The three-send-modes ruling
    # (docs/cx_chat/TURN_BOUNDARY_INBOX.md).
    _interrupt_fence = len(current_request.config.messages)

    while iteration < max_iterations:
        # TWO independent stop layers, polled at every iteration boundary:
        # 1) the in-process RequestControlRegistry (instant, this process only);
        # 2) the runtime-spine control row (durable + cross-process: POST /cancel
        #    stamps it, and the tree dollar budget / deadline live there too).
        _stop_reason: str | None = None
        _poll_request_id = current_request.request_id or getattr(
            exec_ctx, "request_id", None
        )
        if _is_request_cancelled(_poll_request_id):
            _stop_reason = "Request cancelled before the next provider call."
        else:
            _spine_reason = await _spine_stop_reason()
            if _spine_reason:
                _stop_reason = f"Request stopped by execution control: {_spine_reason}"
        if _stop_reason:
            _interrupted = _is_request_interrupted(_poll_request_id)
            _hidden_count = 0
            if _interrupted:
                _hidden_count = _hide_interrupted_tail(
                    current_request.config.messages, _interrupt_fence
                )
            await exec_ctx.emitter.send_phase("complete")
            await exec_ctx.emitter.send_info(
                InfoPayload(
                    code="request_cancelled",
                    system_message=_stop_reason,
                    user_message="Request cancelled.",
                    metadata={
                        "iteration": iteration + 1,
                        "interrupted": _interrupted,
                        "hidden_tail_messages": _hidden_count,
                    },
                )
            )
            return await _finalize_and_persist(
                current_request=current_request,
                iteration=iteration,
                final_response=UnifiedResponse(messages=[]),
                metadata={
                    "status": "cancelled",
                    "error": _stop_reason,
                    "cancelled_iteration": iteration + 1,
                    **(
                        {"interrupted": True, "hidden_tail_messages": _hidden_count}
                        if _interrupted
                        else {}
                    ),
                },
                trigger_position=trigger_position,
                pre_execution_message_count=pre_execution_message_count,
                debug=debug,
                state=state,
            )

        # This boundary is clean — everything before this point is history the
        # user has fully received. Advance the interrupt fence.
        _interrupt_fence = len(current_request.config.messages)

        iteration += 1
        state.iteration = iteration
        # Keep the cancel-persist context current: current_request accumulates
        # usage across iterations and is reassigned when tool results feed the
        # next turn. The outer cancel handler reads state.current_request.
        state.current_request = current_request
        current_timing = TimingUsage(start_time=time.time(), iteration=iteration)

        vcprint(
            f"\n{'=' * 60}\nIteration {iteration}\n{'=' * 60}",
            "[AI REQUESTS EXECUTE UNTIL COMPLETE] Iteration",
            color="cyan",
            verbose=debug,
        )

        # Pre-generate a cx_request ID for this iteration.
        # The actual DB INSERT happens in persist_completed_request because
        # cx_request.ai_model_id is NOT NULL and unknown until the API call
        # returns. We still announce the ID now so the client has it.
        iter_request_id = str(uuid4())
        try:
            req_parent_refs = dict(_parent_refs)
            req_metadata: dict[str, Any] = {"iteration": iteration}

            if response is not None:
                call_ids = []
                _msgs = (
                    response.messages
                    if isinstance(response.messages, list)
                    else [response.messages]
                )
                for msg in _msgs:
                    for content in msg.content:
                        if isinstance(content, ToolCallContent):
                            call_ids.append(content.id)
                if call_ids:
                    req_parent_refs["call_id"] = call_ids[0]
                    req_metadata["call_id"] = call_ids[0]
                    req_metadata["call_ids"] = call_ids

            await tracker.reserve(
                emitter=exec_ctx.emitter,
                db_project="matrx",
                table="request",
                parent_refs=req_parent_refs,
                metadata=req_metadata,
                record_id=iter_request_id,
            )
            state.reserved_request_ids[iteration] = iter_request_id
        except Exception as exc:
            vcprint(
                f"[Executor] Failed to announce cx_request for iteration {iteration}: {exc}",
                color="yellow",
            )
        chat_timing_mark("iteration_request_reserved", f"cx_request reserved iteration {iteration}")

        # Retry loop for recoverable errors
        response = None
        last_error: Exception | None = None

        # Overload-class reroute bookkeeping (sibling-offering ladder + the
        # model-level retry_max_attempts / retry_fallback_id policy — see
        # orchestrator/overload_reroute.py).
        from matrx_ai.orchestrator.overload_reroute import (
            OverloadRerouteState,
            RerouteNote,
            decide_overload_action,
            is_reroutable_provider_error,
            load_offering_ladder,
            load_overload_policy,
        )

        overload_state = OverloadRerouteState()

        retry_loop_ceiling = max(max_retries_per_iteration, len(PROVIDER_OVERLOAD_RETRY_DELAYS))
        # While-with-manual-increment (not `for ... in range`): an overload
        # reroute extends the ceiling so the fallback model gets its own
        # attempt budget within this iteration.
        retry_attempt = -1
        while retry_attempt < retry_loop_ceiling:
            retry_attempt += 1
            try:
                request_control_id = current_request.request_id or getattr(
                    exec_ctx, "request_id", None
                )
                if _is_request_cancelled(request_control_id):
                    await exec_ctx.emitter.send_phase("complete")
                    await exec_ctx.emitter.send_info(
                        InfoPayload(
                            code="request_cancelled",
                            system_message="Request cancelled before the next retry attempt.",
                            user_message="Request cancelled.",
                            metadata={"iteration": iteration, "retry_attempt": retry_attempt},
                        )
                    )
                    return await _finalize_and_persist(
                        current_request=current_request,
                        iteration=iteration,
                        final_response=UnifiedResponse(messages=[]),
                        metadata={
                            "status": "cancelled",
                            "error": "Request cancelled before the next retry attempt.",
                            "cancelled_iteration": iteration,
                        },
                        trigger_position=trigger_position,
                        pre_execution_message_count=pre_execution_message_count,
                        debug=debug,
                        state=state,
                    )

                # Resolve any structured input blocks (notes, tasks, etc.) in the
                # last user message before sending to the model. Runs concurrently,
                # only on first retry attempt to avoid redundant fetches.
                # Also inject CRUD tools for any block with editable=True.
                if retry_attempt == 0:
                    from matrx_connect.context.app_context import (
                        set_app_context,
                        try_get_app_context,
                    )

                    from matrx_ai.config.structured_input_resolver import (
                        collect_read_only_resource_ids,
                        inject_editable_tools,
                        resolve_structured_inputs,
                    )
                    from matrx_ai.tools.dynamic_drain import drain_pending

                    inject_editable_tools(current_request.config.messages, current_request.config)
                    collect_read_only_resource_ids(current_request.config.messages)
                    await resolve_structured_inputs(current_request.config.messages)

                    # Turn-boundary drain (once per iteration, before the API
                    # call). Two sources, one point:
                    #   1. pending tool mutations queued in-memory by tools that
                    #      ran last iteration (Phase D-loop), and
                    #   2. the DB-backed Turn-Boundary Inbox — user/system
                    #      messages enqueued mid-run (or while idle) that get
                    #      appended as user turns here so the model sees them on
                    #      this turn's API call, without canceling the run.
                    _app_ctx = try_get_app_context()
                    if _app_ctx is not None:
                        _new_ctx = await drain_pending(current_request.config, _app_ctx)
                        if _new_ctx is not _app_ctx:
                            set_app_context(_new_ctx)
                    chat_timing_mark(
                        "structured_inputs_resolved",
                        "structured inputs + drain_pending complete",
                    )

                # Reset the emitter's per-turn text accumulator so it holds only
                # THIS model call's streamed assistant text. If the run is
                # interrupted mid-stream, the cancel handler reads it back to
                # persist the partial assistant turn. Defensive getattr — not
                # every emitter implements it.
                _reset_turn = getattr(exec_ctx.emitter, "reset_turn_text", None)
                if _reset_turn is not None:
                    _reset_turn()

                # Make API call — api_response is UnifiedResponse (never None here)
                t0 = time.time()
                # ── PROVIDER-CALL FAILURE BOUNDARY ─────────────────────────────
                # Errors raised between this `try` and its `except` — i.e. the
                # provider API call ITSELF — ALWAYS land a cx_request_snapshot
                # with the exact wire payload + matrx payload + structured error,
                # then re-raise UNCHANGED into the retry/finalize handler below.
                # Nothing before this call (payload assembly) or after a
                # successful response (parsing, tool dispatch, persistence) is
                # captured here. See _write_request_snapshot_on_failure's
                # BOUNDARY CONTRACT for the full in/out-of-scope list.
                # Host reference-fence staging (per-send). Resolves the host's
                # in-content reference fences into the wire swaps EVERY
                # iteration, in THIS task — the only placement that covers
                # continue turns, current-turn user input, programmatic child
                # agents, /resume, and injection drains alike (the pre-2026-07
                # defect staged only in turn-1 HTTP prep). Best-effort: a
                # staging failure never breaks the send.
                _fence_stager = None
                try:
                    from matrx_ai._ext import get_reference_fence_stager

                    _fence_stager = get_reference_fence_stager()
                except Exception:  # noqa: BLE001 — optional seam, never fatal
                    _fence_stager = None
                if _fence_stager is not None:
                    try:
                        await _fence_stager(current_request.config)
                    except Exception as _stager_exc:  # noqa: BLE001
                        vcprint(
                            f"[executor] reference fence stager failed (ignored): "
                            f"{type(_stager_exc).__name__}: {_stager_exc}",
                            color="yellow",
                        )

                # Tool loops grow after ConversationResolver's one-time trim.
                # Re-apply the idempotent in-memory trim at the actual send
                # boundary so older results created during this same run cannot
                # accumulate until the provider rejects the prompt. Originals
                # remain durable and retrievable; only the wire-facing config is
                # compacted.
                try:
                    from matrx_ai.config.context_trim import trim_messages_context

                    _loop_trim_report = trim_messages_context(
                        list(current_request.config.messages)
                        if not isinstance(current_request.config.messages, list)
                        else current_request.config.messages
                    )
                    if _loop_trim_report.blocks_rewritten:
                        _app_ctx = try_get_app_context()
                        if _app_ctx is not None:
                            _app_ctx.metadata["last_trim_report"] = _loop_trim_report.to_dict()
                except Exception as _trim_exc:  # noqa: BLE001 -- send remains available
                    vcprint(
                        f"[executor] per-iteration context trim failed (ignored): "
                        f"{type(_trim_exc).__name__}: {_trim_exc}",
                        color="yellow",
                    )

                # Picklist secret injection (clone-at-send). Swap placeholder tokens for the
                # real descriptions into a throwaway clone of the config used ONLY for this
                # provider call; the canonical current_request keeps placeholders so the secret
                # never reaches persistence / snapshots / the conversation labeler. When secrets
                # are materialized we also drop the captured wire payload so cx_request_snapshot
                # never stores the description.
                from matrx_ai.config.picklist_runtime import build_wire_config
                from matrx_ai.providers.cache_guard import provider_prompt_cache_key

                current_request.config.prompt_cache_key = provider_prompt_cache_key(
                    current_request.conversation_id,
                    current_request.request_id,
                )

                _wire_config = build_wire_config(current_request.config)
                _orig_config = current_request.config
                if _wire_config is not None:
                    current_request.config = _wire_config
                chat_timing_mark("wire_config_built", "build_wire_config complete")
                chat_timing_mark(
                    "pre_provider_execute",
                    "calling UnifiedAIClient.execute",
                )
                from matrx_connect.request_latency import mark_first_provider_call

                mark_first_provider_call()
                try:
                    async with buffer_error_events():
                        api_response: UnifiedResponse = await client.execute(current_request)
                except Exception as _provider_exc:
                    if _wire_config is not None:
                        current_request.config = _orig_config
                        # Redact (values → their placeholder/fence keys) instead
                        # of dropping — a reference-heavy request keeps a
                        # debuggable payload; fail-closed → None (dropped).
                        from matrx_ai.config.picklist_runtime import redact_wire_payload

                        state.snapshot_payload = redact_wire_payload(state.snapshot_payload)
                    await _write_request_snapshot_on_failure(
                        exec_ctx=exec_ctx,
                        iteration=iteration,
                        current_request=current_request,
                        state=state,
                        error=_provider_exc,
                        trigger_position=trigger_position,
                        first_assistant_position=first_assistant_position,
                    )
                    raise
                if _wire_config is not None:
                    current_request.config = _orig_config
                    from matrx_ai.config.picklist_runtime import redact_wire_payload

                    state.snapshot_payload = redact_wire_payload(state.snapshot_payload)
                chat_timing_mark(
                    "provider_execute_complete",
                    "UnifiedAIClient.execute complete",
                )
                current_timing.api_call_duration = time.time() - t0
                current_timing.model = current_request.config.model

                if _request_snapshot_enabled(exec_ctx):
                    # Pull the payload captured by the provider's execute()
                    # just before the SDK call. Clear it so we don't carry it
                    # across iterations.
                    snap_payload = state.snapshot_payload
                    state.snapshot_payload = None
                    # Stamped by the same capture call as the payload. The
                    # response object carries no provider key, so without this
                    # every success-path row recorded provider="unknown".
                    snap_provider = state.snapshot_provider
                    state.snapshot_provider = None
                    # Also capture the matrx-canonical pre-provider view.
                    # Best-effort: never let a to_dict() bug break the live
                    # request — fall back to None and the writer just leaves
                    # unified_payload empty for that row.
                    try:
                        unified_snap = current_request.to_dict()
                    except Exception:
                        unified_snap = None
                    # Take a frozen snapshot of execution state NOW so capture
                    # reads owned copies, not live dicts the loop will mutate.
                    _state_snapshot = state.snapshot()
                    # Stay in the request task long enough to queue the row into
                    # its active Coordinator.  Detaching here strips request
                    # context, so the writer mistakes an in-lane request for an
                    # out-of-lane caller and races a direct snapshot INSERT
                    # against the parent conversation's end-of-stream commit.
                    await _write_request_snapshot(
                        exec_ctx=exec_ctx,
                        iteration=iteration,
                        api_response=api_response,
                        request_payload=snap_payload,
                        unified_payload=unified_snap,
                        trigger_position=trigger_position,
                        first_assistant_position=first_assistant_position,
                        state_snapshot=_state_snapshot,
                        provider=snap_provider,
                        # The model that actually ran, read from the config
                        # the request was executed with — the same source
                        # the failure path uses. UnifiedResponse.metadata
                        # carries no bare "model" key either, so without
                        # this the column was NULL on every success row.
                        model=current_request.config.model,
                    )

                if debug:
                    print("\n\n[EXECUTE UNTIL COMPLETE] DEBUG PRINT 1\n\n")
                    rich.print(api_response)

                # Stamp the provider iteration onto the messages it produced.
                # Persistence uses this durable semantic association to link the
                # request cost to the correct assistant row; list order is not a
                # billing key because one response may contain multiple messages.
                for provider_message in api_response.messages:
                    provider_role = getattr(provider_message, "role", None)
                    provider_role_value = (
                        provider_role.value if hasattr(provider_role, "value") else provider_role
                    )
                    if provider_role_value == "assistant":
                        provider_message.metadata = {
                            **(provider_message.metadata or {}),
                            "provider_iteration": iteration,
                        }

                # Keep every paid provider call, including retries, at call
                # grain. Persistence groups these by iteration for the legacy
                # cx_request row while request/runtime totals retain exact
                # per-model cost.
                if api_response.usage is not None:
                    api_response.usage.metadata["iteration"] = iteration
                    api_response.usage.metadata["provider_attempt"] = retry_attempt + 1
                    api_response.usage.metadata["attempt_outcome"] = "succeeded"
                else:
                    await _capture_missing_provider_usage(
                        exec_ctx=exec_ctx,
                        current_request=current_request,
                        provider=snap_provider or "unknown",
                        iteration=iteration,
                    )
                current_request.add_usage(api_response.usage)

                # Prompt-cache observability guard. Ground-truth check on the
                # provider's own usage: screams (big RED banner + app_log ERROR)
                # if the system prompt mutated between rounds or if a stable,
                # large prefix produced ZERO cache reads — the exact silent
                # failure that quietly multiplies input cost. Self-gating and
                # never raises into the loop. Uses the ORIGINAL (non-wire) config
                # — picklist/fence swaps touch message CONTENT, never the system
                # text or tool names the cache prefix is keyed on.
                if api_response.usage is not None:
                    from matrx_ai.providers.cache_guard import observe_cache_usage

                    observe_cache_usage(
                        provider=api_response.usage.api,
                        model=(
                            api_response.usage.provider_model_name
                            or api_response.usage.matrx_model_name
                            or current_request.config.model
                        ),
                        conversation_id=current_request.conversation_id,
                        request_id=current_request.request_id,
                        system_text=(current_request.config.resolved_system_instruction or ""),
                        tool_names=_cache_prefix_tool_names(current_request.config),
                        raw_usage=api_response.usage.raw_usage or {},
                    )

                # Fold this call's cost into the tree-wide dollar budget. Parent
                # turns and every sub-agent share the same request_id, so one
                # accumulator sums the whole tree; the next turn's tool calls
                # read remaining_budget() and the guardrail blocks new spawns
                # LOUDLY once the tree is out of budget.
                if api_response.usage is not None:
                    try:
                        from matrx_ai.orchestrator.cost_budget import record_tree_cost

                        record_tree_cost(
                            current_request.request_id,
                            api_response.usage.calculate_cost(),
                        )
                    except Exception:
                        pass
                    # Runtime-spine mirror of the same chokepoint: the host hook
                    # (when configured) schedules a DETACHED meter write so the
                    # execution tree's budget/rollup sees spend DURING the turn,
                    # not only at settle. Sync + non-blocking by contract.
                    _spine_meter_call(api_response.usage)

                # Handle finish reason
                finish_action = handle_finish_reason(
                    api_response,
                    current_request,
                    retry_attempt,
                    max_retries_per_iteration,
                    debug,
                )

                # Decide what to tell the UI BEFORE we say "planning next steps".
                # If this response has no tool calls we are about to exit the loop
                # — emitting "Planning next steps…" here would leave the UI stuck
                # on that status after the stream ends. Instead, transition to
                # the terminal "complete" phase and emit an empty user_message
                # so the frontend clears any in-progress indicator.
                _will_continue = finish_action == "retry" or _response_has_tool_calls(api_response)

                status = {
                    "Iteration": iteration,
                    "Retry Attempt": retry_attempt,
                    "Finish Action": finish_action,
                    "Finish Reason": api_response.finish_reason,
                    "will_continue": _will_continue,
                }

                if _will_continue:
                    # COUNTABLE WORK (SPEC §5.1). An agent step's tool
                    # iterations are the one long loop a workflow node cannot
                    # see — it lives here, inside the provider call. The
                    # emitter carries the invocation's durable coordinates, so
                    # this lands as a properly attributed NodeProgressEvent
                    # ("iteration 4 of 20") and is a silent no-op outside a
                    # workflow run. Throttled and best-effort at the emitter.
                    _send_step_progress = getattr(exec_ctx.emitter, "send_step_progress", None)
                    if _send_step_progress is not None:
                        await _send_step_progress(
                            current=iteration,
                            total=max_iterations,
                            message=f"Tool iteration {iteration} of {max_iterations}",
                        )
                    await exec_ctx.emitter.send_phase("processing")
                    await exec_ctx.emitter.send_info(
                        InfoPayload(
                            code="iteration_update",
                            system_message="Processing update",
                            user_message="Planning next steps...",
                            metadata=status,
                        )
                    )
                else:
                    await exec_ctx.emitter.send_phase("complete")
                    await exec_ctx.emitter.send_info(
                        InfoPayload(
                            code="iteration_finalizing",
                            system_message="Final response received — no further tool calls; finalizing.",
                            user_message="",
                            metadata=status,
                        )
                    )

                vcprint(
                    status,
                    "[AI REQUESTS EXECUTE UNTIL COMPLETE] Request Status",
                    color="magenta",
                    verbose=debug,
                )

                if finish_action == "retry":
                    finish_str = (
                        str(api_response.finish_reason) if api_response.finish_reason else "unknown"
                    )
                    await exec_ctx.emitter.send_warning(
                        WarningPayload(
                            code="model_retry",
                            system_message=(
                                f"Model returned a non-success finish reason '{finish_str}' — retrying "
                                f"(attempt {retry_attempt + 1}/{max_retries_per_iteration + 1})."
                            ),
                            user_message=(
                                "The model encountered an issue and is retrying automatically. "
                                "This may take a moment."
                            ),
                            level="medium",
                            recoverable=True,
                            metadata={
                                "finish_reason": finish_str,
                                "retry_attempt": retry_attempt + 1,
                                "max_retries": max_retries_per_iteration + 1,
                                "iteration": iteration,
                            },
                        )
                    )
                    continue  # Retry with updated context

                elif finish_action == "truncated":
                    # The model ran out of output tokens — response is incomplete
                    # BUT content was already streamed chunk-by-chunk to the UI.
                    # This is a caveat about an otherwise-delivered response, not
                    # a failure to deliver — emit as WARNING so the UI flags the
                    # condition without invalidating the content the user
                    # already received and already paid for.
                    # See StreamEmitter.send_error docstring for the rule.
                    model = current_request.config.model or "unknown model"
                    max_tokens = current_request.config.max_output_tokens

                    await _capture_truncated_response(
                        exec_ctx=exec_ctx,
                        current_request=current_request,
                        iteration=iteration,
                    )

                    print("\n")
                    print("=" * 70)
                    print("⚠  EXECUTOR: TRUNCATED RESPONSE DETECTED")
                    print(f"  Model      : {model}")
                    print(
                        f"  max_tokens : {max_tokens if max_tokens is not None else '(none set — model default used)'}"
                    )
                    print(f"  Iteration  : {iteration}")
                    print("  Content was delivered; emitting WARNING (not ERROR).")
                    print("=" * 70)
                    print("\n")

                    await exec_ctx.emitter.send_warning(
                        WarningPayload(
                            code="truncated_response",
                            system_message=(
                                f"Model '{model}' hit the output token limit and returned an incomplete response "
                                f"(max_output_tokens={max_tokens})."
                            ),
                            user_message=(
                                "The response was cut off because the model reached its output token limit. "
                                "The answer you received may be incomplete. Consider breaking your request "
                                "into smaller parts."
                            ),
                            level="medium",
                            recoverable=True,
                            metadata={
                                "model": model,
                                "max_output_tokens": max_tokens,
                                "finish_reason": str(api_response.finish_reason),
                                "iteration": iteration,
                            },
                        )
                    )

                    # Persist the partial content the model streamed before it
                    # was truncated. The early return here happens BEFORE the
                    # normal add_response() below, so without this the assistant
                    # text the user already saw would never reach cx_message.
                    current_request = _append_partial_response(current_request, api_response, state)

                    return await _finalize_and_persist(
                        current_request=current_request,
                        iteration=iteration,
                        final_response=api_response,
                        metadata={
                            "status": "truncated",
                            "finish_reason": str(api_response.finish_reason),
                            "error": f"Response truncated: model hit the output token limit (model={model}, max_output_tokens={max_tokens})",
                            "error_type": "truncated_response",
                        },
                        trigger_position=trigger_position,
                        pre_execution_message_count=pre_execution_message_count,
                        debug=debug,
                        state=state,
                    )

                elif finish_action == "stop":
                    # The model stopped with a non-success finish_reason that
                    # we don't retry. Whatever content streamed before this
                    # point was already delivered to the client, so the
                    # condition is a caveat on an otherwise-delivered
                    # response — emit WARNING, not ERROR. The request-level
                    # metadata still records ``status=failed`` so the
                    # persistence layer can flag it, but the user's stream
                    # is not invalidated.
                    # See StreamEmitter.send_error docstring for the rule.
                    model = current_request.config.model or "unknown model"
                    finish_str = (
                        str(api_response.finish_reason) if api_response.finish_reason else "unknown"
                    )

                    print("\n")
                    print("=" * 70)
                    print("⚠  EXECUTOR: NON-SUCCESS FINISH REASON — stopping execution")
                    print(f"  Model         : {model}")
                    print(f"  finish_reason : {finish_str}")
                    print(f"  Iteration     : {iteration}")
                    print("  Content already streamed; emitting WARNING (not ERROR).")
                    print("=" * 70)
                    print("\n")

                    from matrx_ai.config.finish_reason import FinishReason

                    try:
                        fr = FinishReason(finish_str)
                        retries_exhausted = (
                            fr.is_retryable() and retry_attempt >= max_retries_per_iteration
                        )
                    except ValueError:
                        retries_exhausted = False

                    # Safety / content-filter finish reasons get a clear,
                    # specific user message (this is the common Google case once
                    # adjustable categories are off — non-adjustable blocks and
                    # prompt-level blocks still land here). Whatever text streamed
                    # before the block is preserved (appended below), so the
                    # message tells the user the answer may be partial.
                    _SAFETY_REASONS = {
                        FinishReason.SAFETY,
                        FinishReason.CONTENT_FILTER,
                        FinishReason.PROHIBITED_CONTENT,
                        FinishReason.RECITATION,
                        FinishReason.SPII,
                        FinishReason.BLOCKLIST,
                        FinishReason.IMAGE_SAFETY,
                        FinishReason.IMAGE_PROHIBITED_CONTENT,
                        FinishReason.IMAGE_RECITATION,
                        FinishReason.LANGUAGE,
                    }
                    _fr_for_msg: FinishReason | None
                    try:
                        _fr_for_msg = FinishReason(finish_str)
                    except ValueError:
                        _fr_for_msg = None

                    if retries_exhausted:
                        user_msg = (
                            f"The model made a malformed function call and failed to recover after "
                            f"{max_retries_per_iteration + 1} retry attempt(s). "
                            "The request could not be completed."
                        )
                        warning_code = "max_retries_exceeded"
                        warning_level: Literal["low", "medium", "high"] = "high"
                    elif _fr_for_msg in _SAFETY_REASONS:
                        user_msg = (
                            "The response was stopped by the provider's content-safety "
                            "filters, so the answer may be incomplete. Any text generated "
                            "before it stopped has been saved. Try rephrasing your request."
                        )
                        warning_code = "content_safety_stop"
                        warning_level = "medium"
                    else:
                        user_msg = (
                            "The model was unable to complete the response. "
                            "This may be due to content restrictions or a model error."
                        )
                        warning_code = "model_stop"
                        warning_level = "medium"

                    await exec_ctx.emitter.send_warning(
                        WarningPayload(
                            code=warning_code,
                            system_message=f"Model '{model}' stopped with finish reason: {finish_str}",
                            user_message=user_msg,
                            level=warning_level,
                            recoverable=False,
                            metadata={
                                "model": model,
                                "finish_reason": finish_str,
                                "iteration": iteration,
                                "retry_attempt": retry_attempt,
                                "max_retries": max_retries_per_iteration,
                            },
                        )
                    )

                    # Provider/runtime failures represented as a terminal
                    # finish reason must reach the human-review queue too.
                    # Safety/content-policy stops are expected provider control
                    # flow and deliberately remain outside system_error.
                    if _fr_for_msg not in _SAFETY_REASONS:
                        from matrx_connect.streaming.error_capture import capture_error

                        finish_exc = RuntimeError(
                            f"Model {model!r} stopped with finish reason {finish_str!r}"
                        )
                        await capture_error(
                            finish_exc,
                            kind="provider_response_failed",
                            request_id=getattr(exec_ctx, "request_id", None),
                            conversation_id=getattr(exec_ctx, "conversation_id", None),
                            route="orchestrator/provider_response",
                            error_type="finish_reason_error",
                            payload={
                                "model": model,
                                "finish_reason": finish_str,
                                "iteration": iteration,
                                "retry_attempt": retry_attempt,
                            },
                        )

                    # Persist whatever partial content streamed before the model
                    # stopped (safety/content blocks frequently arrive after some
                    # text). The early return here is BEFORE the normal
                    # add_response() below, so without this the partial assistant
                    # turn the user already saw would never reach cx_message.
                    current_request = _append_partial_response(current_request, api_response, state)

                    return await _finalize_and_persist(
                        current_request=current_request,
                        iteration=iteration,
                        final_response=api_response,
                        metadata={
                            "status": "failed",
                            "finish_reason": str(api_response.finish_reason),
                            "error": f"Model stopped with finish reason: {api_response.finish_reason}",
                            "error_type": "finish_reason_error",
                        },
                        trigger_position=trigger_position,
                        pre_execution_message_count=pre_execution_message_count,
                        debug=debug,
                        state=state,
                    )

                # Promote to outer scope so post-loop code can access it
                response = api_response

                if retry_attempt > 0 and last_error is not None:
                    _recovered_info: RetryableError | None = getattr(last_error, "error_info", None)
                    if _recovered_info:
                        _rec_provider = (
                            _recovered_info.details.get("provider")
                            if _recovered_info.details
                            else None
                        ) or "unknown"
                        await capture_issue(
                            f"{_rec_provider}.{_recovered_info.error_type}",
                            error_type=_recovered_info.error_type,
                            provider=_rec_provider if _rec_provider != "unknown" else None,
                            model=current_request.config.model,
                            status_code=_recovered_info.status_code,
                            is_retryable=True,
                            was_recovered=True,
                            retry_count=retry_attempt,
                            user_id=exec_ctx.user_id,
                            conversation_id=exec_ctx.conversation_id,
                            request_id=current_request.request_id,
                            detail={
                                "message": _recovered_info.message,
                                "iteration": iteration,
                                "recovered_after_attempts": retry_attempt,
                            },
                        )
                        await _emit_provider_retry(
                            exec_ctx=exec_ctx,
                            current_request=current_request,
                            error_info=_recovered_info,
                            provider=_rec_provider,
                            iteration=iteration,
                            failed_attempt=retry_attempt,
                            max_retries=_max_retries_for_error(
                                _recovered_info,
                                max_retries_per_iteration,
                            ),
                            state="recovered",
                        )

                break

            except Exception as e:
                last_error = e
                # Provider for telemetry / error classification comes from the
                # RESOLVED CATALOG (endpoint vendor), never a model-name guess.
                provider = await _catalog_vendor_for(current_request.config)

                # Check if error has classification info attached
                attached: RetryableError | None = getattr(e, "error_info", None)
                if attached is not None:
                    error_info = attached
                else:
                    error_info = classify_provider_error(provider, e)

                # Paid failed attempts are usage, even when a later retry
                # succeeds. Harvest each one immediately and mark the exception
                # so terminal cleanup cannot count it twice.
                _record_billed_usage_on_failure(
                    current_request,
                    e,
                    iteration=iteration,
                    provider_attempt=retry_attempt + 1,
                )

                # Provider responses can contain account, billing, and prompt
                # details.  Their full diagnostics are retained in the runtime
                # snapshot/issue capture below, but operational logs receive a
                # stable, non-sensitive classification rather than repr(e) or
                # the full request payload.
                if error_info.error_type == "matrx_internal_error":
                    vcprint(
                        {
                            "request_id": current_request.request_id,
                            "conversation_id": current_request.conversation_id,
                            "model": current_request.config.model,
                            "provider": provider,
                            "iteration": iteration,
                            "provider_attempt": retry_attempt + 1,
                            "exception_type": (
                                f"{type(e).__module__}.{type(e).__qualname__}"
                            ),
                            "message": str(e) or type(e).__name__,
                        },
                        "[AI REQUESTS EXECUTE UNTIL COMPLETE] Internal Exception Error",
                        color="red",
                    )
                else:
                    vcprint(
                        {
                            "request_id": current_request.request_id,
                            "conversation_id": current_request.conversation_id,
                            "model": current_request.config.model,
                            "provider": provider,
                            "error_type": error_info.error_type,
                            "status_code": error_info.status_code,
                            "retryable": error_info.is_retryable,
                            "iteration": iteration,
                            "provider_attempt": retry_attempt + 1,
                            "exception_type": (
                                f"{type(e).__module__}.{type(e).__qualname__}"
                            ),
                            "message": error_info.message
                            or type(e).__name__,
                        },
                        "[AI REQUESTS EXECUTE UNTIL COMPLETE] Provider Error",
                        color="yellow",
                    )

                # Derive the issue key for ops telemetry
                _issue_provider = (
                    error_info.details.get("provider") or provider
                    if error_info.details
                    else provider
                ) or "unknown"
                _issue_key = f"{_issue_provider}.{error_info.error_type}"
                effective_max_retries = _max_retries_for_error(
                    error_info,
                    max_retries_per_iteration,
                )

                # ── OVERLOAD-CLASS REROUTING (model-level policy) ──────────
                # 429/529/503/overloaded: ai.model_definition.retry_max_attempts
                # caps SAME-model retries and retry_fallback_id reroutes the
                # request when they are exhausted. One decision function —
                # decide_overload_action — owns the whole policy; this block
                # only feeds it and applies its verdict through the EXISTING
                # retry machinery (no parallel retry path).
                _overload_backoff_attempt = retry_attempt
                if is_reroutable_provider_error(error_info):
                    _ov_policy = await load_overload_policy(
                        current_request.config.model, overload_state
                    )
                    _attempts_on_model = retry_attempt - overload_state.attempt_base + 1
                    # Backoff schedule position is per-MODEL, not global — the
                    # fallback model starts its schedule from the top.
                    _overload_backoff_attempt = _attempts_on_model - 1
                    effective_max_retries = (
                        overload_state.attempt_base + _ov_policy.retry_max_attempts
                    )
                    # Sibling-offering ladder — computed only once the same-
                    # offering retry budget is exhausted (a catalog read on
                    # every transient 429 would be waste). Degrades to None →
                    # classic model-level behavior.
                    _ov_ladder = None
                    if (
                        error_info.error_type == "billing_error"
                        or _attempts_on_model > _ov_policy.retry_max_attempts
                    ):
                        _ov_ladder = await load_offering_ladder(
                            current_request.config.model or "",
                            routing_offering_id=current_request.config.routing_offering_id,
                            offerings_tried=overload_state.offerings_tried,
                        )
                    _ov_decision = decide_overload_action(
                        error_info=error_info,
                        current_model=current_request.config.model or "",
                        attempts_on_model=_attempts_on_model,
                        policy=_ov_policy,
                        models_tried=overload_state.models_tried,
                        hops=overload_state.hops,
                        produced_output=bool(_partial_response_from_emitter(exec_ctx).messages),
                        current_offering_id=(
                            _ov_ladder.current_offering_id if _ov_ladder else None
                        ),
                        sibling_offering_ids=(
                            _ov_ladder.sibling_offering_ids if _ov_ladder else []
                        ),
                        offering_hops=overload_state.offering_hops,
                    )
                    if (
                        _ov_decision.action == "reroute_offering"
                        and _ov_decision.to_offering_id
                        and _ov_ladder is not None
                    ):
                        _note = _ov_decision.note
                        vcprint(
                            _note.model_dump()
                            if _note
                            else {"to_offering_id": _ov_decision.to_offering_id},
                            title=(
                                f"🔀 PROVIDER SIBLING-OFFERING REROUTE "
                                f"[{current_request.config.model}] offering "
                                f"'{_ov_ladder.current_offering_id}' → "
                                f"'{_ov_decision.to_offering_id}': {_ov_decision.reason}. "
                                "SAME model, SAME canonical config — re-resolved through "
                                "the sibling offering's api rules on the next attempt."
                            ),
                            color="red",
                            log_level="WARNING",
                        )
                        await capture_issue(
                            _issue_key,
                            error_type=error_info.error_type,
                            provider=_issue_provider if _issue_provider != "unknown" else None,
                            model=current_request.config.model,
                            status_code=error_info.status_code,
                            is_retryable=error_info.is_retryable,
                            was_recovered=False,
                            retry_count=retry_attempt,
                            user_id=exec_ctx.user_id,
                            conversation_id=exec_ctx.conversation_id,
                            request_id=current_request.request_id,
                            detail={
                                "message": error_info.message,
                                "iteration": iteration,
                                "overload_reroute": _note.model_dump() if _note else None,
                            },
                        )
                        await exec_ctx.emitter.send_info(
                            InfoPayload(
                                code=(
                                    "provider_credit_reroute"
                                    if error_info.error_type == "billing_error"
                                    else "provider_overload_reroute"
                                ),
                                system_message=_ov_decision.reason,
                                user_message=(
                                    "The selected AI service could not fund the call — "
                                    "automatically continuing on another service for the same model."
                                    if error_info.error_type == "billing_error"
                                    else "The AI provider is overloaded — automatically continuing "
                                    "your request on another service for the same model."
                                ),
                                metadata={
                                    "iteration": iteration,
                                    "retry_attempt": retry_attempt,
                                    **(_note.model_dump() if _note else {}),
                                },
                            )
                        )
                        if _note is not None:
                            current_request.metadata.setdefault("overload_reroutes", []).append(
                                _note.model_dump()
                            )
                        overload_state.record_offering_reroute(
                            from_offering_id=_ov_ladder.current_offering_id,
                            note=_note
                            if _note is not None
                            else RerouteNote(  # pragma: no cover — reroute always carries a note
                                scope="offering",
                                from_model=current_request.config.model or "",
                                to_model=current_request.config.model or "",
                                from_offering_id=_ov_ladder.current_offering_id,
                                to_offering_id=_ov_decision.to_offering_id,
                                attempts_on_model=_attempts_on_model,
                                error_type=error_info.error_type,
                                reason=_ov_decision.reason,
                            ),
                            next_base=retry_attempt + 1,
                        )
                        # RUNTIME pin (never persisted — the user's own pin in
                        # config.offering_id stays intact for future turns) +
                        # restore the canonical model ref so resolution can't
                        # trip on a diverging provider_model_id. The sibling
                        # gets a full same-model budget.
                        current_request.config.runtime_offering_id = (
                            _ov_decision.to_offering_id
                        )
                        current_request.config.model = _ov_ladder.canonical_model_id
                        retry_loop_ceiling = max(
                            retry_loop_ceiling,
                            retry_attempt + 1 + len(PROVIDER_OVERLOAD_RETRY_DELAYS),
                        )
                        continue
                    if _ov_decision.action == "reroute" and _ov_decision.to_model:
                        _note = _ov_decision.note
                        vcprint(
                            _note.model_dump() if _note else {"to_model": _ov_decision.to_model},
                            title=(
                                f"🔀 PROVIDER REROUTE [{current_request.config.model}] → "
                                f"'{_ov_decision.to_model}': {_ov_decision.reason}. The SAME "
                                "canonical config continues on the fallback model — the "
                                "resolution pipeline re-translates it on the next call."
                            ),
                            color="red",
                            log_level="WARNING",
                        )
                        await capture_issue(
                            _issue_key,
                            error_type=error_info.error_type,
                            provider=_issue_provider if _issue_provider != "unknown" else None,
                            model=current_request.config.model,
                            status_code=error_info.status_code,
                            is_retryable=error_info.is_retryable,
                            was_recovered=False,
                            retry_count=retry_attempt,
                            user_id=exec_ctx.user_id,
                            conversation_id=exec_ctx.conversation_id,
                            request_id=current_request.request_id,
                            detail={
                                "message": error_info.message,
                                "iteration": iteration,
                                "overload_reroute": _note.model_dump() if _note else None,
                            },
                        )
                        await exec_ctx.emitter.send_info(
                            InfoPayload(
                                code=(
                                    "provider_credit_reroute"
                                    if error_info.error_type == "billing_error"
                                    else "provider_overload_reroute"
                                ),
                                system_message=_ov_decision.reason,
                                user_message=(
                                    "The selected AI service could not fund the call — "
                                    "automatically continuing on a fallback model."
                                    if error_info.error_type == "billing_error"
                                    else "The AI provider is overloaded — automatically continuing "
                                    "your request on a fallback model."
                                ),
                                metadata={
                                    "iteration": iteration,
                                    "retry_attempt": retry_attempt,
                                    **(_note.model_dump() if _note else {}),
                                },
                            )
                        )
                        # Adjustment-style note in the request metadata — rides
                        # the usual call record (CompletedRequest merges
                        # request.metadata into the persisted metadata).
                        if _note is not None:
                            current_request.metadata.setdefault("overload_reroutes", []).append(
                                _note.model_dump()
                            )
                        overload_state.record_reroute(
                            from_model=current_request.config.model or "",
                            note=_note
                            if _note is not None
                            else RerouteNote(  # pragma: no cover — reroute always carries a note
                                from_model=current_request.config.model or "",
                                to_model=_ov_decision.to_model,
                                attempts_on_model=_attempts_on_model,
                                error_type=error_info.error_type,
                                reason=_ov_decision.reason,
                            ),
                            next_base=retry_attempt + 1,
                        )
                        # Swap the model — resolve_call_profile inside
                        # UnifiedAIClient.execute re-resolves + re-translates
                        # the SAME canonical config for the fallback on the
                        # next attempt. Extend the ceiling so the fallback
                        # gets a full budget. Any offering pin (user or
                        # runtime) belongs to the ABANDONED model — clear both
                        # or the fallback model's resolution raises on a
                        # cross-model pin.
                        current_request.config.model = _ov_decision.to_model
                        current_request.config.offering_id = None
                        current_request.config.runtime_offering_id = None
                        retry_loop_ceiling = max(
                            retry_loop_ceiling,
                            retry_attempt + 1 + len(PROVIDER_OVERLOAD_RETRY_DELAYS),
                        )
                        continue

                _will_retry = error_info.is_retryable and retry_attempt < effective_max_retries

                # Handle retryable errors (error_info is now set)
                if _will_retry:
                    backoff_delay = error_info.get_backoff_delay(_overload_backoff_attempt)
                    retry_at = time.time() + backoff_delay
                    failed_attempt = retry_attempt + 1
                    next_attempt = retry_attempt + 2

                    vcprint(
                        {
                            "request_id": current_request.request_id,
                            "conversation_id": current_request.conversation_id,
                            "model": current_request.config.model,
                            "provider": provider,
                            "error_type": error_info.error_type,
                            "attempt": failed_attempt,
                            "max_attempts": effective_max_retries + 1,
                            "retry_delay_seconds": backoff_delay,
                            "retry_at": retry_at,
                        },
                        "[AI REQUESTS EXECUTE UNTIL COMPLETE] Provider retry scheduled",
                        color="yellow",
                    )

                    await exec_ctx.emitter.send_phase("retrying")
                    await _emit_provider_retry(
                        exec_ctx=exec_ctx,
                        current_request=current_request,
                        error_info=error_info,
                        provider=provider,
                        iteration=iteration,
                        failed_attempt=failed_attempt,
                        next_attempt=next_attempt,
                        max_retries=effective_max_retries,
                        state="scheduled",
                        retry_delay=backoff_delay,
                        retry_at=retry_at,
                    )
                    await exec_ctx.emitter.send_info(
                        InfoPayload(
                            code="provider_retry",
                            system_message=error_info.user_message,
                            user_message=error_info.user_message,
                            metadata={
                                "error_type": error_info.error_type,
                                "retry_attempt": failed_attempt,
                                "next_attempt": next_attempt,
                                "max_retries": effective_max_retries,
                                "retry_delay": backoff_delay,
                                "retry_at": retry_at,
                            },
                        )
                    )

                    wait_result = await _wait_for_retry_or_control(
                        current_request.request_id or getattr(exec_ctx, "request_id", None),
                        backoff_delay,
                    )
                    if wait_result == "cancelled":
                        await _emit_provider_retry(
                            exec_ctx=exec_ctx,
                            current_request=current_request,
                            error_info=error_info,
                            provider=provider,
                            iteration=iteration,
                            failed_attempt=failed_attempt,
                            max_retries=effective_max_retries,
                            state="cancelled",
                        )
                        await exec_ctx.emitter.send_phase("complete")
                        return await _finalize_and_persist(
                            current_request=current_request,
                            iteration=iteration,
                            final_response=UnifiedResponse(messages=[]),
                            metadata={
                                "status": "cancelled",
                                "error": "Request cancelled during provider retry wait.",
                                "error_type": error_info.error_type,
                                "provider": _provider_name_for_event(error_info, provider),
                                "model": current_request.config.model,
                                "cancelled_iteration": iteration,
                            },
                            trigger_position=trigger_position,
                            pre_execution_message_count=pre_execution_message_count,
                            debug=debug,
                            state=state,
                        )
                    if wait_result == "retry_now":
                        await _emit_provider_retry(
                            exec_ctx=exec_ctx,
                            current_request=current_request,
                            error_info=error_info,
                            provider=provider,
                            iteration=iteration,
                            failed_attempt=failed_attempt,
                            next_attempt=next_attempt,
                            max_retries=effective_max_retries,
                            state="retrying_now",
                        )
                    continue
                else:
                    if error_info.error_type == "provider_overloaded" and error_info.is_retryable:
                        await capture_issue(
                            _issue_key,
                            error_type=error_info.error_type,
                            provider=_issue_provider if _issue_provider != "unknown" else None,
                            model=current_request.config.model,
                            status_code=error_info.status_code,
                            is_retryable=True,
                            was_recovered=False,
                            retry_count=retry_attempt,
                            user_id=exec_ctx.user_id,
                            conversation_id=exec_ctx.conversation_id,
                            request_id=current_request.request_id,
                            detail={
                                "message": error_info.message,
                                "user_message": error_info.user_message,
                                "retry_after": error_info.retry_after,
                                "iteration": iteration,
                                "retries_exhausted": True,
                                "suspended": True,
                            },
                        )
                        await _emit_provider_retry(
                            exec_ctx=exec_ctx,
                            current_request=current_request,
                            error_info=error_info,
                            provider=provider,
                            iteration=iteration,
                            failed_attempt=retry_attempt + 1,
                            max_retries=effective_max_retries,
                            state="suspended",
                        )
                        await exec_ctx.emitter.send_phase("complete")
                        await exec_ctx.emitter.send_warning(
                            WarningPayload(
                                code="provider_overload_suspended",
                                system_message=(
                                    f"{_provider_name_for_event(error_info, provider)} remained "
                                    f"overloaded after {retry_attempt + 1} provider attempts."
                                ),
                                user_message=(
                                    "The AI provider is still busy. This is a provider-side capacity "
                                    "problem, not a problem with your request. We paused here so you "
                                    "can retry when the provider has capacity."
                                ),
                                level="medium",
                                recoverable=True,
                                metadata={
                                    "error_type": error_info.error_type,
                                    "provider": _provider_name_for_event(error_info, provider),
                                    "retry_attempts": retry_attempt + 1,
                                    "max_retries": effective_max_retries,
                                    "status_code": error_info.status_code,
                                    "iteration": iteration,
                                },
                            )
                        )
                        if current_timing.end_time is None:
                            current_timing.end_time = time.time()
                            current_request.add_timing(current_timing)
                        _record_billed_usage_on_failure(
                            current_request,
                            e,
                            iteration=iteration,
                            provider_attempt=retry_attempt + 1,
                        )
                        _partial_resp = _partial_response_from_emitter(exec_ctx)
                        current_request = _append_partial_response(
                            current_request,
                            _partial_resp,
                            state,
                        )
                        return await _finalize_and_persist(
                            current_request=current_request,
                            iteration=iteration,
                            final_response=_partial_resp,
                            metadata={
                                "status": "suspended_provider_overload",
                                "error": error_info.message,
                                "error_type": error_info.error_type,
                                "provider": _provider_name_for_event(error_info, provider),
                                "model": current_request.config.model,
                                "status_code": error_info.status_code,
                                "retries_exhausted": True,
                                "retry_attempts": retry_attempt + 1,
                                "iteration": iteration,
                            },
                            trigger_position=trigger_position,
                            pre_execution_message_count=pre_execution_message_count,
                            debug=debug,
                            state=state,
                        )

                    # Non-retryable or max retries exceeded
                    _retries_exhausted = error_info.is_retryable
                    if not _retries_exhausted:
                        vcprint(
                            f"✗ Non-retryable error: {error_info.message}",
                            "[AI REQUESTS EXECUTE UNTIL COMPLETE] Non-retryable Error",
                            color="red",
                        )
                    else:
                        vcprint(
                            f"✗ Max retries exceeded after {retry_attempt + 1} attempts",
                            "[AI REQUESTS EXECUTE UNTIL COMPLETE] Max Retries Exceeded",
                            color="red",
                        )

                    await capture_issue(
                        _issue_key,
                        error_type=error_info.error_type,
                        provider=_issue_provider if _issue_provider != "unknown" else None,
                        model=current_request.config.model,
                        status_code=error_info.status_code,
                        is_retryable=error_info.is_retryable,
                        was_recovered=False,
                        retry_count=retry_attempt,
                        user_id=exec_ctx.user_id,
                        conversation_id=exec_ctx.conversation_id,
                        request_id=current_request.request_id,
                        detail={
                            "message": error_info.message,
                            "user_message": error_info.user_message,
                            "retry_after": error_info.retry_after,
                            "iteration": iteration,
                            "retries_exhausted": _retries_exhausted,
                        },
                    )

                    await _capture_terminal_provider_failure(
                        e,
                        exec_ctx=exec_ctx,
                        current_request=current_request,
                        error_info=error_info,
                        provider=provider,
                        iteration=iteration,
                        retry_attempt=retry_attempt,
                    )

                    await exec_ctx.emitter.send_error(
                        error_type=error_info.error_type,
                        # Provider messages can contain account identifiers,
                        # request fragments, or SDK formatting. The stream is
                        # a user-facing contract; raw diagnostics remain in
                        # the server-side snapshot and ops issue record.
                        message=error_info.user_message,
                        user_message=error_info.user_message
                        if not error_info.is_retryable
                        else f"Failed after {retry_attempt + 1} retry attempts. {error_info.user_message}",
                    )

                    # Containment: finalize this request as failed and return
                    # a CompletedRequest instead of re-raising. Re-raising
                    # bubbles up to matrx-connect's _run_with_error_handling,
                    # which calls emitter.fatal_error() → tracker.fail_all_pending()
                    # → every reserved cx_request/cx_message/cx_tool_call record in
                    # the conversation gets tombstoned with status=failed. A single
                    # bad turn (e.g. provider 400 on one model) should fail
                    # *that turn*, not the entire conversation.
                    if current_timing.end_time is None:
                        current_timing.end_time = time.time()
                        current_request.add_timing(current_timing)
                    # Record provider-billed usage from the failed call (the
                    # provider bills the instant the call starts — a 400/timeout
                    # after billing must still cost the failed row, not $0).
                    _record_billed_usage_on_failure(
                        current_request,
                        e,
                        iteration=iteration,
                        provider_attempt=retry_attempt + 1,
                    )
                    # Recover any text streamed before the provider raised
                    # mid-stream (common on a safety block after some tokens) so
                    # the partial answer the user saw is persisted, not lost.
                    _partial_resp = _partial_response_from_emitter(exec_ctx)
                    current_request = _append_partial_response(
                        current_request, _partial_resp, state
                    )
                    return await _finalize_and_persist(
                        current_request=current_request,
                        iteration=iteration,
                        final_response=_partial_resp,
                        metadata={
                            "status": "failed",
                            "error": error_info.user_message,
                            "error_type": error_info.error_type,
                            "provider_error_type": error_info.details.get("provider_error_type"),
                            "provider": _issue_provider,
                            "model": current_request.config.model,
                            "status_code": error_info.status_code,
                            "retries_exhausted": _retries_exhausted,
                            "retry_attempts": retry_attempt + 1,
                            "iteration": iteration,
                        },
                        trigger_position=trigger_position,
                        pre_execution_message_count=pre_execution_message_count,
                        debug=debug,
                        state=state,
                    )

        # After retry loop - check if we have a valid response
        if response is None:
            # All retries failed, handle the last error
            vcprint(
                f"\n✗ All retries failed in iteration {iteration}",
                "[AI REQUESTS EXECUTE UNTIL COMPLETE] All Retries Failed",
                color="red",
            )

            if current_timing.end_time is None:
                current_timing.end_time = time.time()
                current_request.add_timing(current_timing)

            # Get error info from last_error if available
            last_error_info: RetryableError | None = getattr(last_error, "error_info", None)

            error_message = last_error_info.message if last_error_info else str(last_error)
            error_type = (
                last_error_info.error_type if last_error_info else type(last_error).__name__
            )

            # Record provider-billed usage from the final failed attempt so the
            # failed row carries real cost (the provider billed us even though
            # every retry ultimately failed).
            _record_billed_usage_on_failure(
                current_request,
                last_error,
                iteration=iteration,
                provider_attempt=retry_attempt + 1,
            )
            # Recover any partial text streamed during the final (failed) attempt
            # so it is persisted rather than lost.
            _partial_resp = _partial_response_from_emitter(exec_ctx)
            current_request = _append_partial_response(current_request, _partial_resp, state)
            return await _finalize_and_persist(
                current_request=current_request,
                iteration=iteration,
                final_response=_partial_resp,
                metadata={
                    "error": error_message,
                    "error_type": error_type,
                    "error_iteration": iteration,
                    "status": "failed",
                    "retries_exhausted": True,
                },
                trigger_position=trigger_position,
                pre_execution_message_count=pre_execution_message_count,
                debug=debug,
                state=state,
            )

        # IF no errors, and response isn't None, we go here...

        # Mid-loop durability checkpoint: if this iteration's response triggers
        # at least one CLIENT-delegated tool call, the loop is about to suspend
        # on an in-memory Future awaiting the client's POST. Flush the assistant
        # cx_message row NOW (with the real tool_calls content) so that if the
        # SSE dies or the server restarts during the wait, the conversation is
        # still fully reconstructable from cx_message + cx_tool_call rows.
        iteration_message_id: str | None = None
        if _response_has_live_client_delegated_call(response):
            iteration_message_id = await _flush_assistant_message_mid_loop(
                response=response,
                current_request=current_request,
                exec_ctx=exec_ctx,
                reserved_messages=reserved_messages,
                parent_refs=_parent_refs,
                trigger_position=trigger_position,
                state=state,
            )
            # The assistant message for this turn is complete (it carries the
            # delegated tool_call) and the loop is about to SUSPEND awaiting the
            # client — possibly forever if the client never returns. Commit the
            # assistant NOW so a process death during the wait can't lose it
            # (e.g. the question the agent just asked the user). The tool-result
            # messages finalize after the client returns, via the per-turn
            # barrier below. (Persistence contract — CLAUDE.md.)
            if iteration_message_id is not None:
                if response.usage is not None:
                    response.usage.metadata["response_message_id"] = iteration_message_id
                from matrx_ai.persistence.queue_helpers import (
                    get_coordinator,
                    queue_user_request_update,
                )

                _delegate_coord = get_coordinator()
                if _delegate_coord is not None:
                    _assistant_pos = len(current_request.config.messages.to_list())
                    # Heartbeat the request BEFORE suspending on the client. A
                    # delegated wait commits no turns, so without this a long
                    # client/human turn (a prompt the user takes minutes to
                    # answer) would let last_activity_at go stale and the watchdog
                    # would falsely abandon an alive-and-waiting request. Rides
                    # this same pre-suspend commit (atomic). (Persistence contract.)
                    _req_id = current_request.request_id or getattr(exec_ctx, "request_id", None)
                    if _req_id:
                        from datetime import UTC, datetime

                        queue_user_request_update(_req_id, last_activity_at=datetime.now(UTC))
                    await _delegate_coord.finalize(reason=f"turn_{iteration}_delegate_precommit")
                    state.committed_position = max(state.committed_position, _assistant_pos)

        # Required-member forced turn just returned from the provider: the
        # restriction (only the missing member tools + tool_choice='required')
        # applied to THAT provider call only. Restore the full toolset now,
        # BEFORE dispatch, so the loop continues normally afterwards —
        # dispatch reads response.tool_calls, never config.tools, so the
        # member call the forced turn produced still executes.
        if state is not None and state.required_member_forced_pending:
            _rm_saved = state.required_member_saved_tools
            if _rm_saved is not None:
                (
                    current_request.config.tools,
                    current_request.config.custom_tools,
                    current_request.config.tool_choice,
                ) = _rm_saved
            state.required_member_forced_pending = False
            state.required_member_saved_tools = None

        # Process tool calls
        try:
            # Check for tool calls
            t0 = time.time()
            (
                tool_results,
                tool_call_usage,
                child_token_usages,
                pending_call_ids,
                iteration_auto_stub_keys,
                handoff_outcome,
            ) = await handle_tool_calls(
                response, current_request, iteration, message_id=iteration_message_id
            )
            current_timing.tool_execution_duration = time.time() - t0

            # Child agent token usages are intentionally NOT added to the parent's
            # usage_history here.  Each child agent creates its own cx_request rows
            # (linked to the same cx_user_request via shared request_id).  Adding
            # child usages to the parent's usage_history would cause double-counting
            # because persist_completed_request() aggregates ALL cx_request rows
            # under the shared user_request_id.

            # Record completion of this iteration's main work
            current_timing.end_time = time.time()
            current_request.add_timing(current_timing)

            # Track tool calls if any were made
            current_request.add_tool_calls(tool_call_usage)

            # Always update request with the response and tool results (if any)
            current_request = AIMatrixRequest.add_response(
                original_request=current_request,
                response=response,
                tool_results=tool_results,
            )
            # Keep the cancel-persist context pointing at the carried-forward
            # request (it holds the cumulative usage). If a disconnect lands
            # between here and the next loop top, the outer handler still has
            # the full accumulated cost.
            state.current_request = current_request

            # Turn-directive scan (host seam) — the model can groom context
            # mid-prose via an inline fence without spending a tool call; the
            # handler's queued stamps ride the barrier commit below. THIS
            # response also just CONSUMED the previous batch's serve-once value
            # reads — their auto-stub keys are drained here (consumption time,
            # never completion time), and this batch's keys queue up next.
            await _apply_turn_directives(
                response,
                current_request,
                auto_stub_keys=state.pending_auto_stub_keys if state else [],
            )
            if state is not None:
                state.pending_auto_stub_keys = list(iteration_auto_stub_keys or [])

            # ── TERMINAL HANDOFF (Pattern 1) ──────────────────────────────
            # A handoff-flagged agent tool succeeded: its answer already
            # streamed to the client on this wire; now it persists as the
            # conversation's OWN assistant response and the loop ends — the
            # caller is never called again (its next-turn history shows
            # [tool_use → compact stub → "its own" response]: structural
            # in-context learning). The synthetic row is appended BEFORE the
            # barrier so stub + response commit atomically — a crash can never
            # leave a durable 'handoff_delivered' claim with no response.
            if handoff_outcome is not None:
                completed_handoff = await _finalize_handoff(
                    handoff_outcome=handoff_outcome,
                    current_request=current_request,
                    iteration=iteration,
                    response=response,
                    trigger_position=trigger_position,
                    pre_execution_message_count=pre_execution_message_count,
                    debug=debug,
                    state=state,
                    exec_ctx=exec_ctx,
                )
                if completed_handoff is not None:
                    return completed_handoff
                # The turn-boundary inbox held new user message(s): B's answer
                # is durable, and the loop continues so the caller answers the
                # genuinely-new input on top of it (the 'queue anytime'
                # guarantee survives the terminal exit).
                current_request = state.current_request or current_request
                continue

            terminal_problem = (
                _terminal_response_problem(response)
                if tool_results is None and not pending_call_ids
                else None
            )
            if terminal_problem is not None:
                error_type, user_message = terminal_problem
                # Mark before the final persistence barrier so a cold reload
                # renders the same failed turn as the live stream.
                for message in response.messages:
                    if getattr(message, "role", None) == "assistant":
                        message.status = "failed"
                last_assistant = current_request.config.messages.get_last_by_role(
                    "assistant"
                )
                if last_assistant is not None:
                    last_assistant.status = "failed"

                vcprint(
                    {
                        "error_type": error_type,
                        "iteration": iteration,
                        "model": current_request.config.model,
                        "finish_reason": response.finish_reason,
                    },
                    "[execute_until_complete] Provider reported a terminal "
                    "success with no user-visible assistant output",
                    color="red",
                )
                await exec_ctx.emitter.send_error(
                    error_type=error_type,
                    message=user_message,
                    user_message=user_message,
                )
                return await _finalize_and_persist(
                    current_request=current_request,
                    iteration=iteration,
                    final_response=response,
                    metadata={
                        "status": "failed",
                        "error": user_message,
                        "error_type": error_type,
                        "finish_reason": response.finish_reason,
                        "iteration": iteration,
                    },
                    trigger_position=trigger_position,
                    pre_execution_message_count=pre_execution_message_count,
                    debug=debug,
                    state=state,
                )

            # ── PER-TURN COMMIT BARRIER ───────────────────────────────────
            # This turn's data (assistant message + any tool results) is now
            # complete and in current_request. Commit it DURABLY before we loop
            # or exit. A failed commit raises PersistenceBarrierError and stops
            # the run — we never continue on top of data that didn't land.
            # (Persistence contract — CLAUDE.md.)
            await _persist_turn_and_commit(
                current_request=current_request,
                iteration=iteration,
                final_response=response,
                trigger_position=trigger_position,
                pre_execution_message_count=pre_execution_message_count,
                debug=debug,
                state=state,
            )

            # ── DELEGATION SUSPENSION ─────────────────────────────────────
            # One or more tool calls were delegated to the client. Delegation
            # is a hard suspension point: the assistant message + any completed
            # server-tool results just committed durably above, and the
            # delegated cx_tool_call rows are 'delegated'. STOP — do not loop on a
            # result that doesn't exist yet. The client POSTs results to
            # /tool_results and, once no delegated rows remain, /resume
            # reconstructs the conversation and continues the loop. This is what
            # structurally kills the runaway-tool-call loop.
            # (docs/tool_delegation/DELEGATION_LOOP_BUGS.md)
            if pending_call_ids:
                return await _suspend_for_delegation(
                    exec_ctx=exec_ctx,
                    state=state,
                    current_request=current_request,
                    response=response,
                    iteration=iteration,
                    pending_call_ids=pending_call_ids,
                    trigger_position=trigger_position,
                    pre_execution_message_count=pre_execution_message_count,
                    debug=debug,
                )

            # if debug:
            #     print("\n\n[EXECUTE UNTIL COMPLETE] DEBUG PRINT Execute Until complete 2\n\n")
            #     rich.print(current_request)

            # Finish - no more tool calls needed
            if tool_results is None:
                # Self-drain guarantee: a message queued into this conversation's
                # Turn-Boundary Inbox DURING this final turn must be answered in
                # THIS stream, not stranded until the user sends again. Drain it
                # now; if anything was injected, loop one more model turn instead
                # of exiting. Bounded by the while loop's max_iterations. This is
                # what makes "queue anytime, even at the last second" just work —
                # the run doesn't go idle while the inbox has pending items.
                from matrx_connect.context.app_context import try_get_app_context as _try_ctx

                from matrx_ai.tools.dynamic_drain import drain_pending_injections

                _inbox_ctx = _try_ctx()
                if _inbox_ctx is not None:
                    _n_before = len(current_request.config.messages)
                    # include_turn_end: the run is completely done — deliver
                    # THE NEXT QUEUE-mode message (one per turn) alongside any
                    # remaining steers, then loop to answer it.
                    await drain_pending_injections(
                        current_request.config, _inbox_ctx, include_turn_end=True
                    )
                    if len(current_request.config.messages) > _n_before:
                        await exec_ctx.emitter.send_info(
                            InfoPayload(
                                code="inbox_continue",
                                system_message="Queued message(s) drained at end of turn — continuing to answer them.",
                                user_message="",
                                metadata={"iteration": iteration, "will_continue": True},
                            )
                        )
                        continue

                # ── REQUIRED-MEMBER GATE (C-26, ruling D-38) ──────────────
                # The run wants to finish with no tool calls. If its Orchestra
                # declared required member(s) that were never successfully
                # called, this finalize BOUNDARY is where the runtime — not
                # the prompt — refuses: one course-correction turn forced to
                # the missing member tool(s) (tool_choice='required'); a
                # second miss is terminal (chat: distinct resumable pause;
                # workflow step: loud failure). By _finalize_and_persist the
                # turn is durable, so the check must fire here.
                _rm_action, _rm_report, _rm_is_workflow = _required_member_gate(
                    current_request, state
                )
                if _rm_action == "force" and _rm_report is not None and state is not None:
                    state.required_member_intervened = True
                    state.required_member_forced_pending = True
                    state.required_member_saved_tools = (
                        list(current_request.config.tools or []),
                        list(current_request.config.custom_tools or []),
                        current_request.config.tool_choice,
                    )
                    current_request.config.tools = list(_rm_report.forceable_names)
                    current_request.config.custom_tools = []
                    current_request.config.tool_choice = "required"

                    from matrx_ai.config import TextContent, UnifiedMessage

                    _rm_titles = ", ".join(m.display for m in _rm_report.missing)
                    _rm_notice = (
                        f"⚠️ SYSTEM NOTICE (not from the user): this Orchestra "
                        f"designates the following member(s) as REQUIRED — they "
                        f"MUST be successfully consulted before you finish: "
                        f"{_rm_titles}. You attempted to finish without calling "
                        f"them. For your NEXT turn only the required member "
                        f"tool(s) are available and a tool call is mandatory: "
                        f"call them now with a clear, complete request "
                        f"(include the draft answer or material they must "
                        f"review). Your full toolset returns afterwards, and "
                        f"you will then deliver your final answer incorporating "
                        f"their output."
                    )
                    current_request.config.messages.append(
                        UnifiedMessage(role="user", content=[TextContent(text=_rm_notice)])
                    )
                    vcprint(
                        f"⚠️  Required-member gate: finish attempted without required "
                        f"member(s) [{_rm_titles}] — forcing one corrective turn.",
                        "[AI REQUESTS EXECUTE UNTIL COMPLETE] Required Member Gate",
                        color="yellow",
                    )
                    await exec_ctx.emitter.send_phase("processing")
                    await exec_ctx.emitter.send_warning(
                        WarningPayload(
                            code="required_member_correction",
                            system_message=(
                                f"Orchestrator tried to finish without required "
                                f"member(s): {_rm_titles}. Forcing one turn "
                                f"restricted to the required member tool(s)."
                            ),
                            user_message=(
                                "The orchestrator skipped a required team member — "
                                "correcting course so they are consulted before it finishes."
                            ),
                            level="medium",
                            recoverable=True,
                            metadata={
                                "missing_members": [
                                    {
                                        "agent_id": m.agent_id,
                                        "role_title": m.role_title,
                                        "projected_name": m.projected_name,
                                    }
                                    for m in _rm_report.missing
                                ],
                                "forced_tools": list(_rm_report.forceable_names),
                                "iteration": iteration,
                            },
                        )
                    )
                    continue  # one forced turn — restricted tools, required call

                if _rm_action == "fail" and _rm_report is not None:
                    from matrx_ai.orchestrator.required_members import (
                        REQUIRED_MEMBER_ERROR_TYPE,
                    )

                    _rm_missing = ", ".join(m.display for m in _rm_report.missing)
                    _rm_msg = (
                        f"This Orchestra requires member(s) [{_rm_missing}] to be "
                        f"successfully consulted before the orchestrator finishes, "
                        f"and it finished without them despite a forced correction "
                        f"turn. The workflow step fails so a briefing its required "
                        f"member never contributed to is not recorded as complete."
                    )
                    vcprint(
                        f"🛑 Required-member gate: workflow step FAILED — {_rm_msg}",
                        "[AI REQUESTS EXECUTE UNTIL COMPLETE] Required Member Gate",
                        color="red",
                    )
                    await exec_ctx.emitter.send_error(
                        error_type=REQUIRED_MEMBER_ERROR_TYPE,
                        message=_rm_msg,
                        user_message=_rm_msg,
                    )
                    return await _finalize_and_persist(
                        current_request=current_request,
                        iteration=iteration,
                        final_response=response,
                        metadata={
                            "status": "failed",
                            "error": _rm_msg,
                            "error_type": REQUIRED_MEMBER_ERROR_TYPE,
                            "finish_reason": response.finish_reason,
                            "iteration": iteration,
                        },
                        trigger_position=trigger_position,
                        pre_execution_message_count=pre_execution_message_count,
                        debug=debug,
                        state=state,
                    )

                if _rm_action == "pause" and _rm_report is not None:
                    _rm_missing = ", ".join(m.display for m in _rm_report.missing)
                    vcprint(
                        f"⚠️  Required-member gate: still skipped after forced turn — "
                        f"pausing (never clean 'completed'). Missing: {_rm_missing}",
                        "[AI REQUESTS EXECUTE UNTIL COMPLETE] Required Member Gate",
                        color="yellow",
                    )
                    await exec_ctx.emitter.send_warning(
                        WarningPayload(
                            code="required_member_skipped",
                            system_message=(
                                f"Run pausing: required member(s) [{_rm_missing}] "
                                f"were never successfully called, even after the "
                                f"forced correction turn."
                            ),
                            user_message=(
                                "The orchestrator finished without consulting a "
                                "required team member, so this run is paused rather "
                                "than marked complete. You can reply to resume."
                            ),
                            level="medium",
                            recoverable=True,
                            metadata={
                                "missing_members": [
                                    {
                                        "agent_id": m.agent_id,
                                        "role_title": m.role_title,
                                        "projected_name": m.projected_name,
                                    }
                                    for m in _rm_report.missing
                                ],
                                "iteration": iteration,
                            },
                        )
                    )

                # Print accumulated usage for debugging
                vcprint(
                    current_request.usage_history,
                    "[AI REQUESTS EXECUTE UNTIL COMPLETE] Usage History",
                    color="magenta",
                    verbose=debug,
                )
                vcprint(
                    current_request.total_usage,
                    "[AI REQUESTS EXECUTE UNTIL COMPLETE] Total Usage",
                    color="green",
                    verbose=debug,
                )
                vcprint(
                    current_request.tool_call_stats,
                    "[AI REQUESTS EXECUTE UNTIL COMPLETE] Tool Call Stats",
                    color="blue",
                    verbose=debug,
                )

                # Build complete response and persist

                if debug:
                    vcprint(
                        response,
                        "[AI REQUESTS EXECUTE UNTIL COMPLETE] Response just before finalize and persist",
                        color="yellow",
                    )

                # Final UI clear — guarantees the frontend leaves any
                # "Planning next steps…" / in-progress indicator before we
                # persist and the stream closes.  Safe to double-emit: the
                # earlier site already emitted "complete" for the normal case,
                # but this covers any ordering race where a late mid-iteration
                # info update arrived after it.
                await exec_ctx.emitter.send_phase("complete")
                await exec_ctx.emitter.send_info(
                    InfoPayload(
                        code="iteration_done",
                        system_message="No more tool calls — exiting execution loop.",
                        user_message="",
                        metadata={
                            "iteration": iteration,
                            "will_continue": False,
                        },
                    )
                )

                _completion_meta: dict[str, Any] = {
                    "finish_reason": response.finish_reason,
                    "response_id": response.usage.response_id if response.usage else None,
                    "matrx_model_name": response.usage.matrx_model_name if response.usage else None,
                    "provider_model_name": response.usage.provider_model_name
                    if response.usage
                    else None,
                }
                # If this final, tool-less turn is the loop-guard's transparency
                # turn (tools were disabled after repeated failures), the run did
                # NOT complete its task — it paused for user review. Mark it
                # 'paused' (resumable) so it is never misrecorded as a clean
                # 'completed'. The model's explanation streamed normally.
                if state is not None and state.loop_guard_intervened:
                    _completion_meta["status"] = "paused_loop_guard"
                # Required-member terminal pause (C-26): the orchestrator still
                # refused its required member after the forced turn. A distinct,
                # resumable status — this run NEVER records a clean 'completed'.
                if _rm_action == "pause":
                    from matrx_ai.orchestrator.required_members import (
                        REQUIRED_MEMBER_SKIPPED_STATUS,
                    )

                    _completion_meta["status"] = REQUIRED_MEMBER_SKIPPED_STATUS
                    _completion_meta["required_members_missing"] = [
                        {"agent_id": m.agent_id, "role_title": m.role_title}
                        for m in (_rm_report.missing if _rm_report else [])
                    ]
                return await _finalize_and_persist(
                    current_request=current_request,
                    iteration=iteration,
                    final_response=response,
                    metadata=_completion_meta,
                    trigger_position=trigger_position,
                    pre_execution_message_count=pre_execution_message_count,
                    debug=debug,
                    state=state,
                )

            # Loop guard: tool_results were just executed and we're about to
            # loop back for another iteration. Evaluate health on the rolling
            # window of recent tool calls. The guard exists for SMALLER models —
            # a capable model self-corrects — but its real value is catching the
            # case the model can't: the TOOL ITSELF is broken, and the model
            # would otherwise burn tokens (and the user's money) retrying forever.
            #
            # We do NOT silently end the run. The sequence is:
            #   1. Approaching the ceiling → inject a one-time caution so the
            #      model can course-correct or wrap up while it still has tools.
            #   2. At the ceiling (verdict 'stuck') the FIRST time → DISABLE all
            #      tools, tell the model crystal-clearly that it failed N in a row
            #      and must now be transparent with the USER (what it tried, what
            #      broke, whether the tool looks broken), then loop back for ONE
            #      tool-less turn. The user can reply 'continue' / new guidance and
            #      /resume rebuilds the request with tools restored — a fresh start.
            #      The run finalizes as 'paused' (resumable), never a silent
            #      'completed'.
            #   3. If we already intervened and it's STILL stuck → hard graceful
            #      exit (belt-and-suspenders; normally unreachable since tools are
            #      gone on the tool-less turn).
            from matrx_ai.orchestrator.loop_guard import DEFAULT_FAILURE_THRESHOLD

            health = evaluate_loop_health(current_request.tool_call_history)

            if (
                health.verdict != "stuck"
                and not state.loop_guard_intervened
                and not state.loop_guard_warned
                and health.failures_in_window >= max(1, DEFAULT_FAILURE_THRESHOLD - 2)
            ):
                # Approaching the failure ceiling — caution the model once.
                state.loop_guard_warned = True
                from matrx_ai.config import TextContent, UnifiedMessage

                _remaining = max(1, DEFAULT_FAILURE_THRESHOLD - health.failures_in_window)
                _caution = (
                    f"⚠️ SYSTEM NOTICE (not from the user): {health.failures_in_window} of your "
                    f"last {health.window_size} tool calls have FAILED. If you reach "
                    f"{DEFAULT_FAILURE_THRESHOLD} failures, all tools will be disabled as a "
                    f"safety precaution and you'll have to explain the problem to the user. "
                    f"You have roughly {_remaining} attempt(s) left. Before trying again: "
                    f"re-read the exact error and the tool's input schema, and consider whether "
                    f"the tool itself may be broken/misconfigured rather than your arguments. "
                    f"If you can't make progress, stop and tell the user what's wrong now."
                )
                current_request.config.messages.append(
                    UnifiedMessage(role="user", content=[TextContent(text=_caution)])
                )
                await exec_ctx.emitter.send_warning(
                    WarningPayload(
                        code="loop_guard_approaching",
                        system_message=f"Loop guard approaching: {health.reason}",
                        user_message="",
                        level="low",
                        recoverable=True,
                        metadata={
                            "failures_in_window": health.failures_in_window,
                            "threshold": DEFAULT_FAILURE_THRESHOLD,
                            "iteration": iteration,
                        },
                    )
                )

            if health.verdict == "stuck" and not state.loop_guard_intervened:
                vcprint(
                    f"⚠️  Loop guard tripped — disabling tools for one transparent turn: "
                    f"{health.reason}",
                    "[AI REQUESTS EXECUTE UNTIL COMPLETE] Loop Guard",
                    color="yellow",
                )
                state.loop_guard_intervened = True
                # Hard precaution: strip every tool for the next turn so the model
                # CANNOT make another call even if it tries. Clearing the tool
                # lists is sufficient and provider-safe — every translator omits
                # the tools array (and its tool_choice) when there are no tools.
                # We deliberately do NOT set tool_choice='none' here: with an
                # empty tools array some providers/models treat an explicit
                # tool_choice inconsistently, and Anthropic already defaults to
                # 'none' when no tools are sent. Leaving it unset is the safe path.
                current_request.config.tools = []
                current_request.config.custom_tools = []

                from matrx_ai.config import TextContent, UnifiedMessage

                _directive = (
                    f"⚠️ SYSTEM NOTICE (not from the user): {health.failures_in_window} of your "
                    f"last {health.window_size} tool calls FAILED. As a safety precaution, ALL "
                    f"TOOLS HAVE BEEN DISABLED for your next response — you cannot and must not "
                    f"attempt any further tool calls right now.\n\n"
                    f"Stop retrying. Instead, write a clear, honest message directly to the user that:\n"
                    f"  • states plainly that you hit repeated tool errors and have paused;\n"
                    f"  • summarizes what you were trying to accomplish and the SPECIFIC errors "
                    f"you received;\n"
                    f"  • gives your best assessment of WHY — in particular, whether the tool "
                    f"itself appears to be broken or misconfigured (so a developer should look at "
                    f"it) versus something about this request that you could fix;\n"
                    f"  • tells the user they can reply 'continue' (or give new guidance) to resume "
                    f"with tools restored.\n\n"
                    f"Be direct and useful — this transparency is more valuable than another failed "
                    f"attempt."
                )
                current_request.config.messages.append(
                    UnifiedMessage(role="user", content=[TextContent(text=_directive)])
                )

                await exec_ctx.emitter.send_phase("processing")
                await exec_ctx.emitter.send_warning(
                    WarningPayload(
                        code="loop_guard_tools_disabled",
                        system_message=(
                            f"Loop guard tripped ({health.reason}). Tools disabled for one "
                            f"transparent turn; run will pause for user review."
                        ),
                        user_message=(
                            "The assistant hit repeated tool errors, so tools were paused for a "
                            "moment while it explains what happened. You can reply to continue."
                        ),
                        level="medium",
                        recoverable=True,
                        metadata={
                            "loop_health": {
                                "verdict": health.verdict,
                                "reason": health.reason,
                                "failures_in_window": health.failures_in_window,
                                "window_size": health.window_size,
                            },
                            "iteration": iteration,
                            "tools_disabled": True,
                        },
                    )
                )
                continue  # one more turn, tool-less — the model explains to the user

            if health.verdict == "stuck" and state.loop_guard_intervened:
                # Already gave the model its tool-less turn and it is somehow STILL
                # stuck. Exit gracefully for real now (resumable, marked 'paused').
                vcprint(
                    f"⚠️  Loop guard still stuck after intervention — graceful exit: "
                    f"{health.reason}",
                    "[AI REQUESTS EXECUTE UNTIL COMPLETE] Loop Guard",
                    color="yellow",
                )
                return await _exit_with_loop_guard(
                    exec_ctx=exec_ctx,
                    state=state,
                    current_request=current_request,
                    response=response,
                    health=health,
                    iteration=iteration,
                    trigger_position=trigger_position,
                    pre_execution_message_count=pre_execution_message_count,
                    debug=debug,
                    status="paused_loop_guard",
                    code="loop_guard_paused",
                    user_message=(
                        "I'm still hitting repeated tool errors and am pausing here so you can "
                        "review. Reply with 'continue' or new guidance to resume."
                    ),
                )

            # Continue - loop back for next iteration

        except PersistenceBarrierError:
            # A commit barrier failed — STOP EVERYTHING. DEGRADE first (data
            # before speed): synchronously flush the cache + drain any other
            # in-flight commits (captured to system_write_failure). Then let it
            # propagate to the streaming handler (fatal_error + system_error).
            # Do NOT route through the soft error-persist path below.
            await _degrade_and_secure(reason="barrier_failed")
            raise
        except Exception as e:
            # DEGRADE first — on ANY error the first priority is zero data loss,
            # not speed: synchronously flush + confirm everything cached / in
            # flight BEFORE persisting the error state or unwinding. (CLAUDE.md)
            await _degrade_and_secure(reason="iteration_error")
            # Ensure we close out the timing for this failed iteration
            if current_timing.end_time is None:
                current_timing.end_time = time.time()
                current_request.add_timing(current_timing)

            vcprint(
                f"\n✗ Error in iteration {iteration}: {str(e)}",
                "[AI REQUESTS EXECUTE UNTIL COMPLETE] Error in Iteration",
                color="red",
            )
            traceback.print_exc()

            # CRITICAL: Preserve all accumulated usage and data even on error
            # Print what we've collected so far
            if current_request.usage_history:
                vcprint(
                    current_request.usage_history,
                    "[AI REQUESTS EXECUTE UNTIL COMPLETE] Usage History (at error)",
                    color="magenta",
                    verbose=debug,
                )
                vcprint(
                    current_request.total_usage,
                    "[AI REQUESTS EXECUTE UNTIL COMPLETE] Total Usage (at error)",
                    color="yellow",
                    verbose=debug,
                )

            # Return a CompletedRequest with error information
            # This ensures the client never loses accumulated data
            error_response = await _finalize_and_persist(
                current_request=current_request,
                iteration=iteration,
                final_response=response if response else UnifiedResponse(messages=[]),
                metadata={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "error_iteration": iteration,
                    "status": "failed",
                },
                trigger_position=trigger_position,
                pre_execution_message_count=pre_execution_message_count,
                debug=debug,
                state=state,
            )

            vcprint(
                error_response,
                "[AI REQUESTS EXECUTE UNTIL COMPLETE] Error Response",
                color="yellow",
            )

            return error_response

    # Hit max iterations - still return accumulated data
    vcprint(
        f"\n⚠️  Max iterations reached ({max_iterations}) - returning accumulated data",
        "[AI REQUESTS EXECUTE UNTIL COMPLETE] Max Iterations Reached",
        color="yellow",
    )
    if current_request.usage_history:
        vcprint(
            current_request.usage_history,
            "[AI REQUESTS EXECUTE UNTIL COMPLETE] Usage History (max iterations)",
            color="magenta",
            verbose=debug,
        )
        vcprint(
            current_request.total_usage,
            "[AI REQUESTS EXECUTE UNTIL COMPLETE] Total Usage (max iterations)",
            color="yellow",
            verbose=debug,
        )

    # Use the same graceful exit as the loop guard so the FE sees a clean
    # complete-phase + warning instead of a silent stream end with orphaned
    # tool_use blocks. Health is evaluated for telemetry only — the verdict
    # is not what triggered this exit, the iteration cap was.
    health_for_metadata = evaluate_loop_health(current_request.tool_call_history)
    return await _exit_with_loop_guard(
        exec_ctx=exec_ctx,
        state=state,
        current_request=current_request,
        response=response if response is not None else UnifiedResponse(messages=[]),
        health=health_for_metadata,
        iteration=iteration,
        trigger_position=trigger_position,
        pre_execution_message_count=pre_execution_message_count,
        debug=debug,
        status="max_iterations_exceeded",
        code="max_iterations_exceeded",
        user_message=(
            f"Stopped after {max_iterations} iterations to avoid a runaway loop. "
            "Reply with 'continue' or new guidance to resume."
        ),
        extra_metadata={"max_iterations": max_iterations},
    )
