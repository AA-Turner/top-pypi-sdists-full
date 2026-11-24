"""A spec that declares ``executes = False`` is an information type, and its name is in the ``info.*`` family.

The database views and the Studio decide "is this node information" by the ``info.`` name prefix because
they cannot read the registry; the engine decides by the spec. This test holds the two equal, so the
prefix rule is exact and the engine needs no prefix guess of its own (CONTRACTS §2.3, REGISTER C1).
"""

from __future__ import annotations

from matrx_graph import NodeRegistry, register_builtin_nodes
from matrx_graph.information import INFO_PREFIX
from matrx_graph.types.primitives import NodeCategory


def disagreements(registry: NodeRegistry) -> list[str]:
    """Every spec whose "never runs" and "named info.*" answers differ."""
    out: list[str] = []
    for spec in registry.all_specs():
        named_info = spec.node_type.startswith(INFO_PREFIX)
        if (not spec.executes) != named_info:
            out.append(f"{spec.node_type}: executes={spec.executes} but {'is' if named_info else 'is not'} in the info.* family")
        if (not spec.executes) and spec.category is not NodeCategory.INFO:
            out.append(f"{spec.node_type}: never runs but its category is {spec.category}, not info")
    return out


def _registry() -> NodeRegistry:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    return registry


def test_every_spec_that_never_runs_is_an_info_type_and_every_info_type_never_runs() -> None:
    registry = _registry()
    assert any(not s.executes for s in registry.all_specs()), "no information spec registered: the test would pass on nothing"
    assert disagreements(registry) == []


def test_the_check_can_fail() -> None:
    registry = _registry()
    note = registry.get("info.note")
    # a non-running spec outside the family, and a running spec inside it
    outside = note.spec.model_copy(update={"node_type": "ref.card"})
    inside = note.spec.model_copy(update={"node_type": "info.runs", "executes": True})

    class _Reg:
        def all_specs(self) -> list:
            return [outside, inside]

    found = disagreements(_Reg())  # type: ignore[arg-type]
    assert len(found) >= 2
    assert any("ref.card" in f for f in found) and any("info.runs" in f for f in found)
