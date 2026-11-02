"""Adversarial review, round 1 — hostile payloads against the kinds ENGINE CORE.

Attacks the seams of the 2026-08-20/21 kinds push (KINDS_EVERYWHERE_PLAN):
the ingestion gate's position judgment (markers.reduce_for_ingestion), the
settlement stamp's actual reach (event/outcome vs routed edges vs replay vs
mock), runtime kind propagation's trust boundary, KindModel identity
integrity, and the compatibility gate's blind spots.

Convention: a test marked ``xfail(strict=True)`` IS a finding — it encodes
the behavior the plan/doctrine promises, and it currently fails. A green
test documents an attack that HELD (or a demonstrated hazard, where noted).
"""

from __future__ import annotations

import logging
import time
from typing import Any, ClassVar

import pytest
from pydantic import BaseModel, ConfigDict

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
from matrx_graph.content_ir.markers import reduce_for_ingestion
from matrx_graph.content_ir.model import KindModel, kind_of
from matrx_graph.content_ir.sdk import compatibility_verdict
from matrx_graph.kinds import KindEntry, invalidate_kind_catalog_cache
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success

from tests._fixtures import FakeEmitter, make_app_context

FINDING = "ADVERSARIAL FINDING"


# ---------------------------------------------------------------------------
# Shared harness bits
# ---------------------------------------------------------------------------


def _seed_kind(slug: str, json_schema: dict[str, Any] | None) -> None:
    kinds_mod._cache[slug] = (
        time.monotonic(),
        KindEntry(slug=slug, version=1, label=slug, json_schema=json_schema),
    )


@pytest.fixture(autouse=True)
def _clean_kind_cache():
    invalidate_kind_catalog_cache()
    yield
    invalidate_kind_catalog_cache()


class _EmptyConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _OpenInput(BaseModel):
    model_config = ConfigDict(extra="allow")


# =========================================================================
# 1. THE INGESTION GATE — misjudged positions
#
# The promise (scheduler wiring comment + plan): "the marker can never fatal
# a run at the next node's door." reduce_for_ingestion drops __kind ONLY
# where the receiving schema explicitly closes the object. Its position
# judgment (_forbids_marker) reads additionalProperties on the RESOLVED node
# itself — it never looks through anyOf/oneOf/allOf branches, never into
# additionalProperties-as-schema, and never into patternProperties. Every
# one of those is a closed legacy object hiding one indirection deeper.
# =========================================================================


class _LegacyStrict(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str


class _OptionalClosedInput(BaseModel):
    """Optional[closed legacy model] — the single most common nesting form."""

    model_config = ConfigDict(extra="forbid")

    item: _LegacyStrict | None = None


# FIXED (round-1 triage, 2026-08-21): the finding this test pinned is
# closed; the test now guards the fix.
def test_gate_optional_closed_field() -> None:
    incoming = {"item": {"text": "hi", "__kind": "note"}}
    reduced = reduce_for_ingestion(incoming, _OptionalClosedInput.model_json_schema())
    _OptionalClosedInput.model_validate(reduced)


class _LegacyStrictB(BaseModel):
    model_config = ConfigDict(extra="forbid")

    number: int


class _UnionClosedInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item: _LegacyStrict | _LegacyStrictB


# FIXED (round-1 triage, 2026-08-21): the finding this test pinned is
# closed; the test now guards the fix.
def test_gate_union_of_closed_models() -> None:
    incoming = {"item": {"text": "hi", "__kind": "note"}}
    reduced = reduce_for_ingestion(incoming, _UnionClosedInput.model_json_schema())
    _UnionClosedInput.model_validate(reduced)


class _MapOfClosedInput(BaseModel):
    """dict[str, closed model] — additionalProperties-as-schema."""

    model_config = ConfigDict(extra="forbid")

    items: dict[str, _LegacyStrict]


# FIXED (round-1 triage, 2026-08-21): the finding this test pinned is
# closed; the test now guards the fix.
def test_gate_dict_of_closed_models() -> None:
    incoming = {"items": {"a": {"text": "hi", "__kind": "note"}}}
    reduced = reduce_for_ingestion(incoming, _MapOfClosedInput.model_json_schema())
    _MapOfClosedInput.model_validate(reduced)


# FIXED (round-1 triage, 2026-08-21): the finding this test pinned is
# closed; the test now guards the fix.
def test_gate_pattern_properties_closed() -> None:
    schema = {
        "type": "object",
        "patternProperties": {
            "^x_": {
                "type": "object",
                "additionalProperties": False,
                "properties": {"text": {"type": "string"}},
            }
        },
    }
    incoming = {"x_one": {"text": "hi", "__kind": "note"}}
    reduced = reduce_for_ingestion(incoming, schema)
    # jsonschema semantics: the inner object is closed and __kind undeclared.
    assert "__kind" not in reduced["x_one"]


# FIXED (round-1 triage, 2026-08-21): the finding this test pinned is
# closed; the test now guards the fix.
def test_gate_allof_wrapped_closed_ref() -> None:
    schema = {
        "type": "object",
        "properties": {"item": {"allOf": [{"$ref": "#/$defs/L"}]}},
        "$defs": {
            "L": {
                "type": "object",
                "additionalProperties": False,
                "properties": {"text": {"type": "string"}},
            }
        },
    }
    incoming = {"item": {"text": "hi", "__kind": "note"}}
    reduced = reduce_for_ingestion(incoming, schema)
    assert "__kind" not in reduced["item"]


class _ListOfClosedInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[_LegacyStrict]


def test_gate_list_of_closed_models_held() -> None:
    """HELD: list[$ref-to-closed] is judged correctly (items IS traversed)."""
    incoming = {"items": [{"text": "hi", "__kind": "note"}]}
    reduced = reduce_for_ingestion(incoming, _ListOfClosedInput.model_json_schema())
    model = _ListOfClosedInput.model_validate(reduced)
    assert model.items[0].text == "hi"


def test_gate_business_dunder_kind_survives_where_declared_held() -> None:
    """HELD: a schema that declares __kind as a REAL property keeps the
    user's value even inside a closed object."""
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {"__kind": {"type": "string"}, "text": {"type": "string"}},
    }
    incoming = {"__kind": "user-data-not-a-slug", "text": "hi"}
    reduced = reduce_for_ingestion(incoming, schema)
    assert reduced["__kind"] == "user-data-not-a-slug"


