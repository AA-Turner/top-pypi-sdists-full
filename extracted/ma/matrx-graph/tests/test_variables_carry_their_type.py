"""A declared workflow variable reaches the run form as its TYPE, never all as text.

Every variable used to compile to ``kind="text"`` / ``{"type": "string"}``, so the run
form drew a number as a text box ("2") and a yes/no as a text box ("true") — live on
"Plan research keywords", 2026-10-27. A variable now declares a type in the same
vocabulary an io.user_input field uses, or its default says it.
"""

import pytest

from matrx_graph import Definition, compile_graph, register_builtin_nodes
from pydantic import ValidationError
from matrx_graph.types.variables import VariableSpec, variable_json_schema


@pytest.fixture(scope="module", autouse=True)
def _register() -> None:
    register_builtin_nodes(overwrite=True)


def test_type_is_read_from_the_default() -> None:
    assert variable_json_schema(VariableSpec(name="n", default=3))["type"] == "integer"
    assert variable_json_schema(VariableSpec(name="r", default=0.5))["type"] == "number"
    assert variable_json_schema(VariableSpec(name="b", default=False))["type"] == "boolean"
    assert variable_json_schema(VariableSpec(name="s", default=""))["type"] == "string"
    assert variable_json_schema(VariableSpec(name="o", default={"a": 1}))["type"] == "object"
    assert variable_json_schema(VariableSpec(name="u"))["type"] == "string"


def test_the_title_a_person_reads_is_the_label_never_the_name() -> None:
    """Live 2026-10-29: a labelled variable served ``json_schema.title`` = its snake_case name."""
    labelled = variable_json_schema(VariableSpec(name="search_set", label="Custom searches", default=[]))
    assert labelled["title"] == "Custom searches"
    assert variable_json_schema(VariableSpec(name="topic", default=""))["title"] == "topic"


def test_a_declared_type_wins_and_speaks_the_field_vocabulary() -> None:
    choice = variable_json_schema(VariableSpec(name="tone", type="choice", options=["warm", "dry"]))
    assert choice["enum"] == ["warm", "dry"]
    assert variable_json_schema(VariableSpec(name="notes", type="long_text"))["ui:widget"] == "textarea"
    assert variable_json_schema(VariableSpec(name="count", type="number"))["type"] == "number"


def test_the_compiled_surface_carries_the_type() -> None:
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "in1",
                    "type": "io",
                    "position": {"x": 0, "y": 0},
                    "data": {"spec_type": "io.user_input", "config": {"fields": [{"key": "topic"}]}},
                }
            ],
            "edges": [],
            "variables": [
                {"name": "max_keywords", "default": 3},
                {"name": "review", "default": False},
                {"name": "tone", "type": "choice", "options": ["warm", "dry"], "default": "warm"},
            ],
        }
    )
    surface = compile_graph(definition).input_surface
    assert surface["max_keywords"].kind == "number"
    assert surface["max_keywords"].json_schema["type"] == "integer"
    assert surface["review"].kind == "boolean"
    assert surface["tone"].variant == "dropdown"
    assert surface["tone"].options == ["warm", "dry"]


def test_a_reference_input_offers_a_person_a_door() -> None:
    """Every workflow takes a person's input too (generic-only VISION, 2026-10-27): an id input
    that names its record type renders a picker, and a file input stores files (ids)."""
    picked = variable_json_schema(VariableSpec(name="brand_id", picks="web_brand", default=""))
    assert picked["ui:widget"] == "record_picker"
    assert picked["ui:entity_type"] == "web_brand"
    assert picked["type"] == "string"
    photos = variable_json_schema(
        VariableSpec(name="photos", type="file", multiple=True, accept="image/*", default=[])
    )
    assert photos["ui:widget"] == "file"
    assert photos["type"] == "array" and photos["items"] == {"type": "string"}
    assert photos["ui:multiple"] is True and photos["ui:accept"] == "image/*"
    one = variable_json_schema(VariableSpec(name="doc", type="file"))
    assert one["type"] == "string" and "ui:multiple" not in one
    with pytest.raises(ValueError):
        VariableSpec(name="x", picks="Not A Token")


def test_a_reference_input_may_accept_several_record_types() -> None:
    """An input that takes a note OR a file offers one picker over both, and tells the workflow
    which type was picked: the run form writes the picked record's type into ``picks_type_into``."""
    several = variable_json_schema(
        VariableSpec(name="source_id", picks=["note", "file"], picks_type_into="source_kind", default=None)
    )
    assert several["ui:widget"] == "record_picker"
    assert several["ui:entity_type"] == ["note", "file"]
    assert several["ui:entity_type_field"] == "source_kind"
    one = variable_json_schema(VariableSpec(name="brand_id", picks=["web_brand"], default=""))
    assert one["ui:entity_type"] == "web_brand" and "ui:entity_type_field" not in one
    with pytest.raises(ValidationError):
        VariableSpec(name="x_id", picks=["Not A Token"])
