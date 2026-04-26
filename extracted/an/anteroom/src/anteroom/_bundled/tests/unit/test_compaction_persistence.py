"""Tests for compaction persistence (#1413).

Covers ``persist_compacted_messages()`` contract: DELETE non-tail rows,
INSERT summary + boundary as ``role="system"``, UPDATE tail positions
without recreating rows so attachments / tool_calls / embeddings survive.
"""

from __future__ import annotations

import json
import sqlite3

import pytest

from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.services.compaction import (
    BOUNDARY_MARKER_CONTENT,
    build_boundary_marker,
    persist_compacted_messages,
    runtime_messages_from_stored_rows,
)
from anteroom.services.storage import (
    create_conversation,
    create_message,
    create_tool_call,
    list_messages,
    update_tool_call,
)


@pytest.fixture()
def db() -> ThreadSafeConnection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


def _seed_conversation(db: ThreadSafeConnection, count: int = 8) -> tuple[str, list[dict]]:
    """Create a conversation with *count* messages."""
    conv = create_conversation(db, title="Test")
    msgs: list[dict] = []
    for i in range(count):
        role = "user" if i % 2 == 0 else "assistant"
        msgs.append(create_message(db, conv["id"], role, f"message {i}"))
    return conv["id"], msgs


# ---------------------------------------------------------------------------
# Core behaviour
# ---------------------------------------------------------------------------


def test_deletes_non_tail_messages(db: ThreadSafeConnection) -> None:
    conv_id, msgs = _seed_conversation(db, count=8)
    tail_ids = [m["id"] for m in msgs[-4:]]

    persist_compacted_messages(
        db,
        conv_id,
        summary_msg={"role": "user", "content": "summary text", "metadata": {"compact_summary": True}},
        boundary_msg=build_boundary_marker(original_count=4, preserved_count=4, summary_tokens=100),
        tail_message_ids=tail_ids,
    )

    # Old region deleted (messages 0–3)
    rows = db.execute_fetchall("SELECT id FROM messages WHERE conversation_id = ? ORDER BY position", (conv_id,))
    ids = [r["id"] for r in rows]
    # 1 summary + 1 boundary + 4 tail = 6 rows
    assert len(ids) == 6
    # Tail IDs preserved
    for tail_id in tail_ids:
        assert tail_id in ids


def test_summary_persisted_as_system_role(db: ThreadSafeConnection) -> None:
    """In-memory summary role='user' becomes role='system' on disk (v4 contract)."""
    conv_id, msgs = _seed_conversation(db, count=8)
    tail_ids = [m["id"] for m in msgs[-4:]]

    persist_compacted_messages(
        db,
        conv_id,
        summary_msg={"role": "user", "content": "X", "metadata": {}},
        boundary_msg=None,
        tail_message_ids=tail_ids,
    )

    summary_row = db.execute_fetchone(
        "SELECT role FROM messages WHERE conversation_id = ? AND position = 0", (conv_id,)
    )
    assert summary_row is not None
    assert summary_row["role"] == "system"


def test_summary_metadata_compact_summary_flag_persisted(db: ThreadSafeConnection) -> None:
    conv_id, msgs = _seed_conversation(db, count=8)
    tail_ids = [m["id"] for m in msgs[-4:]]

    persist_compacted_messages(
        db,
        conv_id,
        summary_msg={"role": "user", "content": "X", "metadata": {}},
        boundary_msg=None,
        tail_message_ids=tail_ids,
    )

    summary_row = db.execute_fetchone(
        "SELECT metadata FROM messages WHERE conversation_id = ? AND position = 0", (conv_id,)
    )
    meta = json.loads(summary_row["metadata"])
    assert meta.get("compact_summary") is True


