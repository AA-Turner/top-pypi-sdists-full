"""Finalize-Only Mode — escape hatch that always reaches a terminal state.

When the optimizer can no longer safely retry (compaction loop, pre_retry
budget exhausted, token starvation) or when the completion-evidence
detector has determined the durable work is already done but the agent
is going to restart anyway, we enter Finalize-Only Mode.

In this mode the agno tool gate accepts only a small allowed-list of
tools (see :class:`FinalizeOnlyState.allowed_tools`). Everything else
returns a synthetic short-circuit result: it points at ``xpfinalize_task``
when that tool is registered for the run (finalize was already active at
run start), and otherwise asks for a plain-text final answer — the tool is
deliberately absent from a normal run's tool map so the model cannot call
it spontaneously.

Putting this in its own module keeps the orchestration logic out of the
already-large ``context_optimizer.py`` and out of the agno hook in
``frameworks/agno.py``. Both call into the helpers here.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Union

from loguru import logger

from xpander_sdk.core.context_optimizer.action_ledger import get_attached_ledger
from xpander_sdk.utils.json_parsing import parse_structured_string

from xpander_sdk.models.action_ledger import (
    EvidenceReport,
    FinalizeOnlyState,
)

# Mirrors the literal union on ``FinalizeOnlyState.reason`` so type
# checkers reject unknown reasons at the call site instead of suppressing
# the mismatch with ``# type: ignore`` and exploding at model
# construction on the very escape-hatch path that's supposed to be
# safest. Add new literals here AND in ``models/action_ledger.py``.
FinalizeReason = Literal[
    "evidence",
    "compact_loop",
    "pre_retry_exhausted",
    "token_floor",
    "stagnant_compactions",
    "repeated_tool_call",
    "error_streak",
    "tool_overuse",
    "plan_churn",
    "no_progress",
]

# System-prompt override appended to the agent's instructions while
# Finalize-Only is active. Reads off ``<authoritative_ledger>`` from the
# resumption message — that block is rendered by ``ActionLedger`` and
# already contains every WRITE/VERIFY entry the agent needs.
FINALIZE_ONLY_SYSTEM_OVERRIDE = """
<finalize_only_mode>
The system determined this task must finalize NOW (context budget exhausted, a
compaction loop detected, or durable evidence the work is already done).
- The ONLY mutation tool you may call is `xpfinalize_task`. Every other mutation
  tool (writes, exec, HTTP POST, etc.) is rejected with a synthetic error — do not retry it.
- Read-only escape hatch: you MAY call `xpget_agent_plan`,
  `xpworkspace-context-retrieve`, or `xpworkspace-file-read` to look up a value
  before answering (e.g. an offloaded payload). Use sparingly — not to keep working.
- Read the `<authoritative_ledger>` block in the resume message; it lists every
  WRITE you executed and every VERIFY that confirmed it.
- Compose a concise final answer citing the verified targets (table names, row
  counts, file paths). Pass everything in ONE call:
  `xpfinalize_task(payload={"final_answer": "...", "completed_items": [<ids the
  ledger covers>], "headers": {"toolcallreasoningtitle": "...",
  "toolcallreasoningdescription": "..."}})`. This sets `task.result` and ends the
  run — do NOT call `xpcomplete_agent_plan_items` separately.
- If you genuinely have nothing to report, still call `xpfinalize_task` with a
  short-status `final_answer` — the task must terminate.
