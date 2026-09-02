"""Cross-field gate for providers that reject tools + structured output."""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.config import UnifiedConfig
from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities
from matrx_ai.providers.unified_client import _resolve_tool_structured_output_conflict


def _caps(name: str = "test-model"):
    return resolve_model_capabilities(
        SimpleNamespace(
            name=name,
            capabilities={
                "input": ["text"],
                "output": ["text"],
                "features": ["function_calling", "structured_output"],
            },
        )
    )


def _config(response_type: str = "json_schema") -> UnifiedConfig:
    return UnifiedConfig(
        model="test-model",
        messages=[],
        tools=["ctx_get"],
        custom_tools=[
            {
                "name": "lookup",
                "description": "Look up supporting evidence.",
                "input_schema": {"type": "object", "properties": {}},
            }
        ],
        mcp_servers=["research"],
        response_format={"type": response_type},
    )


def test_cerebras_keeps_schema_and_clears_effective_tools() -> None:
    config = _config()

    _resolve_tool_structured_output_conflict(config, _caps(), "cerebras_chat")

    assert config.response_format == {"type": "json_schema"}
    assert config.tools == []
    assert config.custom_tools == []
    assert config.mcp_servers == []
    assert config.tool_capability_filtered is True
    assert config.authored_tools == ["ctx_get"]
    assert [tool.name for tool in config.authored_custom_tools] == ["lookup"]
    assert config.authored_mcp_servers == ["research"]


def test_groq_json_mode_uses_the_same_shared_gate() -> None:
    config = _config("json_object")

    _resolve_tool_structured_output_conflict(config, _caps(), "groq_chat")

    assert config.response_format == {"type": "json_object"}
    assert config.tools == []


def test_compatible_wire_format_keeps_both_features() -> None:
    config = _config()

    _resolve_tool_structured_output_conflict(config, _caps(), "openai_chat")

    assert config.tools == ["ctx_get"]
    assert len(config.custom_tools) == 1


def test_text_output_keeps_tools() -> None:
    config = _config("text")

    _resolve_tool_structured_output_conflict(config, _caps(), "cerebras_chat")

    assert config.tools == ["ctx_get"]


def test_no_tool_surface_is_a_noop() -> None:
    config = UnifiedConfig(model="test-model", messages=[], response_format={"type": "json_schema"})

    _resolve_tool_structured_output_conflict(config, _caps(), "cerebras_chat")

    assert config.response_format == {"type": "json_schema"}
    assert config.tool_capability_filtered is False
