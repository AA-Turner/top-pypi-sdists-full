"""A person's backlog of N items is read through the durable work set, never one For each over N.

Knowledge buckets run f0f285af (2026-10-31): the owner's 6,596 unread items went to ONE ``data.for_each``
step and the For each refused them (``control.map: 6596 items exceeds max_dispatches=1000``). Raising the
cap only moves the wall. The shape that has no wall: a transform pages the list (page size grows with the list, so the page count stays bounded), a For each over the PAGES seeds the run's work set
(``control.work_seed``), and ``control.work_queue`` drains it in waves of ``batch_size``.

The page/ceiling expressions below are the ones the live workflow's ``points`` / ``go`` steps carry
(``common-docs/systems/workflows/projects/generic-only/conversions/KNOWLEDGE-BUCKETS.md`` § Backlog), so this
proves the live expressions on the real engine, not a copy of the idea.
"""

from __future__ import annotations

from typing import ClassVar
from uuid import uuid4

import pytest
from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    MemoryWorkSetStore,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    configure_work_set_store,
    register_builtin_nodes,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.workset import get_work_set_store
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context

#: The live ``points`` step's paging and ceiling defines (knowledge buckets, 2026-10-31).
PAGE_DEFINES = {
    "cap": "int(inputs['points_ceiling'] / inputs['points_per_item']) if inputs['points_per_item'] else len(inputs['to_cover_all'])",
    "reading": "[c for j, c in enumerate(inputs['to_cover_all']) if j < inputs['cap']]",
    # One pass, never a loop per page (the expression loop budget): pages of `page_size`, at most ~500 of them,
    # so the For each over pages stays far under its dispatch cap however long the list is. Each source carries
    # its own organization, so a page may mix organizations; the read runs in each item's own.
    "page_size": "max(500, int(len(inputs['reading']) / 500) + 1)",
    "starts": "[j for j, c in enumerate(inputs['reading']) if j % inputs['page_size'] == 0]",
    "pages": "[{'sources': inputs['reading'][j:j + inputs['page_size']]} for j in inputs['starts']]",
}
PAGE_EXPRESSION = (
    "{'pages': inputs['pages'], 'reading': len(inputs['reading']), 'to_read': len(inputs['to_cover_all']),"
    " 'stopped': 'points_ceiling' if len(inputs['reading']) < len(inputs['to_cover_all']) else ''}"
)


@pytest.fixture(autouse=True)
def _fresh_store():
    configure_work_set_store(MemoryWorkSetStore())
    yield
    configure_work_set_store(None)


class _AnyIO(BaseModel):
    model_config = ConfigDict(extra="allow")


