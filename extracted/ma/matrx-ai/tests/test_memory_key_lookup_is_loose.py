"""The memory tool takes the name the model is SHOWN for a saved fact must be a key the memory tool accepts (2026-11-17).

Live report: the injected block showed "preference credentials and 2fa self managed" while the stored key was
"preference_credentials_and_2fa_self_managed"; ``memory`` update with the displayed name returned not_found.
Fixed twice over: the block shows the exact stored key, and every key lookup (recall, update, forget) treats
spaces, underscores and hyphens the same. Also pins the age/outdated and missing-tool flags.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

from matrx_ai.db import cxm
from matrx_ai.tools.implementations import memory as memory_module
from matrx_ai.tools.models import ToolContext

USER = "11111111-1111-4111-8111-111111111111"
KEY = "preference_credentials_and_2fa_self_managed"
DISPLAYED_BEFORE_THE_FIX = "preference credentials and 2fa self managed"  # what the block used to print


class _Emitter:
    async def send_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_data(self, *_a: Any, **_kw: Any) -> None: ...


def _row(id: str, key: str, deleted_at: str | None = None) -> Any:
    fields = {"id": id, "key": key, "content": "I manage my own 2FA.", "deleted_at": deleted_at,
              "memory_type": "long_term", "importance": 0.5, "scope": "user", "scope_id": None,
              "access_count": 0, "expires_at": None, "created_at": None, "updated_at": None}
    return type("Row", (), {**fields, "to_dict": lambda self: dict(fields)})()


@pytest.fixture(autouse=True)
def _ctx() -> Any:
    token = set_app_context(AppContext(emitter=_Emitter(), user_id=USER, organization_id="org-1"))
    yield
    clear_app_context(token)


def _wire(monkeypatch: pytest.MonkeyPatch, updates: list[tuple[str, dict]]) -> None:
    rows = [_row("mem-1", KEY)]

    async def fake_filter(**f: Any) -> list[Any]:
        return [r for r in rows if "key" not in f or r.key == f["key"]]

    monkeypatch.setattr(cxm.agent_memory, "filter_agent_memories", fake_filter)
    monkeypatch.setattr(memory_module, "queue_agent_memory_update", lambda id, **kw: updates.append((id, kw)) or "q")
    monkeypatch.setattr("matrx_utils.detached_task", lambda *_a, **_kw: None)


@pytest.mark.asyncio
async def test_update_by_the_displayed_name_finds_the_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    updates: list[tuple[str, dict]] = []
    _wire(monkeypatch, updates)
    result = await memory_module.memory_update(
        {"key": DISPLAYED_BEFORE_THE_FIX, "scope": "user", "content": "New text."}, ToolContext(call_id="u1")
    )
    assert result.success, result.error
    assert updates and updates[0][0] == "mem-1" and updates[0][1]["content"] == "New text."


@pytest.mark.asyncio
async def test_forget_by_the_displayed_name_archives_the_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    updates: list[tuple[str, dict]] = []
    _wire(monkeypatch, updates)
    result = await memory_module.memory_forget({"key": DISPLAYED_BEFORE_THE_FIX, "scope": "user"}, ToolContext(call_id="f1"))
    assert result.success, result.error
    assert result.output["deleted"] == 1 and updates[0][1]["deleted_at"]


@pytest.mark.asyncio
@pytest.mark.parametrize("typed", ["preference credentials and 2fa self managed", "preference-credentials-and-2fa-self-managed"])
async def test_every_lookup_treats_spaces_underscores_and_hyphens_alike(monkeypatch: pytest.MonkeyPatch, typed: str) -> None:
    updates: list[tuple[str, dict]] = []
    _wire(monkeypatch, updates)
    got = await memory_module.memory_recall({"key": typed, "scope": "user"}, ToolContext(call_id="r1"))
    assert got.success and got.output["count"] == 1
    upd = await memory_module.memory_update({"key": typed, "scope": "user", "content": "x"}, ToolContext(call_id="u2"))
    assert upd.success, upd.error
    gone = await memory_module.memory_forget({"key": typed, "scope": "user"}, ToolContext(call_id="f3"))
    assert gone.success and gone.output["deleted"] == 1


def _two_loose_keys(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, dict]]:
    rows = [_row("a", "x_y"), _row("b", "x-y")]
    updates: list[tuple[str, dict]] = []

    async def fake_filter(**f: Any) -> list[Any]:
        return [r for r in rows if "key" not in f or r.key == f["key"]]

    monkeypatch.setattr(cxm.agent_memory, "filter_agent_memories", fake_filter)
    monkeypatch.setattr(memory_module, "queue_agent_memory_update", lambda id, **kw: updates.append((id, kw)) or "q")
    monkeypatch.setattr(
        memory_module, "queue_agent_memory_create", lambda *_a, **_kw: pytest.fail("ambiguous: nothing is created")
    )
    return updates


@pytest.mark.asyncio
@pytest.mark.parametrize("action", ["update", "forget", "recall", "store"])
async def test_an_ambiguous_loose_key_fails_loudly_and_lists_the_stored_keys(
    monkeypatch: pytest.MonkeyPatch, action: str
) -> None:
    updates = _two_loose_keys(monkeypatch)
    args: dict[str, Any] = {"key": "x y", "scope": "user"}
    if action in ("update", "store"):
        args["content"] = "c"
    if action == "store":
        args["memory_type"] = "long_term"
    fn = {"update": memory_module.memory_update, "forget": memory_module.memory_forget,
          "recall": memory_module.memory_recall, "store": memory_module.memory_store}[action]
    res = await fn(args, ToolContext(call_id="amb"))
    assert not res.success
    assert res.error.error_type == "ambiguous_key"
    assert "'x-y'" in res.error.message and "'x_y'" in res.error.message
    assert updates == []


@pytest.mark.asyncio
async def test_store_with_the_spaced_name_updates_the_existing_memory_not_a_duplicate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    updates: list[tuple[str, dict]] = []
    _wire(monkeypatch, updates)
    monkeypatch.setattr(
        memory_module, "queue_agent_memory_create", lambda *_a, **_kw: pytest.fail("a duplicate memory was created")
    )
    res = await memory_module.memory_store(
        {"key": DISPLAYED_BEFORE_THE_FIX, "scope": "user", "memory_type": "long_term", "content": "New."},
        ToolContext(call_id="s1"),
    )
    assert res.success, res.error
    assert updates[0][0] == "mem-1" and updates[0][1]["key"] == "preference_credentials_and_2fa_self_managed"


@pytest.mark.asyncio
async def test_search_finds_an_underscored_key_from_a_spaced_query(monkeypatch: pytest.MonkeyPatch) -> None:
    _wire(monkeypatch, [])
    res = await memory_module.memory_search({"query": "credentials and 2fa", "scope": "user"}, ToolContext(call_id="q1"))
    assert res.success and res.output["count"] == 1


STORED = "preference_credentials_and_2fa_self_managed"


@pytest.mark.asyncio
async def test_results_name_the_stored_key_and_say_when_it_differs_from_the_typed_one(monkeypatch: pytest.MonkeyPatch) -> None:
    _wire(monkeypatch, [])
    upd = await memory_module.memory_update(
        {"key": DISPLAYED_BEFORE_THE_FIX, "scope": "user", "content": "x"}, ToolContext(call_id="k1"))
    assert upd.output["key"] == STORED and upd.output["typed_key"] == DISPLAYED_BEFORE_THE_FIX and STORED in upd.output["note"]
    exact = await memory_module.memory_update({"key": STORED, "scope": "user", "content": "x"}, ToolContext(call_id="k2"))
    assert exact.output["key"] == STORED and "note" not in exact.output
    gone = await memory_module.memory_forget({"key": DISPLAYED_BEFORE_THE_FIX, "scope": "user"}, ToolContext(call_id="k3"))
    assert gone.output["key"] == STORED and STORED in gone.output["note"]


@pytest.mark.asyncio
async def test_store_on_a_loose_key_says_it_updated_the_existing_memory(monkeypatch: pytest.MonkeyPatch) -> None:
    _wire(monkeypatch, [])
    res = await memory_module.memory_store(
        {"key": DISPLAYED_BEFORE_THE_FIX, "scope": "user", "memory_type": "long_term", "content": "New."},
        ToolContext(call_id="m1"))
    assert res.output["updated_existing"] is True and res.output["merged_into_existing"] is True
    assert res.output["key"] == STORED and STORED in res.output["note"]
    plain = await memory_module.memory_store(
        {"key": STORED, "scope": "user", "memory_type": "long_term", "content": "New."}, ToolContext(call_id="m2"))
    assert plain.output["updated_existing"] is True and "merged_into_existing" not in plain.output


@pytest.mark.asyncio
async def test_forget_of_a_missing_key_is_not_found_never_a_silent_success(monkeypatch: pytest.MonkeyPatch) -> None:
    _wire(monkeypatch, [])
    res = await memory_module.memory_forget({"key": "no_such_key", "scope": "user"}, ToolContext(call_id="n1"))
    assert not res.success and res.error.error_type == "not_found"


@pytest.mark.asyncio
@pytest.mark.parametrize("action", ["update", "forget", "recall", "store"])
@pytest.mark.parametrize("key", ["-", "___", " . "])
async def test_a_key_of_only_separators_is_refused_not_matched_to_a_stored_underscore(
    monkeypatch: pytest.MonkeyPatch, action: str, key: str
) -> None:
    rows = [_row("u", "_")]

    async def fake_filter(**f: Any) -> list[Any]:
        return [r for r in rows if "key" not in f or r.key == f["key"]]

    monkeypatch.setattr(cxm.agent_memory, "filter_agent_memories", fake_filter)
    monkeypatch.setattr(memory_module, "queue_agent_memory_update", lambda *_a, **_kw: pytest.fail("matched '_'"))
    args: dict[str, Any] = {"key": key, "scope": "user"}
    if action in ("update", "store"):
        args["content"] = "c"
    if action == "store":
        args["memory_type"] = "long_term"
    fn = getattr(memory_module, f"memory_{action}")
    res = await fn(args, ToolContext(call_id="e1"))
    assert not res.success and res.error.error_type == "invalid_key"
