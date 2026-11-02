"""Live mid-run node injection (C-25 / D-35) — engine-level proof.

The aidream host orchestrates injection (pause → additive patch → resume);
what the ENGINE must guarantee is proven here with the real Scheduler and an
in-memory checkpointer: a run parked mid-flight can resume against a
recompiled graph that contains NEW nodes/edges, and the injected node
actually EXECUTES with its output recorded — including after an
intermediate park between patch and completion (the crash-recovery shape).
"""

from __future__ import annotations

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.patch import (
    AddEdgeOp,
    AddNodeOp,
    DefinitionPatch,
    apply_patch,
)
from matrx_graph.types.definition import EdgeDef, NodeDef

from tests._fixtures import FakeEmitter, make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _chain_definition() -> Definition:
    """a -> b -> c, all data.transform with constant expressions."""
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": nid,
                    "type": "data.transform",
                    "position": {"x": i * 200, "y": 0},
                    "data": {"config": {"expression": f"'{nid.upper()}'"}},
                }
                for i, nid in enumerate(["a", "b", "c"])
            ],
            "edges": [
                {"id": "e-ab", "source": "a", "target": "b"},
                {"id": "e-bc", "source": "b", "target": "c"},
            ],
        }
    )


def _injection_patch() -> DefinitionPatch:
    """Add node ``d`` fed by a new edge b -> d (additive only)."""
    return DefinitionPatch(
        summary="inject d after b",
        ops=[
            AddNodeOp(
                node=NodeDef.model_validate(
                    {
                        "id": "d",
                        "type": "data.transform",
                        "position": {"x": 400, "y": 200},
                        "data": {"config": {"expression": "'INJECTED'"}},
                    }
                )
            ),
            AddEdgeOp(edge=EdgeDef.model_validate({"id": "e-bd", "source": "b", "target": "d"})),
        ],
    )


def _pause_after(n_polls: int):
    calls = {"n": 0}

    async def check() -> bool:
        calls["n"] += 1
        return calls["n"] > n_polls

    return check


async def test_injected_node_executes_after_mid_run_pause():
    """Park after one super-step (only ``a`` ran), patch the definition with
    a NEW node ``d`` + edge b->d, resume the SAME run against the recompiled
    graph — the run completes and ``d`` executed with its output recorded."""
    registry = _registry()
    definition = _chain_definition()
    graph = compile_graph(definition, registry=registry)
    checkpointer = MemoryCheckpointer()
    emitter = FakeEmitter()

    scheduler = Scheduler(
        graph,
        checkpointer,
        make_app_context(emitter),
        registry=registry,
        pause_check=_pause_after(1),
    )
    parked = await scheduler.run(run_id="inject-1")
    assert parked.status is RunStatus.PAUSED
    assert parked.steps_executed == 1  # only ``a`` ran

    cp = await checkpointer.latest_checkpoint("inject-1")
    assert cp is not None
    assert {ni.node_id for ni in cp.next_invocations} == {"b"}

    patched = apply_patch(definition, _injection_patch())
    patched_graph = compile_graph(patched, registry=registry)
    assert patched_graph.definition_hash != graph.definition_hash

    resumed = await Scheduler(
        patched_graph,
        checkpointer,
        make_app_context(FakeEmitter()),
        registry=registry,
    ).resume(run_id="inject-1", checkpoint_id=cp.checkpoint_id)

    assert resumed.status is RunStatus.COMPLETED
    assert resumed.last_outputs.get("d", {}).get("result") == "INJECTED"
    assert resumed.last_outputs.get("c", {}).get("result") == "C"


async def test_injection_survives_park_between_patch_and_completion():
    """Crash-recoverability shape: the patch lands, the first resume attempt
    parks again immediately (process death / second pause), and a LATER
    resume from the newest checkpoint still executes the injected node."""
    registry = _registry()
    definition = _chain_definition()
    checkpointer = MemoryCheckpointer()

    parked = await Scheduler(
        compile_graph(definition, registry=registry),
        checkpointer,
        make_app_context(FakeEmitter()),
        registry=registry,
        pause_check=_pause_after(1),
    ).run(run_id="inject-2")
    assert parked.status is RunStatus.PAUSED

    patched = apply_patch(definition, _injection_patch())
    patched_graph = compile_graph(patched, registry=registry)

    cp1 = await checkpointer.latest_checkpoint("inject-2")
    assert cp1 is not None

    # First resume after the patch parks again before doing anything —
    # the injected work must not be lost with it.
    interrupted_resume = await Scheduler(
        patched_graph,
        checkpointer,
        make_app_context(FakeEmitter()),
        registry=registry,
        pause_check=_pause_after(0),
    ).resume(run_id="inject-2", checkpoint_id=cp1.checkpoint_id)
    assert interrupted_resume.status is RunStatus.PAUSED

    cp2 = await checkpointer.latest_checkpoint("inject-2")
    assert cp2 is not None

    final = await Scheduler(
        patched_graph,
        checkpointer,
        make_app_context(FakeEmitter()),
        registry=registry,
    ).resume(run_id="inject-2", checkpoint_id=cp2.checkpoint_id)
    assert final.status is RunStatus.COMPLETED
    assert final.last_outputs.get("d", {}).get("result") == "INJECTED"
