"""Named degraded mode + compile-time schema validity + enforcement flags.

Content-IR Wave 1 (lane W1-G). Every kind-validation fail-open is a named,
enumerable ``KindDegradedReason`` — surfaced on the KindCheck envelope, in
logs, and on events/outcomes — and per-family fatal enforcement flags
(``matrx_graph.kinds.KIND_ENFORCEMENT``, a code constant, default OFF) escalate per the documented
matrix: everything fatal when ON except ``catalog_unreachable``, which stays
loudly degraded (an infra outage must never masquerade as validation success
OR take down execution).

Flags are flipped ONLY inside these tests (monkeypatch.setenv).
"""

from __future__ import annotations

import time
from typing import Any, ClassVar

from pathlib import Path

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
from matrx_graph.errors import CompilationError, ExecutionError
from matrx_graph.executor.schema_validation import schema_validity_errors
from matrx_graph.kinds import (
    KindCheck,
    KindDegradedReason,
    KindEntry,
    check_against_kind,
    degraded_escalation,
    invalidate_kind_catalog_cache,
    KIND_ENFORCEMENT,
    kind_enforcement_enabled,
    resolve_kind,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.content_ir.model import KindModel
from pydantic import BaseModel, ConfigDict, Field, RootModel

from tests._fixtures import FakeEmitter, make_app_context


@pytest.fixture(autouse=True)
def _clean_kind_cache():
    invalidate_kind_catalog_cache()
    yield
    invalidate_kind_catalog_cache()


# --------------------------------------------------------------- fakes


class _FakeRow:
    """Duck-typed content_ir.kind_definition row for the catalog manager."""

    def __init__(
        self,
        kind: str,
        emitted_json_schema: dict[str, Any] | None,
        *,
        is_active: bool = True,
        version: int = 1,
    ) -> None:
        self.kind = kind
        self.emitted_json_schema = emitted_json_schema
        self.is_active = is_active
        self.version = version
        self.label = kind
        self.deleted_at = None
        self.published_to_web = True


def _fake_manager(rows_by_slug: dict[str, list[_FakeRow]]):
    class _Mgr:
        @staticmethod
        async def load_items(kind: str):
            return rows_by_slug.get(kind, [])

    return _Mgr()


def _broken_manager():
    class _Mgr:
        @staticmethod
        async def load_items(kind: str):
            raise RuntimeError("db not wired")

    return _Mgr()


def _seed_entry(slug: str, entry: KindEntry | None) -> None:
    kinds_mod._cache[slug] = (time.monotonic(), entry)


# ------------------------------------------- degraded reasons (unit)


async def test_degraded_kind_not_registered(monkeypatch, caplog):
    monkeypatch.setattr(kinds_mod, "_manager", lambda: _fake_manager({}))
    with caplog.at_level("ERROR"):
        check = await check_against_kind({"x": 1}, "ghost_kind")
    assert check.checked is False
    assert check.degraded_reason is KindDegradedReason.KIND_NOT_REGISTERED
    assert check.kind_version is None
    assert any("degraded_reason=kind_not_registered" in r.message for r in caplog.records)


async def test_degraded_catalog_unreachable_and_uncached(monkeypatch, caplog):
    monkeypatch.setattr(kinds_mod, "_manager", _broken_manager)
    with caplog.at_level("ERROR"):
        check = await check_against_kind({"x": 1}, "any_kind")
    assert check.checked is False
    assert check.degraded_reason is KindDegradedReason.CATALOG_UNREACHABLE
    assert any("degraded_reason=catalog_unreachable" in r.message for r in caplog.records)
    # Transient infra failure must NOT be cached: once the catalog is back,
    # the very next resolution succeeds.
    monkeypatch.setattr(
        kinds_mod,
        "_manager",
        lambda: _fake_manager({"any_kind": [_FakeRow("any_kind", {"type": "object"})]}),
    )
    entry, reason = await resolve_kind("any_kind")
    assert reason is None
    assert entry is not None and entry.version == 1


async def test_degraded_schema_unavailable(monkeypatch, caplog):
    monkeypatch.setattr(
        kinds_mod,
        "_manager",
        lambda: _fake_manager({"bare_kind": [_FakeRow("bare_kind", None, version=3)]}),
    )
    with caplog.at_level("ERROR"):
        check = await check_against_kind({"x": 1}, "bare_kind")
    assert check.checked is False
    assert check.degraded_reason is KindDegradedReason.SCHEMA_UNAVAILABLE
    # The registry row DID resolve — version/active still travel.
    assert check.kind_version == 3
    assert check.kind_active is True
    assert any("degraded_reason=schema_unavailable" in r.message for r in caplog.records)


async def test_degraded_schema_invalid(monkeypatch, caplog):
    monkeypatch.setattr(
        kinds_mod,
        "_manager",
        lambda: _fake_manager(
            {"bad_schema_kind": [_FakeRow("bad_schema_kind", {"type": "banana"})]}
        ),
    )
    with caplog.at_level("ERROR"):
        check = await check_against_kind({"x": 1}, "bad_schema_kind")
    assert check.checked is False
    assert check.degraded_reason is KindDegradedReason.SCHEMA_INVALID
    assert check.kind_version == 1
    assert any("degraded_reason=schema_invalid" in r.message for r in caplog.records)


async def test_inactive_kind_still_validates_when_enforcement_off(monkeypatch):
    """Ratified engine semantics: is_active is the frontend dual-gate flag.
    With enforcement OFF an inactive kind validates normally — no degradation
    (the seeded workflow-I/O kinds are is_active=false and must keep working)."""
    monkeypatch.setattr(
        kinds_mod,
        "_manager",
        lambda: _fake_manager(
            {
                "sleepy_kind": [
                    _FakeRow(
                        "sleepy_kind",
                        {"type": "object", "required": ["a"], "properties": {"a": {}}},
                        is_active=False,
                    )
                ]
            }
        ),
    )
    check = await check_against_kind({"a": 1}, "sleepy_kind")
    assert check.checked is True
    assert check.errors == []
    assert check.degraded_reason is None
    assert check.kind_active is False  # truth carried for enforcement callers


# -------------------------------------- metaschema check (unit)


def test_schema_validity_errors_accepts_valid_schema():
    assert (
        schema_validity_errors(
            {"type": "object", "properties": {"x": {"type": "integer"}}, "required": ["x"]}
        )
        == []
    )
    assert schema_validity_errors({}) == []  # "any value" is a valid schema


def test_schema_validity_errors_rejects_malformed_schema():
    findings = schema_validity_errors({"type": "banana"})
    assert findings and "banana" in findings[0]
    findings = schema_validity_errors({"type": "object", "required": "not-a-list"})
    assert findings


def test_schema_validity_errors_rejects_non_dict():
    assert schema_validity_errors(["not", "a", "schema"]) == [
        "schema must be a JSON object, got list"
    ]


# ------------------------------------ flags + escalation matrix


def test_enforcement_is_a_code_constant_and_workflow_io_is_on(monkeypatch):
    """The invariant is that this is a CODE constant, never an env read (see
    ``test_the_env_var_can_never_come_back``) -- overridden IN CODE, in
    tests, via ``monkeypatch.setitem``. The committed value for
    ``workflow_io`` is ON (flipped 2026-08-26, Arman-authorized: "if those
    are problematic, let's get rid of them, but then we just need to do the
    legwork to make sure that nothing breaks"; pre-flight record:
    common-docs/projects/archive/kind-directives/PLAN.md § Enforcement pre-flight) --
    this constant IS the deployed behavior of every server, container and
    sandbox at once, and the pre-flight comment documenting that legwork must
    stay in the source (rolling back is editing the line, not deleting the
    evidence)."""
    assert KIND_ENFORCEMENT == {"workflow_io": True}, (
        "the committed enforcement state changed -- this constant IS the "
        "deployed behavior of every server, container and sandbox at once."
    )
    assert kind_enforcement_enabled("workflow_io") is True
    monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", False)
    assert kind_enforcement_enabled("workflow_io") is False

    import matrx_graph.kinds as kinds_module

    source = Path(kinds_module.__file__).read_text(encoding="utf-8")
    assert "FLIPPED ON 2026-08-26" in source
    assert "kind-directives/PLAN.md" in source and "Enforcement" in source


def test_the_env_var_can_never_come_back(monkeypatch):
    """🚨 THE FORCING FUNCTION. `MATRX_KINDS_ENFORCE_*` was an env var until
    2026-08-25 and Arman deleted it by ruling: a toggle in the environment
    means local, server, container and sandbox can disagree about the same
    code, and the divergence is invisible until it produces a bug nobody can
    reproduce. Leniency in CODE is fine -- one push and the whole universe
    enforces the identical rule.

    So setting the retired variable must do NOTHING, whatever the CODE
    constant's committed value happens to be right now -- the fix is to
    delete the environment read again, never to relax this assertion."""
    before = kind_enforcement_enabled("workflow_io")
    monkeypatch.setenv("MATRX_KINDS_ENFORCE_WORKFLOW_IO", "1")
    assert kind_enforcement_enabled("workflow_io") == before, (
        "MATRX_KINDS_ENFORCE_WORKFLOW_IO is being read again. An env var is a "
        "VALUE, never a TOGGLE -- common-docs/policies/env-vars-are-values-not-toggles.md."
    )
    monkeypatch.setenv("MATRX_KINDS_ENFORCE_WORKFLOW_IO", "0")
    assert kind_enforcement_enabled("workflow_io") == before
    import matrx_graph.kinds as kinds_module

    source = Path(kinds_module.__file__).read_text(encoding="utf-8")
    assert "os.environ" not in source, "kinds.py reads os.environ again."


def test_a_deleted_family_is_loud_not_silently_off():
    """The four inert families (action_io / tool_io / agent_io / render) had a
    flag and ZERO call sites -- a knob for behavior that did not exist. They
    were deleted, not converted. Asking for one now RAISES, because a typo'd
    family silently reading False is indistinguishable from a working gate."""
    for family in ("action_io", "tool_io", "agent_io", "render"):
        with pytest.raises(ValueError, match="Unknown kind-enforcement family"):
            kind_enforcement_enabled(family)


def test_inactive_kinds_are_never_fatal_in_either_mode():
    """`is_active` is the FRONTEND's dual-gate flag; the engine ignores it in
    every mode (Arman, 2026-08-25). Until that ruling, turning enforcement on
    would have made the engine start honoring a flag it had never honored,
    killing runs on 5 bound node types over a display setting."""
    assert degraded_escalation(KindDegradedReason.KIND_INACTIVE) == "degraded"
    scheduler_src = (
        Path(__file__).resolve().parents[1] / "matrx_graph" / "executor" / "scheduler.py"
    ).read_text(encoding="utf-8")
    assert "kind_active is False" not in scheduler_src
    assert "not entry.is_active" not in scheduler_src


def test_enforcement_flag_unknown_family_is_loud():
    with pytest.raises(ValueError, match="Unknown kind-enforcement family"):
        kind_enforcement_enabled("not_a_family")


def test_escalation_matrix():
    assert degraded_escalation(KindDegradedReason.KIND_NOT_REGISTERED) == "fatal"
    assert degraded_escalation(KindDegradedReason.KIND_INACTIVE) == "degraded"
    assert degraded_escalation(KindDegradedReason.SCHEMA_UNAVAILABLE) == "fatal"
    assert degraded_escalation(KindDegradedReason.SCHEMA_INVALID) == "fatal"
    # Infra outage NEVER escalates — degraded-but-not-fatal even when ON.
    assert degraded_escalation(KindDegradedReason.CATALOG_UNREACHABLE) == "degraded"


def test_kindcheck_skip_is_never_a_pass():
    check = KindCheck(checked=False, degraded_reason=KindDegradedReason.SCHEMA_UNAVAILABLE)
    assert check.checked is False and check.errors == []
    # A consumer keying off errors alone would misread this as a pass —
    # the envelope forces the distinction.
    assert check.degraded_reason is not None


# --------------------------------------------- scheduler wiring


class _Input(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Output(BaseModel):
    model_config = ConfigDict(extra="forbid")
    result: str = Field(default="ok")


class _Config(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _KindedExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.enforced",
        category=NodeCategory.DATA,
        display_name="Enforced kinded node",
        description="Declares its I/O as platform kinds.",
        input_schema=_Input,
        output_schema=_Output,
        config_schema=_Config,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        input_kind="enf_input",
        output_kind="enf_result",
    )

    async def execute(
        self,
        _ctx: NodeExecutionContext,
        _inputs: _Input,
        _config: _Config,
    ) -> NodeResult[_Output]:
        return success(_Output(result="ok"))


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
                    "type": "test.enforced",
                    "position": {"x": 0, "y": 0},
                    "data": node_data or {"config": {}},
                },
            ],
            "edges": [],
        }
    )


