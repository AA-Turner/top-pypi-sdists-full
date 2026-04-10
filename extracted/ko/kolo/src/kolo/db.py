from __future__ import annotations

import json
import logging
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, Tuple

from io import BytesIO

import msgpack

from .serialize import dump_msgpack

logger = logging.getLogger("kolo")

# Directory name for file-based trace storage (inside .internal/)
RAW_TRACES_DIR = "raw"


def extract_trace_name_fast(msgpack_bytes: bytes) -> str | None:
    """Extract just trace_name from msgpack without full deserialization.

    Uses msgpack's skip() to avoid deserializing the bulk of the trace data.
    Returns None if trace_name is not set or not found.
    """
    unpacker = msgpack.Unpacker(BytesIO(msgpack_bytes), raw=False)

    # Read map header
    num_items = unpacker.read_map_header()

    for _ in range(num_items):
        key = unpacker.unpack()
        if key == "trace_name":
            value = unpacker.unpack()
            # Return only if it's actually set (not None or empty)
            if value:
                return value
            return None
        else:
            unpacker.skip()  # Skip without deserializing

    return None


class TraceNotFoundError(Exception):
    pass


@contextmanager
def db_connection(db_path, timeout=60):
    """
    Wrap sqlite's connection for use as a context manager

    Commits all changes if no exception is raised.
    Always closes the connection after the context manager exits.
    """
    connection = sqlite3.connect(str(db_path), isolation_level=None, timeout=timeout)
    try:
        connection.execute("pragma journal_mode=wal")
    finally:
        connection.close()

    connection = sqlite3.connect(str(db_path), isolation_level=None, timeout=timeout)
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def get_db_path() -> Path:
    # Import from _paths (lightweight) instead of config (heavy - cerberus, toolz)
    from ._paths import INTERNAL_DIR, create_kolo_directory

    return create_kolo_directory() / INTERNAL_DIR / "db.sqlite3"


def get_db_last_modified() -> datetime | None:
    try:
        modified = get_db_path().stat().st_mtime_ns
    except FileNotFoundError:
        return None
    else:
        return datetime.fromtimestamp(modified / 1e9, tz=timezone.utc)


def get_raw_traces_directory(db_path: Path | None = None) -> Path:
    """Get the path to the raw directory where trace files are stored."""
    if db_path is not None:
        # db_path is .kolo/.internal/db.sqlite3, parent is .kolo/.internal/
        return db_path.parent / RAW_TRACES_DIR
    from ._paths import INTERNAL_DIR, create_kolo_directory

    return create_kolo_directory() / INTERNAL_DIR / RAW_TRACES_DIR


def get_trace_file_path(trace_id: str, db_path: Path | None = None) -> Path:
    """Get the file path for a trace given its ID.

    Validates that the trace_id doesn't contain path traversal characters.
    """
    raw_dir = get_raw_traces_directory(db_path).resolve()
    trace_path = (raw_dir / f"{trace_id}.msgpack").resolve()
    # Ensure the resolved path is still within the raw traces directory
    try:
        trace_path.relative_to(raw_dir)
    except ValueError:
        raise ValueError(f"Invalid trace_id: {trace_id}")
    return trace_path


def save_trace_to_file(
    trace_id: str,
    msgpack_data: bytes,
    *,
    created_at: datetime | None = None,
    db_path: Path | None = None,
) -> None:
    """Save trace msgpack data to a file in the .internal/raw/ directory."""
    trace_path = get_trace_file_path(trace_id, db_path)

    # Ensure the directory exists
    trace_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the msgpack data
    trace_path.write_bytes(msgpack_data)

    # Set the file's modification time if created_at is provided
    if created_at is not None:
        timestamp = created_at.timestamp()
        os.utime(trace_path, (timestamp, timestamp))


