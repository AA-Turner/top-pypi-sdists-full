"""Kolo's store: trace files and the SQLite database that indexes them.

A process that saves traces in quick succession keeps the metadata
connection open between them (see ``_KeptConnection``). Setting
``KOLO_KEEP_DB_CONNECTION=0`` before Kolo is imported turns that off: every
save and ``setup_db`` then opens and closes a connection of its own.
"""

from __future__ import annotations

import atexit
import json
import logging
import os
import sqlite3
import stat
import sys
import threading
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from secrets import token_hex
from typing import BinaryIO, Iterable, Iterator, Tuple

from io import BytesIO

import msgpack

from .serialize import dump_msgpack
from .threads import kolo_worker_thread

logger = logging.getLogger("kolo")

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

# WAL mode persists per file: set it once per file identity (not path, so a recreated db gets it).
# POSIX keeps fds so an unlinked inode isn't reused; Windows skips this cache.
_WAL_IDENTITY_CACHE_SIZE = 32
_WalDatabaseIdentity = Tuple[int, int, BinaryIO]
_wal_database_identities: dict[str, _WalDatabaseIdentity] = {}
_wal_database_identities_lock = threading.Lock()


def _database_identity(stat: os.stat_result) -> tuple[int, int]:
    return stat.st_dev, stat.st_ino


def _reset_wal_identities_lock_after_fork() -> None:
    # Another thread of the parent may have held the lock during the fork:
    # the child's copy would then stay locked for good.
    global _wal_database_identities_lock

    _wal_database_identities_lock = threading.Lock()


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_reset_wal_identities_lock_after_fork)


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

    num_items = unpacker.read_map_header()

    for _ in range(num_items):
        key = unpacker.unpack()
        if key == "trace_name":
            value = unpacker.unpack()
            if value:
                return value
            return None
        else:
            unpacker.skip()

    return None


class TraceNotFoundError(Exception):
    pass


def _checkpoint(connection, busy_timeout_ms: int | None = None) -> bool:
    """Move committed rows from the write-ahead log into the database file
    and empty the log, as far as other connections allow right now.

    Closing a database's last connection does both. That is how a write
    reaches the file itself and moves its modification time (the web UI and
    the VS Code extension watch it for new traces), and why no log is left
    behind to be replayed into a database file that later replaces this one.
    A kept connection (see ``_KeptConnection``) does not close after its
    write, so it checkpoints explicitly instead.

    Never waits: with a reader or writer in the way, as much as possible is
    copied and the log stays, just as that other connection would have kept
    a close from removing it. Returns whether the log was emptied; if not,
    the caller must close its connection, so that the close of whichever
    connection is last finishes the job. ``busy_timeout_ms`` is restored
    afterwards on a connection that stays open.
    """
    try:
        connection.execute("pragma busy_timeout = 0")
        try:
            row = connection.execute("pragma wal_checkpoint(truncate)").fetchone()
        finally:
            if busy_timeout_ms is not None:
                connection.execute(f"pragma busy_timeout = {busy_timeout_ms}")
    except sqlite3.Error:
        # The write is committed either way; a later checkpoint or the last
        # close picks the rows up.
        logger.debug("Could not checkpoint the Kolo database", exc_info=True)
        return False
    # (blocked, frames in the log, frames checkpointed); the latter two are
    # -1 for a database that is not in WAL mode and has no log.
    return row is not None and row[0] == 0


@contextmanager
def db_connection(db_path, timeout=60, keep=False):
    """
    Wrap sqlite's connection for use as a context manager

    Commits all changes if no exception is raised.
    Always closes the connection after the context manager exits, unless
    ``keep`` is set: then the connection may be one this process keeps for
    the database (see ``_KeptConnection``), and stays open if the block
    succeeds. Only for a block of writes that each commit on their own.
    """
    kept = _acquire_kept_connection(db_path, timeout) if keep else None
    if kept is not None:
        succeeded = False
        try:
            yield kept.connection
            succeeded = True
        finally:
            kept.release(keep=succeeded)
        return
    connection = sqlite3.connect(str(db_path), isolation_level=None, timeout=timeout)
    schema_version = None
    try:
        _ensure_wal_mode(connection, db_path)
        if _has_kept_connection(db_path):
            schema_version = _schema_version(connection)
        with connection:
            yield connection
    finally:
        if connection.total_changes or (
            _has_kept_connection(db_path)
            if schema_version is None
            else _schema_version(connection) != schema_version
        ):
            # So that this close is the database's last one in this process
            # and checkpoints what was written, as it always did.
            _forget_kept_connection(db_path)
        connection.close()


