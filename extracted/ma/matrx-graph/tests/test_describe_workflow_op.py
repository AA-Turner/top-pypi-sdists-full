"""A workflow's own name and description change through the patch door (lane U4 item 9, 2026-11-16).

The research workflows' descriptions named internals (max_keywords, research.journey.pick) and there was no
op to rewrite them: name and description are the workflow's COLUMNS, so ``describe_workflow`` leaves the graph
as it is and hands them to the save through ``io_declaration_columns`` — the one home ``set_result`` uses."""

from __future__ import annotations

import pytest

from matrx_graph import Definition
from matrx_graph.patch import DefinitionPatch, DefinitionPatchError, apply_patch, io_declaration_columns


def _defn() -> Definition:
    return Definition.model_validate({"nodes": [], "edges": []})


def test_describe_workflow_hands_name_and_description_to_the_save() -> None:
    patch = DefinitionPatch(ops=[{"op": "describe_workflow", "name": " Read the sources ", "description": "Reads each source."}])
    assert apply_patch(_defn(), patch).model_dump() == _defn().model_dump()
    assert io_declaration_columns(patch) == {"name": "Read the sources", "description": "Reads each source."}


def test_an_omitted_field_is_untouched_and_an_empty_description_clears() -> None:
    patch = DefinitionPatch(ops=[{"op": "describe_workflow", "description": ""}])
    apply_patch(_defn(), patch)
    assert io_declaration_columns(patch) == {"description": None}


@pytest.mark.parametrize("op", [{"op": "describe_workflow", "name": "  "}, {"op": "describe_workflow"}])
def test_an_empty_name_or_nothing_to_say_is_refused(op: dict[str, object]) -> None:
    with pytest.raises(DefinitionPatchError):
        apply_patch(_defn(), DefinitionPatch(ops=[op]))
