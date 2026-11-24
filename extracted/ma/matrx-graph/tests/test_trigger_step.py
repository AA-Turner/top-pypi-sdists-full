"""THE TRIGGER STEP (``io.trigger``) — a second registration of the Collect Inputs executor.

Its fields join the ONE input surface beside ``io.user_input``'s; a field name both declare is a
compile refusal naming both steps; at most one Trigger step, and nothing wires into it; a
definition without one validates exactly as before; the palette never confuses it with
``data.trigger_kind``.
"""

from __future__ import annotations

import pytest

from matrx_graph import Definition, compile_graph, default_registry, register_builtin_nodes
from matrx_graph.errors import CompilationError
from matrx_graph.nodes.io.user_input import INPUT_SOURCE_TYPES, TriggerStepExecutor, UserInputExecutor
from matrx_graph.validation import validate_definition


@pytest.fixture(scope="module", autouse=True)
def _register() -> None:
    register_builtin_nodes(overwrite=True)


def _node(node_id: str, spec_type: str, fields: list[dict] | None = None) -> dict:
    config = {"fields": fields} if fields is not None else {}
    return {"id": node_id, "type": "io", "position": {"x": 0, "y": 0}, "data": {"spec_type": spec_type, "config": config}}


def _field(name: str, required: bool = False) -> dict:
    return {"key": name, "label": name.title(), "type": "text", "required": required}


def _definition(nodes: list[dict], edges: list[dict] | None = None) -> Definition:
    return Definition.model_validate({"nodes": nodes, "edges": edges or []})


def _messages(d: Definition) -> list[str]:
    return [i.message for i in validate_definition(d, registry=default_registry()).issues]


def test_it_is_the_same_executor_class_and_config_registered_twice() -> None:
    reg = default_registry()
    trig, collect = reg.get("io.trigger"), reg.get("io.user_input")
    assert isinstance(trig, TriggerStepExecutor) and isinstance(trig, UserInputExecutor)
    assert type(trig).execute is UserInputExecutor.execute
    assert trig.spec.config_schema is collect.spec.config_schema
    assert trig.spec.is_source and trig.spec.dynamic_output
    assert INPUT_SOURCE_TYPES == {"io.user_input", "io.trigger"}


def test_the_palette_never_calls_the_kind_subscription_a_trigger_step() -> None:
    reg = default_registry()
    entry = reg.get("io.trigger").spec.to_palette_descriptor()
    assert entry["display_name"] == "Trigger"
    assert entry["group"] == reg.get("io.user_input").spec.to_palette_descriptor()["group"]
    assert "Not a mid-run data subscription" in entry["description"]
    if reg.has("data.trigger_kind"):
        assert reg.get("data.trigger_kind").spec.display_name != "Trigger"


def test_its_fields_join_the_one_input_surface() -> None:
    d = _definition([_node("start", "io.trigger", [_field("item_id", True)]), _node("ask", "io.user_input", [_field("note")])])
    surface = compile_graph(d, registry=default_registry()).input_surface
    assert set(surface) == {"item_id", "note"}
    assert surface["item_id"].node_id == "start" and surface["item_id"].sourcing == "require"


def test_a_field_name_clash_names_both_steps() -> None:
    d = _definition([_node("start", "io.trigger", [_field("topic")]), _node("ask", "io.user_input", [_field("topic")])])
    with pytest.raises(CompilationError) as err:
        compile_graph(d, registry=default_registry())
    assert "the Trigger step 'start'" in str(err.value) and "input node 'ask'" in str(err.value)
    assert any("the Trigger step 'start'" in m and "input node 'ask'" in m for m in _messages(d))


def test_one_trigger_step_per_workflow() -> None:
    d = _definition([_node("t1", "io.trigger", [_field("a")]), _node("t2", "io.trigger", [_field("b")])])
    assert any("one Trigger step" in m and "'t2'" in m for m in _messages(d))


def test_nothing_connects_into_the_trigger_step() -> None:
    d = _definition(
        [_node("ask", "io.user_input", [_field("a")]), _node("start", "io.trigger", [_field("b")])],
        [{"id": "e1", "source": "ask", "target": "start"}],
    )
    assert any("nothing connects into it" in m for m in _messages(d))


def test_a_definition_without_a_trigger_step_gains_no_new_error() -> None:
    d = _definition([_node("ask", "io.user_input", [_field("a", True)])])
    assert not any("Trigger step" in m for m in _messages(d))
