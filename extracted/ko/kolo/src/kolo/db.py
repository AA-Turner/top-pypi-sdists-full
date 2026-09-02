from __future__ import annotations

import json
import logging
import os
import sqlite3
import stat
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from secrets import token_hex
from typing import BinaryIO, Iterable, Iterator, Tuple

from io import BytesIO

import msgpack

from .serialize import dump_msgpack

logger = logging.getLogger("kolo")

# Directory name for file-based trace storage (inside .internal/)
RAW_TRACES_DIR = "raw"
_WRITEV_BATCH_BYTES = 8 * 1024 * 1024

try:
    _writev_max_buffers = os.sysconf("SC_IOV_MAX")
except (AttributeError, OSError, ValueError):  # pragma: no cover - Windows
    _WRITEV_MAX_BUFFERS = 0
else:
    _WRITEV_MAX_BUFFERS = (
        min(_writev_max_buffers, 1024)
        if _writev_max_buffers > 0 and hasattr(os, "writev")
        else 0
    )

# WAL mode is persistent for a database file, so paying for
# ``PRAGMA journal_mode=wal`` on every short-lived metadata connection only
# adds locking and filesystem work. Cache the file identity rather than just
# the path so deleting and recreating a database at the same location still
# configures the replacement file correctly. On POSIX, retaining a bounded
# number of file descriptors prevents an unlinked database's inode from being
# reused while its identity is cached. Windows deliberately skips this cache:
# neither inode nor creation-time comparisons are a universal replacement for
# a retained file identity there.
_WAL_IDENTITY_CACHE_SIZE = 32
_WalDatabaseIdentity = Tuple[int, int, BinaryIO]
_wal_database_identities: dict[str, _WalDatabaseIdentity] = {}
_wal_database_identities_lock = threading.Lock()


def _database_identity(stat: os.stat_result) -> tuple[int, int]:
    return stat.st_dev, stat.st_ino


def _close_wal_identity(identity: _WalDatabaseIdentity | None) -> None:
    if identity is not None:
        identity[2].close()


def _identity_file_uses_wal(identity: _WalDatabaseIdentity) -> bool:
    """Check SQLite's persistent journal-mode bytes on the retained file."""
    try:
        # Bytes 18 and 19 are the database file's write/read versions. SQLite
        # stores 2/2 for WAL and 1/1 for rollback-journal modes.
        return os.pread(identity[2].fileno(), 2, 18) == b"\x02\x02"
    except (AttributeError, OSError, ValueError):
        return False


def _ensure_wal_mode(connection, db_path) -> None:
    if os.name == "nt":
        connection.execute("pragma journal_mode=wal").fetchone()
        return

    path = os.path.abspath(os.fspath(db_path))
    try:
        stat = os.stat(path)
    except OSError:
        identity = None
    else:
        identity = _database_identity(stat)

    stale_identity = None
    with _wal_database_identities_lock:
        cached_identity = _wal_database_identities.get(path)
        if identity is not None and cached_identity is not None:
            if cached_identity[:2] == identity and _identity_file_uses_wal(
                cached_identity
            ):
                return
        if cached_identity is not None:
            stale_identity = _wal_database_identities.pop(path)

    try:
        # A first-time DELETE -> WAL conversion can wait for another process's
        # transaction. Do not serialize unrelated databases behind that wait.
        journal_mode = connection.execute("pragma journal_mode=wal").fetchone()
        if identity is None or journal_mode != ("wal",):
            return

        try:
            identity_file = open(path, "rb")
        except OSError:
            return
        try:
            opened_identity = _database_identity(os.fstat(identity_file.fileno()))
        except OSError:
            identity_file.close()
            return
        if opened_identity != identity:
            identity_file.close()
            return

        with _wal_database_identities_lock:
            previous_identity = _wal_database_identities.get(path)
            if (
                previous_identity is not None
                and previous_identity[:2] == opened_identity
                and _identity_file_uses_wal(previous_identity)
            ):
                identity_file.close()
                return

            _wal_database_identities[path] = (*identity, identity_file)
            _close_wal_identity(previous_identity)

            if len(_wal_database_identities) > _WAL_IDENTITY_CACHE_SIZE:
                oldest_path = next(iter(_wal_database_identities))
                oldest_identity = _wal_database_identities.pop(oldest_path)
                _close_wal_identity(oldest_identity)
    finally:
        _close_wal_identity(stale_identity)