def test_boundary_marker_persisted_with_metadata(db: ThreadSafeConnection) -> None:
    conv_id, msgs = _seed_conversation(db, count=8)
    tail_ids = [m["id"] for m in msgs[-4:]]
    marker = build_boundary_marker(original_count=4, preserved_count=4, summary_tokens=123)

    persist_compacted_messages(
        db,
        conv_id,
        summary_msg={"role": "user", "content": "X", "metadata": {}},
        boundary_msg=marker,
        tail_message_ids=tail_ids,
    )

    boundary_row = db.execute_fetchone(
        "SELECT role, content, metadata FROM messages WHERE conversation_id = ? AND position = 1",
        (conv_id,),
    )
    assert boundary_row is not None
    assert boundary_row["role"] == "system"
    assert boundary_row["content"] == BOUNDARY_MARKER_CONTENT
    meta = json.loads(boundary_row["metadata"])
    assert meta["compact_boundary"] is True
    assert meta["preserved_count"] == 4
    assert meta["summary_tokens"] == 123


def test_tail_positions_renumbered_sequentially(db: ThreadSafeConnection) -> None:
    conv_id, msgs = _seed_conversation(db, count=8)
    tail_ids = [m["id"] for m in msgs[-4:]]

    persist_compacted_messages(
        db,
        conv_id,
        summary_msg={"role": "user", "content": "X", "metadata": {}},
        boundary_msg=build_boundary_marker(original_count=4, preserved_count=4, summary_tokens=50),
        tail_message_ids=tail_ids,
    )

    rows = db.execute_fetchall(
        "SELECT id, position FROM messages WHERE conversation_id = ? ORDER BY position", (conv_id,)
    )
    positions = [r["position"] for r in rows]
    # Summary at 0, boundary at 1, tail at 2..5 — no gaps
    assert positions == [0, 1, 2, 3, 4, 5]


def test_no_boundary_marker_still_works(db: ThreadSafeConnection) -> None:
    conv_id, msgs = _seed_conversation(db, count=8)
    tail_ids = [m["id"] for m in msgs[-4:]]

    persist_compacted_messages(
        db,
        conv_id,
        summary_msg={"role": "user", "content": "X", "metadata": {}},
        boundary_msg=None,
        tail_message_ids=tail_ids,
    )

    rows = db.execute_fetchall("SELECT position FROM messages WHERE conversation_id = ? ORDER BY position", (conv_id,))
    # 1 summary + 4 tail, positions 0..4
    assert [r["position"] for r in rows] == [0, 1, 2, 3, 4]


# ---------------------------------------------------------------------------
# FK-child preservation — the critical UPDATE (not DELETE+INSERT) contract
# ---------------------------------------------------------------------------


def test_preserves_attachments_on_tail_messages(db: ThreadSafeConnection) -> None:
    """Tail message IDs must NOT change — their attachments must survive."""
    conv_id, msgs = _seed_conversation(db, count=8)
    tail_msg = msgs[-1]

    # Attach a file to the last message.
    import uuid as _uuid_mod

    att_id = str(_uuid_mod.uuid4())
    db.execute(
        "INSERT INTO attachments (id, message_id, filename, mime_type, size_bytes, storage_path)"
        " VALUES (?, ?, ?, ?, ?, ?)",
        (att_id, tail_msg["id"], "foo.txt", "text/plain", 42, "/tmp/foo.txt"),
    )
    db.commit()

    tail_ids = [m["id"] for m in msgs[-4:]]
    persist_compacted_messages(
        db,
        conv_id,
        summary_msg={"role": "user", "content": "X", "metadata": {}},
        boundary_msg=None,
        tail_message_ids=tail_ids,
    )

    # Attachment still linked to the same tail message ID.
    att_row = db.execute_fetchone("SELECT message_id FROM attachments WHERE id = ?", (att_id,))
    assert att_row is not None
    assert att_row["message_id"] == tail_msg["id"]


def test_cascade_deletes_attachments_on_summarised_messages(db: ThreadSafeConnection) -> None:
    """Attachments on messages that are being summarised away are deleted."""
    conv_id, msgs = _seed_conversation(db, count=8)
    old_msg = msgs[0]  # Will be summarised

    import uuid as _uuid_mod

    att_id = str(_uuid_mod.uuid4())
    db.execute(
        "INSERT INTO attachments (id, message_id, filename, mime_type, size_bytes, storage_path)"
        " VALUES (?, ?, ?, ?, ?, ?)",
        (att_id, old_msg["id"], "gone.txt", "text/plain", 10, "/tmp/gone.txt"),
    )
    db.commit()

    tail_ids = [m["id"] for m in msgs[-4:]]  # old_msg is NOT in the tail
    persist_compacted_messages(
        db,
        conv_id,
        summary_msg={"role": "user", "content": "X", "metadata": {}},
        boundary_msg=None,
        tail_message_ids=tail_ids,
    )

    # Attachment gone — cascaded by messages FK ON DELETE CASCADE.
    row = db.execute_fetchone("SELECT id FROM attachments WHERE id = ?", (att_id,))
    assert row is None


