"""Standardized Node Result System — engine-plane envelope behavior.

Locks the core contract (docs/workflow/NODE_RESULT_CONTRACT.md):

    1. Success unwrap — the bare payload T flows downstream (last_outputs,
       node_outcome.output, edge mappings, conditional predicates all see T,
       never the envelope).
    2. Returned Failure with no ERROR edge → run parks ERRORED; the outcome
       carries the error SUPERSET dict {type, message, code, details}.
    3. Returned Failure enters the retry ladder — RetryPolicy.retry_on
       matches NodeError.code.
    4. ERROR-edge routing: on failure the handler receives the NodeError
       dump (mappable via code/message/details) and the success branch
       prunes; on success the handler prunes and the success branch runs.
    5. Fan-out on_item_failure='hole': a failed fanned item becomes an
       explicit error-carrying hole in gather; the run survives.
    6. Raised exceptions take the SAME routes (ERROR edge / hole).
    7. Author-drift guard: Success[T] where T is not the declared
       output_schema parks the run.
"""

from __future__ import annotations

from typing import Any, ClassVar

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import (
    ActionTier,
    BackoffStrategy,
    NodeCategory,
    RetryPolicy,
)
from matrx_graph.types.result import NodeResult, failure, success
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Payload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = "ok"
    count: int = 1


class _OtherPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    other: str = "nope"


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


def _spec(node_type: str, retry: RetryPolicy | None = None) -> NodeSpec:
    return NodeSpec(
        type=node_type,
        category=NodeCategory.DATA,
        display_name=node_type,
        description="envelope test node",
        input_schema=_In,
        output_schema=_Payload,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        retry=retry or RetryPolicy(max_attempts=1),
    )


class _EnvelopeNode:
    """Configurable envelope-returning node: behavior injected per test."""

    def __init__(self, node_type: str, behavior: Any, retry: RetryPolicy | None = None) -> None:
        self.spec: NodeSpec = _spec(node_type, retry)
        self._behavior = behavior
        self.calls = 0

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg
    ) -> NodeResult[_Payload]:
        self.calls += 1
        return self._behavior(self.calls, inputs)


class _SpyNode:
    """Records the inputs it received — proves what the edge delivered."""

    def __init__(self, node_type: str) -> None:
        self.spec: NodeSpec = _spec(node_type)
        self.seen: list[dict[str, Any]] = []

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg
    ) -> NodeResult[_Payload]:
        self.seen.append(inputs.model_dump())
        return success(_Payload(text="spy", count=len(self.seen)))


def _registry(*executors: Any) -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    for ex in executors:
        reg.register(ex, overwrite=True)
    return reg


def _node(node_id: str, node_type: str, data: dict | None = None) -> dict:
    return {
        "id": node_id,
        "type": node_type,
        "position": {"x": 0, "y": 0},
        "data": data or {"config": {}},
    }


async def _run(definition: dict, registry: NodeRegistry, run_id: str):
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    result = await scheduler.run(run_id=run_id)
    return result, scheduler, emitter


def _events(emitter: FakeEmitter, kind: str) -> list[dict]:
    return [
        e
        for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == kind
    ]


# ---------------------------------------------------------------------------
# 1. Success unwrap — payload T flows, envelope never leaks
# ---------------------------------------------------------------------------


