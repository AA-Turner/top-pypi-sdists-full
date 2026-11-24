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

import asyncio
import json
from collections.abc import Callable
from contextlib import asynccontextmanager
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict
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
PREFLIGHT_RECEIVED: dict[str, Any] = {}


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

    async def sample_preflight(self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg) -> dict[str, bool]:
        PREFLIGHT_RECEIVED[ctx.node_id] = inputs.provision_values
        return {"held_value_resolved": inputs.provision_values is not None}


def _definition(*, readers: tuple[str, ...] = ("agent_a", "agent_b")) -> Definition:
    nodes = [{"id": n, "type": "test.held_capture", "position": {"x": 0, "y": 0},
              "data": {"config": {"capture": n == "point"}}} for n in ("point", *readers)]
    edges = [{"id": f"e_point_{t}", "source": "point", "target": t,
              "data": {"kind": "data", "mappings": {"provision_values": "provision_values"}}}
             for t in readers]
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


async def _run(
    monkeypatch,
    *,
    checkpointer: MemoryCheckpointer | None = None,
    sampled_outputs: dict[str, Any] | None = None,
    on_load: Callable[[], None] | None = None,
    readers: tuple[str, ...] = ("agent_a", "agent_b"),
    expected_status: RunStatus = RunStatus.COMPLETED,
) -> tuple[list[dict[str, Any]], MemoryCheckpointer, dict[str, Any]]:
    RECEIVED.clear()
    PREFLIGHT_RECEIVED.clear()
    store = _fake_store(monkeypatch)
    if on_load is not None:
        original_load = value_store.load_run_values

        async def observed_load(run_id: str, hashes) -> dict[str, Any]:
            on_load()
            return await original_load(run_id, hashes)

        monkeypatch.setattr(value_store, "load_run_values", observed_load)
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_Step())
    graph = compile_graph(_definition(readers=readers), registry=registry)
    emitter = FakeEmitter()
    checkpointer = checkpointer or MemoryCheckpointer()
    scheduler = Scheduler(
        graph,
        checkpointer,
        make_app_context(emitter),
        registry=registry,
        sampled_outputs=sampled_outputs,
    )
    result = await scheduler.run(run_id="mkt-167-held")
    assert result.status is expected_status, result.error
    events = [json.loads(json.dumps(p, default=str)) for name, p in emitter.events
              if name == "data" and isinstance(p, dict) and p.get("event")]
    return events, checkpointer, store


async def test_every_downstream_step_receives_the_full_held_value(monkeypatch) -> None:
    await _run(monkeypatch)
    assert RECEIVED == {"agent_a": STATE, "agent_b": STATE}


async def test_scheduler_scopes_held_reads_for_executor_and_sample_preflight(monkeypatch) -> None:
    """Break: Scheduler resolves held inputs outside the owning checkpointer admission scope."""
    events: list[str] = []
    active_scopes = 0

    @asynccontextmanager
    async def admission(unit: str, run_id: str | None, checkpoint_id: str | None):
        nonlocal active_scopes
        assert (unit, run_id, checkpoint_id) == ("resolve_held_values", "mkt-167-held", None)
        active_scopes += 1
        events.append("enter")
        try:
            yield
        finally:
            events.append("exit")
            active_scopes -= 1

    checkpointer = MemoryCheckpointer()
    checkpointer._read_scope_factory = admission  # type: ignore[attr-defined]  # optional host capability

    def observe_load() -> None:
        events.append("load")
        assert active_scopes > 0, "held storage was read before Scheduler admitted this invocation"

    await _run(
        monkeypatch,
        checkpointer=checkpointer,
        sampled_outputs={"agent_a": {"count": 0}},
        on_load=observe_load,
    )
    assert PREFLIGHT_RECEIVED == {"agent_a": STATE}
    assert RECEIVED == {"agent_b": STATE}, "the sample replaces only the executor after its preflight"
    assert events.count("enter") == events.count("load") == events.count("exit") == 2
    assert active_scopes == 0


async def test_custom_checkpointer_without_scope_keeps_ordinary_held_reads(monkeypatch) -> None:
    """Break: optional admission assumes every custom checkpointer initialized the new capability."""

    class _CustomMemoryCheckpointer(MemoryCheckpointer):
        pass

    await _run(monkeypatch, checkpointer=_CustomMemoryCheckpointer())
    assert RECEIVED == {"agent_a": STATE, "agent_b": STATE}


