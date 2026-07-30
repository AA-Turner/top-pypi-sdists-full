"""Handler for the ``correct_tool_call`` verb."""

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
    span_metadata,
)
from aigie.decision.tool_catalog import catalog_for_span, find_tool, required_args_for
from aigie.rewind.protocol import Corrective, ToolCallOverride

_CORRECT_TOOL_CALL_PARAM_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "target_tool": {"type": "string"},
        "args": {"type": "object"},
        "arg_mapping": {"type": "object", "additionalProperties": {"type": "string"}},
    },
    "required": ["target_tool"],
}


def _failed_call_identity(span: Any) -> tuple[str | None, str | None]:
    """Identify the call that failed: its tool_call_id, and the tool that ran it.

    Only a tool span's ``name`` is a tool name — on a chain/LLM span it is a node
    name, which would mis-target a sibling call.
    """
    call_id = span_metadata(span).get("tool_call_id")
    is_tool_span = getattr(span, "type", "") == "tool"
    source_tool = getattr(span, "name", "") if is_tool_span else ""
    return (str(call_id) if call_id else None, str(source_tool) or None)


class CorrectToolCallHandler:
    async def invoke(self, step: Any, ctx: StepContext) -> StepOutcome:
        params = params_to_dict(step)
        target = params.get("target_tool")
        if not isinstance(target, str) or not target:
            return outcome(step, StepStatus.SKIPPED, "no_target_tool")
        catalog = catalog_for_span(ctx.span, ctx.trace_id)
        tool = find_tool(catalog, target) if catalog is not None else None
        if tool is None:
            observed = {"catalog": "unresolved"} if catalog is None else None
            return outcome(step, StepStatus.SKIPPED, "no_target_tool", observed)
        args = params.get("args")
        mapping = params.get("arg_mapping")
        source_call_id, source_tool = _failed_call_identity(ctx.span)
        override = ToolCallOverride(
            name=target,
            args=args if isinstance(args, dict) else None,
            arg_mapping=mapping if isinstance(mapping, dict) else None,
            required_args=required_args_for(tool),
            source_call_id=source_call_id,
            source_tool=source_tool,
        )
        if override.args is not None:
            missing = override.missing_required(None)
            if missing:
                return outcome(
                    step, StepStatus.SKIPPED, "unmappable_args", {"unmappable_args": list(missing)}
                )
        return await rewind(step, ctx, Corrective(tool_call=override))


BINDINGS = [
    VerbBinding(
        VerbSpec(
            "correct_tool_call",
            "Re-run the failed step against a different tool from the agent's catalog.",
            _CORRECT_TOOL_CALL_PARAM_SCHEMA,
        ),
        CorrectToolCallHandler(),
    )
]
