"""Tests for db.py: ThreadSafeConnection, DatabaseManager, migrations."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from anteroom.db import DatabaseManager, ThreadSafeConnection, init_db

# ---------------------------------------------------------------------------
# ThreadSafeConnection
# ---------------------------------------------------------------------------


class TestThreadSafeConnection:
    def test_execute_and_fetchone(self) -> None:
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        ts = ThreadSafeConnection(conn)
        ts.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, val TEXT)")
        ts.execute("INSERT INTO t VALUES (1, 'hello')")
        ts.commit()
        row = ts.execute_fetchone("SELECT * FROM t WHERE id = ?", (1,))
        assert row is not None
        assert row["val"] == "hello"

    def test_execute_fetchall(self) -> None:
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        ts = ThreadSafeConnection(conn)
        ts.execute("CREATE TABLE t (id INTEGER)")
        ts.execute("INSERT INTO t VALUES (1)")
        ts.execute("INSERT INTO t VALUES (2)")
        ts.commit()
        rows = ts.execute_fetchall("SELECT * FROM t ORDER BY id")
        assert len(rows) == 2

    def test_row_factory_property(self) -> None:
        conn = sqlite3.connect(":memory:")
        ts = ThreadSafeConnection(conn)
        ts.row_factory = sqlite3.Row
        assert ts.row_factory == sqlite3.Row

    def test_transaction_commit(self) -> None:
        conn = sqlite3.connect(":memory:")
        ts = ThreadSafeConnection(conn)
        ts.execute("CREATE TABLE t (id INTEGER)")
        with ts.transaction():
            ts.execute("INSERT INTO t VALUES (1)")
        rows = ts.execute_fetchall("SELECT * FROM t")
        assert len(rows) == 1

    def test_transaction_rollback_on_error(self) -> None:
        conn = sqlite3.connect(":memory:")
        ts = ThreadSafeConnection(conn)
        ts.execute("CREATE TABLE t (id INTEGER PRIMARY KEY)")
        ts.commit()
        ts.execute("INSERT INTO t VALUES (1)")
        ts.commit()

        with pytest.raises(sqlite3.IntegrityError):
            with ts.transaction():
                ts.execute("INSERT INTO t VALUES (1)")

        rows = ts.execute_fetchall("SELECT * FROM t")
        assert len(rows) == 1

    def test_executescript(self) -> None:
        conn = sqlite3.connect(":memory:")
        ts = ThreadSafeConnection(conn)
        ts.executescript("CREATE TABLE t1 (id INTEGER); CREATE TABLE t2 (id INTEGER);")
        ts.execute("INSERT INTO t1 VALUES (1)")
        ts.execute("INSERT INTO t2 VALUES (2)")
        ts.commit()

    def test_close(self) -> None:
        conn = sqlite3.connect(":memory:")
        ts = ThreadSafeConnection(conn)
        ts.close()
        with pytest.raises(Exception):
            ts.execute("SELECT 1")


# ---------------------------------------------------------------------------
# DatabaseManager
# ---------------------------------------------------------------------------


class TestDatabaseManager:
    def test_add_and_get(self, tmp_path: Path) -> None:
        dm = DatabaseManager()
        db_path = tmp_path / "test.db"
        dm.add("test", db_path)
        db = dm.get("test")
        assert db is not None

    def test_get_default_returns_personal(self, tmp_path: Path) -> None:
        dm = DatabaseManager()
        db_path = tmp_path / "personal.db"
        dm.add("personal", db_path)
        assert dm.get() is dm.personal

    def test_get_nonexistent_raises(self) -> None:
        dm = DatabaseManager()
        with pytest.raises(KeyError, match="not found"):
            dm.get("nonexistent")

    def test_list_databases(self, tmp_path: Path) -> None:
        dm = DatabaseManager()
        dm.add("personal", tmp_path / "personal.db")
        dm.add("team", tmp_path / "team.db")
        result = dm.list_databases()
        names = [r["name"] for r in result]
        assert "personal" in names
        assert "team" in names

    def test_remove(self, tmp_path: Path) -> None:
        dm = DatabaseManager()
        dm.add("temp", tmp_path / "temp.db")
        dm.remove("temp")
        with pytest.raises(KeyError):
            dm.get("temp")

    def test_close_all(self, tmp_path: Path) -> None:
        dm = DatabaseManager()
        dm.add("personal", tmp_path / "p.db")
        dm.add("shared", tmp_path / "s.db")
        dm.close_all()
        assert len(dm.list_databases()) == 0

    def test_passphrase_hash(self, tmp_path: Path) -> None:
        dm = DatabaseManager()
        dm.add("secure", tmp_path / "secure.db", passphrase_hash="abc123")
        assert dm.get_passphrase_hash("secure") == "abc123"
        assert dm.requires_auth("secure") is True

    def test_no_passphrase_no_auth(self, tmp_path: Path) -> None:
        dm = DatabaseManager()
        dm.add("open", tmp_path / "open.db")
        assert dm.get_passphrase_hash("open") == ""
        assert dm.requires_auth("open") is False


# ---------------------------------------------------------------------------
# init_db — schema creation on fresh database
# ---------------------------------------------------------------------------


class TestInitDb:
    def test_fresh_db_creates_tables(self, tmp_path: Path) -> None:
        db_path = tmp_path / "fresh.db"
        ts = init_db(db_path)
        tables = [r[0] for r in ts.execute_fetchall("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        assert "conversations" in tables
        assert "messages" in tables
        assert "spaces" in tables
        assert "artifacts" in tables
        assert "packs" in tables
        ts.close()

    def test_fresh_db_has_wal_mode(self, tmp_path: Path) -> None:
        db_path = tmp_path / "wal.db"
        ts = init_db(db_path)
        row = ts.execute_fetchone("PRAGMA journal_mode")
        assert row is not None
        assert row[0] == "wal"
        ts.close()

    def test_fresh_db_has_foreign_keys(self, tmp_path: Path) -> None:
        db_path = tmp_path / "fk.db"
        ts = init_db(db_path)
        row = ts.execute_fetchone("PRAGMA foreign_keys")
        assert row is not None
        assert row[0] == 1
        ts.close()

    def test_idempotent_init(self, tmp_path: Path) -> None:
        db_path = tmp_path / "idem.db"
        ts1 = init_db(db_path)
        ts1.close()
        ts2 = init_db(db_path)
        tables = [r[0] for r in ts2.execute_fetchall("SELECT name FROM sqlite_master WHERE type='table'")]
        assert "conversations" in tables
        ts2.close()

    def test_workflow_tables_created(self, tmp_path: Path) -> None:
        db_path = tmp_path / "wf.db"
        ts = init_db(db_path)
        tables = [r[0] for r in ts.execute_fetchall("SELECT name FROM sqlite_master WHERE type='table'")]
        assert "workflow_runs" in tables
        assert "workflow_steps" in tables
        assert "workflow_events" in tables
        ts.close()

    def test_fts_tables_created(self, tmp_path: Path) -> None:
        db_path = tmp_path / "fts.db"
        ts = init_db(db_path)
        tables = [r[0] for r in ts.execute_fetchall("SELECT name FROM sqlite_master WHERE type='table'")]
        assert "conversations_fts" in tables
        assert "messages_fts" in tables
        ts.close()
