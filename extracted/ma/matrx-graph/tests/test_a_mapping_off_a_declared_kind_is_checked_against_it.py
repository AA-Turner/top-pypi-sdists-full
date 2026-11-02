"""A connection that reads a path its source step's DECLARED KIND rules out is refused — never ``{}``.

Live defect 2026-10-28 (Smart Add offerings units): a Run Typed Agent's output IS the kind it
declares (``{"__kind": ..., "claims": [...]}``), but a Gather was fed ``structured_output`` — the
run-envelope field of the OTHER agent step. The step type's output schema is open, so nothing
could rule the path out; the mapping resolved to nothing and the next step silently got ``{}``.
The source step declares ``output_kind``; its schema decides — at save (the authoring gate) and
at run time (the edge refuses, attributed to the source).
"""

from __future__ import annotations

from typing import Any, ClassVar

import pytest
from pydantic import BaseModel, ConfigDict

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph
from matrx_graph.content_ir.authoring_gate import MappingReason, resolve_authored_kinds
from matrx_graph.db import _registry
from matrx_graph.kinds import invalidate_kind_catalog_cache
from matrx_graph.nodes import register_builtin_nodes
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import NodeCategory
from matrx_graph.types.result import success

from tests._fixtures import make_app_context

_CLAIMS = {
    "type": "object",
    "additionalProperties": False,
    "required": ["__kind"],
    "properties": {
        "__kind": {"type": "string", "const": "scope_claims"},
        "claims": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {"quote": {"type": "string"}},
            },
        },
    },
}


class _Row:
    def __init__(self, slug: str, schema: dict) -> None:
        self.id, self.kind, self.version, self.label = f"id-{slug}", slug, 1, slug
        self.is_active, self.emitted_json_schema = True, schema
        self.deleted_at, self.published_to_web = None, True


class _Catalog:
    def __init__(self, rows: dict[str, _Row]) -> None:
        self._rows = rows

    async def load_items(self, **filters: Any) -> list[_Row]:
        row = self._rows.get(filters.get("kind") or "")
        return [row] if row is not None else []


@pytest.fixture(autouse=True)
def _catalog():
    invalidate_kind_catalog_cache()
    previous = dict(_registry._instances)
    _registry.configure_db(
        instances={
            "kind_definition_manager": _Catalog({"scope_claims": _Row("scope_claims", _CLAIMS)}),
            "kind_edge_manager": _Catalog({}),
        }
    )
    yield
    _registry._instances.clear()
    _registry._instances.update(previous)
    invalidate_kind_catalog_cache()


def _definition(source_key: str, **producer: Any) -> dict[str, Any]:
    return {
        "nodes": [
            {"id": "scope", "type": "data.transform", "position": {"x": 0, "y": 0},
             "data": {"label": "Quote the size claims", "output_kind": "scope_claims",
                      "config": {"expression": "{'claims': [{'quote': 'We make 40 candles'}]}"}, **producer}},
            {"id": "count", "type": "data.transform", "position": {"x": 0, "y": 0},
             "data": {"config": {"expression": "{'n': len(get(inputs, 'items') or [])}"}}},
        ],
        "edges": [
            {"id": "e_scope_count", "source": "scope", "target": "count",
             "data": {"kind": "data", "mappings": {"items": source_key}}},
        ],
    }


async def test_a_path_the_kind_rules_out_is_a_blocking_problem_at_save() -> None:
    problems = await resolve_authored_kinds(Definition.model_validate(_definition("structured_output")))
    assert [(p.reason, p.blocking, p.binding.edge_id) for p in problems] == [
        (MappingReason.PATH_NOT_ON_KIND, True, "e_scope_count")
    ]
    assert "structured_output" in problems[0].message and "scope_claims" in problems[0].message


async def test_a_nested_path_the_kind_rules_out_is_refused_too() -> None:
    problems = await resolve_authored_kinds(Definition.model_validate(_definition("claims[0].text")))
    assert [p.reason for p in problems] == [MappingReason.PATH_NOT_ON_KIND]


async def test_a_path_the_kind_carries_passes_and_so_does_the_whole_payload() -> None:
    for key in ("claims", "claims[0].quote", "$FULL_PAYLOAD"):
        assert await resolve_authored_kinds(Definition.model_validate(_definition(key))) == [], key


async def test_a_reshaped_result_is_not_judged_against_the_kind() -> None:
    defn = _definition("structured_output", shape="{'structured_output': inputs['claims']}")
    assert await resolve_authored_kinds(Definition.model_validate(defn)) == []


async def test_a_field_handed_beside_the_kind_is_not_judged() -> None:
    defn = _definition("usage")
    defn["nodes"][0]["data"]["config"]["run_envelope"] = ["usage"]
    assert await resolve_authored_kinds(Definition.model_validate(defn)) == []


class _Open(BaseModel):
    model_config = ConfigDict(extra="allow")


