"""One at a time per key (``data.one_at_a_time``) — the real Scheduler, the real in-memory store.

Each rule in ``matrx_graph/one_at_a_time.py`` is driven through ``Scheduler.run``: two runs with
the same key never overlap (the second waits, then works on what the first left), different keys
run side by side, the waiting step says why, a dead holder frees the key when its lease runs out,
my own earlier turn is taken back at once, a failure gives the turn back, nothing is stored, a
missing key part or a broken store runs the step and flags it. Steps are real executors that
record when they were working.
"""

from __future__ import annotations

import asyncio
import dataclasses
import time
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from pydantic import BaseModel, ConfigDict

from matrx_graph import (
    CompilationError,
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
    run_log,
)
from matrx_graph import knobs
from matrx_graph.once import ClaimPosition, MemoryStepResultStore, StepResultKey, configure_step_result_store
from matrx_graph.one_at_a_time import parse_one_at_a_time, turn_key, turn_step_type
from matrx_graph.run_log import RunLogEntry
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory, RetryPolicy
from matrx_graph.types.result import NodeResult, failure, success
from tests._fixtures import FakeEmitter, make_app_context

ORG_A = "11111111-1111-4111-8111-111111111111"
WF = "33333333-3333-4333-8333-333333333333"


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Out(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Document:
    """A shared document two runs read, change and write back — the thing the turn protects."""

    def __init__(self) -> None:
        self.lines: list[str] = []
        self.working = 0
        self.overlaps = 0
        self.spans: list[tuple[str, float, float]] = []


class _Editor:
    """Reads the document, thinks, writes it back with its own line (a lost update if two overlap)."""

    def __init__(self, doc: _Document, *, delay: float = 0.3, fail_first: bool = False) -> None:
        self.spec = NodeSpec(
            type="test.edit",
            category=NodeCategory.DATA,
            display_name="Edit the document",
            description="one-at-a-time test step",
            input_schema=_In,
            output_schema=_Out,
            config_schema=_Cfg,
            handles=(
                HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
                HandleSpec(id="out", direction=HandleDirection.OUTPUT),
            ),
            determinism=ActionTier.NON_DETERMINISTIC,
            retry=RetryPolicy(max_attempts=1),
        )
        self.doc = doc
        self.delay = delay
        self.fail_first = fail_first
        self.calls = 0

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        self.calls += 1
        doc = self.doc
        doc.working += 1
        if doc.working > 1:
            doc.overlaps += 1
        began = time.monotonic()
        try:
            seen = list(doc.lines)
            await asyncio.sleep(self.delay)
            if self.fail_first and self.calls == 1:
                return failure(code="Boom", message="the provider refused")
            reply = (inputs.model_dump(mode="json") or {}).get("reply")
            doc.lines = [*seen, str(reply)]
            return success(_Out(lines=list(doc.lines)))
        finally:
            doc.working -= 1
            doc.spans.append((ctx.run_id, began, time.monotonic()))


class _Recorder:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    async def __call__(self, **kw: Any) -> RunLogEntry:
        self.rows.append(kw)
        return RunLogEntry(recorded=True, entry_id=str(len(self.rows)), label=kw["label"], needs_review=kw["needs_review"])

    def labels(self, *, review: bool | None = None) -> list[str]:
        return [r["label"] for r in self.rows if review is None or r["needs_review"] is review]


@pytest.fixture
def store() -> Iterator[MemoryStepResultStore]:
    s = MemoryStepResultStore()
    configure_step_result_store(s)
    knobs._cache[knobs.ONCE_FEATURE] = (
        time.monotonic() + 10**9,
        {"lease_seconds": 5, "wait_poll_seconds": 1, "keep_days_default": 30},
    )
    _max_wait(600)
    try:
        yield s
    finally:
        configure_step_result_store(None)
        knobs._cache.pop(knobs.ONCE_FEATURE, None)
        knobs._cache.pop(knobs.ONE_AT_A_TIME_FEATURE, None)


def _max_wait(seconds: int) -> None:
    knobs._cache[knobs.ONE_AT_A_TIME_FEATURE] = (time.monotonic() + 10**9, {"max_wait_seconds": seconds})


@pytest.fixture
def log() -> Iterator[_Recorder]:
    rec = _Recorder()
    run_log.configure_run_log_writer(rec)
    try:
        yield rec
    finally:
        run_log.configure_run_log_writer(None)


def _registry(step: _Editor) -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    reg.register(step, overwrite=True)
    return reg


TURN = {"key": ["session_id"], "scope": "workflow"}


def _definition(turn: Any, inputs: dict[str, Any]) -> dict[str, Any]:
    data: dict[str, Any] = {"config": {}, "input": inputs}
    if turn is not None:
        data["one_at_a_time"] = turn
    return {"nodes": [{"id": "edit", "type": "test.edit", "position": {"x": 0, "y": 0}, "data": data}], "edges": []}


async def _run(definition: dict[str, Any], registry: NodeRegistry, run_id: str, *,
               emitter: FakeEmitter | None = None, org: str | None = ORG_A, cancel_check: Any = None):
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    em = emitter or FakeEmitter()
    app = dataclasses.replace(make_app_context(em), organization_id=org, user_id="test-user")
    scheduler = Scheduler(graph, MemoryCheckpointer(), app, registry=registry, definition_id=WF,
                          cancel_check=cancel_check)
    return await scheduler.run(run_id=run_id), em


def _progress(em: FakeEmitter) -> list[str]:
    return [p.get("message", "") for (_n, p) in em.events if isinstance(p, dict) and p.get("event") == "node_progress"]


# ── the promise ──────────────────────────────────────────────────────────────


async def test_two_runs_with_the_same_key_never_overlap_and_no_edit_is_lost(store, log):
    doc = _Document()
    editor = _Editor(doc)
    reg = _registry(editor)
    first = _definition(TURN, {"session_id": "s-1", "reply": "first reply"})
    second = _definition(TURN, {"session_id": "s-1", "reply": "second reply"})
    (r1, _), (r2, _) = await asyncio.gather(_run(first, reg, "run-1"), _run(second, reg, "run-2"))
    assert r1.status is RunStatus.COMPLETED and r2.status is RunStatus.COMPLETED
    assert doc.overlaps == 0, "two runs worked on the same document at once"
    assert sorted(doc.lines) == ["first reply", "second reply"], f"an edit was lost: {doc.lines}"
    assert editor.calls == 2, "the second run must run, never reuse"
    assert store.rows() == {}, "a turn given back leaves no row"


async def test_without_the_setting_two_runs_overlap_and_lose_an_edit(store):
    """The hazard the setting exists for — proves the test above can fail."""
    doc = _Document()
    reg = _registry(_Editor(doc))
    first = _definition(None, {"session_id": "s-1", "reply": "first reply"})
    second = _definition(None, {"session_id": "s-1", "reply": "second reply"})
    await asyncio.gather(_run(first, reg, "run-1"), _run(second, reg, "run-2"))
    assert doc.overlaps == 1 and len(doc.lines) == 1


async def test_different_keys_run_side_by_side(store):
    doc = _Document()
    reg = _registry(_Editor(doc, delay=0.4))
    started = time.monotonic()
    await asyncio.gather(
        _run(_definition(TURN, {"session_id": "s-1", "reply": "a"}), reg, "run-1"),
        _run(_definition(TURN, {"session_id": "s-2", "reply": "b"}), reg, "run-2"),
    )
    assert doc.overlaps == 1, "different keys must not wait for each other"
    assert time.monotonic() - started < 0.75


async def test_the_waiting_step_says_why_on_the_step_and_in_the_run_log(store, log):
    doc = _Document()
    reg = _registry(_Editor(doc, delay=0.3))
    em2 = FakeEmitter()

    async def second() -> Any:
        await asyncio.sleep(0.05)
        return await _run(_definition(TURN, {"session_id": "s-1", "reply": "b"}), reg, "run-2", emitter=em2)

    await asyncio.gather(_run(_definition(TURN, {"session_id": "s-1", "reply": "a"}), reg, "run-1"), second())
    lines = _progress(em2)
    assert any(line.startswith("Waiting its turn: run run-1") for line in lines), lines
    waiting = [r for r in log.rows if r["label"] == "engine.waiting_turn"]
    assert len(waiting) == 1 and waiting[0]["run_id"] == "run-2"
    assert waiting[0]["severity"] == "info" and waiting[0]["needs_review"] is False
    assert waiting[0]["payload"]["holder_run_id"] == "run-1"


async def test_a_dead_holder_frees_the_key_when_its_lease_runs_out(store):
    doc = _Document()
    reg = _registry(_Editor(doc, delay=0.0))
    policy = parse_one_at_a_time(TURN)
    assert policy is not None
    key_value, _ = turn_key(policy, {"session_id": "s-1", "reply": "a"})
    assert key_value is not None
    key = StepResultKey(organization_id=ORG_A, scope="workflow", scope_id=WF,
                        step_type=turn_step_type(policy, "edit"), result_key=key_value)
    # A server that took the turn and died: no renewal, no release.
    assert await store.insert_claim(key, token="dead", position=ClaimPosition(run_id="crashed-run", node_id="edit"),
                                    lease_until=datetime.now(UTC) + timedelta(seconds=0.6))
    started = time.monotonic()
    result, _ = await _run(_definition(TURN, {"session_id": "s-1", "reply": "a"}), reg, "run-1")
    assert result.status is RunStatus.COMPLETED
    assert time.monotonic() - started >= 0.5, "did not wait for the live turn"
    assert store.rows() == {}


async def test_my_own_earlier_turn_is_taken_back_at_once(store):
    reg = _registry(_Editor(_Document(), delay=0.0))
    policy = parse_one_at_a_time(TURN)
    assert policy is not None
    key_value, _ = turn_key(policy, {"session_id": "s-1", "reply": "a"})
    key = StepResultKey(organization_id=ORG_A, scope="workflow", scope_id=WF,
                        step_type=turn_step_type(policy, "edit"), result_key=str(key_value))
    await store.insert_claim(key, token="mine-before-crash", position=ClaimPosition(run_id="run-1", node_id="edit"),
                             lease_until=datetime.now(UTC) + timedelta(minutes=5))
    started = time.monotonic()
    result, _ = await _run(_definition(TURN, {"session_id": "s-1", "reply": "a"}), reg, "run-1")
    assert result.status is RunStatus.COMPLETED
    assert time.monotonic() - started < 2.0


async def test_a_failure_gives_the_turn_back_and_the_waiter_works(store):
    doc = _Document()
    editor = _Editor(doc, delay=0.2, fail_first=True)
    reg = _registry(editor)
    (r1, _), (r2, _) = await asyncio.gather(
        _run(_definition(TURN, {"session_id": "s-1", "reply": "a"}), reg, "run-1"),
        _run(_definition(TURN, {"session_id": "s-1", "reply": "b"}), reg, "run-2"),
    )
    assert sorted([r1.status.value, r2.status.value]) == sorted([RunStatus.COMPLETED.value, RunStatus.ERRORED.value])
    assert doc.overlaps == 0 and editor.calls == 2
    assert store.rows() == {}


async def test_steps_sharing_a_name_share_the_turn_across_workflows(store):
    """A finish workflow and an observe workflow guarding one document: organization scope + name."""
    doc = _Document()
    reg = _registry(_Editor(doc))
    shared = {"key": ["session_id"], "scope": "organization", "name": "interview-document"}

    async def run_in(definition_id: str, run_id: str, reply: str) -> None:
        graph = compile_graph(Definition.model_validate(_definition(shared, {"session_id": "s-1", "reply": reply})),
                              registry=reg)
        app = dataclasses.replace(make_app_context(FakeEmitter()), organization_id=ORG_A, user_id="u")
        await Scheduler(graph, MemoryCheckpointer(), app, registry=reg, definition_id=definition_id).run(run_id=run_id)

    await asyncio.gather(
        run_in("44444444-4444-4444-8444-444444444444", "run-1", "observe"),
        run_in("55555555-5555-4555-8555-555555555555", "run-2", "finish"),
    )
    assert doc.overlaps == 0 and sorted(doc.lines) == ["finish", "observe"]


async def test_a_missing_key_part_runs_and_flags(store, log):
    doc = _Document()
    reg = _registry(_Editor(doc, delay=0.0))
    result, _ = await _run(_definition(TURN, {"reply": "a"}), reg, "run-1")
    assert result.status is RunStatus.COMPLETED and doc.lines == ["a"]
    assert "engine.one_at_a_time_unavailable" in log.labels(review=True)


async def test_a_broken_store_runs_the_step_and_flags(log):
    class _Broken(MemoryStepResultStore):
        async def read(self, key: StepResultKey) -> Any:
            raise ConnectionError("store down")

    configure_step_result_store(_Broken())
    knobs._cache[knobs.ONCE_FEATURE] = (time.monotonic() + 10**9,
                                        {"lease_seconds": 5, "wait_poll_seconds": 1, "keep_days_default": 30})
    try:
        doc = _Document()
        result, _ = await _run(_definition(TURN, {"session_id": "s-1", "reply": "a"}), _registry(_Editor(doc, delay=0.0)), "run-1")
    finally:
        configure_step_result_store(None)
        knobs._cache.pop(knobs.ONCE_FEATURE, None)
    assert result.status is RunStatus.COMPLETED and doc.lines == ["a"]
    assert "engine.one_at_a_time_unavailable" in log.labels(review=True)


def test_an_invalid_setting_fails_compilation():
    reg = _registry(_Editor(_Document()))
    for bad in ({"key": ["a..b"]}, {"scope": "galaxy"}, {"unknown": 1}, "yes", {"name": " "}):
        with pytest.raises(CompilationError):
            compile_graph(Definition.model_validate(_definition(bad, {})), registry=reg)


def test_true_means_the_whole_input_is_the_key():
    policy = parse_one_at_a_time(True)
    assert policy is not None and policy.key == [] and policy.scope == "workflow"
    a, _ = turn_key(policy, {"x": 1})
    b, _ = turn_key(policy, {"x": 2})
    assert a and b and a != b


# ── never stuck: cancel, max wait, self-wait, lost turn, cancel mid-claim ────


def _failed_code(em: FakeEmitter) -> list[str]:
    out = []
    for (_n, p) in em.events:
        if isinstance(p, dict) and p.get("event") == "node_failed":
            err = p.get("error") or {}
            out.append(str(err.get("code") if isinstance(err, dict) else err))
    return out


async def test_cancelling_a_waiting_run_stops_the_wait_and_the_run_ends_cancelled(store):
    doc = _Document()
    editor = _Editor(doc, delay=3.0)
    reg = _registry(editor)
    asked = time.monotonic() + 0.4

    async def cancel_soon() -> bool:
        return time.monotonic() >= asked

    async def second() -> Any:
        await asyncio.sleep(0.05)
        started = time.monotonic()
        result, _ = await _run(_definition(TURN, {"session_id": "s-1", "reply": "b"}), reg, "run-2",
                               cancel_check=cancel_soon)
        return result, time.monotonic() - started

    holder = asyncio.create_task(_run(_definition(TURN, {"session_id": "s-1", "reply": "a"}), reg, "run-1"))
    result, took = await second()
    assert result.status is RunStatus.CANCELLED, result.status
    assert took < 2.5, f"the cancel waited for the holder ({took:.2f}s)"
    assert editor.calls == 1, "the cancelled waiter must never work"
    await holder


async def test_a_wait_past_the_knob_fails_loudly_and_never_runs_unguarded(store):
    _max_wait(1)
    doc = _Document()
    editor = _Editor(doc, delay=3.0)
    reg = _registry(editor)
    em2 = FakeEmitter()

    async def second() -> Any:
        await asyncio.sleep(0.05)
        started = time.monotonic()
        result, _ = await _run(_definition(TURN, {"session_id": "s-1", "reply": "b"}), reg, "run-2", emitter=em2)
        return result, time.monotonic() - started

    holder = asyncio.create_task(_run(_definition(TURN, {"session_id": "s-1", "reply": "a"}), reg, "run-1"))
    result, took = await second()
    assert result.status is RunStatus.ERRORED
    assert 0.9 <= took < 2.5, took
    assert _failed_code(em2) == ["TurnNotTaken"], _failed_code(em2)
    assert "limit is 1 s" in str(result.error)
    assert editor.calls == 1 and doc.overlaps == 0
    await holder


class _Nester:
    """A step that holds the turn and runs a child workflow inline whose step asks for the same turn."""

    def __init__(self, child: dict[str, Any], registry_box: list[NodeRegistry]) -> None:
        self.spec = NodeSpec(
            type="test.nest", category=NodeCategory.DATA, display_name="Run a child",
            description="self-wait test step", input_schema=_In, output_schema=_Out, config_schema=_Cfg,
            handles=(HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
                     HandleSpec(id="out", direction=HandleDirection.OUTPUT)),
            determinism=ActionTier.NON_DETERMINISTIC, retry=RetryPolicy(max_attempts=1),
        )
        self.child = child
        self.box = registry_box
        self.child_status: Any = None

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        result, _ = await _run(self.child, self.box[0], "child-run")
        self.child_status = result.status
        return success(_Out(child=result.status.value))


async def test_a_child_asking_for_its_parents_turn_fails_at_once_and_says_why(store, log):
    shared = {"key": ["session_id"], "scope": "organization", "name": "interview-document"}
    box: list[NodeRegistry] = []
    child = _definition(shared, {"session_id": "s-1", "reply": "inner"})
    nester = _Nester(child, box)
    reg = _registry(_Editor(_Document(), delay=0.0))
    reg.register(nester, overwrite=True)
    box.append(reg)
    parent = {"nodes": [{"id": "outer", "type": "test.nest", "position": {"x": 0, "y": 0},
                         "data": {"config": {}, "input": {"session_id": "s-1"}, "one_at_a_time": shared}}],
              "edges": []}
    started = time.monotonic()
    result, _ = await _run(parent, reg, "parent-run")
    assert time.monotonic() - started < 3.0, "the child waited on its own parent"
    assert result.status is RunStatus.COMPLETED
    assert nester.child_status is RunStatus.ERRORED
    assert "engine.one_at_a_time_self_wait" in log.labels(review=True)
    assert store.rows() == {}


async def test_a_turn_lost_while_working_raises_a_review_flag(log):
    class _Losing(MemoryStepResultStore):
        async def renew(self, key: StepResultKey, *, token: str, lease_until: datetime) -> bool:
            return False

    configure_step_result_store(_Losing())
    knobs._cache[knobs.ONCE_FEATURE] = (time.monotonic() + 10**9,
                                        {"lease_seconds": 5, "wait_poll_seconds": 1, "keep_days_default": 30})
    _max_wait(600)
    try:
        result, _ = await _run(_definition(TURN, {"session_id": "s-1", "reply": "a"}),
                               _registry(_Editor(_Document(), delay=2.2)), "run-1")
    finally:
        configure_step_result_store(None)
        knobs._cache.pop(knobs.ONCE_FEATURE, None)
        knobs._cache.pop(knobs.ONE_AT_A_TIME_FEATURE, None)
    assert result.status is RunStatus.COMPLETED
    assert "engine.one_at_a_time_lost_turn" in log.labels(review=True)


async def test_a_cancel_while_the_turn_is_being_written_leaves_no_orphan_turn():
    class _SlowAfterInsert(MemoryStepResultStore):
        async def insert_claim(self, key: StepResultKey, **kw: Any) -> bool:
            landed = await super().insert_claim(key, **kw)
            await asyncio.sleep(0.4)  # the claim landed; the answer is still on its way back
            return landed

    slow = _SlowAfterInsert()
    configure_step_result_store(slow)
    knobs._cache[knobs.ONCE_FEATURE] = (time.monotonic() + 10**9,
                                        {"lease_seconds": 60, "wait_poll_seconds": 1, "keep_days_default": 30})
    _max_wait(600)
    try:
        task = asyncio.create_task(_run(_definition(TURN, {"session_id": "s-1", "reply": "a"}),
                                        _registry(_Editor(_Document(), delay=0.0)), "run-1"))
        await asyncio.sleep(0.15)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert slow.rows() == {}, "a cancel mid-claim left a turn nobody gives back"
    finally:
        configure_step_result_store(None)
        knobs._cache.pop(knobs.ONCE_FEATURE, None)
        knobs._cache.pop(knobs.ONE_AT_A_TIME_FEATURE, None)
