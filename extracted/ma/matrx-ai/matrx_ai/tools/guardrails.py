from __future__ import annotations

import hashlib
import json
import logging
import time
from collections import defaultdict
from dataclasses import dataclass

from matrx_ai.tools.models import GuardrailResult, ToolContext, ToolDefinition, ToolType

logger = logging.getLogger(__name__)

# Type alias for a tool call coming from unified config
ToolCallLike = dict  # Must have "name" and "arguments" keys at minimum


@dataclass
class _CallRecord:
    tool_name: str
    args_hash: str
    timestamp: float
    iteration: int


class GuardrailEngine:
    """Centralized guardrails that run before every tool execution.

    Checks:
      1. Duplicate detection — identical call within recent history
      2. Rate limiting — max calls per minute per tool
      3. Conversation limit — max total calls per tool per conversation
      4. Cost budget — remaining budget vs estimated cost
      5. Loop detection — same tool called with similar args repeatedly
      6. Recursion depth — prevent runaway agent-in-agent chains
    """

    def __init__(self) -> None:
        # conversation_id → list[_CallRecord]
        self._history: dict[str, list[_CallRecord]] = defaultdict(list)

    async def check(
        self,
        tool_name: str,
        arguments: dict,
        ctx: ToolContext,
        tool_def: ToolDefinition,
    ) -> GuardrailResult:
        checks = [
            self._check_duplicate(tool_name, arguments, ctx, tool_def),
            self._check_rate_limit(tool_name, ctx, tool_def),
            self._check_conversation_limit(tool_name, ctx, tool_def),
            self._check_cost_budget(ctx, tool_def),
            self._check_loop_detection(tool_name, arguments, ctx, tool_def),
            self._check_recursion_depth(ctx, tool_def),
        ]
        for check in checks:
            if check.blocked:
                return check
        return GuardrailResult(blocked=False)

    def record_call(self, tool_name: str, arguments: dict, ctx: ToolContext) -> None:
        self._history[ctx.conversation_id].append(
            _CallRecord(
                tool_name=tool_name,
                args_hash=self._hash_args(arguments),
                timestamp=time.time(),
                iteration=ctx.iteration,
            )
        )

    def clear_conversation(self, conversation_id: str) -> None:
        self._history.pop(conversation_id, None)

    # ------------------------------------------------------------------
    # Individual checks
    # ------------------------------------------------------------------

    # Number of back-to-back identical calls required to block.
    # Args-bearing calls block on the 3rd (triplicate); empty-args calls get extra
    # leniency since they are inherently more likely to repeat legitimately.
    _DUPLICATE_THRESHOLD = 3
    _DUPLICATE_THRESHOLD_NO_ARGS = 5

    def _check_duplicate(
        self,
        tool_name: str,
        arguments: dict,
        ctx: ToolContext,
        tool_def: ToolDefinition,
    ) -> GuardrailResult:
        if tool_def.dedupe_exempt:
            return GuardrailResult(blocked=False)

        records = self._history.get(ctx.conversation_id, [])
        current_hash = self._hash_args(arguments)

        is_no_args = not arguments
        threshold = self._DUPLICATE_THRESHOLD_NO_ARGS if is_no_args else self._DUPLICATE_THRESHOLD

        consecutive = 0
        for rec in reversed(records):
            if rec.tool_name == tool_name and rec.args_hash == current_hash:
                consecutive += 1
            else:
                break

        if consecutive >= threshold - 1:
            total = consecutive + 1
            if is_no_args:
                reason = (
                    f"'{tool_name}' has been called {total} times in a row with no arguments. "
                    f"This appears to be a stuck loop."
                )
            else:
                reason = (
                    f"Triplicate call to '{tool_name}' — identical arguments seen "
                    f"{total} times in a row."
                )
            return GuardrailResult(
                blocked=True,
                reason=reason,
                error_type="duplicate",
                suggested_action="Use different parameters or try a different approach.",
            )
        return GuardrailResult(blocked=False)

    def _check_rate_limit(
        self,
        tool_name: str,
        ctx: ToolContext,
        tool_def: ToolDefinition,
    ) -> GuardrailResult:
        if tool_def.max_calls_per_minute is None:
            return GuardrailResult(blocked=False)

        window_start = time.time() - 60
        records = self._history.get(ctx.conversation_id, [])
        recent = [r for r in records if r.tool_name == tool_name and r.timestamp >= window_start]

        if len(recent) >= tool_def.max_calls_per_minute:
            return GuardrailResult(
                blocked=True,
                reason=f"Rate limit exceeded: '{tool_name}' called {len(recent)} times in the last minute (max {tool_def.max_calls_per_minute}).",
                error_type="rate_limit",
                suggested_action="Wait before calling this tool again, or use a different approach.",
            )
        return GuardrailResult(blocked=False)

    def _check_conversation_limit(
        self,
        tool_name: str,
        ctx: ToolContext,
        tool_def: ToolDefinition,
    ) -> GuardrailResult:
        if tool_def.max_calls_per_conversation is None:
            return GuardrailResult(blocked=False)

        records = self._history.get(ctx.conversation_id, [])
        total = sum(1 for r in records if r.tool_name == tool_name)

        if total >= tool_def.max_calls_per_conversation:
            return GuardrailResult(
                blocked=True,
                reason=f"Conversation limit reached: '{tool_name}' already called {total} times (max {tool_def.max_calls_per_conversation}).",
                error_type="conversation_limit",
                suggested_action="You have used this tool the maximum number of times in this conversation. Try a different approach.",
            )
        return GuardrailResult(blocked=False)

    def _check_cost_budget(
        self,
        ctx: ToolContext,
        tool_def: ToolDefinition,
    ) -> GuardrailResult:
        # Tree-wide dollar budget: cost_budget_remaining is the dollars left for
        # this user request's WHOLE tree (parent + every sub-agent share the
        # request_id). None == no budget applies — never treated as exhausted.
        if ctx.cost_budget_remaining is not None and ctx.cost_budget_remaining <= 0:
            self._log_budget_block(
                tool_def.name,
                ctx,
                f"tree dollar budget EXHAUSTED (${ctx.cost_budget_remaining:.4f} remaining)",
            )
            return GuardrailResult(
                blocked=True,
                reason=(
                    "Tree-wide cost budget exhausted for this request — the total "
                    "spend across this run and every sub-agent it spawned has hit "
                    "the ceiling. No further tools (including new agent spawns) can run."
                ),
                error_type="cost_budget",
                suggested_action="Stop spawning work and inform the user that the cost budget for this request has been reached.",
            )

        if tool_def.cost_cap_per_call is not None:
            if (
                ctx.cost_budget_remaining is not None
                and tool_def.cost_cap_per_call > ctx.cost_budget_remaining
            ):
                self._log_budget_block(
                    tool_def.name,
                    ctx,
                    f"est. ${tool_def.cost_cap_per_call:.2f} > ${ctx.cost_budget_remaining:.4f} remaining",
                )
                return GuardrailResult(
                    blocked=True,
                    reason=(
                        f"Estimated cost for '{tool_def.name}' (${tool_def.cost_cap_per_call:.2f}) "
                        f"exceeds the remaining tree-wide budget for this request (${ctx.cost_budget_remaining:.2f})."
                    ),
                    error_type="cost_budget",
                    suggested_action="Use a less expensive tool or inform the user.",
                )
        return GuardrailResult(blocked=False)

    @staticmethod
    def _log_budget_block(tool_name: str, ctx: ToolContext, detail: str) -> None:
        # A money guardrail must never trip silently — a blocked spend is a loud,
        # self-identifying banner (the tool also returns an error to the model,
        # streams an error to the FE, and persists a failed cx_tool_call row).
        try:
            from matrx_utils import vcprint

            vcprint(
                f"\n🛑 [TREE COST BUDGET] Blocked '{tool_name}' — {detail}. "
                f"(request_id={ctx.request_id}, conversation_id={ctx.conversation_id}, "
                f"recursion_depth={ctx.recursion_depth}). Tune the ceiling at "
                f"matrx_ai.orchestrator.cost_budget.TREE_COST_CEILING_USD.\n",
                color="red",
                log_level="warning",
            )
        except Exception:
            logger.warning("[TREE COST BUDGET] Blocked '%s' — %s", tool_name, detail)

    def _check_loop_detection(
        self,
        tool_name: str,
        arguments: dict,
        ctx: ToolContext,
        tool_def: ToolDefinition,
    ) -> GuardrailResult:
        # dedupe_exempt declares "identical repeated calls are this tool's
        # INTENDED use" (status pollers like agent_plan/workflow_run). The
        # duplicate check already honors it; loop detection must too — a
        # legitimate poller trips the similarity check by design, and the
        # 2026-07-07 agent-plan run showed the block landing on the exact
        # poll that would have returned the finished results (the model then
        # burned tokens on filler calls to dodge the guard). Cost/rate/
        # conversation-limit guards still apply to exempt tools.
        if tool_def.dedupe_exempt:
            return GuardrailResult(blocked=False)

        # Threshold of 5 (not 3): real workflows commonly call the same
        # introspection tool a handful of times — read_page after each
        # navigation, computer.action='screenshot' between steps, etc.
        # Trip at 3 produced false positives in mixed-tool sessions where
        # the agent was doing useful work and not actually looping.
        #
        # Distinct from _check_duplicate: that guard trips on CONSECUTIVE
        # identical calls (threshold 3); this one trips on identical calls
        # scattered across the tool's recent window (A,B,A,B,A,B… — the
        # fillers reset the consecutive counter but not this one). Matching
        # is EXACT args (md5 of the sorted-key JSON dump): md5 avalanche
        # makes any non-identical args share only ~1/16 of hex chars, so the
        # old ">0.8 similarity" was always exactly equality — this is honest
        # naming, same behavior. True fuzzy matching would need the raw arg
        # strings and would false-positive on legit paginating tools (a
        # changing cursor each call), so it's deliberately not attempted.
        loop_threshold = 5
        recency_window = 10

        # Per-tool window: this tool's last `recency_window` calls, NOT its
        # calls within the global last-N records. Otherwise a burst of
        # exempt-tool polls (still recorded for rate/cost limits) evicts an
        # unrelated tool's calls from the global window and silently blinds
        # loop detection for it.
        #
        # Side effect (intended): this also TIGHTENS detection for the tool
        # itself — identical calls spread across a long interleaved session now
        # persist in the window instead of aging out of the global last-N.
        # Correct for a stateless idempotent tool (5 identical calls = a real
        # loop). A tool over external MUTABLE state whose identical-args calls
        # return DIFFERENT results (a status poller) must be dedupe_exempt —
        # that flag is exactly its intended use, and it short-circuits above.
        records = self._history.get(ctx.conversation_id, [])
        recent_same = [r for r in records if r.tool_name == tool_name][-recency_window:]

        if len(recent_same) < loop_threshold:
            return GuardrailResult(blocked=False)

        current_hash = self._hash_args(arguments)
        identical_count = sum(1 for r in recent_same if r.args_hash == current_hash)

        if identical_count >= loop_threshold:
            from matrx_ai.tools._debug_log import log_event as _debug_log

            _debug_log(
                "LOOP_BLOCK",
                tool=tool_name,
                count=identical_count,
                threshold=loop_threshold,
                conv=ctx.conversation_id,
            )
            return GuardrailResult(
                blocked=True,
                reason=(
                    f"Loop detected: '{tool_name}' has been called {identical_count} times recently "
                    f"with identical arguments. This appears to be a loop."
                ),
                error_type="loop_detected",
                suggested_action=(
                    "You seem to be calling this tool repeatedly with similar parameters. "
                    "Please try a fundamentally different approach or provide a final answer."
                ),
            )
        return GuardrailResult(blocked=False)

    def _check_recursion_depth(
        self,
        ctx: ToolContext,
        tool_def: ToolDefinition,
    ) -> GuardrailResult:
        if tool_def.tool_type == ToolType.AGENT:
            max_depth = tool_def.max_recursion_depth
            if ctx.recursion_depth >= max_depth:
                return GuardrailResult(
                    blocked=True,
                    reason=(
                        f"Maximum agent recursion depth ({max_depth}) reached. "
                        f"Current depth: {ctx.recursion_depth}."
                    ),
                    error_type="recursion_depth",
                    suggested_action="Agent tools cannot spawn further agent tools at this depth. Use direct tools instead.",
                )
        return GuardrailResult(blocked=False)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _hash_args(arguments: dict) -> str:
        normalized = json.dumps(arguments, sort_keys=True, default=str)
        return hashlib.md5(normalized.encode()).hexdigest()
