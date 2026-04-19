"""Tests for data retention policy enforcement."""

from __future__ import annotations

import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.services.retention import (
    RetentionWorker,
    purge_conversations_before,
    purge_orphaned_attachments,
    purge_orphaned_sources,
)


def _create_test_db(tmp_path: Path) -> sqlite3.Connection:
    """Create a minimal test database with conversations and messages tables."""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(
        """
        CREATE TABLE conversations (
            id TEXT PRIMARY KEY,
            title TEXT,
            created_at TEXT,
            updated_at TEXT
        );
        CREATE TABLE messages (
            id TEXT PRIMARY KEY,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
        );
        """
    )
    conn.commit()
    return conn


def _insert_conversation(conn: sqlite3.Connection, cid: str, updated_at: str) -> None:
    conn.execute(
        "INSERT INTO conversations (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
        (cid, f"Test {cid}", updated_at, updated_at),
    )
    conn.execute(
        "INSERT INTO messages (id, conversation_id, role, content, created_at) VALUES (?, ?, ?, ?, ?)",
        (str(uuid.uuid4()), cid, "user", "hello", updated_at),
    )
    conn.commit()


class TestPurgeConversationsBefore:
    def test_purges_old_conversations(self, tmp_path: Path) -> None:
        conn = _create_test_db(tmp_path)
        old_date = "2024-01-01T00:00:00"
        new_date = "2026-01-01T00:00:00"
        _insert_conversation(conn, "old-conv", old_date)
        _insert_conversation(conn, "new-conv", new_date)

        cutoff = datetime(2025, 6, 1, tzinfo=timezone.utc)
        count = purge_conversations_before(conn, cutoff, tmp_path)

        assert count == 1
        rows = conn.execute("SELECT id FROM conversations").fetchall()
        assert len(rows) == 1
        assert rows[0]["id"] == "new-conv"

    def test_cascade_deletes_messages(self, tmp_path: Path) -> None:
        conn = _create_test_db(tmp_path)
        _insert_conversation(conn, "old-conv", "2024-01-01T00:00:00")

        cutoff = datetime(2025, 1, 1, tzinfo=timezone.utc)
        purge_conversations_before(conn, cutoff, tmp_path)

        msgs = conn.execute("SELECT id FROM messages").fetchall()
        assert len(msgs) == 0

    def test_no_purge_when_all_recent(self, tmp_path: Path) -> None:
        conn = _create_test_db(tmp_path)
        _insert_conversation(conn, "recent", "2026-06-01T00:00:00")

        cutoff = datetime(2025, 1, 1, tzinfo=timezone.utc)
        count = purge_conversations_before(conn, cutoff, tmp_path)

        assert count == 0
        rows = conn.execute("SELECT id FROM conversations").fetchall()
        assert len(rows) == 1

    def test_purge_empty_db(self, tmp_path: Path) -> None:
        conn = _create_test_db(tmp_path)
        cutoff = datetime(2025, 1, 1, tzinfo=timezone.utc)
        count = purge_conversations_before(conn, cutoff, tmp_path)
        assert count == 0

    def test_dry_run_does_not_delete(self, tmp_path: Path) -> None:
        conn = _create_test_db(tmp_path)
        _insert_conversation(conn, "old-conv", "2024-01-01T00:00:00")

        cutoff = datetime(2025, 6, 1, tzinfo=timezone.utc)
        count = purge_conversations_before(conn, cutoff, tmp_path, dry_run=True)

        assert count == 1
        rows = conn.execute("SELECT id FROM conversations").fetchall()
        assert len(rows) == 1  # Still there

    def test_deletes_attachment_files(self, tmp_path: Path) -> None:
        conn = _create_test_db(tmp_path)
        cid = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        _insert_conversation(conn, cid, "2024-01-01T00:00:00")

        att_dir = tmp_path / "attachments" / cid
        att_dir.mkdir(parents=True)
        (att_dir / "file.txt").write_text("hello")

        cutoff = datetime(2025, 6, 1, tzinfo=timezone.utc)
        purge_conversations_before(conn, cutoff, tmp_path, purge_attachments=True)

        assert not att_dir.exists()

    def test_skips_attachment_deletion_when_disabled(self, tmp_path: Path) -> None:
        conn = _create_test_db(tmp_path)
        cid = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        _insert_conversation(conn, cid, "2024-01-01T00:00:00")

        att_dir = tmp_path / "attachments" / cid
        att_dir.mkdir(parents=True)
        (att_dir / "file.txt").write_text("hello")

        cutoff = datetime(2025, 6, 1, tzinfo=timezone.utc)
        purge_conversations_before(conn, cutoff, tmp_path, purge_attachments=False)

        assert att_dir.exists()

    def test_skips_attachment_for_non_uuid_id(self, tmp_path: Path) -> None:
        """Non-UUID conversation IDs are purged from DB but attachments are not deleted."""
        conn = _create_test_db(tmp_path)
        _insert_conversation(conn, "../../etc", "2024-01-01T00:00:00")

        att_dir = tmp_path / "attachments" / "../../etc"
        att_dir.mkdir(parents=True, exist_ok=True)

        cutoff = datetime(2025, 6, 1, tzinfo=timezone.utc)
        count = purge_conversations_before(conn, cutoff, tmp_path, purge_attachments=True)

        assert count == 1  # DB row deleted
        # Attachment dir NOT deleted because ID is not a valid UUID
        assert att_dir.exists()


