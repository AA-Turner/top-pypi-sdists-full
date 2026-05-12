"""Tests for task-aware model routing (C8).

`pick_model_for_task(prompt, available, context_size)` should classify
the prompt's complexity and pick the smallest model that's strong enough.
Goals:
  - Trivial tasks (typo fix, rename) → small fast model (saves time and
    keeps the local GPU free).
  - Complex tasks (architecture, multi-file refactor) → biggest model
    available (correctness matters more than latency here).
  - Large context (close to a model's window) → force a model with
    adequate context regardless of complexity.
"""

from __future__ import annotations

import pytest


def _model(name: str, provider: str = "ollama", local: bool = True):
    from sage.providers.base import ModelInfo
    return ModelInfo(id=name, provider=provider, name=name, local=local)


# Reusable model catalog covering small / medium / big tiers across providers.
SMALL = [
    _model("llama3.2"),        # 3B
    _model("qwen2.5-coder-3b"),
    _model("gemini-2.0-flash", provider="gemini", local=False),
]
MEDIUM = [
    _model("qwen2.5-coder-7b"),
    _model("gemini-1.5-flash", provider="gemini", local=False),
]
BIG = [
    _model("qwen3-coder-next"),
    _model("deepseek-r1"),
]
ALL_MODELS = SMALL + MEDIUM + BIG


class TestComplexityClassification:

    def test_short_typo_fix_is_trivial(self):
        from sage.core.router import classify_task_complexity
        assert classify_task_complexity("rename foo to bar") == "trivial"
        assert classify_task_complexity("fix the typo on line 12") == "trivial"

    def test_long_prompt_is_complex(self):
        from sage.core.router import classify_task_complexity
        long_prompt = (
            "Refactor the authentication subsystem to split the session-cookie "
            "logic from the user-identification logic, and update all 14 call "
            "sites in middleware/, then add tests covering both the happy path "
            "and the 5 edge cases discussed in issue #482. The architecture "
            "should follow the pattern we use for billing."
        )
        assert classify_task_complexity(long_prompt) == "complex"

    def test_keyword_architecture_is_complex(self):
        from sage.core.router import classify_task_complexity
        assert classify_task_complexity("design the architecture") == "complex"
        assert classify_task_complexity("refactor the system") == "complex"

    def test_default_medium_for_normal_prompts(self):
        from sage.core.router import classify_task_complexity
        assert classify_task_complexity("add a /health endpoint") == "medium"


class TestPickModelForTask:

    def test_trivial_picks_smallest_available(self):
        from sage.core.router import pick_model_for_task
        picked = pick_model_for_task("rename foo to bar", ALL_MODELS)
        # Should pick a small-tier model
        assert picked in {m.id for m in SMALL}

    def test_complex_picks_biggest_available(self):
        from sage.core.router import pick_model_for_task
        picked = pick_model_for_task(
            "refactor the entire architecture and add tests for all modules",
            ALL_MODELS,
        )
        assert picked in {m.id for m in BIG}

    def test_returns_none_when_no_models_available(self):
        from sage.core.router import pick_model_for_task
        assert pick_model_for_task("anything", []) is None

    def test_falls_back_to_available_tier_when_preferred_missing(self):
        """If big models aren't available but medium are, complex tasks
        should still pick the best available (medium), not return None."""
        from sage.core.router import pick_model_for_task
        picked = pick_model_for_task(
            "design the architecture for the new payment service",
            SMALL + MEDIUM,  # no big tier
        )
        # Must pick something — fallback to medium is acceptable
        assert picked is not None
        assert picked in {m.id for m in MEDIUM} or picked in {m.id for m in SMALL}

    def test_large_context_forces_capable_model(self):
        """When context_size approaches small-model context window, must
        skip small models even for trivial prompts."""
        from sage.core.router import pick_model_for_task
        # 100k tokens of context — small models with 8k-16k ctx can't handle this
        picked = pick_model_for_task(
            "rename foo to bar",
            ALL_MODELS,
            context_size=100_000,
        )
        # llama3.2 has only ~8k ctx, must be skipped
        assert picked != "llama3.2"


class TestProviderRouterAutoPrefix:
    """Integration: `resolve("auto")` should pick a model via
    pick_model_for_task using whatever prompt context is available.

    For now we verify the API exists. Engine wiring (passing the actual
    user prompt) happens at the engine.py layer in a follow-up.
    """

    def test_resolve_auto_returns_some_provider(self):
        from sage.core.router import ProviderRouter
        from sage.providers.base import ProviderBase, ModelInfo

        class _MockProvider(ProviderBase):
            name = "mock"
            def is_available(self): return True
            def list_models(self):
                return [
                    ModelInfo(id="small-3b", provider="mock", name="small", local=True),
                    ModelInfo(id="big-32b", provider="mock", name="big", local=True),
                ]
            def generate(self, *a, **kw): return "ok"
            def stream(self, *a, **kw): yield "ok"

        router = ProviderRouter([_MockProvider()])
        provider, model_name = router.resolve("auto")
        assert provider.name == "mock"
        assert model_name in ("small-3b", "big-32b")


class TestEngineToAutoRoutingIntegration:
    """C8b: router.generate/.stream extracts the user prompt from messages
    when model_id == "auto" so the picker actually has signal."""

    def test_generate_with_auto_picks_small_for_simple_prompt(self):
        from sage.core.router import ProviderRouter
        from sage.providers.base import Message, ModelInfo, ProviderBase

        called_with = {}

        class _MockProvider(ProviderBase):
            name = "mock"
            def is_available(self): return True
            def list_models(self):
                return [
                    ModelInfo(id="llama3.2", provider="mock", name="3b", local=True),
                    ModelInfo(id="deepseek-r1", provider="mock", name="big", local=True),
                ]
            def generate(self, messages, model_name, *a, **kw):
                called_with["model"] = model_name
                return "ok"
            def stream(self, *a, **kw):
                yield "ok"

        router = ProviderRouter([_MockProvider()])
        router.generate([Message(role="user", content="rename foo to bar")], model_id="auto")
        assert called_with["model"] == "llama3.2"  # small tier for trivial task

    def test_generate_with_auto_picks_big_for_complex_prompt(self):
        from sage.core.router import ProviderRouter
        from sage.providers.base import Message, ModelInfo, ProviderBase

        called_with = {}

        class _MockProvider(ProviderBase):
            name = "mock"
            def is_available(self): return True
            def list_models(self):
                return [
                    ModelInfo(id="llama3.2", provider="mock", name="3b", local=True),
                    ModelInfo(id="deepseek-r1", provider="mock", name="big", local=True),
                ]
            def generate(self, messages, model_name, *a, **kw):
                called_with["model"] = model_name
                return "ok"
            def stream(self, *a, **kw):
                yield "ok"

        router = ProviderRouter([_MockProvider()])
        router.generate(
            [Message(role="user",
                     content="refactor the entire architecture of the auth subsystem")],
            model_id="auto",
        )
        assert called_with["model"] == "deepseek-r1"  # big tier for complex task


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