# Reuse only the same file; checkpoint writes and close kept connections when idle, at exit or after fork.
_KEEP_CONNECTIONS = (
    os.environ.get("KOLO_KEEP_DB_CONNECTION") != "0"
    and os.name != "nt"
    # No threads: nothing could close an idle connection.
    and sys.platform != "emscripten"
    and hasattr(os, "register_at_fork")
    and hasattr(threading, "_register_atexit")
    and sqlite3.sqlite_version_info >= (3, 8, 3)
)
_KEPT_CONNECTIONS_MAX = 4
_KEPT_CONNECTION_IDLE_SECONDS = 0.05
_DatabaseFingerprint = Tuple[int, int, int, int, int]


def _database_fingerprint(path: str) -> _DatabaseFingerprint | None:
    try:
        result = os.stat(path)
    except OSError:
        return None
    return (
        result.st_dev,
        result.st_ino,
        result.st_size,
        result.st_mtime_ns,
        result.st_ctime_ns,
    )


def _busy_timeout_ms(timeout) -> int | None:
    """``timeout`` as the milliseconds sqlite3.connect turns it into, or None
    for values a kept connection does not handle."""
    if type(timeout) not in (int, float):
        return None
    try:
        timeout_ms = int(timeout * 1000)
    except (OverflowError, ValueError):  # pragma: no cover - inf or nan
        return None
    return timeout_ms if 0 <= timeout_ms < 2**31 else None


def _schema_version(connection) -> object:
    """Changes with every change to the schema. An object of its own if it
    cannot be read, so that it never compares equal."""
    try:
        return connection.execute("pragma schema_version").fetchone()
    except sqlite3.Error:  # pragma: no cover - a database that cannot be read
        return object()


def _has_kept_connection(db_path) -> bool:
    if not _KEEP_CONNECTIONS:
        return False
    return os.path.abspath(os.fspath(db_path)) in _kept_connections


def _data_version(connection) -> object:
    """Changes whenever another connection commits to the database."""
    return connection.execute("pragma data_version").fetchone()


