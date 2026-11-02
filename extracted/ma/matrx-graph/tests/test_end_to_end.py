from __future__ import annotations

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
from matrx_graph.errors import CompilationError, ExecutionError
from matrx_graph.types.result import NodeResult, success

from tests._fixtures import FakeEmitter, make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _graph_from_dict(data: dict, registry: NodeRegistry):
    definition = Definition.model_validate(data)
    return compile_graph(definition, registry=registry)


async def test_transform_then_branch_routes_to_true_handle():
    """A → transform(x*2) → branch(result>5) → true-path → sink

    Verifies: data flow between nodes, handle-based routing, PURE determinism,
    end-to-end completion.
    """
    registry = _registry()
    data = {
        "nodes": [
            {
                "id": "double",
                "type": "data.transform",
                "position": {"x": 0, "y": 0},
                "data": {"config": {"expression": "inputs['value'] * 2"}},
            },
            {
                "id": "gt5",
                "type": "control.branch",
                "position": {"x": 200, "y": 0},
                "data": {"config": {"predicate": "inputs['result'] > 5"}},
            },
            {
                "id": "sink_true",
                "type": "data.transform",
                "position": {"x": 400, "y": -50},
                "data": {"config": {"expression": "'HIT_TRUE'"}},
            },
            {
                "id": "sink_false",
                "type": "data.transform",
                "position": {"x": 400, "y": 50},
                "data": {"config": {"expression": "'HIT_FALSE'"}},
            },
        ],
        "edges": [
            {"id": "e1", "source": "double", "target": "gt5"},
            {
                "id": "e2",
                "source": "gt5",
                "sourceHandle": "true",
                "target": "sink_true",
                "data": {"kind": "conditional"},
            },
            {
                "id": "e3",
                "source": "gt5",
                "sourceHandle": "false",
                "target": "sink_false",
                "data": {"kind": "conditional"},
            },
        ],
    }
    graph = _graph_from_dict(data, registry)

    app = make_app_context(FakeEmitter())
    scheduler = Scheduler(graph, MemoryCheckpointer(), app, registry=registry)

    result = await scheduler.run(run_id="run-1", inputs={"value": 4})

    assert result.status is RunStatus.COMPLETED
    # 4 * 2 = 8, which IS > 5 → went 'true' → sink_true fired
    assert result.last_outputs["sink_true"]["result"] == "HIT_TRUE"
    assert "sink_false" not in result.last_outputs  # false path did NOT run


async def test_branch_false_path_takes_only_false_handle():
    registry = _registry()
    data = {
        "nodes": [
            {
                "id": "double",
                "type": "data.transform",
                "position": {"x": 0, "y": 0},
                "data": {"config": {"expression": "inputs['value'] * 2"}},
            },
            {
                "id": "gt5",
                "type": "control.branch",
                "position": {"x": 200, "y": 0},
                "data": {"config": {"predicate": "inputs['result'] > 5"}},
            },
            {
                "id": "sink_true",
                "type": "data.transform",
                "position": {"x": 400, "y": 0},
                "data": {"config": {"expression": "'HIT_TRUE'"}},
            },
            {
                "id": "sink_false",
                "type": "data.transform",
                "position": {"x": 400, "y": 50},
                "data": {"config": {"expression": "'HIT_FALSE'"}},
            },
        ],
        "edges": [
            {"id": "e1", "source": "double", "target": "gt5"},
            {
                "id": "e2",
                "source": "gt5",
                "sourceHandle": "true",
                "target": "sink_true",
                "data": {"kind": "conditional"},
            },
            {
                "id": "e3",
                "source": "gt5",
                "sourceHandle": "false",
                "target": "sink_false",
                "data": {"kind": "conditional"},
            },
        ],
    }
    graph = _graph_from_dict(data, registry)

    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    # 2 * 2 = 4, NOT > 5 → false path
    result = await scheduler.run(run_id="run-2", inputs={"value": 2})

    assert result.status is RunStatus.COMPLETED
    assert result.last_outputs["sink_false"]["result"] == "HIT_FALSE"
    assert "sink_true" not in result.last_outputs


