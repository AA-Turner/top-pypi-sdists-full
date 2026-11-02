"""A connection whose mapped path reads NOTHING at run time raises a review flag — never silent.

Live 2026-10-27 (Smart Add email unit, workflow 4df72f69): the edge read ``last_outputs.result.results`` from a
child that had stopped returning it. Since c55a38c1 such a miss arrives ABSENT (right: data, not wiring), but the
run then said ``completed`` with empty findings for hours and nobody was told. Contract (scheduler
``_queue_mapping_miss``): ONE ``engine.mapping_read_nothing`` flag (category ``unexpected_path``) per (run, edge,
path), naming the connection, the target input, the source step and the path; the run still completes.

Not flagged — nothing was misread: a present path; a conditional connection that was not taken; a ``[*]`` path over
an empty list (an empty fan-out honestly reads ``[]``); an ERROR connection's failure record.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
from pydantic import BaseModel, ConfigDict

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeCategory,
    NodeRegistry,
    NodeSpec,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
    run_log,
)
from matrx_graph.run_log import RunLogEntry
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.result import NodeResult, failure, success
from tests._fixtures import FakeEmitter, make_app_context

LABEL = "engine.mapping_read_nothing"


class _Parts(BaseModel):
    model_config = ConfigDict(extra="forbid")
    local: str
    domain: str


class _ParseOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    first: _Parts | None = None
    items: list[_Parts] = []
    found: int = 0


class _ParseCfg(BaseModel):
    text: str = ""
    fail: bool = False


class _Parse:
    """``first`` is null and ``items`` empty when the text holds no email."""

    spec = NodeSpec(
        type="test.parse_email_flag",
        category=NodeCategory.CUSTOM,
        display_name="Parse email",
        output_schema=_ParseOut,
        config_schema=_ParseCfg,
        handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
    )

    async def execute(self, ctx: NodeExecutionContext, inputs, config) -> NodeResult[_ParseOut]:
        if config.fail:
            return failure("parse_failed", "could not parse")
        if "@" not in config.text:
            return success(_ParseOut())
        local, domain = config.text.split("@", 1)
        parts = _Parts(local=local, domain=domain)
        return success(_ParseOut(first=parts, items=[parts], found=1))


class _Recorder:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    async def __call__(self, **kw: Any) -> RunLogEntry:
        self.rows.append(kw)
        return RunLogEntry(recorded=True, entry_id=str(len(self.rows)), label=kw["label"], needs_review=kw["needs_review"])

    def flags(self) -> list[dict[str, Any]]:
        return [r for r in self.rows if r["needs_review"] and r["label"] == LABEL]


@pytest.fixture
def recorder() -> Iterator[_Recorder]:
    rec = _Recorder()
    run_log.configure_run_log_writer(rec)
    try:
        yield rec
    finally:
        run_log.configure_run_log_writer(None)


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(_Parse())
    return reg


USE = {"config": {"expression": "{'domain': inputs['domain'] if 'domain' in inputs else ''}"}}


def _definition(text: str, *, source_path: str = "first.domain", edge: dict | None = None, fail: bool = False) -> dict:
    return {
        "nodes": [
            {"id": "parse", "type": "test.parse_email_flag", "position": {"x": 0, "y": 0},
             "data": {"label": "Parse email", "config": {"text": text, "fail": fail}}},
            {"id": "use", "type": "data.transform", "position": {"x": 200, "y": 0}, "data": USE},
        ],
        "edges": [
            {"id": "e_domain", "source": "parse", "target": "use",
             "data": edge or {"kind": "data", "mappings": {"domain": source_path}}},
        ],
        "entry_nodes": ["parse"],
    }


async def _run(defn: dict, run_id: str):
    registry = _registry()
    graph = compile_graph(Definition.model_validate(defn), registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry)
    return await scheduler.run(run_id=run_id)


async def test_a_path_that_reads_nothing_raises_one_flag_and_the_run_completes(recorder: _Recorder):
    result = await _run(_definition("not an email"), "read-nothing")
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["use"] == {"domain": ""}
    flags = recorder.flags()
    assert len(flags) == 1, recorder.rows
    flag = flags[0]
    assert flag["category"] == "unexpected_path"
    assert flag["source"] == "engine"
    assert flag["edge_id"] == "e_domain"
    assert flag["node_id"] == "use"
    assert flag["payload"] == {"from_step": "parse", "path": "first.domain", "input": "domain"}
    assert flag["occurrence_key"] == f"{LABEL}|e_domain|first.domain"
    assert "Parse email" in flag["message"] and "first.domain" in flag["message"]


async def test_a_present_path_raises_no_flag(recorder: _Recorder):
    result = await _run(_definition("press@patagonia.com"), "read-present")
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["use"] == {"domain": "patagonia.com"}
    assert recorder.flags() == []


async def test_a_conditional_connection_not_taken_raises_no_flag(recorder: _Recorder):
    edge = {"kind": "conditional", "condition": "inputs['found'] > 0", "mappings": {"domain": "first.domain"}}
    result = await _run(_definition("not an email", edge=edge), "read-not-taken")
    assert result.status is RunStatus.COMPLETED, result.error
    assert recorder.flags() == []


async def test_a_star_path_over_an_empty_list_raises_no_flag(recorder: _Recorder):
    result = await _run(_definition("not an email", source_path="items[*].domain"), "read-empty-list")
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["use"] == {"domain": []}
    assert recorder.flags() == []


async def test_an_error_connection_reading_the_failure_record_raises_no_flag(recorder: _Recorder):
    # The failure record carries no ``first``; the ERROR connection maps it anyway (absent, not misread).
    edge = {"kind": "error", "mappings": {"domain": "first.domain"}}
    result = await _run(_definition("x", edge=edge, fail=True), "read-error-record")
    assert result.status is RunStatus.COMPLETED, result.error
    assert recorder.flags() == []


async def test_an_error_connection_mapping_a_failure_field_never_parks_the_run(recorder: _Recorder):
    """The failure record is judged as the failure record, never against the step's SUCCESS output schema: the
    source declares only first/items/found (closed), yet ``details.domain`` on an ERROR connection is legal — it
    arrives absent when this failure has no such detail, and ``message`` is delivered (c55a38c1 parked both runs
    as "can never resolve")."""
    edge = {"kind": "error", "mappings": {"domain": "details.domain"}}
    result = await _run(_definition("x", edge=edge, fail=True), "error-record-detail")
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["use"] == {"domain": ""}
    assert recorder.flags() == []

    edge = {"kind": "error", "mappings": {"domain": "message"}}
    result = await _run(_definition("x", edge=edge, fail=True), "error-record-message")
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["use"] == {"domain": "could not parse"}


def test_an_error_connection_mapping_a_failure_field_is_not_a_save_time_wiring_error():
    from matrx_graph.validation import validate_definition

    defn = _definition("x", edge={"kind": "error", "mappings": {"domain": "details.domain"}}, fail=True)
    findings = [i for i in validate_definition(defn, _registry()).issues if i.edge_id == "e_domain"]
    assert not any(i.severity == "error" for i in findings), findings
