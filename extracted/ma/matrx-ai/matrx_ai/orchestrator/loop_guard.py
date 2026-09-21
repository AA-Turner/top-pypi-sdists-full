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

import hashlib
import json
from dataclasses import dataclass, replace
from typing import Any, Literal

from matrx_utils import vcprint
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


# ── THE CEILINGS ARE KNOB ROWS, NOT CONSTANTS ────────────────────────────────
# These four numbers governed an expensive, rare decision (measured 2026-09-20:
# 38 of 2,329 (run, tool) pairs ever reach the ceiling) and were unturnable:
# module constants, no row, no org scope, and the one production caller passed
# no override. They live as ROWS now — ``platform.feature_knob`` feature
# ``orchestration.loop_guard``, org-scoped and admin-editable (migration
# ``db/migrations/0972_loop_guard_thresholds_become_knobs.sql``).
#
# What remains here is ONLY the declared default of each row, which is also what
# matrx-ai answers with when it runs standalone (the package must never import
# the host, and a desktop/client host has no Postgres at all). The host resolves
# the rows per organization through :func:`load_loop_guard_thresholds` and hands
# the result to :func:`evaluate_loop_health`; nothing in production reads these
# names directly.
DEFAULT_MIN_CALLS_BEFORE_CHECK = 8
DEFAULT_WINDOW_SIZE = 20
DEFAULT_FAILURE_THRESHOLD = 8
DEFAULT_RECOVERY_WINDOW = 3
#: Minimum confidence in a standoff verdict before the caller acts on it. Below
#: this we fall back to the count rule and disable the failing tool.
DEFAULT_STANDOFF_DECISION_CONFIDENCE = 0.7

#: The knob feature every threshold above is a row of.
LOOP_GUARD_KNOB_FEATURE = "orchestration.loop_guard"
#: field name on :class:`LoopGuardThresholds` → knob key. The key IS the field
#: name; the mapping is explicit so a rename cannot silently stop reading a row.
LOOP_GUARD_KNOB_KEYS: dict[str, str] = {
    "window_size": "window_size",
    "min_calls_before_check": "min_calls_before_check",
    "failure_threshold": "failure_threshold",
    "recovery_window": "recovery_window",
    "standoff_decision_confidence": "standoff_decision_confidence",
}


@dataclass(frozen=True)
class LoopGuardThresholds:
    """The ceilings in force for ONE run, and where they came from.

    ``source`` is never decoration: a run judged on package defaults when the
    host WAS configured means the knob door failed, and the guard says so out
    loud rather than quietly applying a number no admin can see.
    """

    window_size: int = DEFAULT_WINDOW_SIZE
    min_calls_before_check: int = DEFAULT_MIN_CALLS_BEFORE_CHECK
    failure_threshold: int = DEFAULT_FAILURE_THRESHOLD
    recovery_window: int = DEFAULT_RECOVERY_WINDOW
    standoff_decision_confidence: float = DEFAULT_STANDOFF_DECISION_CONFIDENCE
    source: Literal["knobs", "package_defaults"] = "package_defaults"


async def load_loop_guard_thresholds(
    organization_id: str | None = None,
    user_id: str | None = None,
) -> LoopGuardThresholds:
    """The org's effective ceilings, read through the host's settings door.

    matrx-ai may not import the host, so the host injects a reader
    (``loop_guard_threshold_reader`` — see ``aidream/package_integration.py``)
    that resolves the ``orchestration.loop_guard`` knob rows for this principal.
    With NO reader configured (matrx-ai standalone, a client host with no
    Postgres) the declared defaults are the honest answer and stay silent.

    A reader that is configured and FAILS is a different fact: the admin's rows
    exist and did not reach the run. That announces itself.
    """
    from matrx_ai._ext import get_loop_guard_threshold_reader

    reader = get_loop_guard_threshold_reader()
    if reader is None:
        return LoopGuardThresholds()
    try:
        values = await reader(organization_id=organization_id, user_id=user_id)
    except Exception as exc:  # noqa: BLE001 — never let the door break the run
        vcprint(
            f"⚠️  Loop guard could not read its '{LOOP_GUARD_KNOB_FEATURE}' settings "
            f"({type(exc).__name__}: {exc}). Falling back to the package defaults "
            f"(window {DEFAULT_WINDOW_SIZE}, threshold {DEFAULT_FAILURE_THRESHOLD}); "
            f"any organization override is NOT in force for this run.",
            "[LOOP GUARD] Settings unavailable",
            color="yellow",
        )
        return LoopGuardThresholds()
    if not isinstance(values, dict) or not values:
        return LoopGuardThresholds()
    return _thresholds_from_values(values)


