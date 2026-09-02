"""Regression guard: a provider must NEVER receive two tool declarations with
the same name.

The incident: an agent run carried `update_plan` and `user` — each a single
`tool_def` with BOTH a `matrx-ai-core` executor binding (injected as a registered tool
into `config.tools`) AND a client-delegated executor (injected as an inline
copy into `config.custom_tools` by a capability auto-load). `merge_request_tools`
keys registered tools by registry UUID and inline tools by name, so the
cross-bucket name collision slipped past its dedup and both reached Anthropic →
400 "tools: Tool names must be unique."

The structural fix is `BaseTranslator.build_provider_tools`, the single
chokepoint every translator uses to turn a `UnifiedConfig` into the request's
`tools` array. It dedupes by name (first occurrence — the registered one —
wins). These tests pin that guarantee directly on the helper and via two real
translators (anthropic = top-level `name`, generic_openai = nested
`function.name`), so the duplicate can never reach a provider regardless of the
upstream double-injection bug.
"""
from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.providers.base_translator import BaseTranslator
from matrx_ai.tools.models import CustomTool
from matrx_ai.tools.registry import ToolRegistry


class _Translator(BaseTranslator):
    """Concrete stand-in — BaseTranslator is now an ABC (it requires
    _assemble_request), so the shared build_provider_tools is exercised through
    a minimal concrete subclass."""

    def _assemble_request(self, config, api_class=""):  # pragma: no cover
        return {}


def _config(tools: list[str], custom: list[CustomTool]) -> SimpleNamespace:
    # build_provider_tools only touches .tools and .custom_tools.
    return SimpleNamespace(tools=tools, custom_tools=custom)


def _custom(name: str) -> CustomTool:
    return CustomTool(name=name, description=f"inline {name}", input_schema={})


def test_cross_bucket_name_collision_dedups_to_one(monkeypatch) -> None:
    # config.tools (registered) AND config.custom_tools (inline) carry the same
    # name — the exact incident shape.
    monkeypatch.setattr(
        ToolRegistry,
        "get_provider_tools",
        lambda self, names, provider: [
            {"name": n, "description": f"registered {n}", "input_schema": {}}
            for n in names
        ],
    )
    cfg = _config(["update_plan", "user"], [_custom("update_plan"), _custom("user")])

    decls = _Translator().build_provider_tools(cfg, "anthropic")

    names = [d["name"] for d in decls]
    assert names.count("update_plan") == 1
    assert names.count("user") == 1
    assert len(names) == len(set(names))
    # First (registered) occurrence wins — registered tools are emitted first.
    assert decls[0]["description"].startswith("registered")


def test_anthropic_translator_payload_has_unique_tool_names(monkeypatch) -> None:
    monkeypatch.setattr(
        ToolRegistry,
        "get_provider_tools",
        lambda self, names, provider: [
            {"name": n, "description": f"registered {n}", "input_schema": {}}
            for n in names
        ],
    )
    cfg = _config(["update_plan"], [_custom("update_plan")])
    decls = _Translator().build_provider_tools(cfg, "anthropic")
    payload_names = [d["name"] for d in decls]
    assert payload_names == ["update_plan"]


def test_generic_openai_nested_function_name_dedups(monkeypatch) -> None:
    # OpenAI Chat shape nests the name under function.name — the extractor must
    # see through it.
    monkeypatch.setattr(
        ToolRegistry,
        "get_provider_tools",
        lambda self, names, provider: [
            {"type": "function", "function": {"name": n, "parameters": {}}}
            for n in names
        ],
    )
    cfg = _config(["update_plan"], [_custom("update_plan")])
    decls = _Translator().build_provider_tools(cfg, "generic_openai")
    extracted = [BaseTranslator._declaration_name(d) for d in decls]
    assert extracted == ["update_plan"]


def test_nameless_native_tools_are_never_deduped(monkeypatch) -> None:
    # Anthropic/OpenAI native server tools (web search etc.) have no top-level
    # name — they must all survive, never collapsed against each other.
    monkeypatch.setattr(
        ToolRegistry, "get_provider_tools", lambda self, names, provider: []
    )
    cfg = SimpleNamespace(tools=[], custom_tools=[])
    cfg.tools = ["x"]
    monkeypatch.setattr(
        ToolRegistry,
        "get_provider_tools",
        lambda self, names, provider: [
            {"type": "web_search_20250305"},
            {"type": "web_search_20250305"},
        ],
    )
    decls = _Translator().build_provider_tools(cfg, "anthropic")
    assert len(decls) == 2


def test_no_tools_returns_empty(monkeypatch) -> None:
    monkeypatch.setattr(
        ToolRegistry, "get_provider_tools", lambda self, names, provider: []
    )
    cfg = SimpleNamespace(tools=[], custom_tools=[])
    assert _Translator().build_provider_tools(cfg, "anthropic") == []
