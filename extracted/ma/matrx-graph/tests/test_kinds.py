"""Shape system — node I/O declared as platform kinds.

A NodeSpec (or a NodeDef via ``data.input_kind`` / ``data.output_kind``)
declares its I/O as content_ir kind slugs. The compiler carries the kinds onto
CompiledNode; the scheduler gates inputs against the kind's registered JSON
Schema (fatal, per-field) and validates outputs loudly-non-fatally
(node-author-defect posture), stamping ``output_kind`` on every recorded
NodeOutcome.

The kind catalog (matrx_graph.kinds) is DB-backed in production; tests seed
its process cache directly so no DB is touched.
"""

from __future__ import annotations

import logging
import time
from types import SimpleNamespace
from typing import Any, ClassVar

import pytest
from matrx_graph.content_ir.model import KindModel
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
from matrx_graph.errors import CompilationError
from matrx_graph.kinds import (
    KindEntry,
    configure_canonical_kind_organization,
    invalidate_kind_catalog_cache,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict, Field

from tests._fixtures import FakeEmitter, make_app_context


class _Input(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Output(BaseModel):
    model_config = ConfigDict(extra="forbid")
    result: str = Field(default="ok")


class _Config(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _KindedExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.kinded",
        category=NodeCategory.DATA,
        display_name="Kinded node",
        description="Declares its I/O as platform kinds.",
        input_schema=_Input,
        output_schema=_Output,
        config_schema=_Config,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        input_kind="test_strict_input",
        output_kind="test_result",
    )

    async def execute(
        self,
        _ctx: NodeExecutionContext,
        _inputs: _Input,
        _config: _Config,
    ) -> NodeResult[_Output]:
        return success(_Output(result="ok"))


def _seed_kind(slug: str, json_schema: dict[str, Any] | None) -> None:
    """Seed the catalog's process cache directly — no DB in tests."""
    kinds_mod._cache[slug] = (
        time.monotonic(),
        KindEntry(slug=slug, version=1, label=slug, json_schema=json_schema),
    )


@pytest.fixture(autouse=True)
def _clean_kind_cache():
    configure_canonical_kind_organization(None)
    invalidate_kind_catalog_cache()
    yield
    configure_canonical_kind_organization(None)
    invalidate_kind_catalog_cache()


async def test_canonical_organization_wins_same_slug_public_collision(monkeypatch) -> None:
    """Every catalog consumer follows the publisher's canonical platform row."""
    other_public = SimpleNamespace(
        kind="text",
        published_to_web=True,
        organization_id="other-org",
        emitted_json_schema={"required": ["value"]},
    )
    system_public = SimpleNamespace(
        kind="text",
        published_to_web=True,
        organization_id="system-org",
        emitted_json_schema={"required": ["text"]},
    )

    class _Mgr:
        model = None

        @staticmethod
        async def load_items(**_kwargs):
            return [other_public, system_public]

    monkeypatch.setattr(kinds_mod, "_manager", lambda: _Mgr())

    # This is the exact stale-contract shape observed in production before a
    # host identifies the platform organization: the first public duplicate
    # wins and requires ``value``.  The startup seam below is the repair.
    assert await kinds_mod.list_registered_kinds() == (("text", 1, {"required": ["value"]}),)
    configure_canonical_kind_organization("system-org")

    # The synchronous stream catalog must not accept a public duplicate from
    # another organization after the publisher reconciles the system row.
    catalog = await kinds_mod.list_registered_kinds()
    assert catalog == (("text", 1, {"required": ["text"]}),)

    # The per-slug validation lookup uses the exact same rule.
    resolved, reason = await kinds_mod.resolve_kind("text")
    assert reason is None
    assert resolved is not None
    assert resolved.json_schema == {"required": ["text"]}


async def test_catalog_projection_keeps_org_for_canonical_selection(monkeypatch) -> None:
    """The optimized ORM listing retains the field the preference consumes."""
    rows = [
        SimpleNamespace(
            kind="canonical",
            version=1,
            published_to_web=True,
            organization_id="other-org",
            emitted_json_schema={"required": ["value"]},
        ),
        SimpleNamespace(
            kind="canonical",
            version=2,
            published_to_web=True,
            organization_id="system-org",
            emitted_json_schema={"required": ["text"]},
            metadata={"disposition": "record"},
        ),
        SimpleNamespace(
            kind="public_fallback",
            version=3,
            published_to_web=True,
            organization_id="other-org",
            emitted_json_schema={"required": ["public"]},
        ),
        SimpleNamespace(
            kind="private_fallback",
            version=4,
            published_to_web=False,
            organization_id="other-org",
            emitted_json_schema={"required": ["private"]},
        ),
    ]

    class _Query:
        selected_fields: tuple[str, ...] = ()

        def only(self, *fields: str):
            self.selected_fields = fields
            return self

        async def all(self):
            return rows

    query = _Query()

    class _Model:
        @staticmethod
        def filter(**kwargs):
            assert kwargs == {"deleted_at__isnull": True}
            return query

    class _Mgr:
        model = _Model()

    monkeypatch.setattr(kinds_mod, "_manager", lambda: _Mgr())
    configure_canonical_kind_organization("system-org")

    assert await kinds_mod.list_registered_kinds() == (
        ("canonical", 2, {"required": ["text"]}),
        ("private_fallback", 4, {"required": ["private"]}),
        ("public_fallback", 3, {"required": ["public"]}),
    )
    assert query.selected_fields == (
        "kind",
        "version",
        "emitted_json_schema",
        "published_to_web",
        "organization_id",
        "metadata",
    )
    # The same listing carries each kind's declared disposition (the chosen row's), so the
    # sync stream catalog can tell a `record` kind without a second query.
    assert kinds_mod.listed_kind_disposition("canonical") == "record"
    assert kinds_mod.listed_kind_disposition("public_fallback") is None
    assert kinds_mod.listed_kind_disposition("never_listed") is None


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(_KindedExecutor(), overwrite=True)
    return reg


def _definition(node_data: dict | None = None) -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "k1",
                    "type": "test.kinded",
                    "position": {"x": 0, "y": 0},
                    "data": node_data or {"config": {}},
                },
            ],
            "edges": [],
        }
    )


