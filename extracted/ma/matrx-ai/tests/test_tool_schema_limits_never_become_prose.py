"""PB-07 defect 34: a provider-rejected schema keyword is DROPPED and RECORDED,
never rewritten into the tool description (text nobody authored).

Live: on Together (and every OpenAI-family strict schema) ``ask_person`` and
``scope_system`` had ``Must be at least 0.`` appended to parameter descriptions.
"""

from __future__ import annotations

import json
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

from matrx_ai.orchestrator.execution_state import ExecutionState, set_execution_state
from matrx_ai.tools.models import ToolDefinition

AUTHORED = "How long to wait."
_PARAMS: dict[str, Any] = {
    "timeout_seconds": {"type": "integer", "minimum": 0, "maximum": 600, "description": AUTHORED},
    "tags": {
        "type": "array",
        "minItems": 1,
        "description": "Tags.",
        "items": {"type": "string", "maxLength": 12, "description": "A tag."},
    },
    "box": {
        "type": "object",
        "description": "Box.",
        "properties": {"n": {"type": "integer", "minimum": 3, "description": "Count."}},
        "required": [],
    },
    "mode": {"type": "string", "enum": ["a", "b"], "description": "Mode."},
    "payload": {"type": "object", "description": "Free-form."},
    "level": {"type": "integer", "description": "Level.", "enum": [1, 3]},
}


def _tool() -> ToolDefinition:
    return ToolDefinition(name="limits_probe", description="Probe.", parameters=_PARAMS)


def _descriptions(node: Any) -> list[str]:
    out: list[str] = []
    if isinstance(node, dict):
        if isinstance(node.get("description"), str):
            out.append(node["description"])
        for v in node.values():
            out.extend(_descriptions(v))
    elif isinstance(node, list):
        for v in node:
            out.extend(_descriptions(v))
    return out


class _Emitter:
    async def send_info(self, payload: Any) -> None: ...

    async def send_warning(self, payload: Any) -> None: ...


def _run(fmt: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    state = ExecutionState()
    set_execution_state(state)
    token = set_app_context(AppContext(emitter=_Emitter(), user_id="u", request_id="r", conversation_id="c"))  # type: ignore[arg-type]
    try:
        wire = getattr(_tool(), fmt)()
    finally:
        clear_app_context(token)
    return wire, list(state.settings_adjustments or [])


@pytest.mark.parametrize("fmt", ["to_openai_format", "to_openai_responses_format", "to_google_format"])
def test_descriptions_stay_exactly_as_authored(fmt: str) -> None:
    wire, _ = _run(fmt)
    text = json.dumps(wire)
    assert "Must be" not in text and "at least" not in text and "Allowed values" not in text
    authored = {AUTHORED, "Tags.", "A tag.", "Box.", "Count.", "Mode.", "Level.", "Probe."}
    if fmt == "to_google_format":  # the JSON-string hint is kept, and recorded (below)
        authored |= {d for d in _descriptions(wire) if d.startswith("Free-form. Pass this as a JSON-encoded")}
    authored |= {"Free-form."}
    assert set(_descriptions(wire)) <= authored | {""}


@pytest.mark.parametrize("fmt", ["to_openai_format", "to_openai_responses_format"])
def test_strict_drop_is_recorded(fmt: str) -> None:
    _, rows = _run(fmt)
    keys = {r["key"] for r in rows}
    assert {
        "tool:limits_probe.timeout_seconds.minimum",
        "tool:limits_probe.timeout_seconds.maximum",
        "tool:limits_probe.tags.minItems",
        "tool:limits_probe.tags[].maxLength",
        "tool:limits_probe.box.n.minimum",
    } <= keys
    row = next(r for r in rows if r["key"].endswith("timeout_seconds.minimum"))
    assert row["action"] == "drop" and row["from"] == 0 and row["seam"] == "tool_schema"


def test_google_enum_drop_is_recorded() -> None:
    wire, rows = _run("to_google_format")
    assert "tool:limits_probe.level.enum" in {r["key"] for r in rows}
    assert "enum" not in wire["parameters"]["properties"]["level"]


def test_non_strict_providers_keep_limits_and_record_nothing() -> None:
    wire, rows = _run("to_anthropic_format")
    assert wire["input_schema"]["properties"]["timeout_seconds"]["minimum"] == 0
    assert rows == []


def test_google_json_string_hint_is_recorded_as_a_translation() -> None:
    wire, rows = _run("to_google_format")
    assert "JSON-encoded object string" in wire["parameters"]["properties"]["payload"]["description"]
    row = next(r for r in rows if r["key"] == "tool:limits_probe.payload.description_hint")
    assert row["action"] == "translate"
    assert row["reason"] == "Google cannot take object-typed args; sent as JSON string"