# =========================================================================
# 2. SETTLEMENT — where the stamp actually reaches
# =========================================================================


class _LegacyDeclaredOut(BaseModel):
    """A declared node's LEGACY output model — extra='forbid', no kind_ field.

    This is the exact shape the station-1 stamping commit exists for: 214
    declared node types whose pydantic models predate KindModel.
    """

    model_config = ConfigDict(extra="forbid")

    text: str = "payload"


class _LegacyDeclaredSource:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.adv_legacy_declared",
        category=NodeCategory.DATA,
        display_name="Legacy declared source",
        description="Declared kind, legacy closed output model.",
        input_schema=_OpenInput,
        output_schema=_LegacyDeclaredOut,
        config_schema=_EmptyConfig,
        handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
        determinism=ActionTier.PURE,
        is_source=True,
        output_kind="adv_legacy_kind",
    )

    async def execute(
        self, _ctx: NodeExecutionContext, _inputs: _OpenInput, _config: _EmptyConfig
    ) -> NodeResult[_LegacyDeclaredOut]:
        return success(_LegacyDeclaredOut(text="payload"))


class _SpyInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class _SpyOutput(BaseModel):
    model_config = ConfigDict(extra="allow")


class _SpySink:
    """Pass-through: returns exactly what arrived (the data.transform shape)."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.adv_spy_sink",
        category=NodeCategory.DATA,
        display_name="Spy sink",
        description="Echoes its inputs; records them.",
        input_schema=_SpyInput,
        output_schema=_SpyOutput,
        config_schema=_EmptyConfig,
        handles=(HandleSpec(id="in", direction=HandleDirection.INPUT),),
        determinism=ActionTier.PURE,
    )

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def execute(
        self, _ctx: NodeExecutionContext, inputs: _SpyInput, _config: _EmptyConfig
    ) -> NodeResult[_SpyOutput]:
        dump = inputs.model_dump()
        self.calls.append(dump)
        return success(_SpyOutput(**dump))


_ADV_LEGACY_SCHEMA = {
    "type": "object",
    "properties": {"text": {"type": "string"}},
    "required": ["text"],
}


def _chain_definition() -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "src",
                    "type": "test.adv_legacy_declared",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}, "input": {}},
                },
                {
                    "id": "snk",
                    "type": "test.adv_spy_sink",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [{"id": "e1", "source": "src", "target": "snk", "data": {}}],
        }
    )


async def _run_chain(run_id: str, checkpointer: MemoryCheckpointer | None = None):
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    sink = _SpySink()
    reg.register(_LegacyDeclaredSource(), overwrite=True)
    reg.register(sink, overwrite=True)
    graph = compile_graph(_chain_definition(), registry=reg)
    checkpointer = checkpointer or MemoryCheckpointer()
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, checkpointer, make_app_context(emitter), registry=reg)
    result = await scheduler.run(run_id=run_id)
    return result, checkpointer, emitter, sink


def _events(emitter: FakeEmitter, event: str) -> list[dict[str, Any]]:
    return [
        p
        for (m, p) in emitter.events
        if m == "data" and isinstance(p, dict) and p.get("event") == event
    ]


# FIXED (round-1 triage, 2026-08-21): the finding this test pinned is
# closed; the test now guards the fix.
async def test_stamp_reaches_downstream_edges() -> None:
    _seed_kind("adv_legacy_kind", _ADV_LEGACY_SCHEMA)
    result, _, emitter, sink = await _run_chain("adv-stamp-route")
    assert result.status is RunStatus.COMPLETED
    # The event side IS stamped (the half that works):
    completed = {e["node_id"]: e for e in _events(emitter, "node_completed")}
    assert completed["src"]["output"].get("__kind") == "adv_legacy_kind"
    # The routed side must be too — this is the claim under test:
    assert sink.calls and sink.calls[0].get("__kind") == "adv_legacy_kind"


# FIXED (round-1 triage, 2026-08-21): the finding this test pinned is
# closed; the test now guards the fix.
async def test_propagation_through_passthrough_after_stamped_legacy() -> None:
    _seed_kind("adv_legacy_kind", _ADV_LEGACY_SCHEMA)
    result, _, emitter, _ = await _run_chain("adv-stamp-prop")
    assert result.status is RunStatus.COMPLETED
    completed = {e["node_id"]: e for e in _events(emitter, "node_completed")}
    assert completed["snk"]["output_kind"] == "adv_legacy_kind"


# FIXED (round-1 triage, 2026-08-21): the finding this test pinned is
# closed; the test now guards the fix.
async def test_replay_of_stamped_outcome_is_clean(caplog) -> None:
    _seed_kind("adv_legacy_kind", _ADV_LEGACY_SCHEMA)
    checkpointer = MemoryCheckpointer()
    result, _, _, _ = await _run_chain("adv-stamp-replay", checkpointer)
    assert result.status is RunStatus.COMPLETED
    # Same run id, same checkpointer: the idempotent replay path.
    with caplog.at_level(logging.ERROR):
        result2, _, _, _ = await _run_chain("adv-stamp-replay", checkpointer)
    assert result2.status is RunStatus.COMPLETED
    assert not [r for r in caplog.records if "LEGACY-REPLAY" in r.getMessage()]


def _mocked_definition() -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "src",
                    "type": "test.adv_legacy_declared",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {},
                        "input": {},
                        "mock_response": {"enabled": True, "output": {"text": "mocked"}},
                    },
                },
            ],
            "edges": [],
        }
    )


# FIXED (round-1 triage, 2026-08-21): the root is part of the contract;
# this test now guards the gate.
def test_compat_gate_non_object_root_is_not_blind() -> None:
    verdict = compatibility_verdict({"type": "string"}, {"type": "integer"})
    assert not verdict.compatible


# FIXED (round-1 triage, 2026-08-21): the root is part of the contract;
# this test now guards the gate.
def test_compat_gate_sees_map_root_value_change() -> None:
    old = {"type": "object", "additionalProperties": {"type": "string"}}
    new = {"type": "object", "additionalProperties": {"type": "integer"}}
    verdict = compatibility_verdict(new, old)
    assert not verdict.compatible


# FIXED (round-1 triage, 2026-08-21): the root is part of the contract;
# this test now guards the gate.
def test_compat_gate_refuses_root_tightening() -> None:
    old = {"type": "object", "properties": {"a": {"type": "string"}}}
    new = {
        "type": "object",
        "properties": {"a": {"type": "string"}},
        "additionalProperties": False,
    }
    verdict = compatibility_verdict(new, old)
    assert not verdict.compatible


def test_compat_gate_core_semantics_held() -> None:
    """HELD: the advertised core — required-add refused, optional-add
    allowed, removal refused, nested requiredness tightening refused."""
    base = {
        "type": "object",
        "properties": {"a": {"type": "string"}},
        "required": ["a"],
    }
    assert compatibility_verdict(
        {**base, "properties": {"a": {"type": "string"}, "b": {"type": "integer"}}},
        base,
    ).compatible
    assert not compatibility_verdict(
        {
            "type": "object",
            "properties": {"a": {"type": "string"}, "b": {"type": "integer"}},
            "required": ["a", "b"],
        },
        base,
    ).compatible
    assert not compatibility_verdict({"type": "object", "properties": {}}, base).compatible