# ---------------------------------------------------------------- compile


def test_compile_carries_spec_kinds():
    graph = compile_graph(_definition(), registry=_registry())
    node = graph.nodes["k1"]
    assert node.input_kind == "test_strict_input"
    assert node.output_kind == "test_result"


def test_compile_authored_override_wins():
    graph = compile_graph(
        _definition({"config": {}, "output_kind": "flashcard_set", "input_kind": "json"}),
        registry=_registry(),
    )
    node = graph.nodes["k1"]
    assert node.input_kind == "json"
    assert node.output_kind == "flashcard_set"


def test_compile_invalid_authored_kind_raises():
    with pytest.raises(CompilationError, match="output_kind"):
        compile_graph(_definition({"config": {}, "output_kind": 123}), registry=_registry())
    with pytest.raises(CompilationError, match="input_kind"):
        compile_graph(_definition({"config": {}, "input_kind": "  "}), registry=_registry())


def test_builtin_specs_declare_output_kinds():
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    by_type = {spec.node_type: spec for spec in reg.all_specs()}
    assert by_type["http.get"].output_kind == "http_response"
    assert by_type["control.branch"].output_kind == "branch_result"
    assert by_type["subgraph.call"].output_kind == "workflow_run_result"
    # Dynamic-output nodes are still governed by their compiled inline schema;
    # io.user_input additionally names its shape ('user_inputs', an open
    # object) so pickers/labels speak a real name instead of nothing.
    assert by_type["io.user_input"].output_kind == "user_inputs"
    assert by_type["io.user_input"].dynamic_output is True
    assert by_type["text.render_list"].output_kind == "rendered_text"
    # Every non-dynamic builtin is kind-typed EXCEPT the ruled pass-throughs:
    # 'json' is a format word, not an identity (round-1 F7) — data.transform
    # and output.to_frontend declare nothing and settle with the kind of what
    # actually flowed (runtime propagation).
    # The flow pack (2026-08-21) is pass-through by construction: sleep /
    # wait_until / throttle / noop hand the payload downstream unchanged, so
    # they declare nothing and runtime propagation carries identity.
    PASS_THROUGHS = {
        "data.transform",
        "output.to_frontend",
        "flow.sleep",
        "flow.wait_until",
        "flow.throttle",
        "flow.noop",
    }
    untyped = [
        s.node_type
        for s in by_type.values()
        if s.output_kind is None and not s.dynamic_output and s.node_type not in PASS_THROUGHS
    ]
    assert untyped == [], f"kind-less builtin specs: {untyped}"


# ---------------------------------------------------------------- scheduler


async def _run(definition: Definition, run_id: str):
    registry = _registry()
    graph = compile_graph(definition, registry=registry)
    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    result = await scheduler.run(run_id=run_id)
    return result, checkpointer


async def test_input_kind_gate_rejects_nonconforming_inputs():
    _seed_kind(
        "test_strict_input",
        {
            "type": "object",
            "properties": {"topic": {"type": "string"}},
            "required": ["topic"],
        },
    )
    _seed_kind("test_result", {})
    result, _ = await _run(_definition({"config": {}, "input": {"topic": 42}}), "kind-gate-bad")
    assert result.status is not RunStatus.COMPLETED


