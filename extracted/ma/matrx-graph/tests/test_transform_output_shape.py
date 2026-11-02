"""data.transform output shape — the vestigial ``result: null`` regression.

A dict expression result is spread flat onto the output root. Before the fix,
the declared ``result`` field still serialized as ``null`` alongside the real
keys, so:

1.  TWO transforms broadcasting into one join both delivered ``result`` and
    the §3.7 multi-writer guard parked the run ERRORED — for a key neither
    author ever wrote (found live 2026-08-08, "Certified Blurb Pipeline").
2.  The studio's connection picker surfaced a useless "Result — (null)"
    option for every dict-shaped transform.

Contract: dict result → flat keys ONLY; non-dict result (including None) →
``{"result": <value>}`` exactly as before.
"""

from __future__ import annotations

from typing import Any, ClassVar

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.nodes.data.transform import TransformOutput
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context


def test_dict_result_spreads_flat_without_vestigial_result_key() -> None:
    dumped = TransformOutput(match={"topic": "espresso"}).model_dump(mode="json")
    assert dumped == {"match": {"topic": "espresso"}}


def test_scalar_result_keeps_result_key() -> None:
    assert TransformOutput(result=43).model_dump(mode="json") == {"result": 43}


def test_none_result_alone_is_preserved() -> None:
    # A non-dict expression legitimately evaluating to None still reports it.
    assert TransformOutput().model_dump(mode="json") == {"result": None}


def test_authored_result_key_in_dict_wins() -> None:
    dumped = TransformOutput(result=7, extra="x").model_dump(mode="json")
    assert dumped == {"result": 7, "extra": "x"}


class _SinkInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class _SinkOutput(BaseModel):
    model_config = ConfigDict(extra="allow")


class _SinkConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Sink:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.sink",
        category=NodeCategory.DATA,
        display_name="Sink",
        description="Records routed inputs.",
        input_schema=_SinkInput,
        output_schema=_SinkOutput,
        config_schema=_SinkConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def execute(
        self,
        _ctx: NodeExecutionContext,
        inputs: _SinkInput,
        _config: _SinkConfig,
    ) -> NodeResult[_SinkOutput]:
        dump = inputs.model_dump(mode="json")
        self.calls.append(dump)
        return success(_SinkOutput(**dump))


async def test_two_dict_transforms_broadcast_into_one_join_no_result_collision() -> None:
    """The exact live failure: two pass-through transform edges into one node
    must not trip the multi-writer guard on the vestigial ``result`` key."""
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    sink = _Sink()
    registry.register(sink, overwrite=True)

    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "t1",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": "{'match': {'topic': 'espresso'}}"}},
                },
                {
                    "id": "t2",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 200},
                    "data": {"config": {"expression": "{'values': {'quantity': 6}}"}},
                },
                {
                    "id": "j",
                    "type": "test.sink",
                    "position": {"x": 300, "y": 100},
                    "data": {"config": {}},
                },
            ],
            "edges": [
                {"id": "e1", "source": "t1", "target": "j", "data": {}},
                {"id": "e2", "source": "t2", "target": "j", "data": {}},
            ],
        }
    )
    graph = compile_graph(definition, registry=registry)
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        registry=registry,
    )

    result = await scheduler.run(run_id="transform-no-result-collision")

    assert result.status is RunStatus.COMPLETED, f"run parked: {result.status}"
    assert len(sink.calls) == 1
    assert sink.calls[0] == {"match": {"topic": "espresso"}, "values": {"quantity": 6}}


# ---------------------------------------------------------------------------
# DECLARED vs EMITTED — the shape the platform READS must be the shape the
# runtime SENDS.
#
# The second live failure (run 6511ffd1, 2026-09-12): the node declared
# ``result`` (the registered TransformOutput), the runtime emitted the dict's
# keys flat, and the Conductor — which can only read declarations — wired
# ``variables <- result``. EdgeRoutingError, KeyError: 'result'. The fix makes
# the COMPILER resolve the expression into the node's effective_output_schema;
# these tests hold that schema to what the engine really emits, by running it.
# ---------------------------------------------------------------------------