@pytest.mark.parametrize(
    ("failure_name", "sampled"),
    [
        ("RecordingOperationRefused", False),
        ("RecordingOperationRefused", True),
        ("RecordingOperationUnavailable", False),
        ("RecordingOperationUnavailable", True),
    ],
)
async def test_actual_recording_worker_scope_refuses_held_reads_before_scheduler_body(
    monkeypatch, failure_name: str, sampled: bool
) -> None:
    """The imported recording worker gate stops both real Scheduler read callers before a load or body."""
    # Host-only integration must not make the standalone package require aidream.
    recording_operation = pytest.importorskip("aidream.services.meet.recording_operation")
    from matrx_graph.workers.queue import Job

    failure = getattr(recording_operation, failure_name)
    run_id = "mkt-167-held"
    job = Job(job_id="held-read-host-proof", run_id=run_id, kind="start", claimed_by="worker")
    source = recording_operation._Source(
        "recording", "landing", run_id, "actor", "org", "uri", "nonce", "def", "version", "hash"
    )
    pending = recording_operation._Pending(job, source)
    invocation_token = recording_operation._current.set(
        (pending, recording_operation.WorkerInvocation(job, object()))
    )
    monkeypatch.setattr(recording_operation, "RECORDING_OPERATION_PROTOCOL", 1)
    source_calls: list[tuple[object, ...]] = []
    body_calls: list[str] = []
    held_ref = "preexisting-held-ref"
    cache_key = (id(asyncio.get_running_loop()), run_id, held_ref)
    shared = asyncio.get_running_loop().create_future()
    shared.set_result({held_ref: {"poison": True}})
    value_store._HELD_LOADS[cache_key] = shared

    @asynccontextmanager
    async def transaction(**_kwargs):
        yield object()

    async def denied_source(*args, **_kwargs):
        source_calls.append(args)
        raise failure("host denied")

    original_execute = _Step.execute
    original_preflight = _Step.sample_preflight

    async def execute_never(*args, **kwargs):
        if args[1].node_id == "agent_a":
            body_calls.append("executor")
        return await original_execute(*args, **kwargs)

    async def preflight_never(*args, **kwargs):
        if args[1].node_id == "agent_a":
            body_calls.append("preflight")
        return await original_preflight(*args, **kwargs)

    monkeypatch.setattr(recording_operation, "_fresh_transaction", transaction)
    monkeypatch.setattr(recording_operation, "_source_and_job", denied_source)
    monkeypatch.setattr(_Step, "execute", execute_never)
    monkeypatch.setattr(_Step, "sample_preflight", preflight_never)
    monkeypatch.setattr(value_store, "new_held_ref", lambda: held_ref)
    loads: list[None] = []
    cache_calls: list[tuple[str, str]] = []
    original_shared_load = value_store._load_held_shared

    async def observe_shared_load(actual_run_id: str, ref: str) -> dict[str, Any]:
        cache_calls.append((actual_run_id, ref))
        return await original_shared_load(actual_run_id, ref)

    monkeypatch.setattr(value_store, "_load_held_shared", observe_shared_load)
    checkpointer = MemoryCheckpointer()
    checkpointer._read_scope_factory = recording_operation.worker_read_scope  # type: ignore[attr-defined]
    try:
        await _run(
            monkeypatch,
            checkpointer=checkpointer,
            sampled_outputs={"agent_a": {"count": 0}} if sampled else None,
            readers=("agent_a",),
            expected_status=RunStatus.ERRORED,
            on_load=lambda: loads.append(None),
        )
        assert len(source_calls) == 1
        assert loads == [], "host refusal must precede held-store reads"
        assert cache_calls == [], "host refusal must not consume a shared held-load future"
        assert cache_key in value_store._HELD_LOADS and value_store._HELD_LOADS[cache_key] is shared
        assert body_calls == [], "host refusal must precede executor and sampled-preflight bodies"
    finally:
        value_store._HELD_LOADS.pop(cache_key, None)
        if not shared.done():
            shared.cancel()
        recording_operation._current.reset(invocation_token)
        assert recording_operation.RECORDING_OPERATION_PROTOCOL == 1


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