async def test_input_kind_gate_supplies_declared_identity_marker():
    """Schema-law companion (2026-08-23): kind schemas declare __kind — often
    required — but a plain edge payload has no author to supply it. The
    node's input_kind IS the identity claim, so the gate injects the root
    marker when absent. First live casualty: Agent Foundry run 72ca63ab,
    where {"text": ...} from a regex edge failed the `text` kind for a
    missing __kind. A payload that self-identifies WRONGLY must still fail."""
    _seed_kind(
        "test_strict_input",
        {
            "type": "object",
            "properties": {
                "__kind": {"const": "test_strict_input"},
                "topic": {"type": "string"},
            },
            "required": ["__kind", "topic"],
            "additionalProperties": False,
        },
    )
    _seed_kind("test_result", {})
    result, _ = await _run(
        _definition({"config": {}, "input": {"topic": "photosynthesis"}}),
        "kind-gate-identity",
    )
    assert result.status is RunStatus.COMPLETED

    # Wrong self-identification is NOT healed — it fails loudly.
    result_bad, _ = await _run(
        _definition({"config": {}, "input": {"__kind": "impostor", "topic": "x"}}),
        "kind-gate-impostor",
    )
    assert result_bad.status is not RunStatus.COMPLETED


async def test_input_kind_gate_passes_conforming_inputs():
    _seed_kind(
        "test_strict_input",
        {
            "type": "object",
            "properties": {"topic": {"type": "string"}},
            "required": ["topic"],
        },
    )
    _seed_kind("test_result", {})
    result, checkpointer = await _run(
        _definition({"config": {}, "input": {"topic": "photosynthesis"}}),
        "kind-gate-good",
    )
    assert result.status is RunStatus.COMPLETED
    outcome = await checkpointer.get_outcome("kind-gate-good", 0, "k1", 1)
    assert outcome is not None
    assert outcome.output_kind == "test_result"


async def test_output_kind_drift_is_fatal_when_family_on(caplog):
    """workflow_io kind enforcement is ON by default (flipped 2026-08-26):
    genuine output drift is now the node author's defect made FATAL — the
    run ERRORS, and the error names the node, the kind, and that enforcement
    is on. See ``test_output_kind_drift_is_loud_but_non_fatal_when_family_off``
    for the still-live rollback path."""
    _seed_kind("test_strict_input", {})
    # The executor emits {"result": "ok"} — this schema demands a number, so
    # the output drifts from its declared kind. Author defect: FATAL under ON.
    _seed_kind(
        "test_result",
        {
            "type": "object",
            "properties": {"result": {"type": "number"}},
            "required": ["result"],
        },
    )
    with caplog.at_level("ERROR"):
        result, checkpointer = await _run(_definition(), "kind-drift")
    assert result.status is not RunStatus.COMPLETED
    outcome = await checkpointer.get_outcome("kind-drift", 0, "k1", 1)
    assert outcome is not None
    assert outcome.error is not None
    assert outcome.error["code"] == "KindContractViolation"
    assert "k1" in outcome.error["message"]
    assert "test_result" in outcome.error["message"]
    assert "workflow_io kind enforcement is ON" in outcome.error["message"]
    assert any("does NOT match its declared kind" in r.message for r in caplog.records)
    assert any("FATAL (workflow_io enforcement ON)" in r.message for r in caplog.records)


async def test_output_kind_drift_is_loud_but_non_fatal_when_family_off(monkeypatch, caplog):
    """The rollback path stays proven: with workflow_io explicitly off — the
    exact override the constant's own docstring prescribes — the same drift
    is loud but never fatal."""
    monkeypatch.setitem(kinds_mod.KIND_ENFORCEMENT, "workflow_io", False)
    _seed_kind("test_strict_input", {})
    _seed_kind(
        "test_result",
        {
            "type": "object",
            "properties": {"result": {"type": "number"}},
            "required": ["result"],
        },
    )
    with caplog.at_level("ERROR"):
        result, checkpointer = await _run(_definition(), "kind-drift-off")
    assert result.status is RunStatus.COMPLETED
    outcome = await checkpointer.get_outcome("kind-drift-off", 0, "k1", 1)
    assert outcome is not None and outcome.output_kind == "test_result"
    assert any("does NOT match its declared kind" in r.message for r in caplog.records)
    assert any("run continues" in r.message for r in caplog.records)


async def _run_capture(definition: Definition, run_id: str, extra_executors: tuple = ()):
    registry = _registry()
    for executor in extra_executors:
        registry.register(executor, overwrite=True)
    graph = compile_graph(definition, registry=registry)
    checkpointer = MemoryCheckpointer()
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, checkpointer, make_app_context(emitter), registry=registry)
    result = await scheduler.run(run_id=run_id)
    return result, checkpointer, emitter


def _events(emitter: FakeEmitter, event: str) -> list[dict[str, Any]]:
    return [
        p
        for (m, p) in emitter.events
        if m == "data" and isinstance(p, dict) and p.get("event") == event
    ]


