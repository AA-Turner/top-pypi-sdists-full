"""Guard (G3 + G7, packages/matrx-graph/matrx_graph/executor/FEATURE.md § For each: `until`, `wave_size` and the item cap, 2026-11-02): a For each that stops on what it gathered.

* ``until`` — an expression over the results gathered so far. Once it is true nothing new dispatches;
  an item already in flight finishes (the Stop semantics of § B1). The items never sent are skipped,
  named as such, and the run goes on.
* ``wave_size`` — an expression over the same scope. Items go in index order, one wave at a time: the
  next wave starts only after every item of the wave before it settled, and its size is read again.
* ``max_dispatches`` — a number or an expression (default: the list's length), never above the
  platform knob ``workflow.for_each.max_items``. A list over the cap fails loudly.

Real ``Scheduler`` + ``MemoryCheckpointer`` over the real For each (``data.for_each``); the only double
is the item step, which records when each item started and finished.
"""

from __future__ import annotations

import asyncio
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
from matrx_graph import knobs as graph_knobs
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from tests._fixtures import FakeEmitter, make_app_context


class _Page(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Read(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int
    good: bool
    rows: list[int]


class _ReadPage:
    """One item's branch. Even pages are good; ``empty_from`` and later pages return no rows."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.read_page",
        category=NodeCategory.DATA,
        display_name="Read a page",
        description="until / waves test step",
        input_schema=_Page,
        output_schema=_Read,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
    )

    def __init__(self, empty_from: int = 10_000) -> None:
        self.empty_from = empty_from
        self.started: list[int] = []
        self.finished: list[int] = []
        self.log: list[tuple[str, int]] = []

    async def execute(self, ctx: NodeExecutionContext, inputs: _Page, config: _Cfg) -> NodeResult[_Read]:
        page = int(getattr(inputs, "page"))
        self.started.append(page)
        self.log.append(("start", page))
        await asyncio.sleep(0.01 + 0.005 * (page % 3))
        self.finished.append(page)
        self.log.append(("end", page))
        rows = [] if page >= self.empty_from else [page]
        return success(_Read(page=page, good=page % 2 == 0, rows=rows))


GOOD = "len([r for r in inputs['results'] if r['good']])"


def _definition(n: int, each: dict[str, Any], *, concurrency: int = 1, target: int | None = None) -> dict[str, Any]:
    pages = "{'pages': [" + ", ".join(str(i) for i in range(n)) + "], 'target': " + str(target or 0) + "}"
    mappings = {"items": "pages"}
    if target is not None:
        mappings["target"] = "target"
    return {
        "nodes": [
            {"id": "pages", "type": "data.transform", "position": {"x": 0, "y": 0},
             "data": {"config": {"expression": pages}}},
            {"id": "read", "type": "test.read_page", "position": {"x": 300, "y": 0},
             "data": {"label": "Read a page", "for_each": {"as": "page", **each}, "concurrency": concurrency,
                      "config": {}}},
            {"id": "report", "type": "data.transform", "position": {"x": 600, "y": 0},
             "data": {"config": {"expression": "{'n': inputs['n'], 'skipped': inputs['skipped']}"}}},
        ],
        "edges": [
            {"id": "e1", "source": "pages", "target": "read",
             "data": {"kind": "data", "mappings": mappings}},
            {"id": "e2", "source": "read", "target": "report",
             "data": {"kind": "data", "mappings": {"n": "count", "skipped": "skipped_indexes"}}},
        ],
        "entry_nodes": ["pages"],
    }


@pytest.fixture(autouse=True)
def eight_at_a_time(monkeypatch):
    async def _policy() -> graph_knobs.FanOutPolicy:
        return graph_knobs.FanOutPolicy(default_item_concurrency=8, max_item_concurrency=8, paid_first_wave=8)

    monkeypatch.setattr(graph_knobs, "fan_out_policy", _policy)


async def _run(step: _ReadPage, definition: dict[str, Any], run_id: str) -> Any:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(step, overwrite=True)
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry)
    return await scheduler.run(run_id=run_id)


async def test_until_n_good_stops_dispatching_once_enough_are_good() -> None:
    step = _ReadPage()
    result = await _run(step, _definition(10, {"until": f"{GOOD} >= 3"}), "until-n-good")

    assert result.status is RunStatus.COMPLETED, result.error
    # Good pages are 0, 2, 4: the third good one lands on item 4, so items 5..9 are never sent.
    assert step.started == [0, 1, 2, 3, 4], step.started
    assert result.last_outputs["report"] == {"n": 5, "skipped": [5, 6, 7, 8, 9]}


async def test_until_an_empty_page_stops_after_the_first_empty_page() -> None:
    step = _ReadPage(empty_from=3)
    until = "len(inputs['results']) > 0 and len(inputs['results'][-1]['rows']) == 0"
    result = await _run(step, _definition(10, {"until": until}), "until-empty-page")

    assert result.status is RunStatus.COMPLETED, result.error
    assert step.started == [0, 1, 2, 3], step.started
    assert result.last_outputs["report"]["skipped"] == [4, 5, 6, 7, 8, 9]


async def test_waves_go_in_order_and_each_wave_waits_for_the_one_before() -> None:
    step = _ReadPage()
    each = {"until": f"{GOOD} >= inputs['target']", "wave_size": f"inputs['target'] - {GOOD}"}
    result = await _run(step, _definition(10, each, concurrency=8, target=4), "waves")

    assert result.status is RunStatus.COMPLETED, result.error
    # Wave 1: 4 items (0..3, good 0, 2). Wave 2: 4 - 2 = 2 items (4, 5; good 4). Wave 3: 1 item (6, good).
    assert sorted(step.started) == [0, 1, 2, 3, 4, 5, 6], step.started
    waves = [{0, 1, 2, 3}, {4, 5}, {6}]
    for earlier, later in zip(waves, waves[1:]):
        last_end = max(i for i, (what, page) in enumerate(step.log) if what == "end" and page in earlier)
        first_start = min(i for i, (what, page) in enumerate(step.log) if what == "start" and page in later)
        assert last_end < first_start, step.log
    assert result.last_outputs["report"] == {"n": 7, "skipped": [7, 8, 9]}


async def test_without_until_or_waves_every_item_runs_as_before() -> None:
    step = _ReadPage()
    result = await _run(step, _definition(6, {}, concurrency=3), "plain")
    assert result.status is RunStatus.COMPLETED, result.error
    assert sorted(step.started) == list(range(6))
    assert result.last_outputs["report"] == {"n": 6, "skipped": []}


async def test_the_cap_is_the_platform_knob_and_a_list_over_it_fails_loudly(monkeypatch) -> None:
    async def _cap() -> int:
        return 5

    monkeypatch.setattr(graph_knobs, "for_each_max_items", _cap)
    ok = _ReadPage()
    result = await _run(ok, _definition(5, {}), "at-the-cap")
    assert result.status is RunStatus.COMPLETED, result.error
    assert sorted(ok.started) == list(range(5))

    over = _ReadPage()
    result = await _run(over, _definition(6, {}), "over-the-cap")
    assert result.status is not RunStatus.COMPLETED
    assert "workflow.for_each.max_items" in (result.error or ""), result.error
    assert over.started == []


async def test_max_dispatches_takes_an_expression_bounded_by_the_knob(monkeypatch) -> None:
    async def _cap() -> int:
        return 5

    monkeypatch.setattr(graph_knobs, "for_each_max_items", _cap)
    # An expression asking for more than the platform allows is still held to the knob.
    step = _ReadPage()
    result = await _run(step, _definition(6, {"max_dispatches": "len(inputs['items']) * 10"}), "expr-over-knob")
    assert result.status is not RunStatus.COMPLETED
    assert "workflow.for_each.max_items" in (result.error or ""), result.error

    # An expression below the list's length fails the same way, naming the cap it evaluated to.
    step = _ReadPage()
    result = await _run(step, _definition(4, {"max_dispatches": "len(inputs['items']) - 1"}), "expr-under")
    assert result.status is not RunStatus.COMPLETED
    assert "max_dispatches=3" in (result.error or ""), result.error


# --- wave_gap (2026-11-07): a provider's spacing, paced visibly on the For each ------------------
class _TimedPage(_ReadPage):
    def __init__(self, empty_from: int = 10_000) -> None:
        super().__init__(empty_from)
        self.started_at: list[float] = []

    async def execute(self, ctx: NodeExecutionContext, inputs: _Page, config: _Cfg) -> NodeResult[_Read]:
        self.started_at.append(asyncio.get_running_loop().time())
        return await super().execute(ctx, inputs, config)


async def test_a_wave_gap_spaces_the_waves_and_never_the_first() -> None:
    step = _TimedPage(empty_from=3)
    until = "len(inputs['results']) > 0 and len(inputs['results'][-1]['rows']) == 0"
    each = {"until": until, "wave_size": "1", "wave_gap": "0.3"}
    t0 = asyncio.get_running_loop().time()
    result = await _run(step, _definition(10, each), "wave-gap")

    assert result.status is RunStatus.COMPLETED, result.error
    assert step.started == [0, 1, 2, 3], step.started
    assert step.started_at[0] - t0 < 0.25, "the first wave waited"
    gaps = [b - a for a, b in zip(step.started_at, step.started_at[1:])]
    assert all(g >= 0.3 for g in gaps), gaps
    assert result.last_outputs["report"]["skipped"] == [4, 5, 6, 7, 8, 9]


def test_a_wave_gap_alone_sends_one_item_per_wave() -> None:
    from matrx_graph.nodes.control.map import pace_of

    assert pace_of(None, None, {}, 5, "1.5") == {
        "until": None, "wave_size": "1", "wave_gap": "1.5", "scope": {}, "total": 5,
    }
    assert pace_of(None, None, {}, 5) is None
