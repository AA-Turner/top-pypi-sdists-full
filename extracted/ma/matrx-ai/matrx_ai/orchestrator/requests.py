"""
Unified AI API System for OpenAI, Anthropic, and Google Gemini
Preserves ALL content types and metadata from all providers
"""

from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field, replace
from datetime import UTC, datetime
from typing import Any, ClassVar

from matrx_ai.config import (
    MessageList,
    ToolResultContent,
    UnifiedConfig,
    UnifiedMessage,
    UnifiedResponse,
)
from matrx_ai.config.usage_config import AggregatedUsage, TokenUsage
from matrx_ai.context.emitter_protocol import Emitter
from matrx_ai.orchestrator.tracking import TimingUsage

from .tracking import ToolCallUsage


def _usage_by_iteration(
    usage_history: list[TokenUsage],
    iterations: int,
) -> dict[int, list[TokenUsage]]:
    """Group provider-call usage under its logical loop iteration."""
    grouped: dict[int, list[TokenUsage]] = {i: [] for i in range(1, iterations + 1)}
    for index, usage in enumerate(usage_history):
        raw_iteration = usage.metadata.get("iteration")
        try:
            iteration = int(raw_iteration) if raw_iteration is not None else index + 1
        except (TypeError, ValueError):
            iteration = index + 1
        if 1 <= iteration <= iterations:
            grouped[iteration].append(usage)
    return grouped


# ============================================================================
# UNIFIED CLIENT
# ============================================================================


@dataclass
class AIMatrixRequest:
    conversation_id: str

    config: UnifiedConfig

    debug: bool | None = False

    request_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    created_by: str | None = None  # API key ID or session ID
    organization_id: str | None = None
    status: str | None = None

    # === USAGE TRACKING ===
    usage_history: list[TokenUsage] = field(default_factory=list)
    """Track usage from each API call in this request"""

    timing_history: list[TimingUsage] = field(default_factory=list)
    """Track timing from each step in this request"""

    tool_call_history: list[ToolCallUsage] = field(default_factory=list)
    """Track tool calls from each iteration in this request"""

    # === PARENT TRACKING ===
    parent_conversation_id: str | None = None

    # === EXTENSIBILITY ===
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.request_id is None:
            self.request_id = str(uuid.uuid4())

    @property
    def user_id(self) -> str:
        from matrx_ai.context.app_context import get_app_context

        return get_app_context().user_id

    @property
    def emitter(self) -> Emitter | None:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        return ctx.emitter if ctx else None

    @property
    def total_usage(self) -> AggregatedUsage:
        return TokenUsage.aggregate_by_model(self.usage_history)

    @property
    def timing_stats(self) -> dict[str, Any]:
        """Aggregate timing statistics for the request process."""
        return TimingUsage.aggregate(self.timing_history)

    @property
    def tool_call_stats(self) -> dict[str, Any]:
        """Aggregate tool call statistics for the request process."""
        return ToolCallUsage.aggregate(self.tool_call_history)

    def add_usage(self, usage: TokenUsage | None) -> None:
        """Add usage from an API response to the history."""
        if usage:
            self.usage_history.append(usage)

    def add_timing(self, timing: TimingUsage | None) -> None:
        """Add timing statistics to the history."""
        if timing:
            self.timing_history.append(timing)

    def add_tool_calls(self, tool_calls: ToolCallUsage | None) -> None:
        """Add tool call statistics to the history."""
        if tool_calls:
            self.tool_call_history.append(tool_calls)

    @classmethod
    def from_dict(cls, data: dict[str, Any], emitter: Emitter | None = None) -> AIMatrixRequest:
        """Create AIMatrixRequest from dictionary.

        The ``emitter`` parameter is accepted for backward compatibility
        but ignored; the emitter is read from ExecutionContext.
        """
        config_data = data.get("config", {})
        if isinstance(config_data, dict):
            config = UnifiedConfig.from_dict(config_data)
        else:
            config = config_data

        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        elif created_at is None:
            created_at = datetime.now(UTC)

        return cls(
            conversation_id=data.get("conversation_id", ""),
            config=config,
            debug=data.get("debug", False),
            request_id=data.get("request_id"),
            created_at=created_at,
            created_by=data.get("created_by"),
            organization_id=data.get("organization_id"),
            status=data.get("status"),
            metadata=data.get("metadata", {}),
        )

    @classmethod
    def add_response(
        cls,
        original_request: AIMatrixRequest,
        response: UnifiedResponse,
        tool_results: list[ToolResultContent] | None = None,
    ) -> AIMatrixRequest:
        """Add response (and optionally tool results) to the conversation history.

        This is used both when continuing with tool results and when finishing
        without tool results.
        """
        messages = response.messages
        if isinstance(response.messages, UnifiedMessage):
            messages = [messages]
            print("Converted UnifiedMessage to list of messages")

        # Create new MessageList with extended messages
        updated_messages = MessageList(
            _messages=[
                *original_request.config.messages.to_list(),
                *messages,
            ]
        )

        if tool_results:
            # Use role='tool' to distinguish from actual user messages
            updated_messages.append(UnifiedMessage(role="tool", content=tool_results))

        # Create new request with updated messages (everything else stays the same)
        new_config = replace(original_request.config, messages=updated_messages)
        return replace(original_request, config=new_config)

    def to_dict(self) -> dict[str, Any]:
        return {
            "conversation_id": self.conversation_id,
            "user_id": self.user_id,
            # "ai_model_id": self.ai_model_id,
            "debug": self.debug,
            "config": self.config.to_dict(),
            "request_id": self.request_id,
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
            "status": self.status,
            "metadata": self.metadata,
        }


