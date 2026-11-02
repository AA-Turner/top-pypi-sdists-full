"""A sub-workflow is called by name and answers with its ONE declared result.

P4 of common-docs/systems/workflows/projects/generic-only/PRIMITIVES-TOPIC-AND-MAPS.md:
reusable units of work are separate workflows other workflows call, so improving
one improves every caller. That only holds when a caller (a) names the child by
a stable name instead of a uuid seeded at build time, and (b) reads the child's
declared result instead of reaching into its step ids (``last_outputs``).

Each test fails on the engine before P4: ``SubgraphCallConfig`` had no
``workflow_key``, ``SubgraphCallOutput`` had no ``output``, there was no
``set_result`` patch op / ``declared_result`` rule, a refused call was a generic
``child_run_errored``, a run-once subgraph step reused with no child version,
and a step failure during a cancel parked the run errored.
"""

from __future__ import annotations

from typing import ClassVar

import pytest
from pydantic import BaseModel, ConfigDict, ValidationError

from matrx_graph import (
    Definition,
    DefinitionPatch,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    apply_patch,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.nodes.subgraph.call import (
    SubgraphCallConfig,
    SubgraphCallExecutor,
    SubgraphCallInput,
    SubgraphCallRefused,
    SubgraphTarget,
    set_subgraph_resolver,
    set_subgraph_target_resolver,
)
from matrx_graph.patch import io_declaration_columns
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.deliverables import claim_kind_value, declared_result
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import Failure, NodeResult, Success, success
from tests._fixtures import FakeEmitter, make_app_context


@pytest.fixture(autouse=True)
def _clean_resolvers():
    set_subgraph_resolver(None)
    set_subgraph_target_resolver(None)
    yield
    set_subgraph_resolver(None)
    set_subgraph_target_resolver(None)


# ── calling by name ────────────────────────────────────────────────────────


def test_a_step_names_its_child_by_key_or_by_id_never_both_never_neither():
    assert SubgraphCallConfig(workflow_key="read_material").workflow_key == "read_material"
    assert SubgraphCallConfig(definition_id="d-1").definition_id == "d-1"
    # The tag spelling names the same workflow as the bare name.
    assert SubgraphCallConfig(workflow_key="platform:mandate.run_each").workflow_key == "mandate.run_each"
    with pytest.raises(ValidationError, match="Choose the workflow"):
        SubgraphCallConfig(definition_id="  ")
    with pytest.raises(ValidationError, match="not both"):
        SubgraphCallConfig(workflow_key="read_material", definition_id="d-1")


async def test_a_refused_call_fails_with_its_own_code_and_sentence():
    async def _resolver(_ctx, _config, _inputs):
        raise SubgraphCallRefused(
            "child_input_refused", "The workflow 'Read' takes 'ingested_sources' …", {"errors": ["x"]}
        )

    set_subgraph_resolver(_resolver)
    result = await SubgraphCallExecutor().execute(
        None, SubgraphCallInput(), SubgraphCallConfig(workflow_key="read")
    )
    assert isinstance(result, Failure)
    assert result.error.code == "child_input_refused"
    assert "takes 'ingested_sources'" in result.error.message


# ── one typed result ───────────────────────────────────────────────────────


async def test_a_declared_result_is_the_answer_and_step_ids_stay_inside():
    async def _resolver(_ctx, _config, _inputs):
        return {
            "run_id": "child-1",
            "definition_id": "def-9",
            "version_number": 3,
            "result": {"value": {"__kind": "ingested_sources", "chunks": []},
                       "output_kind": "ingested_sources", "step": "emit"},
        }

    set_subgraph_resolver(_resolver)
    result = await SubgraphCallExecutor().execute(
        None, SubgraphCallInput(), SubgraphCallConfig(workflow_key="read")
    )
    assert isinstance(result, Success)
    payload = result.result
    assert payload.output == {"__kind": "ingested_sources", "chunks": []}
    assert payload.output_kind == "ingested_sources"
    assert payload.result_step == "emit"
    assert (payload.definition_id, payload.version_number) == ("def-9", 3)
    assert payload.last_outputs == {} and payload.channel_values == {}


async def test_an_undeclared_child_still_answers_with_its_step_outputs():
    async def _resolver(_ctx, _config, _inputs):
        return {"run_id": "child-1", "last_outputs": {"n": {"x": 1}}, "channel_values": {}}

    set_subgraph_resolver(_resolver)
    result = await SubgraphCallExecutor().execute(
        None, SubgraphCallInput(), SubgraphCallConfig(definition_id="d")
    )
    assert isinstance(result, Success)
    assert result.result.output is None and result.result.last_outputs == {"n": {"x": 1}}


def _two_results() -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {"id": "start", "type": "data.transform", "position": {"x": 0, "y": 0},
                 "data": {"config": {"expression": "1"}}},
                {"id": "a", "type": "output.to_frontend", "position": {"x": 0, "y": 0}, "data": {}},
                {"id": "b", "type": "output.to_frontend", "position": {"x": 0, "y": 0}, "data": {}},
            ],
            "edges": [
                {"id": "e1", "source": "start", "target": "a"},
                {"id": "e2", "source": "start", "target": "b"},
            ],
            "entry_nodes": ["start"],
        }
    )