def _thresholds_from_values(values: dict[str, Any]) -> LoopGuardThresholds:
    """Build thresholds from resolved knob values, keeping the declared default
    for any key the door did not answer."""
    out = LoopGuardThresholds(source="knobs")
    for field_name, key in LOOP_GUARD_KNOB_KEYS.items():
        if key not in values or values[key] is None:
            continue
        raw = values[key]
        try:
            value = float(raw) if field_name == "standoff_decision_confidence" else int(raw)
        except (TypeError, ValueError):
            continue
        out = replace(out, **{field_name: value})
    return out


def evaluate_loop_health(
    history: list[ToolCallUsage],
    *,
    thresholds: LoopGuardThresholds | None = None,
    min_calls_before_check: int | None = None,
    window_size: int | None = None,
    failure_threshold: int | None = None,
    recovery_window: int | None = None,
) -> LoopHealth:
    """Decide whether the agent loop is making progress.

    ``thresholds`` is the org's effective ceilings from
    :func:`load_loop_guard_thresholds` — the shape production passes. The four
    individual keyword arguments remain for tests and for a caller that needs to
    override exactly one number; each wins over ``thresholds`` when given.

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
    limits = thresholds or LoopGuardThresholds()
    min_calls_before_check = (
        limits.min_calls_before_check if min_calls_before_check is None else min_calls_before_check
    )
    window_size = limits.window_size if window_size is None else window_size
    failure_threshold = limits.failure_threshold if failure_threshold is None else failure_threshold
    recovery_window = limits.recovery_window if recovery_window is None else recovery_window

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
    sentence += " Fix that tool, or the value this step passes it, then retry the step."
    return sentence


# ── ONE TOOL, NOT EVERY TOOL ─────────────────────────────────────────────────
# Until 2026-09-20 tripping the guard set ``config.tools = []`` and
# ``config.custom_tools = []``: one broken tool took every other tool with it
# and the run paused for a human. Measured on chat.tool_call the same day: of
# 2,054 adjacent same-tool failure pairs only 416 (20.3%) repeat BYTE-IDENTICAL
# arguments, so four out of five shut-offs landed on an agent that was adapting
# — and it lost its whole tool belt for it. The guard now removes the ONE tool
# whose failures tripped it and lets the run continue on the rest.

#: Recent calls of the failing tool carried into a standoff decision. Enough to
#: see a repeat (the worst real pair failed 41 times), short enough for a
#: text-only decision model.
STANDOFF_RECENT_CALLS = 12
#: Per-call argument text in ``recent_calls_text``. The fingerprints answer
#: "identical?" deterministically; this is only for a reader's eyes.
STANDOFF_ARGS_TEXT_CAP = 240

#: The four things a standoff verdict may ask the caller to do.
STANDOFF_ACTIONS = (
    "continue",
    "continue_with_hint",
    "disable_this_tool",
    "stop_the_run",
)
#: The mandate that decides. Named in every fallback warning so "we did not ask"
#: is never silent (Nothing fails silently).
STANDOFF_MANDATE_KEY = "orchestration.tool_failure_standoff_decision"


def _details(history: list[ToolCallUsage] | None) -> list[dict[str, Any]]:
    """Every tool-call detail in the run, oldest first."""
    return [
        detail
        for usage in history or []
        for detail in (getattr(usage, "tool_calls_details", None) or [])
        if isinstance(detail, dict)
    ]


def _detail_name(detail: dict[str, Any]) -> str:
    return str(detail.get("name") or "") or "(unnamed tool)"


def failing_tool_from_history(
    history: list[ToolCallUsage] | None,
    *,
    window_size: int = DEFAULT_WINDOW_SIZE,
    exclude: tuple[str, ...] | list[str] | None = None,
) -> str | None:
    """The ONE tool to switch off: most failures inside the guard's window.

    Ties break on the most RECENT failure, because that is the tool the agent is
    still hammering. ``exclude`` names tools this run has ALREADY disabled — a
    tool that can no longer be called must never be re-chosen, or the guard
    would trip forever on failures it has already answered. Returns ``None``
    when nothing blameable remains, and the caller then disables nothing rather
    than picking arbitrarily.
    """
    blocked = tuple(exclude or ())
    window = _details(history)[-window_size:] if window_size > 0 else _details(history)
    scores: dict[str, tuple[int, int]] = {}
    for index, detail in enumerate(window):
        if bool(detail.get("success", True)):
            continue
        name = _detail_name(detail)
        if any(_tool_name_matches(name, off) for off in blocked):
            continue
        failures, _last = scores.get(name, (0, -1))
        scores[name] = (failures + 1, index)
    if not scores:
        return None
    return max(scores.items(), key=lambda item: (item[1][0], item[1][1]))[0]


@dataclass(frozen=True)
class ToolDisableOutcome:
    """What removing one tool from a live request actually did."""

    tool: str
    removed: bool
    remaining_tools: tuple[str, ...]
    #: True when the failing tool was the run's ONLY tool — there is no
    #: "continue with the rest", so the caller keeps the pause-for-human path.
    was_only_tool: bool


def _tool_name_matches(candidate: str, target: str) -> bool:
    """Match a config entry against a called tool name across the wire form.

    Internal names may carry a namespace colon (``bundle:list_supabase``) that
    the provider boundary rewrites to ``__``; a call recorded under either form
    must still find its declaration.
    """
    if candidate == target:
        return True
    return candidate.replace(":", "__") == target.replace(":", "__")


def disable_failing_tool(config: Any, tool_name: str) -> ToolDisableOutcome:
    """Remove ONE tool from a live request config, leaving every other tool.

    Touches ``config.tools`` (registered names) and ``config.custom_tools``
    (inline declarations, matched on ``.name``) — the two lists the provider
    boundary assembles its declarations from. Nothing else about the request
    changes, so the run continues with the rest of its belt.
    """
    registered = [t for t in (getattr(config, "tools", None) or [])]
    custom = [t for t in (getattr(config, "custom_tools", None) or [])]

    kept_registered = [
        t for t in registered if not (isinstance(t, str) and _tool_name_matches(t, tool_name))
    ]
    kept_custom = [
        t for t in custom if not _tool_name_matches(str(getattr(t, "name", "") or ""), tool_name)
    ]
    removed = len(kept_registered) != len(registered) or len(kept_custom) != len(custom)

    config.tools = kept_registered
    config.custom_tools = kept_custom

    remaining = tuple(
        [t for t in kept_registered if isinstance(t, str)]
        + [str(getattr(t, "name", "") or "") for t in kept_custom]
    )
    return ToolDisableOutcome(
        tool=tool_name,
        removed=removed,
        remaining_tools=remaining,
        was_only_tool=removed and not remaining,
    )


def disabled_tool_notice(outcome: ToolDisableOutcome, *, reason: str) -> str:
    """The ONE sentence the assistant is told, naming the tool and why.

    A control that vanished without a word is exactly the dead screen the
    platform forbids: the model must know which tool left its belt, so it can
    say so to the person and route around it.
    """
    remaining = (
        f" Your other tools ({', '.join(outcome.remaining_tools)}) still work"
        if outcome.remaining_tools
        else " You have no other tools left"
    )
    return (
        f"⚠️ SYSTEM NOTICE (not from the user): the '{outcome.tool}' tool has been "
        f"disabled for the rest of this run because {reason}.{remaining} — continue "
        f"without '{outcome.tool}', and tell the user plainly if the job cannot be "
        f"finished without it."
    )


# ── THE PROVISION THE VERDICT IS DECIDED FROM ────────────────────────────────


def _arguments_fingerprint(arguments: Any) -> str:
    """A stable short hash of one call's arguments.

    Two equal adjacent entries are a byte-identical repeat — the deterministic
    fact that separates a loop from an adapting agent, so the decision confirms
    it rather than eyeballing prose.
    """
    try:
        text = json.dumps(arguments, sort_keys=True, default=str)
    except Exception:  # noqa: BLE001
        text = repr(arguments)
    return hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()[:16]


def _arguments_text(arguments: Any) -> str:
    try:
        text = json.dumps(arguments, sort_keys=True, default=str)
    except Exception:  # noqa: BLE001
        text = repr(arguments)
    return text[:STANDOFF_ARGS_TEXT_CAP]


def _error_class(detail: dict[str, Any]) -> str:
    error = detail.get("error")
    if isinstance(error, dict):
        for key in ("error_type", "type", "code"):
            value = error.get(key)
            if isinstance(value, str) and value:
                return value
    value = detail.get("error_type")
    return value if isinstance(value, str) and value else "unclassified"


def build_standoff_provision(
    history: list[ToolCallUsage] | None,
    *,
    tool_name: str,
    health: LoopHealth,
    thresholds: LoopGuardThresholds | None = None,
    config: Any = None,
    model_id: str | None = None,
    run_goal: str | None = None,
    assistant_text_between_calls: str | None = None,
    is_unattended: bool = False,
    already_intervened: bool = False,
) -> dict[str, Any]:
    """Assemble ``orchestration.tool_failure_standoff`` from the IN-MEMORY history.

    The persisted evidence blob deliberately carries no arguments, so the one
    question that separates a loop from an adapting agent is unanswerable from
    it. ``tool_calls_details`` still holds the full arguments at verdict time —
    this reads them there, and nothing here is routed back into the persisted
    blob.
    """
    limits = thresholds or LoopGuardThresholds()
    all_details = _details(history)
    mine = [d for d in all_details if _tool_name_matches(_detail_name(d), tool_name)]
    recent = mine[-STANDOFF_RECENT_CALLS:]

    failures_this_tool = sum(1 for d in mine if not bool(d.get("success", True)))
    successes_this_tool = len(mine) - failures_this_tool
    consecutive = 0
    for detail in reversed(mine):
        if bool(detail.get("success", True)):
            break
        consecutive += 1

    recent_json: list[dict[str, Any]] = []
    lines: list[str] = []
    fingerprints: list[str] = []
    error_classes: list[str] = []
    error_messages: list[str] = []
    for position, detail in enumerate(recent, start=1):
        success = bool(detail.get("success", True))
        arguments = detail.get("arguments", {})
        fingerprint = _arguments_fingerprint(arguments)
        fingerprints.append(fingerprint)
        message = _detail_error_text(detail)
        row = {
            "position": position,
            "call_id": str(detail.get("call_id") or detail.get("id") or ""),
            "arguments": arguments,
            "success": success,
            "arguments_fingerprint": fingerprint,
        }
        if not success:
            error_class = _error_class(detail)
            error_classes.append(error_class)
            row["error_type"] = error_class
            if message:
                error_messages.append(message)
                row["error_message"] = message
        recent_json.append(row)
        lines.append(
            f"#{position} {'OK  ' if success else 'FAIL'} "
            f"{'' if success else _error_class(detail) + ' '}"
            f"{_arguments_text(arguments)}" + (f" -> {message}" if message else "")
        )

    definition = next(
        (d.get("definition") for d in reversed(mine) if isinstance(d.get("definition"), dict)),
        None,
    )
    other_tools = [
        name
        for name in (
            [t for t in (getattr(config, "tools", None) or []) if isinstance(t, str)]
            + [
                str(getattr(t, "name", "") or "")
                for t in (getattr(config, "custom_tools", None) or [])
            ]
        )
        if name and not _tool_name_matches(name, tool_name)
    ]

    provision: dict[str, Any] = {
        "tool_name": tool_name,
        "recent_calls_json": recent_json,
        "recent_calls_text": "\n".join(lines),
        "arguments_fingerprints": fingerprints,
        "error_classes": error_classes,
        "error_messages": error_messages,
        "model_id": model_id or "",
        "other_tools_available": other_tools,
        "failures_this_tool": failures_this_tool,
        "consecutive_failures_this_tool": consecutive,
        "successes_this_tool": successes_this_tool,
        "failures_in_window": health.failures_in_window,
        "window_size": health.window_size or limits.window_size,
        "failures_total": sum(1 for d in all_details if not bool(d.get("success", True))),
        "call_count_total": len(all_details),
        "failure_limit": limits.failure_threshold,
        "is_unattended": bool(is_unattended),
        "already_intervened": bool(already_intervened),
    }
    if isinstance(definition, dict):
        description = definition.get("description")
        if isinstance(description, str) and description:
            provision["tool_description"] = description
        for key in ("input_schema", "parameters", "schema"):
            schema = definition.get(key)
            if isinstance(schema, dict) and schema:
                provision["tool_schema"] = schema
                break
    if run_goal:
        provision["run_goal"] = run_goal
    if assistant_text_between_calls:
        provision["assistant_text_between_calls"] = assistant_text_between_calls
    return provision


# ── THE VERDICT ──────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class StandoffVerdict:
    """What to do about the failing tool, and who decided it."""

    action: Literal["continue", "continue_with_hint", "disable_this_tool", "stop_the_run"]
    confidence: float
    source: Literal["mandate", "fallback"]
    reason: str
    hint: str = ""


def _scalar(value: Any) -> tuple[Any, float | None]:
    """Unwrap one mandate answer into ``(value, probability)``.

    An atomic answer may arrive flat (``"disable_this_tool"``) or wrapped with
    its calibrated probability (``{"value": …, "probability": 0.82}``); both are
    the same answer and neither is guessed at.
    """
    if isinstance(value, dict):
        for key in ("value", "answer", "action"):
            if key in value:
                inner = value[key]
                break
        else:
            return None, None
        probability = None
        for key in ("probability", "confidence", "score"):
            candidate = value.get(key)
            if isinstance(candidate, int | float):
                probability = float(candidate)
                break
        return inner, probability
    return value, None


def fallback_standoff_verdict(reason: str) -> StandoffVerdict:
    """Today's count rule — but scoped to the ONE failing tool."""
    return StandoffVerdict(
        action="disable_this_tool",
        confidence=1.0,
        source="fallback",
        reason=reason,
    )