def load_trace_from_file(
    trace_id: str, db_path: Path | None = None
) -> Tuple[bytes, str] | None:
    """
    Load trace msgpack data from a file in the .internal/raw/ directory.

    Returns (msgpack_bytes, created_at_string) or None if the file doesn't exist.
    """
    trace_path = get_trace_file_path(trace_id, db_path)

    if not trace_path.exists():
        return None

    try:
        msgpack_data = trace_path.read_bytes()
        # Get the file's modification time as the created_at timestamp
        stat = trace_path.stat()
        created_at = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
        # Format to millisecond precision to match database timestamp format
        created_at_str = created_at.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        return msgpack_data, created_at_str
    except Exception as e:
        logger.warning(f"Failed to load trace {trace_id} from file: {e}")
        return None


def delete_trace_file(trace_id: str, db_path: Path | None = None) -> bool:
    """Delete a trace file. Returns True if the file was deleted."""
    trace_path = get_trace_file_path(trace_id, db_path)

    try:
        if trace_path.exists():
            trace_path.unlink()
            return True
        return False
    except Exception as e:
        logger.warning(f"Failed to delete trace file {trace_id}: {e}")
        return False


def _load_trace_data_for_row(
    trace_id: str,
    db_msgpack: bytes | None,
    db_created_at: str | None,
    db_path: Path,
) -> Tuple[bytes, str] | None:
    """
    Load trace data from file or database for a given row.

    Tries file-based storage first, falls back to database.
    Returns (msgpack_data, created_at) or None if data is missing.
    """
    # Try loading from file first
    file_result = load_trace_from_file(trace_id, db_path)
    if file_result is not None:
        msgpack_data, file_created_at = file_result
        # Use DB created_at if available, else file timestamp
        return msgpack_data, db_created_at or file_created_at

    # Fall back to database
    if db_msgpack is not None and db_created_at is not None:
        return db_msgpack, db_created_at

    return None


def create_traces_table(connection) -> None:
    create_table_query = """
    CREATE TABLE IF NOT EXISTS traces (
        id text PRIMARY KEY NOT NULL,
        created_at TEXT DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')) NOT NULL,
        data text NULL,
        msgpack blob NULL,
        is_pinned INTEGER DEFAULT 0,
        auto_generated_name TEXT NULL
    );
    """
    create_timestamp_index_query = """
        CREATE INDEX IF NOT EXISTS
        idx_traces_created_at
        ON traces (created_at);
        """

    connection.execute(create_table_query)
    connection.execute(create_timestamp_index_query)


