"""One meaning of ``input_tokens``, on every chat-completions provider.

CANONICAL (same as OpenAI / Gemini / Anthropic in ``TokenUsage.from_*``):
``input_tokens`` EXCLUDES cache reads; ``cached_input_tokens`` carries them; the
provider's ``prompt_tokens`` == input_tokens + cached_input_tokens. Cost is
``input_tokens * input_price + cached_input_tokens * cached_input_price``.

Before 2026-10-18 Groq and Together stored the whole ``prompt_tokens`` as
input and dropped the cache split (Groq: 1.13M cached of 8.31M prompt tokens in
14 days, cached_tokens column 0 on all 3,748 rows), so cache hits were billed
at the full input rate. Each case below is a recorded raw usage block (shapes
copied from chat.request.raw_usage) -> translator -> TokenUsage -> cost, against
a hand-computed expectation.
"""

from __future__ import annotations

from types import SimpleNamespace as NS

import pytest

from matrx_ai.config.usage_config import ModelPricing, PricingTier, openai_compatible_usage_counts


def _lookup(api: str, model: str, inp: float, cached: float, out: float) -> dict[str, ModelPricing]:
    tier = PricingTier(max_tokens=None, input_price=inp, output_price=out, cached_input_price=cached)
    return {model: ModelPricing(model_name=model, api=api, tiers=[tier])}


def _response(model: str, usage: dict) -> NS:
    msg = NS(content="hi", role="assistant", tool_calls=None, reasoning=None, reasoning_content=None, executed_tools=None, annotations=None)
    choice = NS(message=msg, finish_reason="stop", index=0)
    details = usage.get("prompt_tokens_details")
    u = NS(**{**usage, "prompt_tokens_details": NS(**details) if isinstance(details, dict) else details})
    return NS(id="r1", model=model, choices=[choice], usage=u, created=0)


def _translators():
    from matrx_ai.providers.cerebras.translator import CerebrasTranslator
    from matrx_ai.providers.generic_openai.translator import GenericOpenAITranslator
    from matrx_ai.providers.groq.translator import GroqTranslator
    from matrx_ai.providers.together.translator import TogetherTranslator

    return {
        "groq": lambda r: GroqTranslator().from_groq(r),
        "together": lambda r: TogetherTranslator().from_together(r),
        "cerebras": lambda r: CerebrasTranslator().from_cerebras(r),
        "moonshot": lambda r: GenericOpenAITranslator().from_generic_openai(r, "moonshot"),
    }


# provider, model, usage block, expected (input, cached, output), prices (in, cached, out)
CASES = [
    ("groq", "openai/gpt-oss-20b",
     {"prompt_tokens": 2390, "completion_tokens": 156, "total_tokens": 2546, "prompt_tokens_details": {"cached_tokens": 768}},
     (1622, 768, 156), (0.075, 0.0375, 0.30)),
    ("groq", "openai/gpt-oss-20b",  # prompt_tokens_details null, as groq sends it on a miss
     {"prompt_tokens": 1106, "completion_tokens": 106, "total_tokens": 1212, "prompt_tokens_details": None},
     (1106, 0, 106), (0.075, 0.0375, 0.30)),
    ("together", "deepseek-ai/DeepSeek-V4-Flash",
     {"prompt_tokens": 5000, "completion_tokens": 200, "total_tokens": 5200, "prompt_tokens_details": {"cached_tokens": 4096}},
     (904, 4096, 200), (0.14, 0.03, 0.28)),
    ("cerebras", "qwen-3.8-27b",
     {"prompt_tokens": 3000, "completion_tokens": 100, "total_tokens": 3100, "prompt_tokens_details": {"cached_tokens": 1024}},
     (1976, 1024, 100), (0.99, 0.99, 2.00)),
    ("moonshot", "kimi-k3",
     {"prompt_tokens": 10000, "completion_tokens": 50, "total_tokens": 10050, "prompt_tokens_details": {"cached_tokens": 8000}},
     (2000, 8000, 50), (3.00, 0.30, 15.00)),
]


@pytest.mark.parametrize("provider,model,usage,expected,prices", CASES)
def test_raw_usage_to_unified_usage_to_cost(provider, model, usage, expected, prices) -> None:
    inp, cached, out = expected
    p_in, p_cached, p_out = prices
    unified = _translators()[provider](_response(model, usage))
    tu = unified.usage
    assert (tu.input_tokens, tu.cached_input_tokens, tu.output_tokens) == expected
    # the provider's prompt_tokens is exactly input + cached: nothing lost, nothing doubled
    assert tu.input_tokens + tu.cached_input_tokens == usage["prompt_tokens"]
    tu.matrx_model_name = tu.provider_model_name = model
    tu.api = provider
    cost = tu.calculate_cost(_lookup(provider, model, p_in, p_cached, p_out))
    hand = (inp * p_in + cached * p_cached + out * p_out) / 1_000_000
    assert cost == pytest.approx(hand, rel=1e-9)


def test_xai_cached_prompt_text_tokens_are_split() -> None:
    usage = {"prompt_tokens": 5053, "completion_tokens": 1745, "cached_prompt_text_tokens": 1152}
    assert openai_compatible_usage_counts(usage) == (5053 - 1152, 1745, 1152)
