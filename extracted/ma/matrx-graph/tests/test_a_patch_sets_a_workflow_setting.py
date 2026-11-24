"""The patch door sets a workflow-wide engine setting (``set_workflow_setting``).

2026-11-09 (L-SPEED 6b): lane 6a's ``metadata.durability: "boundaries"`` had no patch op, so an agent could set it
only by writing back a whole fetched draft. The op sets one known setting, refuses an unknown key or value naming
what is allowed, and clears it with ``None``; the compiled graph reads what it set.
"""

from __future__ import annotations

import pytest

from matrx_graph import Definition, compile_graph, register_builtin_nodes
from matrx_graph.patch import DefinitionPatch, DefinitionPatchError, apply_patch


def _definition(**metadata: object) -> Definition:
    return Definition.model_validate({
        "nodes": [{"id": "a", "type": "data", "position": {"x": 0, "y": 0},
                   "data": {"spec_type": "data.transform", "config": {"expression": "1"}}}],
        "edges": [],
        "metadata": {"annotations": [{"id": "n1", "text": "keep me", "position": {"x": 0, "y": 0}}], **metadata},
    })


def _apply(definition: Definition, *ops: dict) -> Definition:
    return apply_patch(definition, DefinitionPatch.model_validate({"ops": list(ops)}))


def test_it_sets_durability_and_the_compiled_graph_reads_it() -> None:
    register_builtin_nodes(overwrite=True)  # the default registry may already hold them from an earlier test
    out = _apply(_definition(), {"op": "set_workflow_setting", "key": "durability", "value": "boundaries"})
    assert out.metadata["durability"] == "boundaries"
    assert out.metadata["annotations"][0]["text"] == "keep me"  # the rest of the metadata untouched
    assert compile_graph(out).durability == "boundaries"


def test_none_puts_the_default_back() -> None:
    out = _apply(_definition(durability="boundaries"), {"op": "set_workflow_setting", "key": "durability", "value": None})
    assert "durability" not in out.metadata


@pytest.mark.parametrize(
    ("op", "says"),
    [
        ({"op": "set_workflow_setting", "key": "durability", "value": "sometimes"}, "every_step"),
        ({"op": "set_workflow_setting", "key": "annotations", "value": "x"}, "not a workflow setting"),
    ],
)
def test_an_unknown_value_or_key_is_refused_naming_what_is_allowed(op: dict, says: str) -> None:
    with pytest.raises(DefinitionPatchError) as refused:
        _apply(_definition(), op)
    assert says in str(refused.value)


def test_a_workflow_that_runs_as_a_step_needs_no_screen_step() -> None:
    from matrx_graph.visible_io import visible_io_findings

    plain = _definition()
    assert "no_output_step" in {f.code for f in visible_io_findings(plain)}
    child = _apply(plain, {"op": "set_workflow_setting", "key": "runs_as", "value": "step"})
    assert child.metadata["runs_as"] == "step"
    codes = {f.code for f in visible_io_findings(child)}
    assert "no_output_step" not in codes and "no_input_step" in codes  # only the screen-step rule is lifted