async def test_output_kind_ok_true_on_event_and_outcome():
    _seed_kind("test_strict_input", {})
    _seed_kind(
        "test_result",
        {
            "type": "object",
            "properties": {"result": {"type": "string"}},
            "required": ["result"],
        },
    )
    result, checkpointer, emitter = await _run_capture(_definition(), "kind-ok")
    assert result.status is RunStatus.COMPLETED
    completed = _events(emitter, "node_completed")
    assert len(completed) == 1
    assert completed[0]["output_kind"] == "test_result"
    assert completed[0]["output_kind_ok"] is True
    assert completed[0]["output_kind_errors"] is None
    outcome = await checkpointer.get_outcome("kind-ok", 0, "k1", 1)
    assert outcome is not None
    assert outcome.output_kind_ok is True
    assert outcome.output_kind_errors is None
    # Content IR envelope hand-off (D2): a verified pass ships the canonical
    # envelope at metadata.__ir — out-of-band beside the UNMUTATED output.
    from matrx_graph.content_ir.envelope import compact_json
    from matrx_graph.content_ir.fingerprint import fingerprint_text

    envelope = (completed[0].get("metadata") or {}).get("__ir")
    assert envelope is not None, "verified output must carry metadata.__ir"
    assert envelope["v"] == 1
    assert envelope["engine"] == "py-block-detector"
    root = envelope["root"]
    assert root["role"] == "structured"
    assert root["kind"] == "test_result"
    assert root["kindState"] == "resolved"
    assert root["status"] == "complete"
    assert root["residue"] is None
    # Wire elision: the payload rides ONCE per event — in `output` — never a
    # second inline copy in the envelope. root.value is dropped and the
    # value_ref marker names the frame field the consumer rehydrates from.
    assert root["value"] is None
    assert root["value_ref"] == "output"
    # STATION 1 (plan §4.2): a settled, verified payload SAYS what it is —
    # the root discriminator is stamped for declared legacy models, so the
    # value is self-describing on the wire and in the outcome row.
    assert completed[0]["output"] == {"result": "ok", "__kind": "test_result"}
    # The serialized metadata must not smuggle the payload back in anywhere.
    import json as _json

    assert '"result"' not in _json.dumps(completed[0]["metadata"])
    # Fingerprint = the twin's fingerprint_text over the compact JSON of the
    # FULL value (hashed at stamp time, before elision — the TS
    # envelopeFromCompleteValue analogue).
    assert envelope["fingerprint"] == fingerprint_text(compact_json(completed[0]["output"]))


async def test_output_kind_ok_false_with_errors_on_drift_when_family_off(monkeypatch, caplog):
    """The verdict-on-the-wire shape (output_kind_ok=False + per-field errors
    on node_completed) is an OFF-mode-only observation: with workflow_io ON
    (the shipped default) the run ERRORS before a node_completed for a
    drifting output ever ships — see
    ``test_output_kind_drift_is_fatal_when_family_on``. Pinned here with the
    family explicitly off, the exact override the constant's own docstring
    prescribes."""
    monkeypatch.setitem(kinds_mod.KIND_ENFORCEMENT, "workflow_io", False)
    _seed_kind("test_strict_input", {})
    _seed_kind(
        "test_result",
        {
            "type": "object",
            "properties": {"result": {"type": "number"}},
            "required": ["result"],
        },
    )
    with caplog.at_level("ERROR"):
        result, checkpointer, emitter = await _run_capture(_definition(), "kind-drift-wire")
    assert result.status is RunStatus.COMPLETED  # drift stays non-fatal
    completed = _events(emitter, "node_completed")
    assert len(completed) == 1
    assert completed[0]["output_kind_ok"] is False
    assert completed[0]["output_kind_errors"]  # non-empty per-field list
    outcome = await checkpointer.get_outcome("kind-drift-wire", 0, "k1", 1)
    assert outcome is not None
    assert outcome.output_kind_ok is False
    assert outcome.output_kind_errors == completed[0]["output_kind_errors"]
    # D2 verified-only law: a DRIFTING output never ships an envelope.
    assert completed[0]["metadata"] is None
    # THE HONESTY GUARD (station 1): a payload is NEVER stamped with a kind it
    # measurably violates - the column + verdict record the drift, the data
    # does not lie about itself.
    assert "__kind" not in completed[0]["output"]


