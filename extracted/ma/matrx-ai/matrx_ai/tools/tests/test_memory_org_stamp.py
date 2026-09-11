"""Regression guard for the memory-tool org-stamping bug.

``memory_store`` used to stamp only ``created_by``/``user_id`` (via
``stamp_row_owner``) and never touched ``organization_id``. Every insert then
fell through to the DB backstop trigger (``chat._stamp_org_default``), which
defaults a NULL org to the creator's PERSONAL organization — so a memory
stored while a team org was active silently landed attributed to the user's
personal org instead. For ``scope="organization"`` this produced a
split-brain row: ``scope_id`` correctly pointed at the team org while
``organization_id`` pointed at the personal org.

These tests assert the fix: ``memory_store`` stamps the request's explicit
org (``ctx.organization_id``) on both the create and update paths, and for
``scope="organization"`` keeps ``organization_id`` aligned with the semantic
target org (``scope_id``). ``memory_store``/``memory_update``/``memory_forget``/
``memory_search`` must also scope their lookups by ``scope_id`` for org/project
scope, so one org's memory is never read or overwritten from another.

Org law (aidream CLAUDE.md; common-docs/projects/no-db-assigned-org/PLAN.md):
a writer never invents an org. With no active org, ``memory_store`` today
leaves ``organization_id`` unset and relies on the forbidden DB backstop —
that open defect is recorded in the no-db-assigned-org register, not pinned
here; the guard below only forbids inventing a substitute org.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any
from unittest.mock import AsyncMock

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

from matrx_ai.db import cxm
from matrx_ai.tools.implementations import memory as memory_module
from matrx_ai.tools.implementations.memory import (
    memory_forget,
    memory_recall,
    memory_search,
    memory_store,
    memory_update,
)
from matrx_ai.tools.models import ToolContext

TEAM_ORG_ID = "team-org-11111111-1111-1111-1111-111111111111"
USER_ID = "user-99999999-9999-9999-9999-999999999999"


class _NullEmitter:
    async def send_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_data(self, *_a: Any, **_kw: Any) -> None: ...


@pytest.fixture()
def app_ctx_with_active_org():
    """Install an AppContext with a given active org; auto-cleanup after the test."""
    tokens: list[Any] = []

    def _make(organization_id: str | None) -> None:
        ctx = AppContext(
            emitter=_NullEmitter(),
            user_id=USER_ID,
            organization_id=organization_id,
        )
        tokens.append(set_app_context(ctx))

    yield _make

    for token in tokens:
        try:
            clear_app_context(token)
        except ValueError:
            # pytest-asyncio runs the test coroutine in its own Task/Context;
            # a Token minted inside that Task cannot be reset from this
            # (sync) fixture's outer Context. Best-effort cleanup — the
            # ContextVar default still applies to any *new* Task, so this
            # never leaks state across tests.
            pass


def _tool_ctx() -> ToolContext:
    return ToolContext(call_id="test-call")


async def test_memory_recall_access_update_owns_standalone_coordinator(
    monkeypatch: pytest.MonkeyPatch, app_ctx_with_active_org
) -> None:
    app_ctx_with_active_org(TEAM_ORG_ID)
    row = type(
        "Row",
        (),
        {
            "id": "memory-id",
            "importance": 1,
            "updated_at": "2026-08-26T00:00:00Z",
            "access_count": 2,
            "to_dict": lambda self: {"id": self.id},
        },
    )()
    monkeypatch.setattr(
        cxm.agent_memory, "filter_agent_memories", AsyncMock(return_value=[row])
    )
    entered: list[str] = []
    queued: list[tuple[str, dict[str, Any]]] = []
    spawned: list[Any] = []

    @asynccontextmanager
    async def fake_standalone(**kwargs: Any):
        entered.append(kwargs["reason"])
        yield object()

    def fake_queue(item_id: str, **fields: Any) -> str:
        queued.append((item_id, fields))
        return "queued"

    def fake_detached(coro: Any, **_kwargs: Any) -> None:
        spawned.append(coro)

    monkeypatch.setattr(memory_module, "standalone_coordinator", fake_standalone)
    monkeypatch.setattr(memory_module, "queue_agent_memory_update", fake_queue)
    monkeypatch.setattr("matrx_utils.detached_task", fake_detached)

    result = await memory_recall({"scope": "user"}, _tool_ctx())
    assert result.success is True
    assert len(spawned) == 1
    await spawned[0]
    assert entered == ["agent_memory_access_count"]
    assert queued == [
        (
            "memory-id",
            {"access_count": 3, "last_accessed_at": queued[0][1]["last_accessed_at"]},
        )
    ]


async def test_memory_store_stamps_active_org_for_user_scope(
    monkeypatch: pytest.MonkeyPatch, app_ctx_with_active_org
) -> None:
    """A user-scope memory stored while a team org is active must be attributed
    to that team org, not fall through to the personal-org DB backstop."""
    app_ctx_with_active_org(TEAM_ORG_ID)

    monkeypatch.setattr(cxm.agent_memory, "filter_agent_memories", AsyncMock(return_value=[]))
    captured: dict[str, Any] = {}

    def fake_create(**data: Any) -> str:
        captured.update(data)
        return "queued"

    monkeypatch.setattr(memory_module, "queue_agent_memory_create", fake_create)

    result = await memory_store(
        {"key": "pref", "content": "likes dark mode", "scope": "user"}, _tool_ctx()
    )

    assert result.success is True
    assert captured.get("organization_id") == TEAM_ORG_ID
    assert captured["scope"] == "user"
    assert captured.get("scope_id") is None


async def test_memory_store_organization_scope_aligns_org_id_with_scope_id(
    monkeypatch: pytest.MonkeyPatch, app_ctx_with_active_org
) -> None:
    """For scope='organization' the row's organization_id must match the
    semantic target org (scope_id) — never split-brained."""
    app_ctx_with_active_org(TEAM_ORG_ID)

    monkeypatch.setattr(cxm.agent_memory, "filter_agent_memories", AsyncMock(return_value=[]))
    captured: dict[str, Any] = {}

    def fake_create(**data: Any) -> str:
        captured.update(data)
        return "queued"

    monkeypatch.setattr(memory_module, "queue_agent_memory_create", fake_create)

    await memory_store(
        {"key": "team_pref", "content": "shared setting", "scope": "organization"}, _tool_ctx()
    )

    assert captured.get("scope_id") == TEAM_ORG_ID
    assert captured.get("organization_id") == TEAM_ORG_ID


async def test_memory_store_never_invents_an_org_when_none_is_active(
    monkeypatch: pytest.MonkeyPatch, app_ctx_with_active_org
) -> None:
    """Break caught: a writer substituting a default/personal/system org when the
    request carries none. (A refusal that queues nothing also satisfies this.)"""
    app_ctx_with_active_org(None)

    monkeypatch.setattr(cxm.agent_memory, "filter_agent_memories", AsyncMock(return_value=[]))
    written: list[dict[str, Any]] = []
    monkeypatch.setattr(
        memory_module, "queue_agent_memory_create", lambda **data: written.append(data) or "q"
    )
    monkeypatch.setattr(
        memory_module,
        "queue_agent_memory_update",
        lambda _id, **data: written.append(data) or "q",
    )

    await memory_store({"key": "pref", "content": "x", "scope": "user"}, _tool_ctx())

    assert [w.get("organization_id") for w in written if "organization_id" in w] == []


async def test_memory_store_lookup_never_overwrites_another_orgs_memory(
    monkeypatch: pytest.MonkeyPatch, app_ctx_with_active_org
) -> None:
    """Break caught: memory_store's existence lookup dropping ``scope_id`` —
    an org-scope store would then UPDATE the same-key memory of a different
    org instead of creating this org's own row."""
    app_ctx_with_active_org(TEAM_ORG_ID)

    other_orgs_row = type("Row", (), {"id": "other-org-memory"})()

    async def fake_filter(**filters: Any) -> list[Any]:
        return [] if filters.get("scope_id") == TEAM_ORG_ID else [other_orgs_row]

    monkeypatch.setattr(cxm.agent_memory, "filter_agent_memories", fake_filter)
    created: list[dict[str, Any]] = []
    updated: list[str] = []
    monkeypatch.setattr(
        memory_module, "queue_agent_memory_create", lambda **data: created.append(data) or "q"
    )
    monkeypatch.setattr(
        memory_module, "queue_agent_memory_update", lambda item_id, **_d: updated.append(item_id) or "q"
    )

    result = await memory_store(
        {"key": "team_pref", "content": "shared setting", "scope": "organization"}, _tool_ctx()
    )

    assert result.success is True
    assert updated == []
    assert [(c.get("key"), c.get("organization_id")) for c in created] == [
        ("team_pref", TEAM_ORG_ID)
    ]


