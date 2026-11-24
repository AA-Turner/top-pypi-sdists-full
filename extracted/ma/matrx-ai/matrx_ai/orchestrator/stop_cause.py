"""WHY a run stopped before it finished, as one structured value a caller can relay truthfully.

A run the loop stops early ends with a sentence ("Stopped after 12 iterations", "the desk ran out of
its 360s time budget"). A caller that relays the stop to a person (a delegation desk, agent_call, a
staff turn) must not guess from that sentence which limit bound. This module is the ONE place the
cause is named: the loop stamps it into the run's completion metadata under ``STOP_CAUSE_KEY``
when it knows it at the stop site (time, cost cap, cancel), and :func:`stop_cause_from_metadata`
derives the rest from what the loop already records (rounds, the guardrail budget wrap-up).

``AgentRunResult.stop_cause`` carries it to every ``run_agent`` caller. ``None`` means the run was
not stopped by a limit (it finished, or it failed for another reason).
"""

from __future__ import annotations

import time
from typing import Any, Literal

from pydantic import BaseModel

#: Completion-metadata key the loop stamps a known stop cause under.
STOP_CAUSE_KEY = "stop_cause"

StopCauseKind = Literal["rounds", "time", "cost", "cancelled", "execution_control"]


class RunStopCause(BaseModel):
    """The limit that stopped a run, with its numbers.

    ``kind``: ``rounds`` (the tool-round ceiling), ``time`` (a subtree time budget), ``cost`` (a
    dollar cap or the spend guardrail's run budget), ``cancelled`` (a person or the platform
    stopped it), ``execution_control`` (a host control whose axis it did not name).
    ``allowed`` / ``used`` are in ``unit`` (``rounds`` / ``seconds`` / ``usd``) when known.
    ``label`` names the budget's owner when one was given ("senior desk"). ``detail`` is the
    loop's own sentence, for display.
    """

    kind: StopCauseKind
    allowed: float | None = None
    used: float | None = None
    unit: Literal["rounds", "seconds", "usd"] | None = None
    label: str | None = None
    detail: str = ""


def rounds_cause(max_iterations: int, used: int | None = None) -> RunStopCause:
    return RunStopCause(
        kind="rounds",
        allowed=float(max_iterations),
        used=float(used if used is not None else max_iterations),
        unit="rounds",
        detail=f"used all {int(max_iterations)} tool rounds this run allows",
    )


def time_cause(budget: dict[str, Any], *, now: float | None = None) -> RunStopCause:
    moment = time.time() if now is None else now
    opened = float(budget.get("opened_at") or moment)
    seconds = int(budget.get("seconds") or 0)
    label = str(budget.get("label") or "") or None
    return RunStopCause(
        kind="time",
        allowed=float(seconds),
        used=round(max(0.0, moment - opened), 1),
        unit="seconds",
        label=label,
        detail=f"{label or 'this run'} ran out of its {seconds}s time budget",
    )


def cost_cause(*, allowed: float | None, used: float | None, detail: str) -> RunStopCause:
    return RunStopCause(kind="cost", allowed=allowed, used=used, unit="usd", detail=detail)


def stop_cause_from_metadata(metadata: Any) -> RunStopCause | None:
    """The stop cause a run's completion metadata records, or None when no limit stopped it."""
    if not isinstance(metadata, dict):
        return None
    stamped = metadata.get(STOP_CAUSE_KEY)
    if isinstance(stamped, RunStopCause):
        return stamped
    if isinstance(stamped, dict):
        try:
            return RunStopCause.model_validate(stamped)
        except Exception:  # noqa: BLE001 — an unreadable stamp falls back to derivation below
            pass
    if metadata.get("budget_wrap_up"):
        return cost_cause(allowed=None, used=None, detail="reached this run's spend budget")
    if metadata.get("status") == "max_iterations_exceeded" or metadata.get("ceiling_wrap_up"):
        limit = metadata.get("max_iterations")
        if isinstance(limit, int | float) and limit > 0:
            return rounds_cause(int(limit))
        return RunStopCause(kind="rounds", unit="rounds", detail="used all tool rounds this run allows")
    if metadata.get("status") == "cancelled":
        error = metadata.get("error")
        detail = str(error.get("message") if isinstance(error, dict) else error or "the run was stopped")
        return RunStopCause(kind="execution_control", detail=detail)
    return None


def stop_cause_from_exception(exc: Any) -> RunStopCause | None:
    """The stop cause a guardrail refusal raised into the run names (``guardrail_gate.GuardrailStopError``, read by
    shape so this module imports nothing): Max cost per run and the spend caps are ``cost`` (USD, with the host's own
    sentence, written in points, as ``detail``), max turns is ``rounds``, any other guardrail ``execution_control``.
    None for anything that is not a guardrail stop (2026-11-18: a helper stopped by its run budget reached its desk
    with no cause, so the stop read as a generic failure)."""
    kind = str(getattr(exc, "kind", "") or "")
    if exc is None or not kind.startswith("guardrail."):
        return None
    limit, observed = getattr(exc, "limit", None), getattr(exc, "observed", None)
    allowed = float(limit) if isinstance(limit, int | float) else None
    used = float(observed) if isinstance(observed, int | float) else None
    detail = str(getattr(exc, "message", "") or exc)
    if kind == "guardrail.max_cost_run" or kind.startswith("guardrail.cap_"):
        label = "Max cost per run" if kind == "guardrail.max_cost_run" else None
        return RunStopCause(kind="cost", allowed=allowed, used=used, unit="usd", label=label, detail=detail)
    if kind == "guardrail.max_turns":
        return RunStopCause(kind="rounds", allowed=allowed, used=used, unit="rounds", detail=detail)
    return RunStopCause(kind="execution_control", detail=detail)


#: The host's guardrail sentences begin so (``automation_guardrails.GUARDRAIL_MESSAGE_PREFIXES``): already written for
#: a person, in points — relayed as written, never re-worded into dollars.
_PERSON_SENTENCE_PREFIXES = ("Stopped: limit", "Refused:", "Held:")


def _num(value: float | None) -> str:
    return f"{value:g}" if value is not None else "?"


def describe_stop_cause(cause: RunStopCause) -> str:
    """The one sentence a caller relays for a stop, naming the exact limit and its numbers.

    Rounds are never worded as time: each kind has its own noun and unit.
    """
    owner = f" ({cause.label})" if cause.label else ""
    if cause.kind == "rounds":
        return f"Stopped at its round limit{owner}: used {_num(cause.used)} of {_num(cause.allowed)} rounds, not finished."
    if cause.kind == "time":
        return f"Stopped at its time limit{owner}: ran {_num(cause.used)} of {_num(cause.allowed)} seconds, not finished."
    if cause.kind == "cost":
        if cause.detail.startswith(_PERSON_SENTENCE_PREFIXES):
            return cause.detail
        if cause.allowed is None and cause.used is None:
            return f"Stopped at its spending limit{owner}, not finished."
        return f"Stopped at its spending limit{owner}: used {_num(cause.used)} of {_num(cause.allowed)} usd, not finished."
    if cause.kind == "cancelled":
        return f"Stopped before it finished: {cause.detail or 'the run was cancelled'}."
    return f"Stopped by a host control before it finished: {cause.detail or 'a limit was reached'}."


__all__ = [
    "STOP_CAUSE_KEY",
    "describe_stop_cause",
    "RunStopCause",
    "StopCauseKind",
    "cost_cause",
    "rounds_cause",
    "stop_cause_from_exception",
    "stop_cause_from_metadata",
    "time_cause",
]
