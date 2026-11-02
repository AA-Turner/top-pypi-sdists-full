"""An input step can carry everything a declared variable can (Rule 18, 2026-10-28).

Rule 18 moves every value a workflow uses onto a visible input step. A declared
variable could already be a LIST (``multiple``) or a record PICKER (``picks``,
e.g. organizations); an ``io.user_input`` field could not, so a workflow taking
"which organizations" had to keep that value secret in its variables. These pin
that a field carries both: the run form asks for a list / a picker, and a
started run delivers the list unchanged to the steps that read it.
"""

from __future__ import annotations

import pytest

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)

from tests._fixtures import FakeEmitter, make_app_context


@pytest.fixture(scope="module", autouse=True)
def _register() -> None:
    register_builtin_nodes(overwrite=True)


def _graph():
    return compile_graph(
        Definition.model_validate(
            {
                "nodes": [
                    {
                        "id": "in1",
                        "type": "io",
                        "position": {"x": 0, "y": 0},
                        "data": {
                            "spec_type": "io.user_input",
                            "config": {
                                "fields": [
                                    {"key": "organization_ids", "label": "Organizations", "picks": "organization", "multiple": True, "default": []},
                                    {"key": "kinds", "label": "Kinds", "multiple": True, "default": []},
                                ]
                            },
                        },
                    }
                ],
                "edges": [],
            }
        )
    )


def test_a_field_asks_for_a_list_and_a_picker() -> None:
    surface = _graph().input_surface
    orgs = surface["organization_ids"].json_schema
    assert orgs["type"] == "array" and orgs["items"] == {"type": "string"}
    assert orgs["ui:multiple"] is True
    assert orgs["ui:widget"] == "record_picker" and orgs["ui:entity_type"] == "organization"
    assert orgs["default"] == []
    kinds = surface["kinds"].json_schema
    assert kinds["type"] == "array" and kinds["ui:multiple"] is True
    assert "ui:entity_type" not in kinds


async def test_a_started_run_delivers_the_list_unchanged() -> None:
    scheduler = Scheduler(
        _graph(),
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        surface_inputs={"organization_ids": ["o1", "o2"], "kinds": ["note"]},
        input_provenance={"organization_ids": "caller", "kinds": "caller"},
    )
    result = await scheduler.run(run_id="run-lists-1", max_steps=10)
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["in1"]["organization_ids"] == ["o1", "o2"]
    assert result.last_outputs["in1"]["kinds"] == ["note"]


def test_a_pick_several_choice_limits_each_item_not_the_list() -> None:
    """A choice field with ``multiple`` takes a list; each ITEM must be one of the options.
    An ``enum`` on the array itself would refuse every list (Choose pages to read, 2026-10-29)."""
    graph = compile_graph(
        Definition.model_validate(
            {
                "nodes": [
                    {
                        "id": "in1",
                        "type": "io",
                        "position": {"x": 0, "y": 0},
                        "data": {
                            "spec_type": "io.user_input",
                            "config": {
                                "fields": [
                                    {"key": "kinds_first", "type": "choice", "multiple": True, "options": ["about", "pricing"], "option_labels": {"about": "About us"}, "default": ["about"]},
                                ]
                            },
                        },
                    }
                ],
                "edges": [],
            }
        )
    )
    schema = graph.input_surface["kinds_first"].json_schema
    assert schema["type"] == "array"
    assert "enum" not in schema
    assert schema["items"] == {"type": "string", "enum": ["about", "pricing"]}
    assert schema["ui:option_labels"] == {"about": "About us"}


def test_a_json_field_takes_structured_data_like_a_run_variable() -> None:
    """Moving a run variable that holds records onto the input step must not refuse them (Rule 18,
    2026-10-29): a field of kind ``json`` accepts a list of objects or an object."""
    from matrx_graph.nodes.io.user_input import UserInputConfig
    from matrx_graph.executor.schema_validation import validate_instance

    config = UserInputConfig.model_validate(
        {"fields": [{"key": "batches", "kind": "json", "default": []}, {"key": "extra", "kind": "json", "default": {}}]}
    )
    schema = config.effective_output_json_schema()
    assert "type" not in schema["properties"]["batches"]
    assert schema["properties"]["batches"]["ui:widget"] == "json"
    assert validate_instance(schema, {"batches": [{"batch_id": "b1", "values": {}}], "extra": {"a": 1}}) == []


async def test_a_started_run_takes_records_on_a_json_field() -> None:
    graph = compile_graph(
        Definition.model_validate(
            {
                "nodes": [
                    {
                        "id": "in1",
                        "type": "io",
                        "position": {"x": 0, "y": 0},
                        "data": {
                            "spec_type": "io.user_input",
                            "config": {"fields": [{"key": "batches", "label": "Batches", "kind": "json", "default": []}]},
                        },
                    }
                ],
                "edges": [],
            }
        )
    )
    batches = [{"batch_id": "b1", "values": {"x": 1}}]
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(FakeEmitter()),
        surface_inputs={"batches": batches},
        input_provenance={"batches": "caller"},
    )
    result = await scheduler.run(run_id="run-json-1", max_steps=10)
    assert result.status is RunStatus.COMPLETED, result.error
    assert result.last_outputs["in1"]["batches"] == batches


def test_an_input_step_field_may_pick_from_several_record_types() -> None:
    from matrx_graph.nodes.io.user_input import UserInputConfig

    cfg = UserInputConfig(fields=[
        {"key": "source_kind", "label": "Kind", "required": False, "default": ""},
        {"key": "source_id", "label": "Source", "picks": ["note", "file"], "picks_type_into": "source_kind"},
    ])
    prop = cfg.effective_output_json_schema()["properties"]["source_id"]
    assert prop["ui:widget"] == "record_picker"
    assert prop["ui:entity_type"] == ["note", "file"]
    assert prop["ui:entity_type_field"] == "source_kind"
