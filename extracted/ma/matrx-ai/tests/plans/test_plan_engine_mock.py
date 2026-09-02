"""End-to-end: a compiled AgentPlan runs on the REAL matrx-graph scheduler.

Every agent node carries a mock_response (validated against
AiExecutionResult), so the whole flow — assembler expressions, dependency
routing, fan-out via control.map payload_template, channel fan-in via
output_channel, when-conditionals, empty-list pads — executes with zero
LLM calls and zero DB access.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from matrx_ai.graph_nodes import register_with_graph
from matrx_ai.plans import AgentPlan, compile_plan
from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.executor.registry import default_registry

_A1 = "1fd0cb1f-5b95-49f0-a7f8-79308dc50f58"
_A2 = "9f8eab67-96e4-4a08-9563-7a982f920527"

_CARDS = [
    {"question": "Q1", "answer": "A1"},
    {"question": "Q2", "answer": "A2"},
    {"question": "Q3", "answer": "A3"},
]


@dataclass
class _FakeEmitter:
    events: list[tuple[str, Any]] = field(default_factory=list)

    async def send_chunk(self, text: str) -> None:
        self.events.append(("chunk", text))

    async def send_data(self, payload: Any) -> None:
        self.events.append(("data", payload))

    async def send_error(self, *args: Any, **kwargs: Any) -> None:
        self.events.append(("error", {"args": args, "kwargs": kwargs}))

    async def send_end(self) -> None:
        self.events.append(("end", None))


def _app_context() -> Any:
    from matrx_connect.context.app_context import AppContext

    return AppContext(
        emitter=_FakeEmitter(),
        user_id="test-user",
        is_authenticated=True,
        conversation_id="test-conv",
        request_id="test-req",
    )


def _mock_result(final_text: str, structured: dict | None = None) -> dict[str, Any]:
    return {
        "conversation_id": "conv-mock",
        "request_id": "req-mock",
        "iterations": 1,
        "final_text": final_text,
        "structured_output": structured,
    }


def _stamp_mocks(definition: Definition, mocks: dict[str, dict[str, Any]]) -> None:
    for node in definition.nodes:
        if node.id in mocks:
            node.data["mock_response"] = {"enabled": True, "output": mocks[node.id]}


async def _run(definition: Definition, run_id: str) -> Any:
    register_builtin_nodes(default_registry(), overwrite=True)
    register_with_graph()
    graph = compile_graph(definition)
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        _app_context(),
        registry=default_registry(),
    )
    return await scheduler.run(run_id=run_id)


def _flashcard_plan(cards_when: str | None = None) -> AgentPlan:
    steps: list[dict[str, Any]] = [
        {
            "step": 1,
            "agent_id": _A1,
            "purpose": "generate cards",
            "inputs": {"user_input": "make cards", "topic": "$inputs.topic"},
        },
        {
            "step": 2,
            "agent_id": _A2,
            "purpose": "enrich each card",
            "for_each": "$steps.1.output.structured_output.cards",
            "inputs": {"front": "$item.question", "back": "$item.answer"},
        },
        {
            "step": 3,
            "agent_id": _A1,
            "purpose": "summarize",
            "inputs": {
                "enriched_count": "$steps.2.output.count",
                "source": "$steps.1.output.final_text",
            },
        },
        {
            "step": 4,
            "agent_id": _A1,
            "purpose": "conditional extra",
            "depends_on": [1],
            "when": cards_when or "$steps.1.output.iterations > 99",
        },
    ]
    return AgentPlan.model_validate(
        {
            "name": "flashcards",
            "reasoning": "seed, then parallel enrich, then join; step 4 conditional",
            "inputs": {"topic": "Chemistry"},
            "steps": steps,
        }
    )


async def test_full_plan_runs_with_mocked_agents():
    definition = compile_plan(_flashcard_plan())
    _stamp_mocks(
        definition,
        {
            "step_1": _mock_result("made 3 cards", {"cards": _CARDS}),
            "step_2": _mock_result("enriched"),
            "step_3": _mock_result("summary done"),
            "step_4": _mock_result("should never run"),
        },
    )
    result = await _run(definition, "plan-e2e-1")
    assert result.status is RunStatus.COMPLETED

    # Cross-step structured_output ref resolved: the fan-out assembler
    # received the exact card list from step 1's mocked payload.
    assert result.last_outputs["step_2_args"]["items"] == _CARDS

    # Fan-in: all three parallel worker outputs reached the gather.
    gathered = result.last_outputs["step_2_gather"]
    assert gathered["count"] == 3
    assert [v["final_text"] for v in gathered["values"]] == ["enriched"] * 3

    # The join assembler resolved refs from BOTH branches (unequal depths —
    # this is the layer-padding proof at runtime).
    join_inputs = result.last_outputs["step_3_args"]
    assert join_inputs["variables"] == {"enriched_count": 3, "source": "made 3 cards"}
    assert result.last_outputs["step_3"]["final_text"] == "summary done"

    # when-false: step 4 never fired; the run still completed.
    assert "step_4" not in result.last_outputs
    assert "step_4_args" not in result.last_outputs

    # Result contract: metadata result_map points at nodes that exist in
    # last_outputs (except skipped ones).
    result_map = definition.metadata["agent_plan"]["result_map"]
    assert result.last_outputs[result_map["1"]["node_id"]]["final_text"] == "made 3 cards"
    assert result.last_outputs[result_map["2"]["node_id"]]["count"] == 3


async def test_when_true_branch_executes():
    definition = compile_plan(_flashcard_plan(cards_when="$steps.1.output.iterations < 99"))
    _stamp_mocks(
        definition,
        {
            "step_1": _mock_result("made 3 cards", {"cards": _CARDS}),
            "step_2": _mock_result("enriched"),
            "step_3": _mock_result("summary done"),
            "step_4": _mock_result("conditional ran"),
        },
    )
    result = await _run(definition, "plan-e2e-2")
    assert result.status is RunStatus.COMPLETED
    assert result.last_outputs["step_4"]["final_text"] == "conditional ran"


async def test_empty_fan_out_completes_with_zero_results():
    definition = compile_plan(_flashcard_plan())
    _stamp_mocks(
        definition,
        {
            "step_1": _mock_result("no cards this time", {"cards": []}),
            "step_2": _mock_result("enriched"),
            "step_3": _mock_result("summary done"),
            "step_4": _mock_result("never"),
        },
    )
    result = await _run(definition, "plan-e2e-3")
    assert result.status is RunStatus.COMPLETED

    gathered = result.last_outputs["step_2_gather"]
    assert gathered["count"] == 0
    assert gathered["values"] == []
    # No worker ever fired…
    assert "step_2" not in result.last_outputs
    # …but the join still ran, seeing count == 0.
    assert result.last_outputs["step_3_args"]["variables"]["enriched_count"] == 0