async def test_success_unwraps_to_bare_payload():
    node = _EnvelopeNode("test.env_ok", lambda n, i: success(_Payload(text="hello", count=7)))
    spy = _SpyNode("test.env_spy")
    registry = _registry(node, spy)
    result, scheduler, emitter = await _run(
        {
            "nodes": [_node("a", "test.env_ok"), _node("b", "test.env_spy")],
            "edges": [
                {
                    "id": "e1",
                    "source": "a",
                    "target": "b",
                    "data": {"mappings": {"text": "text"}},
                }
            ],
        },
        registry,
        "env-ok",
    )
    assert result.status is RunStatus.COMPLETED
    # last_outputs holds the BARE payload — no status/result wrapper.
    assert result.last_outputs["a"] == {"text": "hello", "count": 7}
    # The edge mapping resolved against the payload's flat keys.
    assert spy.seen and spy.seen[0]["text"] == "hello"
    # node_completed carries the bare payload too.
    completed = [e for e in _events(emitter, "node_completed") if e["node_id"] == "a"]
    assert completed and completed[0]["output"] == {"text": "hello", "count": 7}
    # The recorded outcome stores the bare payload.
    outcome = await scheduler.checkpointer.get_outcome(
        run_id="env-ok", step=0, node_id="a", attempt=1
    )
    assert outcome is not None
    assert outcome.output == {"text": "hello", "count": 7}
    assert outcome.error is None


async def test_conditional_predicate_reads_bare_payload():
    node = _EnvelopeNode("test.env_ok2", lambda n, i: success(_Payload(text="go", count=9)))
    spy = _SpyNode("test.env_spy2")
    registry = _registry(node, spy)
    result, _, _ = await _run(
        {
            "nodes": [_node("a", "test.env_ok2"), _node("b", "test.env_spy2")],
            "edges": [
                {
                    "id": "e1",
                    "source": "a",
                    "target": "b",
                    "data": {"kind": "conditional", "condition": "inputs['count'] > 5"},
                }
            ],
        },
        registry,
        "env-cond",
    )
    assert result.status is RunStatus.COMPLETED
    assert spy.seen  # predicate saw flat payload keys and passed


# ---------------------------------------------------------------------------
# 2. Returned Failure, no ERROR edge → park with the superset error dict
# ---------------------------------------------------------------------------


async def test_failure_without_error_edge_parks_with_structured_error():
    node = _EnvelopeNode(
        "test.env_fail",
        lambda n, i: failure("provider_error", "upstream 500", details={"status": 500}),
    )
    registry = _registry(node)
    result, scheduler, emitter = await _run(
        {"nodes": [_node("a", "test.env_fail")], "edges": []},
        registry,
        "env-fail",
    )
    assert result.status is RunStatus.ERRORED
    assert "provider_error" in (result.error or "")
    outcome = await scheduler.checkpointer.get_outcome(
        run_id="env-fail", step=0, node_id="a", attempt=1
    )
    assert outcome is not None
    assert outcome.output == {}
    # The node plane's four original keys are UNCHANGED — every existing
    # consumer (agent_plans, checkpoint preview, replay walk-forward) reads
    # these and must keep working.
    assert outcome.error["type"] == "provider_error"
    assert outcome.error["message"] == "upstream 500"
    assert outcome.error["code"] == "provider_error"
    assert outcome.error["details"] == {"status": 500}
    # …and the structured half (matrx_graph.failure) rides alongside, so a
    # step-level surface explains itself from data instead of regexing the
    # message. Strictly additive.
    assert outcome.error["cause"] == "provider_error"
    assert outcome.error["step_id"] == "a"
    assert outcome.error["technical"]
    failed = _events(emitter, "node_failed")
    assert failed and failed[0]["error"]["code"] == "provider_error"
    assert failed[0]["error_type"] == "provider_error"


# ---------------------------------------------------------------------------
# 3. Returned Failure enters the retry ladder via NodeError.code
# ---------------------------------------------------------------------------


async def test_returned_failure_retries_on_code_then_succeeds():
    def behavior(call: int, _inputs: _In):
        if call == 1:
            return failure("rate_limited", "429 slow down")
        return success(_Payload(text="recovered", count=call))

    node = _EnvelopeNode(
        "test.env_retry",
        behavior,
        retry=RetryPolicy(
            max_attempts=3,
            backoff=BackoffStrategy.NONE,
            initial_delay_ms=0,
            retry_on=["rate_limited"],
        ),
    )
    registry = _registry(node)
    result, _, emitter = await _run(
        {"nodes": [_node("a", "test.env_retry")], "edges": []},
        registry,
        "env-retry",
    )
    assert result.status is RunStatus.COMPLETED
    assert node.calls == 2
    assert result.last_outputs["a"]["text"] == "recovered"
    retries = _events(emitter, "node_retry_scheduled")
    assert len(retries) == 1 and retries[0]["error_type"] == "rate_limited"