import pytest
from matrx_graph.nodes.data.transform import expression_output_shape


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        # The live expression, verbatim.
        (
            "{'situation': inputs['situation'], 'child_age': inputs['child_age'], "
            "'canon': inputs['canon']}",
            ("situation", "child_age", "canon"),
        ),
        ("{'canon': 1}", ("canon",)),
        ("{'result': 1, 'other': 2}", ("result", "other")),
        ("{}", ("result",)),
        ("inputs['value'] * 2", ("result",)),
        ("'a string'", ("result",)),
        ("[1, 2, 3]", ("result",)),
        ("inputs['a'] == inputs['b']", ("result",)),
    ],
)
def test_expression_output_shape_is_resolved(expression: str, expected: tuple[str, ...]) -> None:
    shape = expression_output_shape(expression)
    assert shape is not None, f"{expression!r} should be statically knowable"
    assert shape[0] == expected


@pytest.mark.parametrize(
    "expression",
    [
        "inputs['inputs']",  # the data.assert un-nest — may or may not be a dict
        "{**inputs}",  # spread: unknown keys
        "{k: v for k, v in inputs.items()}",  # comprehension: unknown keys
        "inputs['a'] | inputs['b']",  # dict merge: unknown keys
        "inputs['flag'] and inputs['payload']",  # could be either operand
        "{inputs['key']: 1}",  # computed key
        "this is not python(",
    ],
)
def test_unknowable_expressions_declare_nothing_rather_than_lying(expression: str) -> None:
    """The honest answer for a shape nobody can know before the run is None —
    NOT a guess. The joint check turns None into a named 'unverified joint'."""
    assert expression_output_shape(expression) is None


@pytest.mark.parametrize(
    ("expression", "run_inputs"),
    [
        (
            "{'situation': inputs['situation'], 'child_age': inputs['child_age'], "
            "'canon': inputs['canon']}",
            {"situation": "bedtime meltdown", "child_age": 4, "canon": "montessori"},
        ),
        ("{'only': inputs['situation']}", {"situation": "x"}),
        ("inputs['child_age'] * 2", {"child_age": 3}),
        ("'literal'", {}),
        ("{}", {}),
    ],
)
async def test_declared_output_schema_equals_what_the_node_really_emits(
    expression: str, run_inputs: dict[str, Any]
) -> None:
    """THE PARITY GUARD — real compile, real scheduler, real executor.

    Whatever the compiled ``effective_output_schema`` declares is exactly the
    key set the running node delivers downstream. No mocks: the sink records
    what the engine actually spread into it.
    """
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    sink = _Sink()
    registry.register(sink, overwrite=True)

    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "t",
                    "type": "data.transform",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"expression": expression}},
                },
                {
                    "id": "j",
                    "type": "test.sink",
                    "position": {"x": 300, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [{"id": "e1", "source": "t", "target": "j", "data": {}}],
        }
    )
    graph = compile_graph(definition, registry=registry)

    schema = graph.nodes["t"].effective_output_schema
    assert schema is not None, (
        f"{expression!r} is statically knowable but the compiler declared "
        "nothing — every reader (the Conductor, the studio picker, the joint "
        "check) then falls back to the WRONG 'result' declaration."
    )
    declared = set(schema["properties"])

    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )
    result = await scheduler.run(run_id=f"parity-{abs(hash(expression))}", inputs=run_inputs)
    assert result.status is RunStatus.COMPLETED, f"run parked: {result.status}"

    emitted = set(sink.calls[0])
    assert emitted == declared, (
        f"DECLARED {sorted(declared)} but EMITTED {sorted(emitted)} for "
        f"expression {expression!r} — a reader that trusts the declaration "
        "wires an edge the run cannot resolve (run 6511ffd1)."
    )
