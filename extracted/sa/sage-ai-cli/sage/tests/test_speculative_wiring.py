"""Tests pinning speculative-decoding wiring (C10).

Background: `cfg.speculative_draft_model` is a real config field. The
question this file answers is which inference paths actually use it.

Findings as of this test file's creation:
  - llama_cpp provider: WIRED. Uses `speculative_kwargs(cfg)` and merges
    into `Llama(**kwargs)`. Confirmed by inspecting providers/llama_cpp.py:217-227.
  - Ollama provider: NOT WIRED. /api/chat payload omits any draft_model.
    Ollama's documented mechanism is Modelfile params (`PARAMETER
    draft_model X`), not request-time. Wiring it requires a Modelfile-
    baking change in `sage train`.

These tests pin both states. If someone unwires llama_cpp, the first
test catches it; if someone wires Ollama, the second test goes red as a
signal to update this file and the roadmap.
"""

from __future__ import annotations

from pathlib import Path

import pytest


# ── llama_cpp: WIRED ─────────────────────────────────────────────────────


class TestLlamaCppSpeculativeWiring:

    def test_speculative_kwargs_returns_empty_when_unconfigured(self):
        """No draft model in cfg → speculative_kwargs returns {}."""
        from sage.config import SageConfig
        from sage.core.speculative import speculative_kwargs
        cfg = SageConfig()  # default has empty speculative_draft_model
        assert cfg.speculative_draft_model == ""
        assert speculative_kwargs(cfg) == {}

    def test_speculative_kwargs_returns_path_when_configured(self, tmp_path, monkeypatch):
        """Configured draft model resolves to path → kwargs include draft_model."""
        from sage.config import SageConfig
        from sage.core.speculative import speculative_kwargs

        # Plant a fake GGUF in the simulated SAGE models dir.
        sage_dir = tmp_path / ".sage"
        models_dir = sage_dir / "models"
        models_dir.mkdir(parents=True)
        gguf = models_dir / "llama3.2.gguf"
        gguf.write_bytes(b"fake-gguf-data")
        monkeypatch.setattr(Path, "home", lambda: tmp_path)

        cfg = SageConfig(speculative_draft_model="llama_cpp:llama3.2")
        kwargs = speculative_kwargs(cfg)
        assert kwargs == {"draft_model": str(gguf)}

    def test_llama_cpp_provider_invokes_speculative_helper(self, monkeypatch):
        """LlamaCppProvider._maybe_speculative_kwargs delegates to speculative_kwargs(cfg)."""
        from sage.config import SageConfig
        from sage.providers.llama_cpp import LlamaCppProvider

        cfg = SageConfig()
        provider = LlamaCppProvider(cfg)

        sentinel = {"draft_model": "/tmp/draft.gguf"}
        calls = []

        def fake_kwargs(c):
            calls.append(c)
            return sentinel

        monkeypatch.setattr("sage.core.speculative.speculative_kwargs", fake_kwargs)
        out = provider._maybe_speculative_kwargs()
        assert out == sentinel
        assert calls == [cfg], "provider must pass its own config to speculative_kwargs"


# ── Ollama: NOT WIRED (gap documented, future C10b will address) ─────────