def extract_trace_name_fast(msgpack_bytes: bytes) -> str | None:
    """Extract just trace_name from msgpack without full deserialization.

    Uses msgpack's skip() to avoid deserializing the bulk of the trace data.
    Returns None if trace_name is not set or not found.
    """
    from .trace_container import extract_v3_trace_name, is_v3_trace

    if is_v3_trace(msgpack_bytes):
        return extract_v3_trace_name(msgpack_bytes)

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
        _ensure_wal_mode(connection, db_path)
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


def get_v3_trace_file_path(trace_id: str, db_path: Path | None = None) -> Path:
    """Return the default Kolo 3.3+ container path for a trace."""
    raw_dir = get_raw_traces_directory(db_path).resolve()
    trace_path = (raw_dir / f"{trace_id}.kolo").resolve()
    try:
        trace_path.relative_to(raw_dir)
    except ValueError:
        raise ValueError(f"Invalid trace_id: {trace_id}")
    return trace_path


def _existing_trace_file_path(
    trace_id: str, db_path: Path | None = None
) -> Path | None:
    for trace_path in (
        get_v3_trace_file_path(trace_id, db_path),
        get_trace_file_path(trace_id, db_path),
    ):
        if trace_path.exists():
            return trace_path
    return None


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


def save_trace_chunks_to_file(
    trace_id: str,
    chunks: Iterable[bytes],
    *,
    created_at: datetime | None = None,
    db_path: Path | None = None,
) -> None:
    """Stream pre-packed msgpack chunks to file without joining them first."""
    trace_path = get_trace_file_path(trace_id, db_path)
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        temporary_path, trace_file = _open_atomic_trace_file(trace_path)
        with trace_file:
            if _WRITEV_MAX_BUFFERS:
                _write_chunks_with_writev(trace_file.fileno(), chunks)
            else:  # pragma: no cover - Windows
                trace_file.writelines(chunks)
        os.replace(temporary_path, trace_path)
    except BaseException:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise

    if created_at is not None:
        timestamp = created_at.timestamp()
        os.utime(trace_path, (timestamp, timestamp))


def save_v3_trace_chunks_to_file(
    trace_id: str,
    chunks: Iterable[bytes],
    *,
    created_at: datetime | None = None,
    db_path: Path | None = None,
) -> None:
    """Atomically stream a write-once v3 container to its final ``.kolo`` path."""
    trace_path = get_v3_trace_file_path(trace_id, db_path)
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        temporary_path, trace_file = _open_atomic_trace_file(trace_path)
        with trace_file:
            if _WRITEV_MAX_BUFFERS:
                _write_chunks_with_writev(trace_file.fileno(), chunks)
            else:  # pragma: no cover - Windows
                trace_file.writelines(chunks)
        os.replace(temporary_path, trace_path)
    except BaseException:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise

    if created_at is not None:
        timestamp = created_at.timestamp()
        os.utime(trace_path, (timestamp, timestamp))


def _open_atomic_trace_file(trace_path: Path) -> tuple[Path, BinaryIO]:
    """Create a sibling temporary file with normal trace-file permissions."""
    try:
        existing_mode = stat.S_IMODE(trace_path.stat().st_mode)
    except FileNotFoundError:
        existing_mode = None

    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
    for _ in range(10):
        temporary_path = trace_path.with_name(f".{trace_path.name}.{token_hex(8)}.tmp")
        try:
            file_descriptor = os.open(temporary_path, flags, 0o666)
        except FileExistsError:
            continue

        try:
            if existing_mode is not None:
                os.chmod(temporary_path, existing_mode)
            return temporary_path, os.fdopen(
                file_descriptor,
                "wb",
                buffering=0 if _WRITEV_MAX_BUFFERS else 1024 * 1024,
            )
        except BaseException:
            os.close(file_descriptor)
            temporary_path.unlink(missing_ok=True)
            raise

    raise FileExistsError(f"Could not create temporary trace beside {trace_path}")


