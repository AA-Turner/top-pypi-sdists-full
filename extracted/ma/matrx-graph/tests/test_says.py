"""Guard (Says, 2026-11-19): any step announces its progress on its own events, as the work happens.

``data.says`` (matrx_graph/says.py) lists what a step says on start / done / failed / each item /
item failed; the scheduler renders each line onto the step's real ``node_started`` /
``node_completed`` / ``node_failed`` / ``item_settled`` the moment it is sent. The counts
``{done}`` ``{failed}`` ``{total}`` are the engine's, on ``item_settled`` as plain fields, and
survive a resume. A value missing at render time shows empty and is flagged once — never a
failed run. Real ``Scheduler`` + ``MemoryCheckpointer`` over the real For each; the only double
is the item step.
"""

from __future__ import annotations

import asyncio
from collections.abc import Iterator
from typing import Any, ClassVar
from uuid import uuid4

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
from matrx_graph import knobs as graph_knobs
from matrx_graph import run_log
from matrx_graph.checkpoint.protocol import Checkpoint
from matrx_graph.errors import CompilationError
from matrx_graph.run_log import RunLogEntry
from matrx_graph.says import parse_says
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.events import ItemSettledEvent
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory, RetryPolicy
from matrx_graph.types.result import NodeResult, failure, success
from tests._fixtures import FakeEmitter, make_app_context


