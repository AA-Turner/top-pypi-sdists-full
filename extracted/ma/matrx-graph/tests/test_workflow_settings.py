"""Workflow settings: named, labelled, typed behaviour knobs a person changes without touching steps.

R3 (2026-11-15, the readable-research ruling): "a graph a non-programmer reads and changes ... every rule
that shapes behaviour a visible, editable setting". A setting is a declared input in the ``Settings`` group
(``matrx_graph.workflow_settings``): steps read it with ``{"$input": name}``, it is versioned with the
definition, a run may override it, and both its default and an override are checked against its type.
"""

from __future__ import annotations

import pytest

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph
from matrx_graph.nodes import register_builtin_nodes
from matrx_graph.patch import DefinitionPatch, DefinitionPatchError, apply_patch
from matrx_graph.validation import validate_definition
from matrx_graph.workflow_settings import declared_settings

from tests._fixtures import make_app_context


def _setting(**over: object) -> dict[str, object]:
    base: dict[str, object] = {
        "name": "part_size",
        "label": "Part size",
        "helpText": "How many items go in each part.",
        "defaultValue": 2,
        "customComponent": {"type": "number"},
        "hints": {"group": "Settings"},
    }
    base.update(over)
    return base


def _unit(setting: dict[str, object]) -> Definition:
    return Definition.model_validate(
        {
            "variables": [setting],
            "nodes": [
                {
                    "id": "split",
                    "type": "data.batch",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"size": {"$input": "part_size"}}, "input": {"items": [1, 2, 3, 4, 5, 6]}},
                }
            ],
            "edges": [],
        }
    )


def test_a_setting_is_a_declared_input_in_the_settings_group() -> None:
    defn = _unit(_setting())
    assert [s.name for s in declared_settings(list(defn.variables))] == ["part_size"]
    plain = _unit(_setting(hints=None))
    assert declared_settings(list(plain.variables)) == []


@pytest.mark.parametrize(
    ("over", "words"),
    [
        ({"defaultValue": None}, "needs a default value"),
        ({"defaultValue": "lots"}, "takes a number"),
        ({"sourcing": "ask"}, "cannot be asked for or required"),
    ],
)
def test_a_wrongly_declared_setting_is_named_at_validate(over: dict[str, object], words: str) -> None:
    registry = register_builtin_nodes(NodeRegistry())
    result = validate_definition(_unit(_setting(**over)).model_dump(mode="json"), registry=registry)
    assert any(words in i.message for i in result.issues), [i.message for i in result.issues]


def test_set_workflow_setting_changes_a_declared_setting_by_name() -> None:
    defn = _unit(_setting())
    changed = apply_patch(
        defn, DefinitionPatch(ops=[{"op": "set_workflow_setting", "key": "part_size", "value": "3"}])
    )
    assert changed.variables[0].defaultValue == 3
    with pytest.raises(DefinitionPatchError, match="takes a number"):
        apply_patch(defn, DefinitionPatch(ops=[{"op": "set_workflow_setting", "key": "part_size", "value": "lots"}]))


async def _run(defn: Definition, **surface: object):
    registry = register_builtin_nodes(NodeRegistry())
    graph = compile_graph(defn, registry=registry)
    return await Scheduler(
        graph, MemoryCheckpointer(), make_app_context(), registry=registry, surface_inputs=dict(surface)
    ).run(run_id=f"t-setting-{len(surface)}-{sorted(surface.items())!r}")


async def test_steps_read_the_setting_and_a_run_may_override_it() -> None:
    defn = _unit(_setting(defaultValue=2))
    default_run = await _run(defn)
    assert default_run.status is RunStatus.COMPLETED, default_run.error
    assert default_run.last_outputs["split"]["count"] == 3
    override = await _run(defn, part_size=3)
    assert override.status is RunStatus.COMPLETED, override.error
    assert override.last_outputs["split"]["count"] == 2


async def test_a_run_override_that_does_not_fit_parks_the_run_naming_it() -> None:
    result = await _run(_unit(_setting()), part_size="lots")
    assert result.status is RunStatus.AWAITING_INPUT
    assert "takes a number" in repr(result.model_dump() if hasattr(result, "model_dump") else result)


def _list_setting(**over: object) -> dict[str, object]:
    base: dict[str, object] = {
        "name": "left_out",
        "label": "Left out",
        "helpText": "Verdicts that keep a source out.",
        "defaultValue": ["ignored", "dead_link"],
        "hints": {"group": "Settings"},
    }
    base.update(over)
    return base


def test_a_list_setting_is_a_list_of_text() -> None:
    from matrx_graph.input_declaration import VariableDefinition
    from matrx_graph.workflow_settings import setting_type, setting_value_problem

    var = VariableDefinition.model_validate(_list_setting())
    assert setting_type(var) == "list"
    assert setting_value_problem(var, ["a", "b"]) is None
    assert setting_value_problem(var, []) is None
    assert "takes a list of text" in (setting_value_problem(var, "a") or "")
    assert "takes a list of text" in (setting_value_problem(var, ["a", 3]) or "")
    registry = register_builtin_nodes(NodeRegistry())
    bad = _unit(_list_setting(defaultValue=["a", 3])).model_dump(mode="json")
    result = validate_definition(bad, registry=registry)
    assert any("takes a list of text" in i.message for i in result.issues), [i.message for i in result.issues]


def test_set_workflow_setting_sets_a_list_from_text() -> None:
    defn = _unit(_list_setting())
    for text in ('["ignored", "content_mismatch"]', "ignored, content_mismatch"):
        changed = apply_patch(
            defn, DefinitionPatch(ops=[{"op": "set_workflow_setting", "key": "left_out", "value": text}])
        )
        assert changed.variables[0].defaultValue == ["ignored", "content_mismatch"]
    with pytest.raises(DefinitionPatchError, match="takes a list of text"):
        apply_patch(defn, DefinitionPatch(ops=[{"op": "set_workflow_setting", "key": "left_out", "value": "[1, 2]"}]))


def test_a_choice_setting_names_a_value_outside_its_options() -> None:
    choice = {"customComponent": {"type": "select", "options": ["quick", "deep"]}, "defaultValue": "quick"}
    defn = _unit(_setting(**choice))
    changed = apply_patch(
        defn, DefinitionPatch(ops=[{"op": "set_workflow_setting", "key": "part_size", "value": "deep"}])
    )
    assert changed.variables[0].defaultValue == "deep"
    with pytest.raises(DefinitionPatchError, match="is one of quick, deep"):
        apply_patch(defn, DefinitionPatch(ops=[{"op": "set_workflow_setting", "key": "part_size", "value": "huge"}]))