class _KeptConnection:
    """One store's metadata connection, used by one thread at a time."""

    def __init__(self, path: str) -> None:
        self.path = path
        self.pid = os.getpid()
        # Reentrant, like the registry lock: a signal handler or a finalizer
        # that saves a trace can run on a thread that is already saving one.
        self.lock = threading.RLock()
        self.connection: sqlite3.Connection | None = None
        self.timeout_ms: int | None = None
        self.identity: Tuple[int, int] | None = None
        self.fingerprint: _DatabaseFingerprint | None = None
        self.data_version: object = None
        self.schema_data_version: object = None
        self.dropped = False
        self.users = 0
        self.last_used = time.monotonic()

    def open(self, db_path, timeout, timeout_ms: int) -> sqlite3.Connection:
        """The connection for this path, reopened unless the database file is
        exactly as this connection left it. Call with the lock held."""
        if self.pid != os.getpid():
            self._forget_after_fork()
        if self.connection is not None and self.users > 1:
            return self.connection
        if self.connection is not None and not self._file_as_left():
            self.close()
        if self.connection is None:
            before = _database_fingerprint(self.path)
            connection = sqlite3.connect(
                self.path,
                isolation_level=None,
                timeout=timeout,
                check_same_thread=False,
            )
            try:
                _ensure_wal_mode(connection, db_path)
                after = _database_fingerprint(self.path)
            except BaseException:
                connection.close()
                raise
            self.connection = connection
            self.pid = os.getpid()
            self.timeout_ms = timeout_ms
            self.fingerprint = None
            # Only if the path named the same file before and after opening is that the open file
            # (an open file's inode is not reused); otherwise close after this use.
            self.identity = (
                (before[0], before[1])
                if before is not None and after is not None and before[:2] == after[:2]
                else None
            )
        elif self.timeout_ms != timeout_ms:
            self.connection.execute(f"pragma busy_timeout = {timeout_ms}")
            self.timeout_ms = timeout_ms
        return self.connection

    def _file_as_left(self) -> bool:
        """Whether nothing but SQLite connections touched the database file
        since this connection's last write."""
        assert self.connection is not None
        fingerprint = _database_fingerprint(self.path)
        if (
            fingerprint is None
            or self.fingerprint is None
            or fingerprint[:2] != self.identity
        ):
            return False
        if fingerprint == self.fingerprint:
            return True
        try:
            data_version = _data_version(self.connection)
        except sqlite3.Error:  # pragma: no cover - the file is no database now
            return False
        if data_version == self.data_version:
            # No other connection committed, so something else rewrote the
            # file.
            return False
        self.fingerprint = fingerprint
        self.data_version = data_version
        return True

    def ensure_schema(self) -> bool:
        """Run ``setup_db``'s schema statements unless this connection ran
        them and no other connection has committed since (its own commits
        only insert rows). Returns whether it ran them. Call with the lock
        held."""
        assert self.connection is not None
        # Read first: a commit that lands after this read moves the version
        # again, so the next call runs the statements.
        data_version = _data_version(self.connection)
        if self.schema_data_version == data_version:
            return False
        create_traces_table(self.connection)
        migrate_db(self.connection)
        self.schema_data_version = data_version
        return True

    def wrote(self) -> None:
        """Record the file as this connection's write leaves it. Call with
        the lock held."""
        # Read once: a finalizer or signal handler on this thread can close this connection meanwhile.
        connection = self.connection
        if connection is None:  # pragma: no cover - closed before this
            return
        emptied = _checkpoint(connection, self.timeout_ms)
        self.data_version = _data_version(connection)
        self.fingerprint = _database_fingerprint(self.path)
        if (
            not emptied
            or self.fingerprint is None
            or self.fingerprint[:2] != self.identity
        ):
            # Rows are still in the log, or the path no longer names the
            # file this connection has open.
            self.close()

    def _forget_after_fork(self) -> None:
        """This entry reached a forked child by a way the fork hooks do not
        see (a fork on a thread that had it out of the registry). Its
        connection is the parent's: never used here, and kept alive rather
        than closed."""
        _inherited_connections.append(self.connection)
        self.connection = None
        self.fingerprint = None
        self.identity = None
        self.schema_data_version = None
        self.pid = os.getpid()

    def close(self) -> None:
        """Call with the lock held."""
        if self.pid != os.getpid():
            self._forget_after_fork()
        connection, self.connection = self.connection, None
        self.fingerprint = None
        self.identity = None
        self.schema_data_version = None
        if connection is not None:
            try:
                connection.close()
            except sqlite3.Error:
                logger.debug("Could not close a Kolo database", exc_info=True)

    def release(self, keep: bool, wrote: bool = True) -> None:
        """Give the connection back after ``_acquire_kept_connection``.

        ``keep``: every statement succeeded. ``wrote``: they may have
        changed the database.
        """
        try:
            if self.pid != os.getpid():
                # Before anything below can touch a connection that is
                # another process's: no checkpoint, no close.
                self._forget_after_fork()
            self.users -= 1
            self.last_used = time.monotonic()
            if keep and not self.dropped:
                try:
                    if wrote or self.fingerprint is None:
                        self.wrote()
                except sqlite3.Error:  # pragma: no cover - failing storage
                    self.close()
                except BaseException:  # pragma: no cover - an interrupt
                    self.close()
                    raise
                # Dropped while it was checkpointing: nobody else closes it.
                if self.dropped and not self.users:
                    self.close()
            elif not self.users:
                if keep and wrote and self.connection is not None:
                    # Dropped while in use: another connection may be kept now, so this close may not be the last.
                    # Checkpoint what was written first.
                    _checkpoint(self.connection)
                self.close()
        finally:
            self.lock.release()
        # Whoever drops an entry it finds in use leaves closing it to this
        # release, and may have done so after the checks above. It marks the
        # entry before it tries the lock, so the mark is visible by now.
        if self.dropped and self.connection is not None:  # pragma: no cover - race
            if self.lock.acquire(blocking=False):
                try:
                    if not self.users:
                        self.close()
                finally:
                    self.lock.release()


