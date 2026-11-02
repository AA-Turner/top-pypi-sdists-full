"""Guard (generic-only, 2026-10-26): a deprecated step type screams everywhere an agent looks.

The list lives in ``matrx_graph/deprecated_steps.json`` (empty for real steps; one
``test_fixture`` entry used here). These prove: the list loads, the ONE sentence names the
step / display name / node / workflow / replacement and orders the agent to report it, the
palette descriptor carries the record (Workflow Studio reads it), and a RUN of a deprecated
step logs a WARNING, raises ONE review flag per step per run, writes ONE system_error per
(step type, workflow), and still completes.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from typing import Any

import pytest
from pydantic import BaseModel, ConfigDict

import matrx_utils
from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
    run_log,
)
from matrx_graph import deprecations
from matrx_graph.executor import scheduler as scheduler_module
from matrx_graph.run_log import RunLogEntry
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import NodeCategory, RetryPolicy
from matrx_graph.types.result import NodeResult, success
from tests._fixtures import FakeEmitter, make_app_context

FIXTURE_TYPE = "test.deprecated_fixture"


class _Open(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Out(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = "ok"


class _Step:
    def __init__(self, node_type: str, *, fail_first: bool = False) -> None:
        self.spec = NodeSpec(
            type=node_type,
            category=NodeCategory.DATA,
            display_name="Old Fixture Step",
            input_schema=_Open,
            output_schema=_Out,
            handles=(
                HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
                HandleSpec(id="out", direction=HandleDirection.OUTPUT),
            ),
            retry=RetryPolicy(max_attempts=2 if fail_first else 1),
        )
        self.fail_first = fail_first
        self.calls = 0

    async def execute(self, ctx: NodeExecutionContext, inputs: _Open, config: BaseModel) -> NodeResult[_Out]:
        self.calls += 1
        if self.fail_first and self.calls == 1:
            raise RuntimeError("upstream timed out")
        return success(_Out())


class _Recorder:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    async def __call__(self, **kw: Any) -> RunLogEntry:
        self.rows.append(kw)
        return RunLogEntry(recorded=True, entry_id=str(len(self.rows)), label=kw["label"], needs_review=kw["needs_review"])

    def flags(self, label: str) -> list[dict[str, Any]]:
        return [r for r in self.rows if r["needs_review"] and r["label"] == label]


@pytest.fixture
def fixture_list() -> Iterator[None]:
    with deprecations.use_deprecations(deprecations.fixture_deprecations()):
        yield


@pytest.fixture
def recorder() -> Iterator[_Recorder]:
    rec = _Recorder()
    run_log.configure_run_log_writer(rec)
    try:
        yield rec
    finally:
        run_log.configure_run_log_writer(None)


@pytest.fixture
def captured(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []

    async def fake_capture(exc: BaseException, *, kind: str, **kw: Any) -> None:
        calls.append({"kind": kind, "text": str(exc), **kw})

    monkeypatch.setattr(matrx_utils, "capture_error", fake_capture)
    monkeypatch.setattr(scheduler_module, "_DEPRECATION_CAPTURED", set())
    return calls


def _node(node_id: str, node_type: str) -> dict[str, Any]:
    return {"id": node_id, "type": node_type, "position": {"x": 0, "y": 0}, "data": {"config": {}}}


async def _run(definition: dict[str, Any], *steps: _Step, run_id: str, definition_id: str = "wf-old") -> Any:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    for s in steps:
        reg.register(s, overwrite=True)
    graph = compile_graph(Definition.model_validate(definition), registry=reg)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=reg, definition_id=definition_id
    )
    return await scheduler.run(run_id=run_id)


# ── the list ─────────────────────────────────────────────────────────────────


def test_the_real_list_holds_no_fixture_and_the_fixture_loads() -> None:
    real = deprecations.deprecated_steps()
    assert FIXTURE_TYPE not in real, "the fixture step is never a live deprecation"
    # Owner-approved node-library cleanup (Arman, 2026-10-29, workflows VISION.md).
    owner_approved: set[str] = set()
    assert all(t.startswith("brand.discovery.") or t in owner_approved for t in real), (
        "real deprecations are added by the owner, never by an agent"
    )
    fixtures = deprecations.fixture_deprecations()
    assert [f.step_type for f in fixtures] == [FIXTURE_TYPE]


def test_the_sentence_orders_the_agent_to_report_and_fix(fixture_list: None) -> None:
    dep = deprecations.deprecation_for(FIXTURE_TYPE)
    assert dep is not None
    msg = deprecations.deprecation_message(
        dep, display_name="Old Fixture Step", node_id="n7", workflow_name="Weekly digest", workflow_id="wf-1"
    )
    for part in (
        f"this workflow uses deprecated step {FIXTURE_TYPE} (Old Fixture Step)",
        "in step n7 of workflow 'Weekly digest' (wf-1)",
        "Any agent seeing this message is required to report it immediately",
        "`feedback` tool",
        f"fix it by replacing the step with {dep.replacement}",
        "will stop working when it is deleted",
    ):
        assert part in msg, (part, msg)


def test_usages_are_found_in_raw_and_legacy_prefixed_nodes(fixture_list: None) -> None:
    nodes = [
        _node("a", "data.transform"),
        {"id": "b", "type": "data", "data": {"spec_type": FIXTURE_TYPE}},
        _node("c", f"action.{FIXTURE_TYPE}"),
    ]
    found = deprecations.find_deprecated_usages(nodes, workflow_id="wf-1", workflow_name="X")
    assert [u.node_id for u in found] == ["b", "c"]
    assert "step b of workflow 'X' (wf-1)" in found[0].message


def test_no_list_no_usages() -> None:
    assert deprecations.find_deprecated_usages([_node("b", FIXTURE_TYPE)], workflow_id="wf") == []


def test_the_palette_descriptor_carries_the_record(fixture_list: None) -> None:
    entry = _Step(FIXTURE_TYPE).spec.to_palette_descriptor()["deprecation"]
    assert entry is not None and entry["replacement"]
    assert _Step("test.fine_step").spec.to_palette_descriptor()["deprecation"] is None


# ── the run ──────────────────────────────────────────────────────────────────


async def test_a_run_screams_once_per_step_and_still_completes(
    fixture_list: None, recorder: _Recorder, captured: list[dict[str, Any]], caplog: pytest.LogCaptureFixture
) -> None:
    old = _Step(FIXTURE_TYPE, fail_first=True)
    definition = {
        "nodes": [_node("old1", FIXTURE_TYPE), _node("old2", FIXTURE_TYPE)],
        "edges": [{"id": "e1", "source": "old1", "target": "old2", "data": {"kind": "data"}}],
    }
    with caplog.at_level(logging.WARNING, logger=scheduler_module.__name__):
        result = await _run(definition, old, run_id="dep-run-1")
    assert result.status is RunStatus.COMPLETED, result.error

    flags = recorder.flags(deprecations.DEPRECATED_STEP_FLAG_LABEL)
    # old1 runs twice (one retry) and old2 once — still exactly one flag per step.
    assert sorted(f["node_id"] for f in flags) == ["old1", "old2"], recorder.rows
    assert "required to report it immediately" in flags[0]["message"]

    warnings = [r.getMessage() for r in caplog.records if "DEPRECATED STEP IN USE" in r.getMessage()]
    assert len(warnings) == 3, warnings  # every attempt logs

    assert len(captured) == 1, captured  # one system_error per (step type, workflow)
    assert captured[0]["kind"] == deprecations.DEPRECATED_STEP_ERROR_KIND
    assert captured[0]["context"]["workflow_id"] == "wf-old"

    await _run(definition, _Step(FIXTURE_TYPE), run_id="dep-run-2")
    assert len(captured) == 1, "the same workflow's second run must not add a second system_error"
    await _run(definition, _Step(FIXTURE_TYPE), run_id="dep-run-3", definition_id="wf-other")
    assert len(captured) == 2


async def test_a_clean_step_never_screams(
    fixture_list: None, recorder: _Recorder, captured: list[dict[str, Any]]
) -> None:
    result = await _run({"nodes": [_node("fine", "test.fine_step")], "edges": []}, _Step("test.fine_step"), run_id="ok")
    assert result.status is RunStatus.COMPLETED
    assert recorder.flags(deprecations.DEPRECATED_STEP_FLAG_LABEL) == []
    assert captured == []