async def _run_capture(definition: Definition, run_id: str):
    registry = _registry()
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


_GOOD_INPUT = {"type": "object"}
_GOOD_OUTPUT = {
    "type": "object",
    "properties": {"result": {"type": "string"}},
    "required": ["result"],
}


# ------------------------- verdict envelope with flags OFF (no behavior change)


async def test_flags_off_verdict_carries_version_on_event_and_outcome():
    _seed_entry("enf_input", KindEntry(slug="enf_input", version=2, json_schema=_GOOD_INPUT))
    _seed_entry("enf_result", KindEntry(slug="enf_result", version=5, json_schema=_GOOD_OUTPUT))
    result, checkpointer, emitter = await _run_capture(_definition(), "enf-ver")
    assert result.status is RunStatus.COMPLETED
    completed = _events(emitter, "node_completed")
    assert completed[0]["output_kind"] == "enf_result"
    assert completed[0]["output_kind_ok"] is True
    assert completed[0]["output_kind_version"] == 5
    assert completed[0]["output_kind_degraded"] is None
    outcome = await checkpointer.get_outcome("enf-ver", 0, "k1", 1)
    assert outcome is not None
    assert outcome.output_kind_version == 5
    assert outcome.output_kind_degraded is None


async def test_flags_off_degraded_reason_stamped_on_event_and_outcome_when_family_off(
    monkeypatch, caplog
):
    """With workflow_io explicitly off -- the exact override the constant's
    own docstring prescribes -- a degraded (unresolvable) output kind stays
    a named, neutral verdict and the run completes. See
    ``test_flag_on_degraded_reason_is_fatal_at_admission`` for the ON-mode
    counterpart (schema_unavailable escalates to FATAL at admission)."""
    monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", False)
    _seed_entry("enf_input", KindEntry(slug="enf_input", version=1, json_schema=_GOOD_INPUT))
    # Registered but schema-less output kind → named degraded, run completes.
    _seed_entry("enf_result", KindEntry(slug="enf_result", version=4, json_schema=None))
    with caplog.at_level("WARNING"):
        result, checkpointer, emitter = await _run_capture(_definition(), "enf-deg")
    assert result.status is RunStatus.COMPLETED
    completed = _events(emitter, "node_completed")
    assert completed[0]["output_kind_ok"] is None  # neutral, never a pass
    assert completed[0]["output_kind_degraded"] == "schema_unavailable"
    assert completed[0]["output_kind_version"] == 4
    outcome = await checkpointer.get_outcome("enf-deg", 0, "k1", 1)
    assert outcome is not None
    assert outcome.output_kind_degraded == "schema_unavailable"
    assert any("degraded_reason=schema_unavailable" in r.message for r in caplog.records)
    assert any("DEGRADED" in r.message for r in caplog.records)