class TestPurgeOrphanedAttachments:
    def test_removes_orphaned_directories(self, tmp_path: Path) -> None:
        conn = _create_test_db(tmp_path)
        active_id = "a1b2c3d4-1111-2222-3333-444444444444"
        orphan_id = "b2c3d4e5-5555-6666-7777-888888888888"
        _insert_conversation(conn, active_id, "2026-01-01T00:00:00")

        # Active conversation's attachments
        active_dir = tmp_path / "attachments" / active_id
        active_dir.mkdir(parents=True)

        # Orphaned directory (no matching conversation)
        orphan_dir = tmp_path / "attachments" / orphan_id
        orphan_dir.mkdir(parents=True)
        (orphan_dir / "leftover.txt").write_text("orphan")

        count = purge_orphaned_attachments(tmp_path, conn)

        assert count == 1
        assert not orphan_dir.exists()
        assert active_dir.exists()

    def test_no_orphans(self, tmp_path: Path) -> None:
        conn = _create_test_db(tmp_path)
        active_id = "a1b2c3d4-1111-2222-3333-444444444444"
        _insert_conversation(conn, active_id, "2026-01-01T00:00:00")
        att_dir = tmp_path / "attachments" / active_id
        att_dir.mkdir(parents=True)

        count = purge_orphaned_attachments(tmp_path, conn)
        assert count == 0

    def test_no_attachments_dir(self, tmp_path: Path) -> None:
        conn = _create_test_db(tmp_path)
        count = purge_orphaned_attachments(tmp_path, conn)
        assert count == 0

    def test_dry_run_does_not_remove(self, tmp_path: Path) -> None:
        conn = _create_test_db(tmp_path)
        orphan_id = "c3d4e5f6-9999-aaaa-bbbb-cccccccccccc"
        orphan_dir = tmp_path / "attachments" / orphan_id
        orphan_dir.mkdir(parents=True)

        count = purge_orphaned_attachments(tmp_path, conn, dry_run=True)
        assert count == 1
        assert orphan_dir.exists()

    def test_skips_non_uuid_directory_names(self, tmp_path: Path) -> None:
        """Non-UUID directory names under attachments/ are ignored."""
        conn = _create_test_db(tmp_path)
        bad_dir = tmp_path / "attachments" / "not-a-uuid"
        bad_dir.mkdir(parents=True)

        count = purge_orphaned_attachments(tmp_path, conn)
        assert count == 0
        assert bad_dir.exists()


