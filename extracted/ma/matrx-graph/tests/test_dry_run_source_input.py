"""ENGINE_SPEC §8 — dry-run must match runtime's FATAL posture for a source
node's own input contract.

At runtime a source (entry) node validates its ACTUAL provided values against
its dynamic output schema BEFORE it runs (``scheduler.py`` is_source gate) and
raises ``NodeInputValidationError`` → ERRORED on any violation. dry_run used to
downgrade the same violation to a mere warning and still report state=ready /
ok=True — greenlighting a graph that deterministically ERRORS. This pack pins
the corrected posture: a bad enum/type on the provided input marks the source
node ``blocked`` and drops ``ok`` to False; a valid value stays ready/ok.
"""

from __future__ import annotations

from typing import Any

from matrx_graph import (
    Definition,
    NodeRegistry,
    compile_graph,
    dry_run,
    register_builtin_nodes,
)


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


def _color_form(node_id: str = "ask") -> dict[str, Any]:
    """An io.user_input entry node with a required enum field color=[red,blue]."""
    return {
        "id": node_id,
        "type": "io.user_input",
        "position": {"x": 0, "y": 0},
        "data": {
            "config": {
                "title": "Pick a color",
                "fields": [
                    {
                        "key": "color",
                        "label": "Color",
                        "type": "choice",
                        "options": ["red", "blue"],
                        "required": True,
                    }
                ],
            }
        },
    }


def _graph(registry: NodeRegistry):
    return compile_graph(
        Definition.model_validate({"nodes": [_color_form("ask")], "edges": []}),
        registry=registry,
    )


def test_source_node_bad_enum_is_blocked_and_not_ok() -> None:
    registry = _registry()
    graph = _graph(registry)

    report = dry_run(
        graph,
        node_inputs={"ask": {"color": "green"}},  # not in the enum
        registry=registry,
    )

    # Runtime would ERROR on this exact input — dry_run must NOT greenlight it.
    assert report.ok is False
    assert report.nodes["ask"].state == "blocked"
    # The violation surfaces as an error (not a mere warning) mentioning the field.
    assert any("color" in e for e in report.errors)


def test_source_node_valid_enum_is_ready_and_ok() -> None:
    registry = _registry()
    graph = _graph(registry)

    report = dry_run(
        graph,
        node_inputs={"ask": {"color": "red"}},  # valid
        registry=registry,
    )

    assert report.ok is True
    assert report.nodes["ask"].state == "ready"
    assert not any("color" in e for e in report.errors)


def test_unregistered_nodes_mark_registry_incomplete() -> None:
    # A bare registry (no builtins) can't validate anything — the report must
    # advertise that so a caller can't trust a hollow green.
    empty = NodeRegistry()
    graph = compile_graph(
        Definition.model_validate({"nodes": [_color_form("ask")], "edges": []}),
        registry=_registry(),  # compile needs the real spec...
    )
    report = dry_run(graph, node_inputs={"ask": {"color": "red"}}, registry=empty)

    assert report.registry_complete is False