def migrate_db(connection) -> None:
    """Apply database migrations."""
    try:
        connection.execute("ALTER TABLE traces ADD COLUMN is_pinned INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        # Column already exists
        pass

    try:
        connection.execute(
            "ALTER TABLE traces ADD COLUMN auto_generated_name TEXT NULL"
        )
    except sqlite3.OperationalError:
        # Column already exists
        pass


def setup_db() -> Path:
    db_path = get_db_path()

    with db_connection(db_path) as connection:
        create_traces_table(connection)
        migrate_db(connection)

    return db_path


def save_trace(
    trace_id: str,
    msgpack_data: bytes,
    *,
    db_path: Path | None = None,
    ignore_errors: bool = True,
    created_at: datetime | None = None,
    timeout: int = 60,
) -> None:
    """
    Save a trace to file storage and store metadata in the database.

    This is the primary way to save traces. The msgpack data is stored
    as a file in .kolo/.internal/raw/, and metadata (id, created_at) is stored
    in the database for querying and indexing.

    If created_at is None, the database's default timestamp is used (SQLite's
    STRFTIME at INSERT time), which matches the legacy behavior and ensures
    consistent trace ordering when multiple traces are saved rapidly.
    """
    if db_path is None:
        db_path = get_db_path()

    # Save the trace data to a file
    try:
        save_trace_to_file(
            trace_id, msgpack_data, created_at=created_at, db_path=db_path
        )
    except Exception as e:
        logger.warning(f"Failed to save trace {trace_id} to file: {e}")
        if not ignore_errors:
            raise
        return

    # Save metadata to the database (without msgpack data)
    # If created_at is provided, include it; otherwise let database use its default
    ignore = " OR IGNORE" if ignore_errors else ""

    if created_at is not None:
        created_at_str = created_at.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        insert_sql = f"INSERT{ignore} INTO traces(id, created_at) VALUES(?, ?)"
        params: tuple = (trace_id, created_at_str)
    else:
        # Let database use its default timestamp (SQLite's NOW at INSERT time)
        # This matches the legacy save_trace_in_sqlite behavior
        insert_sql = f"INSERT{ignore} INTO traces(id) VALUES(?)"
        params = (trace_id,)

    with db_connection(db_path, timeout) as connection:
        try:
            connection.execute(insert_sql, params)
        except Exception as e:
            logger.warning(f"Failed to save trace metadata to database: {e}")
            if not ignore_errors:
                # Clean up the file we just created to avoid orphans
                delete_trace_file(trace_id, db_path)  # pragma: no cover
                raise  # pragma: no cover


def save_trace_in_sqlite(
    db_path: Path,
    trace_id: str,
    msgpack: bytes,
    *,
    ignore_errors: bool = True,
    created_at: datetime | None = None,
    timeout=60,
) -> None:
    """
    Legacy function for saving traces directly to SQLite.

    This is kept for backwards compatibility. New code should use save_trace().
    """
    ignore = " OR IGNORE" if ignore_errors else ""
    _columns = ["id", "msgpack"]
    values: list[object] = [trace_id, msgpack]
    if created_at is not None:
        _columns.append("created_at")
        values.append(created_at)
    columns = ", ".join(_columns)
    params = ",".join(["?" for _ in _columns])

    insert_sql = f"INSERT{ignore} INTO traces({columns}) VALUES({params})"

    # We can't reuse a connection
    # because we're in a new thread
    with db_connection(db_path, timeout) as connection:
        try:
            connection.execute(insert_sql, values)
        except (sqlite3.DataError, sqlite3.InterfaceError):
            # DataError on python 3.11+
            # InterfaceError on python 3.10-
            logger.exception("The generated trace was too big to store in sqlite.")


def trace_exists(trace_id: str, db_path: Path | None = None) -> bool:
    """Check if a trace exists (in file or database)."""
    if db_path is None:
        db_path = get_db_path()

    # Check if file exists
    trace_path = get_trace_file_path(trace_id, db_path)
    if trace_path.exists():
        return True

    # Check if database record exists
    with db_connection(db_path) as connection:
        cursor = connection.execute("SELECT 1 FROM traces WHERE id = ?", (trace_id,))
        return cursor.fetchone() is not None


def load_trace_from_db(db_path: Path, trace_id: str) -> Tuple[bytes, str]:
    """
    Load a trace, checking files first, then falling back to the database.

    Returns (msgpack_bytes, created_at_string).
    """
    # Try loading from file first
    file_result = load_trace_from_file(trace_id, db_path)
    if file_result is not None:
        return file_result

    # Fall back to database
    fetch_sql = "SELECT msgpack, created_at FROM traces WHERE id = ?"

    with db_connection(db_path) as connection:
        cursor = connection.execute(fetch_sql, (trace_id,))
        row = cursor.fetchone()

    if row is None:
        raise TraceNotFoundError(trace_id)

    msgpack_data, created_at = row
    if msgpack_data is None:
        # Trace metadata exists but data is missing (should not happen normally)
        raise TraceNotFoundError(trace_id)

    return msgpack_data, created_at


def load_trace_with_size_from_db(
    db_path: Path, trace_id: str
) -> Tuple[str, str, int, bytes]:
    """
    Load a trace with size info, checking files first, then falling back to the database.

    Returns (id, created_at, size, msgpack_bytes).
    """
    # Try loading from file first
    file_result = load_trace_from_file(trace_id, db_path)
    if file_result is not None:
        msgpack_data, created_at = file_result
        return trace_id, created_at, len(msgpack_data), msgpack_data

    # Fall back to database
    fetch_sql = """
        SELECT id, created_at, LENGTH(msgpack), msgpack
        FROM traces WHERE id = ?
    """

    with db_connection(db_path) as connection:
        cursor = connection.execute(fetch_sql, (trace_id,))
        row = cursor.fetchone()

    if row is None:
        raise TraceNotFoundError(trace_id)

    _id, _created_at, _size, msgpack_data = row
    if msgpack_data is None:
        # Trace metadata exists but data is missing
        raise TraceNotFoundError(trace_id)

    return row


def list_traces_from_db(db_path: Path, count=500, reverse=False):
    list_sql = """
    SELECT id, created_at, LENGTH(msgpack)
    FROM traces ORDER BY created_at DESC LIMIT ?
    """

    with db_connection(db_path) as connection:
        cursor = connection.execute(list_sql, [count])
        rows = cursor.fetchall()
    if reverse:
        return reversed(rows)
    return rows


def list_traces_with_data_from_db(
    db_path: Path, count: int = 500, reverse: bool = False
) -> Iterator[Tuple[str, str, int, bytes, str | None]]:
    """Like list_traces_from_db but includes the msgpack data for each trace.

    Checks files first for trace data, falls back to database.
    Returns tuples of (id, created_at, size, msgpack, auto_generated_name).
    """
    # Get metadata from database (includes both file-based and db-based traces)
    list_sql = """
    SELECT id, created_at, msgpack, auto_generated_name
    FROM traces ORDER BY created_at DESC LIMIT ?
    """

    with db_connection(db_path) as connection:
        cursor = connection.execute(list_sql, [count])
        rows = []
        while True:
            row = cursor.fetchone()
            if row is None:
                break

            trace_id, db_created_at, db_msgpack, auto_generated_name = row

            loaded = _load_trace_data_for_row(
                trace_id, db_msgpack, db_created_at, db_path
            )
            if loaded is None:
                logger.warning(f"Trace {trace_id} has no data in file or database")
                continue

            msgpack_data, created_at = loaded
            result = (
                trace_id,
                created_at,
                len(msgpack_data),
                msgpack_data,
                auto_generated_name,
            )

            if reverse:
                rows.append(result)
            else:
                yield result

    if reverse:
        for row in reversed(rows):
            yield row


def get_pinned_traces(
    db_path: Path,
) -> Iterator[Tuple[str, str, int, bytes, str | None]]:
    """Get all pinned traces.

    Checks files first for trace data, falls back to database.
    Returns tuples of (id, created_at, size, msgpack, auto_generated_name).
    """
    with db_connection(db_path) as connection:
        cursor = connection.execute(
            """
            SELECT id, created_at, msgpack, auto_generated_name
            FROM traces
            WHERE is_pinned = 1
            ORDER BY created_at DESC
            """
        )
        while True:
            row = cursor.fetchone()
            if row is None:
                break

            trace_id, db_created_at, db_msgpack, auto_generated_name = row

            loaded = _load_trace_data_for_row(
                trace_id, db_msgpack, db_created_at, db_path
            )
            if loaded is None:
                logger.warning(
                    f"Pinned trace {trace_id} has no data in file or database"
                )
                continue

            msgpack_data, created_at = loaded
            yield (
                trace_id,
                created_at,
                len(msgpack_data),
                msgpack_data,
                auto_generated_name,
            )


def update_auto_generated_name(db_path: Path, trace_id: str, auto_name: str) -> None:
    """Update the auto_generated_name for a trace (lazy migration)."""
    with db_connection(db_path) as connection:
        connection.execute(
            "UPDATE traces SET auto_generated_name = ? WHERE id = ?",
            (auto_name, trace_id),
        )


def delete_traces_by_id(db_path: Path, trace_ids: Tuple[str, ...]):
    """Delete traces by ID from both files and database."""
    # Delete trace files
    for trace_id in trace_ids:
        delete_trace_file(trace_id, db_path)

    # Delete from database
    params = ", ".join("?" * len(trace_ids))
    delete_sql = f"DELETE FROM traces WHERE id in ({params})"

    with db_connection(db_path) as connection:
        cursor = connection.execute(delete_sql, trace_ids)
        return cursor.rowcount


def delete_traces_before(db_path: Path, before: datetime):
    """Delete traces created before the given datetime from both files and database."""
    # First, get the IDs of traces to delete so we can delete their files
    select_sql = "SELECT id FROM traces WHERE created_at < ?"

    with db_connection(db_path) as connection:
        cursor = connection.execute(select_sql, (before,))
        trace_ids = [row[0] for row in cursor.fetchall()]

    # Delete trace files
    for trace_id in trace_ids:
        delete_trace_file(trace_id, db_path)

    # Also delete any orphaned files (files without DB entries)
    raw_traces_dir = get_raw_traces_directory(db_path)
    if raw_traces_dir.exists():
        before_timestamp = before.timestamp()
        for trace_file in raw_traces_dir.glob("*.msgpack"):
            try:
                if trace_file.stat().st_mtime < before_timestamp:
                    trace_file.unlink()
            except Exception as e:  # pragma: no cover
                logger.warning(f"Failed to delete old trace file {trace_file}: {e}")

    # Delete from database
    delete_sql = "DELETE FROM traces WHERE (created_at < ?)"

    with db_connection(db_path) as connection:
        connection.execute(delete_sql, (before,))
        cursor = connection.execute("SELECT changes()")
        deleted_count = cursor.fetchone()[0]
    return deleted_count


def vacuum_db(db_path):
    with db_connection(db_path) as connection:
        connection.execute("VACUUM")


def convert_json_to_msgpack(db_path: Path):  # pragma: no cover
    json_traces = "SELECT id, data FROM traces WHERE data IS NOT NULL"
    update_trace = "UPDATE traces SET data = NULL, msgpack = ? WHERE id = ?"

    with db_connection(db_path) as connection:
        cursor = connection.execute(json_traces)
        rows = cursor.fetchall()

        for trace_id, json_data in rows:
            msgpack_data = dump_msgpack(json.loads(json_data))
            cursor.execute(update_trace, (msgpack_data, trace_id))

    return len(rows)


def pin_trace(db_path: Path, trace_id: str) -> bool:
    """Pin a trace. Returns True if the trace was found and pinned.

    Works with both file-based and database-stored traces.
    """
    with db_connection(db_path) as connection:
        try:
            connection.execute(
                "ALTER TABLE traces ADD COLUMN is_pinned INTEGER DEFAULT 0"
            )
        except sqlite3.OperationalError:
            # Column already exists
            pass

        # Try to update existing record
        cursor = connection.execute(
            "UPDATE traces SET is_pinned = 1 WHERE id = ?",
            (trace_id,),
        )

        if cursor.rowcount > 0:
            return True

        # If no record exists, check if the trace exists as a file
        file_result = load_trace_from_file(trace_id, db_path)
        if file_result is not None:
            _, created_at_str = file_result
            # Create a metadata record for the file-based trace
            connection.execute(
                "INSERT OR IGNORE INTO traces (id, created_at, is_pinned) VALUES (?, ?, 1)",
                (trace_id, created_at_str),
            )
            return True

        return False


def unpin_trace(db_path: Path, trace_id: str) -> bool:
    """Unpin a trace. Returns True if the trace was found and unpinned."""
    with db_connection(db_path) as connection:
        cursor = connection.execute(
            "UPDATE traces SET is_pinned = 0 WHERE id = ?",
            (trace_id,),
        )
        return cursor.rowcount > 0


def migrate_traces_to_files(
    db_path: Path | None = None,
    batch_size: int = 100,
    callback=None,
) -> int:
    """
    Migrate traces from SQLite database to file-based storage.

    This function migrates traces in batches to avoid memory issues.
    It handles both:
    - Traces with msgpack data (newer format)
    - Traces with JSON in the data column (legacy format)

    After migration, both msgpack and data columns are set to NULL
    but the metadata (id, created_at, is_pinned, etc.) is preserved.

    Args:
        db_path: Path to the database. If None, uses default.
        batch_size: Number of traces to migrate per batch.
        callback: Optional callback function called after each batch with
                  (migrated_count, total_remaining) as arguments.

    Returns:
        Total number of traces migrated.
    """
    if db_path is None:
        db_path = get_db_path()

    total_migrated = 0

    while True:
        # Get a batch of traces that haven't been migrated yet
        # Priority: msgpack first (binary data), then JSON data column (legacy)
        with db_connection(db_path) as connection:
            cursor = connection.execute(
                """
                SELECT id, msgpack, data, created_at
                FROM traces
                WHERE msgpack IS NOT NULL OR data IS NOT NULL
                LIMIT ?
                """,
                (batch_size,),
            )
            batch = cursor.fetchall()

        if not batch:
            break

        # Migrate each trace in the batch, tracking successful IDs
        successful_ids: list[str] = []
        for trace_id, msgpack_data, json_data, created_at_str in batch:
            try:
                # Determine the data to save
                if msgpack_data is not None:
                    # Use msgpack data directly (newer format)
                    data_to_save = msgpack_data
                elif json_data is not None:
                    # Convert JSON to msgpack (legacy format)
                    data_to_save = dump_msgpack(json.loads(json_data))
                else:  # pragma: no cover
                    # No data to migrate (shouldn't happen due to WHERE clause)
                    continue

                # Parse created_at timestamp
                try:
                    created_at = datetime.strptime(
                        created_at_str, "%Y-%m-%d %H:%M:%S.%f"
                    )
                    created_at = created_at.replace(tzinfo=timezone.utc)
                except (ValueError, TypeError):
                    created_at = datetime.now(tz=timezone.utc)

                # Save to file
                save_trace_to_file(
                    trace_id, data_to_save, created_at=created_at, db_path=db_path
                )
                successful_ids.append(trace_id)
            except Exception as e:
                logger.warning(f"Failed to migrate trace {trace_id}: {e}")

        # If no traces were migrated in this batch, stop to avoid infinite loop
        # This can happen if all saves fail (e.g., disk full, permissions)
        if not successful_ids:
            if batch:
                logger.warning(
                    f"All {len(batch)} traces failed to migrate, stopping migration"
                )
            break

        # Clear msgpack and data from database for successfully migrated traces
        if successful_ids:
            placeholders = ", ".join("?" * len(successful_ids))
            with db_connection(db_path) as connection:
                connection.execute(
                    f"UPDATE traces SET msgpack = NULL, data = NULL WHERE id IN ({placeholders})",
                    tuple(successful_ids),
                )

        total_migrated += len(successful_ids)

        # Get count of remaining traces (both msgpack and JSON)
        with db_connection(db_path) as connection:
            cursor = connection.execute(
                "SELECT COUNT(*) FROM traces WHERE msgpack IS NOT NULL OR data IS NOT NULL"
            )
            remaining = cursor.fetchone()[0]

        if callback:
            callback(total_migrated, remaining)

        if remaining == 0:
            break

    return total_migrated


def get_migration_status(db_path: Path | None = None) -> dict:
    """
    Get the current migration status.

    Returns a dict with:
        - db_traces: Number of traces with msgpack data in database
        - json_traces: Number of traces with JSON data in database (legacy)
        - file_traces: Number of trace files in .internal/raw/ directory
        - total_traces: Total number of traces in database (metadata)
        - needs_migration: Total traces that need migration (db_traces + json_traces)
    """
    if db_path is None:
        db_path = get_db_path()

    with db_connection(db_path) as connection:
        cursor = connection.execute(
            "SELECT COUNT(*) FROM traces WHERE msgpack IS NOT NULL"
        )
        db_traces = cursor.fetchone()[0]

        # Count JSON-only traces (legacy format)
        cursor = connection.execute(
            "SELECT COUNT(*) FROM traces WHERE data IS NOT NULL AND msgpack IS NULL"
        )
        json_traces = cursor.fetchone()[0]

        cursor = connection.execute("SELECT COUNT(*) FROM traces")
        total_traces = cursor.fetchone()[0]

    # Count files in .internal/raw/ directory
    raw_traces_dir = get_raw_traces_directory(db_path)
    file_traces = 0
    if raw_traces_dir.exists():
        file_traces = len(list(raw_traces_dir.glob("*.msgpack")))

    return {
        "db_traces": db_traces,
        "json_traces": json_traces,
        "file_traces": file_traces,
        "total_traces": total_traces,
        "needs_migration": db_traces + json_traces,
    }
