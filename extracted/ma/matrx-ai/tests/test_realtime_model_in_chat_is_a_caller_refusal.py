"""A realtime / embedding model asked to answer a typed turn is a CALLER REFUSAL, never a crash.

THE RECORDED FAILURE, 2026-11-12 23:09 UTC (system_error e8dba7a9): a matrx-ios chat opened an
agent bound to ``gemini-3.8-live`` (a live voice model, interaction ``realtime``). The dispatch
seam raised a plain ``ValueError``; the executor classified it ``invalid_request`` and filed a
``system_error`` for what is the agent's own setting, with no sentence a person could act on.

WHAT EACH TEST CATCHES:

* the seam raises a plain ``ValueError`` again (or drops ``is_caller_refusal`` / its
  non-retryable ``error_info``) — ``test_the_seam_refuses_a_realtime_model_by_name`` goes red;
* the refusal code leaves the ONE registry, so a retry loop retries it —
  ``test_the_refusal_code_is_final``;
* a turn model is refused too (the gate over-fires) — ``test_a_turn_model_passes_the_channel_gate``.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

import matrx_ai.catalog.resolve as resolve_mod
from matrx_ai.providers.caller_refusal import caller_refusal_codes, is_caller_refusal
from matrx_ai.providers.model_channel_gate import MODEL_NOT_FOR_CHAT, ModelNotForChatError
from matrx_ai.providers.unified_client import UnifiedAIClient


class _PastTheGate(Exception):
    pass


def _stub_seam(monkeypatch: pytest.MonkeyPatch, *, interaction: str, wire_format: str, client_attr: str) -> None:
    async def _none(*_a: Any, **_k: Any) -> Any:
        return None

    async def _false(*_a: Any, **_k: Any) -> bool:
        return False

    async def _resolve(model: str, *_a: Any, **_k: Any) -> Any:
        return SimpleNamespace(
            model_name=model,
            model_cost_rating=1,
            wire_format=wire_format,
            client_attr=client_attr,
            vendor="google",
            provider_model_id=model,
            capabilities=SimpleNamespace(
                interaction=interaction, supports_vision=True, structured_output_mode=None
            ),
        )

    monkeypatch.setattr("matrx_ai.providers.child_safety_gate.admit_child_safety", _none)
    monkeypatch.setattr("matrx_ai.providers.free_tier_models.swap_for_free_tier", _false)
    monkeypatch.setattr("matrx_ai.providers.baa_gate.swap_for_baa", _false)
    monkeypatch.setattr("matrx_ai.providers.baa_gate.apply_baa_features", _none)
    monkeypatch.setattr(resolve_mod, "resolve_tts_call_profile", _resolve)

    def _past(*_a: Any, **_k: Any) -> None:
        raise _PastTheGate

    monkeypatch.setattr(
        "matrx_ai.providers.unified_client._enforce_required_native_document_input",
        lambda *_a, **_k: None,
    )
    # The first step after the channel gate: reaching it means the gate admitted the model.
    monkeypatch.setattr("matrx_ai.decisions.translate.prepare_verbalized_decision", _past)


def _request(model: str) -> Any:
    config = SimpleNamespace(
        model=model, offering_id=None, runtime_offering_id=None, routing_offering_id=None,
        tts_quality=None, metadata={}, messages=[],
    )
    return SimpleNamespace(config=config, debug=False)


@pytest.mark.asyncio
async def test_the_seam_refuses_a_realtime_model_by_name(monkeypatch: pytest.MonkeyPatch) -> None:
    _stub_seam(monkeypatch, interaction="realtime", wire_format="google_live", client_attr="realtime")
    client = UnifiedAIClient.__new__(UnifiedAIClient)
    with pytest.raises(ModelNotForChatError) as err:
        await client._execute_dispatch(_request("gemini-3.8-live"))  # type: ignore[arg-type]
    exc = err.value
    assert isinstance(exc, ValueError)  # old `except ValueError` callers still catch it
    assert is_caller_refusal(exc)
    assert exc.error_info.error_type == MODEL_NOT_FOR_CHAT
    assert exc.error_info.is_retryable is False
    assert "gemini-3.8-live" not in exc.error_info.user_message
    assert "gemini-3.8-live" in exc.error_info.message
    assert "live voice model" in exc.error_info.user_message


@pytest.mark.asyncio
async def test_a_turn_model_passes_the_channel_gate(monkeypatch: pytest.MonkeyPatch) -> None:
    _stub_seam(monkeypatch, interaction="turn", wire_format="google", client_attr="google")
    client = UnifiedAIClient.__new__(UnifiedAIClient)
    with pytest.raises(_PastTheGate):
        await client._execute_dispatch(_request("gemini-3-flash"))  # type: ignore[arg-type]


def test_the_refusal_code_is_final() -> None:
    assert MODEL_NOT_FOR_CHAT in caller_refusal_codes()
    assert is_caller_refusal(MODEL_NOT_FOR_CHAT)


@pytest.mark.asyncio
async def test_a_rerank_model_is_refused_not_read_as_a_chat_model(monkeypatch: pytest.MonkeyPatch) -> None:
    """THE RECORDED FAILURE, 2026-11-18 09:10 UTC: ``rerank-v4.0-pro`` was catalogued with
    interaction ``rerank``, a mode neither vocabulary named. The resolver read it as ``turn``,
    so the chat seam admitted a reranker as a chat model, and every admin model page filed a
    ``data-shape`` error. The capabilities below are the live row's, resolved for real."""
    from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities

    row = SimpleNamespace(
        name="rerank-v4.0-pro",
        capabilities={"input": ["text"], "output": [], "features": [], "interaction": "rerank", "multilingual": True},
    )
    interaction = resolve_model_capabilities(row).interaction
    assert interaction == "rerank"
    _stub_seam(monkeypatch, interaction=interaction, wire_format="cohere", client_attr="cohere")
    client = UnifiedAIClient.__new__(UnifiedAIClient)
    with pytest.raises(ModelNotForChatError) as err:
        await client._execute_dispatch(_request("rerank-v4.0-pro"))  # type: ignore[arg-type]
    assert err.value.channel == "rerank"
    assert "reranking model" in err.value.error_info.user_message
