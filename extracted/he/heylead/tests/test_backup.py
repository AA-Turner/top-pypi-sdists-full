"""Tests for database backup and restore utilities."""

from __future__ import annotations

import sqlite3
import time

from heylead import config
from heylead.db import schema
from heylead.db.backup import (
    BackupInfo,
    create_backup,
    list_backups,
    restore_backup,
    rotate_backups,
)


class TestCreateBackup:
    def test_creates_backup_file(self):
        # Initialize DB with some data
        db = schema.get_db()
        db.execute(
            "INSERT INTO campaigns (id, name, status, icp_json, created_at) "
            "VALUES ('c1', 'Test', 'active', '{}', 1000)"
        )
        db.execute(
            "INSERT INTO contacts (id, campaign_id, name, title, company, linkedin_url, status, created_at) "
            "VALUES ('x1', 'c1', 'Alice', 'CEO', 'Acme', 'https://linkedin.com/in/alice', 'pending', 1000)"
        )
        db.commit()

        path = create_backup("test")
        assert path is not None
        assert path.exists()
        assert path.name.startswith("heylead-")
        assert path.name.endswith("-test.db")
        assert path.stat().st_size > 0

    def test_backup_contains_data(self):
        db = schema.get_db()
        db.execute(
            "INSERT INTO campaigns (id, name, status, icp_json, created_at) "
            "VALUES ('c1', 'Test', 'active', '{}', 1000)"
        )
        db.execute(
            "INSERT INTO contacts (id, campaign_id, name, title, company, linkedin_url, status, created_at) "
            "VALUES ('x1', 'c1', 'Alice', 'CEO', 'Acme', 'https://linkedin.com/in/alice', 'pending', 1000)"
        )
        db.commit()

        path = create_backup("verify")
        # Open backup independently and check data
        conn = sqlite3.connect(str(path))
        row = conn.execute("SELECT name FROM contacts WHERE id='x1'").fetchone()
        conn.close()
        assert row is not None
        assert row[0] == "Alice"

    def test_returns_none_when_no_db(self):
        # DB file doesn't exist yet (no get_db() call)
        db_path = config.db_path()
        if db_path.exists():
            db_path.unlink()
        result = create_backup("empty")
        assert result is None

    def test_sanitizes_reason(self):
        db = schema.get_db()
        path = create_backup("pre reset/test")
        assert path is not None
        assert "pre-reset-test" in path.name


class TestListBackups:
    def test_empty_when_no_backups(self):
        assert list_backups() == []

    def test_lists_created_backups(self):
        schema.get_db()  # Ensure DB exists
        create_backup("first")
        time.sleep(0.1)
        create_backup("second")

        backups = list_backups()
        assert len(backups) == 2
        # Newest first
        assert backups[0].reason == "second"
        assert backups[1].reason == "first"

    def test_returns_backup_info(self):
        schema.get_db()
        create_backup("info-test")

        backups = list_backups()
        assert len(backups) == 1
        b = backups[0]
        assert isinstance(b, BackupInfo)
        assert b.reason == "info-test"
        assert b.size_bytes > 0
        assert b.timestamp > 0


class TestRestoreBackup:
    def test_restores_data(self):
        db = schema.get_db()
        db.execute(
            "INSERT INTO campaigns (id, name, status, icp_json, created_at) "
            "VALUES ('c1', 'OrigCampaign', 'active', '{}', 1000)"
        )
        db.commit()

        # Create backup with this data
        backup_path = create_backup("restore-test")

        # Delete original data
        db.execute("DELETE FROM campaigns")
        db.commit()
        row = db.execute("SELECT COUNT(*) FROM campaigns").fetchone()
        assert row[0] == 0

        # Restore
        restore_backup(backup_path)

        # Re-open DB and verify
        db2 = schema.get_db()
        row = db2.execute("SELECT name FROM campaigns WHERE id='c1'").fetchone()
        assert row is not None
        assert row[0] == "OrigCampaign"

    def test_raises_on_missing_backup(self):
        from pathlib import Path

        import pytest

        with pytest.raises(FileNotFoundError):
            restore_backup(Path("/nonexistent/backup.db"))


class TestRotateBackups:
    def test_keeps_only_n_backups(self):
        schema.get_db()
        for i in range(7):
            create_backup(f"rot-{i}")
            time.sleep(0.05)  # Ensure distinct timestamps

        assert len(list_backups()) == 7

        removed = rotate_backups(keep=5)
        assert removed == 2
        assert len(list_backups()) == 5

    def test_no_op_when_under_limit(self):
        schema.get_db()
        create_backup("only-one")

        removed = rotate_backups(keep=5)
        assert removed == 0
        assert len(list_backups()) == 1

    def test_keeps_newest(self):
        schema.get_db()
        for i in range(4):
            create_backup(f"keep-{i}")
            time.sleep(0.05)

        rotate_backups(keep=2)
        backups = list_backups()
        assert len(backups) == 2
        # Should keep the two newest
        assert backups[0].reason == "keep-3"
        assert backups[1].reason == "keep-2"


class TestResetDbCreatesBackup:
    def test_reset_creates_backup_first(self):
        db = schema.get_db()
        db.execute(
            "INSERT INTO campaigns (id, name, status, icp_json, created_at) "
            "VALUES ('c1', 'BeforeReset', 'active', '{}', 1000)"
        )
        db.commit()

        schema.reset_db()

        # DB should be gone
        assert not config.db_path().exists()

        # But a backup should exist
        backups = list_backups()
        assert len(backups) >= 1
        assert backups[0].reason == "pre-reset"

        # Backup should contain the data
        conn = sqlite3.connect(str(backups[0].path))
        row = conn.execute("SELECT name FROM campaigns WHERE id='c1'").fetchone()
        conn.close()
        assert row[0] == "BeforeReset"


class TestFreshDbWarning:
    def test_logs_warning_when_config_exists_but_db_is_new(self, caplog):
        import logging

        # Create config first (simulates existing user)
        config.save_config({"test": True})
        assert config.config_path().exists()
        # DB doesn't exist yet
        assert not config.db_path().exists()

        with caplog.at_level(logging.WARNING, logger="heylead.db.schema"):
            schema.get_db()

        assert any("previous data may have been lost" in r.message for r in caplog.records)