async def test_returned_failure_code_not_in_retry_on_does_not_retry():
    node = _EnvelopeNode(
        "test.env_noretry",
        lambda n, i: failure("parse_failed", "bad json"),
        retry=RetryPolicy(max_attempts=3, retry_on=["rate_limited"]),
    )
    registry = _registry(node)
    result, _, emitter = await _run(
        {"nodes": [_node("a", "test.env_noretry")], "edges": []},
        registry,
        "env-noretry",
    )
    assert result.status is RunStatus.ERRORED
    assert node.calls == 1
    assert not _events(emitter, "node_retry_scheduled")


# ---------------------------------------------------------------------------
# 4. ERROR-edge routing
# ---------------------------------------------------------------------------

_TRY_CATCH_DEF: dict = {
    "nodes": [],  # filled per test
    "edges": [
        {
            "id": "e_ok",
            "source": "a",
            "target": "b",
            "data": {"mappings": {"text": "text"}},
        },
        {
            "id": "e_err",
            "source": "a",
            "target": "h",
            "data": {"kind": "error", "mappings": {"text": "message"}},
        },
    ],
}


def _try_catch_nodes(src_type: str) -> list[dict]:
    return [_node("a", src_type), _node("b", "test.env_spy_ok"), _node("h", "test.env_spy_err")]


async def test_error_edge_delivers_node_error_and_prunes_success_branch():
    node = _EnvelopeNode(
        "test.env_fail2",
        lambda n, i: failure("provider_error", "boom", details={"attempt": n}),
    )
    ok_spy = _SpyNode("test.env_spy_ok")
    err_spy = _SpyNode("test.env_spy_err")
    registry = _registry(node, ok_spy, err_spy)
    definition = dict(_TRY_CATCH_DEF, nodes=_try_catch_nodes("test.env_fail2"))
    result, _, emitter = await _run(definition, registry, "env-error-edge")
    # The failure was HANDLED by topology — the run completes.
    assert result.status is RunStatus.COMPLETED
    # Handler received the mapped NodeError field.
    assert err_spy.seen and err_spy.seen[0]["text"] == "boom"
    # Success branch pruned.
    assert not ok_spy.seen
    # node_failed still emitted (observability unchanged).
    assert _events(emitter, "node_failed")


async def test_error_edge_prunes_on_success():
    node = _EnvelopeNode("test.env_ok3", lambda n, i: success(_Payload(text="fine", count=1)))
    ok_spy = _SpyNode("test.env_spy_ok")
    err_spy = _SpyNode("test.env_spy_err")
    registry = _registry(node, ok_spy, err_spy)
    definition = dict(_TRY_CATCH_DEF, nodes=_try_catch_nodes("test.env_ok3"))
    result, _, _ = await _run(definition, registry, "env-error-edge-ok")
    assert result.status is RunStatus.COMPLETED
    assert ok_spy.seen and ok_spy.seen[0]["text"] == "fine"
    assert not err_spy.seen


async def test_error_edge_broadcast_delivers_full_node_error():
    node = _EnvelopeNode(
        "test.env_fail3",
        lambda n, i: failure("timeout", "too slow", details={"elapsed_ms": 99}),
    )
    err_spy = _SpyNode("test.env_spy_err")
    registry = _registry(node, err_spy)
    result, _, _ = await _run(
        {
            "nodes": [_node("a", "test.env_fail3"), _node("h", "test.env_spy_err")],
            "edges": [{"id": "e_err", "source": "a", "target": "h", "data": {"kind": "error"}}],
        },
        registry,
        "env-error-broadcast",
    )
    assert result.status is RunStatus.COMPLETED
    assert err_spy.seen
    delivered = err_spy.seen[0]
    assert delivered["code"] == "timeout"
    assert delivered["message"] == "too slow"
    assert delivered["details"] == {"elapsed_ms": 99}