# ------------------- SCHEMA LAW: root `__kind` required by the emitted schema
#
# Feedback 77069e51: the SCHEMA LAW (2026-08-23) makes every
# emitted_json_schema require the root `__kind`. A deterministic node's
# output is a pydantic dump with no marker field — the marker is stamped at
# settlement (STATION 1). The check must therefore validate the candidate
# settlement produces, not the pre-stamp dump, or every plain declared node
# reports output_kind_ok=False with "'__kind' is a required property".

_SCHEMA_LAW_OUTPUT = {
    "type": "object",
    "properties": {
        "__kind": {"type": "string"},
        "result": {"type": "string"},
    },
    "required": ["__kind", "result"],
    "additionalProperties": False,
}


async def test_schema_law_marker_requirement_passes_for_deterministic_node():
    """Regression: run 46c935e8 — all-TRUE definition flipped all-FALSE."""
    _seed_entry("enf_input", KindEntry(slug="enf_input", version=1, json_schema=_GOOD_INPUT))
    _seed_entry(
        "enf_result",
        KindEntry(slug="enf_result", version=7, json_schema=_SCHEMA_LAW_OUTPUT),
    )
    result, checkpointer, emitter = await _run_capture(_definition(), "enf-law")
    assert result.status is RunStatus.COMPLETED
    completed = _events(emitter, "node_completed")
    assert completed[0]["output_kind_ok"] is True
    assert completed[0]["output_kind_errors"] is None
    # The settled payload the event ships carries the marker it was checked
    # with — the check saw the truth, not a fiction.
    assert completed[0]["output"]["__kind"] == "enf_result"
    outcome = await checkpointer.get_outcome("enf-law", 0, "k1", 1)
    assert outcome is not None
    assert outcome.output_kind_ok is True


