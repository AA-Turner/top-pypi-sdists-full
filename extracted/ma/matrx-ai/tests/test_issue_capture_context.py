from __future__ import annotations

from typing import Any

import pytest
from matrx_connect import AppContext, clear_app_context, set_app_context

from matrx_ai.ops import issue_capture, issue_registry


@pytest.mark.asyncio
async def test_capture_issue_inherits_ambient_request_identity(monkeypatch: pytest.MonkeyPatch):
    created: list[dict[str, Any]] = []
    detached: list[Any] = []

    class _OpsIssueEvent:
        @classmethod
        async def create(cls, **payload: Any) -> None:
            created.append(payload)

    async def _get_issue_class(_key: str) -> dict[str, Any]:
        return {"id": "issue-class-id", "is_active": True}

    def _track_detached(coro: Any, *, name: str) -> None:
        detached.append(coro)

    monkeypatch.setattr(issue_capture, "get_model", lambda _name: _OpsIssueEvent)
    monkeypatch.setattr(issue_registry, "get_issue_class", _get_issue_class)
    monkeypatch.setattr("matrx_utils.detached_task", _track_detached)

    token = set_app_context(
        AppContext(
            emitter=None,  # type: ignore[arg-type]
            user_id="user-id",
            organization_id="organization-id",
            conversation_id="conversation-id",
            request_id="request-id",
            is_authenticated=True,
        )
    )
    try:
        await issue_capture.capture_issue(
            "anthropic.streaming_required",
            error_type="streaming_required",
            provider="anthropic",
            was_recovered=True,
        )
        await detached.pop()
    finally:
        clear_app_context(token)

    assert len(created) == 1
    assert created[0]["user_id"] == "user-id"
    assert created[0]["organization_id"] == "organization-id"
    assert created[0]["conversation_id"] == "conversation-id"
    assert created[0]["request_id"] == "request-id"


@pytest.mark.asyncio
async def test_capture_issue_resolves_system_organization_without_context(
    monkeypatch: pytest.MonkeyPatch,
):
    created: list[dict[str, Any]] = []
    detached: list[Any] = []

    class _OpsIssueEvent:
        @classmethod
        async def create(cls, **payload: Any) -> None:
            created.append(payload)

    async def _get_issue_class(_key: str) -> dict[str, Any]:
        return {"id": "issue-class-id", "is_active": True}

    async def _resolve(**identity: Any) -> str:
        assert identity == {"user_id": None, "organization_id": None}
        return "system-organization-id"

    def _track_detached(coro: Any, *, name: str) -> None:
        detached.append(coro)

    monkeypatch.setattr(issue_capture, "get_model", lambda _name: _OpsIssueEvent)
    monkeypatch.setattr(issue_registry, "get_issue_class", _get_issue_class)
    monkeypatch.setattr("matrx_utils.detached_task", _track_detached)
    monkeypatch.setattr(issue_capture, "has_ext", lambda name: True)
    monkeypatch.setattr(issue_capture, "get_ext", lambda name: _resolve)

    await issue_capture.capture_issue(
        "anthropic.grammar_too_large",
        error_type="grammar_too_large",
        provider="anthropic",
    )
    await detached.pop()

    assert len(created) == 1
    assert created[0]["organization_id"] == "system-organization-id"
