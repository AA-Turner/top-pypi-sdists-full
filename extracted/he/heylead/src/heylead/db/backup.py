"""Database backup and restore utilities."""

from __future__ import annotations

import logging
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path

from .. import config, constants

logger = logging.getLogger(__name__)


@dataclass
class BackupInfo:
    """Metadata about a database backup."""

    path: Path
    reason: str
    timestamp: float
    size_bytes: int


def create_backup(reason: str = "manual") -> Path | None:
    """Create a backup of the current database using SQLite's backup API.

    Uses sqlite3.backup() which safely handles WAL mode — the resulting
    backup file is a consistent snapshot even if writes are in progress.

    Returns the backup path, or None if there's no database to back up.
    """
    src_path = config.db_path()
    if not src_path.exists():
        logger.info("No database to back up")
        return None

    config.ensure_dirs()
    dest_dir = config.backups_dir()
    ts = int(time.time() * 1000)
    safe_reason = reason.replace(" ", "-").replace("/", "-")[:30]
    dest_path = dest_dir / f"heylead-{ts}-{safe_reason}.db"

    src_conn = sqlite3.connect(str(src_path), timeout=10)
    try:
        dst_conn = sqlite3.connect(str(dest_path))
        try:
            src_conn.backup(dst_conn)
            dst_conn.close()
        except Exception:
            dst_conn.close()
            if dest_path.exists():
                dest_path.unlink()
            raise
    finally:
        src_conn.close()

    size = dest_path.stat().st_size
    logger.info("Backup created: %s (%d bytes)", dest_path.name, size)
    return dest_path


def list_backups() -> list[BackupInfo]:
    """List available backups, sorted newest first."""
    backup_dir = config.backups_dir()
    if not backup_dir.exists():
        return []

    backups = []
    for f in backup_dir.glob("heylead-*-*.db"):
        parts = f.stem.split("-", 2)  # heylead, timestamp, reason
        if len(parts) >= 3:
            try:
                ts = float(parts[1])
            except ValueError:
                ts = f.stat().st_mtime
            reason = parts[2]
        else:
            ts = f.stat().st_mtime
            reason = "unknown"
        backups.append(BackupInfo(
            path=f,
            reason=reason,
            timestamp=ts,
            size_bytes=f.stat().st_size,
        ))

    backups.sort(key=lambda b: b.timestamp, reverse=True)
    return backups


def restore_backup(backup_path: Path) -> None:
    """Restore a backup by replacing the current database.

    Closes the singleton connection, replaces the DB file using
    SQLite's backup API, then lets get_db() reconnect on next call.
    """
    from . import schema

    if not backup_path.exists():
        raise FileNotFoundError(f"Backup not found: {backup_path}")

    db_path = config.db_path()

    # Close the singleton connection so we can replace the file
    if schema._conn is not None:
        real = getattr(schema._conn, "_real", schema._conn)
        real.close()
        schema._conn = None

    # Use SQLite backup API to safely restore
    src_conn = sqlite3.connect(str(backup_path), timeout=10)
    try:
        dst_conn = sqlite3.connect(str(db_path))
        try:
            src_conn.backup(dst_conn)
        finally:
            dst_conn.close()
    finally:
        src_conn.close()

    logger.info("Database restored from %s", backup_path.name)


def rotate_backups(keep: int = constants.MAX_BACKUPS) -> int:
    """Remove old backups, keeping only the most recent `keep` files.

    Returns the number of backups removed.
    """
    backups = list_backups()
    removed = 0
    for backup in backups[keep:]:
        backup.path.unlink(missing_ok=True)
        removed += 1
        logger.info("Removed old backup: %s", backup.path.name)
    return removed
