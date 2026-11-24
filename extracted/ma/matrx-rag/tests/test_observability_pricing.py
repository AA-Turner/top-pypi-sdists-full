"""matrx-rag prices every call through the HOST's catalog seam (``configure(model_token_cost=...)``), never a private
price list (cost adversary pass 4, 2026-11-17). No price = None + one alarm, never a silent $0."""

from __future__ import annotations

from unittest.mock import patch

from matrx_rag import _ext
from matrx_rag import _observability as obs
from matrx_rag._observability import (
    _MISSING_PRICE_ALARM_KEYS,
    _embedding_cost_from_tokens,
    _embedding_cost_usd,
)


def setup_function() -> None:
    _MISSING_PRICE_ALARM_KEYS.clear()


def _catalog(prices: dict[str, float]):
    calls: list[dict] = []

    def model_token_cost(*, model: str, input_tokens: int, output_tokens: int):
        calls.append({"model": model, "input_tokens": input_tokens, "output_tokens": output_tokens})
        price = prices.get(model)
        return None if price is None else (input_tokens + output_tokens) * price / 1_000_000.0

    return model_token_cost, calls


def test_the_package_keeps_no_price_list_of_its_own() -> None:
    names = [n for n in vars(obs) if "PRICE_PER_M_TOKENS" in n]
    assert not names, f"matrx-rag must price through the host catalog, not a private table: {names}"


def test_cost_comes_from_the_host_catalog_seam_with_the_bare_model_name() -> None:
    seam, calls = _catalog({"voyage-4-large": 0.12})
    with patch.dict(_ext._registry, {"model_token_cost": seam}):
        cost = _embedding_cost_from_tokens("voyage:voyage-4-large", 780, context="test")
    assert cost == 780 * 0.12 / 1_000_000.0
    assert calls == [{"model": "voyage-4-large", "input_tokens": 780, "output_tokens": 0}]


def test_a_model_the_catalog_cannot_price_is_none_and_alarms_once() -> None:
    seam, _ = _catalog({})
    model = "totally-unknown-embedding-model"
    with patch.dict(_ext._registry, {"model_token_cost": seam}):
        assert _embedding_cost_from_tokens(model, 100, context="test") is None
        assert _embedding_cost_usd(model, 400, context="test") is None
        assert ("embedding", model) in _MISSING_PRICE_ALARM_KEYS
        before = len(_MISSING_PRICE_ALARM_KEYS)
        assert _embedding_cost_from_tokens(model, 200, context="test") is None
        assert len(_MISSING_PRICE_ALARM_KEYS) == before


def test_no_host_seam_is_unpriced_never_free() -> None:
    registry = {k: v for k, v in _ext._registry.items() if k != "model_token_cost"}
    with patch.dict(_ext._registry, registry, clear=True):
        assert _embedding_cost_from_tokens("text-embedding-3-small", 100, context="test") is None


def test_a_raising_seam_is_unpriced_never_free() -> None:
    def broken(**_kw):
        raise RuntimeError("catalog down")

    with patch.dict(_ext._registry, {"model_token_cost": broken}):
        assert _embedding_cost_from_tokens("text-embedding-3-large", 100, context="test") is None
