"""Shared helpers for the per-verb step handlers."""

from __future__ import annotations

from typing import Any

from aigie.decision.steps import StepContext, StepOutcome, StepStatus
from aigie.rewind.protocol import Corrective, RewindOutcome, RewindStatus

_PROMPT_KEYS = ("prompt", "message", "context", "guidance")

# Verbs that take no meaningful params advertise an opaque object.
OPAQUE_PARAM_SCHEMA: dict[str, Any] = {"type": "object"}

# Prompt-carrying verbs accept any of the corrective-prompt keys `first_prompt`
# reads, plus opaque extras. Derived from _PROMPT_KEYS so the advertised keys
# and the consumed keys can't drift.
PROMPT_PARAM_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {key: {"type": "string"} for key in _PROMPT_KEYS},
}


def outcome(step: Any, status: StepStatus, reason: str = "", observed: Any = None) -> StepOutcome:
    return StepOutcome(step.step_id, step.verb, status, reason, observed)


def _map_rewind(step: Any, result: RewindOutcome) -> StepOutcome:
    if result.status == RewindStatus.OK:
        return outcome(step, StepStatus.APPLIED, observed=result.result)
    if result.status == RewindStatus.FAILED:
        return outcome(step, StepStatus.FAILED, result.reason or "rewind_failed")
    if result.status == RewindStatus.SKIPPED:
        return outcome(step, StepStatus.SKIPPED, result.reason or "rewind_skipped")
    return outcome(step, StepStatus.SKIPPED, "no_handle")


async def rewind(step: Any, ctx: StepContext, corrective: Corrective | None) -> StepOutcome:
    if ctx.rewind_coordinator is None:
        return outcome(step, StepStatus.SKIPPED, "no_coordinator")
    coordinator = ctx.rewind_coordinator
    result = await coordinator.rewind(ctx.trace_id, ctx.span_id, corrective)
    if result.status == RewindStatus.NOT_FOUND:
        parent_id = getattr(ctx.span, "parent_id", "")
        if parent_id:
            result = await coordinator.rewind(ctx.trace_id, str(parent_id), corrective)
    return _map_rewind(step, result)


def first_prompt(params: dict[str, Any]) -> str | None:
    for key in _PROMPT_KEYS:
        if params.get(key):
            return str(params[key])
    return None
