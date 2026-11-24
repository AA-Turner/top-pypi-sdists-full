"""A declared workflow variable reaches the run form as its TYPE, never all as text.

Every variable used to compile to ``kind="text"`` / ``{"type": "string"}``, so the run
form drew a number as a text box ("2") and a yes/no as a text box ("true") — live on
"Plan research keywords", 2026-10-27. A variable now declares a type in the same
vocabulary an io.user_input field uses, or its default says it.
"""

import pytest

from matrx_graph import Definition, compile_graph, register_builtin_nodes
from pydantic import ValidationError
from matrx_graph.types.input_surface import declared_input, input_options
from matrx_graph.types.variables import variable_json_schema


def _var(**old):
    """One variable as an OLD-shape stored dict, read through the converter (never a hand copy)."""
    return declared_input(old)


@pytest.fixture(scope="module", autouse=True)
def _register() -> None:
    register_builtin_nodes(overwrite=True)


def test_type_is_read_from_the_default() -> None:
    assert variable_json_schema(_var(name="n", default=3))["type"] == "integer"
    assert variable_json_schema(_var(name="r", default=0.5))["type"] == "number"
    assert variable_json_schema(_var(name="b", default=False))["type"] == "boolean"
    assert variable_json_schema(_var(name="s", default=""))["type"] == "string"
    assert variable_json_schema(_var(name="o", default={"a": 1}))["type"] == "object"
    assert variable_json_schema(_var(name="u"))["type"] == "string"


def test_the_title_a_person_reads_is_the_label_never_the_name() -> None:
    """Live 2026-10-29: a labelled variable served ``json_schema.title`` = its snake_case name."""
    labelled = variable_json_schema(_var(name="search_set", label="Custom searches", default=[]))
    assert labelled["title"] == "Custom searches"
    assert variable_json_schema(_var(name="topic", default=""))["title"] == "topic"


def test_a_declared_type_wins_and_speaks_the_field_vocabulary() -> None:
    choice = variable_json_schema(_var(name="tone", type="choice", options=["warm", "dry"]))
    assert choice["enum"] == ["warm", "dry"]
    assert variable_json_schema(_var(name="notes", type="long_text"))["ui:widget"] == "textarea"
    assert variable_json_schema(_var(name="count", type="number"))["type"] == "number"


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
    assert input_options(surface["tone"].declaration) == ["warm", "dry"]


def test_a_reference_input_offers_a_person_a_door() -> None:
    """Every workflow takes a person's input too (generic-only VISION, 2026-10-27): an id input
    that names its record type renders a picker, and a file input stores files (ids)."""
    picked = variable_json_schema(_var(name="brand_id", picks="brand", default=""))
    assert picked["ui:widget"] == "record_picker"
    assert picked["ui:entity_type"] == "brand"
    assert picked["type"] == "string"
    photos = variable_json_schema(
        _var(name="photos", type="file", multiple=True, accept="image/*", default=[])
    )
    assert photos["ui:widget"] == "file"
    assert photos["type"] == "array" and photos["items"] == {"type": "string"}
    assert photos["ui:multiple"] is True and photos["ui:accept"] == "image/*"
    one = variable_json_schema(_var(name="doc", type="file"))
    assert one["type"] == "string" and "ui:multiple" not in one
    with pytest.raises(ValueError):
        _var(name="x", picks="Not A Token")


def test_a_reference_input_may_accept_several_record_types() -> None:
    """An input that takes a note OR a file offers one picker over both, and tells the workflow
    which type was picked: the run form writes the picked record's type into ``picks_type_into``."""
    several = variable_json_schema(_var(name="source_id", picks=["note", "file"], default=None))
    assert several["ui:widget"] == "record_picker"
    assert several["ui:entity_type"] == ["note", "file"]
    one = variable_json_schema(_var(name="brand_id", picks=["brand"], default=""))
    assert one["ui:entity_type"] == "brand" and "ui:entity_type_field" not in one
    with pytest.raises(ValidationError):
        _var(name="x_id", picks=["Not A Token"])


def test_picked_type_goes_to_the_named_input() -> None:
    several = variable_json_schema(
        _var(name="source_id", picks=["note", "file"], picks_type_into="source_kind", default=None)
    )
    assert several["ui:entity_type_field"] == "source_kind"