async def test_memory_store_updates_existing_row_with_active_org(
    monkeypatch: pytest.MonkeyPatch, app_ctx_with_active_org
) -> None:
    """The update-path (existing row found) must also get the org stamp."""
    app_ctx_with_active_org(TEAM_ORG_ID)

    existing_row = type("Row", (), {"id": "existing-id"})()
    monkeypatch.setattr(
        cxm.agent_memory, "filter_agent_memories", AsyncMock(return_value=[existing_row])
    )
    captured: dict[str, Any] = {}

    def fake_update(item_id: str, **data: Any) -> str:
        captured["item_id"] = item_id
        captured.update(data)
        return "queued"

    monkeypatch.setattr(memory_module, "queue_agent_memory_update", fake_update)

    await memory_store({"key": "pref", "content": "updated", "scope": "user"}, _tool_ctx())

    assert captured["item_id"] == "existing-id"
    assert captured.get("organization_id") == TEAM_ORG_ID


async def test_memory_update_filters_by_scope_id_for_organization_scope(
    monkeypatch: pytest.MonkeyPatch, app_ctx_with_active_org
) -> None:
    app_ctx_with_active_org(TEAM_ORG_ID)

    captured_filters: dict[str, Any] = {}

    async def fake_filter(**filters: Any) -> list[Any]:
        captured_filters.update(filters)
        return []

    monkeypatch.setattr(cxm.agent_memory, "filter_agent_memories", fake_filter)

    result = await memory_update(
        {"key": "team_pref", "content": "new content", "scope": "organization"}, _tool_ctx()
    )

    assert result.success is False  # not found — the point is the filter shape, not a hit
    assert captured_filters["scope_id"] == TEAM_ORG_ID


