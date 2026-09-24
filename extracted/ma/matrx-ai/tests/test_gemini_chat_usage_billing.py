"""Regression test for `TokenUsage.from_gemini` (chat path) dropping thinking
tokens and double-counting cached input — the same class of billing defect
fixed for the Gemini image path in 564a449822.

Recorded real Gemini chat `usage_metadata` (chat.request id
efb0ac2c-906f-4d22-90f1-8502cb481940, 2026-09-22 21:54 UTC): prompt_token_count
6576 (which INCLUDES the 3474 cached), thoughts_token_count 5160,
candidates_token_count 1029.

Before the fix: input_tokens=6576 (cached double-counted into input instead of
split out), output_tokens=1029 (thinking silently dropped, never billed).

After the fix: input_tokens=3102 (6576-3474), output_tokens=6189 (1029+5160,
thinking billed as output — mirrors the image path), cached_input_tokens=3474.
"""

from __future__ import annotations

import types

from matrx_ai.config.usage_config import TokenUsage

# Verbatim recorded usage_metadata shape (chat.request.raw_usage), reconstructed
# as the SDK-like object `from_gemini` reads (attribute access, not dict).
_RECORDED = types.SimpleNamespace(
    prompt_token_count=6576,
    cached_content_token_count=3474,
    thoughts_token_count=5160,
    candidates_token_count=1029,
)


def test_gemini_chat_thoughts_bill_as_output_and_cache_splits_out():
    usage = TokenUsage.from_gemini(
        _RECORDED, matrx_model_name="gemini-3-pro", provider_model_name="gemini-3-pro"
    )
    assert usage.input_tokens == 3102, "cached must be split out of prompt, never double-counted"
    assert usage.output_tokens == 6189, "thoughts_token_count must be billed as output"
    assert usage.cached_input_tokens == 3474


def test_gemini_chat_without_thinking_or_cache_is_unchanged():
    """No-thinking, no-cache calls must bill exactly as before (no regression)."""
    raw = types.SimpleNamespace(
        prompt_token_count=74,
        cached_content_token_count=0,
        thoughts_token_count=None,
        candidates_token_count=1477,
    )
    usage = TokenUsage.from_gemini(raw, matrx_model_name="gemini-3-pro")
    assert usage.input_tokens == 74
    assert usage.output_tokens == 1477
    assert usage.cached_input_tokens == 0
