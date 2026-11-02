from __future__ import annotations

from matrx_rag._observability import (
    _MISSING_PRICE_ALARM_KEYS,
    _embedding_cost_from_tokens,
    _embedding_cost_usd,
)


def setup_function() -> None:
    _MISSING_PRICE_ALARM_KEYS.clear()


def test_voyage_4_large_exact_cost_from_provider_tokens() -> None:
    cost = _embedding_cost_from_tokens(
        "voyage-4-large",
        780,
        context="test",
    )
    assert cost == 780 * 0.12 / 1_000_000.0


def test_missing_embedding_price_returns_none_and_alarms_once() -> None:
    model = "totally-unknown-embedding-model"
    assert _embedding_cost_from_tokens(model, 100, context="test") is None
    assert _embedding_cost_usd(model, 400, context="test") is None
    assert ("embedding", model) in _MISSING_PRICE_ALARM_KEYS
    before = len(_MISSING_PRICE_ALARM_KEYS)
    assert _embedding_cost_from_tokens(model, 200, context="test") is None
    assert len(_MISSING_PRICE_ALARM_KEYS) == before
