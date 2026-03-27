"""Tests for storage.py advanced CRUD: folders, tags, artifacts, usage, cloning (#1021)."""

from __future__ import annotations

import sqlite3

import pytest

from anteroom.db import _FTS_SCHEMA, _FTS_TRIGGERS, _SCHEMA, ThreadSafeConnection
from anteroom.services.storage import (
    add_tag_to_conversation,
    create_conversation,
    create_folder,
    create_message,
    create_tag,
    delete_folder,
    delete_tag,
    fork_conversation,
    get_conversation,
    get_conversation_tags,
    get_conversation_token_total,
    get_daily_token_total,
    get_usage_stats,
    list_conversations,
    list_folders,
    list_messages,
    list_tags,
    move_conversation_to_folder,
    remove_tag_from_conversation,
    update_folder,
    update_tag,
)


@pytest.fixture()
def db() -> ThreadSafeConnection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(_SCHEMA)
    try:
        conn.executescript(_FTS_SCHEMA)
        conn.executescript(_FTS_TRIGGERS)
    except sqlite3.OperationalError:
        pass
    conn.commit()
    return ThreadSafeConnection(conn)


# ---------------------------------------------------------------------------
# Folder CRUD
# ---------------------------------------------------------------------------


class TestFolderCRUD:
    def test_create_folder(self, db: ThreadSafeConnection) -> None:
        folder = create_folder(db, "Work")
        assert folder["name"] == "Work"
        assert "id" in folder
        assert folder["parent_id"] is None
        assert folder["collapsed"] is False

    def test_create_nested_folder(self, db: ThreadSafeConnection) -> None:
        parent = create_folder(db, "Root")
        child = create_folder(db, "Sub", parent_id=parent["id"])
        assert child["parent_id"] == parent["id"]

    def test_list_folders(self, db: ThreadSafeConnection) -> None:
        create_folder(db, "A")
        create_folder(db, "B")
        folders = list_folders(db)
        assert len(folders) == 2

    def test_list_folders_empty(self, db: ThreadSafeConnection) -> None:
        assert list_folders(db) == []

    def test_update_folder_name(self, db: ThreadSafeConnection) -> None:
        folder = create_folder(db, "Old")
        updated = update_folder(db, folder["id"], name="New")
        assert updated is not None
        assert updated["name"] == "New"

    def test_update_folder_collapsed(self, db: ThreadSafeConnection) -> None:
        folder = create_folder(db, "Test")
        updated = update_folder(db, folder["id"], collapsed=True)
        assert updated is not None
        assert updated["collapsed"] is True

    def test_update_folder_position(self, db: ThreadSafeConnection) -> None:
        folder = create_folder(db, "Test")
        updated = update_folder(db, folder["id"], position=5)
        assert updated is not None
        assert updated["position"] == 5

    def test_update_nonexistent_folder(self, db: ThreadSafeConnection) -> None:
        result = update_folder(db, "nonexistent", name="X")
        assert result is None

    def test_delete_folder(self, db: ThreadSafeConnection) -> None:
        folder = create_folder(db, "Doomed")
        assert delete_folder(db, folder["id"]) is True
        assert list_folders(db) == []

    def test_delete_folder_cascades_to_children(self, db: ThreadSafeConnection) -> None:
        parent = create_folder(db, "Parent")
        create_folder(db, "Child", parent_id=parent["id"])
        assert delete_folder(db, parent["id"]) is True
        assert list_folders(db) == []

    def test_delete_folder_unlinks_conversations(self, db: ThreadSafeConnection) -> None:
        folder = create_folder(db, "Folder")
        conv = create_conversation(db, title="Test")
        move_conversation_to_folder(db, conv["id"], folder["id"])
        delete_folder(db, folder["id"])
        reloaded = get_conversation(db, conv["id"])
        assert reloaded is not None
        assert reloaded.get("folder_id") is None

    def test_delete_nonexistent_folder(self, db: ThreadSafeConnection) -> None:
        assert delete_folder(db, "nope") is False

    def test_move_conversation_to_folder(self, db: ThreadSafeConnection) -> None:
        folder = create_folder(db, "Target")
        conv = create_conversation(db, title="Move Me")
        move_conversation_to_folder(db, conv["id"], folder["id"])
        reloaded = get_conversation(db, conv["id"])
        assert reloaded is not None
        assert reloaded["folder_id"] == folder["id"]


