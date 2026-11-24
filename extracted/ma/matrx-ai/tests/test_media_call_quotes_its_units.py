"""A per-image / per-second / per-character call is priced from its units before it is sent (cost adversary pass 5, F3).

Before: ``quote_call`` returned None for any synthetic usage basis, and the dispatch read a route's history only when
the call carried NO config, so a media call (which always carries one) reserved the host's flat unpriced amount ($3)
whatever it asked for: a $8 video was admitted into $4 of room and the run ended at $9 under a $5 cap.

Now: the request's units (images = ``count``, clips, tracks, seconds = ``duration_seconds`` x ``count``, characters of
the text sent) x the catalog's unit price, config or not; a request that does not say its units (no duration)
answers None and the dispatch falls back to the route's recorded calls (``quote_for_dispatch``).

SUT: ``guardrail_gate.quote_call`` and ``guardrail_gate.quote_for_dispatch``. Doubles: the catalog lookup (one tier),
the prompt estimate, the guarded-run read and the route-history host hook."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace as NS
from typing import Any

import pytest

from matrx_ai.config import context_preflight, usage_config
from matrx_ai.providers import guardrail_gate as gg

PROFILE = NS(model_name="media-x", controls=None, offering_id="", provider_model_id="", vendor="")


@pytest.fixture
def tier(monkeypatch):
    holder: dict[str, Any] = {}

    def set_tier(basis: str | None, input_price: float, output_price: float) -> None:
        holder["tier"] = NS(usage_basis=basis, input_price=input_price, output_price=output_price,
                            cache_write_5m_price=None, cache_hit_price=None, cached_input_price=None)

    monkeypatch.setattr(usage_config, "lookup_model_pricing", lambda *a, **k: NS(get_tier=lambda _u: holder["tier"]))
    monkeypatch.setattr(usage_config, "_get_db_pricing_lookup", lambda: None)
    monkeypatch.setattr(context_preflight, "estimate_prompt_tokens", lambda _c: 40)
    return set_tier


def _config(**kw: Any) -> Any:
    base = {"count": 1, "duration_seconds": None, "max_output_tokens": None, "messages": [], "system_instruction": None}
    return NS(**{**base, **kw})


def test_a_video_priced_per_second_reserves_its_seconds(tier) -> None:
    tier("video_second_output", 0.0, 0.50)
    quote = gg.quote_call(PROFILE, _config(duration_seconds=16))
    assert quote is not None and abs(quote.worst_usd(0) - 8.0) < 1e-9


def test_images_priced_per_image_reserve_their_count(tier) -> None:
    tier("image_output", 0.0, 0.04)
    quote = gg.quote_call(PROFILE, _config(count=4))
    assert quote is not None and abs(quote.worst_usd(0) - 0.16) < 1e-9


def test_a_clip_priced_per_clip_reserves_one_clip_each(tier) -> None:
    tier("video_unit_output", 0.0, 1.20)
    quote = gg.quote_call(PROFILE, _config(count=2))
    assert quote is not None and abs(quote.worst_usd(0) - 2.40) < 1e-9


def test_speech_priced_per_character_reserves_the_characters_sent(tier) -> None:
    tier("character_input", 30.0, 0.0)  # $30 / 1M characters
    message = NS(content=[NS(text="a" * 10_000)])
    quote = gg.quote_call(PROFILE, _config(messages=[message]))
    assert quote is not None and abs(quote.worst_usd(0) - 0.30) < 1e-9


def test_a_per_second_call_that_names_no_duration_cannot_be_priced_from_its_request(tier) -> None:
    tier("video_second_output", 0.0, 0.50)
    assert gg.quote_call(PROFILE, _config()) is None


def test_a_token_call_still_prices_from_its_tokens(tier) -> None:
    tier(None, 3.0, 15.0)
    quote = gg.quote_call(PROFILE, _config(max_output_tokens=1000))
    assert quote is not None and abs(quote.worst_usd(0) - (40 * 3.0 + 1000 * 15.0) / 1e6) < 1e-12


def _guarded(monkeypatch, history: float | None) -> None:
    async def route_worst(_profile: Any) -> float | None:
        return history

    monkeypatch.setattr(gg, "_budget_reserve", lambda ctx, quote: None)
    monkeypatch.setattr(gg, "_is_guarded", lambda ctx: True)
    monkeypatch.setattr(gg, "_route_worst", route_worst)
    from matrx_ai.providers import usage_gate

    monkeypatch.setattr(usage_gate, "costs_nothing_on_a_device", lambda _p: False)


def test_the_dispatch_hands_a_media_call_with_a_config_its_unit_quote(tier, monkeypatch) -> None:
    tier("video_second_output", 0.0, 0.50)
    _guarded(monkeypatch, history=None)
    quote = asyncio.run(gg.quote_for_dispatch(PROFILE, _config(duration_seconds=16), None))
    assert quote is not None and abs(quote.worst_usd(0) - 8.0) < 1e-9, "the $8 video must reserve $8, not the flat $3"


def test_a_call_with_a_config_it_cannot_price_uses_its_routes_history(tier, monkeypatch) -> None:
    tier("video_second_output", 0.0, 0.50)
    _guarded(monkeypatch, history=6.5)
    quote = asyncio.run(gg.quote_for_dispatch(PROFILE, _config(), None))
    assert quote is not None and abs(quote.worst_usd(0) - 6.5) < 1e-9


def test_a_callers_own_quote_wins(tier, monkeypatch) -> None:
    _guarded(monkeypatch, history=6.5)
    own = gg.fixed_quote("media-x", 0.25)
    assert asyncio.run(gg.quote_for_dispatch(PROFILE, _config(), own)) is own