class TestOllamaSpeculativeUnwired:
    """Pins the *current* state: Ollama provider does not forward
    `speculative_draft_model` to the daemon. This is intentional for now —
    Ollama enables speculation via Modelfile PARAMETER, not request-time.
    Wiring it requires modifying `sage train` to bake `PARAMETER draft_model X`
    into the Modelfile.

    When someone wires it (future C10b work), this test should be UPDATED
    to assert the new behavior, not deleted — the assertion shape is the
    canonical place to document what payload Ollama receives.
    """

    def test_generate_payload_does_not_include_draft_model(self, monkeypatch):
        import sage.providers.openai_compat as oc
        from sage.config import SageConfig
        from sage.providers.base import Message
        from sage.providers.openai_compat import OllamaProvider

        cfg = SageConfig(speculative_draft_model="llama_cpp:llama3.2")
        provider = OllamaProvider(cfg)
        provider._pulled_names = {"qwen3"}  # skip auto-pull

        captured_payload: dict = {}

        class _FakeResponse:
            status_code = 200
            def raise_for_status(self): pass
            def json(self):
                return {"message": {"content": "hello", "thinking": ""}}

        class _FakeClient:
            def __init__(self, *a, **kw): pass
            def __enter__(self): return self
            def __exit__(self, *a): pass
            def post(self, url, json):
                captured_payload.update(json)
                return _FakeResponse()

        monkeypatch.setattr(oc.httpx, "Client", _FakeClient)
        provider.generate([Message(role="user", content="ping")], model="qwen3")

        # Pin the current behavior: payload has no draft hint anywhere.
        assert "draft_model" not in captured_payload
        assert "draft" not in (captured_payload.get("options") or {})


class TestOllamaModelfileDraftWiring:
    """C10b: when cfg.speculative_draft_model is set, `sage train` should
    bake `PARAMETER draft_model <name>` into the Modelfile so Ollama uses
    speculative decoding."""

    def test_speculative_for_ollama_returns_none_when_unconfigured(self):
        from sage.config import SageConfig
        from sage.core.speculative import speculative_for_ollama
        assert speculative_for_ollama(SageConfig()) is None

    def test_speculative_for_ollama_returns_bare_name(self):
        from sage.config import SageConfig
        from sage.core.speculative import speculative_for_ollama
        cfg = SageConfig(speculative_draft_model="ollama:llama3.2")
        assert speculative_for_ollama(cfg) == "llama3.2"

    def test_speculative_for_ollama_accepts_bare_name(self):
        """User may set `speculative_draft_model = "llama3.2"` without prefix."""
        from sage.config import SageConfig
        from sage.core.speculative import speculative_for_ollama
        cfg = SageConfig(speculative_draft_model="llama3.2")
        assert speculative_for_ollama(cfg) == "llama3.2"

    def test_speculative_for_ollama_skips_llama_cpp_prefix(self):
        """Cfg using llama_cpp prefix means draft is for llama_cpp path,
        not Ollama. speculative_for_ollama should return None."""
        from sage.config import SageConfig
        from sage.core.speculative import speculative_for_ollama
        cfg = SageConfig(speculative_draft_model="llama_cpp:llama3.2")
        assert speculative_for_ollama(cfg) is None

    def test_train_ollama_model_bakes_draft_parameter(self, tmp_path, monkeypatch):
        """When speculative is configured, the Modelfile must include
        `PARAMETER draft_model <name>`."""
        from sage.config import SageConfig
        import sage.main as sage_main

        # Force the speculative config
        monkeypatch.setattr(
            "sage.config.load_config",
            lambda *a, **kw: SageConfig(speculative_draft_model="ollama:llama3.2"),
        )
        # Mock the model-size probe so we don't depend on Ollama running.
        monkeypatch.setattr(sage_main, "_get_model_size_gb", lambda _name: 5.0)
        # Mock ollama exe + subprocess.run to avoid actually creating the model.
        monkeypatch.setattr(sage_main, "_ollama_exe", lambda: "/bin/true")
        import types as _types
        monkeypatch.setattr(
            sage_main.subprocess,
            "run",
            lambda *a, **kw: _types.SimpleNamespace(returncode=0, stdout="", stderr=""),
        )

        # Use a tmp home so the modelfile lands in a known place
        monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

        ok = sage_main._train_ollama_model("qwen3-coder-next")
        assert ok is True

        # Read the Modelfile we wrote
        modelfile = (tmp_path / ".sage" / "modelfiles" / "qwen3-coder-next.modelfile").read_text()
        assert "PARAMETER draft_model llama3.2" in modelfile, (
            f"Modelfile should bake the speculative draft model. Got:\n{modelfile}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
