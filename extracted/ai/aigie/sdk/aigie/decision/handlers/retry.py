"""Handler for the ``retry`` verb."""

from __future__ import annotations

from typing import Any

from aigie.decision.handlers._common import rewind
from aigie.decision.steps import StepContext, StepOutcome, VerbBinding, VerbSpec

_RETRY_PARAM_SCHEMA = {
    "type": "object",
    "properties": {
        "max_attempts": {"type": "integer", "minimum": 1},
        "backoff": {"type": "object"},
    },
}


class RetryHandler:
    async def invoke(self, step: Any, ctx: StepContext) -> StepOutcome:
        return await rewind(step, ctx, corrective=None)


BINDINGS = [
    VerbBinding(VerbSpec("retry", "Re-run the failed call.", _RETRY_PARAM_SCHEMA), RetryHandler())
]