_kept_connections: dict[str, _KeptConnection] = {}
_kept_connections_lock = threading.RLock()
_kept_connections_pid = os.getpid()
_kept_connections_closer: threading.Thread | None = None
_kept_connections_closer_token: object = None
# Held by that thread while it closes connections it has already taken out of
# the registry, so that shutdown can wait for those closes too.
_kept_connections_closing = threading.Lock()
_kept_connections_atexit_registered = False
_kept_connections_closed = False
# Connections inherited over a fork. They belong to the parent: the child
# does not use them, and keeps them alive rather than close them.
_inherited_connections: list[object] = []


def _acquire_kept_connection(db_path, timeout) -> _KeptConnection | None:
    """This process's kept connection for ``db_path``, locked and open.

    Returns None when the caller should use ``db_connection`` instead. Raises
    whatever opening the database raises. The caller must ``release`` it.
    """
    global _kept_connections_atexit_registered, _kept_connections_closer
    global _kept_connections_closer_token

    if not _KEEP_CONNECTIONS:
        return None
    timeout_ms = _busy_timeout_ms(timeout)
    if timeout_ms is None:
        return None
    path = os.path.abspath(os.fspath(db_path))
    if _kept_connections_pid != os.getpid():
        _forget_kept_connections_after_fork()  # pragma: no cover
    dropped = []
    with _kept_connections_lock:
        if _kept_connections_closed:
            return None
        if not _kept_connections_atexit_registered:
            # A multiprocessing child shuts threading down and may then leave
            # without running exit handlers.
            try:
                threading._register_atexit(  # type: ignore[attr-defined]
                    _close_kept_connections_at_exit
                )
            except RuntimeError:  # pragma: no cover - already shutting down
                return None
            atexit.register(_close_kept_connections_at_exit)
            _kept_connections_atexit_registered = True
        if _kept_connections_closer is None or not _kept_connections_closer.is_alive():
            token = object()
            closer = kolo_worker_thread(
                _close_idle_kept_connections,
                name="kolo-close_idle_db",
                daemon=True,
                args=(token,),
            )
            try:
                closer.start()
            except RuntimeError:  # pragma: no cover - interpreter shutting down
                return None
            _kept_connections_closer = closer
            _kept_connections_closer_token = token
        entry = _kept_connections.pop(path, None)
        if entry is None:
            entry = _KeptConnection(path)
        entry.last_used = time.monotonic()
        _kept_connections[path] = entry
        # Checked once it is back in the registry, where the fork hooks see
        # it: a fork on this thread (from a signal handler or a finalizer)
        # while it was out leaves a child holding the parent's entry, whose
        # lock a thread that does not exist here may hold.
        if entry.pid != os.getpid():
            _inherited_connections.append(entry)
            entry = _kept_connections[path] = _KeptConnection(path)
        while len(_kept_connections) > _KEPT_CONNECTIONS_MAX:
            # The least recently used one that no save is using: dropping one
            # in use would let a second connection be kept beside it.
            oldest = next(
                (
                    candidate
                    # A copy, and ``pop`` rather than ``del`` below: a
                    # finalizer or signal handler that saves a trace or forks
                    # can run on this thread during the scan or after it, and
                    # drop or replace entries.
                    for candidate in list(_kept_connections.values())
                    if candidate is not entry and not candidate.users
                ),
                None,
            )
            if oldest is None:
                break
            replaced = _kept_connections.pop(oldest.path, None)
            oldest.dropped = True
            dropped.append(oldest)
            if replaced is not None and replaced is not oldest:  # pragma: no cover
                replaced.dropped = True
                dropped.append(replaced)
    for oldest in dropped:
        # Never wait for another database here: its user closes it on release.
        if oldest.lock.acquire(blocking=False):
            try:
                if not oldest.users:
                    oldest.close()
            finally:
                oldest.lock.release()
    # A save that finds the connection busy opens its own: it must not wait out another's busy timeout.
    if not entry.lock.acquire(blocking=False):
        return None
    if entry.dropped:
        entry.lock.release()
        return None
    entry.users += 1
    try:
        entry.open(db_path, timeout, timeout_ms)
    except BaseException:
        entry.release(keep=False)
        raise
    return entry


