"""Execution provenance reaches the executor and sampled preflight, never caller inputs."""
from __future__ import annotations

import pytest
from pydantic import BaseModel, ConfigDict

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import success
from tests._fixtures import make_app_context


class Payload(BaseModel):
    model_config = ConfigDict(extra="allow")


class Observer:
    spec = NodeSpec(
        type="test.provenance_observer", category=NodeCategory.DATA,
        display_name="Observer", description="Observe the running leg",
        input_schema=Payload, output_schema=Payload, config_schema=Payload,
        handles=(HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
                 HandleSpec(id="out", direction=HandleDirection.OUTPUT)),
        determinism=ActionTier.PURE,
    )

    def __init__(self):
        self.seen = []

    def observe(self, ctx):
        self.seen.append((ctx.execution_job_id, ctx.execution_job_kind,
                          ctx.definition_version_id, ctx.definition_hash))

    async def execute(self, ctx, inputs, config):
        self.observe(ctx)
        return success(Payload())

    async def sample_preflight(self, ctx, inputs, config):
        self.observe(ctx)
        return {"checked": True}


def graph_for(observer):
    registry = NodeRegistry()
    registry.register(observer)
    definition = Definition.model_validate({"nodes": [{"id": "observe", "type": "test.provenance_observer",
        "position": {"x": 0, "y": 0}, "data": {"config": {}}}], "edges": []})
    return compile_graph(definition, registry=registry), registry


@pytest.mark.parametrize("job_id,kind,version,sampled", [
    ("start-leg-87", "start", "version-12", False),
    ("resume-leg-96", "resume", "version-48", True),
    (None, None, None, False),
])
async def test_scheduler_gives_real_executor_or_preflight_leg_and_compiled_provenance(job_id, kind, version, sampled):
    observer = Observer()
    graph, registry = graph_for(observer)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry,
                          definition_version_id=version, execution_job_id=job_id,
                          execution_job_kind=kind,
                          sampled_outputs={"observe": {}} if sampled else None)
    result = await scheduler.run(run_id="run-provenance", inputs={"execution_job_id": "forged",
        "execution_job_kind": "forged", "definition_version_id": "forged", "definition_hash": "forged"})
    assert result.status is RunStatus.COMPLETED, result.error
    assert observer.seen == [(job_id, kind, version, graph.definition_hash)]


def test_original_context_positional_arguments_do_not_shift():
    args = [None, "run", "thread", "node", 1, 2, None, None, "dispatch", 3, 4, "registry",
            "kind", "workflow", "answer", ("output",)]
    ctx = NodeExecutionContext(*args)
    assert (ctx.dispatch_id, ctx.registry, ctx.output_reads) == ("dispatch", "registry", ("output",))
    assert (ctx.execution_job_id, ctx.execution_job_kind, ctx.definition_version_id, ctx.definition_hash) == (None, None, None, None)


async def test_inline_child_uses_its_own_definition_without_inheriting_parents_job():
    from types import SimpleNamespace

    from matrx_graph.nodes.subgraph.inline import run_inline_child

    observer = Observer()
    graph, registry = graph_for(observer)
    app = make_app_context()
    parent = SimpleNamespace(run_id="parent-run", thread_id="parent-run", node_id="call",
                             dispatch_id="parent-dispatch", item_index=0, firing=0, app=app,
                             execution_job_id="parent-job", execution_job_kind="start",
                             definition_version_id="parent-version", definition_hash="parent-hash")
    result = await run_inline_child(parent, graph, checkpointer=MemoryCheckpointer(), registry=registry,
                                    inputs={}, definition_version_id="child-version")
    assert result.status is RunStatus.COMPLETED, result.error
    assert observer.seen == [(None, None, "child-version", graph.definition_hash)]


async def test_code_pipe_delegate_receives_scheduler_provenance():
    from matrx_graph import register_builtin_nodes

    observer = Observer()
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(observer)
    definition = Definition.model_validate({"nodes": [{"id": "dispatch", "type": "pipe.step",
        "position": {"x": 0, "y": 0}, "data": {"config": {
            "contract": {"name": "Observe the execution", "output_schema": {"type": "object"}},
            "pipes": {"code": {"node_type": "test.provenance_observer"}},
            "policy": {"pipe": "code"}}}}], "edges": []})
    graph = compile_graph(definition, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry,
                          definition_version_id="delegate-version", execution_job_id="delegate-leg",
                          execution_job_kind="resume")
    result = await scheduler.run(run_id="delegated-run")
    assert result.status is RunStatus.COMPLETED, result.error
    assert observer.seen == [("delegate-leg", "resume", "delegate-version", graph.definition_hash)]


async def test_scheduler_retains_all_original_positional_arguments():
    observer = Observer()
    graph, registry = graph_for(observer)
    # All original positional slots through invocation_namespace remain in their original order.
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry,
                          None, None, None, None, False, False, None, None, False,
                          None, None, "positional-version", "positional-workflow", None,
                          None, None, "prefix/")
    result = await scheduler.run(run_id="positional-run")
    assert result.status is RunStatus.COMPLETED, result.error
    assert scheduler.definition_id == "positional-workflow"
    assert observer.seen == [(None, None, "positional-version", graph.definition_hash)]
