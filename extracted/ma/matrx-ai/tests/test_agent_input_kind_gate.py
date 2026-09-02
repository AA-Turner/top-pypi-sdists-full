"""THE PAYOFF — a workflow node refuses bad input BEFORE the paid model call.

This is what binding an agent's inputs to a kind is FOR (§10d-C). The chain,
end to end, on a real agent:

    agent.definition.variable_definitions   (what the author declared)
      → variable_kinds.variable_definitions_to_kind_fields
      → agent_input_json_schema             (the registered contract)
      → node `data.input_kind`              (a workflow step declares it)
      → the scheduler's fatal input gate    (refuses before execute)

The agent is REAL: "Education: Language Practice Designer", whose declarations
are copied verbatim below — a closed option set (`difficulty`), a bounded
number (`count`, 3–20, step 1), and free text. Before this bridge existed,
NOTHING in that declaration reached anything that could enforce it: a run with
`difficulty="Fluent"` or `count=50` went straight to the provider, was paid
for, and came back wrong.

The forcing function is the call counter: every refusal asserts the node's
executor ran ZERO times. A test that only checked "an error was raised" would
pass just as happily if the model had been called first and the money spent.
"""

from __future__ import annotations

import time
from typing import Any, ClassVar

import pytest
from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph import kinds as kinds_mod
from matrx_graph.kinds import KindEntry, invalidate_kind_catalog_cache
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict

from matrx_ai.agents.variable_kinds import (
    agent_input_json_schema,
    coerce_variables_to_instance,
    variable_definitions_to_kind_fields,
)

# Verbatim from agent.definition (live registry, read-only, 2026-08-23).
LANGUAGE_PRACTICE_VARIABLES: list[dict[str, Any]] = [
    {
        "name": "focus",
        "helpText": "The target language plus what to practice.",
        "defaultValue": "",
    },
    {
        "name": "difficulty",
        "helpText": "The level of rigor for this session.",
        "defaultValue": "Beginner",
        "customComponent": {
            "type": "radio",
            "options": [
                "Beginner",
                "Intermediate",
                "High School",
                "Undergraduate",
                "Advanced",
            ],
            "allowOther": False,
        },
    },
    {
        "name": "count",
        "helpText": "How many spoken prompts to generate for this session.",
        "defaultValue": "8",
        "customComponent": {"max": 20, "min": 3, "step": 1, "type": "number"},
    },
    {
        "name": "study_material",
        "helpText": "Optional — the student's own vocabulary list or notes.",
        "defaultValue": "",
    },
]

AGENT_INPUT_KIND = "agent_input_focus_difficulty_count_study_material"


# --- the node that would spend the money ------------------------------------


class _Inputs(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Output(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prompts: int = 0


class _Config(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _PaidAgentNode:
    """Stands in for `ai.agent.start` — the step that calls a provider."""

    calls: ClassVar[int] = 0

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.paid_agent",
        category=NodeCategory.AGENT,
        display_name="Run the agent (paid)",
        description="Every execution here is a provider call that costs money.",
        input_schema=_Inputs,
        output_schema=_Output,
        config_schema=_Config,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
    )

    async def execute(
        self, _ctx: NodeExecutionContext, _inputs: _Inputs, _config: _Config
    ) -> NodeResult[_Output]:
        type(self).calls += 1
        return success(_Output(prompts=8))


@pytest.fixture(autouse=True)
def _clean():
    _PaidAgentNode.calls = 0
    invalidate_kind_catalog_cache()
    yield
    invalidate_kind_catalog_cache()


def _seed_agent_input_kind() -> dict[str, Any]:
    """Register the REAL derived contract in the catalog's process cache."""
    conversion = variable_definitions_to_kind_fields(LANGUAGE_PRACTICE_VARIABLES)
    schema = agent_input_json_schema(conversion.fields)
    kinds_mod._cache[AGENT_INPUT_KIND] = (
        time.monotonic(),
        KindEntry(
            slug=AGENT_INPUT_KIND, version=1, label="Language practice", json_schema=schema
        ),
    )
    return schema


def _registry() -> NodeRegistry:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_PaidAgentNode(), overwrite=True)
    return registry


def _definition(inputs: dict[str, Any]) -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "run_agent",
                    "type": "test.paid_agent",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {},
                        # The whole point: the step declares WHAT IT FEEDS the agent.
                        "input_kind": AGENT_INPUT_KIND,
                        "inputs": inputs,
                    },
                }
            ],
            "edges": [],
        }
    )