async def test_output_kind_loud_skip_is_neutral_not_a_pass_when_family_off(monkeypatch, caplog):
    """A "neutral, never a pass" verdict is inherently an OFF-mode/degraded
    concept: with workflow_io ON (the shipped default) this same
    schema_unavailable reason escalates to FATAL at admission — see
    ``test_flag_on_degraded_reason_is_fatal_at_admission`` in
    test_kind_enforcement.py — so there is no neutral node_completed to
    observe. Pinned here with the family explicitly off, the exact override
    the constant's own docstring prescribes."""
    monkeypatch.setitem(kinds_mod.KIND_ENFORCEMENT, "workflow_io", False)
    _seed_kind("test_strict_input", {})
    # Kind registered but WITHOUT an emitted schema → loud-skip: the check
    # never ran, so ok must stay None (neutral), never True.
    _seed_kind("test_result", None)
    with caplog.at_level("ERROR"):
        result, checkpointer, emitter = await _run_capture(_definition(), "kind-skip")
    assert result.status is RunStatus.COMPLETED
    completed = _events(emitter, "node_completed")
    assert completed[0]["output_kind"] == "test_result"
    assert completed[0]["output_kind_ok"] is None
    assert completed[0]["output_kind_errors"] is None
    outcome = await checkpointer.get_outcome("kind-skip", 0, "k1", 1)
    assert outcome is not None
    assert outcome.output_kind_ok is None
    assert any("no emitted_json_schema" in r.message for r in caplog.records)
    # D2 verified-only law: a DEGRADED (loud-skip) check never ships an
    # envelope — a skipped check is not a pass, and an envelope IS one.
    assert completed[0]["metadata"] is None


class _KindlessDynamicExecutor:
    # A dynamic-output node with NO declared output_kind — io.user_input used
    # to be this case, but it now names its shape ('user_inputs'), so the
    # neutral posture is pinned with a dedicated spec.
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.kindless_dynamic",
        category=NodeCategory.IO,
        display_name="Kindless dynamic node",
        description="Dynamic output, no declared kind.",
        input_schema=_Input,
        output_schema=_Input,
        config_schema=_Config,
        handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
        determinism=ActionTier.PURE,
        is_source=True,
        dynamic_output=True,
    )

    async def execute(
        self,
        _ctx: NodeExecutionContext,
        inputs: _Input,
        _config: _Config,
    ) -> NodeResult[_Input]:
        return success(inputs)


async def test_no_declared_kind_is_neutral():
    graph_def = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "u1",
                    "type": "test.kindless_dynamic",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}, "input": {}},
                },
            ],
            "edges": [],
        }
    )
    result, checkpointer, emitter = await _run_capture(
        graph_def, "kind-none", extra_executors=(_KindlessDynamicExecutor(),)
    )
    assert result.status is RunStatus.COMPLETED
    completed = _events(emitter, "node_completed")
    assert completed[0]["output_kind"] is None
    assert completed[0]["output_kind_ok"] is None
    # D2: no declared kind → no envelope.
    assert completed[0]["metadata"] is None
    outcome = await checkpointer.get_outcome("kind-none", 0, "u1", 1)
    assert outcome is not None and outcome.output_kind_ok is None


async def test_input_kind_violation_is_structured_on_the_wire():
    """The input gate's fatal path must reach the wire structurally: the
    node_failed event's ``error.details.field_errors`` carries the per-field
    list, not just a joined message string."""
    _seed_kind(
        "test_strict_input",
        {
            "type": "object",
            "properties": {"topic": {"type": "string"}},
            "required": ["topic"],
        },
    )
    _seed_kind("test_result", {})
    result, checkpointer, emitter = await _run_capture(
        _definition({"config": {}, "input": {"topic": 42}}), "kind-gate-wire"
    )
    assert result.status is not RunStatus.COMPLETED
    failed = _events(emitter, "node_failed")
    assert len(failed) == 1
    assert failed[0]["error_type"] == "NodeInputValidationError"
    error = failed[0]["error"]
    assert isinstance(error, dict)
    field_errors = (error.get("details") or {}).get("field_errors")
    assert isinstance(field_errors, list) and field_errors
    assert "test_strict_input" in error["message"]
    # Same structured error persisted on the outcome row.
    outcome = await checkpointer.get_outcome("kind-gate-wire", 0, "k1", 1)
    assert outcome is not None and outcome.error is not None
    assert outcome.error["details"]["field_errors"] == field_errors


async def test_unregistered_kind_fails_open_and_loud(caplog, monkeypatch):
    async def _boom(**_kw):
        raise RuntimeError("db not wired")

    class _Mgr:
        load_items = staticmethod(_boom)

    monkeypatch.setattr(kinds_mod, "_manager", lambda: _Mgr())
    with caplog.at_level("ERROR"):
        errors = await kinds_mod.validate_against_kind({"x": 1}, "nope_not_real")
    assert errors == []
    assert any("SKIPPED" in r.message for r in caplog.records)


# ------------------------------------------------- runtime kind propagation


class _FlowResult(KindModel, kind="test_flow_result"):
    result: str


