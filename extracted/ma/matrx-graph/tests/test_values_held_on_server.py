"""A value a step HOLDS ON THE SERVER travels as a reference; the next step still gets the value (MKT-167 part 2).

Arman, 2026-10-15: "The whole point of a provision is that it sits on the server and
the client doesn't get the things it doesn't need." A provision capture step stores
its snapshot once (``hold_on_server``) and outputs only the reference. The engine
must then:

* keep the REFERENCE in channels, the checkpoint row and every event (never the value);
* hand every downstream executor the FULL value, resolved server-side, exactly as if
  it had traveled inline.
"""

from __future__ import annotations

import json
from typing import Any, ClassVar

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
from matrx_graph.checkpoint import value_store
from matrx_graph.checkpoint.value_store import HELD_KEY as REF_KEY
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from tests._fixtures import FakeEmitter, make_app_context

STATE = {f"value_{i}": "z" * 2000 for i in range(200)}  # ~400 KB, a provision-sized state
RECEIVED: dict[str, Any] = {}


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")

    provision_values: dict[str, Any] | None = None


class _Out(BaseModel):
    model_config = ConfigDict(extra="allow")

    provision_values: dict[str, Any] | None = None
    count: int = 0


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")

    capture: bool = False


class _Step:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.held_capture",
        category=NodeCategory.DATA,
        display_name="Capture or read",
        description="capture=True holds a state on the server; otherwise records what it received.",
        input_schema=_In,
        output_schema=_Out,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
    )

    async def execute(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> NodeResult[_Out]:
        if config.capture:
            held = await value_store.hold_on_server(ctx.run_id, dict(STATE))
            return success(_Out(provision_values=held, count=len(STATE)))
        RECEIVED[ctx.node_id] = inputs.provision_values
        return success(_Out(count=len(inputs.provision_values or {})))


def _definition() -> Definition:
    nodes = [{"id": n, "type": "test.held_capture", "position": {"x": 0, "y": 0},
              "data": {"config": {"capture": n == "point"}}} for n in ("point", "agent_a", "agent_b")]
    edges = [{"id": f"e_point_{t}", "source": "point", "target": t,
              "data": {"kind": "data", "mappings": {"provision_values": "provision_values"}}}
             for t in ("agent_a", "agent_b")]
    return Definition.model_validate({"nodes": nodes, "edges": edges, "entry_nodes": ["point"]})


def _fake_store(monkeypatch) -> dict[str, Any]:
    """The run's value store as a dict (the Postgres one is exercised live)."""
    store: dict[str, Any] = {}

    async def _store(run_id: str, values: dict[str, Any], *, organization_id: str | None = None) -> None:
        store.update(values)

    async def _load(run_id: str, hashes) -> dict[str, Any]:
        return {h: store[h] for h in hashes if h in store}

    monkeypatch.setattr(value_store, "store_run_values", _store)
    monkeypatch.setattr(value_store, "load_run_values", _load)
    monkeypatch.setattr(value_store, "_store_available", lambda: True)
    return store


async def _run(monkeypatch) -> tuple[list[dict[str, Any]], MemoryCheckpointer, dict[str, Any]]:
    RECEIVED.clear()
    store = _fake_store(monkeypatch)
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_Step())
    graph = compile_graph(_definition(), registry=registry)
    emitter = FakeEmitter()
    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(graph, checkpointer, make_app_context(emitter), registry=registry)
    result = await scheduler.run(run_id="mkt-167-held")
    assert result.status is RunStatus.COMPLETED, result.error
    events = [json.loads(json.dumps(p, default=str)) for name, p in emitter.events
              if name == "data" and isinstance(p, dict) and p.get("event")]
    return events, checkpointer, store


async def test_every_downstream_step_receives_the_full_held_value(monkeypatch) -> None:
    await _run(monkeypatch)
    assert RECEIVED == {"agent_a": STATE, "agent_b": STATE}


async def test_the_held_value_never_travels_inline(monkeypatch) -> None:
    events, checkpointer, store = await _run(monkeypatch)
    big = len(json.dumps(STATE))
    assert len(store) == 1 and list(store.values())[0] == STATE
    for event in events:
        assert len(json.dumps(event, default=str)) < big // 10, (event["event"], event.get("node_id"))
        if event["event"] == "node_started" and event.get("node_id", "").startswith("agent"):
            assert set(event["inputs"]["provision_values"]) == {REF_KEY}
    cps = await checkpointer.list_checkpoints("mkt-167-held")
    assert cps, "the run saved no checkpoint"
    for cp in cps:
        assert len(json.dumps(cp.model_dump(mode="json"), default=str)) < big // 10


async def test_without_a_value_store_the_value_stays_inline(monkeypatch) -> None:
    """A DB-less install keeps working: hold_on_server returns the value itself."""
    monkeypatch.setattr(value_store, "_store_available", lambda: False)
    assert await value_store.hold_on_server("r", {"a": 1}) == {"a": 1}


