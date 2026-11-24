"""A version id in ``ctx.agent_id`` is stamped as the version, with its BASE agent as ``agent_id``.

chat.user_request.agent_id (and chat.conversation.initial_agent_id) reference agent.definition. On
2026-11-19 three phone calls ran a mandate whose Holder is a pinned agent.definition_version; the
version id reached ``ctx.agent_id``, the user_request insert failed ``cx_user_request_agent_fk`` and
every write of each turn was lost. The write point now settles the pair itself, so no caller can.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from matrx_ai.db import conversation_gate as gate
from matrx_ai.db import persistence

BASE = "992095cc-0019-4672-80be-f7544a29b0a2"
VERSION = "dea88565-8662-4621-96e5-b07d6160cb6b"


class _Versions:
    """``DefinitionVersion`` with exactly one row: VERSION, owned by BASE."""

    def filter(self, *, id__in):
        rows = [SimpleNamespace(id=VERSION, agent_id=BASE)] if VERSION in id__in else []
        return SimpleNamespace(all=AsyncMock(return_value=rows))


def _wire(monkeypatch, *, agent_id, agent_version_id):
    import matrx_ai.context.app_context as contexts
    import matrx_ai.db._registry as registry

    persistence._VERSION_BASE.clear()
    monkeypatch.setattr(registry, "has_requirements", lambda **_k: True)
    monkeypatch.setattr(registry, "get_model", lambda name: _Versions())
    ctx = SimpleNamespace(
        metadata={},
        source_app="aidream",
        source_feature="voice.phone_line",
        organization_id="33333333-3333-4333-8333-333333333333",
        agent_id=agent_id,
        agent_version_id=agent_version_id,
    )
    monkeypatch.setattr(contexts, "try_get_app_context", lambda: ctx)
    monkeypatch.setattr(gate, "_store_pending_user_request", AsyncMock(return_value=False))
    monkeypatch.setattr(gate, "_stamp_origin", lambda *a, **k: None)
    monkeypatch.setattr(gate, "_stamp_attribution", lambda *a, **k: None)
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
@pytest.mark.parametrize("version_slot", [VERSION, None], ids=["both-stamped", "agent-id-only"])
async def test_a_version_id_in_agent_id_persists_the_base_agent(monkeypatch, door, version_slot):
    captured = _wire(monkeypatch, agent_id=VERSION, agent_version_id=version_slot)
    await _reserve(door)
    assert len(captured) == 1
    assert captured[0]["agent_id"] == BASE
    assert captured[0]["agent_version_id"] == VERSION


@pytest.mark.asyncio
@pytest.mark.parametrize("door", ["pending", "ensured"])
async def test_a_pinned_run_gets_its_base_agent_and_a_floating_run_is_untouched(monkeypatch, door):
    captured = _wire(monkeypatch, agent_id=None, agent_version_id=VERSION)
    await _reserve(door)
    assert captured[0]["agent_id"] == BASE
    assert captured[0]["agent_version_id"] == VERSION

    captured = _wire(monkeypatch, agent_id=BASE, agent_version_id=None)
    await _reserve(door)
    assert captured[0]["agent_id"] == BASE
    assert "agent_version_id" not in captured[0]