async def test_schema_law_real_drift_still_fails_and_withholds_stamp_when_family_off(monkeypatch):
    """The candidate stamp must not paper over genuine drift: a schema that
    demands a field the node never emits still fails, and the honesty guard
    still withholds the settlement stamp on the failed verdict. Pinned with
    workflow_io explicitly off -- the exact override the constant's own
    docstring prescribes -- because with the family ON (the shipped default)
    this same drift now ERRORS the run instead of leaving a verdict-only
    node_completed to inspect (see test_flag_on_output_violation_is_execution_failure)."""
    monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", False)
    _seed_entry("enf_input", KindEntry(slug="enf_input", version=1, json_schema=_GOOD_INPUT))
    drifted = {
        "type": "object",
        "properties": {"__kind": {"type": "string"}, "result": {"type": "number"}},
        "required": ["__kind", "result"],
    }
    _seed_entry("enf_result", KindEntry(slug="enf_result", version=1, json_schema=drifted))
    result, _, emitter = await _run_capture(_definition(), "enf-law-drift")
    assert result.status is RunStatus.COMPLETED  # flags off: verdict only
    completed = _events(emitter, "node_completed")
    assert completed[0]["output_kind_ok"] is False
    assert any("result" in e for e in completed[0]["output_kind_errors"])
    # No marker-missing false negative among the errors...
    assert not any("__kind" in e for e in completed[0]["output_kind_errors"])
    # ...and no stamp on a payload that measurably violates its kind.
    assert "__kind" not in completed[0]["output"]


