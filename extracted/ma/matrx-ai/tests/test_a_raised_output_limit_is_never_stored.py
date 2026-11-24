"""A RAISED OUTPUT LIMIT RIDES THE WIRE, NEVER THE CHAT (CGU-10 IMG5 finding 8, 2026-11-11).

Live: a reasoning model's answer reserve raised ``max_output_tokens`` 1,500 → 2,250 on the
CANONICAL config, the conversation stored it, and the next turn raised again from the stored value
(2,250 → 3,375; ten turns pass 85,000), even with ``model_this_turn_only``. The boundary now keeps
every per-call raise on ``prep.wire_config`` and puts the author's values back on the canonical
config before it returns.

Forcing: three TURNS (three requests, each its own request id, the same canonical config object
standing in for the stored conversation config) through the REAL ``prepare_for_send``. On the
pre-fix boundary the canonical config leaves turn 1 at 2,250 and turn 2 sends 3,375.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from test_thinking_leaves_room_for_the_answer import _config, _controls

from matrx_ai.catalog import resolve as catalog_resolve
from matrx_ai.config import context_preflight
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send, reset_loop_state
from matrx_ai.knobs import configure_package_knobs

CONVERSATION_ID = "conv-raised-limit-never-stored"
REQUESTS = [f"img5-8-turn-{n}" for n in (1, 2, 3)]


@pytest.fixture(autouse=True)
def _catalog(monkeypatch):
    for rid in REQUESTS:
        reset_loop_state(CONVERSATION_ID, rid)
    configure_package_knobs(None)
    monkeypatch.setattr(context_preflight, "_declared_window", lambda _ref: None)

    async def _profile(model: str, **_kw: Any) -> Any:
        return SimpleNamespace(model_name=model, offering_id="", controls=_controls(model))

    monkeypatch.setattr(catalog_resolve, "resolve_call_profile", _profile)
    yield
    for rid in REQUESTS:
        reset_loop_state(CONVERSATION_ID, rid)


@pytest.mark.asyncio
@pytest.mark.parametrize("model", ["claude-haiku-5-5", "gpt-5.5", "gemini-3.8-flash"])
async def test_three_reasoning_turns_send_the_same_raise_and_store_the_authored_limit(model: str) -> None:
    stored = _config(model, effort="medium" if model == "gpt-5.5" else None)
    sent: list[int] = []
    for rid in REQUESTS:
        prep = await prepare_for_send(
            stored, stage=STAGE_LOOP, conversation_id=CONVERSATION_ID, request_id=rid, iteration=1
        )
        assert prep.wire_config is not None and prep.wire_config is not stored
        sent.append(prep.wire_config.max_output_tokens)
        assert stored.max_output_tokens == 1500, f"turn {rid} stored the raised limit"
    assert sent == [2250, 2250, 2250]


@pytest.mark.asyncio
async def test_a_clamped_thinking_budget_is_not_stored_either() -> None:
    stored = _config("gemini-2.5-flash", effort="low")
    stored.thinking_budget = 1024
    for rid in REQUESTS:
        prep = await prepare_for_send(
            stored, stage=STAGE_LOOP, conversation_id=CONVERSATION_ID, request_id=rid, iteration=1
        )
        assert prep.wire_config.thinking_budget == 750
        assert stored.thinking_budget == 1024


@pytest.mark.asyncio
async def test_a_refused_send_still_gives_the_author_their_limit_back(monkeypatch) -> None:
    from matrx_ai.config import request_firewall

    def _refuse(_config: Any) -> None:
        raise RuntimeError("refused at the firewall")

    monkeypatch.setattr(request_firewall, "check_at_send", _refuse)
    stored = _config("claude-haiku-5-5")
    with pytest.raises(RuntimeError):
        await prepare_for_send(
            stored, stage=STAGE_LOOP, conversation_id=CONVERSATION_ID, request_id=REQUESTS[0], iteration=1
        )
    assert stored.max_output_tokens == 1500