class TestRetentionWorker:
    def test_init_defaults(self, tmp_path: Path) -> None:
        db = MagicMock()
        worker = RetentionWorker(db, tmp_path, retention_days=30)
        assert worker.retention_days == 30
        assert worker.running is False

    def test_clamps_check_interval(self, tmp_path: Path) -> None:
        db = MagicMock()
        worker = RetentionWorker(db, tmp_path, retention_days=30, check_interval=10)
        assert worker._check_interval == 60  # clamped to minimum

    @pytest.mark.asyncio
    async def test_run_once_purges(self, tmp_path: Path) -> None:
        conn = _create_test_db(tmp_path)
        _insert_conversation(conn, "old", "2024-01-01T00:00:00")
        _insert_conversation(conn, "new", "2026-06-01T00:00:00")

        worker = RetentionWorker(conn, tmp_path, retention_days=30)
        count = await worker.run_once()

        assert count == 1
        rows = conn.execute("SELECT id FROM conversations").fetchall()
        assert len(rows) == 1

    @pytest.mark.asyncio
    async def test_run_once_nothing_to_purge(self, tmp_path: Path) -> None:
        conn = _create_test_db(tmp_path)
        _insert_conversation(conn, "recent", "2026-06-01T00:00:00")

        worker = RetentionWorker(conn, tmp_path, retention_days=30)
        count = await worker.run_once()
        assert count == 0

    @pytest.mark.asyncio
    async def test_start_and_stop(self, tmp_path: Path) -> None:
        db = MagicMock()
        worker = RetentionWorker(db, tmp_path, retention_days=30)

        with patch.object(worker, "run_forever", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = None
            worker.start()
            assert worker._task is not None
            worker.stop()
            assert worker._running is False

    def test_backoff_on_failure(self, tmp_path: Path) -> None:
        db = MagicMock()
        worker = RetentionWorker(db, tmp_path, retention_days=30, check_interval=100)

        worker._apply_backoff()
        assert worker._consecutive_failures == 1
        assert worker._current_interval > 100

        worker._reset_backoff()
        assert worker._consecutive_failures == 0
        assert worker._current_interval == 100.0

    @pytest.mark.asyncio
    async def test_retention_days_zero_skips_conversation_branch(self, tmp_path: Path) -> None:
        """With retention_days=0 the conversation branch is a no-op.

        Before #625 the worker was only started when retention_days>0,
        so this case wasn't reachable in production. #625 starts the
        worker for memory-only retention (retention_days=0 +
        memory.retention.enabled=True). An unguarded
        ``cutoff = now - timedelta(days=0)`` would match every
        conversation whose created_at < now — catastrophic. The new
        ``if self._retention_days > 0:`` guard in run_once() makes the
        conversation branch a no-op in this mode. This test pins that
        safety invariant.
        """
        conn = _create_test_db(tmp_path)
        _insert_conversation(conn, "old", "2020-01-01T00:00:00")

        worker = RetentionWorker(conn, tmp_path, retention_days=0)
        count = await worker.run_once()

        # No conversations touched (guard active).
        assert count == 0
        survived = conn.execute("SELECT id FROM conversations WHERE id = ?", ("old",)).fetchone()
        assert survived is not None

    @pytest.mark.asyncio
    async def test_run_forever_disables_after_max_failures(self, tmp_path: Path) -> None:
        """Worker stops after MAX_CONSECUTIVE_FAILURES errors."""
        from anteroom.services.retention import MAX_CONSECUTIVE_FAILURES

        db = MagicMock()
        worker = RetentionWorker(db, tmp_path, retention_days=30, check_interval=60)

        call_count = 0

        async def _failing_run_once() -> int:
            nonlocal call_count
            call_count += 1
            raise RuntimeError("db error")

        with patch.object(worker, "run_once", side_effect=_failing_run_once):
            with patch("asyncio.sleep", new_callable=AsyncMock):
                await worker.run_forever()

        assert call_count == MAX_CONSECUTIVE_FAILURES
        assert worker._consecutive_failures == MAX_CONSECUTIVE_FAILURES

    @pytest.mark.asyncio
    async def test_run_forever_resets_backoff_on_success(self, tmp_path: Path) -> None:
        """Worker resets backoff after a successful run following failures."""
        db = MagicMock()
        worker = RetentionWorker(db, tmp_path, retention_days=30, check_interval=60)

        # Simulate: fail once, then succeed, then stop
        call_count = 0

        async def _fail_then_succeed() -> int:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise RuntimeError("transient error")
            # On second call, stop the worker to exit the loop
            worker._running = False
            return 0

        with patch.object(worker, "run_once", side_effect=_fail_then_succeed):
            with patch("asyncio.sleep", new_callable=AsyncMock):
                await worker.run_forever()

        assert call_count == 2
        assert worker._consecutive_failures == 0  # reset after success

    def test_purge_conversation_without_attachment_dir(self, tmp_path: Path) -> None:
        """Purge succeeds even when no attachment directory exists for the conversation."""
        conn = _create_test_db(tmp_path)
        _insert_conversation(conn, "old-no-att", "2024-01-01T00:00:00")

        # No attachments directory created
        cutoff = datetime(2025, 6, 1, tzinfo=timezone.utc)
        count = purge_conversations_before(conn, cutoff, tmp_path, purge_attachments=True)

        assert count == 1
        rows = conn.execute("SELECT id FROM conversations").fetchall()
        assert len(rows) == 0


class TestRetentionPurgesTaskOutput:
    @pytest.mark.asyncio
    async def test_run_once_purges_orphaned_task_output(self, tmp_path: Path) -> None:
        conn = _create_test_db(tmp_path)
        _insert_conversation(conn, "active", "2026-06-01T00:00:00")

        orphan_id = "b2c3d4e5-5555-6666-7777-888888888888"
        orphan_dir = tmp_path / "task_output" / orphan_id
        orphan_dir.mkdir(parents=True)
        (orphan_dir / "task.stdout").write_text("orphaned output")

        worker = RetentionWorker(conn, tmp_path, retention_days=30)
        count = await worker.run_once()

        assert count >= 1
        assert not orphan_dir.exists()


class TestPurgeOrphanedSkipsFiles:
    def test_skips_non_directory_entries(self, tmp_path: Path) -> None:
        """Files directly in attachments root are not counted as orphaned dirs."""
        conn = _create_test_db(tmp_path)
        att_root = tmp_path / "attachments"
        att_root.mkdir()
        (att_root / "stray-file.txt").write_text("not a dir")

        count = purge_orphaned_attachments(tmp_path, conn)
        assert count == 0
        assert (att_root / "stray-file.txt").exists()


def _create_test_db_with_sources(tmp_path: Path) -> sqlite3.Connection:
    conn = _create_test_db(tmp_path)
    conn.execute("CREATE TABLE sources (id TEXT PRIMARY KEY, type TEXT, title TEXT)")
    conn.commit()
    return conn


class TestPurgeOrphanedSources:
    def test_removes_orphaned_source_dirs(self, tmp_path: Path) -> None:
        conn = _create_test_db_with_sources(tmp_path)
        orphan_id = str(uuid.uuid4())
        src_dir = tmp_path / "sources" / orphan_id
        src_dir.mkdir(parents=True)
        (src_dir / "file.txt").write_text("test")

        count = purge_orphaned_sources(tmp_path, conn)
        assert count == 1
        assert not src_dir.exists()

    def test_keeps_source_dirs_with_db_record(self, tmp_path: Path) -> None:
        conn = _create_test_db_with_sources(tmp_path)
        source_id = str(uuid.uuid4())
        conn.execute("INSERT INTO sources (id, type, title) VALUES (?, 'file', 'test')", (source_id,))
        conn.commit()
        src_dir = tmp_path / "sources" / source_id
        src_dir.mkdir(parents=True)
        (src_dir / "file.txt").write_text("test")

        count = purge_orphaned_sources(tmp_path, conn)
        assert count == 0
        assert src_dir.exists()

    def test_noop_when_sources_dir_missing(self, tmp_path: Path) -> None:
        conn = _create_test_db_with_sources(tmp_path)
        count = purge_orphaned_sources(tmp_path, conn)
        assert count == 0

    def test_dry_run_does_not_delete(self, tmp_path: Path) -> None:
        conn = _create_test_db_with_sources(tmp_path)
        orphan_id = str(uuid.uuid4())
        src_dir = tmp_path / "sources" / orphan_id
        src_dir.mkdir(parents=True)

        count = purge_orphaned_sources(tmp_path, conn, dry_run=True)
        assert count == 1
        assert src_dir.exists()


# ---------------------------------------------------------------------------
# #625 — run_once() wiring for memory retention
# ---------------------------------------------------------------------------


def _full_schema_db(tmp_path: Path):  # type: ignore[no-untyped-def]
    """Return a ThreadSafeConnection wrapping the full anteroom schema.

    The conversation-retention tests above use a minimal two-table
    schema. The memory-retention branch needs the artifacts tables, so
    the worker-wiring tests use the canonical schema instead.
    """
    from anteroom.db import _SCHEMA, ThreadSafeConnection

    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


class TestRunOnceMemoryBranch:
    @pytest.mark.asyncio
    async def test_memory_only_retention_does_not_purge_conversations(self, tmp_path: Path) -> None:
        """Regression for the load-bearing retention_days > 0 guard.

        With retention_days=0 and memory.retention.enabled=True, an
        unguarded ``cutoff = now - timedelta(days=0)`` would match every
        conversation. The guard must make the conversation branch a
        no-op and let only the memory branch run.
        """
        from anteroom.config import MemoryRetentionConfig
        from anteroom.services.memory_service import (
            create_memory,
            update_memory_metadata,
        )
        from anteroom.services.retention import RetentionWorker

        db = _full_schema_db(tmp_path)
        conv_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        db.execute(
            "INSERT INTO conversations (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (conv_id, "survivor", "2026-01-01T00:00:00+00:00", "2026-01-01T00:00:00+00:00"),
        )
        art = create_memory(db, "junk", scope="user", category="preference", name="mr1")
        update_memory_metadata(db, art["fqn"], memory_status="rejected")
        db.commit()

        worker = RetentionWorker(
            db=db,
            data_dir=tmp_path,
            retention_days=0,  # memory-only mode
            memory_retention_config=MemoryRetentionConfig(enabled=True, purge_statuses=["rejected"]),
        )
        total = await worker.run_once()

        assert total == 1
        # Conversation is UNCHANGED — this is the regression we're guarding.
        row = db.execute("SELECT id FROM conversations WHERE id = ?", (conv_id,)).fetchone()
        assert row is not None

    @pytest.mark.asyncio
    async def test_conversation_retention_runs_without_memory_config(self, tmp_path: Path) -> None:
        from anteroom.services.retention import RetentionWorker

        db = _full_schema_db(tmp_path)
        worker = RetentionWorker(
            db=db,
            data_dir=tmp_path,
            retention_days=30,
        )
        assert await worker.run_once() == 0

    @pytest.mark.asyncio
    async def test_both_branches_run_together(self, tmp_path: Path) -> None:
        from anteroom.config import MemoryRetentionConfig
        from anteroom.services.memory_service import (
            create_memory,
            update_memory_metadata,
        )
        from anteroom.services.retention import RetentionWorker

        db = _full_schema_db(tmp_path)
        art = create_memory(db, "x", scope="user", category="preference", name="both1")
        update_memory_metadata(db, art["fqn"], memory_status="rejected")

        worker = RetentionWorker(
            db=db,
            data_dir=tmp_path,
            retention_days=30,
            memory_retention_config=MemoryRetentionConfig(enabled=True, purge_statuses=["rejected"]),
        )
        total = await worker.run_once()
        assert total >= 1

    @pytest.mark.asyncio
    async def test_memory_branch_failure_does_not_abort_conversation_branch(self, tmp_path: Path) -> None:
        from anteroom.config import MemoryRetentionConfig
        from anteroom.services.retention import RetentionWorker

        db = _full_schema_db(tmp_path)
        worker = RetentionWorker(
            db=db,
            data_dir=tmp_path,
            retention_days=30,
            memory_retention_config=MemoryRetentionConfig(enabled=True, purge_statuses=["rejected"]),
        )
        with patch(
            "anteroom.services.memory_retention.purge_memories",
            side_effect=RuntimeError("boom"),
        ):
            total = await worker.run_once()
        assert total == 0

    @pytest.mark.asyncio
    async def test_audit_writer_is_threaded_to_purge(self, tmp_path: Path) -> None:
        from anteroom.config import MemoryRetentionConfig
        from anteroom.services.memory_service import (
            create_memory,
            update_memory_metadata,
        )
        from anteroom.services.retention import RetentionWorker

        db = _full_schema_db(tmp_path)
        art = create_memory(db, "x", scope="user", category="preference", name="aw1")
        update_memory_metadata(db, art["fqn"], memory_status="rejected")

        audit_writer = MagicMock()
        worker = RetentionWorker(
            db=db,
            data_dir=tmp_path,
            retention_days=0,
            memory_retention_config=MemoryRetentionConfig(enabled=True, purge_statuses=["rejected"]),
            audit_writer=audit_writer,
        )
        await worker.run_once()
        assert audit_writer.emit.call_count == 1
        entry = audit_writer.emit.call_args.args[0]
        assert entry.event_type == "memory.purge"