class _FlowThroughExecutor:
    # A pass-through-shaped node: NO declared output_kind, but its payload is
    # a KindModel, so the dump carries __kind — the self-described case that
    # runtime propagation (plan §7 / the audit's "missing primitive") stamps.
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.flow_through",
        category=NodeCategory.DATA,
        display_name="Flow-through node",
        description="No declared kind; output describes itself.",
        input_schema=_Input,
        output_schema=_FlowResult,
        config_schema=_Config,
        handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
        determinism=ActionTier.PURE,
        is_source=True,
    )

    async def execute(
        self,
        _ctx: NodeExecutionContext,
        _inputs: _Input,
        _config: _Config,
    ) -> NodeResult[_FlowResult]:
        return success(_FlowResult(result="flowed"))


def _flow_definition() -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "f1",
                    "type": "test.flow_through",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}, "input": {}},
                },
            ],
            "edges": [],
        }
    )


async def test_undeclared_kind_propagates_from_self_described_payload():
    # The payload SAYS what it is; settlement reads it, verifies it against
    # the registry like any declared kind, and stamps it on event + outcome.
    _seed_kind(
        "test_flow_result",
        {
            "type": "object",
            "properties": {"result": {"type": "string"}},
            "required": ["result"],
        },
    )
    result, checkpointer, emitter = await _run_capture(
        _flow_definition(), "kind-flow", extra_executors=(_FlowThroughExecutor(),)
    )
    assert result.status is RunStatus.COMPLETED
    completed = _events(emitter, "node_completed")
    assert completed[0]["output_kind"] == "test_flow_result"
    assert completed[0]["output_kind_ok"] is True
    outcome = await checkpointer.get_outcome("kind-flow", 0, "f1", 1)
    assert outcome is not None
    assert outcome.output_kind == "test_flow_result"
    assert outcome.output_kind_ok is True


async def test_propagated_kind_is_verified_not_trusted(caplog):
    """A payload lying about itself (its registered schema demands a field it
    lacks) is verified, not trusted, exactly like author drift — and with
    workflow_io enforcement ON (the shipped default, flipped 2026-08-26) that
    verification is FATAL: the run ERRORS, naming the node, that the kind is
    "self-described" (not declared — the node itself declares no output_kind;
    the payload's own __kind is what's being checked), and that enforcement
    is on. See ``test_propagated_kind_is_verified_not_trusted_when_family_off``
    for the still-live rollback path."""
    _seed_kind(
        "test_flow_result",
        {
            "type": "object",
            "properties": {
                "result": {"type": "string"},
                "mandatory": {"type": "string"},
            },
            "required": ["result", "mandatory"],
        },
    )
    with caplog.at_level(logging.ERROR):
        result, checkpointer, emitter = await _run_capture(
            _flow_definition(), "kind-flow-lie", extra_executors=(_FlowThroughExecutor(),)
        )
    assert result.status is not RunStatus.COMPLETED  # FATAL under enforcement ON
    assert _events(emitter, "node_completed") == []
    outcome = await checkpointer.get_outcome("kind-flow-lie", 0, "f1", 1)
    assert outcome is not None
    assert outcome.error is not None
    assert outcome.error["code"] == "KindContractViolation"
    assert "f1" in outcome.error["message"]
    assert "self-described kind 'test_flow_result'" in outcome.error["message"]
    assert "workflow_io kind enforcement is ON" in outcome.error["message"]


async def test_propagated_kind_is_verified_not_trusted_when_family_off(monkeypatch, caplog):
    """The rollback path stays proven: with workflow_io explicitly off — the
    exact override the constant's own docstring prescribes — a self-described
    payload that lies about itself screams exactly like author drift, loud
    but never fatal."""
    monkeypatch.setitem(kinds_mod.KIND_ENFORCEMENT, "workflow_io", False)
    _seed_kind(
        "test_flow_result",
        {
            "type": "object",
            "properties": {
                "result": {"type": "string"},
                "mandatory": {"type": "string"},
            },
            "required": ["result", "mandatory"],
        },
    )
    with caplog.at_level(logging.ERROR):
        result, checkpointer, emitter = await _run_capture(
            _flow_definition(), "kind-flow-lie-off", extra_executors=(_FlowThroughExecutor(),)
        )
    assert result.status is RunStatus.COMPLETED  # loud, not fatal
    completed = _events(emitter, "node_completed")
    assert completed[0]["output_kind"] == "test_flow_result"
    assert completed[0]["output_kind_ok"] is False
    assert completed[0]["output_kind_errors"]
    outcome = await checkpointer.get_outcome("kind-flow-lie-off", 0, "f1", 1)
    assert outcome is not None and outcome.output_kind_ok is False


# ---------------------------------------------------------------------------
# The runtime wrapper on the wire (KINDS_EVERYWHERE_PLAN §10b item 8)
# ---------------------------------------------------------------------------


