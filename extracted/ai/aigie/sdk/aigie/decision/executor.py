"""Framework-agnostic RemediationStep dispatch.

The verb registry and advertised capabilities are both derived from the
handlers' ``DEFAULT_BINDINGS`` — this module only wires them; verb metadata
(description, param_schema) lives with each handler.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace
from time import perf_counter
from typing import Any

from aigie.decision.handlers import DEFAULT_BINDINGS
from aigie.decision.steps import StepContext, StepHandler, StepOutcome, StepStatus, VerbSpec
from aigie.telemetry._safe import safe_span

_STEP_SPAN_NAME = "kytte.remediation.step"

_DEFAULT_HANDLERS: dict[str, StepHandler] = {b.spec.name: b.handler for b in DEFAULT_BINDINGS}
_DEFAULT_SPECS: dict[str, VerbSpec] = {b.spec.name: b.spec for b in DEFAULT_BINDINGS}


class StepExecutor:
    def __init__(self, handlers: dict[str, StepHandler] | None = None) -> None:
        self._handlers = handlers if handlers is not None else dict(_DEFAULT_HANDLERS)

    def capabilities(self) -> list[VerbSpec]:
        """Advertise verbs this executor can both dispatch (a registered handler)
        and describe (a known spec)."""
        return [_DEFAULT_SPECS[verb] for verb in self._handlers if verb in _DEFAULT_SPECS]

    async def execute(self, steps: Sequence[Any], ctx: StepContext) -> list[StepOutcome]:
        return [await self._run_one(step, ctx) for step in steps]

    async def _run_one(self, step: Any, ctx: StepContext) -> StepOutcome:
        step_id = step.step_id
        verb = step.verb
        handler = self._handlers.get(verb)
        if handler is None:
            return StepOutcome(step_id, verb, StepStatus.SKIPPED, "unknown_verb")
        with safe_span(_STEP_SPAN_NAME) as span:
            started = perf_counter()
            outcome = await self._invoke(handler, step, ctx)
            outcome = replace(outcome, latency_ms=int((perf_counter() - started) * 1000))
            _annotate(span, outcome)
            return outcome

    async def _invoke(self, handler: StepHandler, step: Any, ctx: StepContext) -> StepOutcome:
        try:
            return await handler.invoke(step, ctx)
        except Exception as exc:  # noqa: BLE001 — executor must stay fail-open
            ctx.logger.debug("[AIGIE] step handler raised verb=%s: %s", step.verb, exc)
            return StepOutcome(step.step_id, step.verb, StepStatus.FAILED, str(exc))


def _annotate(span: Any, outcome: StepOutcome) -> None:
    """Tag the per-step span with the attributes the execution UI reads. Cost is
    omitted deliberately — it is attributed platform-side from post-execution
    spans, not known here."""
    span.set_attribute("kytte.step.id", outcome.step_id)
    span.set_attribute("kytte.step.verb", outcome.verb)
    span.set_attribute("kytte.step.status", outcome.status.value)
    span.set_attribute("kytte.step.latency_ms", outcome.latency_ms)
