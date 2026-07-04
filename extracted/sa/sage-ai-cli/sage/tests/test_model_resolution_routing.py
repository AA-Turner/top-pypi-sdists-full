"""Regression tests for `_resolve_model_prefix` model-routing bugs.

Specifically guards against the bug where an OpenRouter-format model ID like
`qwen/qwen3-coder:free` was being split on the colon (treating the part
before `:` as a provider), then falling through to fuzzy match and landing
on `deepinfra:Qwen/Qwen3-Coder` — which the user has no API key for.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest

from sage.config import SageConfig
from sage.cli_core import _resolve_model_prefix, _providers_with_keys


@pytest.fixture
def openrouter_only_config(monkeypatch):
    """Simulate a user with only an OpenRouter key set — no DeepInfra etc.

    Constructs a SageConfig directly instead of calling load_config(), which
    would re-read the project .env file. That file has inline-comment lines
    that, when re-parsed into env, poison pydantic-settings in later tests.
    """
    for env_var in (
        "SAGE_GROQ_API_KEY", "SAGE_CEREBRAS_API_KEY", "SAGE_SAMBANOVA_API_KEY",
        "SAGE_TOGETHER_API_KEY", "SAGE_MISTRAL_API_KEY", "SAGE_COHERE_API_KEY",
        "GITHUB_TOKEN", "SAGE_DEEPSEEK_API_KEY", "SAGE_DEEPINFRA_API_KEY",
        "GOOGLE_API_KEY", "GEMINI_API_KEY",
    ):
        monkeypatch.delenv(env_var, raising=False)
    monkeypatch.setenv("SAGE_OPENROUTER_API_KEY", "test-key")
    return SageConfig(api_keys={"openrouter": "test-key"})


class TestOpenRouterColonInModelId:
    """`qwen/qwen3-coder:free` must NOT be split as provider=qwen/qwen3-coder."""

    def test_openrouter_free_id_resolves_to_openrouter(self, openrouter_only_config):
        # The `:free` suffix is part of the OpenRouter ID — `/` in the prefix
        # signals "this is a vendor-namespaced model, not provider:model".
        with patch("sage.providers.openrouter_catalog.fetch_free_models",
                   return_value=[]):
            result = _resolve_model_prefix(
                "qwen/qwen3-coder:free", openrouter_only_config,
            )
        assert result == "openrouter:qwen/qwen3-coder:free", \
            f"Expected openrouter: prefix, got {result!r}"

    def test_openai_oss_id_resolves_to_openrouter(self, openrouter_only_config):
        with patch("sage.providers.openrouter_catalog.fetch_free_models",
                   return_value=[]):
            result = _resolve_model_prefix(
                "openai/gpt-oss-120b:free", openrouter_only_config,
            )
        assert result == "openrouter:openai/gpt-oss-120b:free"

    def test_deepseek_v3_resolves_to_openrouter(self, openrouter_only_config):
        with patch("sage.providers.openrouter_catalog.fetch_free_models",
                   return_value=[]):
            result = _resolve_model_prefix(
                "deepseek/deepseek-r1:free", openrouter_only_config,
            )
        assert result == "openrouter:deepseek/deepseek-r1:free"

    def test_ollama_style_colon_tag_still_works(self, openrouter_only_config):
        """`gemma3:latest` is an Ollama tag — no `/` in prefix, must NOT
        re-route to openrouter. Falls through to the Ollama-running probe."""
        with patch("sage.providers.openrouter_catalog.fetch_free_models",
                   return_value=[]), \
             patch("httpx.get", side_effect=Exception("no ollama")):
            result = _resolve_model_prefix("gemma3:latest", openrouter_only_config)
        # Either ollama:gemma3:latest or falls all the way back to ollama tag
        assert result.startswith("ollama:"), f"got {result!r}"


class TestFuzzyMatchRespectsKeyedProviders:
    """Fuzzy match must skip providers the user has no key for."""

    def test_qwen3_coder_does_not_fall_to_deepinfra(self, openrouter_only_config):
        """The historical bug: `qwen3-coder` (no slash, no colon) fuzzy-matched
        to deepinfra:Qwen/Qwen3-Coder, then 4xx'd at runtime because no key."""
        with patch("sage.providers.openrouter_catalog.fetch_free_models",
                   return_value=[]), \
             patch("httpx.get", side_effect=Exception("no ollama")):
            result = _resolve_model_prefix("qwen3-coder", openrouter_only_config)
        # Should NOT land on deepinfra (no key). Acceptable outcomes:
        # openrouter:... (if matched live), ollama:qwen3-coder (last resort),
        # or any keyed provider.
        provider = result.split(":", 1)[0]
        assert provider != "deepinfra", \
            f"resolved to {result!r} — should never pick deepinfra without an API key"


class TestProvidersWithKeys:
    """The keyed-providers helper used by the fuzzy-match gate."""

    def test_no_keys_returns_only_local_providers(self, monkeypatch):
        # Construct config directly (don't load_config) to keep .env out of env.
        from sage.providers.openai_compat import PROVIDER_SPECS
        cfg = SageConfig(api_keys={})
        for spec in PROVIDER_SPECS:
            monkeypatch.delenv(spec.env_var, raising=False)
        for v in ("GOOGLE_API_KEY", "GEMINI_API_KEY"):
            monkeypatch.delenv(v, raising=False)
        result = _providers_with_keys(cfg)
        assert {"ollama", "llama_cpp"} <= result
        assert "deepinfra" not in result
        assert "openrouter" not in result

    def test_openrouter_key_present(self, monkeypatch):
        monkeypatch.setenv("SAGE_OPENROUTER_API_KEY", "test-key")
        cfg = SageConfig(api_keys={})
        result = _providers_with_keys(cfg)
        assert "openrouter" in result

    def test_gemini_via_google_api_key(self, monkeypatch):
        monkeypatch.setenv("GOOGLE_API_KEY", "test-key")
        cfg = SageConfig(api_keys={})
        result = _providers_with_keys(cfg)
        assert "gemini" in result