async def test_raised_exception_routes_error_edge_too():
    class _Raiser:
        spec: ClassVar[NodeSpec] = _spec("test.env_raiser")

        async def execute(self, ctx, inputs, config):
            raise ValueError("kapow")

    ok_spy = _SpyNode("test.env_spy_ok")
    err_spy = _SpyNode("test.env_spy_err")
    registry = _registry(_Raiser(), ok_spy, err_spy)
    definition = dict(_TRY_CATCH_DEF, nodes=_try_catch_nodes("test.env_raiser"))
    result, _, _ = await _run(definition, registry, "env-raise-route")
    assert result.status is RunStatus.COMPLETED
    # Exceptions synthesize the same NodeError: code == exception class name.
    assert err_spy.seen and err_spy.seen[0]["text"] == "kapow"
    assert not ok_spy.seen


# ---------------------------------------------------------------------------
# 5. Fan-out on_item_failure='hole'
# ---------------------------------------------------------------------------


async def test_fanout_hole_survives_failed_item_and_reports_error():
    def behavior(call: int, inputs: _In):
        value = getattr(inputs, "value", None)
        if value == "bad":
            return failure("scrape_failed", "404 not found", details={"url": value})
        return success(_Payload(text=str(value).upper(), count=call))

    worker = _EnvelopeNode("test.env_worker", behavior)
    registry = _registry(worker)
    result, _, _ = await _run(
        {
            "nodes": [
                {
                    "id": "map1",
                    "type": "control.map",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"target_node_id": "worker", "payload_key": "value"},
                        "input": {"items": ["good", "bad", "fine"]},
                    },
                },
                _node("worker", "test.env_worker", {"config": {}, "on_item_failure": "hole"}),
                _node("gather", "control.gather"),
            ],
            "edges": [
                {
                    "id": "e_wg",
                    "source": "worker",
                    "target": "gather",
                    "data": {"mappings": {"value": "text"}},
                }
            ],
            "entry_nodes": ["map1"],
        },
        registry,
        "env-hole",
    )
    assert result.status is RunStatus.COMPLETED
    gathered = result.last_outputs["gather"]
    assert sorted(gathered["values"]) == ["FINE", "GOOD"]
    assert gathered["count"] == 2
    assert gathered["expected"] == 3
    holes = gathered["holes"]
    assert len(holes) == 1
    assert holes[0]["status"] == "failed"
    assert holes[0]["error"]["code"] == "scrape_failed"
    assert holes[0]["error"]["details"] == {"url": "bad"}


async def test_fanout_default_park_policy_still_parks():
    def behavior(call: int, inputs: _In):
        value = getattr(inputs, "value", None)
        if value == "bad":
            return failure("scrape_failed", "404 not found")
        return success(_Payload(text=str(value).upper(), count=call))

    worker = _EnvelopeNode("test.env_worker2", behavior)
    registry = _registry(worker)
    result, _, _ = await _run(
        {
            "nodes": [
                {
                    "id": "map1",
                    "type": "control.map",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"target_node_id": "worker", "payload_key": "value"},
                        "input": {"items": ["good", "bad"]},
                    },
                },
                _node("worker", "test.env_worker2"),
                _node("gather", "control.gather"),
            ],
            "edges": [
                {
                    "id": "e_wg",
                    "source": "worker",
                    "target": "gather",
                    "data": {"mappings": {"value": "text"}},
                }
            ],
            "entry_nodes": ["map1"],
        },
        registry,
        "env-park",
    )
    assert result.status is RunStatus.ERRORED


# ---------------------------------------------------------------------------
# 6. Author-drift guard
# ---------------------------------------------------------------------------


