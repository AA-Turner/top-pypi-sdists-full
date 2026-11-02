"""ERRORS ARE KINDS — KINDS_EVERYWHERE_PLAN §10d-B3.

Before this, a node failure was the ONE value the engine produced that crossed
every boundary anonymously: the ERROR edge carried a bare three-field dump, the
``error`` column carried a DIFFERENT (superset) loose dict, and
``node_failed`` shipped a raw object the frontend could only print. A
kind-filtered edge could not select it and a trigger could not subscribe to it.

These tests pin the fix, and they are forcing functions: every assertion reads
what the ENGINE actually produced on a real run of a real graph whose node
really failed — never a hand-built model.

  1. The failure that rides an ERROR edge says what it is (``__kind``), and the
     handler can still map ``code``/``message`` exactly as before.
  2. The persisted ``error`` column and ``node_failed.error`` are the SAME
     self-describing instance — one failure, one shape, not three dialects.
  3. ``node_failed`` carries the ``node_outcome`` wrapper with
     ``status="failed"`` and the ``node_error`` NESTED under ``error`` — the
     same packet shape a completion ships, so a consumer renders both through
     one path.
  4. The structured half (cause/step_id/technical/fields) rides ON the kind,
     and nested field problems are their own ``field_problem`` kind instances
     (sectioned, not flattened).
  5. Backward compatibility: every key the old loose dict carried is still
     there, so no existing reader breaks.
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
from matrx_graph.content_ir.model import kind_of
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory, RetryPolicy
from matrx_graph.types.result import NodeResult, failure, success
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context


class _In(BaseModel):
    model_config = ConfigDict(extra="allow")


class _Payload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = "ok"


class _Cfg(BaseModel):
    model_config = ConfigDict(extra="forbid")


def _spec(node_type: str) -> NodeSpec:
    return NodeSpec(
        type=node_type,
        category=NodeCategory.DATA,
        display_name=node_type,
        description="node_error kind test node",
        input_schema=_In,
        output_schema=_Payload,
        config_schema=_Cfg,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        retry=RetryPolicy(max_attempts=1),
    )


class _FailingNode:
    """Fails deliberately, the way a real node reports a real problem."""

    def __init__(self, node_type: str, *, raises: bool = False) -> None:
        self.spec: NodeSpec = _spec(node_type)
        self._raises = raises

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg
    ) -> NodeResult[_Payload]:
        if self._raises:
            raise ValueError("the provider hung up")
        return failure(
            "rate_limited",
            "The search provider is rate limiting us.",
            details={"retry_after_s": 30},
        )


class _SpyNode:
    """Records what the ERROR edge actually delivered."""

    spec: ClassVar[NodeSpec]

    def __init__(self, node_type: str) -> None:
        self.spec = _spec(node_type)
        self.seen: list[dict[str, Any]] = []

    async def execute(
        self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg
    ) -> NodeResult[_Payload]:
        self.seen.append(inputs.model_dump())
        return success(_Payload(text="handled"))


def _registry(*executors: Any) -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    for ex in executors:
        reg.register(ex, overwrite=True)
    return reg


def _node(node_id: str, node_type: str) -> dict:
    return {
        "id": node_id,
        "type": node_type,
        "position": {"x": 0, "y": 0},
        "data": {"config": {}},
    }


async def _run(definition: dict, registry: NodeRegistry, run_id: str):
    graph = compile_graph(Definition.model_validate(definition), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    result = await scheduler.run(run_id=run_id)
    return result, scheduler, emitter


def _events(emitter: FakeEmitter, name: str) -> list[dict]:
    return [
        e
        for k, e in emitter.events
        if k == "data" and isinstance(e, dict) and e.get("event") == name
    ]


# ---------------------------------------------------------------------------
# 1 + 4 + 5 — the ERROR edge carries a self-describing node_error
# ---------------------------------------------------------------------------


async def test_error_edge_delivers_a_self_describing_node_error():
    node = _FailingNode("test.b3_fail")
    spy = _SpyNode("test.b3_handler")
    result, scheduler, emitter = await _run(
        {
            "nodes": [_node("a", "test.b3_fail"), _node("h", "test.b3_handler")],
            "edges": [
                {
                    "id": "e1",
                    "source": "a",
                    "target": "h",
                    "data": {"kind": "error", "mappings": {"text": "message"}},
                }
            ],
        },
        _registry(node, spy),
        "b3-edge",
    )
    assert result.status is RunStatus.COMPLETED  # the handler absorbed it
    # The handler still maps the failure's own keys — nothing about the old
    # addressing changed.
    assert spy.seen and spy.seen[0]["text"] == "The search provider is rate limiting us."

    failed = _events(emitter, "node_failed")
    assert len(failed) == 1
    error = failed[0]["error"]
    # THE POINT: the failure says what it IS. A kind-filtered edge and a
    # trigger can now select on this; a renderer can route on it.
    assert kind_of(error) == "node_error"
    # …without losing anything the old loose dict carried.
    assert error["code"] == "rate_limited"
    assert error["message"] == "The search provider is rate limiting us."
    assert error["details"] == {"retry_after_s": 30}
    assert error["type"] == "rate_limited"
    # The structured half rides ON the kind now, not in a parallel dict.
    assert error["cause"]
    assert error["step_id"] == "a"
    assert error["technical"]


# ---------------------------------------------------------------------------
# 2 — one failure, one shape: the column and the event are the same instance
# ---------------------------------------------------------------------------


async def test_persisted_error_and_event_error_are_the_same_kind_instance():
    node = _FailingNode("test.b3_fail_park")
    result, scheduler, emitter = await _run(
        {"nodes": [_node("a", "test.b3_fail_park")], "edges": []},
        _registry(node),
        "b3-park",
    )
    assert result.status is RunStatus.ERRORED  # no ERROR edge → the run parks

    outcome = await scheduler.checkpointer.get_outcome(
        run_id="b3-park", step=0, node_id="a", attempt=1
    )
    assert outcome is not None and outcome.error is not None
    assert kind_of(outcome.error) == "node_error"

    failed = _events(emitter, "node_failed")
    assert failed and failed[0]["error"] == outcome.error


# ---------------------------------------------------------------------------
# 3 — the runtime wrapper family's failure member
# ---------------------------------------------------------------------------


async def test_node_failed_ships_the_node_outcome_wrapper_with_the_error_nested():
    node = _FailingNode("test.b3_wrapped", raises=True)
    _result, _scheduler, emitter = await _run(
        {"nodes": [_node("a", "test.b3_wrapped")], "edges": []},
        _registry(node),
        "b3-wrapper",
    )
    failed = _events(emitter, "node_failed")
    assert failed
    wrapper = failed[0]["wrapper"]
    assert wrapper is not None, "the failure path must ship the runtime wrapper too"
    assert kind_of(wrapper) == "node_outcome"
    assert wrapper["status"] == "failed"
    assert wrapper["node_id"] == "a"
    # The data kind's slot is empty and the failure is NESTED — same packet
    # shape as a completion, one rendering path for both.
    assert wrapper["output"] is None
    assert kind_of(wrapper["error"]) == "node_error"
    assert wrapper["error"]["type"] == "ValueError"
    assert wrapper["error"]["message"] == "the provider hung up"


# ---------------------------------------------------------------------------
# 4 — nested field problems are their own kind (sectioned, not flattened)
# ---------------------------------------------------------------------------


async def test_validation_failure_nests_field_problem_kind_instances():
    """A node whose own parse rejects a payload — the everyday extraction
    failure. The exception carries WHICH field and WHY, so the failure kind
    carries it too, each problem its own nested ``field_problem``."""

    class _Extracted(BaseModel):
        model_config = ConfigDict(extra="forbid")

        topic: str

    class _ParsingNode:
        spec: ClassVar[NodeSpec] = _spec("test.b3_parse")

        async def execute(
            self, ctx: NodeExecutionContext, inputs: _In, config: _Cfg
        ) -> NodeResult[_Payload]:
            # The provider answered without the field the contract requires.
            _Extracted.model_validate({})
            raise AssertionError("unreachable")  # pragma: no cover

    _result, _scheduler, emitter = await _run(
        {"nodes": [_node("a", "test.b3_parse")], "edges": []},
        _registry(_ParsingNode()),
        "b3-fields",
    )
    failed = _events(emitter, "node_failed")
    assert failed
    error = failed[0]["error"]
    assert kind_of(error) == "node_error"
    assert error["type"] == "ValidationError"
    assert error.get("field") == "topic"
    problems = error.get("fields") or []
    assert problems, "a validation failure must name its bad fields"
    assert all(kind_of(p) == "field_problem" for p in problems)
    assert problems[0]["field"] == "topic"
