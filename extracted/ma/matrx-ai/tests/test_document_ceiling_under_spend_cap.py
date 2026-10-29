"""THE DOCUMENT CEILING UNDER A PER-CALL SPEND CAP — both money rules hold at once.

Live 2026-10-27, run ``a880bc2e`` (AI-visibility V3 ``who_buys``): the step carried
``max_output_tokens: 20000`` and ``max_call_cost_usd: 0.15``. Its output schema has an array,
so the send boundary's document-ceiling floor raised the ceiling to the model maximum (128,000)
on the rationale "raising a ceiling is free" — and the per-call cap, asked AFTER the boundary,
priced the call at that ceiling. On Gemini Flash ($0.75/M in, $3.75/M out) 128,000 out is about
$0.48, so every list-shaped Flash step of the panel would be refused at its $0.15 cap.

The rule now: with a cap open, the raise goes only as far as the cap affords, never below the
author's own limit; an unaffordable author limit is sent as authored and the cap refuses it
before anything is spent. No cap: exactly as before.

Forcing: every case runs the REAL ``prepare_for_send`` and the REAL ``admit_call_spend_cap``
over the same config; only the model catalog, the context window and the price table (Flash
rates) are replaced. On the pre-fix boundary the capped case goes out at 128,000 and the cap
refuses it — ``test_a_capped_flash_list_call_is_raised_only_as_far_as_the_cap_affords`` fails.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.catalog import resolve as catalog_resolve
from matrx_ai.config import context_preflight, output_ceiling, usage_config
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send, reset_loop_state
from matrx_ai.providers import guardrail_gate as gg

CONVERSATION_ID = "conv-who-buys"
REQUEST_ID = "a880bc2e-0000-4000-8000-000000000001"
FLASH = "gemini-3.8-flash"
FLASH_MAX = 128_000
#: ``ai.model_definition.id`` of gemini-3.8-flash: what ``config.model`` carries at the boundary.
FLASH_ID = "b32f2079-4fa5-4613-a01d-726f1243ebe5"
AUTHORED = 20_000
IN_PER_TOKEN = 0.75 / 1e6
OUT_PER_TOKEN = 3.75 / 1e6

LIST_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "buyers": {
            "type": "array",
            "items": {"type": "object", "properties": {"who": {"type": "string"}}},
        }
    },
}


def _config(
    *, ceiling: int = AUTHORED, prompt_chars: int = 40_000, model: str = FLASH
) -> SimpleNamespace:
    return SimpleNamespace(
        model=model,
        matrx_model_name=model,
        messages=[{"role": "user", "content": "Who buys this?"}],
        system_instruction="x" * prompt_chars,
        tools=[],
        prompt_cache_key=None,
        max_output_tokens=ceiling,
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "who_buys", "schema": LIST_SCHEMA, "strict": True},
        },
    )


async def _send(config: SimpleNamespace) -> Any:
    return await prepare_for_send(
        config,
        stage=STAGE_LOOP,
        conversation_id=CONVERSATION_ID,
        request_id=REQUEST_ID,
        iteration=1,
    )


@pytest.fixture(autouse=True)
def _catalog(monkeypatch):
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)
    monkeypatch.setattr(context_preflight, "_declared_window", lambda _ref: None)

    async def _model_max(name: Any) -> int | None:
        return FLASH_MAX if str(name) in (FLASH, FLASH_ID) else None

    monkeypatch.setattr(output_ceiling, "model_output_maximum", _model_max)

    def cost(self: Any, _lookup: Any = None, _at: Any = None) -> float | None:
        # Prices are keyed by the catalog NAME (or offering), never the model's catalog id.
        if self.matrx_model_name != FLASH:
            return None
        return self.input_tokens * IN_PER_TOKEN + self.output_tokens * OUT_PER_TOKEN

    async def _profile(model: str, **_kw: Any) -> Any:
        # The catalog resolves both the name and the catalog id to the one route.
        if model in (FLASH, FLASH_ID):
            return SimpleNamespace(model_name=FLASH, offering_id="")
        raise LookupError(model)

    monkeypatch.setattr(catalog_resolve, "resolve_call_profile", _profile)

    monkeypatch.setattr(usage_config.TokenUsage, "calculate_catalog_cost", cost)
    monkeypatch.setattr(usage_config, "_get_db_pricing_lookup", lambda: {})
    yield
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)


def _usd(config: Any) -> float:
    usd = gg.estimate_call_usd(None, config)[0]
    assert usd is not None
    return usd


@pytest.mark.asyncio
async def test_a_capped_flash_list_call_is_raised_only_as_far_as_the_cap_affords() -> None:
    config = _config()
    with gg.call_spend_cap_scope(0.15, subject="Step who_buys"):
        prep = await _send(config)
        sent = config.max_output_tokens
        # Above the author's limit (the document rule), below the model max (the money rule)…
        assert AUTHORED < sent < FLASH_MAX
        # …and the cap admits it: nothing refused.
        gg.admit_call_spend_cap(None, config)
    assert "document_output_ceiling" in prep.steps
    assert _usd(config) <= 0.15
    # It uses what the cap affords, not a token less than a percent or two of headroom.
    assert _usd(config) >= 0.15 * 0.95


@pytest.mark.asyncio
async def test_an_uncapped_call_still_goes_to_the_model_maximum() -> None:
    config = _config()
    prep = await _send(config)
    assert config.max_output_tokens == FLASH_MAX
    assert "document_output_ceiling" in prep.steps


@pytest.mark.asyncio
async def test_a_cap_that_affords_the_maximum_takes_it() -> None:
    config = _config()
    with gg.call_spend_cap_scope(1.00, subject="Step who_buys"):
        await _send(config)
        gg.admit_call_spend_cap(None, config)
    assert config.max_output_tokens == FLASH_MAX


@pytest.mark.asyncio
async def test_an_unaffordable_author_limit_is_refused_before_anything_is_sent() -> None:
    """20,000 out alone is $0.075 on Flash: over a $0.05 cap. The author's limit goes out
    as authored (never lowered below it) and the cap refuses it — nothing dispatched."""
    config = _config()
    dispatched: list[Any] = []
    with gg.call_spend_cap_scope(0.05, subject="Step who_buys"):
        await _send(config)
        assert config.max_output_tokens == AUTHORED
        with pytest.raises(gg.GuardrailStopError, match="Nothing was sent or charged") as refused:
            gg.admit_guardrails(None, config)
            dispatched.append(config)  # the provider call would follow the gate
    assert refused.value.kind == gg.CALL_SPEND_CAP
    assert dispatched == []


@pytest.mark.asyncio
async def test_later_rounds_bound_from_the_authors_limit_not_the_last_round() -> None:
    """A tool loop's prompt grows; each round re-bounds from the AUTHOR's 20,000, so a round
    never inherits the previous bounded number as its floor (which would refuse it)."""
    config = _config()
    with gg.call_spend_cap_scope(0.15, subject="Step who_buys"):
        await _send(config)
        first = config.max_output_tokens
        config.system_instruction = "x" * 120_000  # tool results arrived
        await _send(config)
        second = config.max_output_tokens
        gg.admit_call_spend_cap(None, config)
    assert AUTHORED < second < first


class _RecordingEmitter:
    def __init__(self) -> None:
        self.warnings: list[Any] = []

    async def send_warning(self, payload: Any) -> None:
        self.warnings.append(payload)


@pytest.mark.asyncio
async def test_the_bound_is_announced_naming_the_cap(monkeypatch) -> None:
    import asyncio

    import matrx_connect

    rec = _RecordingEmitter()
    monkeypatch.setattr(matrx_connect, "get_app_context", lambda: SimpleNamespace(emitter=rec))
    config = _config()
    with gg.call_spend_cap_scope(0.15, subject="Step who_buys"):
        await _send(config)
    for _ in range(5):
        await asyncio.sleep(0)
    assert len(rec.warnings) == 1
    warning = rec.warnings[0]
    assert warning.metadata["adjusted"] == [
        {"key": "max_output_tokens", "requested": AUTHORED, "sent": config.max_output_tokens}
    ]
    assert "bounded by the $0.15 cap" in warning.user_message
    assert "bounded by the $0.15 per-call cap" in warning.system_message
    assert len(warning.user_message) <= 140


@pytest.mark.asyncio
async def test_a_call_named_by_its_catalog_id_is_priced_through_its_profile() -> None:
    """Live 2026-10-28 (run c91d63b3): ``config.model`` was the model's catalog id, which no
    price is keyed by, so the bound fell back to the author's 20,000 on a call the cap could
    afford at the maximum. The bound prices the profile the provider call resolves."""
    config = _config(model=FLASH_ID)
    with gg.call_spend_cap_scope(0.15, subject="Step who_buys"):
        await _send(config)
    assert AUTHORED < config.max_output_tokens < FLASH_MAX
