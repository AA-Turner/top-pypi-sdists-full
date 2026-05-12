"""Tests for the structured-tool abstraction (B5).

Adds two new methods to ProviderBase:
  - `supports_tools()` — True iff the provider can accept structured
    tool definitions instead of free-text RUN:/READ:/SEARCH:/FILE: blocks.
  - `format_tools(specs)` — translates a list of ToolSpec into the
    provider's wire format (Gemini function_declarations, OpenAI tools, etc.).

Default behavior on the base class: supports_tools() = False, format_tools()
raises NotImplementedError. Small/local providers (llama_cpp, ollama) keep
the default — small models don't follow JSON tool grammar reliably and
sage's text-format fallback is fine for them. Frontier providers (Gemini,
OpenAI-compat with strong models) override to return True and emit
provider-specific tool descriptors.
"""

from __future__ import annotations

import pytest


class TestProviderBaseDefaults:

    def test_supports_tools_default_false(self):
        from sage.providers.base import ProviderBase
        assert ProviderBase().supports_tools() is False

    def test_format_tools_default_raises(self):
        from sage.providers.base import ProviderBase
        with pytest.raises(NotImplementedError):
            ProviderBase().format_tools([])


class TestToolSpec:

    def test_tool_spec_is_constructible(self):
        from sage.providers.base import ToolSpec
        spec = ToolSpec(
            name="READ",
            description="Read a file from the project",
            parameters={
                "path": {"type": "string", "description": "Path to read"},
            },
            required=["path"],
        )
        assert spec.name == "READ"
        assert "path" in spec.parameters

    def test_sage_default_tools_includes_core_four(self):
        from sage.providers.base import default_sage_tools
        specs = default_sage_tools()
        names = {s.name for s in specs}
        assert {"READ", "SEARCH", "RUN", "FILE"} <= names


class TestLocalProvidersOptOut:

    def test_llama_cpp_does_not_support_tools(self):
        from sage.config import SageConfig
        from sage.providers.llama_cpp import LlamaCppProvider
        assert LlamaCppProvider(SageConfig()).supports_tools() is False

    def test_ollama_does_not_support_tools(self):
        from sage.config import SageConfig
        from sage.providers.openai_compat import OllamaProvider
        assert OllamaProvider(SageConfig()).supports_tools() is False


class TestGeminiSupportsTools:

    def test_gemini_supports_tools_returns_true(self):
        from sage.config import SageConfig
        from sage.providers.gemini import GeminiProvider
        provider = GeminiProvider(SageConfig())
        assert provider.supports_tools() is True

    def test_gemini_format_tools_returns_function_declarations(self):
        from sage.config import SageConfig
        from sage.providers.base import ToolSpec, default_sage_tools
        from sage.providers.gemini import GeminiProvider

        provider = GeminiProvider(SageConfig())
        formatted = provider.format_tools(default_sage_tools())
        # Gemini's tool format: {"function_declarations": [...]}
        assert "function_declarations" in formatted
        decls = formatted["function_declarations"]
        assert isinstance(decls, list)
        assert len(decls) >= 4  # READ, SEARCH, RUN, FILE
        names = {d["name"] for d in decls}
        assert {"READ", "SEARCH", "RUN", "FILE"} <= names

    def test_gemini_format_tools_includes_param_schema(self):
        from sage.config import SageConfig
        from sage.providers.base import ToolSpec
        from sage.providers.gemini import GeminiProvider

        provider = GeminiProvider(SageConfig())
        specs = [ToolSpec(
            name="READ",
            description="Read a file",
            parameters={"path": {"type": "string"}},
            required=["path"],
        )]
        formatted = provider.format_tools(specs)
        decl = formatted["function_declarations"][0]
        assert decl["name"] == "READ"
        # OpenAPI-style parameters object
        params = decl["parameters"]
        assert params["type"] == "object"
        assert "path" in params["properties"]
        assert params["required"] == ["path"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