async def test_schema_law_nested_marker_requirement_is_a_modeling_error():
    """The engine stamps the ROOT only. A kind whose schema requires nested
    `__kind` markers that a deterministic producer can never emit is a
    modeling error — the root-stamped candidate must still FAIL on the nested
    requirement (the honest verdict), never be deep-stamped into passing."""
    nested_schema = {
        "type": "object",
        "properties": {
            "__kind": {"type": "string"},
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {"__kind": {"type": "string"}, "text": {"type": "string"}},
                    "required": ["__kind", "text"],
                },
            },
        },
        "required": ["__kind", "items"],
    }
    _seed_entry(
        "nested_kind", KindEntry(slug="nested_kind", version=1, json_schema=nested_schema)
    )
    # What the scheduler's root-only candidate stamp would produce for a
    # deterministic dump: root marker present, nested items bare.
    candidate = {"__kind": "nested_kind", "items": [{"text": "no nested marker"}]}
    check = await check_against_kind(candidate, "nested_kind")
    assert check.checked is True
    assert any("__kind" in e for e in check.errors)


# --------------- STATION 1 boundary cases (run ff8d23c6 / Study Pack v2 class)
#
# The live defect: every deterministic node with a declared kind persisted
# output_kind_ok=false with ONLY "'__kind' is a required property" and shipped
# an unmarked payload — the frontend fell to raw JSON. The candidate check +
# settlement stamp fix that class; these tests pin the stamp's exact boundary
# so it never over-reaches: already-marked payloads stay byte-identical,
# non-dict payloads stay untouched, kind-less nodes stay unstamped.


class _MarkedOutput(KindModel, kind="enf_result"):
    result: str = Field(default="ok")


class _MarkedExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.enforced.marked",
        category=NodeCategory.DATA,
        display_name="KindModel output node",
        description="Output already carries __kind as declared data.",
        input_schema=_Input,
        output_schema=_MarkedOutput,
        config_schema=_Config,
        handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
        determinism=ActionTier.PURE,
        input_kind="enf_input",
        output_kind="enf_result",
    )

    async def execute(
        self, _ctx: NodeExecutionContext, _inputs: _Input, _config: _Config
    ) -> NodeResult[_MarkedOutput]:
        return success(_MarkedOutput(result="ok"))


class _KindlessExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.enforced.kindless",
        category=NodeCategory.DATA,
        display_name="No declared output kind",
        description="Declares no output_kind; payload carries no __kind.",
        input_schema=_Input,
        output_schema=_Output,
        config_schema=_Config,
        handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
        determinism=ActionTier.PURE,
    )

    async def execute(
        self, _ctx: NodeExecutionContext, _inputs: _Input, _config: _Config
    ) -> NodeResult[_Output]:
        return success(_Output(result="ok"))


async def _run_single(executor: Any, run_id: str):
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(executor, overwrite=True)
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "k1",
                    "type": executor.spec.node_type,
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [],
        }
    )
    graph = compile_graph(definition, registry=reg)
    checkpointer = MemoryCheckpointer()
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, checkpointer, make_app_context(emitter), registry=reg)
    result = await scheduler.run(run_id=run_id)
    return result, checkpointer, emitter


async def test_station1_already_marked_output_is_byte_identical():
    """A payload that already SAYS what it is (KindModel) is never re-stamped
    or reshaped — the settled wire value is byte-identical to the dump, the
    verdict is a real pass, and the outcome row mirrors the event."""
    _seed_entry("enf_input", KindEntry(slug="enf_input", version=1, json_schema=_GOOD_INPUT))
    _seed_entry(
        "enf_result", KindEntry(slug="enf_result", version=1, json_schema=_SCHEMA_LAW_OUTPUT)
    )
    result, checkpointer, emitter = await _run_single(_MarkedExecutor(), "st1-marked")
    assert result.status is RunStatus.COMPLETED
    completed = _events(emitter, "node_completed")
    expected = _MarkedOutput(result="ok").model_dump(mode="json")
    assert expected["__kind"] == "enf_result"  # the model itself carries it
    import json as _json

    assert _json.dumps(completed[0]["output"], sort_keys=False) == _json.dumps(
        expected, sort_keys=False
    )
    assert completed[0]["output_kind_ok"] is True
    outcome = await checkpointer.get_outcome("st1-marked", 0, "k1", 1)
    assert outcome is not None
    assert outcome.output == completed[0]["output"]
    assert outcome.output_kind_ok is True


async def test_station1_non_dict_dump_is_never_stamped_by_construction():
    """A non-dict value has no root to stamp. A non-dict output cannot lawfully
    complete a run at all (NodeCompletedEvent.output is dict-typed — the wire
    contract), so the seam's guards are defensive: pin them in the source, and
    pin that the kind check itself never mutates a non-dict value."""
    scheduler_src = (
        Path(__file__).resolve().parents[1] / "matrx_graph" / "executor" / "scheduler.py"
    ).read_text(encoding="utf-8")
    # Both the candidate-check injection and the settlement stamp are gated on
    # the dump being a dict — a list/scalar payload can never grow a marker.
    assert scheduler_src.count("isinstance(output_dump, dict)") >= 2, (
        "STATION 1 lost its non-dict guard: both the check_value injection "
        "and the settlement stamp must be gated on isinstance(output_dump, dict)."
    )
    # And the validator itself never mutates the caller's value.
    _seed_entry(
        "enf_list",
        KindEntry(
            slug="enf_list",
            version=1,
            json_schema={"type": "array", "items": {"type": "string"}},
        ),
    )
    value = ["a", "b"]
    check = await check_against_kind(value, "enf_list")
    assert check.checked is True and check.errors == []
    assert value == ["a", "b"]  # untouched — no marker anywhere


