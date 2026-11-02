"""Type-contract audit engine — ruleset semantics."""

from __future__ import annotations

from typing import Any

from matrx_graph.contracts import (
    RULESET_V1,
    ConformanceState,
    LeakRule,
    audit_model,
    audit_registry,
)
from pydantic import BaseModel, ConfigDict


class _Clean(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    count: int
    ratio: float | None = None


class _CleanParent(BaseModel):
    model_config = ConfigDict(extra="forbid")
    child: _Clean
    children: list[_Clean]
    tags: list[str]
    lookup: dict[str, int]


class _DeepLeak(BaseModel):
    model_config = ConfigDict(extra="forbid")
    meta: dict[str, Any]


class _PartialParent(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str
    nested: _DeepLeak


class _Open(BaseModel):
    model_config = ConfigDict(extra="allow")
    x: int


class _Cyclic(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    parent: "_Cyclic | None" = None


def test_fully_conformant_recursive():
    report = audit_model(_CleanParent)
    assert report.state is ConformanceState.FULL
    assert report.leaks == []


def test_top_level_any_is_non_conformant():
    report = audit_model(_DeepLeak)
    assert report.state is ConformanceState.NON_CONFORMANT
    (leak,) = report.leaks
    assert leak.rule is LeakRule.ANY
    assert leak.path == "meta[value]"
    assert leak.depth == 0


def test_deep_leak_is_partial_with_exact_path():
    report = audit_model(_PartialParent)
    assert report.state is ConformanceState.PARTIAL
    (leak,) = report.leaks
    assert leak.path == "nested.meta[value]"
    assert leak.depth == 1
    assert leak.owner_model == "_DeepLeak"


def test_extra_allow_flagged():
    report = audit_model(_Open)
    assert report.state is ConformanceState.NON_CONFORMANT
    assert any(leak.rule is LeakRule.EXTRA_ALLOW for leak in report.leaks)


def test_bare_container_and_object():
    class _Bare(BaseModel):
        items: list
        blob: object

    report = audit_model(_Bare)
    rules = {leak.path: leak.rule for leak in report.leaks}
    assert rules["items"] is LeakRule.BARE_CONTAINER
    assert rules["blob"] is LeakRule.OBJECT


def test_union_arms_each_checked():
    class _U(BaseModel):
        value: int | dict[str, Any]

    report = audit_model(_U)
    (leak,) = report.leaks
    assert leak.path == "value[value]"
    assert leak.rule is LeakRule.ANY


def test_cycle_is_not_a_leak():
    report = audit_model(_Cyclic)
    assert report.state is ConformanceState.FULL
    assert report.cyclic is True


def test_registry_audit_totals_and_model_blast_radius():
    from matrx_graph import NodeRegistry, register_builtin_nodes

    reg = NodeRegistry()
    register_builtin_nodes(reg)
    report = audit_registry(reg)
    from matrx_graph.contracts import RULESET_V3

    assert report.ruleset.version == RULESET_V3.version
    assert report.totals.nodes == len(reg.all_types())
    assert (
        report.totals.full
        + report.totals.dynamic
        + report.totals.partial
        + report.totals.non_conformant
        == report.totals.nodes
    )
    # Shared models carry a blast radius: HttpResponse-style shapes are
    # referenced by several http.* nodes.
    multi = [m for m in report.models if len(m.referenced_by) >= 2]
    assert multi, "expected at least one shared model with multiple referrers"
    # Every node report is JSON-serializable end to end.
    assert report.model_dump_json()


class _CycleA(BaseModel):
    model_config = ConfigDict(extra="forbid")
    leaky: dict
    b: "_CycleB | None" = None


class _CycleB(BaseModel):
    model_config = ConfigDict(extra="forbid")
    a: _CycleA | None = None


_CycleA.model_rebuild()


def test_mutual_cycle_no_cache_poisoning():
    # Auditing A first must not cache B's truncated (cycle-cut) walk as
    # B's standalone result — B genuinely leaks through its reference to A.
    from matrx_graph.contracts.audit import RULESET_V1, _Auditor

    auditor = _Auditor(RULESET_V1)
    report_a = auditor.audit_schema(_CycleA)
    report_b = auditor.audit_schema(_CycleB)
    assert report_a.state is ConformanceState.NON_CONFORMANT
    assert report_b.state is ConformanceState.PARTIAL
    assert any("a.leaky" in leak.path for leak in report_b.leaks)


def test_computed_fields_audited():
    from pydantic import computed_field

    class _WithComputed(BaseModel):
        model_config = ConfigDict(extra="forbid")
        name: str

        @computed_field  # type: ignore[prop-decorator]
        @property
        def blob(self) -> dict:
            return {}

    report = audit_model(_WithComputed)
    assert report.state is ConformanceState.NON_CONFORMANT
    (leak,) = report.leaks
    assert leak.path == "blob"
    assert leak.rule is LeakRule.BARE_CONTAINER


def test_typed_abc_containers_conformant():
    from collections.abc import Mapping, Sequence

    class _Abc(BaseModel):
        model_config = ConfigDict(extra="forbid")
        m: Mapping[str, int]
        s: Sequence[str]
        bad: Mapping[str, Any]

    report = audit_model(_Abc)
    (leak,) = report.leaks
    assert leak.path == "bad[value]"
    assert leak.rule is LeakRule.ANY


def test_jsonvalue_is_the_blessed_dynamic_primitive():
    from pydantic import JsonValue

    class _Dyn(BaseModel):
        model_config = ConfigDict(extra="forbid")
        body: JsonValue
        rows: list[dict[str, JsonValue]]

    report = audit_model(_Dyn)
    assert report.state is ConformanceState.FULL


class _AcknowledgedDynamic(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={"x-contract-dynamic": "raw provider item passthrough"},
    )
    x: int


def test_acknowledged_dynamic_is_dynamic_with_reason():
    report = audit_model(_AcknowledgedDynamic)
    assert report.state is ConformanceState.DYNAMIC
    (leak,) = report.leaks
    assert leak.rule is LeakRule.ACKNOWLEDGED_DYNAMIC
    assert leak.annotation == 'extra="allow" — raw provider item passthrough'


def test_acknowledged_plus_real_leak_keeps_real_state():
    class _AckedButLeaky(BaseModel):
        model_config = ConfigDict(
            extra="allow",
            json_schema_extra={"x-contract-dynamic": "open by design"},
        )
        blob: Any

    report = audit_model(_AckedButLeaky)
    assert report.state is ConformanceState.NON_CONFORMANT  # the Any wins
    rules = {leak.rule for leak in report.leaks}
    assert rules == {LeakRule.ACKNOWLEDGED_DYNAMIC, LeakRule.ANY}


def test_callable_json_schema_extra_is_not_an_acknowledgment():
    class _CallableExtra(BaseModel):
        model_config = ConfigDict(
            extra="allow",
            json_schema_extra=lambda schema: schema.update({"x-contract-dynamic": "nope"}),
        )
        x: int

    report = audit_model(_CallableExtra)
    assert report.state is ConformanceState.NON_CONFORMANT
    (leak,) = report.leaks
    assert leak.rule is LeakRule.EXTRA_ALLOW


def test_empty_reason_is_not_an_acknowledgment():
    class _EmptyReason(BaseModel):
        model_config = ConfigDict(
            extra="allow",
            json_schema_extra={"x-contract-dynamic": "   "},
        )
        x: int

    report = audit_model(_EmptyReason)
    assert report.state is ConformanceState.NON_CONFORMANT
    (leak,) = report.leaks
    assert leak.rule is LeakRule.EXTRA_ALLOW


def test_acknowledgment_without_extra_allow_does_nothing():
    class _ClosedButAnnotated(BaseModel):
        model_config = ConfigDict(
            extra="forbid",
            json_schema_extra={"x-contract-dynamic": "irrelevant"},
        )
        x: int

    report = audit_model(_ClosedButAnnotated)
    assert report.state is ConformanceState.FULL
    assert report.leaks == []


def test_v2_still_reports_acknowledged_models_as_extra_allow():
    from matrx_graph.contracts import RULESET_V2

    report = audit_model(_AcknowledgedDynamic, ruleset=RULESET_V2)
    assert report.state is ConformanceState.NON_CONFORMANT
    (leak,) = report.leaks
    assert leak.rule is LeakRule.EXTRA_ALLOW


def test_input_role_excuses_acknowledged_dynamic_in_v3():
    from matrx_graph.contracts import RULESET_V3, SchemaRole
    from matrx_graph.contracts.audit import _Auditor

    auditor = _Auditor(RULESET_V3)
    as_input = auditor.audit_schema(_AcknowledgedDynamic, role=SchemaRole.INPUT)
    assert as_input.state is ConformanceState.FULL
    assert as_input.leaks == []


def test_input_role_excuses_extra_allow_only():
    from matrx_graph.contracts import RULESET_V2, SchemaRole
    from matrx_graph.contracts.audit import _Auditor

    class _OpenInput(BaseModel):
        model_config = ConfigDict(extra="allow")
        q: str

    class _OpenLeakyInput(BaseModel):
        model_config = ConfigDict(extra="allow")
        blob: Any

    auditor = _Auditor(RULESET_V2)
    as_input = auditor.audit_schema(_OpenInput, role=SchemaRole.INPUT)
    as_output = auditor.audit_schema(_OpenInput, role=SchemaRole.OUTPUT)
    assert as_input.state is ConformanceState.FULL
    assert as_output.state is ConformanceState.NON_CONFORMANT
    leaky = auditor.audit_schema(_OpenLeakyInput, role=SchemaRole.INPUT)
    assert leaky.state is ConformanceState.NON_CONFORMANT  # Any still counts