async def test_a_screen_viewer_gets_what_the_screen_renders_and_never_a_marker(monkeypatch) -> None:
    """Not an admin in debug mode: step arguments screened like an output, no channel state, no held value, no raw
    value — and a withheld argument says so instead of vanishing (Arman, 2026-10-27: "No inputs received" lied)."""
    from matrx_graph.checkpoint.values import REF_KEY as LARGE_KEY

    events, _, store = await _run(monkeypatch)
    big_list = [{"__kind": "brand_basics", "text": "e" * 1000}] * 50
    store["big"] = big_list
    store["ledger"] = [{"url": "https://x.com", "body": "r" * 1000}] * 50
    events.append({"event": "node_completed", "node_id": "web",
                   "output": {"content": {LARGE_KEY: "big"}, "requests": {LARGE_KEY: "ledger"}, "decision": "keep"}})
    events.append({"event": "run_interrupted", "channel_values": {"x": 1}})
    events.append({"event": "node_started", "node_id": "search",
                   "inputs": {"query": "Agentic harness", "page": {LARGE_KEY: "ledger"}, "hits": {LARGE_KEY: "big"},
                              "requests": [1], "messages": [{"role": "user"}]}})
    views = await value_store.screen_views("mkt-167-held", events)
    text = json.dumps(views)
    assert REF_KEY not in text and LARGE_KEY not in text, "a marker reached a screen viewer"
    for view in views:
        if view["event"] == "node_started":
            # A held provision never reaches the In tab: its key is gone or announced, never its value.
            assert view["inputs"].get("provision_values") in (None, value_store.WITHHELD_VALUE)
        assert "channel_values" not in view and "last_outputs" not in view
    point_done = next(v for v in views if v["event"] == "node_completed" and v.get("node_id") == "point")
    assert "provision_values" not in point_done["output"] and point_done["output"]["count"] == len(STATE)
    # A large kind list (what the screen renders) comes inline; a large raw ledger is withheld.
    assert views[-3]["output"] == {"content": big_list, "decision": "keep"}
    # The step's arguments reach its In tab: small ones inline, a large kind list inline, a large raw value announced.
    # An argument named like a debug-only key is announced, never silently absent.
    withheld = value_store.WITHHELD_VALUE
    assert views[-1]["inputs"] == {"query": "Agentic harness", "page": withheld, "hits": big_list,
                                   "requests": withheld, "messages": withheld}
    assert len(json.dumps(views[:-1])) < len(json.dumps(STATE)) // 4


async def test_a_withheld_output_value_is_described_where_it_was(monkeypatch) -> None:
    """2026-10-29: a step's large non-kind output child (five read pages) vanished from a screen viewer's
    node_completed with nothing to say so. It still stays out of the value (its shape unchanged) and the event's
    ``withheld`` list says where it was, what it was, how big, and the stored copy that brings it back."""
    from matrx_graph.checkpoint.values import REF_KEY as LARGE_KEY

    events, _, store = await _run(monkeypatch)
    pages = [{"url": "https://x.com/about", "text": "p" * 1000}] * 5
    store["pages"] = pages
    events.append({"event": "node_completed", "node_id": "website",
                   "output": {"pages": {LARGE_KEY: "pages"}, "front_page": {"text": "hello"}}})
    view = (await value_store.screen_views("withheld-output", events))[-1]
    assert view["output"] == {"front_page": {"text": "hello"}}
    assert view["withheld"] == [{"path": ["output", "pages"], "value_type": "list", "items": 5, "chars": None,
                                 "bytes": len(json.dumps(pages, separators=(",", ":")).encode()), "ref": "pages"}]
    assert LARGE_KEY not in json.dumps(view), "a marker reached a screen viewer"


async def test_nothing_withheld_adds_no_field(monkeypatch) -> None:
    events, _, _ = await _run(monkeypatch)
    events.append({"event": "node_completed", "node_id": "small", "output": {"a": 1}})
    assert "withheld" not in (await value_store.screen_views("nothing-withheld", events))[-1]


async def test_a_held_marker_reveals_nothing_about_its_value(monkeypatch) -> None:
    """Review 46 leak class: the marker was the unsalted sha256 of the held snapshot, so anyone holding an event
    could confirm a guessed small provision snapshot. The marker is now an opaque random reference: not the value's
    digest, different for the same value held twice, and it still resolves server-side to the exact value."""
    import hashlib

    from matrx_graph.checkpoint.values import _dumps

    store = _fake_store(monkeypatch)
    small = {"brand_voice": "warm"}
    first = await value_store.hold_on_server("r", dict(small))
    second = await value_store.hold_on_server("r", dict(small))
    ref = first[REF_KEY]
    assert ref != hashlib.sha256(_dumps(small).encode()).hexdigest(), "the marker is the value's digest"
    assert hashlib.sha256(_dumps(small).encode()).hexdigest() not in store, "the value is still keyed by its digest"
    assert ref != second[REF_KEY], "the same value held twice gives the same marker (a digest by another name)"
    assert await value_store.resolve_step_inputs("r", {"provision_values": first}) == {"provision_values": small}


async def test_the_withheld_list_is_capped_and_counts_the_rest(monkeypatch) -> None:
    """One cut per page of fifty would grow the event the screen view keeps small: the list is capped and the rest
    counted, never silently dropped."""
    events, _, _ = await _run(monkeypatch)
    pages = [{"url": f"https://x.com/{i}", "html": "<p>x</p>"} for i in range(50)]
    events.append({"event": "node_completed", "node_id": "crawl", "output": {"pages": pages}})
    view = (await value_store.screen_views("capped", events))[-1]
    from matrx_graph.knobs import STARTING_WITHHELD_LIST_MAX

    assert len(view["withheld"]) == STARTING_WITHHELD_LIST_MAX
    assert view["withheld_more"] == 50 - STARTING_WITHHELD_LIST_MAX
    assert view["withheld"][0]["path"] == ["output", "pages", 0, "html"]
