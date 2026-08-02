"""PRO-1879: reasoning tools attach only for weak non-reasoning models.

``_is_weak_model`` is the classifier gating agno's ReasoningTools in
``build_agent_args``. Weak-marker allowlist: unknown/unmatched ids are
treated as strong (no tools), and natively-reasoning families are excluded
even when a weak size marker matches (``gpt-5-mini``).
"""

from types import SimpleNamespace

import pytest

from xpander_sdk.modules.backend.frameworks.agno import _is_weak_model


def _model(model_id):
    return SimpleNamespace(id=model_id)


@pytest.mark.parametrize(
    "model_id",
    [
        "gpt-4.1-mini",
        "openai/gpt-4.1-nano",
        "gpt-4o-mini",
        "gpt-4o",
        "gpt-3.5-turbo",
        "google/gemini-2.5-flash-lite",
        "amazon.nova-lite-v1:0",
        "amazon.nova-micro-v1:0",
        "mistral-small-3",
        "ministral-8b",
        "meta.llama3-8b-instruct-v1:0",
        "meta-llama/llama-3.1-8b-instruct",
        "google/gemma-3-4b-it",
        "z-ai/glm-4.5-air",
    ],
)
def test_weak_models_get_reasoning_tools(model_id):
    assert _is_weak_model(_model(model_id)) is True


@pytest.mark.parametrize(
    "model_id",
    [
        # small but natively reasoning — exclusion wins over the size marker
        "gpt-5-mini",
        "gpt-5-nano",
        "openai/o4-mini",
        "o3-mini",
        "x-ai/grok-3-mini",
        "moonshotai/kimi-k2-thinking",
        "deepseek/deepseek-r1-distill-llama-8b",
        "perplexity/sonar-reasoning",
    ],
)
def test_native_reasoning_models_excluded(model_id):
    assert _is_weak_model(_model(model_id)) is False


@pytest.mark.parametrize(
    "model_id",
    [
        "claude-sonnet-4-6",
        "global.anthropic.claude-opus-4-7",
        "gpt-5.2",
        "google/gemini-3-pro-preview",
        "gemini-2.5-pro",
        "deepseek-r1",
        "qwen/qwen3-max",
        "openai/gpt-oss-120b",
    ],
)
def test_strong_models_excluded(model_id):
    assert _is_weak_model(_model(model_id)) is False


@pytest.mark.parametrize("model_id", ["", None, "some-brand-new-model"])
def test_unknown_or_empty_id_defaults_to_strong(model_id):
    assert _is_weak_model(_model(model_id)) is False
