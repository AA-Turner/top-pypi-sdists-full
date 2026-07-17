"""Handler for the ``reduce_context`` verb."""

from __future__ import annotations

from typing import Any

from aigie.decision.handlers._common import outcome, rewind
from aigie.decision.steps import (
    StepContext,
    StepOutcome,
    StepStatus,
    VerbBinding,
    VerbSpec,
    params_to_dict,
)
from aigie.rewind.protocol import Corrective

_REDUCE_CONTEXT_PARAM_SCHEMA = {
    "type": "object",
    "properties": {"state_patch": {"type": "object", "minProperties": 1}},
    "required": ["state_patch"],
}


class ReduceContextHandler:
    async def invoke(self, step: Any, ctx: StepContext) -> StepOutcome:
        patch = params_to_dict(step).get("state_patch")
        if not isinstance(patch, dict) or not patch:
            return outcome(step, StepStatus.SKIPPED, "no_state_patch")
        return await rewind(step, ctx, Corrective(state_patch=patch))


BINDINGS = [
    VerbBinding(
        VerbSpec(
            "reduce_context",
            "Re-run after patching the agent state to reduce or repair its context.",
            _REDUCE_CONTEXT_PARAM_SCHEMA,
        ),
        ReduceContextHandler(),
    )
]
