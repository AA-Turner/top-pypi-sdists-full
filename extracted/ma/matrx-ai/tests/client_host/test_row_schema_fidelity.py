"""Row → provider-schema fidelity: required flags and anyOf optionals survive.

A ``tool.definition`` row carries a FULL JSON schema
(``{type, properties, required}``); the registry unwraps it to the internal
key→property notation. Without explicit carry-over, the top-level
``required`` list vanishes (the model then omits mandatory args) and
``anyOf`` optionals get defaulted to ``"type": "string"`` (the model sends
strings for integers). 65/113 matrx-local tools lost required flags this
way. Pinned here across the row → ToolDefinition → provider-format path.
"""

from __future__ import annotations

import uuid

from matrx_ai.tools.registry import ToolRegistry


def _bash_like_row() -> dict:
    return {
        "id": str(uuid.uuid4()),
        "name": "local_bash",
        "description": "Run a shell command",
        "source_kind": "native",
        "function_path": "",
        "is_active": True,
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "the command"},
                "timeout": {
                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                    "description": "seconds",
                },
                "options": {
                    "type": "object",
                    "properties": {"cwd": {"type": "string"}},
                    "required": ["cwd"],
                },
            },
            "required": ["command", "options"],
        },
    }


def test_required_list_survives_to_anthropic_schema():
    tool_def = ToolRegistry._row_to_definition(_bash_like_row())
    schema = tool_def.get_provider_format("anthropic")["input_schema"]

    assert sorted(schema["required"]) == ["command", "options"]
    # The nested object keeps its OWN required list untouched.
    assert schema["properties"]["options"]["required"] == ["cwd"]


def test_anyof_optional_keeps_real_type():
    tool_def = ToolRegistry._row_to_definition(_bash_like_row())
    schema = tool_def.get_provider_format("anthropic")["input_schema"]
    assert schema["properties"]["timeout"]["type"] == "integer"


def test_required_list_survives_to_openai_and_google():
    tool_def = ToolRegistry._row_to_definition(_bash_like_row())

    openai_schema = tool_def.get_provider_format("openai")["parameters"]
    assert sorted(openai_schema["required"]) == ["command", "options"]

    google_schema = tool_def.get_provider_format("google")
    params = google_schema["parameters"] if "parameters" in google_schema else google_schema
    assert sorted(params.get("required", [])) == ["command", "options"]


def test_internal_notation_rows_unchanged():
    """Rows already in the internal key→property notation (no wrapper) keep
    their per-property required bools working as before."""
    row = {
        "id": str(uuid.uuid4()),
        "name": "legacy_tool",
        "source_kind": "native",
        "is_active": True,
        "parameters": {
            "query": {"type": "string", "required": True},
            "limit": {"type": "integer"},
        },
    }
    tool_def = ToolRegistry._row_to_definition(row)
    schema = tool_def.get_provider_format("anthropic")["input_schema"]
    assert schema["required"] == ["query"]