async def test_node_completed_carries_the_node_outcome_wrapper():
    """The packet: which workflow, which node, and what the data IS."""
    _seed_kind("test_strict_input", {})
    _seed_kind(
        "test_result",
        {
            "type": "object",
            "properties": {"result": {"type": "string"}},
            "required": ["result"],
        },
    )
    _, _, emitter = await _run_capture(_definition(), "kind-wrapper")
    completed = _events(emitter, "node_completed")
    wrapper = completed[0]["wrapper"]
    assert wrapper is not None, "every completion carries its node_outcome wrapper"
    # Self-describing: the packet says what it is, in the data.
    assert wrapper["__kind"] == "node_outcome"
    # Provenance — run, node, step, attempt, timing.
    assert wrapper["run_id"] == "kind-wrapper"
    assert wrapper["node_id"] == "k1"
    assert wrapper["step"] == 0
    assert wrapper["attempt"] == 1
    assert wrapper["status"] == "completed"
    assert isinstance(wrapper["duration_ms"], int)
    assert wrapper["started_at"] and wrapper["ended_at"]
    # The kind verdict rides the wrapper exactly as it rides the columns.
    assert wrapper["output_kind"] == "test_result"
    assert wrapper["output_kind_ok"] is True
    assert wrapper["output_kind_errors"] is None
    # Elision (the __ir value_ref rule): the payload is serialized ONCE per
    # event, on the frame's own `output` field.
    assert wrapper["output"] is None
    assert wrapper["output_ref"] == "output"
    assert completed[0]["output"] == {"result": "ok", "__kind": "test_result"}
    import json as _json

    assert '"result"' not in _json.dumps(wrapper)


