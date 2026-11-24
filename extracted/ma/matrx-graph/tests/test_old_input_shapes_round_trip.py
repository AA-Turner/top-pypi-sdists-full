"""Every OLD stored input shape reads through the converter and compiles to what the old engine gave.

The golden file is the output of the OLD engine (its three per-door copies of the input shape) for the stored dicts below — placeholder, sourcing, value kind, picks and
``multiple`` (record), variant, primary, advanced, group, order, choice_style, inline, example,
option_labels, detect, required_in_form, multi-choice, files, lists, bindings. The new engine reads
them with ``declared_input`` -> ``InputSpec`` + the reader API; the only differences are the named
``DEVIATIONS`` below, each a consequence of the converter's one mapping (never a silent drift).
"""

import json
from pathlib import Path

import pytest

from matrx_graph import Definition, compile_graph, register_builtin_nodes
from matrx_graph.input_declaration import VariableDefinition
from matrx_graph.types.input_surface import (
    declared_input,
    input_choice_style,
    input_hint,
    input_label,
    input_multiple,
    input_option_labels,
    input_options,
    input_picks,
    input_type,
)

GOLDEN = json.loads((Path(__file__).parent / "fixtures" / "old_input_shapes_golden.json").read_text())

# (input name, section, key) -> the new value; the old value is in the golden file.
DEVIATIONS: dict[tuple[str, str, str], object] = {
    # The converter derives a component from the option count: pill-toggle (chips) up to six.
    ("f_choice_auto", "hints", "choice_style"): "chips",
    ("v_choice", "hints", "choice_style"): "chips",
    ("v_choice_opts_only", "hints", "choice_style"): "chips",
    # A dict / list default is stored as valueKind "json", so it compiles to the json kind.
    ("v_arr", "top", "kind"): "json",
    ("v_obj", "top", "kind"): "json",
    # A record input's "" default is stored as null (see the pinned test below); its sourcing is not.
    ("v_picks", "top", "default"): None,
    ("v_picks", "top", "json_schema"): {
        "title": "v_picks", "type": "string", "ui:entity_type": "brand", "ui:widget": "record_picker",
    },
    # help alone becomes helpText, which the variable schema reads as its description.
    ("v_hints", "top", "json_schema"): {"default": "", "description": "H", "title": "L", "type": "string"},
}


@pytest.fixture(scope="module", autouse=True)
def _register() -> None:
    register_builtin_nodes(overwrite=True)


@pytest.fixture(scope="module")
def surface():
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "in1",
                    "type": "io",
                    "position": {"x": 0, "y": 0},
                    "data": {"spec_type": "io.user_input", "config": {"fields": GOLDEN["fields"]}},
                }
            ],
            "edges": [],
            "variables": GOLDEN["variables"],
        }
    )
    return compile_graph(definition).input_surface


def _hints(spec) -> dict[str, object]:
    d = spec.declaration
    out: dict[str, object] = {
        "label": input_label(d) if spec.origin == "field" else (d.label or ""),
        "help": d.helpText or "",
        "placeholder": input_hint(d, "placeholder"),
        "options": input_options(d),
        "choice_style": input_choice_style(d),
        "option_labels": input_option_labels(d),
    }
    for key in ("primary", "advanced", "group", "order", "inline", "example", "detect", "required_in_form"):
        out[key] = input_hint(d, key)
    return out


@pytest.mark.parametrize("name", sorted(GOLDEN["expected"]))
def test_an_old_stored_input_compiles_to_what_the_old_engine_gave(name: str, surface) -> None:
    old = GOLDEN["expected"][name]
    spec = surface[name]
    assert isinstance(spec.declaration, VariableDefinition)
    new_top = {
        "kind": spec.kind,
        "variant": spec.variant,
        "sourcing": spec.sourcing,
        "default": spec.default,
        "json_schema": spec.json_schema,
        "referenced": spec.referenced,
    }
    for key, expected in old.items():
        if key == "hints":
            continue
        assert new_top[key] == DEVIATIONS.get((name, "top", key), expected), (name, key)
    new_hints = _hints(spec)
    for key, expected in old["hints"].items():
        assert new_hints[key] == DEVIATIONS.get((name, "hints", key), expected), (name, "hint", key)


