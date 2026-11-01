"""the drain lock: take it, and hand it fairly to a close that is waiting for it between two ops."""

from __future__ import annotations
import hashlib
import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from ....._shared import oscompat
from .... import errors


#: How long a pass keeps the drain lock before letting go once between two ops (#3618, R11). A
#: close that says it is waiting (`Journal.drain_want`) gets the lock at the next op; this is
#: for one that only polls: an older release's `finish()`, which waited out whole passes, up
#: to 600 s.
PASS_HOLD_SECONDS = 3.0
#: How long that letting go lasts: about half the gap between two polls of an older release's
#: `_take_drain_lock` late in its wait (0.25 s), so such a close gets in within a few
#: letting-go's, and a pass nobody waits on loses 3%.
_LET_GO_PAUSE_SECONDS = 0.1
#: Longest a pass waits, lock let go, for the closes waiting on it to take it in turn (they
#: poll every 20 ms). One that holds the signal and never takes the lock (a stopped process)
#: is ignored for `PASS_HOLD_SECONDS`, then twice as long each repeat, up to
#: `_WANT_IGNORE_MAX_SECONDS`.
_WANT_WAIT_SECONDS = 2.0
_WANT_IGNORE_MAX_SECONDS = 60.0
#: Run-lock slots per queue. Two runs that share one only wait for each other.
_RUN_LOCK_SLOTS = 256


@contextmanager
def _wanting(path: Path | None):
    """Say "a close is waiting for the drain lock" while the body runs: a shared flock on
    ``path`` (None: say nothing). Best-effort: a platform with no shared lock (Windows) lets
    one waiter say it at a time, which is enough."""
    if path is None:
        yield
        return
    try:
        handle = open(path, "a+")
    except OSError:
        yield
        return
    try:
        for _ in range(5):
            try:
                oscompat.flock(handle.fileno(), oscompat.LOCK_SH | oscompat.LOCK_NB)
                break
            except BlockingIOError:
                # A pass checking the signal holds it exclusively for a moment.
                time.sleep(0.001)
            except OSError:
                break
        yield
    finally:
        try:
            oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
        except OSError:
            pass
        handle.close()


class _LockNotBack(errors.DeadlineExceeded):
    """A close's pass let go of the drain lock and could not take it back by its deadline
    (another drain, an older release's that never gives it up mid-pass, kept it). The pass
    ends where it is and touches no op file: what it sent meanwhile stays queued for the next
    drain (#3618)."""


def _take_drain_lock(
    handle, *, wait_for_lock: bool, timeout: float | None, want: Path | None = None
) -> bool:
    """Take the drain flock. ``timeout`` None: block (``wait_for_lock``) or try once.
    Otherwise POLL until free or ``timeout`` seconds pass (a blocking flock has no timeout and
    a close waiting on a worker's long pass must be able to give up at its deadline).
    ``want`` (a run's close): while waiting it says so (`_wanting`) so the pass holding the
    lock gives it up at its next op, and it polls often enough to take it then."""
    try:
        oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        return True
    except BlockingIOError:
        if timeout is None and not wait_for_lock:
            return False
    with _wanting(want):
        if timeout is None:
            oscompat.flock(handle.fileno(), oscompat.LOCK_EX)
            return True
        give_up = time.monotonic() + max(0.0, timeout)
        pause = 0.01
        cap = 0.02 if want is not None else 0.25
        while True:
            try:
                oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
                return True
            except BlockingIOError:
                left = give_up - time.monotonic()
                if left <= 0:
                    return False
                time.sleep(min(pause, left))
                pause = min(pause * 2, cap)


