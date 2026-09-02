from matrx_ai.agents.auto_assignment import (
    is_auto_assign_request,
    random_assignment_bindings_from_variables,
)
from matrx_ai.agents.variables import AgentVariable


def test_marker_contract_is_exact() -> None:
    assert is_auto_assign_request({"type": "auto_assign", "strategy": "random"})
    assert not is_auto_assign_request({"type": "auto_assign", "strategy": "round_robin"})
    assert not is_auto_assign_request(
        {"type": "auto_assign", "strategy": "random", "list_id": "forged"}
    )


def test_binding_comes_from_trusted_variable_definition() -> None:
    variables = {
        "tone": AgentVariable(
            name="tone",
            custom_component={
                "type": "select",
                "options": ["warm", "direct"],
                "assignment": {"random": True},
            },
        ),
        "disabled": AgentVariable(
            name="disabled",
            custom_component={
                "type": "select",
                "options": ["one", "two"],
            },
        ),
    }

    assert random_assignment_bindings_from_variables(variables) == {
        "tone": {"source": "static", "options": ["warm", "direct"]}
    }


def test_structured_list_binding_is_authoritative() -> None:
    variables = {
        "item": AgentVariable(
            name="item",
            custom_component={
                "type": "radio",
                "structured_list": {"listId": "list-1", "groupName": "A"},
                "assignment": {"random": True},
            },
        )
    }

    assert random_assignment_bindings_from_variables(variables) == {
        "item": {
            "source": "structured_list",
            "list_id": "list-1",
            "group_name": "A",
        }
    }


def test_agent_variable_preserves_structured_default() -> None:
    marker = {"type": "auto_assign", "strategy": "random"}
    variable = AgentVariable.from_dict({"name": "tone", "defaultValue": marker})
    assert variable.get_value() == marker


def test_agent_variable_keeps_existing_scalar_string_coercion() -> None:
    assert AgentVariable(name="count", default_value=3).get_value() == "3"
    assert AgentVariable(name="enabled", default_value=False).get_value() == "False"


def test_agent_variable_serializes_containers_as_json_not_python_repr() -> None:
    # Dicts/lists must enter prompts as canonical JSON — str() produced
    # Python repr ("{'a': 1}") which no downstream JSON contract can parse.
    assert AgentVariable(name="cfg", value={"a": 1, "b": ["x", "ü"]}).get_value() == (
        '{"a": 1, "b": ["x", "ü"]}'
    )
    assert AgentVariable(name="items", default_value=[1, {"k": None}]).get_value() == (
        '[1, {"k": null}]'
    )