def _close_idle_kept_connections(token: object) -> None:
    """Runs on a thread of its own while this process keeps connections.

    Knows itself by ``token`` rather than by asking
    threading.current_thread(), which applications may wrap.
    """
    global _kept_connections_closer

    while True:
        time.sleep(min(_KEPT_CONNECTION_IDLE_SECONDS, 0.05))
        idle = []
        with _kept_connections_closing:
            with _kept_connections_lock:
                if _kept_connections_closer_token is not token:
                    return
                cutoff = time.monotonic() - _KEPT_CONNECTION_IDLE_SECONDS
                for path, entry in list(_kept_connections.items()):
                    # One in use (waiting out a busy timeout) stays, so that
                    # no second connection is kept beside it.
                    if entry.last_used <= cutoff and not entry.users:
                        # `pop`, not `del`: a finalizer on this thread may already have dropped or replaced the entry.
                        replaced = _kept_connections.pop(path, None)
                        entry.dropped = True
                        idle.append(entry)
                        if (
                            replaced is not None and replaced is not entry
                        ):  # pragma: no cover
                            replaced.dropped = True
                            idle.append(replaced)
                finished = not _kept_connections
                if finished:
                    _kept_connections_closer = None
            for entry in idle:
                if entry.lock.acquire(blocking=False):
                    try:
                        if not entry.users:
                            entry.close()
                    finally:
                        entry.lock.release()
        if finished:
            return


def _forget_kept_connection(db_path) -> None:
    if not _KEEP_CONNECTIONS:
        return
    path = os.path.abspath(os.fspath(db_path))
    if _kept_connections_pid != os.getpid():
        _forget_kept_connections_after_fork()  # pragma: no cover
    with _kept_connections_lock:
        entry = _kept_connections.pop(path, None)
        if entry is None:
            return
        entry.dropped = True
    if entry.lock.acquire(blocking=False):
        try:
            if not entry.users:
                entry.close()
        finally:
            entry.lock.release()


def _close_kept_connections(wait: bool = True) -> None:
    """Close every kept connection. One in use is closed by its user; with
    ``wait`` unset, without waiting for it."""
    if _kept_connections_pid != os.getpid():
        # Forked without Python's fork hooks running: not ours to close.
        _forget_kept_connections_after_fork()  # pragma: no cover
    with _kept_connections_lock:
        entries = list(_kept_connections.values())
        _kept_connections.clear()
        for entry in entries:
            entry.dropped = True
    for entry in entries:
        if entry.lock.acquire(blocking=wait):
            try:
                if not entry.users:
                    entry.close()
            finally:
                entry.lock.release()


def _close_kept_connections_before_fork() -> None:
    # So that a child inherits none. A save in progress on another thread
    # keeps its connection; the child never touches that one.
    _close_kept_connections(wait=False)


def _close_kept_connections_at_exit() -> None:
    global _kept_connections_closed

    if _kept_connections_pid != os.getpid():
        _forget_kept_connections_after_fork()  # pragma: no cover
    with _kept_connections_lock:
        _kept_connections_closed = True
    _close_kept_connections()
    # The idle closer may be closing a connection it had already taken.
    with _kept_connections_closing:
        pass


def _forget_kept_connections_after_fork() -> None:
    global _kept_connections, _kept_connections_lock, _kept_connections_pid
    global _kept_connections_atexit_registered, _kept_connections_closer
    global _kept_connections_closing, _kept_connections_closer_token

    _kept_connections_closing = threading.Lock()
    # A child can start with the parent's exit handlers cleared, and has
    # none of its threads.
    _kept_connections_atexit_registered = False
    _kept_connections_closer = None
    _kept_connections_closer_token = None
    _inherited_connections.append(_kept_connections)
    _kept_connections = {}
    # Another thread of the parent may have held either lock during the fork.
    _kept_connections_lock = threading.RLock()
    _kept_connections_pid = os.getpid()