def verdict_from_mandate_output(
    parsed: Any,
    *,
    thresholds: LoopGuardThresholds | None = None,
) -> StandoffVerdict | None:
    """Read a standoff answer, or ``None`` when it cannot be acted on.

    ``None`` means the caller falls back — an unreadable answer, an action
    outside the declared set, or a probability under the org's configured bar.
    Never a silent "continue": a verdict we cannot trust must not be the reason
    a failing tool keeps running.
    """
    limits = thresholds or LoopGuardThresholds()
    if not isinstance(parsed, dict):
        return None
    action, probability = _scalar(parsed.get("action"))
    if not isinstance(action, str) or action not in STANDOFF_ACTIONS:
        return None
    if probability is None:
        for key in ("action_confidence", "confidence", "probability"):
            candidate = parsed.get(key)
            if isinstance(candidate, int | float):
                probability = float(candidate)
                break
    confidence = 1.0 if probability is None else probability
    if confidence < limits.standoff_decision_confidence:
        return None
    hint_value, _ = _scalar(parsed.get("hint"))
    hint = hint_value if isinstance(hint_value, str) else ""
    if action == "continue_with_hint" and not hint.strip():
        # The contract says the hint names the specific thing to change. An
        # empty one is not a hint, and injecting nothing would be a silent
        # no-op dressed as an intervention.
        return None
    return StandoffVerdict(
        action=action,  # type: ignore[arg-type]
        confidence=confidence,
        source="mandate",
        reason=str(parsed.get("reason") or "").strip(),
        hint=hint.strip(),
    )


