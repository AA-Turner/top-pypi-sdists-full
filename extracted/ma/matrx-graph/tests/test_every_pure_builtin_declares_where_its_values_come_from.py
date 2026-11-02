"""Every PURE built-in step is listed in ``BUILTIN_VALUES_ARE``.

``values_are`` is deny-by-default: a built-in missing from the table reads as ``'ai'`` (its
output could be an agent's words), so a step that only computes from its inputs and settings —
``data.rules`` was missed for a day — is treated as untrusted lineage everywhere downstream.
A PURE step computes its output from its inputs and config alone, which is exactly what
``deterministic`` means, so each one must be listed. The only PURE exception is ruled in the
table's own comment: ``io.user_input`` (its bound values live on client-writable rows).
"""

from __future__ import annotations

from matrx_graph import NodeRegistry, register_builtin_nodes
from matrx_graph.nodes import BUILTIN_VALUES_ARE
from matrx_graph.types.primitives import ActionTier

#: PURE built-ins whose values are deliberately NOT deterministic (see BUILTIN_VALUES_ARE's comment).
RULED_EXCEPTIONS = {"io.user_input"}


def test_every_pure_builtin_is_listed() -> None:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    unlisted = sorted(
        spec.node_type
        for spec in registry.all_specs()
        if spec.determinism == ActionTier.PURE
        and spec.node_type not in BUILTIN_VALUES_ARE
        and spec.node_type not in RULED_EXCEPTIONS
    )
    assert unlisted == [], (
        f"PURE built-ins missing from BUILTIN_VALUES_ARE (they read as 'ai'): {unlisted}. "
        "Add each to the deterministic list in matrx_graph/nodes/__init__.py."
    )


def test_data_rules_reads_as_deterministic() -> None:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    assert registry.get("data.rules").spec.values_are == "deterministic"
