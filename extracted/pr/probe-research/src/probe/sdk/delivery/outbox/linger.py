"""the worker's exit guard: linger for new work and check whether anything arrived after the last pass."""

from __future__ import annotations

import os
import time
from probe.foundation.compat.compat import StrEnum
from probe.sdk.delivery.outbox.lease import _stop_path
from probe.sdk.delivery.status_fields import StatusField
#: How long a worker that found its queue empty stays, looking every _LINGER_POLL_SECONDS
#: for new work, before exiting (#3625). A training loop queues an op every second or two:
#: a worker leaving after one 1.5 s look was restarted by the next op (38 starts, 37.5
#: CPU-s in 155 s). Far longer than DetachedDrainer.kick_interval, so an op whose kick the
#: writer's throttle swallowed is seen too, and a dying writer's last op (prod smoke
#: 2026-08-06). A look costs a status.json read and a listing of an empty `ops/`; the drain
#: lock is not held, so `finish()` never waits on it.
_LINGER_SECONDS = 30.0
_LINGER_POLL_SECONDS = 0.5
#: Test-only override of _LINGER_SECONDS (seconds; at least one look is always
#: taken). Nothing in production sets it.
LINGER_ENV = "PROBE_OUTBOX_LINGER_S"


def _work_arrived(journal, fresh: dict) -> bool:
    """The exit guard's question: did anything arrive after the pass that found the queue
    empty? status.json's `pending`, a crash-recovery marker, and the multipart queue (plan
    (g)), which status.json never counts. Missing that last one stranded a > 64 MiB upload
    queued in the worker's final stretch: the producer's kick saw the lease held and the
    worker exited `drained`."""
    from .drain.lanes import _multipart_pending_count

    return bool(
        fresh.get(StatusField.PENDING)
        # status.json is bookkeeping: on a full volume the op lands and its count does not
        # (#2090), so a worker trusting the count exited with the op queued and every later
        # write of that run was dropped behind it (7-day soak, 0.200.2). The listing stops
        # at the first op: an idle queue costs one listing of an empty directory.
        or any(_has_queued_op(q) for q in journal.own_namespaces())
        or _multipart_pending_count(journal)
        or any(q.recovery_file.exists() for q in journal.own_namespaces())
    )


class LingerEnd(StrEnum):
    """Why a worker's linger (`_linger`) ended before its time was up."""

    WORK = "work"  # an op arrived: drain it
    WAITING = "waiting"  # an upload in the waiting room: look at it as before
    ASKED = "asked"  # a stop or a pause: the top of the loop reads which


def _linger_polls() -> int:
    """How many looks the linger takes: _LINGER_SECONDS (or LINGER_ENV) of
    them, _LINGER_POLL_SECONDS apart, and never none."""
    try:
        seconds = float(os.environ.get(LINGER_ENV) or _LINGER_SECONDS)
    except ValueError:
        seconds = _LINGER_SECONDS
    if not 0 <= seconds <= _LINGER_SECONDS:  # nan and inf included
        seconds = _LINGER_SECONDS
    return max(1, int(seconds / _LINGER_POLL_SECONDS + 0.5))


def _linger(journal, *, waiting: bool) -> LingerEnd | None:
    """Stay a while with the queue empty, looking for new work (`_work_arrived`) or, as
    ``waiting``, an upload in the waiting room, a stop file or a pause: what ended it, or
    None. Counted looks, not a deadline: the same stay however the wall clock jumps."""
    from ..journal.journal import Journal

    for _ in range(_linger_polls()):
        time.sleep(_LINGER_POLL_SECONDS)
        fresh = Journal.read_status(str(journal.dir), credential_queues=False) or {}
        if _work_arrived(journal, fresh):
            return LingerEnd.WORK
        if waiting and fresh.get(StatusField.WAITING):
            return LingerEnd.WAITING
        if _stop_path(journal).exists() or journal.paused:
            return LingerEnd.ASKED
    return None


def _has_queued_op(journal) -> bool:
    """Whether ``ops/`` holds an op the drain never attempted (``attempts`` 0), from a listing that
    stops at the first one. Asked only when status.json says nothing is pending, which a full disk or
    a crash can leave wrong (#2090); an op set aside earlier is not new work."""
    import json

    try:
        with os.scandir(journal.ops_dir) as entries:
            for entry in entries:
                if not entry.name.endswith(".json"):
                    continue
                try:
                    attempts = json.loads((journal.ops_dir / entry.name).read_text()).get("attempts")
                except (OSError, json.JSONDecodeError, AttributeError):
                    return True  # unreadable: assume it is new rather than spin silently
                try:
                    attempts = int(attempts or 0)
                except (TypeError, ValueError):
                    attempts = 0
                if attempts <= 0:
                    return True
    except OSError:
        return False
    return False