def test_the_only_differences_are_the_named_deviations(surface) -> None:
    """A deviation entry that no longer deviates is itself a failure — the list stays honest."""
    for (name, section, key), new in DEVIATIONS.items():
        old = GOLDEN["expected"][name]
        old_value = old["hints"][key] if section == "hints" else old[key]
        assert old_value != new, (name, key)


def test_an_unrelated_deviation_is_known_and_pinned(surface) -> None:
    # The converter writes a record input's empty-string default as null (its "no value"), but the
    # sourcing stays what it was (owner ruling 2026-10-31): the old engine said 'optional' for a
    # variable with default "", so the converter writes that rule down instead of letting the null
    # turn it into 'require'. An explicit sourcing is kept as is.
    assert GOLDEN["expected"]["v_picks"]["sourcing"] == "optional"
    assert surface["v_picks"].sourcing == "optional"
    assert surface["v_picks"].default is None
    asked = declared_input({"name": "who", "picks": "note", "default": "", "sourcing": "ask"})
    assert asked.sourcing == "ask" and asked.defaultValue is None
    # help alone used to carry no description; the converter makes it the helpText, which the
    # variable schema reads as its description.
    assert "description" not in GOLDEN["expected"]["v_hints"]["json_schema"]
    assert surface["v_hints"].json_schema["description"] == "H"


def test_record_picks_and_multiple_derive_from_the_component() -> None:
    d = declared_input({"key": "src", "picks": ["note", "file"], "multiple": True})
    assert d.customComponent is not None and d.customComponent.type == "record"
    assert input_picks(d) == ["note", "file"]
    assert input_multiple(d) is True and input_type(d) == "text"
    one = declared_input({"key": "src", "picks": "note"})
    assert input_picks(one) == "note" and input_multiple(one) is False


def test_multi_choice_is_a_checkbox_and_reads_as_a_choice_that_takes_several() -> None:
    d = declared_input({"key": "tags", "type": "choice", "options": ["a", "b"], "multiple": True})
    assert d.customComponent is not None and d.customComponent.type == "checkbox"
    assert input_type(d) == "choice" and input_multiple(d) is True
    assert input_choice_style(d) == ""


def test_a_declaration_dict_passes_through_unchanged() -> None:
    d = declared_input({"key": "a", "type": "yes_no", "default": True})
    assert declared_input(d) is d
    assert declared_input(d.model_dump(mode="json", by_alias=True)) == d


def test_the_reader_defaults_are_the_old_hint_defaults() -> None:
    d = declared_input({"name": "bare"})
    assert [input_hint(d, k) for k in ("primary", "advanced", "group", "order", "inline", "example", "detect", "required_in_form", "placeholder")] == [
        False, None, "", None, False, "", [], False, "",
    ]
    with pytest.raises(KeyError):
        input_hint(d, "no_such_hint")


def test_a_number_that_took_several_keeps_multiple_in_stash() -> None:
    # Owner ruling 2026-10-31: the converter never drops data. A number cannot carry `multiple`,
    # so it is parked in the component's stash.
    d = declared_input({"key": "n", "type": "number", "multiple": True})
    assert d.customComponent is not None and d.customComponent.type == "number"
    assert d.customComponent.stash is not None
    assert d.customComponent.stash.model_dump(exclude_none=True, by_alias=True) == {"multiple": True}
    assert input_type(d) == "number"


def test_picks_on_a_file_field_keeps_the_file_and_parks_the_picks() -> None:
    # Owner ruling 2026-10-31: a file field stays a file field; `picks` (and picks_type_into) are
    # parked in stash, never turned into a record picker.
    d = declared_input({"key": "doc", "type": "file", "picks": "note", "picks_type_into": "q", "multiple": True})
    assert d.customComponent is not None and d.customComponent.type == "document"
    assert d.customComponent.stash is not None
    assert d.customComponent.stash.model_dump(exclude_none=True, by_alias=True) == {"tokens": ["note"], "picksTypeInto": "q"}
    assert input_type(d) == "file" and input_multiple(d) is True and input_picks(d) is None
