"""The first Anthropic call streams whenever the SDK would refuse a non-streaming send.

The SDK refuses with "Streaming is required..." when 3600*max_tokens/128000 > 600 s OR when max_tokens exceeds a
per-model ceiling (MODEL_NONSTREAMING_TOKENS, e.g. 8192 for claude-opus-4). The provider decides to stream BEFORE
the first call, from the SDK's own rule, so the refusal never happens. A decision that nothing failed on is not an
issue (ops class anthropic.streaming_required collected ~6,800 recovered events that were this decision).
"""

from __future__ import annotations

import pytest
from anthropic._constants import MODEL_NONSTREAMING_TOKENS
from matrx_utils.source_guard import stable_source

from matrx_ai.providers.anthropic import anthropic_api


def _must_stream(model: str, max_tokens: int) -> bool:
    return anthropic_api.anthropic_requires_streaming(model, max_tokens)


def test_the_general_ten_minute_ceiling_streams() -> None:
    assert _must_stream("claude-sonnet-4-5", 21_334)
    assert not _must_stream("claude-sonnet-4-5", 21_333)


@pytest.mark.parametrize("model", sorted(MODEL_NONSTREAMING_TOKENS))
def test_a_model_with_a_lower_sdk_ceiling_streams_above_it(model: str) -> None:
    ceiling = MODEL_NONSTREAMING_TOKENS[model]
    assert _must_stream(model, ceiling + 1)
    assert not _must_stream(model, ceiling)


def test_the_decision_agrees_with_the_sdk_itself() -> None:
    from anthropic import AsyncAnthropic

    client = AsyncAnthropic(api_key="test")
    for model, max_tokens in [("claude-opus-4-0", 9_000), ("claude-sonnet-4-5", 30_000), ("claude-sonnet-4-5", 8_000)]:
        try:
            client._calculate_nonstreaming_timeout(max_tokens, MODEL_NONSTREAMING_TOKENS.get(model))
            sdk_refuses = False
        except ValueError:
            sdk_refuses = True
        assert _must_stream(model, max_tokens) is sdk_refuses


def test_the_proactive_stream_files_no_issue() -> None:
    src = stable_source(anthropic_api.AnthropicChat)
    assert '"anthropic.streaming_required"' not in src
