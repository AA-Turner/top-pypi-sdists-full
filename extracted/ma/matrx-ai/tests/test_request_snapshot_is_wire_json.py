"""PB-03 defect 10: ``chat.request_snapshot.request_payload`` is the WIRE JSON.

Live 2026-10-16 (conversation a6f49033-…): the Google snapshot stored
``config`` as the Python ``str()`` of the SDK's ``GenerateContentConfig``
("http_options=None should_return_http_response=None …") — unreadable as data,
unreplayable. Root cause: ``picklist_runtime.redact_wire_payload`` serialized the
captured payload with ``json.dumps(..., default=str)``; any request carrying a
pick-list / reference swap turned every SDK model in it into a string. The
snapshot writer's own serializer also dumped SDK models in python mode (every
``None`` field kept, bytes as ``<bytes len=N>`` placeholders), which is not what
the SDK puts on the wire either.

Both seams now go through ``providers.snapshot.wire_json``: an SDK (pydantic)
model becomes ``model_dump(mode="json", exclude_none=True)`` — the SDK's own wire
form — so every provider's snapshot is plain JSON (OpenAI / Anthropic / Together
payloads are already dicts and are unchanged).
"""

from __future__ import annotations

import json
from typing import Any

from google.genai import types

from matrx_ai.config.picklist_runtime import clear_wire_swaps, redact_wire_payload, set_wire_swaps
from matrx_ai.orchestrator.executor import _snapshot_request_json
from matrx_ai.providers.snapshot import wire_json

SECRET = "Pacific Crest Freight — bay 3, dock 14, the long reference value"


def _google_payload() -> dict[str, Any]:
    return {
        "model": "gemini-flash-lite-latest",
        "contents": [
            types.Content(
                role="user",
                parts=[types.Part(text=f"Carrier notes: {SECRET}")],
            ),
            types.Content(
                role="model",
                parts=[types.Part(text="ok", thought_signature=b"\x01\x02\x03")],
            ),
        ],
        "config": types.GenerateContentConfig(
            system_instruction="You are the routing desk.",
            temperature=0.3,
            max_output_tokens=65536,
            thinking_config=types.ThinkingConfig(thinking_budget=2048, include_thoughts=True),
            tool_config=types.ToolConfig(
                function_calling_config=types.FunctionCallingConfig(mode="AUTO")
            ),
            tools=[
                types.Tool(
                    function_declarations=[
                        {
                            "name": "agent_call",
                            "description": "Run a saved agent",
                            "parameters": {
                                "type": "object",
                                "properties": {"agent_id": {"type": "string"}},
                                "required": ["agent_id"],
                            },
                        }
                    ]
                )
            ],
        ),
    }


def _assert_wire_json(payload: Any) -> None:
    assert isinstance(payload, dict)
    config = payload["config"]
    assert isinstance(config, dict), f"config stored as {type(config).__name__}: {str(config)[:80]}"
    assert config["thinking_config"] == {"include_thoughts": True, "thinking_budget": 2048}
    assert config["tools"][0]["function_declarations"][0]["name"] == "agent_call"
    assert "http_options" not in config  # None fields are not on the wire
    assert isinstance(payload["contents"][0], dict)
    signature = payload["contents"][1]["parts"][0]["thought_signature"]
    assert isinstance(signature, str) and "len=" not in signature  # base64, never a placeholder
    json.dumps(payload)  # plain JSON all the way down


def test_wire_json_serializes_sdk_models() -> None:
    _assert_wire_json(wire_json(_google_payload()))


def test_snapshot_writer_stores_wire_json() -> None:
    _assert_wire_json(_snapshot_request_json(_google_payload()))


def test_redaction_keeps_the_wire_json_shape() -> None:
    set_wire_swaps({"{{carrier}}": SECRET})
    try:
        redacted = redact_wire_payload(_google_payload())
    finally:
        clear_wire_swaps()
    _assert_wire_json(redacted)
    assert SECRET not in json.dumps(redacted)
    assert "{{carrier}}" in json.dumps(redacted)


def test_plain_dict_payloads_are_unchanged() -> None:
    openai_like = {"model": "gpt-5-nano", "input": [{"role": "user", "content": "hi"}], "reasoning": {"effort": "high"}}
    assert wire_json(openai_like) == openai_like
