"""A turn whose agent has tools must never run with zero tools because this
process's tool registry is not loaded.

The incident (2026-10-12 to 2026-10-15): a local aidream started with
``uvicorn --lifespan off`` never ran ``initialize_tool_system``. Every agent turn
it served went to the provider with NO ``tools`` key — the model wrote its tool
calls as plain text and 0 tools ran (conversation 7c272874 + 11 others), while
``/health`` said ok. ``get_provider_tools`` printed a red line and returned ``[]``.

Guarded here, through the real chokepoint (``BaseTranslator.build_provider_tools``):
  - unloaded registry + registered tools  -> ToolSystemNotReadyError (never ``[]``)
  - the error classifies as non-retryable ``matrx_tool_system_not_ready``
  - ``ensure_tool_system_ready`` loads on demand, and is bounded when the load hangs
  - request-scoped projections still need no registry
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from matrx_ai.providers.base_translator import BaseTranslator
from matrx_ai.providers.errors import classify_internal_error
from matrx_ai.tools import handle_tool_calls
from matrx_ai.tools.models import ToolDefinition, ToolType
from matrx_ai.tools.registry import ToolRegistry, ToolSystemNotReadyError


class _Translator(BaseTranslator):
    def _assemble_request(self, config, api_class=""):  # pragma: no cover
        return {}


def _config(tools: list[str]) -> SimpleNamespace:
    return SimpleNamespace(tools=tools, custom_tools=[])


def _tool(name: str) -> ToolDefinition:
    return ToolDefinition(
        name=name,
        description=f"{name} tool",
        parameters={"q": {"type": "string", "description": "query"}},
        tool_type=ToolType.EXTERNAL_MCP,
    )


@pytest.fixture
def fresh_registry(monkeypatch) -> ToolRegistry:
    """A brand-new, never-loaded registry — the --lifespan off process state."""
    registry = ToolRegistry()
    monkeypatch.setattr(ToolRegistry, "_instance", registry)
    monkeypatch.setattr(handle_tool_calls, "_ready_lock", None)
    return registry


def test_unloaded_registry_refuses_turn_instead_of_sending_zero_tools(fresh_registry) -> None:
    assert not fresh_registry.loaded
    with pytest.raises(ToolSystemNotReadyError, match="tools are not loaded yet"):
        _Translator().build_provider_tools(_config(["web_search", "news_get"]), "anthropic")


def test_loaded_empty_registry_also_refuses(fresh_registry) -> None:
    fresh_registry.load_from_definitions([])
    assert fresh_registry.loaded and fresh_registry.count == 0
    with pytest.raises(ToolSystemNotReadyError):
        _Translator().build_provider_tools(_config(["web_search"]), "anthropic")


def test_no_registered_tools_needs_no_registry(fresh_registry) -> None:
    assert _Translator().build_provider_tools(_config([]), "anthropic") == []


def test_loaded_registry_sends_the_tools(fresh_registry) -> None:
    fresh_registry.load_from_definitions([_tool("web_search")])
    decls = _Translator().build_provider_tools(_config(["web_search"]), "anthropic")
    assert [d["name"] for d in decls] == ["web_search"]


def test_refusal_classifies_as_non_retryable_not_ready() -> None:
    err = classify_internal_error(ToolSystemNotReadyError("tools are not loaded yet"), "anthropic")
    assert err is not None
    assert err.error_type == "matrx_tool_system_not_ready"
    assert err.is_retryable is False
    assert "tools are not loaded yet" in err.user_message


def test_ensure_ready_loads_on_demand(fresh_registry, monkeypatch) -> None:
    calls: list[int] = []

    async def _load() -> int:
        calls.append(1)
        return fresh_registry.load_from_definitions([_tool("web_search")])

    monkeypatch.setattr(handle_tool_calls, "initialize_tool_system", _load)

    async def _run() -> tuple[bool, bool]:
        first, second = await asyncio.gather(
            handle_tool_calls.ensure_tool_system_ready(),
            handle_tool_calls.ensure_tool_system_ready(),
        )
        return first, second

    assert asyncio.run(_run()) == (True, True)
    assert calls == [1]  # concurrent turns share one load
    decls = _Translator().build_provider_tools(_config(["web_search"]), "anthropic")
    assert [d["name"] for d in decls] == ["web_search"]


def test_ensure_ready_is_bounded_when_load_hangs(fresh_registry, monkeypatch) -> None:
    async def _hang() -> int:
        await asyncio.sleep(30)
        return 0

    monkeypatch.setattr(handle_tool_calls, "initialize_tool_system", _hang)
    ready = asyncio.run(handle_tool_calls.ensure_tool_system_ready(timeout_s=0.05))
    assert ready is False
    with pytest.raises(ToolSystemNotReadyError):
        _Translator().build_provider_tools(_config(["web_search"]), "anthropic")