async def test_memory_forget_filters_by_scope_id_for_organization_scope(
    monkeypatch: pytest.MonkeyPatch, app_ctx_with_active_org
) -> None:
    app_ctx_with_active_org(TEAM_ORG_ID)

    captured_filters: dict[str, Any] = {}

    async def fake_filter(**filters: Any) -> list[Any]:
        captured_filters.update(filters)
        return []

    monkeypatch.setattr(cxm.agent_memory, "filter_agent_memories", fake_filter)

    result = await memory_forget({"key": "team_pref", "scope": "organization"}, _tool_ctx())

    assert result.success is True
    assert captured_filters["scope_id"] == TEAM_ORG_ID


async def test_memory_search_filters_by_scope_id_for_organization_scope(
    monkeypatch: pytest.MonkeyPatch, app_ctx_with_active_org
) -> None:
    app_ctx_with_active_org(TEAM_ORG_ID)

    captured_filters: dict[str, Any] = {}

    async def fake_filter(**filters: Any) -> list[Any]:
        captured_filters.update(filters)
        return []

    monkeypatch.setattr(cxm.agent_memory, "filter_agent_memories", fake_filter)

    result = await memory_search({"query": "setting", "scope": "organization"}, _tool_ctx())

    assert result.success is True
    assert captured_filters["scope_id"] == TEAM_ORG_ID