async def test_station1_no_declared_kind_stays_unstamped_and_neutral():
    """No declared output_kind + no self-described __kind = NO kind: the
    payload is untouched, the verdict stays neutral (None, never a pass)."""
    result, checkpointer, emitter = await _run_single(_KindlessExecutor(), "st1-kindless")
    assert result.status is RunStatus.COMPLETED
    completed = _events(emitter, "node_completed")
    assert completed[0]["output"] == {"result": "ok"}
    assert "__kind" not in completed[0]["output"]
    assert completed[0]["output_kind"] is None
    assert completed[0]["output_kind_ok"] is None
    outcome = await checkpointer.get_outcome("st1-kindless", 0, "k1", 1)
    assert outcome is not None
    assert outcome.output == {"result": "ok"}
    assert outcome.output_kind is None
    assert outcome.output_kind_ok is None


# ------------------------------------------------ flag ON: fatal behavior


async def test_flag_on_unknown_kind_fatal_at_admission(monkeypatch):
    monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", True)
    _seed_entry("enf_input", None)  # kind_not_registered
    _seed_entry("enf_result", KindEntry(slug="enf_result", version=1, json_schema=_GOOD_OUTPUT))
    with pytest.raises(ExecutionError, match="degraded_reason=kind_not_registered"):
        await _run_capture(_definition(), "enf-admit-unknown")


async def test_flag_on_degraded_reason_is_fatal_at_admission(monkeypatch):
    """Not just kind_not_registered: ANY fatal-escalating degraded reason
    blocks admission with workflow_io ON. Here the output kind is registered
    but schema-less (schema_unavailable), which the escalation matrix marks
    fatal -- the run must not even start."""
    monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", True)
    _seed_entry("enf_input", KindEntry(slug="enf_input", version=1, json_schema=_GOOD_INPUT))
    _seed_entry("enf_result", KindEntry(slug="enf_result", version=1, json_schema=None))
    with pytest.raises(ExecutionError, match="degraded_reason=schema_unavailable"):
        await _run_capture(_definition(), "enf-admit-degraded")


async def test_flag_on_inactive_kind_is_ignored_at_admission(monkeypatch):
    monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", True)
    _seed_entry("enf_input", KindEntry(slug="enf_input", version=1, json_schema=_GOOD_INPUT))
    _seed_entry(
        "enf_result",
        KindEntry(slug="enf_result", version=1, json_schema=_GOOD_OUTPUT, is_active=False),
    )
    result, _, _ = await _run_capture(_definition(), "enf-admit-inactive")
    assert result.status is RunStatus.COMPLETED


async def test_flag_on_output_violation_is_execution_failure(monkeypatch, caplog):
    monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", True)
    _seed_entry("enf_input", KindEntry(slug="enf_input", version=1, json_schema=_GOOD_INPUT))
    # Executor emits {"result": "ok"}; this schema demands a number → drift.
    _seed_entry(
        "enf_result",
        KindEntry(
            slug="enf_result",
            version=1,
            json_schema={
                "type": "object",
                "properties": {"result": {"type": "number"}},
                "required": ["result"],
            },
        ),
    )
    with caplog.at_level("ERROR"):
        result, checkpointer, emitter = await _run_capture(_definition(), "enf-out-fatal")
    assert result.status is not RunStatus.COMPLETED
    # The invalid typed output is NEVER stored as a successful outcome.
    assert _events(emitter, "node_completed") == []
    failed = _events(emitter, "node_failed")
    assert len(failed) == 1
    assert failed[0]["error_type"] == "KindContractViolation"
    outcome = await checkpointer.get_outcome("enf-out-fatal", 0, "k1", 1)
    assert outcome is not None
    assert outcome.output == {}
    assert outcome.error is not None
    assert outcome.error["code"] == "KindContractViolation"
    assert any("FATAL (workflow_io enforcement ON)" in r.message for r in caplog.records)


async def test_flag_off_same_drift_stays_non_fatal(monkeypatch, caplog):
    monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", False)
    _seed_entry("enf_input", KindEntry(slug="enf_input", version=1, json_schema=_GOOD_INPUT))
    _seed_entry(
        "enf_result",
        KindEntry(
            slug="enf_result",
            version=1,
            json_schema={
                "type": "object",
                "properties": {"result": {"type": "number"}},
                "required": ["result"],
            },
        ),
    )
    with caplog.at_level("ERROR"):
        result, _, emitter = await _run_capture(_definition(), "enf-out-loud")
    assert result.status is RunStatus.COMPLETED
    completed = _events(emitter, "node_completed")
    assert completed[0]["output_kind_ok"] is False
    assert any("run continues" in r.message for r in caplog.records)


