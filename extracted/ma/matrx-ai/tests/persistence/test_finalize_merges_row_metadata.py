"""Finalize MERGES into chat.user_request / chat.conversation metadata, never replaces it.

Recorded shape: request e1ae687d (extend.browser_chat), resumed after an
ask_person answer. The door had stamped ``mandate_key`` / ``mandate_resolution``
on the row; the resumed run's context carried neither, and finalize wrote its
own metadata whole, so the row ended with only run-context keys (ttft_ms,
usage_by_model, jwt_claims, ...). Each test fails when finalize replaces.
"""

from __future__ import annotations

import pytest

import matrx_ai.db.persistence as persistence

# What the door wrote on the row (keys that the resumed run context lacks).
DOOR_KEYS = {
    "mandate_key": "extend.browser_chat",
    "mandate_resolution": {"agent_id": "a1", "version": 3, "source": "holder"},
    "run_label": "chrome-extension/assistant",
}
# What the resumed run's context carries at finalize (recorded key set).
RESUMED_RUN_KEYS = {
    "ttft_ms": 5470,
    "active_ui_surface": "chrome-extension/assistant",
    "usage_by_model": {"claude-opus-4-7": {"cost": 0.1286135}},
    "runtime_execution_id": "d7859caf-bb3f-41bc-a967-a3f3370a3162",
}


class _Row:
    def __init__(self, metadata):
        self.metadata = metadata


class _UserRequestMgr:
    def __init__(self, row):
        self._row = row

    async def filter_user_requests(self, id):  # noqa: A002
        return [self._row] if self._row is not None else []


class _ConversationMgr:
    def __init__(self, row):
        self._row = row

    async def load_conversation_by_id(self, _id):
        return self._row


class _Cxm:
    def __init__(self, row):
        self.user_request = _UserRequestMgr(row)
        self.conversation = _ConversationMgr(row)


def _install(monkeypatch, row):
    monkeypatch.setattr(persistence, "_cxm", lambda: _Cxm(row))


@pytest.mark.asyncio
async def test_resumed_user_request_keeps_the_door_keys(monkeypatch):
    _install(monkeypatch, _Row(dict(DOOR_KEYS)))
    merged = await persistence.merge_into_existing_metadata(
        "user_request", "e1ae687d-935b-4f56-a81d-a74018e5dd8d", dict(RESUMED_RUN_KEYS)
    )
    assert merged["mandate_key"] == "extend.browser_chat"
    assert merged["mandate_resolution"] == DOOR_KEYS["mandate_resolution"]
    assert merged["run_label"] == DOOR_KEYS["run_label"]
    for k, v in RESUMED_RUN_KEYS.items():
        assert merged[k] == v


@pytest.mark.asyncio
async def test_incoming_wins_per_key(monkeypatch):
    _install(monkeypatch, _Row({"ttft_ms": 1, "mandate_key": "old"}))
    merged = await persistence.merge_into_existing_metadata(
        "user_request", "x", {"ttft_ms": 2}
    )
    assert merged == {"ttft_ms": 2, "mandate_key": "old"}


@pytest.mark.asyncio
async def test_conversation_finalize_keeps_run_configuration_and_other_keys(monkeypatch):
    _install(monkeypatch, _Row({"run_configuration": {"outputKinds": ["table"]}, "title_source": "agent"}))
    merged = await persistence.merge_into_existing_metadata(
        "conversation", "c", {"run_configuration": {"x": 1}, "last_request_context": {"a": 1}}
    )
    assert merged["run_configuration"] == {"outputKinds": ["table"], "x": 1}
    assert merged["title_source"] == "agent"
    assert merged["last_request_context"] == {"a": 1}


@pytest.mark.asyncio
async def test_missing_row_or_failed_read_yields_incoming_unchanged(monkeypatch):
    _install(monkeypatch, None)
    assert await persistence.merge_into_existing_metadata("user_request", "x", {"a": 1}) == {"a": 1}

    def boom():
        raise RuntimeError("no db")

    monkeypatch.setattr(persistence, "_cxm", boom)
    assert await persistence.merge_into_existing_metadata("conversation", "x", {"a": 1}) == {"a": 1}


def test_finalize_routes_both_metadata_writes_through_the_merge():
    import inspect

    src = inspect.getsource(persistence)
    assert 'merge_into_existing_metadata(\n                    "conversation"' in src
    assert 'merge_into_existing_metadata(\n                    "user_request"' in src