async def test_success_with_wrong_payload_type_parks():
    node = _EnvelopeNode("test.env_drift", lambda n, i: success(_OtherPayload()))
    registry = _registry(node)
    result, _, _ = await _run(
        {"nodes": [_node("a", "test.env_drift")], "edges": []},
        registry,
        "env-drift",
    )
    assert result.status is RunStatus.ERRORED
    assert "output_schema" in (result.error or "")


async def test_fanned_failure_routes_error_edge_when_no_hole_policy():
    """Adversarial finding #1: Send-driven invocations (map items, loop
    bodies) carry a dispatch_id — ERROR edges must still route for them
    when on_item_failure is the default 'park'."""

    def behavior(call: int, inputs: _In):
        value = getattr(inputs, "value", None)
        if value == "bad":
            return failure("scrape_failed", "404")
        return success(_Payload(text=str(value).upper(), count=call))

    worker = _EnvelopeNode("test.env_worker3", behavior)
    err_spy = _SpyNode("test.env_spy_err")
    registry = _registry(worker, err_spy)
    result, _, _ = await _run(
        {
            "nodes": [
                {
                    "id": "map1",
                    "type": "control.map",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"target_node_id": "worker", "payload_key": "value"},
                        "input": {"items": ["bad"]},
                    },
                },
                _node("worker", "test.env_worker3"),
                _node("h", "test.env_spy_err"),
            ],
            "edges": [
                {"id": "e_err", "source": "worker", "target": "h", "data": {"kind": "error"}}
            ],
            "entry_nodes": ["map1"],
        },
        registry,
        "env-fanned-error-edge",
    )
    assert result.status is RunStatus.COMPLETED
    # A fanned source delivers over its ERROR edge as an aggregated §4.4
    # items group — each failed item carries its structured error.
    assert err_spy.seen
    items = err_spy.seen[0]["items"]
    assert items[0]["status"] == "failed"
    assert items[0]["error"]["code"] == "scrape_failed"


async def test_mixed_inbound_handler_does_not_fire_on_success():
    """Adversarial finding #2: a handler wired A --error--> H, B --data--> H
    must NOT fire when A succeeds (inbound ERROR edges gate the firing)."""
    a = _EnvelopeNode("test.env_ok4", lambda n, i: success(_Payload(text="fine", count=1)))
    b = _EnvelopeNode("test.env_ok5", lambda n, i: success(_Payload(text="ctx", count=2)))
    handler = _SpyNode("test.env_spy_err")
    registry = _registry(a, b, handler)
    result, _, _ = await _run(
        {
            "nodes": [
                _node("a", "test.env_ok4"),
                _node("b", "test.env_ok5"),
                _node("h", "test.env_spy_err"),
            ],
            "edges": [
                {"id": "e_err", "source": "a", "target": "h", "data": {"kind": "error"}},
                {
                    "id": "e_ctx",
                    "source": "b",
                    "target": "h",
                    "data": {"mappings": {"text": "text"}},
                },
            ],
        },
        registry,
        "env-mixed-gate-success",
    )
    assert result.status is RunStatus.COMPLETED
    assert not handler.seen  # gate held: no spurious error-handler run


async def test_mixed_inbound_handler_fires_on_failure_with_context():
    a = _EnvelopeNode("test.env_fail4", lambda n, i: failure("boom_code", "boom"))
    b = _EnvelopeNode("test.env_ok6", lambda n, i: success(_Payload(text="ctx", count=2)))
    handler = _SpyNode("test.env_spy_err")
    registry = _registry(a, b, handler)
    result, _, _ = await _run(
        {
            "nodes": [
                _node("a", "test.env_fail4"),
                _node("b", "test.env_ok6"),
                _node("h", "test.env_spy_err"),
            ],
            "edges": [
                {
                    "id": "e_err",
                    "source": "a",
                    "target": "h",
                    "data": {"kind": "error", "mappings": {"text": "message"}},
                },
                {
                    "id": "e_ctx",
                    "source": "b",
                    "target": "h",
                    "data": {"mappings": {"count": "count"}},
                },
            ],
        },
        registry,
        "env-mixed-gate-failure",
    )
    assert result.status is RunStatus.COMPLETED
    assert handler.seen
    assert handler.seen[0]["text"] == "boom"  # the error
    assert handler.seen[0]["count"] == 2  # the sibling context