class _DrainHold:
    """One pass's hold on its queue's drain lock, which it gives up and takes back mid-pass
    (#3618).

    One pass held the lock from scan to status write, so a `finish()` waited behind every
    upload the pass sent: ~400 s per run behind a swarm's 10k ops, against a 600 s cap. Now
    the pass lets go of the lock:

    * while it waits on the network for an upload (`away`), holding that run's lock (one
      flock per run slot under `Journal.run_locks_dir`), so no other drain sends that run
      meanwhile and its order holds;
    * between two ops (`between_ops`) when a close says it is waiting
      (`Journal.drain_want`), or once it has held the lock `PASS_HOLD_SECONDS`.

    Every drain takes a run's lock only while holding the drain lock, and only tries one
    (never waits on it) there, so a run whose lock is free under the drain lock stays free
    until this pass lets go, and no two drains wait on each other. Another drain may deliver,
    park or dead-letter ops while this pass is away, so after the first letting-go every op is
    checked on disk before acting (`fresh`). A receipt queue (an import) never lets go: its
    receipts are written in queue order.

    A close's pass (``urgent``) takes the lock back within its deadline
    (`transport.deadline_remaining`, `Run.finish`'s one budget) or raises `_LockNotBack`, and
    lets go only for its uploads and other closes, never on the time limit: an older release's
    worker could take the lock in that gap and keep it for its whole pass."""

    def __init__(self, journal: "Journal", handle, *, urgent: bool) -> None:
        self.journal = journal
        self.handle = handle
        #: A run's close (a barrier): it says it is waiting when it takes the
        #: lock back, so a worker's pass gives way to it.
        self.urgent = urgent
        self.yields = not journal.receipt_enabled
        #: How many times this pass let go of the lock.
        self.let_go = 0
        #: Op name -> (inode, size, mtime) when this pass last read it.
        self.stamps: dict[str, tuple] = {}
        self._since = time.monotonic()
        self._slots: dict[str, Any] = {}
        self._mine: set[str] = set()
        self._want: Any = None
        self._ignore_want_until = 0.0
        self._ignore_for = PASS_HOLD_SECONDS

    # -- the drain lock ------------------------------------------------------

    def _release(self) -> None:
        oscompat.flock(self.handle.fileno(), oscompat.LOCK_UN)
        self.let_go += 1

    def _deadline_left(self) -> float | None:
        """Seconds left of a close's deadline, or None for a pass without one."""
        if not self.urgent:
            return None
        from ... import transport  # lazy: enqueue paths must not import httpx

        left = transport.deadline_remaining(float("inf"))
        return None if left == float("inf") else left

    def _take(self) -> None:
        left = self._deadline_left()
        if not _take_drain_lock(
            self.handle,
            wait_for_lock=True,
            timeout=left,
            want=self.journal.drain_want if self.urgent else None,
        ):
            raise _LockNotBack("the close's deadline passed while another drain held the outbox")
        self._since = time.monotonic()

    def _wanted(self) -> bool:
        """Whether a close is waiting for the lock (it holds `drain_want`)."""
        if time.monotonic() < self._ignore_want_until:
            return False
        try:
            if self._want is None:
                self._want = open(self.journal.drain_want, "a+")
            oscompat.flock(self._want.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        except BlockingIOError:
            return True
        except OSError:
            return False
        oscompat.flock(self._want.fileno(), oscompat.LOCK_UN)
        return False

    def _wait_for_wanters(self) -> bool:
        """With the lock let go: wait until every close that was waiting has taken it (and
        stopped saying so), at most `_WANT_WAIT_SECONDS`, never past this pass's own deadline."""
        left = self._deadline_left()
        give_up = time.monotonic() + min(_WANT_WAIT_SECONDS, _WANT_WAIT_SECONDS if left is None else left)
        pause = 0.001
        while self._wanted():
            if time.monotonic() >= give_up:
                return False
            time.sleep(pause)
            pause = min(pause * 2, 0.02)
        return True

    def between_ops(self) -> None:
        """Between two ops: give the lock to a close waiting for it, and to anyone else once
        held `PASS_HOLD_SECONDS`."""
        if not self.yields:
            return
        if self._wanted():
            self._release()
            try:
                if self._wait_for_wanters():
                    self._ignore_for = PASS_HOLD_SECONDS
                else:
                    self._ignore_want_until = time.monotonic() + self._ignore_for
                    self._ignore_for = min(self._ignore_for * 2, _WANT_IGNORE_MAX_SECONDS)
            finally:
                self._take()
        elif not self.urgent and time.monotonic() - self._since >= PASS_HOLD_SECONDS:
            self._release()
            try:
                time.sleep(_LET_GO_PAUSE_SECONDS)
            finally:
                self._take()

    @contextmanager
    def away(self, lanes):
        """Let go of the drain lock while the body waits on the network for uploads of
        ``lanes``, holding their run locks; take it back after, then drop them. Settle what the
        body sent before the next letting-go: once the run locks drop, nothing stops another
        drain sending it again. Stays put (today's behaviour) when a run's lock cannot be had."""
        lanes = set(lanes)
        if not self.yields or any(str(lane).startswith("local:") for lane in lanes):
            yield
            return
        if not self._keep(lanes):
            self._drop()
            yield
            return
        self._release()
        try:
            yield
        finally:
            try:
                self._take()
            finally:
                self._drop()

    # -- run locks ------------------------------------------------------------

    def _slot(self, lane: Any) -> str:
        digest = hashlib.sha256(str(lane).encode("utf-8", "surrogatepass")).digest()
        return f"{int.from_bytes(digest[:4], 'big') % _RUN_LOCK_SLOTS:03d}"

    def _open_slot(self, slot: str):
        self.journal.run_locks_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        return open(self.journal.run_locks_dir / f"{slot}.lock", "a+")

    def busy(self, lane: Any) -> bool:
        """Whether another drain is sending ``lane`` now (holds the run's lock, its drain lock
        let go). Asked under the drain lock. The slot's file is closed again at once: a pass
        over hundreds of runs must not keep one descriptor per slot (macOS allows 256)."""
        if not self.yields:
            return False
        slot = self._slot(lane)
        if slot in self._mine:
            return False
        try:
            handle = self._open_slot(slot)
        except OSError:
            return False  # no lock to be had: nobody else can hold it either
        try:
            oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        except BlockingIOError:
            return True
        except OSError:
            return False
        else:
            oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
            return False
        finally:
            handle.close()

    def _keep(self, lanes) -> bool:
        for lane in lanes:
            slot = self._slot(lane)
            if slot in self._mine:
                continue
            try:
                handle = self._open_slot(slot)
            except OSError:
                return False
            try:
                oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
            except OSError:  # BlockingIOError included
                handle.close()
                return False
            self._slots[slot] = handle
            self._mine.add(slot)
        return True

    def _drop(self) -> None:
        for slot in self._mine:
            handle = self._slots.pop(slot)
            try:
                oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
            except OSError:
                pass
            handle.close()
        self._mine.clear()

    # -- what changed while away ----------------------------------------------

    def fresh(self, path: Path, op: dict) -> bool:
        """Whether ``op`` is still queued as this pass knows it. False: gone (another drain
        delivered, parked or dead-lettered it while this pass was away). A changed op file is
        re-read in place so the pass acts on what is on disk. Free until the pass first lets go."""
        if not self.let_go:
            return True
        try:
            stat = os.stat(path)
        except OSError:
            return False
        stamp = (stat.st_ino, stat.st_size, stat.st_mtime_ns)
        if self.stamps.get(path.name) == stamp:
            return True
        current = _read_op_file(path)
        if not isinstance(current, dict):
            return False
        op.clear()
        op.update(current)
        self.stamps[path.name] = stamp
        return True

    def close(self) -> None:
        self._drop()
        if self._want is not None:
            try:
                self._want.close()
            except OSError:
                pass
            self._want = None
from probe.sdk.delivery.journal.journal import Journal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import _read_op_file  # noqa: E402 -- pieces need each other; the front door loads this one first
