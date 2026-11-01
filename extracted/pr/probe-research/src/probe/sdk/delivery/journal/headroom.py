"""Headroom: backpressure -- the queue ceiling, the free-space floor and the staging budget an append must leave."""

from __future__ import annotations
import os
import shutil
from pathlib import Path


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


#: Headroom the blob store must LEAVE on its filesystem. Staging is a real byte copy whenever
#: the source is on another filesystem (`try_clone` is copy-on-write and cannot span mounts),
#: so importing a research folder off a network share copies every file under the reference
#: threshold onto local disk. Enqueue is fire-and-forget and the drainer a single worker, so a
#: producer outrunning delivery grows the queue without bound: a full disk is the STEADY STATE
#: of that shape.
#:
#: Deliberately blind to whether the copy would consume space: a same-filesystem clone costs
#: nothing, but so does declining to make one (the drainer reads the source in place), so the
#: conservative answer is never worse and costs one statvfs.
#:
#: Zero disables the guard, for a caller who has measured their own ceiling.
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
