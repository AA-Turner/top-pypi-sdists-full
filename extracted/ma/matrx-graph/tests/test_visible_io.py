"""Rule 18 (Arman, 2026-10-28): what comes in and what goes out is visible on the canvas.

A workflow with no input step, no output step, a run value no input step shows, or a write whose
result never reaches an output step is named — by ``visible_io_findings`` and, as a WARNING, by
``validate_definition`` (every save / publish / validate door), which never blocks the save.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.types.definition import Definition
from matrx_graph.validation import validate_definition
from matrx_graph.visible_io import visible_io_findings


def _node(nid: str, spec: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"id": nid, "type": spec, "position": {"x": 0, "y": 0}, "data": {"spec_type": spec, **(data or {})}}


def _edge(src: str, dst: str) -> dict[str, Any]:
    return {"id": f"{src}-{dst}", "source": src, "target": dst}


INPUT = _node("ask", "io.user_input", {"config": {"fields": [{"key": "topic", "label": "Topic", "type": "text"}]}})
OUTPUT = _node("show", "output.to_frontend", {"config": {"mode": "full", "title": "Result"}})


def _codes(raw: dict[str, Any]) -> list[tuple[str, str | None]]:
    return sorted((f.code, f.subject) for f in visible_io_findings(Definition.model_validate(raw)))


def test_a_visible_workflow_has_no_findings() -> None:
    raw = {
        "nodes": [INPUT, _node("shape", "data.transform", {"input": {"t": {"$input": "topic"}}}), OUTPUT],
        "edges": [_edge("ask", "shape"), _edge("shape", "show")],
    }
    assert _codes(raw) == []


def test_no_input_and_no_output_step_are_named() -> None:
    raw = {"nodes": [_node("shape", "data.transform")], "edges": []}
    assert _codes(raw) == [("no_input_step", None), ("no_output_step", None)]


def test_every_secret_input_door_is_named() -> None:
    raw = {
        "nodes": [
            INPUT,
            _node("a", "data.transform", {"input": {"b": {"$input": "brand_id"}, "t": {"$input": "topic"}}}),
            _node("b", "data.transform", {"input": {"who": {"$run": "user_id"}}}),
            _node("c", "text.template", {"inputs": {"template": "Visit {{trigger.record.title}}"}}),
            _node("d", "data.transform", {"input": {"m": {"$var": "mode"}}}),
            OUTPUT,
        ],
        "edges": [_edge("ask", "a"), _edge("a", "b"), _edge("b", "c"), _edge("c", "d"), _edge("d", "show")],
        "variables": [{"name": "scope", "default": "all"}],
    }
    hidden = {(f.subject, f.via) for f in visible_io_findings(Definition.model_validate(raw)) if f.code == "hidden_input"}
    assert hidden == {("brand_id", "$input"), ("run", "$run"), ("trigger", "trigger"), ("mode", "$var"), ("scope", "variable")}


def test_an_entry_step_reading_the_callers_values_is_a_hidden_input() -> None:
    raw = {
        "nodes": [_node("start", "data.transform", {"config": {"expression": "{'b': inputs['brand_id']}"}}), OUTPUT],
        "edges": [_edge("start", "show")],
    }
    assert ("hidden_input", "start (caller values)") in _codes(raw)


def test_a_write_whose_result_never_reaches_an_output_is_hidden() -> None:
    raw = {
        "nodes": [INPUT, _node("save", "data.record.save_many"), _node("save2", "data.record.upsert"), OUTPUT],
        "edges": [_edge("ask", "save"), _edge("ask", "save2"), _edge("save2", "show")],
    }
    assert _codes(raw) == [("hidden_write", "data.record.save_many")]


def test_the_validator_warns_and_never_blocks() -> None:
    raw = {"nodes": [_node("shape", "data.transform")], "edges": []}
    result = validate_definition(raw)
    rule18 = [i for i in result.issues if "input step" in i.message or "output step" in i.message]
    assert len(rule18) == 2
    assert all(i.severity == "warning" for i in rule18)
    assert not [i for i in result.issues if i.severity == "error" and i in rule18]