if _KEEP_CONNECTIONS:
    os.register_at_fork(
        before=_close_kept_connections_before_fork,
        after_in_child=_forget_kept_connections_after_fork,
    )


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

    trace_path.parent.mkdir(parents=True, exist_ok=True)

    trace_path.write_bytes(msgpack_data)

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
    file_result = load_trace_from_file(trace_id, db_path)
    if file_result is not None:
        msgpack_data, file_created_at = file_result
        return msgpack_data, db_created_at or file_created_at

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
    # Partial index over traces still holding inline blobs, so migration_pending() is O(1).
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
        pass

    try:
        connection.execute(
            "ALTER TABLE traces ADD COLUMN auto_generated_name TEXT NULL"
        )
    except sqlite3.OperationalError:
        pass


def setup_db() -> Path:
    db_path = get_db_path()

    kept = _acquire_kept_connection(db_path, 60)
    if kept is None:
        with db_connection(db_path) as connection:
            create_traces_table(connection)
            migrate_db(connection)
        return db_path
    current = wrote = False
    try:
        wrote = kept.ensure_schema()
        current = True
    finally:
        kept.release(keep=current, wrote=wrote)
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
    ignore = " OR IGNORE" if ignore_errors else ""

    if created_at is not None:
        created_at_str = created_at.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        insert_sql = f"INSERT{ignore} INTO traces(id, created_at) VALUES(?, ?)"
        params: tuple = (trace_id, created_at_str)
    else:
        insert_sql = f"INSERT{ignore} INTO traces(id) VALUES(?)"
        params = (trace_id,)

    failed = False
    with db_connection(db_path, timeout, keep=True) as connection:
        try:
            connection.execute(insert_sql, params)
        except Exception as e:
            failed = True
            logger.warning(f"Failed to save trace metadata to database: {e}")
            if not ignore_errors:
                delete_trace_file(trace_id, db_path)  # pragma: no cover
                raise  # pragma: no cover
    if failed:
        _forget_kept_connection(db_path)


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

    if _existing_trace_file_path(trace_id, db_path) is not None:
        return True

    with db_connection(db_path) as connection:
        cursor = connection.execute("SELECT 1 FROM traces WHERE id = ?", (trace_id,))
        return cursor.fetchone() is not None


def load_trace_from_db(db_path: Path, trace_id: str) -> Tuple[bytes, str]:
    """
    Load a trace, checking files first, then falling back to the database.

    Returns (msgpack_bytes, created_at_string).
    """
    file_result = load_trace_from_file(trace_id, db_path)
    if file_result is not None:
        return file_result

    fetch_sql = "SELECT msgpack, created_at FROM traces WHERE id = ?"

    with db_connection(db_path) as connection:
        cursor = connection.execute(fetch_sql, (trace_id,))
        row = cursor.fetchone()

    if row is None:
        raise TraceNotFoundError(trace_id)

    msgpack_data, created_at = row
    if msgpack_data is None:
        raise TraceNotFoundError(trace_id)

    return msgpack_data, created_at


def load_trace_with_size_from_db(
    db_path: Path, trace_id: str
) -> Tuple[str, str, int, bytes]:
    """
    Load a trace with size info, checking files first, then falling back to the database.

    Returns (id, created_at, size, msgpack_bytes).
    """
    file_result = load_trace_from_file(trace_id, db_path)
    if file_result is not None:
        msgpack_data, created_at = file_result
        return trace_id, created_at, len(msgpack_data), msgpack_data

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

            try:
                loaded = _load_trace_data_for_row(
                    trace_id, db_msgpack, db_created_at, db_path
                )
            except Exception as e:
                logger.warning(f"Could not load trace {trace_id}: {e}")
                continue
            if loaded is None:
                logger.warning(f"Trace {trace_id} has no data in file or database")
                continue

            msgpack_data, created_at = loaded
            if not isinstance(msgpack_data, (bytes, bytearray, memoryview)):
                logger.warning(f"Trace {trace_id} has data of the wrong type")
                continue
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

            try:
                loaded = _load_trace_data_for_row(
                    trace_id, db_msgpack, db_created_at, db_path
                )
            except Exception as e:
                logger.warning(f"Could not load pinned trace {trace_id}: {e}")
                continue
            if loaded is None:
                logger.warning(
                    f"Pinned trace {trace_id} has no data in file or database"
                )
                continue

            msgpack_data, created_at = loaded
            if not isinstance(msgpack_data, (bytes, bytearray, memoryview)):
                logger.warning(f"Trace {trace_id} has data of the wrong type")
                continue
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
    for trace_id in trace_ids:
        delete_trace_file(trace_id, db_path)

    params = ", ".join("?" * len(trace_ids))
    delete_sql = f"DELETE FROM traces WHERE id in ({params})"

    with db_connection(db_path) as connection:
        cursor = connection.execute(delete_sql, trace_ids)
        return cursor.rowcount