async def decide_tool_standoff(
    provision: dict[str, Any],
    *,
    thresholds: LoopGuardThresholds | None = None,
) -> StandoffVerdict:
    """Ask the standoff mandate what to do, or fall back out loud.

    matrx-ai may not import the host's mandate registry, so the host injects a
    decider (``tool_failure_standoff_decider``). It returns the mandate's parsed
    answer, or ``None`` when NO Holder is bound to
    ``orchestration.tool_failure_standoff_decision`` — which is the case today.
    Unbound, unreadable, or under-confident, the answer is the same: fall back
    to the count rule, disable only the failing tool, and WARN naming the
    mandate, so "nobody is deciding this" is never silent.
    """
    from matrx_ai._ext import get_tool_failure_standoff_decider

    tool_name = str(provision.get("tool_name") or "the failing tool")
    decider = get_tool_failure_standoff_decider()
    if decider is None:
        return _warned_fallback(
            tool_name,
            "no decider is wired into this host at all",
        )
    try:
        parsed = await decider(provision)
    except Exception as exc:  # noqa: BLE001 — a broken decider never breaks a run
        return _warned_fallback(tool_name, f"the decision run failed ({type(exc).__name__}: {exc})")
    if parsed is None:
        return _warned_fallback(tool_name, "no Holder is bound to it, so nobody can answer yet")
    verdict = verdict_from_mandate_output(parsed, thresholds=thresholds)
    if verdict is None:
        limits = thresholds or LoopGuardThresholds()
        return _warned_fallback(
            tool_name,
            f"its answer was unreadable or under the configured confidence bar "
            f"({limits.standoff_decision_confidence})",
        )
    return verdict