def _write_chunks_with_writev(file_descriptor: int, chunks: Iterable[bytes]) -> None:
    batch: list[bytes] = []
    batch_bytes = 0
    for chunk in chunks:
        if not chunk:
            continue
        if batch and (
            len(batch) == _WRITEV_MAX_BUFFERS
            or batch_bytes + len(chunk) > _WRITEV_BATCH_BYTES
        ):
            _writev_all(file_descriptor, batch)
            batch.clear()
            batch_bytes = 0
        batch.append(chunk)
        batch_bytes += len(chunk)
        if len(batch) == _WRITEV_MAX_BUFFERS or batch_bytes >= _WRITEV_BATCH_BYTES:
            _writev_all(file_descriptor, batch)
            batch.clear()
            batch_bytes = 0
    if batch:
        _writev_all(file_descriptor, batch)


def _writev_all(file_descriptor: int, buffers: list[bytes]) -> None:
    remaining: list[bytes | memoryview] = [buffer for buffer in buffers if buffer]
    while remaining:
        write_buffers: list[bytes | memoryview] = []
        write_bytes = 0
        for buffer in remaining[:_WRITEV_MAX_BUFFERS]:
            available = _WRITEV_BATCH_BYTES - write_bytes
            if len(buffer) > available:
                write_buffers.append(memoryview(buffer)[:available])
                break
            write_buffers.append(buffer)
            write_bytes += len(buffer)
            if write_bytes == _WRITEV_BATCH_BYTES:
                break

        # CPython retries a real EINTR under PEP 475. If the signal handler
        # raises, propagate it so the caller removes the temporary file.
        written = os.writev(file_descriptor, write_buffers)
        if written == 0:  # pragma: no cover - regular files do not short-write zero
            raise OSError("writev returned zero bytes")

        consumed = 0
        while consumed < len(remaining) and written >= len(remaining[consumed]):
            written -= len(remaining[consumed])
            consumed += 1
        if consumed == len(remaining):
            return
        if written:
            remaining[consumed] = memoryview(remaining[consumed])[written:]
        remaining = remaining[consumed:]


def load_trace_from_file(
    trace_id: str, db_path: Path | None = None
) -> Tuple[bytes, str] | None:
    """
    Load trace msgpack data from a file in the .internal/raw/ directory.

    Returns (msgpack_bytes, created_at_string) or None if the file doesn't exist.
    """
    trace_path = _existing_trace_file_path(trace_id, db_path)
    if trace_path is None:
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
    deleted = False
    try:
        for trace_path in (
            get_v3_trace_file_path(trace_id, db_path),
            get_trace_file_path(trace_id, db_path),
        ):
            if trace_path.exists():
                trace_path.unlink()
                deleted = True
        return deleted
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
    # Partial index over only the traces that still hold inline blobs (i.e. are
    # pending migration to file storage). Once a trace is migrated its msgpack
    # and data columns are NULLed, so it drops out of this index, keeping it
    # tiny. This lets migration_pending() answer "is anything pending?" in O(1)
    # instead of scanning the whole traces table. Picked up by existing stores
    # on their next setup_db() via CREATE INDEX IF NOT EXISTS.
    create_pending_migration_index_query = """
        CREATE INDEX IF NOT EXISTS
        idx_traces_pending_migration
        ON traces (id)
        WHERE msgpack IS NOT NULL OR data IS NOT NULL;
        """

    connection.execute(create_table_query)
    connection.execute(create_timestamp_index_query)
    connection.execute(create_pending_migration_index_query)


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

    _save_trace_metadata(
        trace_id,
        db_path=db_path,
        ignore_errors=ignore_errors,
        created_at=created_at,
        timeout=timeout,
    )


def save_trace_chunks(
    trace_id: str,
    chunks: Iterable[bytes],
    *,
    db_path: Path | None = None,
    ignore_errors: bool = True,
    created_at: datetime | None = None,
    timeout: int = 60,
) -> None:
    """Persist a trace incrementally while retaining the normal metadata model."""
    if db_path is None:
        db_path = get_db_path()

    try:
        save_trace_chunks_to_file(
            trace_id, chunks, created_at=created_at, db_path=db_path
        )
    except Exception as e:
        logger.warning(f"Failed to save trace {trace_id} to file: {e}")
        if not ignore_errors:
            raise
        return

    _save_trace_metadata(
        trace_id,
        db_path=db_path,
        ignore_errors=ignore_errors,
        created_at=created_at,
        timeout=timeout,
    )


