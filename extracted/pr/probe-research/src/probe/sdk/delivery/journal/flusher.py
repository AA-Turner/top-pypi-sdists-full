"""JournalFlusher: fsyncs the op files `log()` wrote without one, then their folders, about every
second and at `finish()`, the SIGTERM close and exit (plan T6, D1 = A). One per process."""

from __future__ import annotations

import atexit
import os
import threading
import time

from probe.foundation.compat.compat import StrEnum

#: `each` keeps the per-op fsync (before 0.36x); `interval` (the default) leaves it to the flusher.
FSYNC_ENV = "PROBE_OUTBOX_FSYNC"
FLUSH_EVERY_SECONDS = 1.0
#: Past this many unsynced files, or this much age on the oldest, writers fsync their own op
#: again: a disk slower than the writes never builds a backlog a close must wait out (review of #3785, C2).
BACKLOG_MAX_FILES = 1_000
BACKLOG_MAX_SECONDS = FLUSH_EVERY_SECONDS + 1.0
#: How long a flush outside the flusher thread waits for a flush already running before it
#: syncs that flush's files itself: it may be the frame a SIGTERM interrupted (review of #3785, C1).
_LOCK_WAIT_SECONDS = 0.5
#: A flush at exit stops starting fsyncs after this long.
_EXIT_FLUSH_SECONDS = 5.0
#: A writer catching up for a dead flusher holds the journal's append lock (every process's
#: writes wait): it stops starting fsyncs after this long; finish() and exit get the rest.
_CATCH_UP_SECONDS = 1.0
#: A file whose fsync failed is counted at once, tried once more at the next flush, then forgotten.
_FSYNC_TRIES = 2


class FsyncMode(StrEnum):
    """When an op written by `log()` reaches the disk platter."""

    EACH = "each"  # fsync per op, before the write returns
    INTERVAL = "interval"  # the flusher, within ~2 s; a process death still loses nothing


def get_fsync_mode() -> FsyncMode:
    """`PROBE_OUTBOX_FSYNC`, default `interval`. Windows stays `each`: its fsync needs a
    writable handle, and one held open would make the drain's delete of the op fail."""
    raw = (os.environ.get(FSYNC_ENV) or "").strip().lower()
    if raw in (FsyncMode.EACH, FsyncMode.INTERVAL):
        return FsyncMode(raw)
    return FsyncMode.EACH if os.name == "nt" else FsyncMode.INTERVAL