#: What the caller actually DOES about a standoff verdict.
#:   continue_with_note — the failing tool stays, the assistant is told this is
#:                        its last attempt (and the hint, when there is one).
#:   disable_tool       — remove that ONE tool; the run carries on with the rest.
#:   pause_for_human    — strip everything and stop for review.
StandoffBranch = Literal["continue_with_note", "disable_tool", "pause_for_human"]


def standoff_branch(action: str, *, already_continued: bool) -> StandoffBranch:
    """Turn a verdict's action into the branch the orchestrator takes.

    Pure on purpose: this is the decision the 6,000-line executor loop used to
    make inline as a blind count, and it is the one thing a test must be able to
    pin. ``already_continued`` spends the run's single "keep going" — a second
    one would be an unbounded way to pay for the same broken tool, so it lands
    on ``disable_tool`` like every other action that is not stop.
    """
    if action == "stop_the_run":
        return "pause_for_human"
    if action in ("continue", "continue_with_hint") and not already_continued:
        return "continue_with_note"
    return "disable_tool"


def _warned_fallback(tool_name: str, why: str) -> StandoffVerdict:
    reason = (
        f"The '{STANDOFF_MANDATE_KEY}' mandate did not decide this standoff because "
        f"{why}. Falling back to the failure-count rule and disabling only "
        f"'{tool_name}'; every other tool keeps working."
    )
    vcprint(reason, "[LOOP GUARD] Standoff decided by fallback", color="yellow")
    return fallback_standoff_verdict(reason)