@dataclass
class CompletedRequest:
    """
    Represents a completed AI request with all accumulated responses and usage.

    Designed for easy client-side continuation:
    - Simply add a new message to `request.config.messages`
    - Call the API again with the updated `request`
    - All conversation history and usage is automatically tracked

    No duplication - all messages are in `request.config.messages`
    """

    request: AIMatrixRequest
    """Complete request with full conversation history - ready for next call"""

    iterations: int
    """Number of API calls made"""

    final_response: UnifiedResponse
    """The final API response that completed execution"""

    total_usage: AggregatedUsage = field(default_factory=AggregatedUsage)
    """Complete usage breakdown with individual calls by model and totals"""

    timing_stats: dict[str, Any] = field(default_factory=dict)
    """Complete timing breakdown including total duration, API time, and tool time"""

    tool_call_stats: dict[str, Any] = field(default_factory=dict)
    """Complete tool call breakdown including total calls, by tool name, and success/error counts"""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Additional metadata (finish_reason, timestamps, etc.)"""

    # IN-MEMORY ONLY message-position plumbing for this execution. These drive
    # the per-turn message-write window in persist_completed_request and the
    # in-memory committed_position high-water-mark. They are NO LONGER persisted
    # to cx_user_request (those columns were dropped — see the request↔
    # conversation decoupling; a request spans many conversations now, so a
    # single message-position triple on the request row is meaningless).
    trigger_message_position: int | None = None
    """Position of the user message that triggered this execution"""

    result_start_position: int | None = None
    """First message position produced by this execution"""

    result_end_position: int | None = None
    """Last message position produced by this execution"""

    # Convenience properties for easy access to key info
    @property
    def conversation_id(self) -> str:
        """Quick access to conversation ID"""
        return self.request.conversation_id

    @property
    def user_id(self) -> str:
        """Quick access to user ID"""
        return self.request.user_id

    @property
    def messages(self) -> MessageList:
        """Quick access to all messages in conversation"""
        return self.request.config.messages

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary, excluding non-serializable fields like emitter"""
        return {
            "request": self.request.to_dict(),  # Uses AIMatrixRequest.to_dict() which excludes emitter
            "iterations": self.iterations,
            "final_response": self.final_response.to_dict()
            if hasattr(self.final_response, "to_dict")
            else {},
            "total_usage": self.total_usage.to_dict(),
            "timing_stats": self.timing_stats,
            "tool_call_stats": self.tool_call_stats,
            "metadata": self.metadata,
        }

    # Orchestrator status strings that mean "the run has a valid final assistant turn
    # and is RESUMABLE (waiting on the client/user), NOT an error and NOT done." Shared
    # by cx (→ "paused") and the spine (→ WAITING_INPUT). One list, one meaning.
    RESUMABLE_SUSPEND_STATUSES: ClassVar[tuple[str, ...]] = (
        "suspended_awaiting_client",
        "suspended_provider_overload",
        "paused_loop_guard",
        "max_iterations_exceeded",
        # A Cloud Browser human-handoff parks the run at WAITING_INPUT while a
        # person acts at the panel (WS-6 / browser_handoff.SUSPEND_REASON). It is
        # a client-delegated suspend whose "client" is a human — RESUMABLE, never
        # a terminal, and NOT paused (so the integrity watchdog never alarms on a
        # legitimate multi-minute-to-week wait). Kept in lockstep with
        # matrx_ai.browser_handoff.models.SUSPEND_REASON.
        "suspended_awaiting_human_browser",
        # The model hit its output-token limit mid-response (executor.py's
        # finish_action == "truncated" exit). The partial text was delivered
        # and persisted, so the run is limit-hit + RESUMABLE — never a clean
        # "completed" (it previously fell to the else branch and recorded a
        # real limit-hit as a success). Its structured error detail
        # (metadata["error"] + error_type="truncated_response") is carried
        # onto the summary below.
        "truncated",
    )

    def _structured_error(self) -> dict[str, Any] | Any | None:
        """The completion's error payload, normalized toward the structured-error
        shape. A dict passes through verbatim; a bare-string error with a sibling
        metadata["error_type"] (the "truncated" exit's shape) is lifted into
        {"error_type", "message"} so the type isn't dropped; a bare string with
        no type stays a string (legacy behavior). None when no error."""
        err = self.metadata.get("error")
        if err is None:
            return None
        if isinstance(err, dict):
            return err
        error_type = self.metadata.get("error_type")
        if error_type:
            return {"error_type": str(error_type), "message": str(err)}
        return err

    def build_request_summary(self) -> dict[str, Any]:
        """The aggregated per-request summary — the cx_user_request row shape AND the
        runtime spine's `request_summary` NOTE, from ONE builder so the two never drift
        while both are written in parallel (cx_user_request is being retired onto the
        spine). Pure aggregation over this CompletedRequest; no I/O, no context."""
        usage_total = self.total_usage.total
        timing_agg = self.timing_stats
        tool_stats = self.tool_call_stats

        # Total cost = sum of the per-iteration rounded costs (matches the cx_request
        # rows exactly, so the parent total reconciles against its children).
        total_cost = 0.0
        usage_by_iteration = _usage_by_iteration(
            self.request.usage_history,
            self.iterations,
        )
        has_unknown_cost = any(not calls for calls in usage_by_iteration.values())
        for u in self.request.usage_history:
            try:
                c = u.calculate_cost()
            except Exception:  # noqa: BLE001 — one unpriceable call must not kill the summary
                c = None
            if c is not None:
                total_cost += round(c, 6)
            else:
                has_unknown_cost = True

        user_request: dict[str, Any] = {
            "request_id": self.request.request_id,
            "conversation_id": self.request.conversation_id,
            "created_by": self.request.user_id,
            "total_input_tokens": usage_total.input_tokens,
            "total_output_tokens": usage_total.output_tokens,
            "total_cached_tokens": usage_total.cached_input_tokens,
            "total_tokens": usage_total.total_tokens,
            "total_cost": None if has_unknown_cost else round(total_cost, 6),
            "iterations": self.iterations,
            "total_tool_calls": tool_stats.get("total_tool_calls", 0),
            "finish_reason": str(self.metadata["finish_reason"])
            if self.metadata.get("finish_reason") is not None
            else None,
        }

        # Aggregated timing
        if timing_agg:
            api_dur = timing_agg.get("api_duration")
            tool_dur = timing_agg.get("tool_duration")
            total_dur = timing_agg.get("total_duration")
            if api_dur is not None:
                user_request["api_duration_ms"] = int(api_dur * 1000)
            if tool_dur is not None:
                user_request["tool_duration_ms"] = int(tool_dur * 1000)
            if total_dur is not None:
                user_request["total_duration_ms"] = int(total_dur * 1000)

        # Status from metadata → cx_user_request.status (processing-outcome enum:
        # pending|processing|completed|failed|cancelled|abandoned|paused).
        #   - "failed"                   → "failed" (a real error; carries .error)
        #   - a RESUMABLE_SUSPEND_STATUS → "paused" (delegated client-tool suspend,
        #     provider-overload wait, loop-guard, or iteration cap — a valid final
        #     assistant turn, resumable by client/user action, possibly weeks later)
        #   - "cancelled"                 → "cancelled" (explicit user/server
        #     cancellation at a safe boundary)
        #   - anything else / unset      → "completed"
        # Previously the suspend / guard outcomes were coerced to "completed", which
        # made a run WAITING ON THE CLIENT indistinguishable from a done one — the
        # silent-completion bug that left delegated tool calls orphaned. The precise
        # reason is preserved verbatim in metadata["status"] for analytics.
        status = self.metadata.get("status")
        if status == "failed":
            user_request["status"] = "failed"
            user_request["error"] = self._structured_error()
        elif status in self.RESUMABLE_SUSPEND_STATUSES:
            user_request["status"] = "paused"
            # A paused run may still carry error detail (e.g. "truncated" sets
            # metadata error + error_type="truncated_response"). Preserve it —
            # a limit-hit is resumable but NOT clean, and dropping the payload
            # here would erase the only structured record of why it paused.
            err = self._structured_error()
            if err is not None:
                user_request["error"] = err
        elif status == "cancelled":
            user_request["status"] = "cancelled"
        else:
            user_request["status"] = "completed"

        # Caller-supplied metadata from the request is the base layer.
        # System-generated fields (response_id, usage_by_model) are merged on top
        # so they are always present regardless of what the caller provided.
        request_metadata: dict[str, Any] = dict(self.request.metadata)
        if has_unknown_cost:
            request_metadata["cost_reconciliation"] = "incomplete_child_costs"
            request_metadata["known_cost_subtotal"] = round(total_cost, 6)
        if self.metadata.get("response_id"):
            request_metadata["response_id"] = self.metadata["response_id"]
        if self.total_usage.by_model:
            request_metadata["usage_by_model"] = {
                k: asdict(v) for k, v in self.total_usage.by_model.items()
            }
        user_request["metadata"] = request_metadata
        return user_request

    def to_storage_dict(self) -> dict[str, Any]:
        """Serialize to the cx_ v2 storage format for database persistence.

        Returns dict with:
            - conversation: dict matching cx_conversation columns
            - messages: list[dict] matching cx_message rows
            - user_request: dict matching cx_user_request row (aggregated parent)
            - requests: list[dict] matching cx_request rows (one per iteration)
        """
        config = self.request.config
        config_storage = config.to_storage_dict()
        # vcprint(config_storage, "[CompletedRequest] Config Storage", color="yellow")

        # --- cx_conversation row ---
        conversation = {
            "created_by": self.request.user_id,
            "ai_model": config_storage["model"],
            "system_instruction": config_storage["system_instruction"],
            "config": config_storage["config"],
            "message_count": len(config_storage["messages"]),
            "parent_conversation_id": self.request.parent_conversation_id,
        }

        # --- cx_message rows (with position and status) ---
        messages = []
        for position, msg_dict in enumerate(config_storage["messages"]):
            msg_row: dict[str, Any] = {
                "role": msg_dict["role"],
                "position": position,
                "content": msg_dict["content"],
            }
            # Carry message-level metadata through. Without this the per-turn
            # call-record stamp (model_context / tools_on_call, plus any other
            # cx_message.metadata) is silently dropped before the persist layer —
            # the bug that left metadata.context_manifest empty for its whole life.
            if msg_dict.get("metadata"):
                msg_row["metadata"] = msg_dict["metadata"]
            # Existing DB id (present for messages loaded from the conversation,
            # e.g. on a retry). Persistence uses it to skip re-INSERTing a
            # message that already exists.
            if msg_dict.get("id"):
                msg_row["id"] = msg_dict["id"]
            msg_status = msg_dict.get("status")
            if msg_status and msg_status != "active":
                msg_row["status"] = msg_status
            messages.append(msg_row)

        # --- cx_request rows (one per iteration) ---
        # Retries can produce several paid calls in one logical iteration.
        usage_by_iteration = _usage_by_iteration(
            self.request.usage_history,
            self.iterations,
        )
        timing_list = self.request.timing_history

        # Index tool_call_history by iteration number for quick lookup
        tool_calls_by_iter: dict[int, ToolCallUsage] = {}
        for tc in self.request.tool_call_history:
            tool_calls_by_iter[tc.iteration] = tc

        # Phase 1d: ConversationResolver stashes the TrimReport on AppContext
        # before the orchestrator runs. We attach the report to iteration 1's
        # cx_request row (the only one the trim could have affected — later
        # iterations see the already-trimmed messages). Read once outside the
        # loop; only iteration 0 actually consumes it.
        _trim_summary: dict[str, Any] | None = None
        try:
            from matrx_ai.context.app_context import try_get_app_context

            _ctx = try_get_app_context()
            if _ctx is not None:
                _trim_summary = _ctx.metadata.get("last_trim_report")
        except Exception:
            _trim_summary = None

        request_rows: list[dict[str, Any]] = []
        for i in range(self.iterations):
            row: dict[str, Any] = {"iteration": i + 1}
            if i == 0 and _trim_summary is not None:
                row["trim_summary"] = _trim_summary

            # One cx_request row represents the logical iteration, while the
            # attempt list preserves every paid provider call made by retries.
            iteration_usages = usage_by_iteration[i + 1]
            if iteration_usages:
                u = iteration_usages[-1]
                row["ai_model"] = u.matrx_model_name
                row["provider"] = u.api
                row["input_tokens"] = sum(item.input_tokens for item in iteration_usages)
                row["output_tokens"] = sum(item.output_tokens for item in iteration_usages)
                row["cached_tokens"] = sum(
                    item.cached_input_tokens for item in iteration_usages
                )
                row["total_tokens"] = sum(item.total_tokens for item in iteration_usages)
                row["response_id"] = u.response_id or None
                # Verbatim provider usage block preserved for cx_request.raw_usage
                # (Phase 1c). Recovers cache_creation_input_tokens,
                # service_tier, reasoning_tokens, etc.
                raw_attempts = [
                    item.raw_usage for item in iteration_usages if item.raw_usage
                ]
                if len(iteration_usages) == 1 and raw_attempts:
                    row["raw_usage"] = raw_attempts[0]
                elif raw_attempts:
                    row["raw_usage"] = {"provider_attempts": raw_attempts}
                # The EXACT call that served this iteration — ai.offering uuid +
                # how it was chosen (pinned | preferred | sibling_fallback).
                # Stamped by UnifiedAIClient._stamp_offering_usage; lands in
                # cx_request.metadata (structured note, no schema change).
                if u.offering_id:
                    row["metadata"] = {
                        "offering_id": u.offering_id,
                        "offering_route": u.offering_route or "preferred",
                    }
                attempt_costs = [item.calculate_cost() for item in iteration_usages]
                if all(cost is not None for cost in attempt_costs):
                    row["cost"] = round(
                        sum(round(cost, 6) for cost in attempt_costs if cost is not None),
                        6,
                    )
                catalog_costs = [
                    item.calculate_catalog_cost() for item in iteration_usages
                ]
                catalog_cost = (
                    sum(round(cost, 6) for cost in catalog_costs if cost is not None)
                    if all(cost is not None for cost in catalog_costs)
                    else None
                )
                provider_costs = [
                    item.provider_charge.authoritative_usd
                    for item in iteration_usages
                    if item.provider_charge is not None
                    and item.provider_charge.authoritative_usd is not None
                ]
                authoritative_provider_cost = (
                    sum(provider_costs)
                    if len(provider_costs) == len(iteration_usages)
                    else None
                )
                if authoritative_provider_cost is not None:
                    serialized_charges = [
                        asdict(item.provider_charge)
                        for item in iteration_usages
                        if item.provider_charge is not None
                    ]
                    row.setdefault("metadata", {}).update(
                        {
                            # The row's ``cost`` is ALWAYS our catalog result.
                            # Provider dollars are comparison evidence only.
                            "cost_source": "catalog_from_provider_usage",
                            "provider_charge_available": True,
                            "provider_charge_usd": authoritative_provider_cost,
                            "provider_charges": serialized_charges,
                            "catalog_cost_usd": (
                                round(catalog_cost, 6) if catalog_cost is not None else None
                            ),
                            "provider_catalog_variance_usd": (
                                round(authoritative_provider_cost - catalog_cost, 6)
                                if catalog_cost is not None
                                else None
                            ),
                        }
                    )
                    if len(serialized_charges) == 1:
                        row["metadata"]["provider_charge"] = serialized_charges[0]
                elif catalog_cost is not None:
                    row.setdefault("metadata", {}).update(
                        {
                            "cost_source": "catalog_from_provider_usage",
                            "catalog_cost_usd": round(catalog_cost, 6),
                        }
                    )
                if len(iteration_usages) > 1:
                    row.setdefault("metadata", {})["provider_attempts"] = [
                        {
                            "attempt": item.metadata.get("provider_attempt", attempt_index),
                            "outcome": item.metadata.get("attempt_outcome"),
                            "model": item.matrx_model_name,
                            "provider_model": item.provider_model_name,
                            "provider": item.api,
                            "offering_id": item.offering_id or None,
                            "input_tokens": item.input_tokens,
                            "output_tokens": item.output_tokens,
                            "cached_tokens": item.cached_input_tokens,
                            "catalog_cost_usd": (
                                round(attempt_costs[attempt_index - 1], 6)
                                if attempt_costs[attempt_index - 1] is not None
                                else None
                            ),
                        }
                        for attempt_index, item in enumerate(iteration_usages, start=1)
                    ]
                pricing_snapshots = [
                    item.metadata.get("pricing_snapshot")
                    for item in iteration_usages
                    if item.metadata.get("pricing_snapshot")
                ]
                if pricing_snapshots:
                    row.setdefault("metadata", {})["pricing_snapshots"] = pricing_snapshots
                    if len(pricing_snapshots) == 1:
                        row["metadata"]["pricing_snapshot"] = pricing_snapshots[0]
                response_message_id = u.metadata.get("response_message_id")
                if response_message_id:
                    row.setdefault("metadata", {})["response_message_id"] = response_message_id
                billing_components: dict[str, int] = {}
                for item in iteration_usages:
                    for name, count in item.billing_components.items():
                        billing_components[name] = billing_components.get(name, 0) + count
                if billing_components:
                    row.setdefault("metadata", {})["billing_components"] = billing_components
                reconciliations = [
                    item.metadata.get("cost_reconciliation")
                    for item in iteration_usages
                    if item.metadata.get("cost_reconciliation")
                ]
                if reconciliations:
                    row.setdefault("metadata", {})["cost_reconciliation"] = (
                        reconciliations[0]
                        if len(reconciliations) == 1
                        else reconciliations
                    )

            # Timing for this iteration
            if i < len(timing_list):
                t = timing_list[i]
                row["api_duration_ms"] = int(t.api_call_duration * 1000)
                row["tool_duration_ms"] = int(t.tool_execution_duration * 1000)
                row["total_duration_ms"] = int(t.total_duration * 1000)

            # Tool calls for this iteration (iteration is 1-based)
            tc_entry = tool_calls_by_iter.get(i + 1)
            if tc_entry:
                row["tool_calls_count"] = tc_entry.tool_calls_count
                row["tool_calls_details"] = tc_entry.tool_calls_details
            else:
                row["tool_calls_count"] = 0

            # Finish reason only on last iteration
            if i == self.iterations - 1:
                fr = self.metadata.get("finish_reason")
                row["finish_reason"] = str(fr) if fr is not None else None

            request_rows.append(row)

        # --- cx_user_request row (aggregated parent) ---
        # ONE source of truth for the aggregated request-summary shape, shared with
        # the runtime spine (aidream/services/runtime/conversation.py records the SAME
        # dict as a `request_summary` NOTE + meters). cx_user_request is being retired
        # onto the spine — the summary must be identical on both sides during the
        # parallel-run window, so both read this method, never a divergent copy.
        user_request = self.build_request_summary()

        return {
            "conversation": conversation,
            "messages": messages,
            "user_request": user_request,
            "requests": request_rows,
        }