class JournalFlusher:
    """Op files written without an fsync, forced to disk by a daemon thread every
    `FLUSH_EVERY_SECONDS` (files first, then each folder, so their renames last too), and by
    `flush()` at a close. A writer asks `can_defer_fsync()` before skipping its own fsync: not
    once the thread has died (it catches up on what it held) nor past the backlog cap.

    Only the flusher thread ever blocks on another flush. Any other caller waits at most
    `_LOCK_WAIT_SECONDS` (never, with ``wait=False``), then syncs the running flush's files
    itself: that flush may be the main thread's, interrupted by a SIGTERM whose handler (and its
    flushes on other threads) it waits behind."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._flushing = threading.Lock()
        self._work = threading.Event()
        #: The loop's pause, an Event so a test patching `time.sleep` never sees it; set early
        #: once half the backlog cap waits, so a fast disk never trips the cap.
        self._tick = threading.Event()
        self._paths: list[str] = []
        #: When the oldest of `_paths` was recorded (monotonic), None while empty.
        self._paths_since: float | None = None
        #: The batch a running flush took, kept until it is down so a caller that cannot wait
        #: for that flush syncs it too.
        self._in_flight: list[str] = []
        self._in_flight_since: float | None = None
        #: Files a flush left (past its deadline, a folder not synced, a failed fsync), first in
        #: line next time. Only a flush holding `_flushing` touches them: no `_lock` needed.
        self._retry: list[str] = []
        self._retry_since: float | None = None
        self._tries: dict[str, int] = {}
        self._thread: threading.Thread | None = None
        self._dead = False
        self._pid = os.getpid()
        #: Files whose fsync failed, so they may not survive a power cut.
        self.failed_fsync_count = 0
        self._has_warned = False

    def can_defer_fsync(self) -> bool:
        """Whether a write may skip its own fsync and `record` its file instead."""
        if self._dead:
            if self._retry or self._paths:
                # What a flusher that died or never started left (a failed fsync, a deadline):
                # retried by the writers it now sends to their own fsync, bounded.
                self.flush(deadline=time.monotonic() + _CATCH_UP_SECONDS)
            return False
        if get_fsync_mode() is FsyncMode.EACH:
            return False
        thread = self._thread
        if thread is not None and not thread.is_alive():
            self._dead = True
            # What it held, now, but bounded: the caller holds the journal's append lock.
            self.flush(deadline=time.monotonic() + _CATCH_UP_SECONDS)
            return False
        return not self._is_backlogged()

    def _is_backlogged(self) -> bool:
        """The disk is not keeping up: too many files wait, or the oldest waited too long."""
        if len(self._paths) + len(self._in_flight) + len(self._retry) >= BACKLOG_MAX_FILES:
            return True
        starts = [t for t in (self._retry_since, self._in_flight_since, self._paths_since) if t is not None]
        return bool(starts) and time.monotonic() - min(starts) > BACKLOG_MAX_SECONDS

    def record(self, path) -> None:
        """An op file just renamed into place without an fsync. Never raises: the op is on disk
        and queued, so a flusher that cannot start (interpreter shutdown, a thread limit) syncs
        it here, and every later write syncs its own (review of #3785, C5)."""
        try:
            with self._lock:
                if not self._paths:
                    self._paths_since = time.monotonic()
                self._paths.append(str(path))
                if self._thread is None:
                    self._start()
                self._work.set()
                if len(self._paths) >= BACKLOG_MAX_FILES // 2:
                    # A writer outrunning the cadence on a fast disk: flush now, before the
                    # cap sends every write to its own fsync (final review of #3794).
                    self._tick.set()
            return
        except Exception:  # noqa: BLE001 -- see the docstring
            self._dead = True
        try:
            self.flush(deadline=time.monotonic() + _CATCH_UP_SECONDS)  # under the append lock
        except Exception:  # noqa: BLE001 -- the write stands; only its durability is at risk
            pass

    def _start(self) -> None:
        # Registered first: a thread that cannot start still leaves files for exit to sync.
        atexit.register(self._flush_at_exit)
        thread = threading.Thread(target=self._loop, name="probe-journal-flusher", daemon=True)
        thread.start()
        self._thread = thread

    def _loop(self) -> None:
        while True:
            self._work.wait()
            self._tick.wait(self._get_pause())
            self._tick.clear()
            try:
                self.flush()
                self.warn_once_if_failed()
            except Exception:  # noqa: BLE001 -- a dead thread sends every write back to its own fsync
                continue

    def _get_pause(self) -> float:
        """Until the oldest waiting file is `FLUSH_EVERY_SECONDS` old, not a full period after the
        last flush: that flush's own time would count toward the backlog's age cap, which then
        sent `log()` back to its own fsync while the flusher kept up (final review of #3794)."""
        starts = [t for t in (self._retry_since, self._paths_since) if t is not None]
        if not starts:
            return FLUSH_EVERY_SECONDS
        return max(0.0, min(starts) + FLUSH_EVERY_SECONDS - time.monotonic())

    def _flush_at_exit(self) -> None:
        self.flush(deadline=time.monotonic() + _EXIT_FLUSH_SECONDS)
        self.warn_once_if_failed()

    def warn_once_if_failed(self) -> None:
        """Say once that fsyncs failed (review of #3785, I8). Not from the SIGTERM handler,
        whose interrupted frame may hold stderr's lock."""
        if self.failed_fsync_count and not self._has_warned:
            self._has_warned = True
            _diagnostics.warn(
                f"probe: {self.failed_fsync_count} queued write(s) could not be forced to disk "
                "(fsync failed); they are queued, but a power cut may lose them"
            )

    def flush(self, *, deadline: float | None = None, wait: bool = True) -> int:
        """fsync every recorded file still there, then their folders; returns how many files.
        On return everything recorded before is down, unless ``deadline`` (monotonic) passed
        first: no fsync starts after it, and what it left is kept for the next flush.
        ``wait=False``: never wait for a flush already running (the SIGTERM default action)."""
        if self._pid != os.getpid():
            return 0  # a forked child: the parent's locks may be held forever here
        if deadline is not None and time.monotonic() >= deadline:
            # No fsync may start: moving the lists anyway raced a dying flush's copy of them.
            return 0
        thread = self._thread
        # `get_ident()`, not `current_thread()`: on a raw `_thread` (the dying flush) that takes
        # `threading`'s limbo lock, which the frame a SIGTERM interrupted may hold.
        if thread is not None and threading.get_ident() == thread.ident:
            got = self._flushing.acquire()
        else:
            patience = _LOCK_WAIT_SECONDS if deadline is None else min(_LOCK_WAIT_SECONDS, deadline - time.monotonic())
            got = self._flushing.acquire(timeout=patience) if wait and patience > 0 else self._flushing.acquire(False)
        try:
            # Without the lock: a copy of the running flush's batch and of what came since,
            # synced beside it (an fsync twice is harmless; one skipped is not).
            try:
                paths = self._take() if got else [*self._retry, *self._in_flight, *self._paths]
                synced, left = self._sync(paths, deadline)
                if got and left:
                    self._put_back(left)
            except BaseException:
                if got:
                    # Ctrl-C mid-flush: the batch is kept, or nobody would ever sync it (an
                    # fsync twice is harmless).
                    self._put_back(list(self._in_flight))
                raise
            return synced
        finally:
            if got:
                self._in_flight = []
                self._in_flight_since = None
                self._flushing.release()

    def _take(self) -> list[str]:
        """The files to retry and the recorded ones, as the in-flight batch (the caller holds
        `_flushing`)."""
        is_locked = self._lock.acquire(timeout=_LOCK_WAIT_SECONDS)
        try:
            # Published BEFORE either list is cleared: a SIGTERM landing in between finds every
            # file in one of the three lists `flush(wait=False)` copies (final review of #3794).
            self._in_flight = [*self._retry, *self._paths]
            # Its oldest file's age: a put-back file is stamped when put back, often after the
            # others were recorded.
            starts = [t for t in (self._retry_since, self._paths_since) if t is not None]
            self._in_flight_since = min(starts) if starts else None
            self._retry, self._retry_since = [], None
            if is_locked:
                self._paths, self._paths_since = [], None
                self._work.clear()
            # Else its holder was interrupted: the batch is a copy and its list stays.
        finally:
            if is_locked:
                self._lock.release()
        return self._in_flight

    def _put_back(self, left: list[str]) -> None:
        """Files this flush did not get down: first in line next time (the caller holds
        `_flushing`, so it needs no `_lock`, which an interrupted writer may hold)."""
        self._retry = [*left, *self._retry]
        if self._retry_since is None:
            # Aged from now, not from the batch: a file that fails its fsync every time would
            # otherwise keep the backlog "too old" for good (final review of #3794).
            self._retry_since = time.monotonic()
        self._work.set()

    def _note_failure(self, path: str, left: list[str]) -> None:
        """Count a failed fsync at once: Linux reports a writeback error once, so a retry that
        succeeds proves nothing ("fsyncgate"). Tried once more all the same, then forgotten."""
        tries = self._tries.get(path, 0) + 1
        if tries == 1:
            self.failed_fsync_count += 1
        if tries < _FSYNC_TRIES:
            self._tries[path] = tries
            left.append(path)
        else:
            self._tries.pop(path, None)

    def _sync(self, paths: list[str], deadline: float | None) -> tuple[int, list[str]]:
        """fsync ``paths`` then their folders; (how many files, the ones to try again). A file
        whose folder the deadline left unsynced is tried again too: its rename is not down."""
        folders: dict[str, list[str]] = {}
        synced = 0
        left: list[str] = []
        for index, path in enumerate(paths):
            if deadline is not None and time.monotonic() >= deadline:
                left.extend(paths[index:])
                break
            try:
                fd = os.open(path, os.O_RDONLY)
            except FileNotFoundError:
                self._tries.pop(path, None)
                continue  # delivered and removed meanwhile: nothing left to lose
            except OSError:
                self._note_failure(path, left)  # EMFILE, EACCES: not down, and not gone
                continue
            try:
                os.fsync(fd)
                synced += 1
                self._tries.pop(path, None)
            except OSError:
                self._note_failure(path, left)
            finally:
                try:
                    os.close(fd)
                except OSError:
                    pass  # NFS reports a deferred error here; the fsync above already answered
            folders.setdefault(os.path.dirname(path), []).append(path)
        unsynced = set(left)
        for folder in sorted(folders):
            if deadline is not None and time.monotonic() >= deadline:
                left.extend(path for path in folders[folder] if path not in unsynced)
                continue
            fsync_directory(folder)
        return synced, left


_FLUSHER: JournalFlusher | None = None
_FLUSHER_LOCK = threading.Lock()


def get_journal_flusher() -> JournalFlusher:
    """This process's flusher (a forked child gets its own: the parent's thread is not in it)."""
    global _FLUSHER
    flusher = _FLUSHER
    if flusher is None or flusher._pid != os.getpid():
        with _FLUSHER_LOCK:
            if _FLUSHER is None or _FLUSHER._pid != os.getpid():
                _FLUSHER = JournalFlusher()
            flusher = _FLUSHER
    return flusher


def flush_journal(*, deadline: float | None = None, wait: bool = True, warn: bool = False) -> int:
    """Force this process's unsynced op files to disk now (a close, SIGTERM), starting no fsync
    after ``deadline`` (monotonic). ``wait=False`` never waits for a flush already running;
    ``warn`` says once if fsyncs failed (never from a signal handler). Never raises."""
    flusher = _FLUSHER
    if flusher is None or flusher._pid != os.getpid():
        return 0
    try:
        synced = flusher.flush(deadline=deadline, wait=wait)
        if warn:
            flusher.warn_once_if_failed()
        return synced
    except Exception:  # noqa: BLE001 -- a close may never raise
        return 0


from probe.foundation.durable.durable import fsync_directory  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.foundation.safe_warn import safe_warn as _diagnostics  # noqa: E402 -- pieces need each other; the front door loads this one first