class _TypedAnswer:
    """Stands in for Run Typed Agent: an OPEN output schema whose answer IS the declared kind."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.typed_answer",
        category=NodeCategory.DATA,
        display_name="Typed answer",
        description="returns the kind payload as its output",
        input_schema=_Open,
        output_schema=_Open,
        config_schema=_Open,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
    )

    async def execute(self, ctx: Any, inputs: _Open, config: _Open):
        return success(_Open(claims=[{"quote": "We make 40 candles"}]))


def _typed(defn: dict[str, Any]) -> dict[str, Any]:
    defn["nodes"][0]["type"] = "test.typed_answer"
    defn["nodes"][0]["data"]["config"] = {}
    return defn


async def _run(defn: dict[str, Any], run_id: str):
    registry = register_builtin_nodes(NodeRegistry())
    registry.register(_TypedAnswer(), overwrite=True)
    graph = compile_graph(Definition.model_validate(defn), registry=registry)
    return await Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry).run(run_id=run_id)


async def test_at_run_time_the_path_the_kind_rules_out_stops_the_run_instead_of_handing_on_nothing() -> None:
    result = await _run(_typed(_definition("structured_output")), "kind-path-run")
    assert result.status is not RunStatus.COMPLETED, result.last_outputs
    assert "structured_output" in str(result.error) and "scope_claims" in str(result.error), result.error


async def test_at_run_time_a_path_the_kind_carries_still_flows() -> None:
    result = await _run(_typed(_definition("claims")), "kind-path-ok")
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["count"] == {"n": 1}


# ── Save and run judge the SAME source kind, the SAME way (review of 64775c88, 2026-10-28) ──


class _OwnKindAnswer(_TypedAnswer):
    """A typed ACTION: the step type itself declares the kind (no ``data.output_kind``)."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        **{**_TypedAnswer.spec.model_dump(exclude={"node_type"}, exclude_unset=True),
           "type": "test.own_kind_answer", "output_kind": "scope_claims"}
    )


class _BesideAnswer(_TypedAnswer):
    """Names ``final_text`` beside its kind at run time (``ctx.declare_beside_kind``) only."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        **{**_TypedAnswer.spec.model_dump(exclude={"node_type"}, exclude_unset=True), "type": "test.beside_answer"}
    )

    async def execute(self, ctx: Any, inputs: _Open, config: _Open):
        ctx.declare_beside_kind(["final_text"])
        return success(_Open(claims=[{"quote": "We make 40 candles"}]))


def _registry_with_answers() -> NodeRegistry:
    registry = register_builtin_nodes(NodeRegistry())
    for executor in (_TypedAnswer(), _OwnKindAnswer(), _BesideAnswer()):
        registry.register(executor, overwrite=True)
    return registry


def _own_kind(defn: dict[str, Any]) -> dict[str, Any]:
    defn["nodes"][0]["type"] = "test.own_kind_answer"
    defn["nodes"][0]["data"].pop("output_kind")
    defn["nodes"][0]["data"]["config"] = {}
    return defn


async def _run_with(defn: dict[str, Any], run_id: str):
    registry = _registry_with_answers()
    graph = compile_graph(Definition.model_validate(defn), registry=registry)
    return await Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry).run(run_id=run_id)


async def test_a_step_types_own_kind_is_judged_at_save_like_the_run_judges_it() -> None:
    defn = _own_kind(_definition("structured_output"))
    problems = await resolve_authored_kinds(Definition.model_validate(defn), registry=_registry_with_answers())
    assert [(p.reason, p.blocking) for p in problems] == [(MappingReason.PATH_NOT_ON_KIND, True)]
    result = await _run_with(_own_kind(_definition("structured_output")), "own-kind-run")
    assert result.status is not RunStatus.COMPLETED and "structured_output" in str(result.error)


async def test_save_and_run_agree_on_the_same_definition() -> None:
    for key, refused in (("structured_output", True), ("claims", False), ("claims[0].nope", True)):
        defn = _own_kind(_definition(key))
        saved = await resolve_authored_kinds(Definition.model_validate(defn), registry=_registry_with_answers())
        ran = await _run_with(_own_kind(_definition(key)), f"agree-{key}")
        assert bool(saved) is refused, (key, saved)
        assert (ran.status is not RunStatus.COMPLETED) is refused, (key, ran.error)


async def test_an_envelope_alternative_beside_a_kind_path_saves_clean() -> None:
    defn = _definition("claims ?? final_text")
    defn["nodes"][0]["data"]["config"]["run_envelope"] = ["final_text"]
    assert await resolve_authored_kinds(Definition.model_validate(defn)) == []
    # …and the kind alternative is still judged: a path the kind rules out still blocks.
    defn = _definition("nope ?? final_text")
    defn["nodes"][0]["data"]["config"]["run_envelope"] = ["final_text"]
    problems = await resolve_authored_kinds(Definition.model_validate(defn))
    assert [p.reason for p in problems] == [MappingReason.PATH_NOT_ON_KIND] and "nope" in problems[0].message


async def test_at_run_time_an_envelope_field_is_not_judged_against_the_kind() -> None:
    defn = _typed(_definition("final_text"))
    defn["nodes"][0]["data"]["config"] = {"run_envelope": ["final_text"]}
    result = await _run(defn, "envelope-run")
    assert result.status is RunStatus.COMPLETED, result.error
    # Per ?? alternative: the kind path is valid (just empty here), the envelope one is excluded.
    defn = _typed(_definition("claims[5].quote ?? final_text"))
    defn["nodes"][0]["data"]["config"] = {"run_envelope": ["final_text"]}
    result = await _run(defn, "envelope-alt-run")
    assert result.status is RunStatus.COMPLETED, result.error


async def test_at_run_time_a_key_declared_beside_the_kind_by_the_step_is_not_judged() -> None:
    defn = _typed(_definition("final_text"))
    defn["nodes"][0]["type"] = "test.beside_answer"
    result = await _run_with(defn, "beside-run")
    assert result.status is RunStatus.COMPLETED, result.error


async def test_the_sync_kind_schema_respects_the_cache_ttl() -> None:
    from matrx_graph import kinds

    await kinds.resolve_kind("scope_claims")
    assert kinds.cached_kind_schema("scope_claims") is not None
    stamped, entry = kinds._cache["scope_claims"]
    kinds._cache["scope_claims"] = (stamped - kinds._CACHE_TTL_SECONDS - 1, entry)
    assert kinds.cached_kind_schema("scope_claims") is None
