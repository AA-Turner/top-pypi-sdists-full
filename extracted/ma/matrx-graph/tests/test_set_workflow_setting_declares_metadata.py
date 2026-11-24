"""``set_workflow_setting`` sets or clears a workflow's DECLARED metadata (``output_kind`` / ``input_kind``) through
the one home ``set_result`` uses (``io_declaration_columns`` → the save's columns), validated (L-REPLAY, 2026-11-10).

Live need: pick inner b0a04ce1 declared ``output_kind: user_inputs`` with no on-screen result producing it, so
publishing was refused, and ``set_workflow_setting`` refused ``output_kind`` as "not a workflow setting".
Red before: the clear below raised DefinitionPatchError.
"""

from __future__ import annotations

import pytest

from matrx_graph.patch import DefinitionPatch, DefinitionPatchError, apply_patch, io_declaration_columns
from matrx_graph.types import Definition


def _definition() -> Definition:
    return Definition.model_validate({
        "nodes": [{"id": "a", "type": "data", "position": {"x": 0, "y": 0},
                   "data": {"spec_type": "data.transform", "config": {"expression": "1"}}}],
        "edges": [],
    })


def _patch(*ops: dict) -> DefinitionPatch:
    return DefinitionPatch.model_validate({"ops": list(ops)})


def test_clearing_the_output_kind_is_a_column_never_graph() -> None:
    patch = _patch({"op": "set_workflow_setting", "key": "output_kind", "value": None})
    before = _definition()
    after = apply_patch(before, patch)
    assert io_declaration_columns(patch) == {"output_kind": None}
    assert "output_kind" not in (after.metadata or {}), "the definition carries no copy of a declaration column"


def test_setting_both_declarations_last_op_wins() -> None:
    patch = _patch({"op": "set_workflow_setting", "key": "input_kind", "value": "research_topic"},
                   {"op": "set_workflow_setting", "key": "output_kind", "value": "agent_result"},
                   {"op": "set_result", "output_kind": "table:6f1c2a3b-0000-4000-8000-000000000001"})
    apply_patch(_definition(), patch)
    assert io_declaration_columns(patch) == {"input_kind": "research_topic",
                                             "output_kind": "table:6f1c2a3b-0000-4000-8000-000000000001"}


@pytest.mark.parametrize("bad", ["User Inputs", "x" * 200, "kind;drop", "-starts-with-dash"])
def test_a_value_that_is_not_a_kind_slug_is_refused_in_words(bad: str) -> None:
    with pytest.raises(DefinitionPatchError, match="must be a kind slug"):
        apply_patch(_definition(), _patch({"op": "set_workflow_setting", "key": "output_kind", "value": bad}))


def test_an_unknown_key_still_names_every_setting() -> None:
    with pytest.raises(DefinitionPatchError, match="output_kind"):
        apply_patch(_definition(), _patch({"op": "set_workflow_setting", "key": "colour", "value": "red"}))


def test_engine_settings_are_untouched() -> None:
    after = apply_patch(_definition(), _patch({"op": "set_workflow_setting", "key": "durability", "value": "boundaries"}))
    assert after.metadata["durability"] == "boundaries"
