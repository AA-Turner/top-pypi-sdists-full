"""An agent's ``output_schema`` is its one output contract.

A ``settings.response_format`` saved beside it (written by the agent builder's old
"response format" control) must never shadow it: a stale schema copy missing a
required property, or ``{"type": "text"}``, read downstream as caller-supplied and
kept the real schema from binding (measured 2026-10-06 on five agents).
"""

from __future__ import annotations

import pytest

from matrx_ai.client_host.agent_source import (
    ExecutionAgentDefinition,
    definition_to_agent_config,
)

REAL = {
    "name": "page",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {"__kind": {"type": "string"}, "title": {"type": "string"}},
        "required": ["__kind", "title"],
    },
}
STALE_COPY = {
    "type": "json_schema",
    "json_schema": {
        "name": "page",
        "schema": {
            "type": "object",
            "properties": {"title": {"type": "string"}},
            "required": ["title"],
        },
    },
}


def _config(settings_rf: object | None, output_schema: dict | None = REAL):
    settings: dict[str, object] = {"temperature": 0.2}
    if settings_rf is not None:
        settings["response_format"] = settings_rf
    definition = ExecutionAgentDefinition.model_validate(
        {
            "definition_id": "a1",
            "agent_id": "a1",
            "name": "Page Builder",
            "model_id": "m",
            "messages": [{"role": "system", "content": "x"}],
            "settings": settings,
            "output_schema": output_schema,
        }
    )
    return definition_to_agent_config(definition)


@pytest.mark.parametrize("stale", [{"type": "text"}, STALE_COPY, {"type": "json_object"}])
def test_settings_response_format_never_shadows_output_schema(stale: object) -> None:
    cfg = _config(stale)
    assert cfg.config.response_format == {"type": "json_schema", "json_schema": REAL}
    assert cfg.config.temperature == 0.2  # other settings untouched


def test_agent_without_output_schema_keeps_its_settings_response_format() -> None:
    cfg = _config({"type": "json_object"}, output_schema=None)
    assert cfg.config.response_format == {"type": "json_object"}
