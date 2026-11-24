"""A run keeps alive only what it needs — the two holders lane M1 measured on a research read (2026-11-17).

A research read on the workflow engine (one keyword, 92 real pages, read_keyword + read_page inline) was
reproduced offline (``~/code/temp/research-m1/scripts/read_repro.py``). With the hand-back fixed (a335b000dce)
the engine still peaked ~+550 MB, and two holders were measured:

- an inline child's store deep-copied EVERY super-step's checkpoint and kept them all for the whole call,
  though nothing reads an inline child's history back (it never resumes): ~150 MB at the peak;
- the scheduler's JSON-native cache (``_json_native``) kept its last 512 delivered values alive for the life of
  the process whatever their size — held pages (the parse + raw HTML, MBs each): ~100 MB per keyword, never freed.

Red on the code before: the inline store holds one checkpoint per super-step; 100 one-MB values stay pinned.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, compile_graph, register_builtin_nodes
from matrx_graph.executor import scheduler as sch
from matrx_graph.nodes.subgraph import inline as inline_mod
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import success
from tests._fixtures import FakeEmitter, make_app_context


class _Io(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Page:
    """A read page: a large text the next steps pass on."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.keep_page", category=NodeCategory.DATA, display_name="Page", description="A page.",
        input_schema=_Io, output_schema=_Io, config_schema=_Io, determinism=ActionTier.PURE,
        handles=(HandleSpec(id="in", direction=HandleDirection.INPUT),
                 HandleSpec(id="out", direction=HandleDirection.OUTPUT)),
    )

    async def execute(self, ctx: Any, inputs: _Io, config: _Io) -> Any:
        return success(_Io(text="word " * 200_000))


def _child() -> Any:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_Page(), overwrite=True)
    nodes = [{"id": "page", "type": "test.keep_page", "position": {"x": 0, "y": 0}, "data": {"config": {}}}]
    edges = []
    for i in range(6):
        nodes.append({"id": f"t{i}", "type": "data", "position": {"x": 0, "y": 0},
                      "data": {"spec_type": "data.transform", "config": {"expression": "{'text': inputs['text']}"}}})
        edges.append({"id": f"e{i}", "source": "page" if i == 0 else f"t{i - 1}", "target": f"t{i}",
                      "data": {"kind": "data", "mappings": {"text": "text"}}})
    definition = Definition.model_validate({"nodes": nodes, "edges": edges, "entry_nodes": ["page"],
                                            "metadata": {"runs_as": "inline"}})
    return compile_graph(definition, registry=registry), registry


async def test_an_inline_child_keeps_one_checkpoint_not_one_per_step(monkeypatch):
    stores: list[Any] = []
    saves = {"n": 0}

    class _Seen(inline_mod.InlineChildCheckpointer):
        def __init__(self, *a: Any, **k: Any) -> None:
            super().__init__(*a, **k)
            stores.append(self)

        async def save_checkpoint(self, checkpoint: Any) -> None:
            saves["n"] += 1
            await super().save_checkpoint(checkpoint)

        async def save_checkpoint_with_outcomes(self, checkpoint: Any, outcomes: Any) -> None:
            saves["n"] += 1
            await super().save_checkpoint_with_outcomes(checkpoint, outcomes)

    monkeypatch.setattr(inline_mod, "InlineChildCheckpointer", _Seen)
    graph, registry = _child()
    ctx = SimpleNamespace(run_id="caller-1", node_id="call", dispatch_id="d-1", item_index=0, firing=0,
                          app=make_app_context(FakeEmitter()), thread_id="caller-1")
    result = await inline_mod.run_inline_child(ctx, graph, checkpointer=MemoryCheckpointer(), registry=registry,
                                               inputs={})

    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["t5"]["text"].startswith("word ")
    assert saves["n"] > 1, saves  # the child really saved once per super-step
    kept = await stores[0].list_checkpoints("caller-1")
    assert len(kept) == 1, f"an inline child kept {len(kept)} checkpoints (one deep copy per super-step)"
    assert (await stores[0].latest_checkpoint("caller-1")) is kept[0]


def test_the_json_native_cache_never_keeps_a_runs_pages_alive():
    sch._JSON_NATIVE.clear()
    if hasattr(sch, "_json_native_bytes"):
        sch._json_native_bytes = 0
    mb = 1024 * 1024
    pages = [{"url": f"https://example.test/{i}", "text": "x" * mb + str(i)} for i in range(100)]
    for page in pages:
        assert sch._json_native(page) is True
    pinned = sum(len(entry[0]["text"]) for entry in sch._JSON_NATIVE.values() if isinstance(entry[0], dict))
    assert pinned <= 64 * mb, f"the cache keeps {pinned / mb:.0f} MB of delivered values alive"
    # A value too large to remember is still answered, every time, and never pinned.
    huge = {"text": "y" * (80 * mb)}
    assert sch._json_native(huge) is True and sch._json_native(huge) is True
    assert all(entry[0] is not huge for entry in sch._JSON_NATIVE.values())
    # A remembered small value is a hit (same object, same size).
    small = {"a": [1, 2.5, "b", None]}
    assert sch._json_native(small) is True and sch._JSON_NATIVE[id(small)][0] is small
    assert sch._json_native({"bad": float("nan")}) is False
    sch._JSON_NATIVE.clear()
    if hasattr(sch, "_json_native_bytes"):
        sch._json_native_bytes = 0