async def test_success_accepts_generic_origin_payload():
    """Adversarial finding #6: pydantic parametrized generics — a node
    declaring output_schema=Value[Any] but constructing bare Value(...) or
    Value[int](...) must not park as author drift."""
    from matrx_graph.types.canonical_payloads import Value

    class _GenericNode:
        spec: ClassVar[NodeSpec] = NodeSpec(
            type="test.env_generic",
            category=NodeCategory.DATA,
            display_name="generic",
            description="",
            input_schema=_In,
            output_schema=Value[Any],
            config_schema=_Cfg,
            handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
            determinism=ActionTier.PURE,
        )

        async def execute(self, ctx, inputs, config):
            return success(Value(value=42))  # unparametrized — origin match

    registry = _registry(_GenericNode())
    result, _, _ = await _run(
        {"nodes": [_node("a", "test.env_generic")], "edges": []},
        registry,
        "env-generic-origin",
    )
    assert result.status is RunStatus.COMPLETED
    assert result.last_outputs["a"]["value"] == 42


async def test_legacy_replay_strips_unknown_keys_loudly():
    """Adversarial finding #3: a pre-migration outcome row (old payload shape
    with removed fields) must replay by stripping unknown keys, not re-park."""
    from matrx_graph import MemoryCheckpointer, NodeOutcome

    node = _EnvelopeNode("test.env_replay", lambda n, i: success(_Payload(text="fresh", count=1)))
    registry = _registry(node)
    checkpointer = MemoryCheckpointer()
    # Simulate a pre-migration recorded success with a now-removed field.
    await checkpointer.record_outcome(
        NodeOutcome(
            run_id="env-legacy-replay",
            step=0,
            node_id="a",
            attempt=1,
            output={"text": "old", "count": 5, "ok": True},
        )
    )
    graph = compile_graph(
        Definition.model_validate({"nodes": [_node("a", "test.env_replay")], "edges": []}),
        registry=registry,
    )
    scheduler = Scheduler(graph, checkpointer, make_app_context(FakeEmitter()), registry=registry)
    result = await scheduler.run(run_id="env-legacy-replay")
    assert result.status is RunStatus.COMPLETED
    # Replayed from the historical row (stripped), NOT re-executed.
    assert result.last_outputs["a"] == {"text": "old", "count": 5}
    assert node.calls == 0


async def test_non_model_return_parks_with_clear_message():
    node = _EnvelopeNode("test.env_dict", lambda n, i: {"raw": "dict"})
    registry = _registry(node)
    result, _, _ = await _run(
        {"nodes": [_node("a", "test.env_dict")], "edges": []},
        registry,
        "env-dict",
    )
    assert result.status is RunStatus.ERRORED
    assert "NodeResult" in (result.error or "")


async def test_bare_basemodel_return_parks_post_ratchet_zero():
    """Ratchet zero: the legacy bare-BaseModel branch is DELETED — a node
    returning its payload without the envelope is a hard error, both in the
    scheduler and in the shared interpret_node_result helper."""
    import pytest
    from matrx_graph.types.result import interpret_node_result

    node = _EnvelopeNode("test.env_bare", lambda n, i: _Payload(text="bare", count=1))
    registry = _registry(node)
    result, _, _ = await _run(
        {"nodes": [_node("a", "test.env_bare")], "edges": []},
        registry,
        "env-bare",
    )
    assert result.status is RunStatus.ERRORED
    assert "NodeResult" in (result.error or "")

    with pytest.raises(TypeError, match="NodeResult"):
        interpret_node_result(_Payload())
