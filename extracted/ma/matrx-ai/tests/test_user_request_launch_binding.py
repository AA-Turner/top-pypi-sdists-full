"""A run started from a surface binding's Run door records that binding on its request row.

The host checks the binding (exists, in the caller's reach) and carries its id on
``AppContext.metadata[LAUNCH_BINDING_ID_KEY]``; both reservation doors stamp it into
``chat.user_request.binding_id``. A malformed id is dropped, never written to the uuid column.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from matrx_ai.db import conversation_gate as gate

BINDING = "66666666-6666-4666-8666-666666666666"


def _wire(monkeypatch, metadata):
    import matrx_ai.context.app_context as contexts

    ctx = SimpleNamespace(
        metadata=metadata,
        source_app="matrx-frontend",
        source_feature="ai-results",
        organization_id="33333333-3333-4333-8333-333333333333",
    )
    monkeypatch.setattr(contexts, "try_get_app_context", lambda: ctx)
    monkeypatch.setattr(gate, "_store_pending_user_request", AsyncMock(return_value=False))
    monkeypatch.setattr(gate, "_stamp_origin", lambda *a, **k: None)
    monkeypatch.setattr(gate, "_stamp_attribution", lambda *a, **k: None)
    monkeypatch.setattr(gate, "_stamp_agent_refs", lambda *a, **k: None)
    monkeypatch.setattr(gate, "try_get_tracker", lambda: None)
    captured: list[dict] = []
    manager = SimpleNamespace(
        filter_user_requests=AsyncMock(return_value=[]),
        create_user_request=AsyncMock(side_effect=lambda **kwargs: captured.append(kwargs)),
    )
    monkeypatch.setattr(gate, "_cxm", lambda: SimpleNamespace(user_request=manager))
    monkeypatch.setattr(gate, "_get_active_lane_coordinator", lambda: object())
    monkeypatch.setattr(gate, "_queue_user_request_create", lambda **kwargs: captured.append(kwargs))
    return captured


async def _reserve(door: str) -> None:
    request_id = "44444444-4444-4444-8444-444444444444"
    actor = "55555555-5555-4555-8555-555555555555"
    if door == "pending":
        await gate.create_pending_user_request(request_id, actor)
    else:
        await gate._create_user_request(request_id=request_id, user_id=actor)


@pytest.mark.asyncio
@pytest.mark.parametrize("door", ["pending", "ensured"])
async def test_both_reservation_doors_stamp_the_launch_binding(monkeypatch, door):
    captured = _wire(monkeypatch, {gate.LAUNCH_BINDING_ID_KEY: BINDING})
    await _reserve(door)
    assert len(captured) == 1
    assert captured[0]["binding_id"] == BINDING


@pytest.mark.asyncio
@pytest.mark.parametrize("door", ["pending", "ensured"])
async def test_no_binding_and_a_malformed_binding_leave_the_column_unset(monkeypatch, door):
    captured = _wire(monkeypatch, {})
    await _reserve(door)
    assert "binding_id" not in captured[0]

    captured = _wire(monkeypatch, {gate.LAUNCH_BINDING_ID_KEY: "not-a-uuid"})
    await _reserve(door)
    assert "binding_id" not in captured[0]
