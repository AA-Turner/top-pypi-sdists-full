"""The think/analyze reasoning tools must carry the plan-step id when deep
planning is active. agno builds their schema from a fixed entrypoint
signature, so the SDK injects the field directly and freezes the schema; the
field is stripped from the call args before agno dispatches the entrypoint.
"""

from __future__ import annotations

from xpander_sdk.modules.backend.frameworks.agno import (
    _inject_plan_task_id_into_reasoning_tools,
)
from xpander_sdk.modules.backend.utils.tool_call_events import (
    TOOL_CALL_PLAN_TASK_ID,
    extract_plan_task_id,
)


def _toolkit():
    from agno.tools.reasoning import ReasoningTools

    return ReasoningTools(enable_think=True, enable_analyze=True)


def test_inject_adds_required_plan_task_id_to_think_and_analyze():
    toolkit = _toolkit()
    _inject_plan_task_id_into_reasoning_tools(toolkit)

    for name, fn in toolkit.functions.items():
        props = fn.parameters["properties"]
        assert TOOL_CALL_PLAN_TASK_ID in props, name
        assert TOOL_CALL_PLAN_TASK_ID in fn.parameters["required"], name
        # The original reasoning fields are preserved.
        assert "title" in props, name


def test_inject_survives_agno_reprocessing():
    toolkit = _toolkit()
    _inject_plan_task_id_into_reasoning_tools(toolkit)
    fn = toolkit.functions["think"]
    # agno may re-derive the schema; skip_entrypoint_processing keeps our field.
    fn.process_entrypoint()
    assert TOOL_CALL_PLAN_TASK_ID in fn.parameters["properties"]


def test_extract_plan_task_id_reads_reasoning_top_level_arg():
    # Reasoning tools surface the id as a top-level call argument.
    args = {"title": "t", "thought": "x", TOOL_CALL_PLAN_TASK_ID: "step-9"}
    assert extract_plan_task_id(args) == "step-9"
