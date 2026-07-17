"""Handler for the ``no_op`` verb."""

from __future__ import annotations

from typing import Any

from aigie.decision.handlers._common import OPAQUE_PARAM_SCHEMA, outcome
from aigie.decision.steps import StepContext, StepOutcome, StepStatus, VerbBinding, VerbSpec


class NoOpHandler:
    async def invoke(self, step: Any, _ctx: StepContext) -> StepOutcome:
        return outcome(step, StepStatus.APPLIED)


BINDINGS = [
    VerbBinding(
        VerbSpec("no_op", "Acknowledge the error without taking any action.", OPAQUE_PARAM_SCHEMA),
        NoOpHandler(),
    )
]