async def test_human_input_interrupts_and_resumes():
    """Start a graph that hits a human_input node → run returns INTERRUPTED →
    resume with a value → downstream node receives the value as its input →
    run completes.
    """
    registry = _registry()
    data = {
        "nodes": [
            {
                "id": "ask",
                "type": "control.human_input",
                "position": {"x": 0, "y": 0},
                "data": {"config": {"prompt": "What's your favorite color?"}},
            },
            {
                "id": "echo",
                "type": "data.transform",
                "position": {"x": 200, "y": 0},
                "data": {
                    # Sandbox forbids function calls, so no str() or f-strings.
                    # Use direct concatenation — answer is already a string.
                    "config": {"expression": "'You said ' + inputs['answer']"}
                },
            },
        ],
        "edges": [
            {"id": "e1", "source": "ask", "target": "echo"},
        ],
    }
    graph = _graph_from_dict(data, registry)

    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(graph, checkpointer, make_app_context(), registry=registry)

    result = await scheduler.run(run_id="run-hi-1")
    assert result.status is RunStatus.INTERRUPTED
    assert result.interrupt is not None
    assert result.interrupt["node_id"] == "ask"
    assert result.interrupt["payload"]["prompt"] == "What's your favorite color?"

    # Find the interrupt checkpoint and resume from it
    checkpoints = await checkpointer.list_checkpoints("run-hi-1")
    interrupt_cp = next(cp for cp in checkpoints if cp.interrupt_payload)

    # New scheduler instance — verifies resume doesn't need in-memory state
    resumed_scheduler = Scheduler(graph, checkpointer, make_app_context(), registry=registry)
    resume_result = await resumed_scheduler.resume(
        run_id="run-hi-1",
        checkpoint_id=interrupt_cp.checkpoint_id,
        resume_value={"answer": "blue"},
    )
    assert resume_result.status is RunStatus.COMPLETED
    assert resume_result.last_outputs["echo"]["result"] == "You said blue"


async def test_human_input_resume_schema_fails_before_recording_outcome():
    """An invalid approval cannot be persisted or routed downstream."""
    registry = _registry()
    data = {
        "nodes": [
            {
                "id": "approve",
                "type": "control.human_input",
                "position": {"x": 0, "y": 0},
                "data": {
                    "config": {
                        "prompt": "Approve containment?",
                        "schema_hint": {
                            "type": "object",
                            "required": ["decision", "approver"],
                            "additionalProperties": False,
                            "properties": {
                                "decision": {"enum": ["approve", "reject"]},
                                "approver": {"type": "string", "minLength": 1},
                            },
                        },
                    }
                },
            }
        ],
        "edges": [],
    }
    graph = _graph_from_dict(data, registry)
    checkpointer = MemoryCheckpointer()

    interrupted = await Scheduler(graph, checkpointer, make_app_context(), registry=registry).run(
        run_id="run-hi-schema"
    )
    assert interrupted.status is RunStatus.INTERRUPTED
    checkpoint = next(
        cp for cp in await checkpointer.list_checkpoints("run-hi-schema") if cp.interrupt_payload
    )

    with pytest.raises(ExecutionError, match="Resume value does not satisfy"):
        await Scheduler(graph, checkpointer, make_app_context(), registry=registry).resume(
            run_id="run-hi-schema",
            checkpoint_id=checkpoint.checkpoint_id,
            resume_value={"decision": "maybe"},
        )

    outcome = await checkpointer.get_outcome(
        run_id="run-hi-schema",
        step=checkpoint.step,
        node_id="approve",
        attempt=1,
    )
    assert outcome is None

    completed = await Scheduler(graph, checkpointer, make_app_context(), registry=registry).resume(
        run_id="run-hi-schema",
        checkpoint_id=checkpoint.checkpoint_id,
        resume_value={"decision": "approve", "approver": "incident commander"},
    )
    assert completed.status is RunStatus.COMPLETED


async def test_resume_rejects_checkpoint_from_a_different_run():
    registry = _registry()
    graph = _graph_from_dict(
        {
            "nodes": [
                {
                    "id": "ask",
                    "type": "control.human_input",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"prompt": "Continue?"}},
                }
            ],
            "edges": [],
        },
        registry,
    )
    checkpointer = MemoryCheckpointer()
    await Scheduler(graph, checkpointer, make_app_context(), registry=registry).run(
        run_id="original-run"
    )
    checkpoint = next(
        cp for cp in await checkpointer.list_checkpoints("original-run") if cp.interrupt_payload
    )

    with pytest.raises(ExecutionError, match="belongs to run"):
        await Scheduler(graph, checkpointer, make_app_context(), registry=registry).resume(
            run_id="different-run",
            checkpoint_id=checkpoint.checkpoint_id,
            resume_value={"answer": "yes"},
        )


async def test_human_input_sandbox_rejects_function_calls():
    """Regression: the sandbox admits ONLY safe-helper calls (bare whitelisted
    names, positional args). Every actual escape vector stays rejected —
    attribute access above all, because `.format`/`.__class__` traversal is
    the escape primitive the original ban existed for."""
    from matrx_graph.errors import ExecutionError
    from matrx_graph.nodes._sandbox import safe_eval

    with pytest.raises(ExecutionError, match="Disallowed"):
        safe_eval("inputs.get('x')", {})  # attribute access — ALWAYS forbidden
    with pytest.raises(ExecutionError, match="Disallowed"):
        # method call = attribute access; the str.format escape can't be spelled
        safe_eval("'{0.__class__}'.format(inputs)", {})
    with pytest.raises(ExecutionError, match="Disallowed"):
        safe_eval("__import__('os')", {})  # non-whitelisted name
    with pytest.raises(ExecutionError, match="Disallowed"):
        safe_eval("getattr(inputs, 'x')", {})  # traversal helper — not in table
    with pytest.raises(ExecutionError, match="Disallowed"):
        safe_eval("inputs['f'](1)", {"f": print})  # non-Name call target
    with pytest.raises(ExecutionError, match="Disallowed"):
        safe_eval("sorted(inputs['xs'], key=len)", {"xs": []})  # keywords banned


