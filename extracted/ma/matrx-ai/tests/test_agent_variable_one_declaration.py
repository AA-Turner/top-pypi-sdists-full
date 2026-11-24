"""AgentVariable holds the ONE input declaration: it reads through the one upgrade and keeps nothing a hand copy would."""

import pytest

from matrx_ai.agents.variables import AgentVariable

NOTE = "11111111-1111-4111-8111-111111111111"
BOT = "22222222-2222-4222-8222-222222222222"


def test_a_legacy_element_reads_through_the_one_upgrade():
    var = AgentVariable.from_dict(
        {
            "name": "tone",
            "default_value": "warm",
            "title": "Tone",
            "description": "How it sounds",
            "componentType": "textarea",
        }
    )
    assert var.name == "tone"
    assert var.default_value == "warm"
    assert var.declaration.get("label") == "Tone"
    assert var.custom_component is not None and var.custom_component.get("type") == "textarea"


def test_an_unknown_component_type_is_kept_never_dropped():
    defs = [{"name": "x", "customComponent": {"type": "from-the-future"}}]
    kept = AgentVariable.from_list(defs)
    assert list(kept) == ["x"]
    assert kept["x"].custom_component["type"] == "from-the-future"


def test_a_record_variable_validates_and_renders_its_relations():
    var = AgentVariable.from_dict(
        {
            "name": "refs",
            "customComponent": {"type": "record", "tokens": ["note", "agent"], "multiple": True},
        }
    )
    assert var.definition() is not None
    var.value = [
        {"__kind": "relation", "token": "note", "_record_id": NOTE, "label": "Plan"},
        {"__kind": "relation", "token": "agent", "_record_id": BOT, "label": "Bot"},
    ]
    assert var.get_value() == f"Plan (note {NOTE})\nBot (agent {BOT})"


def test_a_single_relation_without_a_label_renders_token_and_id():
    var = AgentVariable.from_dict(
        {"name": "ref", "customComponent": {"type": "record", "tokens": ["note"]}}
    )
    var.value = {"__kind": "relation", "token": "note", "_record_id": NOTE}
    assert var.get_value() == f"note {NOTE}"


def test_declare_refuses_a_key_the_declaration_does_not_have():
    with pytest.raises(Exception):
        AgentVariable.declare("x", bogusKey=1)