# ---------------------------------------------------------------------------
# Tag operations
# ---------------------------------------------------------------------------


class TestTagOperations:
    def test_create_tag(self, db: ThreadSafeConnection) -> None:
        tag = create_tag(db, "important")
        assert tag["name"] == "important"
        assert tag["color"] == "#3b82f6"

    def test_create_tag_custom_color(self, db: ThreadSafeConnection) -> None:
        tag = create_tag(db, "urgent", color="#ff0000")
        assert tag["color"] == "#ff0000"

    def test_list_tags(self, db: ThreadSafeConnection) -> None:
        create_tag(db, "a")
        create_tag(db, "b")
        tags = list_tags(db)
        assert len(tags) == 2

    def test_update_tag_name(self, db: ThreadSafeConnection) -> None:
        tag = create_tag(db, "old")
        updated = update_tag(db, tag["id"], name="new")
        assert updated is not None
        assert updated["name"] == "new"

    def test_update_tag_color(self, db: ThreadSafeConnection) -> None:
        tag = create_tag(db, "test")
        updated = update_tag(db, tag["id"], color="#00ff00")
        assert updated is not None
        assert updated["color"] == "#00ff00"

    def test_update_tag_no_changes(self, db: ThreadSafeConnection) -> None:
        tag = create_tag(db, "stable")
        updated = update_tag(db, tag["id"])
        assert updated is not None
        assert updated["name"] == "stable"

    def test_update_nonexistent_tag(self, db: ThreadSafeConnection) -> None:
        assert update_tag(db, "nope", name="x") is None

    def test_delete_tag(self, db: ThreadSafeConnection) -> None:
        tag = create_tag(db, "doomed")
        assert delete_tag(db, tag["id"]) is True
        assert list_tags(db) == []

    def test_delete_nonexistent_tag(self, db: ThreadSafeConnection) -> None:
        assert delete_tag(db, "nope") is False

    def test_add_tag_to_conversation(self, db: ThreadSafeConnection) -> None:
        conv = create_conversation(db, title="Tagged")
        tag = create_tag(db, "label")
        assert add_tag_to_conversation(db, conv["id"], tag["id"]) is True
        tags = get_conversation_tags(db, conv["id"])
        assert len(tags) == 1
        assert tags[0]["name"] == "label"

    def test_add_duplicate_tag_ignored(self, db: ThreadSafeConnection) -> None:
        conv = create_conversation(db, title="Tagged")
        tag = create_tag(db, "label")
        add_tag_to_conversation(db, conv["id"], tag["id"])
        add_tag_to_conversation(db, conv["id"], tag["id"])
        tags = get_conversation_tags(db, conv["id"])
        assert len(tags) == 1

    def test_remove_tag_from_conversation(self, db: ThreadSafeConnection) -> None:
        conv = create_conversation(db, title="Tagged")
        tag = create_tag(db, "remove-me")
        add_tag_to_conversation(db, conv["id"], tag["id"])
        remove_tag_from_conversation(db, conv["id"], tag["id"])
        tags = get_conversation_tags(db, conv["id"])
        assert len(tags) == 0


# ---------------------------------------------------------------------------
# Usage aggregation
# ---------------------------------------------------------------------------


