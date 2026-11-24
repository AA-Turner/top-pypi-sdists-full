"""A workflow that DECLARES what it answers (or takes) and whose steps do not compile is refused at publish, naming
why — never published unchecked with only a log line (L-SPEED 6d, 2026-11-10: b0a04ce1 v26 went out declaring
'user_inputs' with no step producing it; a later publish of the same shape was refused). A draft that declares
nothing stays publishable half-built. Red before: the check returned None and the publish went through."""

from __future__ import annotations

import pytest

from matrx_graph.db.definition_store import _validate_io_declaration_for_publish
from matrx_graph.errors import OutputContractError


def _row(**declared: str | None) -> dict:
    return {
        "nodes": [{"id": "a", "type": "no.such_step_type", "position": {"x": 0, "y": 0}, "data": {}}],
        "edges": [], "viewport": None, "channels": [], "strict_channels": False, "entry_nodes": ["a"],
        "metadata": {}, "variables": [], "output_kind": declared.get("output_kind"),
        "input_kind": declared.get("input_kind"),
    }


def test_a_declared_answer_on_steps_that_do_not_compile_is_refused_naming_why():
    with pytest.raises(OutputContractError, match="answers with 'user_inputs'.*do not compile"):
        _validate_io_declaration_for_publish(_row(output_kind="user_inputs"), "wf-1")


def test_a_half_built_draft_that_declares_nothing_still_publishes():
    assert _validate_io_declaration_for_publish(_row(), "wf-1") is None