def delete_traces_before(db_path: Path, before: datetime):
    """Delete traces created before the given datetime from both files and database."""
    # created_at is stored as UTC text (millisecond precision); naive `before`
    # is treated as local time. Match the file mtime check below: a row from
    # the cutoff's millisecond is older only if the cutoff has sub-ms digits.
    cutoff = before.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
    if cutoff.endswith("000"):
        cutoff = cutoff[:-3]

    select_sql = "SELECT id FROM traces WHERE created_at < ?"

    with db_connection(db_path) as connection:
        cursor = connection.execute(select_sql, (cutoff,))
        trace_ids = [row[0] for row in cursor.fetchall()]

    for trace_id in trace_ids:
        delete_trace_file(trace_id, db_path)

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

    delete_sql = "DELETE FROM traces WHERE (created_at < ?)"

    with db_connection(db_path) as connection:
        connection.execute(delete_sql, (cutoff,))
        cursor = connection.execute("SELECT changes()")
        deleted_count = cursor.fetchone()[0]
    return deleted_count


def vacuum_db(db_path):
    # VACUUM changes no rows, so say that the file is about to be rewritten.
    _forget_kept_connection(db_path)
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
            pass

        cursor = connection.execute(
            "UPDATE traces SET is_pinned = 1 WHERE id = ?",
            (trace_id,),
        )

        if cursor.rowcount > 0:
            return True

        file_result = load_trace_from_file(trace_id, db_path)
        if file_result is not None:
            _, created_at_str = file_result
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


def _migrate_one(
    trace_id: str,
    msgpack_data: bytes | None,
    json_data: str | None,
    created_at_str: str,
    db_path: Path,
) -> bool:
    """Write one trace's inline db data to file storage. Returns success."""
    try:
        if msgpack_data is not None:
            data_to_save = msgpack_data
        elif json_data is not None:
            data_to_save = dump_msgpack(json.loads(json_data))
        else:  # pragma: no cover
            return False

        try:
            created_at = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S.%f")
            created_at = created_at.replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            created_at = datetime.now(tz=timezone.utc)

        # Save to file atomically: reads prefer the file over the db
        # row, so a write cut short (e.g. auto-emit's CPU limit) must
        # not leave a truncated file shadowing the intact row.
        save_trace_chunks_to_file(
            trace_id, (data_to_save,), created_at=created_at, db_path=db_path
        )
    except Exception as e:
        logger.warning(f"Failed to migrate trace {trace_id}: {e}")
        return False
    return True


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

        successful_ids: list[str] = []
        try:
            for trace_id, msgpack_data, json_data, created_at_str in batch:
                if _migrate_one(
                    trace_id, msgpack_data, json_data, created_at_str, db_path
                ):
                    successful_ids.append(trace_id)
        finally:
            # Clear rows even on BaseException (auto-emit's CPULimitExceeded)
            # so already-written traces aren't re-migrated next time.
            if successful_ids:
                placeholders = ", ".join("?" * len(successful_ids))
                with db_connection(db_path) as connection:
                    connection.execute(
                        f"UPDATE traces SET msgpack = NULL, data = NULL WHERE id IN ({placeholders})",
                        tuple(successful_ids),
                    )

        if not successful_ids:
            if batch:
                logger.warning(
                    f"All {len(batch)} traces failed to migrate, stopping migration"
                )
            break

        total_migrated += len(successful_ids)

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

        cursor = connection.execute(
            "SELECT COUNT(*) FROM traces WHERE data IS NOT NULL AND msgpack IS NULL"
        )
        json_traces = cursor.fetchone()[0]

        cursor = connection.execute("SELECT COUNT(*) FROM traces")
        total_traces = cursor.fetchone()[0]

    # Globs all of raw/ (possibly >1M entries): opt-in, never on the auto-emit hot path.
    file_traces = -1
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