class _UndeclaredExecutor:
    """A node that declares no kinds — undeclared stays undeclared."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.undeclared",
        category=NodeCategory.DATA,
        display_name="Undeclared node",
        description="Declares no platform kinds at all.",
        input_schema=_Input,
        output_schema=_Output,
        config_schema=_Config,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(
        self,
        _ctx: NodeExecutionContext,
        _inputs: _Input,
        _config: _Config,
    ) -> NodeResult[_Output]:
        return success(_Output(result="ok"))


def _undeclared_definition() -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "u1",
                    "type": "test.undeclared",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [],
        }
    )


async def test_wrapper_reports_an_undeclared_node_honestly():
    """No kind declared is a NULL slug and a neutral verdict — never a pass."""
    _, _, emitter = await _run_capture(
        _undeclared_definition(),
        "kind-wrapper-bare",
        extra_executors=(_UndeclaredExecutor(),),
    )
    wrapper = _events(emitter, "node_completed")[0]["wrapper"]
    assert wrapper["__kind"] == "node_outcome"
    assert wrapper["output_kind"] is None
    assert wrapper["output_kind_ok"] is None
    assert wrapper["output_ref"] == "output"


async def test_wrapper_carries_the_drift_verdict_when_family_off(monkeypatch):
    """A drifting output still gets a wrapper — it just says it failed. This
    is an OFF-mode-only observation: with workflow_io ON (the shipped
    default) genuine drift ERRORS the run and no node_completed (so no
    completion wrapper) ever ships for it — see
    ``test_output_kind_drift_is_fatal_when_family_on``, whose node_failed
    wrapper carries the failure instead. Pinned here with the family
    explicitly off, the exact override the constant's own docstring
    prescribes."""
    monkeypatch.setitem(kinds_mod.KIND_ENFORCEMENT, "workflow_io", False)
    _seed_kind("test_strict_input", {})
    _seed_kind(
        "test_result",
        {
            "type": "object",
            "properties": {"result": {"type": "number"}},
            "required": ["result"],
        },
    )
    _, _, emitter = await _run_capture(_definition(), "kind-wrapper-drift")
    wrapper = _events(emitter, "node_completed")[0]["wrapper"]
    assert wrapper["output_kind"] == "test_result"
    assert wrapper["output_kind_ok"] is False
    assert wrapper["output_kind_errors"]


# ------------------------------------------- pass-through nodes, REAL nodes
#
# The burn-down ledger left `data.transform`, `output.to_frontend` and
# `tool.call` blocked: "reshapes whatever flows through, no fixed contract".
# Runtime propagation is what covers them — a node with NO declared kind
# settles with the ``__kind`` its payload carries, verified against the
# registry like any declaration. These tests prove it on the REAL builtin
# nodes rather than a purpose-built stand-in, which is the evidence the ledger
# asked for before flipping those rows (2026-08-21).


def _seed_flow_kind() -> None:
    _seed_kind(
        "test_flow_result",
        {
            "type": "object",
            "properties": {"result": {"type": "string"}},
            "required": ["result"],
        },
    )


def _passthrough_definition(node_type: str, expression: str | None) -> Definition:
    """source (declares a kind) → the real pass-through node under test."""
    node: dict[str, Any] = {
        "id": "through",
        "type": node_type,
        "position": {"x": 200, "y": 0},
        "data": {"config": {}, "input": {}},
    }
    if expression is not None:
        node["data"]["config"] = {"expression": expression}
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "src",
                    "type": "test.flow_through",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}, "input": {}},
                },
                node,
            ],
            "edges": [{"id": "e1", "source": "src", "target": "through"}],
        }
    )


async def test_data_transform_propagates_the_kind_that_flowed_through():
    """`data.transform` passing its payload through keeps the payload's identity.

    This is the whole reason the row could be unblocked: the node cannot
    DECLARE a kind (its shape is the author's expression), but it does not need
    to — what comes out says what it is.
    """
    _seed_flow_kind()
    result, checkpointer, emitter = await _run_capture(
        _passthrough_definition("data.transform", "inputs"),
        "kind-passthrough-transform",
        extra_executors=(_FlowThroughExecutor(),),
    )
    assert result.status is RunStatus.COMPLETED, result.error

    outcome = await checkpointer.get_outcome("kind-passthrough-transform", 1, "through", 1)
    assert outcome is not None
    assert outcome.output_kind == "test_flow_result", outcome.output_kind
    assert outcome.output_kind_ok is True
    completed = [e for e in _events(emitter, "node_completed") if e["node_id"] == "through"]
    assert completed and completed[0]["output_kind"] == "test_flow_result"


async def test_a_transform_that_REBUILDS_its_payload_claims_no_kind():
    """The honest other half: rebuild the object and identity does NOT travel.

    Propagation must never invent a kind for data that stopped being that
    thing — an undeclared node whose payload says nothing settles with
    nothing, which is exactly what the auto-mint removal was for.
    """
    _seed_flow_kind()
    result, checkpointer, _ = await _run_capture(
        _passthrough_definition("data.transform", "{'result': inputs['result'] + '!'}"),
        "kind-passthrough-rebuilt",
        extra_executors=(_FlowThroughExecutor(),),
    )
    assert result.status is RunStatus.COMPLETED, result.error

    outcome = await checkpointer.get_outcome("kind-passthrough-rebuilt", 1, "through", 1)
    assert outcome is not None
    assert outcome.output_kind is None, (
        "a rebuilt payload carries no identity and must not be given one"
    )


async def test_output_to_frontend_propagates_the_kind_that_flowed_through():
    _seed_flow_kind()
    result, checkpointer, _ = await _run_capture(
        _passthrough_definition("output.to_frontend", None),
        "kind-passthrough-frontend",
        extra_executors=(_FlowThroughExecutor(),),
    )
    assert result.status is RunStatus.COMPLETED, result.error

    outcome = await checkpointer.get_outcome("kind-passthrough-frontend", 1, "through", 1)
    assert outcome is not None
    assert outcome.output_kind == "test_flow_result", outcome.output_kind
    assert outcome.output_kind_ok is True


async def test_output_to_frontend_emission_carries_the_verified_kind_envelope():
    """The emission makes the SAME kind hand-off node_completed makes.

    A `__kind` payload that passes the registry check ships `kind`,
    `kind_ok=True` and the wire-elided Content IR envelope at
    `metadata.__ir` on the node_emitted event — what lets the screen render
    the real kind component (the showcase) instead of a JSON dump.
    """
    _seed_flow_kind()
    result, _, emitter = await _run_capture(
        _passthrough_definition("output.to_frontend", None),
        "kind-emit-envelope",
        extra_executors=(_FlowThroughExecutor(),),
    )
    assert result.status is RunStatus.COMPLETED, result.error

    emitted = _events(emitter, "node_emitted")
    assert len(emitted) == 1
    ev = emitted[0]
    assert ev["payload"]["__kind"] == "test_flow_result"
    assert ev["kind"] == "test_flow_result"
    assert ev["kind_ok"] is True
    ir = ev["metadata"]["__ir"]
    assert ir["root"]["kind"] == "test_flow_result"
    # Wire-elided: the payload rides the event's own `payload` field once.
    assert ir["root"].get("value_ref") == "output"


async def test_output_to_frontend_emission_without_kind_is_neutral():
    """No `__kind` → no verdict, no envelope: the consumer classifies locally."""
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "src",
                    "type": "test.undeclared",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}, "input": {}},
                },
                {
                    "id": "through",
                    "type": "output.to_frontend",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {}, "input": {}},
                },
            ],
            "edges": [{"id": "e1", "source": "src", "target": "through"}],
        }
    )
    result, _, emitter = await _run_capture(
        definition, "kind-emit-neutral", extra_executors=(_UndeclaredExecutor(),)
    )
    assert result.status is RunStatus.COMPLETED, result.error
    ev = _events(emitter, "node_emitted")[0]
    assert ev["kind"] is None and ev["kind_ok"] is None and ev["metadata"] is None