def test_set_result_marks_one_step_and_carries_the_declaration_columns():
    patch = DefinitionPatch.model_validate(
        {"ops": [{"op": "set_result", "node_id": "a", "output_kind": "ingested_sources"},
                 {"op": "set_result", "node_id": "b"}]}
    )
    patched = apply_patch(_two_results(), patch)
    marks = {n.id: n.data.get("is_primary") for n in patched.nodes}
    assert marks == {"start": None, "a": None, "b": True}  # last op wins, one mark only
    assert io_declaration_columns(patch) == {"output_kind": "ingested_sources"}
    # Omitted fields leave the columns alone; an explicit null clears them.
    clear = DefinitionPatch.model_validate({"ops": [{"op": "set_result", "input_kind": None}]})
    assert io_declaration_columns(clear) == {"input_kind": None}
    assert apply_patch(_two_results(), clear).nodes[1].data == {}


def test_the_declared_result_is_the_marked_step_and_a_contradiction_is_refused():
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    marked = apply_patch(
        _two_results(),
        DefinitionPatch.model_validate({"ops": [{"op": "set_result", "node_id": "b"}]}),
    )
    graph = compile_graph(marked, registry=registry)
    # Marked with no kind: the marked step is still the result (Smart Add unit 7 gap —
    # result_step was null, so every caller reached into last_outputs).
    kindless = declared_result(graph, marked, declared_output_kind=None)
    assert kindless is not None and kindless.node_id == "b" and kindless.output_kind is None
    assert declared_result(compile_graph(_two_results(), registry=registry), _two_results(),
                           declared_output_kind=None) is None
    result = declared_result(graph, marked, declared_output_kind="ingested_sources")
    assert result is not None and result.node_id == "b"
    # Two possible answers, none marked: the declaration names no step.
    unmarked = _two_results()
    with pytest.raises(ValueError):
        declared_result(compile_graph(unmarked, registry=registry), unmarked,
                        declared_output_kind="ingested_sources")


def test_a_pass_through_result_hands_back_the_kind_marked_value_inside_it():
    inner = {"__kind": "ingested_sources", "chunks": [1]}
    assert claim_kind_value({"payload": inner, "other": {}}, "ingested_sources") == inner
    assert claim_kind_value(inner, "ingested_sources") is inner
    assert claim_kind_value({"x": 1}, "ingested_sources") == {"x": 1}


# ── run once per key ──────────────────────────────────────────────────────


async def test_run_once_reuses_only_for_the_same_child_version():
    executor = SubgraphCallExecutor()
    config = SubgraphCallConfig(workflow_key="read")
    with pytest.raises(RuntimeError):
        await executor.result_version(None, SubgraphCallInput(), config)

    version = {"n": 3}

    async def _target(_ctx, _config):
        return SubgraphTarget(definition_id="def-9", version_number=version["n"])

    set_subgraph_target_resolver(_target)
    first = await executor.result_version(None, SubgraphCallInput(), config)
    version["n"] = 4  # the child was improved and published again
    assert await executor.result_version(None, SubgraphCallInput(), config) != first
    from matrx_graph.executor.once_step import _VERSIONED_CATEGORIES

    assert NodeCategory.SUBGRAPH in _VERSIONED_CATEGORIES


# ── cancellation ───────────────────────────────────────────────────────────


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Out(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _FailsWhileCancelling:
    """Stands in for a call step whose child stopped on its parent's cancel:
    the person pressed Cancel, then the step fails."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.fails_on_cancel",
        category=NodeCategory.DATA,
        display_name="Fails on cancel",
        description="Marks the run cancelling, then fails.",
        input_schema=_In,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    def __init__(self, status: dict[str, str]) -> None:
        self.status = status

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        self.status["value"] = "cancelling"
        raise RuntimeError("the workflow 'Read' ended cancelled")
        return success(_Out())  # pragma: no cover


async def test_a_step_that_fails_because_of_a_cancel_ends_the_run_cancelled():
    status = {"value": "running"}

    async def _control() -> str:
        return status["value"]

    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_FailsWhileCancelling(status))
    definition = Definition.model_validate(
        {"nodes": [{"id": "call", "type": "test.fails_on_cancel", "position": {"x": 0, "y": 0},
                    "data": {}}], "edges": [], "entry_nodes": ["call"]}
    )
    scheduler = Scheduler(
        compile_graph(definition, registry=registry),
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        registry=registry,
        control_check=_control,
    )
    result = await scheduler.run(run_id="r-cancel", thread_id="r-cancel", inputs={})
    assert result.status is RunStatus.CANCELLED