async def test_sandbox_safe_helpers():
    """The safe-helper primitive: pure builtins callable by bare name — what
    W1's GATE 1 (`len(...) >= 1000`), W2's keep-best guards, and W4's
    prompt-list caps run on."""
    from matrx_graph.nodes._sandbox import safe_eval

    assert safe_eval("len(inputs['list'])", {"list": [1, 2, 3]}) == 3
    assert safe_eval("str(inputs['answer'])", {"answer": 7}) == "7"
    assert safe_eval("min(3, len(inputs['s'] or ''))", {"s": "ab"}) == 2
    assert (
        safe_eval(
            "inputs['a'] if len(inputs['a'] or '') >= 2 else inputs['b']",
            {"a": "x", "b": "fallback"},
        )
        == "fallback"
    )
    assert safe_eval("(inputs['xs'] or [])[:2]", {"xs": [1, 2, 3]}) == [1, 2]


async def test_sandbox_rejects_exponentiation():
    """Regression: `10**10**10` computes an exponential tower eagerly — a
    one-line CPU/memory DoS that no timeout can interrupt (a single C-level
    big-int multiply ignores both KeyboardInterrupt and asyncio timeouts).
    ast.Pow must stay out of BOTH sandbox whitelists."""
    import ast as _ast

    from matrx_graph.errors import ExecutionError
    from matrx_graph.nodes._sandbox import safe_eval

    with pytest.raises(ExecutionError, match="Disallowed"):
        safe_eval("10**10**10", {})
    with pytest.raises(ExecutionError, match="Disallowed"):
        safe_eval("inputs['x'] ** inputs['y']", {"x": 2, "y": 3})

    # custom_extract's richer sandbox must reject Pow at AST-validation
    # time, before any execution starts.
    from matrx_graph.nodes.text.custom_extract import _Walker

    tree = _ast.parse("__result__ = 10**10**10", mode="exec")
    with pytest.raises(ExecutionError, match="Pow"):
        _Walker(frozenset()).visit(tree)