class _NoConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Reader:
    """Stands in for ``rag.ingest_source``: records every source it was handed."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.read_source",
        category=NodeCategory.DATA,
        display_name="Read one source",
        description="Records the source.",
        input_schema=_AnyIO,
        output_schema=_AnyIO,
        config_schema=_NoConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        determinism=ActionTier.SIDE_EFFECT,
    )

    def __init__(self) -> None:
        self.seen: list[tuple[str, str]] = []

    async def execute(self, ctx: NodeExecutionContext, inputs: _AnyIO, _c: _NoConfig) -> NodeResult[_AnyIO]:
        data = inputs.model_dump(mode="json")
        self.seen.append((data["organization_id"], data["source_id"]))
        return success(_AnyIO(source_id=data["source_id"]))


def _backlog(n: int) -> list[dict[str, str]]:
    return [
        {"source_kind": "note", "source_id": f"n{i}", "organization_id": "org-a" if i % 3 else "org-b"}
        for i in range(n)
    ]


def _paged_definition(backlog: list[dict[str, str]], *, ceiling: int, batch_size: int = 100) -> Definition:
    node = lambda nid, typ, data: {"id": nid, "type": typ, "position": {"x": 0, "y": 0}, "data": data}  # noqa: E731
    return Definition.model_validate(
        {
            "nodes": [
                node("pages", "data.transform", {
                    "input": {"to_cover_all": backlog, "points_ceiling": ceiling, "points_per_item": 2},
                    "config": {"define": PAGE_DEFINES, "expression": PAGE_EXPRESSION},
                }),
                node("seed", "control.work_seed", {
                    "config": {"set_name": "ingest", "key_template": "$item.source_id", "max_items": 10000},
                    "for_each": {"payload_template": {"items": "$item.sources"}},
                }),
                node("drain", "control.work_queue", {"config": {
                    "target_node_id": "ingest", "set_name": "ingest", "batch_size": batch_size,
                    "payload_template": {
                        "source_id": "$item.source_id", "source_kind": "$item.source_kind",
                        "organization_id": "$item.organization_id",
                    },
                }}),
                node("ingest", "test.read_source", {"config": {}, "on_item_failure": "hole"}),
                node("done", "data.transform", {"config": {"expression": "{'ok': True}"}}),
            ],
            "edges": [
                {"id": "e_pages_seed", "source": "pages", "target": "seed", "data": {"mappings": {"items": "pages"}}},
                {"id": "e_seed_drain", "source": "seed", "target": "drain", "data": {"kind": "control"}},
                {"id": "e_drain_done", "source": "drain", "sourceHandle": "done", "target": "done",
                 "data": {"kind": "control"}},
            ],
            "entry_nodes": ["pages"],
        }
    )


def _run(definition: Definition, reader: _Reader):
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(reader, overwrite=True)
    scheduler = Scheduler(
        compile_graph(definition, registry=registry), MemoryCheckpointer(), make_app_context(FakeEmitter()),
        registry=registry,
    )
    return scheduler.run(run_id=str(uuid4()))


async def test_a_backlog_past_every_dispatch_cap_is_read_once_each_in_its_own_organization():
    backlog = _backlog(2_600)
    reader = _Reader()
    result = await _run(_paged_definition(backlog, ceiling=100_000), reader)
    assert result.status is RunStatus.COMPLETED, result.error
    assert sorted(s for _, s in reader.seen) == sorted(b["source_id"] for b in backlog)  # every item, once
    assert {(b["organization_id"], b["source_id"]) for b in backlog} == set(reader.seen)
    counts = await get_work_set_store().counts(result.run_id, "ingest")
    assert (counts.discovered, counts.succeeded, counts.pending, counts.in_progress) == (2_600, 2_600, 0, 0)
    assert "done" in result.last_outputs  # the queue's done handle fired: the steps after it run


async def test_the_ceiling_reads_only_what_it_allows_and_says_it_stopped():
    backlog = _backlog(1_500)
    reader = _Reader()
    result = await _run(_paged_definition(backlog, ceiling=2_000), reader)  # 2 points each -> 1,000 items
    assert result.status is RunStatus.COMPLETED, result.error
    assert len(reader.seen) == 1_000
    pages = result.last_outputs.get("pages") or {}
    assert (pages.get("reading"), pages.get("to_read"), pages.get("stopped")) == (1_000, 1_500, "points_ceiling")


async def test_the_old_shape_one_for_each_over_the_backlog_hits_the_cap(monkeypatch):
    """The defect this file guards: the same backlog through one For each refuses at its cap.

    Since G7 (2026-11-02) a For each's cap is the list's length bounded by the platform knob
    ``workflow.for_each.max_items`` (no fixed 1,000), so the knob is pinned at 1,000 here."""
    from matrx_graph import knobs as graph_knobs

    async def _cap() -> int:
        return 1_000

    monkeypatch.setattr(graph_knobs, "for_each_max_items", _cap)
    backlog = _backlog(1_200)
    reader = _Reader()
    node = lambda nid, typ, data: {"id": nid, "type": typ, "position": {"x": 0, "y": 0}, "data": data}  # noqa: E731
    definition = Definition.model_validate({
        "nodes": [
            node("go", "data.transform", {"input": {"to_cover": backlog}, "config": {"expression": "{'to_cover': inputs['to_cover']}"}}),
            node("ingest", "test.read_source", {"config": {}, "for_each": {"payload_template": {
                "source_id": "$item.source_id", "source_kind": "$item.source_kind",
                "organization_id": "$item.organization_id"}}}),
        ],
        "edges": [{"id": "e", "source": "go", "target": "ingest", "data": {"mappings": {"items": "to_cover"}}}],
        "entry_nodes": ["go"],
    })
    result = await _run(definition, reader)
    assert result.status is not RunStatus.COMPLETED
    assert "workflow.for_each.max_items" in str(result.error)
    assert reader.seen == []