def test_preserves_tool_calls_on_tail_messages(db: ThreadSafeConnection) -> None:
    conv_id, msgs = _seed_conversation(db, count=8)
    tail_msg = msgs[-1]

    import uuid as _uuid_mod

    tc_id = str(_uuid_mod.uuid4())
    db.execute(
        "INSERT INTO tool_calls (id, message_id, tool_name, server_name, input_json, output_json, status, created_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (tc_id, tail_msg["id"], "read_file", "builtin", "{}", "{}", "success", "2026-04-17T00:00:00Z"),
    )
    db.commit()

    tail_ids = [m["id"] for m in msgs[-4:]]
    persist_compacted_messages(
        db,
        conv_id,
        summary_msg={"role": "user", "content": "X", "metadata": {}},
        boundary_msg=None,
        tail_message_ids=tail_ids,
    )

    row = db.execute_fetchone("SELECT message_id FROM tool_calls WHERE id = ?", (tc_id,))
    assert row is not None
    assert row["message_id"] == tail_msg["id"]


# ---------------------------------------------------------------------------
# Resume round-trip
# ---------------------------------------------------------------------------


def test_resume_returns_summary_boundary_tail_in_order(db: ThreadSafeConnection) -> None:
    """After persistence, list_messages() returns [summary, boundary, *tail]."""
    conv_id, msgs = _seed_conversation(db, count=8)
    tail_ids = [m["id"] for m in msgs[-4:]]
    marker = build_boundary_marker(original_count=4, preserved_count=4, summary_tokens=50)

    persist_compacted_messages(
        db,
        conv_id,
        summary_msg={"role": "user", "content": "the summary", "metadata": {}},
        boundary_msg=marker,
        tail_message_ids=tail_ids,
    )

    loaded = list_messages(db, conv_id)
    assert len(loaded) == 6
    assert loaded[0]["role"] == "system"  # persisted summary role
    assert "the summary" in loaded[0]["content"]
    assert loaded[1]["role"] == "system"  # boundary marker
    # Tail messages preserved in order with their original IDs
    assert loaded[2]["id"] == tail_ids[0]
    assert loaded[-1]["id"] == tail_ids[-1]


def test_resume_tail_first_non_system_is_user(db: ThreadSafeConnection) -> None:
    """Provider-safe ordering on resume: after system extraction, first is user."""
    conv_id, msgs = _seed_conversation(db, count=8)
    # msgs[-4] should be user (index 4 = even → user per _seed_conversation)
    assert msgs[-4]["role"] == "user"
    tail_ids = [m["id"] for m in msgs[-4:]]
    marker = build_boundary_marker(original_count=4, preserved_count=4, summary_tokens=50)

    persist_compacted_messages(
        db,
        conv_id,
        summary_msg={"role": "user", "content": "X", "metadata": {}},
        boundary_msg=marker,
        tail_message_ids=tail_ids,
    )

    loaded = list_messages(db, conv_id)
    non_system = [m for m in loaded if m["role"] != "system"]
    assert non_system[0]["role"] == "user"


# ---------------------------------------------------------------------------
# Defensive: empty tail, non-existent tail IDs
# ---------------------------------------------------------------------------


def test_empty_tail_ids_deletes_all_old_messages(db: ThreadSafeConnection) -> None:
    """When no tail is preserved (full-summary fallback on resume), all old messages are deleted."""
    conv_id, msgs = _seed_conversation(db, count=4)

    persist_compacted_messages(
        db,
        conv_id,
        summary_msg={"role": "user", "content": "the only surviving message", "metadata": {}},
        boundary_msg=None,
        tail_message_ids=[],
    )

    loaded = list_messages(db, conv_id)
    assert len(loaded) == 1
    assert loaded[0]["role"] == "system"
    assert "the only surviving message" in loaded[0]["content"]


