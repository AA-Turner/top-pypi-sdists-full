"""A PUBLISHED workflow's media is born public — the run declares it, once.

Why this exists. Media persisted as `personal` has exactly one URL: a signed
grant that expires. A node output is written to `workflow.node_outcome` and read
back on resume, by later nodes, and by any past-runs UI days later — so an
expiring URL that reaches it is a permanent 403 with nothing to re-mint from.
On 2026-08-20, 51 outcome rows held exactly that, produced by podcast W7: it
renders episode cover art through `ai.agent.start`, and a published WORKFLOW had
no way to say what a published Python pipeline says with `public_media_scope()`.

`Definition.public_media` is that way. The scheduler enters the scope around
`_drive`, which BOTH `run()` and `resume()` funnel through, so one declaration
covers the whole graph — every node, every resume segment, and every task those
nodes create (ContextVar semantics).

If a test here fails, do NOT relax it. The failure mode it prevents is silent:
the run succeeds, the images render fine for an hour, and the record dies later.
"""

from __future__ import annotations

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.types.definition import NodeDef, Position
from matrx_utils.ctx import public_media_scope_active

from tests._fixtures import FakeEmitter, make_app_context

# What every node in the run observed. The node body runs deep inside the
# scheduler, so this is the only honest way to prove the scope reached it —
# asserting on the flag from the test body would prove nothing.
OBSERVED: list[bool] = []


def _definition(*, public_media: bool) -> Definition:
    """One transform node that records whether it ran inside the scope."""
    return Definition(
        version="1",
        public_media=public_media,
        nodes=[
            NodeDef(
                id="probe",
                type="data.transform",
                data={"config": {"expression": "{'ok': True}"}},
                position=Position(x=0, y=0),
            )
        ],
        edges=[],
        entry_nodes=["probe"],
    )


async def _run(definition: Definition, run_id: str):
    registry = NodeRegistry()
    register_builtin_nodes(registry)

    # Wrap the real executor so the probe reports the ambient scope from
    # inside the scheduler's call stack.
    inner = registry.get("data.transform")

    class _ProbeExecutor(type(inner)):  # type: ignore[misc]
        async def execute(self, ctx, inputs, config):  # type: ignore[override]
            OBSERVED.append(public_media_scope_active())
            return await inner.execute(ctx, inputs, config)

    registry.register(_ProbeExecutor(), overwrite=True)
    graph = compile_graph(definition, registry=registry)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )
    return await scheduler.run(run_id=run_id)


async def test_a_published_workflow_runs_its_nodes_inside_the_scope():
    OBSERVED.clear()
    await _run(_definition(public_media=True), "public-media-on")
    assert OBSERVED == [True], (
        "a node in a public_media workflow must persist its media PUBLIC — "
        "otherwise the only URL it can produce expires, and the node_outcome "
        "row recording it dies with the signature."
    )
    assert not public_media_scope_active(), "the scope must not leak past the run"


async def test_a_private_workflow_is_untouched():
    OBSERVED.clear()
    await _run(_definition(public_media=False), "public-media-off")
    assert OBSERVED == [False], (
        "declaring nothing must stay PRIVATE — a personal image must never "
        "become world-readable because a workflow happened to touch it."
    )


def test_the_declaration_defaults_to_private():
    """Fail closed: publishing is opt-in, never inherited by accident."""
    assert Definition(nodes=[], edges=[]).public_media is False


def test_the_declaration_survives_compilation():
    """A Definition field nothing carries into CompiledGraph is a dead field —
    the scheduler only ever sees the compiled form."""
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    assert compile_graph(_definition(public_media=True), registry=registry).public_media is True
    assert compile_graph(_definition(public_media=False), registry=registry).public_media is False
