"""A paid call is priced: every routable offering carries a price or a recorded reason, and a turn
is never priced against a cold pricing lookup.

2026-10-26 census (CX Explorer "cost empty"): five GLiNER2 offerings held placeholder prices, a free
Gemma offering read as nothing, and one hour on 2026-10-15 saved Anthropic, Google, OpenAI and Groq
calls with cost NULL although their prices existed — the turn was priced before the process's
pricing lookup had loaded. The validator (catalog layer) and ``persist_completed_request`` (write
layer) each stop one half; ``scripts/check_paid_calls_are_priced_live.py`` reads the result live.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.config.usage_config import validate_model_pricing
from matrx_utils.source_guard import stable_source

TEXT = SimpleNamespace(produces_image=False, produces_video=False, produces_audio=False,
                       supports_audio_input=False, supports_text_input=True)
ZERO = [{"max_tokens": None, "input_price": 0, "output_price": 0, "cached_input_price": 0}]
PRICED = [{"max_tokens": None, "input_price": 0.15, "output_price": 0.15}]


def _codes(pricing, **kw) -> dict[str, str]:
    return {i.code: i.severity for i in validate_model_pricing(
        "m", "x", TEXT, pricing, token_billed=True, routable=True, **kw)}


@pytest.mark.parametrize("pricing,code", [([], "no_pricing"), (None, "no_pricing"), (ZERO, "zero_pricing")])
def test_a_routable_offering_with_no_real_price_is_an_error(pricing, code):
    assert _codes(pricing) == {code: "error"}


def test_a_priced_offering_passes():
    assert _codes(PRICED) == {}


def test_a_recorded_free_reason_makes_zero_the_truth():
    assert _codes(ZERO, free_reason="Gemini API serves Gemma free of charge") == {}


def test_an_unpublished_price_is_a_warning_not_a_silent_zero():
    assert _codes([], price_unpublished="Groq publishes no rate") == {"price_unpublished": "warning"}


def test_a_model_with_no_offering_is_not_held_to_the_offering_rule():
    issues = validate_model_pricing("m", "x", TEXT, [], token_billed=False, routable=False)
    assert issues == []


class _Priced(Exception):
    pass


def _completed(order: list[str]):
    def to_storage_dict():
        order.append("priced")
        raise _Priced

    return SimpleNamespace(to_storage_dict=to_storage_dict,
                           request=SimpleNamespace(conversation_id="c1", request_id="r1"))


@pytest.mark.asyncio
async def test_a_turn_is_priced_only_after_the_pricing_lookup_loaded(monkeypatch):
    import matrx_ai.config.usage_config as usage_config
    import matrx_ai.db.persistence as persistence

    order: list[str] = []

    async def warm():
        order.append("warmed")
        return {}

    monkeypatch.setattr(persistence, "_get_live_coordinator", lambda: object())
    monkeypatch.setattr(usage_config, "ensure_pricing_lookup", warm)
    monkeypatch.setattr(usage_config, "is_pricing_lookup_warm", lambda: True)
    with pytest.raises(_Priced):
        await persistence.persist_completed_request(_completed(order), conversation_id="c1")
    assert order == ["warmed", "priced"]


@pytest.mark.asyncio
async def test_a_turn_priced_without_a_lookup_is_recorded_loudly(monkeypatch):
    import matrx_connect.streaming.error_capture as streaming

    import matrx_ai.config.usage_config as usage_config
    import matrx_ai.db.persistence as persistence

    captured: list[str] = []

    async def warm():
        return {}

    async def capture(exc, *, kind, **fields):
        captured.append(kind)

    monkeypatch.setattr(persistence, "_get_live_coordinator", lambda: object())
    monkeypatch.setattr(usage_config, "ensure_pricing_lookup", warm)
    monkeypatch.setattr(usage_config, "is_pricing_lookup_warm", lambda: False)
    monkeypatch.setattr(streaming, "capture_error", capture)
    with pytest.raises(_Priced):
        await persistence.persist_completed_request(_completed([]), conversation_id="c1")
    assert captured == ["pricing_lookup_cold_at_persist"]


def test_an_extraction_turn_estimates_the_usage_its_provider_never_reports():
    """Fastino reports no usage; a reported 0 billed every GLiNER2 call at $0 behind a real price."""
    from matrx_ai.providers import unified_client

    source = stable_source(unified_client.UnifiedAIClient)
    assert "input_tokens=0,\n            output_tokens=0" not in source
    assert unified_client._EXTRACTION_CHARS_PER_TOKEN == 4
    assert "usage_estimated" in source
