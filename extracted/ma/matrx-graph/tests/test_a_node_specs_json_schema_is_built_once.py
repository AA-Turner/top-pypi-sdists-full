"""A node spec's JSON Schema is built once per schema class (2026-11-03: the palette and /ai/context/preview rebuilt
every spec's schema on the event loop — the named frame of repeated 1-3 s event_loop_stall rows)."""

from __future__ import annotations

from pydantic import BaseModel

from matrx_graph.types import node_spec


class _In(BaseModel):
    text: str


def test_the_schema_is_built_once_and_each_caller_gets_its_own_copy(monkeypatch) -> None:
    calls = 0
    real = _In.model_json_schema.__func__

    def counted(cls, *args, **kwargs):
        nonlocal calls
        calls += 1
        return real(cls, *args, **kwargs)

    monkeypatch.setattr(_In, "model_json_schema", classmethod(counted))
    node_spec._JSON_SCHEMAS.pop(_In, None)
    first = node_spec.model_json_schema_once(_In)
    first["properties"]["text"]["poisoned"] = True
    second = node_spec.model_json_schema_once(_In)
    assert calls == 1
    assert "poisoned" not in second["properties"]["text"] and second["required"] == ["text"]


def test_a_registered_specs_schemas_are_not_rebuilt_per_call(monkeypatch) -> None:
    from matrx_graph import NodeRegistry, register_builtin_nodes

    registry = NodeRegistry()
    register_builtin_nodes(registry)
    spec = next(s for s in registry.all_specs() if s.input_schema is not None)
    first = spec.input_json_schema()
    model = spec.input_schema

    def refuse(*args, **kwargs):
        raise AssertionError(f"{model.__name__}'s JSON Schema was rebuilt on a second ask")

    monkeypatch.setattr(model, "model_json_schema", classmethod(refuse))
    assert spec.input_json_schema() == first


def test_an_action_descriptor_does_not_rebuild_a_shared_schema(monkeypatch) -> None:
    """2026-11-13: GET /actions built one descriptor per declared mandate, each rebuilding the same two
    classes' schemas on the event loop (event_loop_stall; the watchdog named ``ActionSpec.to_descriptor``)."""
    from matrx_graph.actions import ActionSpec, build_action_node_spec
    from matrx_graph.types.primitives import ActionTier, NodeCategory

    class _Out(BaseModel):
        answer: str = "none"

    def spec(name: str) -> ActionSpec:
        return ActionSpec(
            name=name, description="d", category=NodeCategory.CUSTOM, determinism=ActionTier.NON_DETERMINISTIC,
            input_schema=_In, output_schema=_Out,
            node_spec=build_action_node_spec(
                name=name, description="d", category=NodeCategory.CUSTOM, determinism=ActionTier.NON_DETERMINISTIC,
                input_schema=_In, output_schema=_Out, icon=None, tags=(), version="1.0.0",
            ),
        )

    first = spec("demo.one").to_descriptor()
    first["output_schema"]["properties"]["answer"]["poisoned"] = True

    def refuse(*args, **kwargs):
        raise AssertionError("a shared Action schema was rebuilt for a second descriptor")

    monkeypatch.setattr(_In, "model_json_schema", classmethod(refuse))
    monkeypatch.setattr(_Out, "model_json_schema", classmethod(refuse))
    second = spec("demo.two").to_descriptor()
    assert "poisoned" not in second["output_schema"]["properties"]["answer"]
    assert second["input_schema"]["required"] == ["text"]