def test_nonexistent_tail_id_is_noop_on_update(db: ThreadSafeConnection) -> None:
    """Stale ID in tail_message_ids doesn't raise — UPDATE just matches nothing."""
    conv_id, msgs = _seed_conversation(db, count=4)
    # Real IDs plus a fake one
    tail_ids = [m["id"] for m in msgs[-2:]] + ["does-not-exist"]

    # Should not raise
    persist_compacted_messages(
        db,
        conv_id,
        summary_msg={"role": "user", "content": "X", "metadata": {}},
        boundary_msg=None,
        tail_message_ids=tail_ids,
    )

    loaded = list_messages(db, conv_id)
    # Summary + 2 real tail messages (fake ID doesn't create a row)
    assert len(loaded) == 3


@pytest.mark.asyncio
async def test_agent_loop_compaction_persists_same_logical_tool_tail(db: ThreadSafeConnection) -> None:
    """Runtime tool-result entries map back to their parent assistant row ID."""
    from unittest.mock import AsyncMock

    from anteroom.services.agent_loop import _compact_messages

    conv_id = create_conversation(db, title="Tool tail")["id"]
    create_message(db, conv_id, "user", "old question")
    create_message(db, conv_id, "assistant", "old answer")
    create_message(db, conv_id, "user", "recent duplicate")
    assistant = create_message(db, conv_id, "assistant", "")
    create_tool_call(db, assistant["id"], "bash", "builtin", {"command": "echo hi"}, tool_call_id="tc1")
    update_tool_call(db, "tc1", {"stdout": "hi"}, "success")
    recent_user = create_message(db, conv_id, "user", "recent duplicate")
    recent_assistant = create_message(db, conv_id, "assistant", "done")

    att_id = "att-tail"
    db.execute(
        "INSERT INTO attachments (id, message_id, filename, mime_type, size_bytes, storage_path)"
        " VALUES (?, ?, ?, ?, ?, ?)",
        (att_id, recent_user["id"], "tail.txt", "text/plain", 3, "/tmp/tail.txt"),
    )
    db.execute(
        "CREATE TABLE IF NOT EXISTS message_embeddings ("
        " message_id TEXT PRIMARY KEY,"
        " conversation_id TEXT NOT NULL,"
        " chunk_index INTEGER NOT NULL DEFAULT 0,"
        " content_hash TEXT NOT NULL,"
        " status TEXT NOT NULL DEFAULT 'embedded',"
        " created_at TEXT NOT NULL,"
        " FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE"
        ")"
    )
    db.execute(
        "INSERT INTO message_embeddings (message_id, conversation_id, content_hash, status, created_at)"
        " VALUES (?, ?, ?, ?, ?)",
        (recent_assistant["id"], conv_id, "hash-tail", "embedded", "2026-04-17T00:00:00Z"),
    )
    db.commit()

    ai_messages = runtime_messages_from_stored_rows(list_messages(db, conv_id))
    svc = AsyncMock()
    svc.complete = AsyncMock(return_value="Summary")

    ok = await _compact_messages(svc, ai_messages, preserve_tail=4, db=db, conversation_id=conv_id)

    assert ok is True
    loaded = list_messages(db, conv_id)
    loaded_ids = [m["id"] for m in loaded]
    assert loaded[0]["role"] == "system"
    assert loaded[1]["metadata"]["compact_boundary"] is True
    assert assistant["id"] in loaded_ids
    assert recent_user["id"] in loaded_ids
    assert recent_assistant["id"] in loaded_ids
    assert len([m for m in loaded if m["role"] not in {"system"}]) == 4

    tool_calls = db.execute_fetchall("SELECT id, message_id FROM tool_calls ORDER BY id")
    assert [(r["id"], r["message_id"]) for r in tool_calls] == [("tc1", assistant["id"])]
    attachment = db.execute_fetchone("SELECT message_id FROM attachments WHERE id = ?", (att_id,))
    assert attachment is not None
    assert attachment["message_id"] == recent_user["id"]
    embedding = db.execute_fetchone(
        "SELECT message_id FROM message_embeddings WHERE message_id = ?",
        (recent_assistant["id"],),
    )
    assert embedding is not None