__all__ = [
    "DEFAULT_FAILURE_THRESHOLD",
    "DEFAULT_MIN_CALLS_BEFORE_CHECK",
    "DEFAULT_RECOVERY_WINDOW",
    "DEFAULT_STANDOFF_DECISION_CONFIDENCE",
    "DEFAULT_WINDOW_SIZE",
    "ERROR_TEXT_CAP",
    "LOOP_GUARD_KNOB_FEATURE",
    "LOOP_GUARD_KNOB_KEYS",
    "LOOP_STALL_ERROR_TYPE",
    "STANDOFF_ACTIONS",
    "STANDOFF_MANDATE_KEY",
    "STANDOFF_RECENT_CALLS",
    "LoopGuardThresholds",
    "LoopHealth",
    "MAX_TOOLS_IN_EVIDENCE",
    "StandoffBranch",
    "StandoffVerdict",
    "ToolDisableOutcome",
    "build_standoff_provision",
    "decide_tool_standoff",
    "disable_failing_tool",
    "disabled_tool_notice",
    "evaluate_loop_health",
    "failing_tool_from_history",
    "fallback_standoff_verdict",
    "load_loop_guard_thresholds",
    "loop_guard_evidence",
    "loop_guard_sentence",
    "standoff_branch",
    "verdict_from_mandate_output",
]