async def test_flag_on_catalog_unreachable_stays_degraded_not_fatal(monkeypatch, caplog):
    """The outage matrix row: enforcement ON + catalog down → the run still
    completes, loudly degraded — an outage neither passes nor kills."""
    monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", True)
    monkeypatch.setattr(kinds_mod, "_manager", _broken_manager)
    with caplog.at_level("WARNING"):
        result, checkpointer, emitter = await _run_capture(_definition(), "enf-outage")
    assert result.status is RunStatus.COMPLETED
    completed = _events(emitter, "node_completed")
    assert completed[0]["output_kind_ok"] is None  # never a pass
    assert completed[0]["output_kind_degraded"] == "catalog_unreachable"
    outcome = await checkpointer.get_outcome("enf-outage", 0, "k1", 1)
    assert outcome is not None
    assert outcome.output_kind_degraded == "catalog_unreachable"
    assert any("degraded_reason=catalog_unreachable" in r.message for r in caplog.records)


async def test_flag_on_resume_is_gated_like_run(monkeypatch, caplog):
    """F3: a parked run must not bypass fatal binding admission on resume."""
    # Park the run ERRORED with enforcement OFF (input kind violation).
    _seed_entry(
        "enf_input",
        KindEntry(
            slug="enf_input",
            version=1,
            json_schema={
                "type": "object",
                "properties": {"topic": {"type": "string"}},
                "required": ["topic"],
            },
        ),
    )
    _seed_entry("enf_result", KindEntry(slug="enf_result", version=1, json_schema=_GOOD_OUTPUT))
    registry = _registry()
    graph = compile_graph(_definition({"config": {}, "input": {"topic": 42}}), registry=registry)
    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    result = await scheduler.run(run_id="enf-resume")
    assert result.status is not RunStatus.COMPLETED
    last_cp = await checkpointer.latest_checkpoint(run_id="enf-resume")
    assert last_cp is not None
    # Flip enforcement ON with an unregistered binding — resume must be
    # rejected at admission, exactly like run().
    monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", True)
    _seed_entry("enf_input", None)  # kind_not_registered
    resumed = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    with pytest.raises(ExecutionError, match="degraded_reason=kind_not_registered"):
        await resumed.resume(run_id="enf-resume", checkpoint_id=last_cp.checkpoint_id)


async def test_flag_on_kind_violation_is_not_retried(monkeypatch, caplog):
    """F4: a kind-contract violation is deterministic — it must fail once,
    never entering the retry ladder even under a retry-anything policy."""
    monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", True)
    _seed_entry("enf_input", KindEntry(slug="enf_input", version=1, json_schema=_GOOD_INPUT))
    _seed_entry(
        "enf_result",
        KindEntry(
            slug="enf_result",
            version=1,
            json_schema={
                "type": "object",
                "properties": {"result": {"type": "number"}},
                "required": ["result"],
            },
        ),
    )
    with caplog.at_level("ERROR"):
        result, checkpointer, emitter = await _run_capture(
            _definition(
                {
                    "config": {},
                    "retry_policy": {"max_attempts": 3, "initial_delay_ms": 0},
                }
            ),
            "enf-no-retry",
        )
    assert result.status is not RunStatus.COMPLETED
    assert _events(emitter, "node_retry_scheduled") == []
    failed = _events(emitter, "node_failed")
    assert len(failed) == 1 and failed[0]["attempt"] == 1
    assert await checkpointer.get_outcome("enf-no-retry", 0, "k1", 2) is None


async def test_degraded_warning_throttled_per_run_and_slug_when_family_off(monkeypatch, caplog):
    """F1: the run-scoped degraded warning fires once per (run, slug), not
    once per node execution. Pinned with workflow_io explicitly off, because
    the degraded reason under test (schema_unavailable) escalates to FATAL
    at admission with the family ON (the shipped default) -- see
    test_flag_on_degraded_reason_is_fatal_at_admission -- which would stop
    the run before either node executes."""
    monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", False)
    _seed_entry("enf_input", KindEntry(slug="enf_input", version=1, json_schema=_GOOD_INPUT))
    _seed_entry("enf_result", KindEntry(slug="enf_result", version=1, json_schema=None))
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "k1",
                    "type": "test.enforced",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}},
                },
                {
                    "id": "k2",
                    "type": "test.enforced",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [
                {"id": "e1", "source": "k1", "target": "k2"},
            ],
        }
    )
    with caplog.at_level("WARNING"):
        result, _, emitter = await _run_capture(definition, "enf-throttle")
    assert result.status is RunStatus.COMPLETED
    # Both executions still carry the degraded reason on the wire…
    completed = _events(emitter, "node_completed")
    assert len(completed) == 2
    assert all(p["output_kind_degraded"] == "schema_unavailable" for p in completed)
    # …but the run-scoped context warning fired exactly once.
    throttled = [r for r in caplog.records if "DEGRADED" in r.message and r.levelname == "WARNING"]
    assert len(throttled) == 1


