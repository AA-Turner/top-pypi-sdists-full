"""Handler for the prompt-carrying verbs (``repair_request``, ``inject_context``)."""

from __future__ import annotations

from typing import Any

from aigie.decision.handlers._common import (
    PROMPT_PARAM_SCHEMA,
    first_prompt,
    outcome,
    rewind,
)
from aigie.decision.steps import (
    StepContext,
    StepOutcome,
    StepStatus,
    VerbBinding,
    VerbSpec,
    params_to_dict,
)
from aigie.rewind.protocol import Corrective


class PromptHandler:
    async def invoke(self, step: Any, ctx: StepContext) -> StepOutcome:
        params = params_to_dict(step)
        prompt = first_prompt(params)
        if prompt is None:
            return outcome(step, StepStatus.SKIPPED, "no_prompt")
        return await rewind(step, ctx, Corrective(prompt=prompt))


# One shared instance backs both prompt-carrying verbs (identical runtime
# behaviour; only the advertised intent differs).
_handler = PromptHandler()

BINDINGS = [
    VerbBinding(
        VerbSpec(
            "repair_request", "Re-issue the request with a corrective prompt.", PROMPT_PARAM_SCHEMA
        ),
        _handler,
    ),
    VerbBinding(
        VerbSpec(
            "inject_context",
            "Re-run with additional context injected into the prompt.",
            PROMPT_PARAM_SCHEMA,
        ),
        _handler,
    ),
]
