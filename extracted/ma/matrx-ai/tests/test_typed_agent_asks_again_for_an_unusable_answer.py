"""Run Typed Agent asks once more when the model's answer cannot be used.

Live 2026-10-28, Group offerings (workflow 5cb9bfc6) runs 48191b96 and ed375042: one Claude Haiku 5.5
call per run answered ``{"__kind":"brand_offering_tree","groups":[{"__kind":"","keys":[],"label":"Placeholder"}]}``.
The parse funnel rightly refused it as degenerate ("the run must be retried"), the step had ONE attempt,
and the whole run errored. These tests pin: (1) that answer becomes ``structured_output_invalid``;
(2) the registered step retries exactly that code once, never a truncation; (3) the engine really runs the
second attempt with the step's own policy and the run completes.

  uv run pytest packages/matrx-ai/tests/test_typed_agent_asks_again_for_an_unusable_answer.py -v
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
)
from matrx_graph.executor._retry import should_retry
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import Failure, success
from pydantic import BaseModel, ConfigDict

from matrx_ai.graph_nodes import agent_produce_action
from matrx_ai.graph_nodes.shared import normalize_completed_result

# The live agent's declared output (agent a5b44611 "Brand offerings: arrange into groups").
_TREE = {
    "name": "brand_offering_tree",
    "schema": {
        "type": "object",
        "$defs": {
            "BrandOfferingGroup": {
                "type": "object",
                "required": ["label"],
                "properties": {
                    "keys": {"type": "array", "items": {"type": "string"}},
                    "label": {"type": "string"},
                    "__kind": {"type": "string", "default": ""},
                },
                "additionalProperties": False,
            }
        },
        "properties": {
            "__kind": {"type": "string", "const": "brand_offering_tree"},
            "groups": {"type": "array", "items": {"$ref": "#/$defs/BrandOfferingGroup"}},
        },
        "additionalProperties": False,
        "required": ["__kind"],
    },
}
_LIVE_PLACEHOLDER = (
    '{"__kind":"brand_offering_tree","groups":[{"__kind":"","keys":[],"label":"Placeholder"}]}'
)


def _completed(text: str) -> SimpleNamespace:
    request = SimpleNamespace(
        config=SimpleNamespace(
            messages=[], response_format={"type": "json_schema", "json_schema": _TREE}
        ),
        conversation_id="conv-1",
        request_id="req-1",
    )
    return SimpleNamespace(
        request=request,
        final_response=SimpleNamespace(messages=None, text=text),
        messages=[],
        total_usage=None,
        metadata={"status": "complete"},
        iterations=1,
        timing_stats={},
        tool_call_stats={},
    )


def _spec_policy():
    spec = agent_produce_action.agent_produce._matrx_action_spec.node_spec  # type: ignore[attr-defined]
    return spec.retry


def test_the_live_placeholder_answer_is_an_unusable_answer() -> None:
    result = normalize_completed_result(_completed(_LIVE_PLACEHOLDER))
    assert isinstance(result, Failure)
    assert result.error.code == "structured_output_invalid"


def test_run_typed_agent_asks_once_more_for_an_unusable_answer_and_never_for_a_cut_off_one() -> (
    None
):
    policy = _spec_policy()
    assert should_retry(policy, 1, "structured_output_invalid"), (
        "Run Typed Agent must ask once more when the answer could not be parsed and validated"
    )
    assert should_retry(policy, 1, "structured_output_empty")
    assert not should_retry(policy, 2, "structured_output_invalid"), "once more, not forever"
    assert not should_retry(policy, 1, "output_truncated"), (
        "the same ceiling cuts the same answer again"
    )
    assert not should_retry(policy, 1, "ai_turn_failed")


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Out(BaseModel):
    model_config = ConfigDict(extra="allow")


class _FlakyTypedStep:
    """A step with Run Typed Agent's own retry policy whose first answer is the live placeholder."""

    def __init__(self) -> None:
        self.calls = 0
        self.spec = NodeSpec(
            type="test.flaky_typed_step",
            category=NodeCategory.AGENT,
            display_name="flaky typed step",
            description="first answer unusable",
            input_schema=_In,
            output_schema=_Out,
            config_schema=_In,
            handles=(
                HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
                HandleSpec(id="out", direction=HandleDirection.OUTPUT),
            ),
            determinism=ActionTier.NON_DETERMINISTIC,
            retry=_spec_policy(),
        )

    async def execute(self, ctx: Any, inputs: _In, config: Any):
        self.calls += 1
        if self.calls == 1:
            return normalize_completed_result(_completed(_LIVE_PLACEHOLDER))
        return success(_Out(groups=[{"label": "Paddles", "keys": ["a"]}]))


async def test_the_engine_asks_again_and_the_run_completes() -> None:
    from matrx_connect.context.app_context import AppContext
    from matrx_graph import register_builtin_nodes

    class _Emitter:
        async def send_chunk(self, text: str) -> None: ...
        async def send_data(self, payload: Any) -> None: ...
        async def send_init(self, payload: Any) -> None: ...
        async def send_completion(self, payload: Any) -> None: ...
        async def send_error(self, *args: Any, **kwargs: Any) -> None: ...
        async def send_end(self) -> None: ...
        async def send_phase(self, phase: Any) -> None: ...

    node = _FlakyTypedStep()
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(node, overwrite=True)
    graph = compile_graph(
        Definition.model_validate(
            {
                "nodes": [
                    {
                        "id": "a",
                        "type": node.spec.node_type,
                        "position": {"x": 0, "y": 0},
                        "data": {"config": {}},
                    }
                ],
                "edges": [],
            }
        ),
        registry=reg,
    )
    context = AppContext(
        emitter=_Emitter(),
        user_id="test-user",
        is_authenticated=True,
        conversation_id="c",
        request_id="r",
    )
    result = await Scheduler(graph, MemoryCheckpointer(), context, registry=reg).run(
        run_id="typed-agent-asks-again"
    )
    assert node.calls == 2
    assert result.status is RunStatus.COMPLETED
