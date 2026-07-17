"""Handler for report-only verbs (``block``, ``escalate``)."""

from __future__ import annotations

from typing import Any

from aigie.decision.handlers._common import OPAQUE_PARAM_SCHEMA, outcome
from aigie.decision.steps import StepContext, StepOutcome, StepStatus, VerbBinding, VerbSpec


class ReportOnlyHandler:
    async def invoke(self, step: Any, _ctx: StepContext) -> StepOutcome:
        return outcome(step, StepStatus.SKIPPED, "report_only")


_handler = ReportOnlyHandler()

BINDINGS = [
    VerbBinding(
        VerbSpec(
            "block",
            "Block the offending action; report only (no runtime change).",
            OPAQUE_PARAM_SCHEMA,
        ),
        _handler,
    ),
    VerbBinding(
        VerbSpec("escalate", "Escalate to a human; report only.", OPAQUE_PARAM_SCHEMA),
        _handler,
    ),
]
