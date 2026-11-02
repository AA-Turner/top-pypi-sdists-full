"""A built-in step that declares the ``items`` input kind must take an ``items`` input.

The ``items`` kind requires an ``items`` field; a step whose input has no such field fails every
live run at the kind gate ("'items' is required") while its own unit tests pass
(text.remove_repeated_lines took ``texts`` and declared ``items``, 2026-10-27).
"""

from __future__ import annotations

from matrx_graph import NodeRegistry, register_builtin_nodes


def test_every_builtin_declaring_items_takes_an_items_input() -> None:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    wrong = []
    for spec in registry.all_specs():
        if spec.input_kind != "items" or spec.input_schema is None:
            continue
        if "items" not in spec.input_schema.model_fields:
            wrong.append(spec.type)
    assert wrong == [], f"declare input_kind='items' but take no 'items' input: {wrong}"
