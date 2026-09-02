from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.persistence import replay


class _ExistingModel:
    _meta = SimpleNamespace(primary_keys=("id",))
    present: set[str] = set()

    @classmethod
    async def exists(cls, **filters):
        return str(filters["id"]) in cls.present


@pytest.mark.asyncio
async def test_replay_treats_existing_insert_and_absent_delete_as_satisfied() -> None:
    from matrx_orm.session.op import make_delete, make_insert

    _ExistingModel.present = {"landed"}

    assert await replay._op_already_satisfied(
        make_insert(_ExistingModel, {"id": "landed"})
    )
    assert await replay._op_already_satisfied(
        make_delete(_ExistingModel, "already-gone")
    )
    assert not await replay._op_already_satisfied(
        make_insert(_ExistingModel, {"id": "missing"})
    )


@pytest.mark.asyncio
async def test_legacy_chat_replay_restores_actor_and_conversation_org(monkeypatch) -> None:
    class Conversation:
        @classmethod
        def filter(cls, **filters):
            assert filters == {"id": "conversation-1"}
            return cls()

        async def values(self, *fields):
            assert fields == ("organization_id", "created_by")
            return [{"organization_id": "org-1", "created_by": "conversation-owner"}]

    monkeypatch.setattr(replay, "get_model", lambda table: Conversation)
    rows = [
        {
            "table_target": "chat.user_request",
            "primary_key": {"id": "user-request-1"},
            "payload": {
                "id": "user-request-1",
                "user_id": "request-actor",
                "status": "pending",
            },
            "user_id": "request-actor",
            "organization_id": "failure-org",
            "created_by": None,
        },
        {
            "table_target": "chat.request",
            "primary_key": {"id": "provider-request-1"},
            "payload": {
                "id": "provider-request-1",
                "user_request_id": "user-request-1",
                "conversation_id": "conversation-1",
            },
            "user_id": None,
            "organization_id": None,
            "created_by": None,
        },
    ]

    upgraded = await replay._upgrade_legacy_chat_payloads(rows)

    assert upgraded[0]["payload"]["created_by"] == "request-actor"
    assert upgraded[0]["payload"]["organization_id"] == "org-1"
    assert upgraded[1]["payload"]["created_by"] == "request-actor"
    assert upgraded[1]["payload"]["organization_id"] == "org-1"


@pytest.mark.asyncio
async def test_request_snapshot_replay_restores_conversation_org(monkeypatch) -> None:
    class Conversation:
        @classmethod
        def filter(cls, **filters):
            assert filters == {"id": "conversation-1"}
            return cls()

        async def values(self, *fields):
            assert fields == ("organization_id", "created_by")
            return [{"organization_id": "org-1", "created_by": "user-1"}]

    monkeypatch.setattr(replay, "get_model", lambda table: Conversation)
    rows = [
        {
            "table_target": "chat.request_snapshot",
            "payload": {
                "id": "snapshot-1",
                "conversation_id": "conversation-1",
            },
            "primary_key": {"id": "snapshot-1"},
            "organization_id": None,
        }
    ]

    upgraded = await replay._upgrade_legacy_chat_payloads(rows)

    assert upgraded[0]["payload"]["organization_id"] == "org-1"


@pytest.mark.asyncio
async def test_legacy_user_request_uses_forensic_failure_org_without_parent() -> None:
    rows = [
        {
            "table_target": "chat.user_request",
            "primary_key": {"id": "user-request-1"},
            "payload": {"id": "user-request-1", "user_id": "request-actor"},
            "user_id": "request-actor",
            "organization_id": "captured-org",
            "created_by": None,
        }
    ]

    upgraded = await replay._upgrade_legacy_chat_payloads(rows)

    assert upgraded[0]["payload"]["created_by"] == "request-actor"
    assert upgraded[0]["payload"]["organization_id"] == "captured-org"


@pytest.mark.asyncio
async def test_replay_failure_is_structurally_captured(monkeypatch) -> None:
    captured: list[tuple[Exception, dict]] = []

    async def fake_capture_error(exc, **kwargs):
        captured.append((exc, kwargs))

    monkeypatch.setattr(
        "matrx_connect.streaming.error_capture.capture_error", fake_capture_error
    )
    exc = RuntimeError("forced replay failure")
    rows = [
        {
            "id": "failure-1",
            "table_target": "chat.tool_call",
            "user_id": "user-1",
            "conversation_id": "conversation-1",
        }
    ]

    await replay._capture_replay_failure(
        exc, request_id="request-1", rows=rows, phase="execute"
    )

    assert captured == [
        (
            exc,
            {
                "kind": "persistence_replay_failed",
                "route": "matrx_ai.persistence.replay.replay_pending",
                "error_type": "RuntimeError",
                "request_id": "request-1",
                "user_id": "user-1",
                "conversation_id": "conversation-1",
                "context": {
                    "phase": "execute",
                    "failure_row_ids": ["failure-1"],
                    "table_targets": ["chat.tool_call"],
                },
            },
        )
    ]