def save_v3_trace_chunks(
    trace_id: str,
    chunks: Iterable[bytes],
    *,
    db_path: Path | None = None,
    ignore_errors: bool = True,
    created_at: datetime | None = None,
    timeout: int = 60,
) -> None:
    """Persist a v3 trace incrementally while retaining the metadata index."""
    if db_path is None:
        db_path = get_db_path()

    try:
        save_v3_trace_chunks_to_file(
            trace_id, chunks, created_at=created_at, db_path=db_path
        )
    except Exception as e:
        logger.warning(f"Failed to save trace {trace_id} to file: {e}")
        if not ignore_errors:
            raise
        return

    _save_trace_metadata(
        trace_id,
        db_path=db_path,
        ignore_errors=ignore_errors,
        created_at=created_at,
        timeout=timeout,
    )


def _save_trace_metadata(
    trace_id: str,
    *,
    db_path: Path,
    ignore_errors: bool,
    created_at: datetime | None,
    timeout: int,
) -> None:
    # Save metadata to the database (without msgpack data). If created_at is
    # omitted, retain SQLite's INSERT-time default for legacy ordering.
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
    if _existing_trace_file_path(trace_id, db_path) is not None:
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
        for trace_file in (
            *raw_traces_dir.glob("*.kolo"),
            *raw_traces_dir.glob("*.msgpack"),
            *raw_traces_dir.glob(".*.tmp"),
        ):
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


def migration_pending(db_path: Path | None = None) -> bool:
    """Cheap, SQLite-only check for whether any traces still need migration.

    Returns True if at least one trace still holds inline blob data (msgpack or
    legacy JSON in the ``data`` column) that has not yet been moved to file
    storage. This is the same predicate as ``get_migration_status()["needs_migration"] > 0``
    but it does NOT enumerate the ``raw/`` directory, so it is safe to call on
    the auto-emit hot path even when ``raw/`` holds millions of files.

    Backed by the ``idx_traces_pending_migration`` partial index (see
    ``create_traces_table``), so the common "nothing to migrate" answer is O(1).
    """
    if db_path is None:
        db_path = get_db_path()

    with db_connection(db_path) as connection:
        cursor = connection.execute(
            "SELECT EXISTS("
            "SELECT 1 FROM traces WHERE msgpack IS NOT NULL OR data IS NOT NULL"
            ")"
        )
        return bool(cursor.fetchone()[0])


def get_migration_status(
    db_path: Path | None = None, *, include_file_count: bool = True
) -> dict:
    """
    Get the current migration status.

    Returns a dict with:
        - db_traces: Number of traces with msgpack data in database
        - json_traces: Number of traces with JSON data in database (legacy)
        - file_traces: Number of trace files in .internal/raw/ directory, or -1
          when ``include_file_count`` is False (not computed)
        - total_traces: Total number of traces in database (metadata)
        - needs_migration: Total traces that need migration (db_traces + json_traces)

    ``include_file_count`` controls the expensive on-disk census: counting files
    globs the entire ``raw/`` directory, which can hold millions of entries.
    Callers that only need the migration decision (e.g. the auto-emit hot path)
    should use :func:`migration_pending` instead; pass
    ``include_file_count=False`` here if they need the rest of the status dict
    but not the file count.
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

    # Count files in .internal/raw/ directory. This globs the whole raw/ dir
    # (potentially >1M entries), so it is opt-in via include_file_count and must
    # never run on the auto-emit hot path. Use a generator (sum) rather than
    # len(list(...)) so we never materialize a Path per file.
    file_traces = -1  # sentinel: not computed
    if include_file_count:
        raw_traces_dir = get_raw_traces_directory(db_path)
        file_traces = 0
        if raw_traces_dir.exists():
            file_traces = sum(1 for _ in raw_traces_dir.glob("*.kolo")) + sum(
                1 for _ in raw_traces_dir.glob("*.msgpack")
            )

    return {
        "db_traces": db_traces,
        "json_traces": json_traces,
        "file_traces": file_traces,
        "total_traces": total_traces,
        "needs_migration": db_traces + json_traces,
    }