async def test_send_dynamic_fanout_dispatches_parallel_workers():
    """A dispatcher node emits 3 Sends to a 'worker' node; verify each worker
    invocation ran independently with its own payload.
    """
    registry = _registry()

    # We need a custom worker and dispatcher — inline executors so the test is self-contained.
    from matrx_graph import NodeCategory, NodeSpec
    from matrx_graph.types.context import NodeExecutionContext
    from matrx_graph.types.handle import HandleDirection, HandleSpec
    from pydantic import BaseModel, ConfigDict

    class DispatchOut(BaseModel):
        model_config = ConfigDict(extra="forbid")
        dispatched: int

    class DispatchExec:
        spec = NodeSpec(
            type="test.dispatch",
            category=NodeCategory.CUSTOM,
            display_name="Dispatch",
            launches_nodes=True,  # ctx.send to a run-time target
            output_schema=DispatchOut,
            handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
        )

        async def execute(
            self, ctx: NodeExecutionContext, inputs, config
        ) -> NodeResult[DispatchOut]:
            for item in ("alpha", "beta", "gamma"):
                ctx.send("worker", {"name": item})
            return success(DispatchOut(dispatched=3))

    class WorkerIn(BaseModel):
        model_config = ConfigDict(extra="allow")
        name: str = ""

    class WorkerOut(BaseModel):
        model_config = ConfigDict(extra="forbid")
        processed: str

    received: list[str] = []

    class WorkerExec:
        spec = NodeSpec(
            type="test.worker",
            category=NodeCategory.CUSTOM,
            display_name="Worker",
            input_schema=WorkerIn,
            output_schema=WorkerOut,
            handles=(HandleSpec(id="in", direction=HandleDirection.INPUT),),
        )

        async def execute(
            self, ctx: NodeExecutionContext, inputs: WorkerIn, config
        ) -> NodeResult[WorkerOut]:
            received.append(inputs.name)
            return success(WorkerOut(processed=inputs.name.upper()))

    registry.register(DispatchExec())
    registry.register(WorkerExec())

    data = {
        "nodes": [
            {
                "id": "disp",
                "type": "test.dispatch",
                "position": {"x": 0, "y": 0},
                "data": {},
            },
            {
                "id": "worker",
                "type": "test.worker",
                "position": {"x": 200, "y": 0},
                "data": {},
            },
        ],
        "edges": [],  # sends are the only way into 'worker'
        # Explicit entry — worker has no incoming edges but is only reached via
        # Sends, not as a graph entry point.
        "entry_nodes": ["disp"],
    }
    graph = _graph_from_dict(data, registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    result = await scheduler.run(run_id="run-fanout")

    assert result.status is RunStatus.COMPLETED
    # The dispatcher plus 3 worker invocations all ran
    assert set(received) == {"alpha", "beta", "gamma"}


async def test_channel_writes_reduced_across_super_steps():
    """Two nodes write to an 'append' channel in the same super-step; the
    reducer merges both values.
    """
    registry = _registry()

    from matrx_graph import ChannelSpec, NodeCategory, NodeSpec
    from matrx_graph.types.context import NodeExecutionContext
    from matrx_graph.types.handle import HandleDirection, HandleSpec
    from pydantic import BaseModel, ConfigDict

    class WriterOut(BaseModel):
        model_config = ConfigDict(extra="forbid")
        who: str

    class WriterA:
        spec = NodeSpec(
            type="test.writer_a",
            category=NodeCategory.CUSTOM,
            display_name="A",
            output_schema=WriterOut,
            handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
        )

        async def execute(self, ctx: NodeExecutionContext, inputs, config):
            ctx.channels.write("log", "A")
            return success(WriterOut(who="A"))

    class WriterB:
        spec = NodeSpec(
            type="test.writer_b",
            category=NodeCategory.CUSTOM,
            display_name="B",
            output_schema=WriterOut,
            handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
        )

        async def execute(self, ctx: NodeExecutionContext, inputs, config):
            ctx.channels.write("log", "B")
            return success(WriterOut(who="B"))

    registry.register(WriterA())
    registry.register(WriterB())

    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "a",
                    "type": "test.writer_a",
                    "position": {"x": 0, "y": 0},
                    "data": {},
                },
                {
                    "id": "b",
                    "type": "test.writer_b",
                    "position": {"x": 100, "y": 0},
                    "data": {},
                },
            ],
            "edges": [],
            "channels": [ChannelSpec(name="log", reducer="append", default=[]).model_dump()],
        }
    )
    graph = compile_graph(definition, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    result = await scheduler.run(run_id="run-channels")

    assert result.status is RunStatus.COMPLETED
    # Both writers ran in the same super-step; the append reducer collected both
    assert sorted(result.channel_values["log"]) == ["A", "B"]


async def test_idempotency_replays_prior_outcome_on_resume():
    """Run a graph to completion, then resume from an interrupt checkpoint
    (by injecting one manually) and verify the already-recorded outcome is
    replayed rather than re-invoked.
    """
    registry = _registry()

    call_count = {"n": 0}

    from matrx_graph import NodeCategory, NodeSpec
    from matrx_graph.types.context import NodeExecutionContext
    from matrx_graph.types.handle import HandleDirection, HandleSpec
    from pydantic import BaseModel, ConfigDict

    class CounterOut(BaseModel):
        model_config = ConfigDict(extra="forbid")
        n: int

    class Counter:
        spec = NodeSpec(
            type="test.counter",
            category=NodeCategory.CUSTOM,
            display_name="Counter",
            output_schema=CounterOut,
            handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
        )

        async def execute(self, ctx: NodeExecutionContext, inputs, config):
            call_count["n"] += 1
            return success(CounterOut(n=call_count["n"]))

    registry.register(Counter())

    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "c",
                    "type": "test.counter",
                    "position": {"x": 0, "y": 0},
                    "data": {},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(definition, registry=registry)
    checkpointer = MemoryCheckpointer()
    scheduler = Scheduler(graph, checkpointer, make_app_context(), registry=registry)

    result = await scheduler.run(run_id="run-idem")
    assert result.status is RunStatus.COMPLETED
    assert call_count["n"] == 1

    # Now pretend we resume — the counter node should NOT execute again
    # because its outcome is recorded. We simulate resume by re-running via
    # a new scheduler instance with the same checkpointer (prior outcomes
    # still present).
    scheduler2 = Scheduler(graph, checkpointer, make_app_context(), registry=registry)
    result2 = await scheduler2.run(run_id="run-idem")  # same run_id, same step+attempt
    assert result2.status is RunStatus.COMPLETED
    assert call_count["n"] == 1  # counter was NOT re-invoked — idempotency worked


async def test_unknown_node_type_fails_compile():
    registry = _registry()
    data = {
        "nodes": [
            {
                "id": "x",
                "type": "nonexistent.type",
                "position": {"x": 0, "y": 0},
                "data": {},
            }
        ],
        "edges": [],
    }
    with pytest.raises(CompilationError):
        _graph_from_dict(data, registry)
