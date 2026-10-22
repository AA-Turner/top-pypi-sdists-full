"""Handoff must find the call's work even when the turn never completes."""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from matrx_ai.db import conversation_gate as gate
from matrx_ai.db import persistence

VOICE = {
    "voice_session_id": "11111111-1111-4111-8111-111111111111",
    "voice_interaction_id": "22222222-2222-4222-8222-222222222222",
    "voice_provider_call_id": "CA" + "1" * 32,
}


@pytest.mark.asyncio
@pytest.mark.parametrize("door", ["pending", "ensured"])
async def test_both_reservation_doors_keep_exact_call_identity_before_completion(monkeypatch, door):
    import matrx_ai.context.app_context as contexts

    ctx = SimpleNamespace(
        metadata={**VOICE, "private_prompt": "never copy arbitrary context"},
        source_app="aidream",
        source_feature="voice-agent",
        organization_id="33333333-3333-4333-8333-333333333333",
    )
    monkeypatch.setattr(contexts, "try_get_app_context", lambda: ctx)
    monkeypatch.setattr(gate, "_store_pending_user_request", AsyncMock(return_value=False))
    monkeypatch.setattr(gate, "_stamp_origin", lambda *a, **k: None)
    monkeypatch.setattr(gate, "_stamp_attribution", lambda *a, **k: None)
    monkeypatch.setattr(gate, "_stamp_agent_refs", lambda *a, **k: None)
    monkeypatch.setattr(gate, "try_get_tracker", lambda: None)
    captured = []
    manager = SimpleNamespace(
        filter_user_requests=AsyncMock(return_value=[]),
        create_user_request=AsyncMock(side_effect=lambda **kwargs: captured.append(kwargs)),
    )
    monkeypatch.setattr(gate, "_cxm", lambda: SimpleNamespace(user_request=manager))
    monkeypatch.setattr(gate, "_get_active_lane_coordinator", lambda: object())
    monkeypatch.setattr(
        gate, "_queue_user_request_create", lambda **kwargs: captured.append(kwargs)
    )
    request_id = "44444444-4444-4444-8444-444444444444"
    actor = "55555555-5555-4555-8555-555555555555"
    if door == "pending":
        await gate.create_pending_user_request(request_id, actor)
    else:
        await gate._create_user_request(request_id=request_id, user_id=actor)
    assert len(captured) == 1
    assert captured[0]["metadata"] == VOICE
    assert captured[0]["source_feature"] == "voice-agent"
    # Completion merges into the existing reservation; a conversation-root rewrite cannot erase call identity.
    monkeypatch.setattr(
        persistence, "_existing_row_metadata", AsyncMock(return_value=captured[0]["metadata"])
    )
    merged = await persistence.merge_into_existing_metadata(
        "user_request", request_id, {"runtime_root_execution_id": "other-root"}
    )
    assert {key: merged[key] for key in VOICE} == VOICE
    assert merged["runtime_root_execution_id"] == "other-root"


def test_non_voice_context_keeps_existing_identity_contract():
    assert gate._run_identity_metadata(
        SimpleNamespace(metadata={"workflow_node_id": "node", "unrelated": "value"})
    ) == {"workflow_node_id": "node"}
    assert gate._run_identity_metadata(None) == {}