class _Page(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Read(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int
    title: str


class _ReadPage:
    """One item. ``fail`` pages return a failure (a hole); ``raise_once`` pages raise on their first
    attempt (the run parks); ``wait_for`` pages wait until the gate opens."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.says_read",
        category=NodeCategory.DATA,
        display_name="Read a page",
        description="says test step",
        input_schema=_Page,
        output_schema=_Read,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        retry=RetryPolicy(max_attempts=1),
    )

    def __init__(self) -> None:
        self.fail: set[int] = set()
        self.raise_once: set[int] = set()
        self.wait_for: dict[int, asyncio.Event] = {}
        self.ran: list[int] = []

    async def execute(self, ctx: NodeExecutionContext, inputs: _Page, config: _Cfg) -> NodeResult[_Read]:
        page = int(getattr(inputs, "page"))
        self.ran.append(page)
        gate = self.wait_for.get(page)
        if gate is not None:
            try:
                await asyncio.wait_for(gate.wait(), timeout=5)
            except TimeoutError:
                return failure("not_live", f"page {page}: the line for the page before never arrived")
        if page in self.raise_once:
            self.raise_once.discard(page)
            raise RuntimeError(f"page {page} broke")
        if page in self.fail:
            return failure("bad_page", f"page {page} is unreadable")
        return success(_Read(page=page, title=f"Page {page}"))


class _Recorder:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []

    async def __call__(self, **kw: Any) -> RunLogEntry:
        self.rows.append(kw)
        return RunLogEntry(recorded=True, entry_id=str(len(self.rows)), label=kw["label"], needs_review=kw["needs_review"])


@pytest.fixture
def recorder() -> Iterator[_Recorder]:
    rec = _Recorder()
    run_log.configure_run_log_writer(rec)
    try:
        yield rec
    finally:
        run_log.configure_run_log_writer(None)


@pytest.fixture(autouse=True)
def eight_at_a_time(monkeypatch):
    async def _policy() -> graph_knobs.FanOutPolicy:
        return graph_knobs.FanOutPolicy(default_item_concurrency=8, max_item_concurrency=8, paid_first_wave=8)

    monkeypatch.setattr(graph_knobs, "fan_out_policy", _policy)


SAYS = [
    {"on": "start", "event": "page_start", "message": "Reading page {item.page}"},
    {"on": "done", "event": "page_done", "message": "Read {result.title}"},
    {"on": "each_item", "event": "page_complete", "message": "Read page {done} of {total} ({result.title})"},
    {"on": "item_failed", "event": "page_failed", "message": "Page {item.page} failed: {error} ({failed} failed)"},
]


def _definition(n: int, says: list[dict[str, Any]], *, concurrency: int = 8, hole: bool = True) -> dict[str, Any]:
    pages = "{'pages': [" + ", ".join(str(i) for i in range(n)) + "]}"
    read_data: dict[str, Any] = {
        "label": "Read a page", "for_each": {"as": "page"}, "concurrency": concurrency, "config": {}, "says": says,
    }
    if hole:
        read_data["on_item_failure"] = "hole"
    return {
        "nodes": [
            {"id": "pages", "type": "data.transform", "position": {"x": 0, "y": 0},
             "data": {"config": {"expression": pages}}},
            {"id": "read", "type": "test.says_read", "position": {"x": 300, "y": 0}, "data": read_data},
        ],
        "edges": [
            {"id": "e1", "source": "pages", "target": "read",
             "data": {"kind": "data", "mappings": {"items": "pages"}}},
        ],
        "entry_nodes": ["pages"],
    }


def _graph(step: _ReadPage, definition: dict[str, Any]) -> tuple[Any, NodeRegistry]:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(step, overwrite=True)
    return compile_graph(Definition.model_validate(definition), registry=registry), registry


def _events(emitter: FakeEmitter, name: str) -> list[dict[str, Any]]:
    return [e for kind, e in emitter.events if kind == "data" and isinstance(e, dict) and e.get("event") == name]


def test_a_bad_says_row_fails_compilation_by_name() -> None:
    step = _ReadPage()
    for row, words in (
        ({"on": "each_item", "event": "x", "message": "{cost}"}, "{cost} is not a placeholder"),
        ({"on": "each_item", "event": "x", "message": "{inputs}"}, "name what to read"),
        ({"on": "each_item", "event": "x", "message": "{done.x}"}, "takes no path"),
        ({"on": "later", "event": "x", "message": ""}, "on"),
        ({"on": "start", "event": "Has Spaces", "message": ""}, "event"),
        ({"on": "start", "event": "x", "message": "", "when": "inputs['a']"}, "when"),
    ):
        with pytest.raises(CompilationError, match="says") as info:
            _graph(step, _definition(2, [row]))
        assert words in str(info.value), (row, str(info.value))
    # Text in braces that is not a placeholder shape stays text; an absent setting is no setting.
    assert parse_says([{"on": "start", "event": "x", "message": "{ not one } {1}"}]) is not None
    assert parse_says(None) is None and parse_says([]) is None


async def test_each_line_rides_its_own_event_with_the_engines_counts(recorder: _Recorder) -> None:
    step = _ReadPage()
    step.fail = {2}
    graph, registry = _graph(step, _definition(4, SAYS))
    emitter = FakeEmitter()
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry).run(
        run_id="says-lines"
    )
    assert result.status is RunStatus.COMPLETED, result.error

    started = {e["item_index"]: e["says"] for e in _events(emitter, "node_started") if e["node_id"] == "read"}
    assert started == {i: [{"event": "page_start", "message": f"Reading page {i}"}] for i in range(4)}, started

    done = {e["item_index"]: e["says"] for e in _events(emitter, "node_completed") if e["node_id"] == "read"}
    assert done == {i: [{"event": "page_done", "message": f"Read Page {i}"}] for i in (0, 1, 3)}, done

    settled = sorted(_events(emitter, "item_settled"), key=lambda e: (e["done"] + e["failed"]))
    for e in settled:
        ItemSettledEvent.model_validate(e)
        assert e["total"] == 4
    # The counts climb one per settled item, in the order they settled.
    assert [e["done"] + e["failed"] for e in settled] == [1, 2, 3, 4]
    by_item = {e["item_index"]: e for e in settled}
    assert by_item[2]["outcome"] == "failed" and by_item[2]["says"] == [
        {"event": "page_failed", "message": f"Page 2 failed: page 2 is unreadable ({by_item[2]['failed']} failed)"}
    ]
    for i in (0, 1, 3):
        e = by_item[i]
        assert e["says"] == [{"event": "page_complete", "message": f"Read page {e['done']} of 4 (Page {i})"}], e
    assert settled[-1]["done"] == 3 and settled[-1]["failed"] == 1
    # Every placeholder had its value: nothing flagged.
    assert not [r for r in recorder.rows if r["label"] == "engine.says_failed"]


async def test_a_step_without_says_sends_no_lines_but_still_counts() -> None:
    step = _ReadPage()
    graph, registry = _graph(step, _definition(3, []))
    emitter = FakeEmitter()
    await Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry).run(run_id="silent")
    assert all(e.get("says") is None for e in _events(emitter, "node_started") + _events(emitter, "node_completed"))
    settled = _events(emitter, "item_settled")
    assert all(e["says"] is None and e["total"] == 3 for e in settled)
    assert sorted(e["done"] for e in settled) == [1, 2, 3]


async def test_a_missing_value_shows_empty_is_flagged_once_and_never_fails_the_run(recorder: _Recorder) -> None:
    step = _ReadPage()
    says = [{"on": "each_item", "event": "page_complete", "message": "Read {result.nope}!"}]
    graph, registry = _graph(step, _definition(3, says))
    emitter = FakeEmitter()
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry).run(
        run_id="says-missing"
    )
    assert result.status is RunStatus.COMPLETED, result.error
    assert [e["says"] for e in _events(emitter, "item_settled")] == [[{"event": "page_complete", "message": "Read !"}]] * 3
    flags = [r for r in recorder.rows if r["label"] == "engine.says_failed"]
    assert len(flags) == 1, flags
    assert "{result.nope}" in flags[0]["message"]


async def test_each_line_is_live_item_two_waits_for_item_ones_line() -> None:
    """Deterministic liveness: item 1 cannot finish until item 0's line has been OBSERVED on the feed.
    A step that said its lines after the whole list (the old after-the-fact say steps) deadlocks here,
    and item 1 fails with ``not_live``."""
    step = _ReadPage()
    gate = asyncio.Event()
    step.wait_for = {1: gate}

    class _Watching(FakeEmitter):
        async def send_data(self, payload: Any) -> None:
            await super().send_data(payload)
            e = self.events[-1][1]
            if isinstance(e, dict) and e.get("event") == "item_settled" and e.get("item_index") == 0 and e.get("says"):
                gate.set()

    emitter = _Watching()
    graph, registry = _graph(step, _definition(2, SAYS))
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry).run(
        run_id="says-live"
    )
    assert result.status is RunStatus.COMPLETED, result.error
    settled = _events(emitter, "item_settled")
    assert [(e["item_index"], e["outcome"]) for e in settled] == [(0, "succeeded"), (1, "succeeded")], settled
    assert [e["says"][0]["message"] for e in settled] == ["Read page 1 of 2 (Page 0)", "Read page 2 of 2 (Page 1)"]


async def test_the_counts_survive_a_resume() -> None:
    """Item 0 breaks the first leg (the run parks); 1..3 settle there. The resumed leg runs item 0 FIRST
    (one at a time, in index order) while 1..3 replay without events — its line must still count all four."""
    step = _ReadPage()
    step.raise_once = {0}
    graph, registry = _graph(step, _definition(4, SAYS, concurrency=1, hole=False))
    cp = MemoryCheckpointer()
    first_feed = FakeEmitter()
    first = await Scheduler(graph, cp, make_app_context(first_feed), registry=registry).run(run_id="says-resume")
    assert first.status is RunStatus.ERRORED, first.status
    first_settled = {e["item_index"]: e["outcome"] for e in _events(first_feed, "item_settled")}
    assert first_settled == {0: "failed", 1: "succeeded", 2: "succeeded", 3: "succeeded"}, first_settled

    last = await cp.latest_checkpoint("says-resume")
    bumped = [
        ni.model_copy(update={"attempt": ni.attempt + 1}) if ni.node_id == "read" and ni.item_index == 0 else ni
        for ni in last.next_invocations
    ]
    cid = str(uuid4())
    await cp.save_checkpoint(
        Checkpoint(
            checkpoint_id=cid,
            run_id="says-resume",
            thread_id=last.thread_id,
            parent_checkpoint_id=last.checkpoint_id,
            step=last.step,
            channel_values=last.channel_values,
            pending_bindings=last.pending_bindings,
            next_invocations=bumped,
            interrupt_payload=None,
        )
    )
    step.ran.clear()
    second_feed = FakeEmitter()
    resumed = await Scheduler(graph, cp, make_app_context(second_feed), registry=registry).resume("says-resume", cid)
    assert resumed.status is RunStatus.COMPLETED, resumed.error
    assert step.ran == [0], f"only the broken item runs again: {step.ran}"
    settled = _events(second_feed, "item_settled")
    assert len(settled) == 1, "a replayed item sends no item_settled"
    e = settled[0]
    assert (e["item_index"], e["outcome"], e["done"], e["failed"], e["total"]) == (0, "succeeded", 4, 0, 4), e
    assert e["says"] == [{"event": "page_complete", "message": "Read page 4 of 4 (Page 0)"}]


async def test_a_line_is_sent_before_its_review_flag_is_written_so_counts_never_go_backwards() -> None:
    """Item 0's line has a missing value, so its step raises the review flag — a database write. The
    write blocks until item 1's line is on the feed. Item 0's "1 of 2" must already be out: a flag
    written BEFORE the line was sent let item 1's "2 of 2" overtake it, and the screen read 2 then 1."""
    step = _ReadPage()
    gate = asyncio.Event()
    step.wait_for = {1: gate}
    second_line_out = asyncio.Event()

    class _Feed(FakeEmitter):
        async def send_data(self, payload: Any) -> None:
            await super().send_data(payload)
            e = self.events[-1][1]
            if isinstance(e, dict) and e.get("event") == "item_settled" and e.get("done") == 2:
                second_line_out.set()

    async def _slow_writer(**kw: Any) -> RunLogEntry:
        gate.set()
        try:
            await asyncio.wait_for(second_line_out.wait(), timeout=2)
        except TimeoutError:
            pass
        return RunLogEntry(recorded=True, entry_id="1", label=kw["label"], needs_review=kw["needs_review"])

    run_log.configure_run_log_writer(_slow_writer)
    try:
        says = [{"on": "each_item", "event": "page_complete", "message": "Read {done} of {total}{result.nope}"}]
        graph, registry = _graph(step, _definition(2, says))
        emitter = _Feed()
        result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry).run(
            run_id="says-order"
        )
    finally:
        run_log.configure_run_log_writer(None)
    assert result.status is RunStatus.COMPLETED, result.error
    assert [e["done"] for e in _events(emitter, "item_settled")] == [1, 2]
    assert [e["says"][0]["message"] for e in _events(emitter, "item_settled")] == ["Read 1 of 2", "Read 2 of 2"]


def _says_findings(definition: dict[str, Any], step: _ReadPage) -> list[str]:
    from matrx_graph import validate_definition

    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(step, overwrite=True)
    result = validate_definition(definition, registry=registry)
    return [i.message for i in result.issues if (i.code or "").startswith("says_")]


def test_a_placeholder_that_can_never_have_a_value_for_its_row_is_refused_by_name() -> None:
    """F4: checked at save (a finding on the step, editing goes on) and publish (compile refuses): ``{result.x}`` on
    start, ``{error}`` outside the failure rows, counts / ``{item.x}`` / the per-item rows on a step with no For each,
    The rows the engine CAN fill pass (``{total}`` on a paced For each included)."""
    step = _ReadPage()
    assert _says_findings(_definition(2, SAYS), step) == []

    wrong_rows = [
        {"on": "start", "event": "a", "message": "Reading {result.title}"},
        {"on": "done", "event": "b", "message": "Done: {error}"},
        {"on": "item_failed", "event": "c", "message": "{result.title} failed"},
    ]
    found = _says_findings(_definition(2, wrong_rows), step)
    assert any("row 1 (when the step starts): {result.title} has no value" in f for f in found), found
    assert any("row 2 (when the step is done): {error} has a value only when" in f for f in found), found
    assert any("row 3 (when an item fails): {result.title} has no value" in f for f in found), found

    # The list step has no For each: per-item rows and counts never fire there.
    plain = _definition(2, SAYS)
    plain["nodes"][0]["data"]["says"] = [
        {"on": "each_item", "event": "x", "message": "one"},
        {"on": "done", "event": "y", "message": "{done} of {total} for {item.page}"},
    ]
    found = _says_findings(plain, step)
    assert any("row 1 (on each item) runs for each item of a For each, and this step has no For each" in f
               for f in found), found
    assert any("{done} reads a For each's items" in f for f in found) and any("{item.page}" in f for f in found), found

    # A paced ``until`` For each still knows its list's length (2026-11-19): {total} is no finding there.
    paced = _definition(2, [{"on": "each_item", "event": "x", "message": "{done} of {total}"}])
    paced["nodes"][1]["data"]["for_each"]["until"] = "len(inputs['results']) >= 1"
    assert _says_findings(paced, step) == []

    with pytest.raises(CompilationError, match="has no value"):
        _graph(step, _definition(2, wrong_rows))


def test_a_line_and_a_step_have_a_size_limit() -> None:
    """F12: many long values cannot make one line huge, and a step cannot carry rows without end."""
    from matrx_graph.says import LINE_MAX_CHARS, ROWS_MAX, SaysLine, render_line

    line = SaysLine(on="done", event="x", message=" ".join(["{result.text}"] * 30))
    said, missing = render_line(line, {"result": {"text": "y" * 1000}})
    assert len(said.message) == LINE_MAX_CHARS and said.message.endswith("…") and not missing
    too_many = [{"on": "start", "event": f"e{i}", "message": ""} for i in range(ROWS_MAX + 1)]
    with pytest.raises(ValueError, match=f"at most {ROWS_MAX} rows"):
        parse_says(too_many)
    assert parse_says(too_many[:ROWS_MAX]) is not None


@pytest.mark.parametrize(
    "pace",
    [{"until": "len(inputs['results']) >= 99"}, {"until": "len(inputs['results']) >= 99", "wave_size": "1"}],
    ids=["until", "until_in_waves"],
)
async def test_a_paced_for_each_says_how_many_items_its_list_holds(pace: dict[str, str]) -> None:
    """2026-11-19 (research-as-workflow lane F2b): a paced For each (``until``, in waves or not) says its list's
    length as ``{total}``. It used to say empty text (a For each that may stop early "had no total"), so the
    research screen's "N remaining" and overview counter had nothing to read on the workflow engine."""
    step = _ReadPage()
    definition = _definition(3, [{"on": "each_item", "event": "page_complete", "message": "Read {done} of {total}"}],
                             concurrency=1)
    definition["nodes"][1]["data"]["for_each"].update(pace)
    assert _says_findings(definition, step) == []

    graph, registry = _graph(step, definition)
    emitter = FakeEmitter()
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry).run(
        run_id=f"paced-total-{len(pace)}"
    )
    assert result.status is RunStatus.COMPLETED, result.error
    settled = sorted(_events(emitter, "item_settled"), key=lambda e: e["done"])
    assert [e["total"] for e in settled] == [3, 3, 3], settled
    assert [e["says"] for e in settled] == [
        [{"event": "page_complete", "message": f"Read {n} of 3"}] for n in (1, 2, 3)
    ], settled