async def _run(inputs: dict[str, Any], run_id: str):
    from matrx_connect.context.app_context import AppContext

    class _Emitter:
        async def send_chunk(self, text: str) -> None: ...
        async def send_data(self, payload: Any) -> None: ...
        async def send_init(self, payload: Any) -> None: ...
        async def send_completion(self, payload: Any) -> None: ...
        async def send_error(self, *args: Any, **kwargs: Any) -> None: ...
        async def send_end(self) -> None: ...
        async def send_phase(self, phase: Any) -> None: ...

    registry = _registry()
    graph = compile_graph(_definition(inputs), registry=registry)
    context = AppContext(
        emitter=_Emitter(),
        user_id="test-user",
        is_authenticated=True,
        conversation_id="test-conv",
        request_id="test-req",
    )
    scheduler = Scheduler(graph, MemoryCheckpointer(), context, registry=registry)
    return await scheduler.run(run_id=run_id)


# --- the contract the bridge derives ----------------------------------------


def test_the_declaration_becomes_an_enforceable_contract():
    schema = _seed_agent_input_kind()
    assert schema["properties"]["difficulty"] == {
        "type": "string",
        "enum": [
            "Beginner",
            "Intermediate",
            "High School",
            "Undergraduate",
            "Advanced",
        ],
        "description": "The level of rigor for this session.",
        "default": "Beginner",
    }
    assert schema["properties"]["count"]["minimum"] == 3
    assert schema["properties"]["count"]["maximum"] == 20
    assert schema["properties"]["count"]["multipleOf"] == 1


# --- the gate ---------------------------------------------------------------


async def test_a_value_outside_the_declared_option_set_never_reaches_the_provider():
    _seed_agent_input_kind()
    result = await _run(
        {"focus": "Spanish — greetings", "difficulty": "Fluent", "count": 8},
        run_id="gate-enum",
    )
    assert result.status is RunStatus.ERRORED
    assert _PaidAgentNode.calls == 0, (
        "the node RAN — the input gate let a value outside the agent's own "
        "declared option set through, and the provider call was paid for"
    )


async def test_a_number_outside_the_declared_bounds_never_reaches_the_provider():
    _seed_agent_input_kind()
    result = await _run(
        {"focus": "Spanish — greetings", "difficulty": "Beginner", "count": 50},
        run_id="gate-bounds",
    )
    assert result.status is RunStatus.ERRORED
    assert _PaidAgentNode.calls == 0


async def test_conforming_input_runs(monkeypatch):
    _seed_agent_input_kind()
    result = await _run(
        {"focus": "Spanish — greetings", "difficulty": "Beginner", "count": 8},
        run_id="gate-ok",
    )
    assert result.status is RunStatus.COMPLETED, result.error
    assert _PaidAgentNode.calls == 1


# --- and the string-space payload the chat path actually sends --------------


async def test_a_real_string_space_payload_conforms_once_coerced():
    """The runtime carries variable values as STRINGS.

    A live payload says `count: "8"`, which is not a number — so the coercion
    layer is not a convenience, it is the difference between a gate that works
    and a gate that rejects every genuine run.
    """
    _seed_agent_input_kind()
    conversion = variable_definitions_to_kind_fields(LANGUAGE_PRACTICE_VARIABLES)
    live_payload = {
        "focus": "Spanish — greetings",
        "difficulty": "Beginner",
        "count": "8",
        "__agent_user_input__": "start me off easy",
    }

    raw = await _run(live_payload, run_id="gate-raw-strings")
    assert raw.status is RunStatus.ERRORED
    assert _PaidAgentNode.calls == 0

    coerced = coerce_variables_to_instance(conversion.fields, live_payload)
    assert coerced.coercion_errors == {}
    # The human's free text is the envelope's, never an input-contract field.
    assert coerced.undeclared == []
    assert coerced.instance["count"] == 8

    ok = await _run(coerced.instance, run_id="gate-coerced")
    assert ok.status is RunStatus.COMPLETED, ok.error
    assert _PaidAgentNode.calls == 1
