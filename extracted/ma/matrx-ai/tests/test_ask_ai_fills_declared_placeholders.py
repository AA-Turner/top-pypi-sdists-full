"""Ask AI (ai.llm.chat) fills {{name}} from a connected step's values and the save gate accepts it (item 75413f42)."""

from __future__ import annotations

from matrx_graph.nodes._template import render_declared_placeholders
from matrx_graph.validation import validate_definition

import matrx_ai.graph_nodes.llm_action  # noqa: F401  (registers ai.llm.chat)


def test_declared_name_is_filled_others_left_as_written() -> None:
    text = "Summarize {{Topic}} in two sentences. Keep {{unknown}} and {{!Topic}} and {{! note }}."
    out = render_declared_placeholders(text, {"Topic": "bees"})
    assert out == "Summarize bees in two sentences. Keep {{unknown}} and {{Topic}} and {{! note }}."


def test_declared_name_without_value_is_empty() -> None:
    assert render_declared_placeholders("a{{Topic}}b", {"Topic": None}) == "ab"


def _issues(field: str) -> list[str]:
    definition = {
        "nodes": [
            {
                "id": "n1",
                "type": "ai.llm.chat",
                "position": {"x": 0, "y": 0},
                "data": {"inputs": {"model": "m", field: "Summarize {{Topic}}"}},
            }
        ],
        "edges": [],
    }
    return [i.path for i in validate_definition(definition).issues if getattr(i, "code", None) == "unrendered_placeholder"]


def test_prompt_and_system_instruction_pass_the_save_gate() -> None:
    assert _issues("prompt") == []
    assert _issues("system_instruction") == []


def test_other_fields_still_refuse_a_placeholder() -> None:
    assert _issues("metadata") != [] or _issues("offering_id") != []
