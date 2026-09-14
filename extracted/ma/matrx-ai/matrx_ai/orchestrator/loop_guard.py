"""The rolling tool-health verdict — and the EVIDENCE behind it.

The verdict alone ("11/11 failed") is enough to stop a loop and useless to
anyone who has to fix it. :func:`loop_guard_evidence` answers the three
questions the guard already knows the answer to — WHICH tool, HOW MANY times,
and WHAT it said — so the reason travels with the pause instead of dying in the
executor's local variables.

Found live 2026-09-12, workflow run ``6fa6ad90`` ("Newsroom Desk"): the check
step's agent called the ``rulebook`` tool 11 times with a slug where a UUID
belongs, every call failed, the guard paused the turn, and the person was told
"Check it against the live Rulebook stopped partway through." The node failure
recorded ``ai_turn_failed: … 'paused_loop_guard': no error detail recorded``
while the executor was holding the tool name, the count and the exact error.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from matrx_utils.error_text import classification_text

from matrx_ai.orchestrator.tracking import ToolCallUsage


@dataclass(frozen=True)
class LoopHealth:
    verdict: Literal["healthy", "stuck"]
    reason: str
    total_calls: int
    window_size: int
    failures_in_window: int
    successes_in_window: int


DEFAULT_MIN_CALLS_BEFORE_CHECK = 8
DEFAULT_WINDOW_SIZE = 20
DEFAULT_FAILURE_THRESHOLD = 8
DEFAULT_RECOVERY_WINDOW = 3


def evaluate_loop_health(
    history: list[ToolCallUsage],
    *,
    min_calls_before_check: int = DEFAULT_MIN_CALLS_BEFORE_CHECK,
    window_size: int = DEFAULT_WINDOW_SIZE,
    failure_threshold: int = DEFAULT_FAILURE_THRESHOLD,
    recovery_window: int = DEFAULT_RECOVERY_WINDOW,
) -> LoopHealth:
    """Decide whether the agent loop is making progress.

    Operates on per-tool-call success flags (one entry per call, not per
    iteration), so a single iteration that fired five parallel tool calls
    contributes five data points. Pure and side-effect-free — safe to call
    every iteration.

    Verdict policy:
      - Fewer than ``min_calls_before_check`` total calls so far → healthy
        (not enough data to judge).
      - If the most recent ``recovery_window`` calls are all successes →
        healthy (the model just recovered from a bad streak).
      - Otherwise, count failures in the most recent ``window_size`` calls.
        If failures ≥ ``failure_threshold`` → stuck.
      - Otherwise → healthy.
    """
    flat: list[bool] = [
        bool(detail.get("success", True))
        for usage in history
        for detail in usage.tool_calls_details
    ]

    total = len(flat)
    if total < min_calls_before_check:
        return LoopHealth(
            verdict="healthy",
            reason=f"only {total} tool calls so far (min {min_calls_before_check} before evaluation)",
            total_calls=total,
            window_size=0,
            failures_in_window=0,
            successes_in_window=0,
        )

    window = flat[-window_size:]
    failures = sum(1 for ok in window if not ok)
    successes = len(window) - failures

    if recovery_window > 0 and total >= recovery_window:
        recent = flat[-recovery_window:]
        if all(recent):
            return LoopHealth(
                verdict="healthy",
                reason=f"last {recovery_window} tool calls all succeeded — recovered",
                total_calls=total,
                window_size=len(window),
                failures_in_window=failures,
                successes_in_window=successes,
            )

    if failures >= failure_threshold:
        return LoopHealth(
            verdict="stuck",
            reason=(
                f"{failures}/{len(window)} tool calls failed in the last {len(window)} "
                f"(threshold ≥ {failure_threshold}) and recent runs did not recover"
            ),
            total_calls=total,
            window_size=len(window),
            failures_in_window=failures,
            successes_in_window=successes,
        )

    return LoopHealth(
        verdict="healthy",
        reason=f"{failures}/{len(window)} failures in window — under threshold",
        total_calls=total,
        window_size=len(window),
        failures_in_window=failures,
        successes_in_window=successes,
    )


# ── THE GUARD'S EVIDENCE ─────────────────────────────────────────────────────
#: Per-tool error text kept in the evidence. Long enough to carry a real
#: diagnostic ("Invalid arguments: 1 validation error … rulebook_id"), short
#: enough that a tool echoing its input cannot turn a failure record into a
#: payload dump. The text is run through ``classification_text`` first, so an
#: args block is cut before this cap is even measured.
#: The ``error_type`` a stalled tool loop records — the machine word every
#: reader downstream keys on (matrx-graph's cause ladder maps it to
#: ``Cause.TOOL_LOOP_STALLED``). Never the bare status: a status says the run
#: PAUSED, this says WHY, and inside an unattended step the why is the failure.
LOOP_STALL_ERROR_TYPE = "tool_loop_stalled"

ERROR_TEXT_CAP = 400
#: Tools named in one evidence record. A stuck loop is one or two broken tools;
#: past this the list stops being a diagnosis.
MAX_TOOLS_IN_EVIDENCE = 4


def _detail_error_text(detail: dict[str, Any]) -> str:
    """The agent-facing error for ONE failed call, bounded and args-stripped.

    Reads the structured ``error.message`` first and the exact agent-facing
    string second — never ``arguments``, which is the call's payload.
    """
    error = detail.get("error")
    text = ""
    if isinstance(error, dict):
        text = str(error.get("message") or "")
    if not text:
        agent_error = detail.get("agent_error")
        text = agent_error if isinstance(agent_error, str) else ""
    if not text:
        return ""
    return classification_text(text).strip()[:ERROR_TEXT_CAP]


def loop_guard_evidence(history: list[ToolCallUsage]) -> dict[str, Any]:
    """What the guard saw, in a JSON-safe shape fit to persist in metadata.

    ``{"failed_calls": 11, "total_calls": 11, "tools": [{"tool": "rulebook",
    "calls": 11, "failures": 11, "last_error": "…"}]}`` — tools ordered by
    failure count, most-broken first. Never carries arguments, never a full
    payload. Returns the counts with an empty ``tools`` list when the history
    holds no failures (the honest "there genuinely is nothing" case).
    """
    per_tool: dict[str, dict[str, Any]] = {}
    total = 0
    failed = 0
    for usage in history or []:
        for detail in getattr(usage, "tool_calls_details", None) or []:
            if not isinstance(detail, dict):
                continue
            total += 1
            name = str(detail.get("name") or "") or "(unnamed tool)"
            row = per_tool.setdefault(
                name, {"tool": name, "calls": 0, "failures": 0, "last_error": ""}
            )
            row["calls"] += 1
            if bool(detail.get("success", True)):
                continue
            failed += 1
            row["failures"] += 1
            text = _detail_error_text(detail)
            if text:
                row["last_error"] = text
    tools = [row for row in per_tool.values() if row["failures"]]
    tools.sort(key=lambda row: (-row["failures"], row["tool"]))
    for row in tools:
        if not row["last_error"]:
            row.pop("last_error")
    return {
        "failed_calls": failed,
        "total_calls": total,
        "tools": tools[:MAX_TOOLS_IN_EVIDENCE],
    }


def loop_guard_sentence(evidence: dict[str, Any] | None, *, unattended: bool = False) -> str:
    """The one honest sentence: what stalled, what it said, what to change.

    Returns ``""`` when there is no evidence at all — the caller says why, rather
    than this inventing a reason. ``unattended`` adds the fact that decides the
    outcome in a workflow: there is nobody to review the pause.
    """
    tools = list((evidence or {}).get("tools") or [])
    if not tools:
        return ""
    parts = [
        f"the '{row['tool']}' tool failed {row['failures']} of its {row['calls']} call(s)"
        for row in tools
    ]
    head = parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + f" and {parts[-1]}"
    sentence = f"{head}, so tools were disabled and the turn stopped."
    last = next((row.get("last_error") for row in tools if row.get("last_error")), "")
    if last:
        sentence += f" Last error from '{tools[0]['tool']}': “{last}”."
    if unattended:
        sentence += (
            " This ran as an unattended step, so there is nobody to review the pause"
            " — it is a failure, not a wait."
        )
    sentence += (
        " Fix that tool, or the value this step passes it, then retry the step."
    )
    return sentence


__all__ = [
    "DEFAULT_FAILURE_THRESHOLD",
    "DEFAULT_MIN_CALLS_BEFORE_CHECK",
    "DEFAULT_RECOVERY_WINDOW",
    "DEFAULT_WINDOW_SIZE",
    "ERROR_TEXT_CAP",
    "LOOP_STALL_ERROR_TYPE",
    "LoopHealth",
    "MAX_TOOLS_IN_EVIDENCE",
    "evaluate_loop_health",
    "loop_guard_evidence",
    "loop_guard_sentence",
]
