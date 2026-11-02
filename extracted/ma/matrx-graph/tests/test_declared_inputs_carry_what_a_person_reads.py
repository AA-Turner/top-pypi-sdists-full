"""A declared input reaches the run form with what a PERSON reads, not its machine name.

Review 2026-10-29 (smart-add workflows, gaps A1/A2/B1/B2/B7): every declared variable
compiled to ``label=<snake_case name>`` with no help, placeholder, example, group, order or
Advanced flag, because ``VariableSpec`` could not carry them; a "several values" text input
compiled to plain ``text`` (one box, no list); and there was no way to say "a person must
fill this in, but a caller may leave it empty".
"""

import pytest

from matrx_graph import Definition, compile_graph, register_builtin_nodes
from matrx_graph.types.input_surface import LIST_KIND, LIST_VARIANT, unsatisfied_inputs


@pytest.fixture(scope="module", autouse=True)
def _register() -> None:
    register_builtin_nodes(overwrite=True)


def _surface(variables: list[dict], fields: list[dict] | None = None):
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "in1",
                    "type": "io",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "spec_type": "io.user_input",
                        "config": {"fields": fields or [{"key": "topic"}]},
                    },
                }
            ],
            "edges": [],
            "variables": variables,
        }
    )
    return compile_graph(definition).input_surface


def test_a_variable_carries_label_hints_and_kind_onto_the_surface() -> None:
    surface = _surface(
        [
            {
                "name": "brand_site",
                "label": "Brand website",
                "help": "The site the brand owns.",
                "placeholder": "acme.com",
                "example": "acme.com",
                "advanced": True,
                "group": "Brand",
                "order": 2,
                "detect": ["domain"],
                "primary": False,
                "kind": "brand_basics",
                "default": "",
            }
        ]
    )
    spec = surface["brand_site"]
    assert spec.label == "Brand website"
    assert spec.help == "The site the brand owns."
    assert spec.placeholder == "acme.com"
    assert spec.example == "acme.com"
    assert spec.advanced is True and spec.group == "Brand" and spec.order == 2
    assert spec.detect == ["domain"]
    assert spec.kind == "brand_basics"


def test_an_unlabelled_variable_sends_no_snake_case_label() -> None:
    """No label declared → empty, so every client shows the name in words."""
    spec = _surface([{"name": "person_name", "default": ""}])["person_name"]
    assert spec.label != "person_name"
    assert spec.label == ""


def test_description_still_reads_as_help() -> None:
    spec = _surface([{"name": "n", "description": "How many.", "default": 3}])["n"]
    assert spec.help == "How many."


@pytest.mark.parametrize("field_type", ["text", "long_text"])
def test_a_several_values_text_field_is_a_list_one_per_line(field_type: str) -> None:
    surface = _surface(
        [{"name": "keywords", "multiple": True, "type": field_type, "default": []}],
        fields=[{"key": "handles", "type": field_type, "multiple": True}],
    )
    for name in ("handles", "keywords"):
        assert surface[name].kind == LIST_KIND == "string_list"
        assert surface[name].variant == LIST_VARIANT == "lines"
        assert surface[name].json_schema["type"] == "array"


def test_a_declared_kind_still_wins_over_several_values() -> None:
    surface = _surface([], fields=[{"key": "accounts", "multiple": True, "kind": "typed_account_list"}])
    assert surface["accounts"].kind == "typed_account_list"


def test_required_in_form_is_carried_and_the_engine_ignores_it() -> None:
    surface = _surface(
        [{"name": "subject", "default": "", "required_in_form": True}],
        fields=[{"key": "topic", "required_in_form": True}],
    )
    assert surface["subject"].required_in_form is True
    assert surface["topic"].required_in_form is True
    # A caller passing nothing is NOT parked: the gate is the form's, never the engine's.
    assert unsatisfied_inputs(surface, {"subject": "", "topic": ""}) == []