</finalize_only_mode>
"""


# Synthetic result returned by the tool gate when a non-allowed tool is
# called while Finalize-Only is active. Matches the shape agno expects
# for a successful tool result — failure shape would trigger retry.
TOOL_GATE_REJECTION_MESSAGE = (
    "Finalize-only mode is active for this task. The only mutation tool "
    "available is `xpfinalize_task`. Read-only lookups (`xpget_agent_plan`, "
    "`xpworkspace-context-retrieve`, `xpworkspace-file-read`) are allowed if "
    "you need to fetch a value before composing the final answer. Read "
    "<authoritative_ledger> and call "
    'xpfinalize_task(payload={"final_answer": "...", "completed_items": [...], '
    '"headers": {"toolcallreasoningtitle": "...", "toolcallreasoningdescription": "..."}}) '
    "to terminate."
)


# Finalize tripped mid-run, so ``xpfinalize_task`` is not in this run's tool map (it is
# registered only when finalize is already active at run start). Terminate with prose instead.
TOOL_GATE_TEXT_EXIT_MESSAGE = (
    "Finalize-only mode is active for this task. Every mutation tool is now "
    "rejected. Read-only lookups (`xpget_agent_plan`, "
    "`xpworkspace-context-retrieve`, `xpworkspace-file-read`) are allowed if you "
    "need to fetch a value before composing the final answer. Read "
    "<authoritative_ledger> and then STOP CALLING TOOLS — reply with your final "
    "answer as a normal assistant message, citing the verified targets (table "
    "names, row counts, file paths). That message ends the task; the system marks "
    "the covered plan items itself."
)

# Escalation after repeated gated calls: the agent is looping instead of answering.
TOOL_GATE_TEXT_EXIT_ESCALATION = (
    "STOP. This is a repeated rejection — no tool you call will run. Your next "
    "message MUST be plain text with your final answer and NO tool calls. If you "
    "have nothing to report, say so in one line."
)

# How many gated calls before the escalation wording kicks in.
MAX_GATED_CALLS_BEFORE_ESCALATION = 3


# Success-shaped like TOOL_GATE_REJECTION_MESSAGE — failure shape would trigger an agno retry of the rejected call.
FINALIZE_NOT_ACTIVE_REJECTION = (
    "Rejected: finalize-only mode is NOT active, so `xpfinalize_task` must not "
    "be called and nothing was finalized. This tool is reserved for a system "
    "emergency state announced by a <finalize_only_mode> block in your "
    "instructions. To finish the task, simply reply with your final answer as "
    "a normal assistant message (the answer you composed is fine to send "
    "verbatim). Do not call `xpfinalize_task` again."
)


def _state_for(optimizer: Any) -> Optional[FinalizeOnlyState]:
    """Return the active FinalizeOnlyState — task-scoped first, then
    optimizer-scoped.

    Task-scope is authoritative: the plan-retry loop replaces the
    optimizer instance, so an optimizer-only state would vanish at the
    very retry boundary the finalize escape hatch needs to honor.
    """
    task = getattr(optimizer, "task", None)
    if task is not None:
        ts = getattr(task, "_xp_finalize_state", None)
        if isinstance(ts, FinalizeOnlyState):
            return ts
    state = getattr(optimizer, "_finalize_state", None)
    return state if isinstance(state, FinalizeOnlyState) else None


def enter_finalize_mode(
    optimizer: Any,
    *,
    reason: FinalizeReason,
    evidence: Optional[EvidenceReport] = None,
) -> FinalizeOnlyState:
    """Mark the optimizer's *task* as in Finalize-Only Mode.

    Idempotent — calling twice keeps the original ``reason`` (the first
    trigger wins so we don't overwrite "evidence" with a downstream
    "compact_loop" if both happen to fire). State is mirrored on
    ``task._xp_finalize_state`` so it survives optimizer replacement
    across plan retries.
    """
    existing = _state_for(optimizer)
    if existing and existing.active:
        return existing
    state = FinalizeOnlyState(
        active=True,
        reason=reason,
        entered_at_compaction_attempt=getattr(optimizer, "_compaction_attempt", 0),
        evidence=evidence,
    )
    # Mirror to both optimizer (legacy callers) and task (cross-retry).
    try:
        setattr(optimizer, "_finalize_state", state)
    except Exception:
        pass
    task = getattr(optimizer, "task", None)
    if task is not None:
        try:
            object.__setattr__(task, "_xp_finalize_state", state)
        except Exception:
            pass
    logger.warning(
        f"[finalize-mode] entered (reason={reason}, "
        f"compaction_attempt={state.entered_at_compaction_attempt})"
    )
    return state


def is_finalize_active(optimizer: Any) -> bool:
    state = _state_for(optimizer)
    return bool(state and state.active)


def is_task_finalize_active(task: Any) -> bool:
    """True when the task itself carries an active FinalizeOnlyState."""
    state = getattr(task, "_xp_finalize_state", None)
    return isinstance(state, FinalizeOnlyState) and state.active


def mark_finalize_tool_registered(task: Any) -> None:
    """Record that ``xpfinalize_task`` is in THIS run's tool map, so the gate knows
    whether it may point the agent at the tool or must ask for a plain-text answer."""
    try:
        object.__setattr__(task, "_xp_finalize_tool_registered", True)
    except Exception:
        pass


def is_finalize_tool_registered(task: Any) -> bool:
    """True when ``xpfinalize_task`` was registered for the run this ``task`` is executing."""
    return bool(getattr(task, "_xp_finalize_tool_registered", False))


def gate_rejection_message(task: Any, gated_calls: int) -> str:
    """Pick the tool-gate rejection: the tool when it exists this run, else plain prose."""
    if is_finalize_tool_registered(task):
        return TOOL_GATE_REJECTION_MESSAGE
    if gated_calls >= MAX_GATED_CALLS_BEFORE_ESCALATION:
        return f"{TOOL_GATE_TEXT_EXIT_MESSAGE}\n\n{TOOL_GATE_TEXT_EXIT_ESCALATION}"
    return TOOL_GATE_TEXT_EXIT_MESSAGE


async def finalize_task_from_run_end(task: Any) -> None:
    """Do the finalize bookkeeping the agent used to do via ``xpfinalize_task``.

    Runs when a task ends while Finalize-Only Mode is active and the tool was never
    called (the mid-run trip terminates with a plain-text answer instead). Plan items
    come from ledger evidence, never from the model.
    """
    if not is_task_finalize_active(task) or getattr(task, "_xp_finalize_ran", False):
        return
    try:
        object.__setattr__(task, "_xp_finalize_ran", True)
    except Exception:
        pass
    completed_items: List[str] = []
    try:
        state = getattr(task, "_xp_finalize_state", None)
        evidence = getattr(state, "evidence", None)
        if evidence is None:
            from xpander_sdk.core.context_optimizer.completion_evidence import (
                detect_completion_evidence,
            )

            evidence = detect_completion_evidence(
                get_attached_ledger(task), getattr(task, "deep_planning", None)
            )
        completed_items = list(getattr(evidence, "matched_plan_items", None) or [])
    except Exception as exc:
        logger.warning(f"[finalize-mode] evidence lookup at run end failed: {exc}")
    # Only a str answer is passed on; a structured result must reach the OutputFormat.Json
    # serializer with its own type, and _run_finalize leaves task.result alone on "".
    answer = getattr(task, "result", "")
    await _run_finalize(
        task=task,
        final_answer=answer if isinstance(answer, str) else "",
        completed_items=completed_items,
    )
    logger.info(
        f"[finalize-mode] finalized from run end "
        f"({len(completed_items)} plan item(s) from ledger evidence)"
    )


def is_tool_allowed(optimizer: Any, tool_name: str) -> bool:
    """Tool gate predicate. Returns ``True`` when the tool may run."""
    state = _state_for(optimizer)
    if not state or not state.active:
        return True
    return tool_name in state.allowed_tools


# ---------------------------------------------------------------------- #
#  xpfinalize_task tool spec — registered with agno when finalize active
# ---------------------------------------------------------------------- #


def build_finalize_tool(task: Any) -> Any:
    """Return an agno ``Function`` for ``xpfinalize_task``.

    Lazy-imports agno so tests that don't exercise the agno path don't
    pay the import cost. The closure captures the running ``task`` so
    the entrypoint can mark plan items + write ``task.result``.
    """
    from agno.tools.function import Function

    async def _entrypoint(
        payload: Optional[Union[Dict[str, Any], str]] = None,
    ) -> str:
        """Finalize the task; string payloads are parsed, unparseable ones become the final answer (finalize must terminate, never bounce)."""
        # Defense-in-depth for paths without tool hooks (e.g. NeMo): the agno hook gate never runs there.
        if not is_task_finalize_active(task):
            logger.warning(
                "[finalize-mode] premature xpfinalize_task call rejected at entrypoint"
            )
            return FINALIZE_NOT_ACTIVE_REJECTION
        if isinstance(payload, str):
            parsed = parse_structured_string(payload)
            payload = parsed if isinstance(parsed, dict) else {"final_answer": payload}
        data = payload or {}
        final_answer = data.get("final_answer", "") or ""
        completed_items = data.get("completed_items") or []
        # Suppresses the run-end fallback: the agent finalized explicitly.
        try:
            object.__setattr__(task, "_xp_finalize_ran", True)
        except Exception:
            pass
        return await _run_finalize(
            task=task,
            final_answer=final_answer,
            completed_items=completed_items,
        )

    return Function(
        name="xpfinalize_task",
        description=(
            "Terminate the current task with a final answer. Use this ONLY when "
            "Finalize-Only Mode is active (a <finalize_only_mode> block is present "
            "in the system instructions). Wrap arguments in a `payload` object: "
            "`payload.final_answer` is the concise final answer, "
            "`payload.completed_items` lists the ids of plan items the ledger "
            "evidence covers. The system marks those items as completed and ends "
            "the run. Calling this while <finalize_only_mode> is absent is an "
            "error — the call is rejected and nothing happens. To finish "
            "normally, just reply with your final answer."
        ),
        parameters={
            "type": "object",
            "properties": {
                "payload": {
                    "type": "object",
                    "properties": {
                        "final_answer": {
                            "type": "string",
                            "description": (
                                "Concise final answer summarizing what was accomplished. "
                                "Cite verified targets (table names, row counts, file paths) "
                                "from <authoritative_ledger>."
                            ),
                        },
                        "completed_items": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": (
                                "Ids of plan items covered by ledger evidence. Pass an "
                                "empty list when no plan is active."
                            ),
                        },
                        "headers": {
                            "type": "object",
                            "properties": {
                                "toolcallreasoningtitle": {
                                    "type": "string",
                                    "description": "Action-oriented title (max 5 words).",
                                },
                                "toolcallreasoningdescription": {
                                    "type": "string",
                                    "description": (
                                        "One-sentence markdown summary of why finalize is "
                                        "being called now (max 100 chars)."
                                    ),
                                },
                            },
                            "required": [
                                "toolcallreasoningtitle",
                                "toolcallreasoningdescription",
                            ],
                        },
                    },
                    "required": ["final_answer", "headers"],
                },
            },
            "required": ["payload"],
        },
        entrypoint=_entrypoint,
    )


async def _run_finalize(
    task: Any,
    *,
    final_answer: str,
    completed_items: List[str],
) -> str:
    """Mark plan items completed + write ``task.result``.

    Errors are logged but never re-raised — the goal is termination,
    so even partial finalization is preferable to another retry loop.
    """
    # Mark plan items as completed via the deep_planning model (no
    # round-trip through xpcomplete_agent_plan_items needed; the SDK
    # serializes deep_planning back on the next status update).
    evidence_note = ""
    try:
        if (
            completed_items
            and getattr(task, "deep_planning", None)
            and task.deep_planning.tasks
        ):
            # Soft gate: every recorded call failed -> the completion claim is fabricated; an absent/empty ledger never blocks.
            ledger = get_attached_ledger(task)
            all_calls_failed = bool(
                ledger
                and ledger.entries
                and all(entry.status != "ok" for entry in ledger.entries)
            )
            if all_calls_failed:
                evidence_note = (
                    "\n\n⚠️ Plan items were NOT marked completed: every recorded "
                    "tool call in this run failed, so there is no evidence the "
                    "work happened."
                )
                logger.warning(
                    f"[finalize-mode] refused to mark {len(completed_items)} plan "
                    f"item(s) complete — ledger has {len(ledger.entries)} entries, "
                    "all failed"
                )
            else:
                wanted = set(completed_items)
                for item in task.deep_planning.tasks:
                    if item.id in wanted and not item.completed:
                        item.completed = True
                logger.info(
                    f"[finalize-mode] marked {len(wanted)} plan item(s) complete"
                )
    except Exception as exc:
        logger.warning(f"[finalize-mode] plan-item update failed: {exc}")

    # Set task.result so the SDK surfaces the final answer.
    try:
        if hasattr(task, "result"):
            task.result = final_answer or task.result or ""
    except Exception as exc:
        logger.warning(f"[finalize-mode] failed to set task.result: {exc}")

    return (final_answer or "Task finalized.") + evidence_note
