"""Headroom: backpressure -- the queue ceiling, the free-space floor and the staging budget an append must leave."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import time

from probe.foundation.durable.durable import file_lock
from probe.sdk.delivery.status_fields import StatusField


def _inline_hash_max() -> int:
    raw = os.environ.get("PROBE_ASYNC_INLINE_HASH_MAX")
    if raw:
        try:
            return int(raw)
        except ValueError:
            # A malformed override must not crash every import of this module (client
            # construction, enqueue, the drainer): fall back loudly.
            import warnings

            warnings.warn(
                f"ignoring malformed PROBE_ASYNC_INLINE_HASH_MAX={raw!r}; "
                "expected an integer byte count",
                stacklevel=2,
            )
    return 256 * 1024 * 1024


#: 11A -- files at or under this size hash (and presign-ping) inline at
#: enqueue; larger ones snapshot instantly and hash in the drainer.
INLINE_HASH_MAX_BYTES = _inline_hash_max()


def _min_free_bytes() -> int | None:
    """``PROBE_OUTBOX_MIN_FREE_BYTES``, or None: scale with the volume
    (`free_floor`)."""
    raw = os.environ.get("PROBE_OUTBOX_MIN_FREE_BYTES")
    if raw:
        try:
            return max(0, int(raw))
        except ValueError:
            # Same contract as _inline_hash_max: a malformed override falls back loudly.
            import warnings

            warnings.warn(
                f"ignoring malformed PROBE_OUTBOX_MIN_FREE_BYTES={raw!r}; "
                "expected an integer byte count",
                stacklevel=2,
            )
    return None


#: The free-space floor without an override (plan 1.5): 5 % of the volume, never under 256 MiB
#: (unless that is over a quarter of the volume) and never over 2 GiB. A fixed 2 GiB floor
#: refused every write on a small pod volume or a laptop with 1.9 GiB free while the network
#: was fine (live: 0 of 30 points arrived).
_FLOOR_CEILING = 2 * 1024 * 1024 * 1024
_FLOOR_MINIMUM = 256 * 1024 * 1024
_FLOOR_FRACTION = 0.05


def free_floor(directory: str | Path) -> int:
    """The free bytes a queue on ``directory`` must leave (0: no floor)."""
    if MIN_FREE_BYTES is not None:
        return MIN_FREE_BYTES
    try:
        total = shutil.disk_usage(directory).total
    except OSError:
        return _FLOOR_CEILING
    # Never more than a quarter of the volume: on a small tmpfs (a fallback $TMPDIR under
    # 256 MiB) the minimum would exceed the whole disk and refuse every write (review of #2054).
    return min(_FLOOR_CEILING, max(_FLOOR_MINIMUM, int(total * _FLOOR_FRACTION)), total // 4)


#: Free space the blob store must leave on its filesystem (0 disables the guard): a producer
#: outrunning delivery otherwise fills the disk. DESIGN.md: why it ignores copy-on-write clones.
MIN_FREE_BYTES = _min_free_bytes()


def _max_pending_ops() -> int:
    raw = os.environ.get("PROBE_OUTBOX_MAX_PENDING")
    if raw:
        try:
            return max(0, int(raw))
        except ValueError:
            import warnings

            warnings.warn(
                f"ignoring malformed PROBE_OUTBOX_MAX_PENDING={raw!r}; "
                "expected an integer op count",
                stacklevel=2,
            )
    return 500_000


#: Backstop on QUEUE LENGTH, independent of the byte floor. Op files are small, so a stalled
#: drainer exhausts inodes and directory-scan patience long before bytes: a loop logging ten
#: points a second queues ~864k files a day. Zero disables. The floor normally bites; this
#: catches a filesystem reporting plenty of free space that cannot take another entry.
MAX_PENDING_OPS = _max_pending_ops()

#: Sample the free-space stat every N appends, not each one: disk pressure builds over
#: thousands of writes, and a per-append statvfs would bring back the per-write syscall cost
#: the enqueue just shed.
_STATVFS_EVERY = 256

#: At most one real directory count of the queue per this many seconds, only on the path that
#: would otherwise REFUSE a write (plan 0.1): a drain pass rewrites status.json only when it
#: ends, so mid-pass the file still says "full" while the real queue has drained (review of
#: #2014: 94 queued, status.json 200, 20 of 20 writes refused; at 500k and ~13 ops/s a pass is
#: hours of refused data).
_RECOUNT_EVERY_SECONDS = 1.0


class OutboxFull(OSError):
    """The journal refused a write because the queue is at its ceiling. An OSError subclass on
    purpose: `Client._enqueue` already treats a failure to journal as "drop the datapoint,
    record the gap, keep training", and a full outbox is that same disk-shaped refusal.
    """


class HeadroomMixin:
    """Part of Journal: its methods run with `self` the Journal; fold_parts() copies them into Journal."""

    def _refresh_pending_estimate(self) -> int:
        """Re-seed `_pending_estimate` from status.json. One small file read."""
        status = self.read_status(self.dir, include_receipts=False) or {}
        try:
            pending = int(status.get(StatusField.PENDING) or 0)
        except (TypeError, ValueError):
            pending = 0
        self._pending_estimate = pending
        return pending

    def _recount_pending(self) -> int | None:
        """The REAL queue length from a directory listing, at most once per
        `_RECOUNT_EVERY_SECONDS` (None when too soon). Only the refusal path calls it, so the
        common append never lists the queue."""
        now = time.monotonic()
        if now - self._recounted_at < _RECOUNT_EVERY_SECONDS:
            return None
        self._recounted_at = now
        # Counted OUTSIDE the append lock, names only and unsorted: a sorted listing of a queue at
        # the cap (500k names) held every other writer's `log()` for its whole length. Each append
        # landing during the listing is missing from the stored count (at the cap, a few per
        # second), so the estimate can read low until the next drain pass recounts: it can admit a
        # few writes over the cap, never refuse one under it.
        try:
            count = sum(1 for name in os.listdir(self.ops_dir) if name.endswith(".json"))
        except FileNotFoundError:
            count = 0
        with file_lock(self.append_lock):
            # Store it, or the next append's delta would rebuild the stale number from status.json
            # and refuse again.
            self._write_status_locked(recount=False, set_pending=count)
        self._pending_estimate = count
        return count

    def _append_headroom(self, *, check_free: bool = True, extra: int = 0) -> str | None:
        """None when there is room for one more op, else why not: the sampled free-space floor and the op
        ceiling, for every append (they once guarded upload staging only)."""
        ceiling = MAX_PENDING_OPS if self.op_ceiling is None else self.op_ceiling
        pending = self._pending_estimate
        other = self._sibling_pending_count()
        if pending is None and extra:
            pending = self._refresh_pending_estimate()
        if pending is not None:
            pending += other + extra
        if pending is not None and ceiling > 0 and pending >= ceiling:
            # Re-read before refusing: a refusal is a dropped datapoint, and another process's
            # drain may have lowered the count since.
            other = self._sibling_pending_count(fresh=True)
            pending = self._refresh_pending_estimate() + other + extra
        if pending is not None and ceiling > 0 and pending >= ceiling:
            # status.json can still say "full" mid-drain-pass after most of the queue was
            # delivered: count it for real.
            real = self._recount_pending()
            if real is not None:
                pending = real + other + extra
        if pending is not None and ceiling > 0 and pending >= ceiling:
            return (
                f"outbox full: {pending} ops queued, at the {ceiling} "
                "ceiling (PROBE_OUTBOX_MAX_PENDING). Delivery is not keeping up "
                "— see `probe outbox status`"
            )
        if not check_free:
            # The caller already made its own headroom decision. `append_upload` asks
            # `_staging_headroom` first and DEGRADES to an unstaged op (a small reference, not a
            # byte copy): the path that must keep working when the disk is tight. Blocking it here
            # would refuse the write the degrade exists to preserve. The op-count ceiling above
            # still applies.
            return None
        return self.below_floor()

    def below_floor(self) -> str | None:
        """Why the queue's volume is under its free-space floor, or None. Sampled, not per call
        (disk pressure builds over thousands of writes): the statvfs runs every
        `_STATVFS_EVERY` calls, and on every call while the last sample was low, so recovery is
        seen at once. `Client` asks before it queues (plan 1.5: below the floor it may send
        directly) and every append asks again."""
        floor = self._free_floor()
        if floor <= 0:
            return None
        self._appends_since_statvfs += 1
        if self._appends_since_statvfs < _STATVFS_EVERY and self._last_free_ok:
            return None
        self._appends_since_statvfs = 0
        free = self._measure_free_bytes()
        self._last_free_ok = free is None or free >= floor  # unmeasurable is not a breach
        if free is None:
            return None
        if self._last_free_ok:
            return None
        return (
            f"low disk: {free} bytes free on {self.ops_dir}, under the "
            f"{floor}-byte floor (PROBE_OUTBOX_MIN_FREE_BYTES). Queued writes "
            "are sent directly while nothing is queued, else dropped rather "
            "than filling the filesystem"
        )

    def is_below_floor_now(self) -> bool:
        """Whether the queue's volume is under its free-space floor right now: one statvfs, never
        sampled (a drainer's collect window, review of #3785, C6). Unmeasurable is not below."""
        floor = self._free_floor()
        if floor <= 0:
            return False
        free = self._measure_free_bytes()
        return free is not None and free < floor

    def _measure_free_bytes(self) -> int | None:
        """Free bytes on the queue's volume, or None when unmeasurable."""
        try:
            return shutil.disk_usage(self.ops_dir if self.ops_dir.exists() else self.dir).free
        except OSError:
            return None

    def _free_floor(self) -> int:
        """`free_floor` for this journal's volume, measured once (a volume's size does not
        change under a running process; an override needs no measuring)."""
        if MIN_FREE_BYTES is not None:
            return MIN_FREE_BYTES
        floor = getattr(self, "_floor_cached", None)
        if floor is None:
            where = self.dir if self.dir.exists() else self.dir.parent
            floor = self._floor_cached = free_floor(where)
        return floor

    def _sibling_pending_count(self, *, fresh: bool = False) -> int:
        """The other namespace's (`delivery-v1` <-> the root) pending count, which the op ceiling
        counts too. Re-read every `_STATVFS_EVERY` appends and before any refusal (``fresh``), not
        each append: it was a status.json open per `log()` for a namespace nearly always empty
        for a training loop (plan 1.3)."""
        self._appends_since_sibling += 1
        if (
            fresh
            or self._sibling_pending is None
            or self._appends_since_sibling >= _STATVFS_EVERY
        ):
            self._appends_since_sibling = 0
            sibling = self.dir.parent if self.receipt_enabled else self.dir / DELIVERY_NAMESPACE
            other = self.read_status(sibling, include_receipts=False) or {}
            try:
                self._sibling_pending = int(other.get(StatusField.PENDING) or 0)
            except (TypeError, ValueError):
                self._sibling_pending = 0
        return self._sibling_pending

    def _staging_headroom(self, src_path: str | Path, *, copies: int = 1) -> str | None:
        """``None`` when there is room to stage ``src_path``, else WHY not. Two stat-class
        syscalls, no read of the file: this runs on every upload enqueue beside a training loop
        and must not scale with the bytes queued. Unmeasurable is NOT a breach (no evidence to
        degrade on; enqueue is fail-open).
        """
        floor = self._free_floor()
        if floor <= 0:
            return None
        try:
            size = os.path.getsize(src_path)
            free = shutil.disk_usage(self.blobs_dir).free
        except OSError:
            return None
        if free - copies * size >= floor:
            return None
        return (
            f"low disk: staging {size} bytes would leave {free - copies * size} bytes "
            f"free on {self.blobs_dir}, under the {floor}-byte floor "
            "(PROBE_OUTBOX_MIN_FREE_BYTES); the op references the source "
            "instead and the drainer reads its original bytes"
        )
from probe.sdk.delivery.ops.ops import DELIVERY_NAMESPACE  # noqa: E402 -- pieces need each other; the front door loads this one first
