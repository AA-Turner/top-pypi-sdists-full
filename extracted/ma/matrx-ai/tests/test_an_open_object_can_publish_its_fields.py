"""An open object lists the fields worth showing and still accepts the rest, on every provider."""

from __future__ import annotations

import json

from matrx_ai.tools.models import ToolDefinition


def _definition() -> ToolDefinition:
    return ToolDefinition(
        name="demo_ask",
        description="Ask.",
        parameters={
            "kind": {"type": "string", "required": True},
            "payload": {
                "type": "object",
                "additionalProperties": True,
                "description": "Per kind.",
                "properties": {
                    "questions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"type": {"type": "string", "enum": ["choice", "text"]}},
                        },
                    }
                },
            },
        },
    )


def _payload(fmt: dict) -> dict:
    return json.loads(json.dumps(fmt))


def test_anthropic_sees_the_enum_and_the_object_stays_open():
    schema = _definition().to_anthropic_format()["input_schema"]["properties"]["payload"]
    assert schema["properties"]["questions"]["items"]["properties"]["type"]["enum"] == ["choice", "text"]
    assert schema["additionalProperties"] is True


def test_strict_mode_keeps_it_a_bare_object_so_no_other_kind_is_forbidden():
    text = json.dumps(_definition().to_openai_format())
    assert '"questions"' not in text


def test_gemini_keeps_it_a_bare_object():
    assert '"questions"' not in json.dumps(_definition().to_google_format())


def test_a_closed_object_stays_closed():
    definition = _definition()
    definition.parameters["payload"].pop("additionalProperties")
    schema = definition.to_anthropic_format()["input_schema"]["properties"]["payload"]
    assert schema["additionalProperties"] is False
