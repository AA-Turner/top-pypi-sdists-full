"""Tests for durable output storage and inspection (#1312)."""

from __future__ import annotations

import sqlite3
import uuid
from pathlib import Path

from anteroom.services.task_output import (
    cleanup_conversation_task_output,
    ensure_task_output_dir,
    preview_from_file,
    purge_orphaned_task_output,
    read_task_output,
    stderr_path,
    stdout_path,
    task_output_dir,
    truncate_output_file,
    update_task_output_paths,
)


def _create_test_db(tmp_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(tmp_path / "test.db"))
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
        CREATE TABLE background_tasks (
            id TEXT PRIMARY KEY,
            conversation_id TEXT NOT NULL,
            command TEXT,
            status TEXT,
            preview TEXT,
            stdout_path TEXT DEFAULT NULL,
            stderr_path TEXT DEFAULT NULL,
            created_at TEXT,
            completed_at TEXT
        );
        """
    )
    conn.commit()
    return conn


class TestPathHelpers:
    def test_task_output_dir(self, tmp_path: Path) -> None:
        result = task_output_dir(tmp_path, "conv-123")
        assert result == tmp_path / "task_output" / "conv-123"

    def test_ensure_task_output_dir_creates(self, tmp_path: Path) -> None:
        out_dir = ensure_task_output_dir(tmp_path, "conv-abc")
        assert out_dir.exists()
        assert out_dir.is_dir()

    def test_stdout_path(self, tmp_path: Path) -> None:
        result = stdout_path(tmp_path, "conv-1", "task-1")
        assert result == tmp_path / "task_output" / "conv-1" / "task-1.stdout"

    def test_stderr_path(self, tmp_path: Path) -> None:
        result = stderr_path(tmp_path, "conv-1", "task-1")
        assert result == tmp_path / "task_output" / "conv-1" / "task-1.stderr"


class TestReadTaskOutput:
    def test_read_nonexistent_file(self, tmp_path: Path) -> None:
        result = read_task_output(tmp_path / "missing.stdout")
        assert result == ""

    def test_read_full_file(self, tmp_path: Path) -> None:
        f = tmp_path / "output.stdout"
        f.write_text("line1\nline2\nline3\n")
        result = read_task_output(f)
        assert result == "line1\nline2\nline3\n"

    def test_read_with_tail(self, tmp_path: Path) -> None:
        f = tmp_path / "output.stdout"
        f.write_text("line1\nline2\nline3\nline4\nline5\n")
        result = read_task_output(f, tail_lines=2)
        assert "line4\n" in result
        assert "line5\n" in result
        assert "line1\n" not in result

    def test_tail_more_than_file(self, tmp_path: Path) -> None:
        f = tmp_path / "output.stdout"
        f.write_text("line1\nline2\n")
        result = read_task_output(f, tail_lines=100)
        assert result == "line1\nline2\n"

    def test_tail_zero_returns_full(self, tmp_path: Path) -> None:
        f = tmp_path / "output.stdout"
        f.write_text("hello\nworld\n")
        result = read_task_output(f, tail_lines=0)
        assert result == "hello\nworld\n"


class TestTruncateOutputFile:
    def test_no_truncation_for_small_file(self, tmp_path: Path) -> None:
        f = tmp_path / "small.stdout"
        f.write_text("small output")
        truncate_output_file(f, max_size=1000)
        assert f.read_text() == "small output"

    def test_truncation_keeps_tail(self, tmp_path: Path) -> None:
        f = tmp_path / "big.stdout"
        lines = [f"line{i}\n" for i in range(1000)]
        f.write_text("".join(lines))
        original_size = f.stat().st_size
        assert original_size > 500

        truncate_output_file(f, max_size=500)
        truncated = f.read_text()
        assert len(truncated.encode()) <= 600  # allow for line boundary alignment
        assert "line999\n" in truncated

    def test_truncation_nonexistent_file(self, tmp_path: Path) -> None:
        truncate_output_file(tmp_path / "missing.stdout")


class TestPreviewFromFile:
    def test_preview_last_lines(self, tmp_path: Path) -> None:
        f = tmp_path / "output.stdout"
        f.write_text("a\nb\nc\nd\ne\nf\n")
        result = preview_from_file(f, lines=3)
        assert "d" in result
        assert "e" in result
        assert "f" in result

    def test_preview_nonexistent(self, tmp_path: Path) -> None:
        result = preview_from_file(tmp_path / "nope")
        assert result == ""


class TestUpdateTaskOutputPaths:
    def test_stores_paths_in_db(self, tmp_path: Path) -> None:
        conn = _create_test_db(tmp_path)
        conn.execute(
            "INSERT INTO background_tasks (id, conversation_id, status, created_at) VALUES (?, ?, ?, ?)",
            ("task-1", "conv-1", "running", "2026-01-01T00:00:00"),
        )
        conn.commit()

        update_task_output_paths(conn, "task-1", "/path/to/stdout", "/path/to/stderr")

        row = conn.execute("SELECT stdout_path, stderr_path FROM background_tasks WHERE id = ?", ("task-1",)).fetchone()
        assert row["stdout_path"] == "/path/to/stdout"
        assert row["stderr_path"] == "/path/to/stderr"


class TestPurgeOrphanedTaskOutput:
    def test_removes_orphaned_dirs(self, tmp_path: Path) -> None:
        conn = _create_test_db(tmp_path)
        active_id = str(uuid.uuid4())
        orphan_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO conversations (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (active_id, "active", "2026-01-01", "2026-01-01"),
        )
        conn.commit()

        active_dir = tmp_path / "task_output" / active_id
        active_dir.mkdir(parents=True)
        orphan_dir = tmp_path / "task_output" / orphan_id
        orphan_dir.mkdir(parents=True)
        (orphan_dir / "task.stdout").write_text("output")

        count = purge_orphaned_task_output(tmp_path, conn)
        assert count == 1
        assert not orphan_dir.exists()
        assert active_dir.exists()

    def test_no_task_output_dir(self, tmp_path: Path) -> None:
        conn = _create_test_db(tmp_path)
        count = purge_orphaned_task_output(tmp_path, conn)
        assert count == 0

    def test_skips_non_uuid_dirs(self, tmp_path: Path) -> None:
        conn = _create_test_db(tmp_path)
        bad_dir = tmp_path / "task_output" / "not-a-uuid"
        bad_dir.mkdir(parents=True)
        count = purge_orphaned_task_output(tmp_path, conn)
        assert count == 0
        assert bad_dir.exists()

    def test_dry_run(self, tmp_path: Path) -> None:
        conn = _create_test_db(tmp_path)
        orphan_id = str(uuid.uuid4())
        orphan_dir = tmp_path / "task_output" / orphan_id
        orphan_dir.mkdir(parents=True)

        count = purge_orphaned_task_output(tmp_path, conn, dry_run=True)
        assert count == 1
        assert orphan_dir.exists()


class TestCleanupConversationTaskOutput:
    def test_removes_task_output_dir(self, tmp_path: Path) -> None:
        conv_id = str(uuid.uuid4())
        out_dir = tmp_path / "task_output" / conv_id
        out_dir.mkdir(parents=True)
        (out_dir / "task.stdout").write_text("output")

        cleanup_conversation_task_output(tmp_path, conv_id)
        assert not out_dir.exists()

    def test_noop_for_missing_dir(self, tmp_path: Path) -> None:
        conv_id = str(uuid.uuid4())
        cleanup_conversation_task_output(tmp_path, conv_id)

    def test_rejects_non_uuid(self, tmp_path: Path) -> None:
        bad_dir = tmp_path / "task_output" / "../../etc"
        bad_dir.mkdir(parents=True, exist_ok=True)
        cleanup_conversation_task_output(tmp_path, "../../etc")
        # Should not attempt to delete
