"""Every dispatcher is seen by the standing-rule lineage (lane 11 round 6, B1).

A step can launch another WITHOUT an edge: a static dispatcher names its target in config
(``target_node_id``), and a step declared ``launches_nodes`` may ``ctx.send`` anywhere. The
lineage that decides whether a write is the owner's standing rule reads both off the SPEC
(``launches_statically`` / ``launches_anything``), never a list of types. This census fails
when the engine's own dispatcher list (``validation.DISPATCHER_NODE_TYPES``, what the scheduler
routes launches for) and what lineage derives from the specs disagree — a new dispatcher the
lineage would not see.
"""

from __future__ import annotations

from matrx_graph import NodeRegistry, register_builtin_nodes
from matrx_graph.db.trigger_proof import launches_anything, launches_statically
from matrx_graph.validation import DISPATCHER_NODE_TYPES


def test_the_engines_dispatchers_are_the_ones_lineage_derives() -> None:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    derived = {t for t in registry._executors if launches_statically(registry.get(t).spec)}
    assert derived == set(DISPATCHER_NODE_TYPES), (
        f"lineage sees {sorted(derived)}, the scheduler dispatches for "
        f"{sorted(DISPATCHER_NODE_TYPES)}"
    )


def test_a_free_launcher_is_seen_too() -> None:
    from types import SimpleNamespace

    assert launches_anything(SimpleNamespace(launches_nodes=True))
    assert not launches_anything(SimpleNamespace(launches_nodes=False))