class TestUsageAggregation:
    def test_conversation_token_total(self, db: ThreadSafeConnection) -> None:
        conv = create_conversation(db, title="Token Test")
        create_message(db, conv["id"], "user", "hi")
        db.execute(
            "UPDATE messages SET total_tokens = 50, prompt_tokens = 30, completion_tokens = 20, model = 'gpt-4'"
            " WHERE conversation_id = ?",
            (conv["id"],),
        )
        db.commit()
        total = get_conversation_token_total(db, conv["id"])
        assert total == 50

    def test_conversation_token_total_empty(self, db: ThreadSafeConnection) -> None:
        conv = create_conversation(db, title="Empty")
        assert get_conversation_token_total(db, conv["id"]) == 0

    def test_daily_token_total(self, db: ThreadSafeConnection) -> None:
        conv = create_conversation(db, title="Daily")
        create_message(db, conv["id"], "user", "msg")
        db.execute(
            "UPDATE messages SET total_tokens = 100, prompt_tokens = 60, completion_tokens = 40, model = 'gpt-4'"
            " WHERE conversation_id = ?",
            (conv["id"],),
        )
        db.commit()
        total = get_daily_token_total(db)
        assert total >= 100

    def test_usage_stats_by_model(self, db: ThreadSafeConnection) -> None:
        conv = create_conversation(db, title="Stats")
        create_message(db, conv["id"], "user", "a")
        create_message(db, conv["id"], "assistant", "b")
        db.execute(
            "UPDATE messages SET total_tokens = 30, prompt_tokens = 20, completion_tokens = 10, model = 'gpt-4'"
            " WHERE conversation_id = ? AND role = 'user'",
            (conv["id"],),
        )
        db.execute(
            "UPDATE messages SET total_tokens = 50, prompt_tokens = 30, completion_tokens = 20, model = 'gpt-4'"
            " WHERE conversation_id = ? AND role = 'assistant'",
            (conv["id"],),
        )
        db.commit()
        stats = get_usage_stats(db)
        assert len(stats) >= 1
        gpt4 = [s for s in stats if s["model"] == "gpt-4"]
        assert len(gpt4) == 1
        assert gpt4[0]["total_tokens"] == 80


# ---------------------------------------------------------------------------
# Conversation forking
# ---------------------------------------------------------------------------


class TestConversationForking:
    def test_fork_creates_copy(self, db: ThreadSafeConnection) -> None:
        conv = create_conversation(db, title="Original")
        create_message(db, conv["id"], "user", "hello")
        create_message(db, conv["id"], "assistant", "hi there")

        forked = fork_conversation(db, conv["id"], up_to_position=1)
        assert forked is not None
        assert forked["id"] != conv["id"]

        forked_msgs = list_messages(db, forked["id"])
        assert len(forked_msgs) == 2

    def test_fork_at_position(self, db: ThreadSafeConnection) -> None:
        conv = create_conversation(db, title="Original")
        create_message(db, conv["id"], "user", "msg1")
        create_message(db, conv["id"], "assistant", "msg2")
        create_message(db, conv["id"], "user", "msg3")

        forked = fork_conversation(db, conv["id"], up_to_position=0)
        assert forked is not None
        forked_msgs = list_messages(db, forked["id"])
        assert len(forked_msgs) == 1


# ---------------------------------------------------------------------------
# Space-scoped listing
# ---------------------------------------------------------------------------


class TestSpaceScopedListing:
    def test_list_conversations_with_space_filter(self, db: ThreadSafeConnection) -> None:
        space_id = "space-123"
        db.execute(
            "INSERT INTO spaces (id, name, source_file, source_hash, created_at, updated_at)"
            " VALUES (?, 'test', '/tmp/test.yaml', 'abc', datetime('now'), datetime('now'))",
            (space_id,),
        )
        db.commit()

        create_conversation(db, title="In Space", space_id=space_id)
        create_conversation(db, title="No Space")

        in_space = list_conversations(db, space_id=space_id)
        assert len(in_space) == 1
        assert in_space[0]["title"] == "In Space"

        all_convs = list_conversations(db)
        assert len(all_convs) == 2