# --------------------------------------- compile-time schema validity


class _DynConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    def effective_output_json_schema(self) -> dict[str, Any]:
        return {"type": "banana"}  # structurally invalid JSON Schema


class _DynExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.dyn_bad_schema",
        category=NodeCategory.DATA,
        display_name="Dynamic node with a broken compiled schema",
        description="Compiles an invalid effective_output_schema.",
        input_schema=_Input,
        output_schema=_Output,
        config_schema=_DynConfig,
        handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
        determinism=ActionTier.PURE,
        dynamic_output=True,
    )

    async def execute(
        self,
        _ctx: NodeExecutionContext,
        _inputs: _Input,
        _config: _DynConfig,
    ) -> NodeResult[_Output]:
        return success(_Output(result="ok"))


def _dyn_definition() -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "d1",
                    "type": "test.dyn_bad_schema",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [],
        }
    )


def _dyn_registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(_DynExecutor(), overwrite=True)
    return reg


def test_compile_invalid_effective_schema_loud_but_not_fatal_by_default(monkeypatch, caplog):
    monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", False)
    with caplog.at_level("ERROR"):
        graph = compile_graph(_dyn_definition(), registry=_dyn_registry())
    assert "d1" in graph.nodes  # compiled — nothing observable changes when OFF
    assert any("NOT a valid Draft 2020-12 JSON Schema" in r.message for r in caplog.records)


def test_compile_invalid_effective_schema_fatal_when_enforced(monkeypatch):
    monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", True)
    with pytest.raises(CompilationError, match="NOT a valid Draft 2020-12 JSON Schema"):
        compile_graph(_dyn_definition(), registry=_dyn_registry())


def test_compile_valid_effective_schema_untouched(monkeypatch):
    """io.user_input compiles a real schema — must pass the metaschema gate
    even with enforcement ON."""
    monkeypatch.setitem(KIND_ENFORCEMENT, "workflow_io", True)
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "u1",
                    "type": "io.user_input",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"fields": []}},
                },
            ],
            "edges": [],
        }
    )
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    graph = compile_graph(definition, registry=reg)
    assert "u1" in graph.nodes


# ── Keys declared BESIDE the kind (ctx.declare_beside_kind, 2026-10-27) ──────
# Run Typed Agent hands downstream the run's facts (final_text, messages…)
# beside its kind answer so a converted step keeps every door. Those keys are
# not the kind's: the verdict ignores them, the payload keeps them.


class _BesideOutput(BaseModel):
    model_config = ConfigDict(extra="allow")
    result: str = Field(default="ok")


class _BesideExecutor:
    declare: ClassVar[bool] = True
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.enforced.beside",
        category=NodeCategory.DATA,
        display_name="Kind answer plus run facts",
        description="Hands over final_text beside its kind answer.",
        input_schema=_Input,
        output_schema=_BesideOutput,
        config_schema=_Config,
        handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
        determinism=ActionTier.PURE,
        input_kind="enf_input",
        output_kind="enf_result",
    )

    async def execute(
        self, ctx: NodeExecutionContext, _inputs: _Input, _config: _Config
    ) -> NodeResult[_BesideOutput]:
        if self.declare:
            ctx.declare_beside_kind(["final_text"])
        return success(_BesideOutput(result="ok", final_text="the answer"))


class _UndeclaredBesideExecutor(_BesideExecutor):
    declare: ClassVar[bool] = False


@pytest.mark.parametrize(("executor", "ok"), [(_BesideExecutor(), True), (_UndeclaredBesideExecutor(), False)])
async def test_keys_declared_beside_the_kind_pass_the_verdict_and_stay_in_the_payload(executor, ok):
    _seed_entry("enf_input", KindEntry(slug="enf_input", version=1, json_schema=_GOOD_INPUT))
    _seed_entry("enf_result", KindEntry(slug="enf_result", version=1, json_schema=_SCHEMA_LAW_OUTPUT))
    result, _checkpointer, emitter = await _run_single(executor, f"beside-{ok}")
    completed = _events(emitter, "node_completed")
    if not ok:  # an undeclared extra key is real drift (fatal under enforcement)
        assert result.status is not RunStatus.COMPLETED and not completed
        return
    assert result.status is RunStatus.COMPLETED
    assert completed[0]["output_kind_ok"] is True
    assert completed[0]["output"]["final_text"] == "the answer"
