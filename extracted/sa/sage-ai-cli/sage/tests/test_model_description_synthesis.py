"""Tests for the synthesized model descriptions in /models table.

Catches the regression where Ollama + llama_cpp rows show an empty
Description column because their ModelInfo objects don't carry one.
"""

from __future__ import annotations

import pytest

from sage.core.renderer_cli import _synthesize_model_description


class TestSynthesizedDescriptions:

    def test_ollama_local_model(self):
        out = _synthesize_model_description({
            "name": "llama3.2:latest", "provider": "ollama", "local": True,
        })
        assert "Local Ollama" in out

    def test_ollama_pullable_model_with_size(self):
        out = _synthesize_model_description({
            "name": "Qwen 2.5 Coder (0.5b-32b)", "provider": "ollama", "local": False,
        })
        assert "Pullable via Ollama" in out
        assert "0.5b-32b" in out
        assert "code generation" in out

    def test_llama_cpp_local(self):
        out = _synthesize_model_description({
            "name": "Qwen2.5-Coder-7B-Instruct-Q4_K_M",
            "provider": "llama_cpp", "local": True,
        })
        assert "GGUF" in out
        assert "code generation" in out

    def test_vision_model_hint(self):
        out = _synthesize_model_description({
            "name": "Llama 3.2 Vision (11b-90b)",
            "provider": "ollama", "local": False,
        })
        assert "multimodal" in out

    def test_embed_model_hint(self):
        out = _synthesize_model_description({
            "name": "Nomic Embed Text V2 MoE (embed)",
            "provider": "ollama", "local": False,
        })
        assert "embedding model" in out

    def test_empty_when_no_useful_signal(self):
        out = _synthesize_model_description({
            "name": "", "provider": "", "local": False,
        })
        assert out == ""

    def test_unknown_family_returns_provider_only(self):
        out = _synthesize_model_description({
            "name": "weird-model-name", "provider": "ollama", "local": False,
        })
        # Falls back to "Pullable via Ollama" with no size or family hint
        assert "Pullable via Ollama" in out
