"""A device route sends OpenAI chat-completions tool declarations, never a catalog-chosen shape.

A model on a person's computer always speaks llama-server's OpenAI dialect, so the device route
sets the tool format itself. An own model file has no catalog offering, so reading the format
from the catalog found none ("names no tool-declaration format") and measured its tools in an
unknown shape (L5 rerun walk, 2026-10-24).
"""

# ruff: noqa: F811 — pytest fixtures imported from test_device_served_via
from __future__ import annotations

from typing import Any

import pytest
from test_device_served_via import FILE_ID, _own_sv, own_file_placement  # noqa: F401


@pytest.fixture
def probe_tool():
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    saved = (dict(registry._tools), dict(registry._tools_by_id), registry._loaded)

    async def _probe(args: dict[str, Any], ctx: Any) -> Any:
        return None

    registry.register_local(
        "math_calculate", _probe, description="calculate",
        parameters={"expression": {"type": "string", "description": "an expression"}},
    )
    registry._loaded = True
    yield "math_calculate"
    registry._tools.clear()
    registry._tools.update(saved[0])
    registry._tools_by_id.clear()
    registry._tools_by_id.update(saved[1])
    registry._loaded = saved[2]


def _own_file_config() -> Any:
    from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage

    return UnifiedConfig(
        model=FILE_ID, served_via=_own_sv(), tools=["math_calculate"],
        messages=MessageList(_messages=[UnifiedMessage(role="user", content=[TextContent(text="2+2?")])]),
    )


def test_the_estimator_reads_the_device_route_not_the_catalog(monkeypatch, probe_tool) -> None:
    from matrx_ai.config import context_preflight

    announced: list[str] = []
    monkeypatch.setattr(context_preflight, "_announce_once", lambda key, message: announced.append(message))
    assert context_preflight._wire_tool_format(_own_file_config()) == "generic_openai"
    assert announced == []


@pytest.mark.asyncio
async def test_an_own_file_device_profile_builds_openai_tool_declarations(own_file_placement, probe_tool) -> None:
    from matrx_ai.catalog.resolve import resolve_call_profile
    from matrx_ai.providers.device import DeviceChat

    profile = await resolve_call_profile(FILE_ID, served_via=_own_sv())
    body = DeviceChat().to_provider_config(_own_file_config(), profile)
    [tool] = body["tools"]
    assert tool["type"] == "function"
    assert tool["function"]["name"] == "math_calculate"
    assert tool["function"]["parameters"]["type"] == "object"
