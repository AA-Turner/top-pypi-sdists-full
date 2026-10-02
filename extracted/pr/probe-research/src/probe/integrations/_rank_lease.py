"""A non-zero rank's writer lease on the run rank 0 opened (plans 2.8, (a), (b)).

Shared by the trainer integrations (``lightning``, ``huggingface``); nothing
here imports a framework. Plan 2.8's server tells a lost node from a finished
job only if EVERY rank of a distributed job holds a writer lease, while the
metrics stay rank-0-only. So rank 0 broadcasts ``(run id, write epoch)`` and
every other rank calls :func:`hold`, which joins that run as a LEASE-ONLY
writer:

* its handle beats a ``rank`` lease from its beat thread and writes nothing
  else: no metric, no capture, no hardware sampling, no config, and never a
  status. The server closes the run from its leases, the worst verdict of
  every writer winning;
* the lease is released when the process exits -- atexit, and for a
  multiprocessing worker (``ddp_fork``, ``ddp_spawn``), whose fork exit skips
  atexit, multiprocessing's own worker-exit finalizers -- with how the process
  ended: an uncaught exception or ``sys.exit(non-zero)`` -> ``failed``, Ctrl-C
  -> ``canceled`` (``fluent``'s exit hooks record them; :func:`hold` installs
  them), else ``completed``. An integration that sees the job end first
  releases it itself (:meth:`RankLease.release`). The release is bounded by
  :data:`WORKER_CLOSE_SECONDS` and holds SIGTERM / SIGINT while it runs
  (``run_held``): torch SIGTERMs the surviving ranks the moment one dies;
* a server that takes no per-writer leases gets nothing from this rank: a
  run-level heartbeat from it would keep the run alive after rank 0 is gone
  (the failure 2.8 exists to catch) and flip a ``leases`` run to legacy.

A SIGKILL releases nothing, and neither does a SIGTERM that meets Python's
default handler (it kills the process with no hook at all; no handler is
installed here, as none is for rank 0): the lease stops beating and the
server reads it expired, which is how 2.8 sees a lost rank.
"""

from __future__ import annotations

import atexit
import logging
import multiprocessing
import os
import signal
import sys
import threading
import uuid
from collections.abc import Callable
from typing import Any

from probe.sdk import fluent

from ._worker_exit import WORKER_CLOSE_SECONDS, WORKER_HOLD_SECONDS, capped_finish_timeout, run_held

log = logging.getLogger(__name__)

#: The server feature a lease needs (``/v1/server/features``).
LEASES_FEATURE = "run_writer_leases"

#: This process's live leases: run id -> lease. One per run: a second Trainer
#: on the same run keeps the lease the first one took.
_LEASES: dict[str, RankLease] = {}
_LEASES_LOCK = threading.Lock()


class RankLease:
    """One rank's lease on one run. Released once, by whoever gets there first."""

    def __init__(self, run: Any, client: Any, *, owns_client: bool) -> None:
        self.run = run
        self.run_id = str(run.id)
        self._client = client
        self._owns_client = owns_client
        self._pid = os.getpid()
        self._released = False
        self._lock = threading.Lock()

    @property
    def session_id(self) -> str | None:
        return getattr(self.run, "session_id", None)

    @property
    def released(self) -> bool:
        return self._released

    def release(self, status: str | None = None, *, in_flight: BaseException | None = None) -> None:
        """Release the lease with ``status``, else with how this process is
        ending (``in_flight``: the exception a worker is exiting on). Once, in
        the process that took it; never raises."""
        with self._lock:
            if self._released or os.getpid() != self._pid:
                return
            self._released = True
        with _LEASES_LOCK:
            if _LEASES.get(self.run_id) is self:
                del _LEASES[self.run_id]
        verdict = status or _process_ending(in_flight) or "completed"

        def close() -> None:
            try:
                # The handle sends no status (`_sends_terminal_status`): its
                # close is the release, behind nothing -- it wrote nothing.
                self.run.finish(verdict, flush_timeout=capped_finish_timeout(WORKER_CLOSE_SECONDS))
            except Exception:  # noqa: BLE001 -- a liveness report never takes down the work
                log.debug("probe: releasing the rank's lease on %s failed", self.run_id, exc_info=True)
            finally:
                if self._owns_client:
                    try:
                        self._client.close()
                    except Exception:  # noqa: BLE001
                        pass

        run_held(close, (signal.SIGTERM, signal.SIGINT), WORKER_HOLD_SECONDS)

    def _release_at_exit(self) -> None:
        self.release()

    def _release_at_worker_exit(self) -> None:
        # Inside the worker's `finally`: the exception in flight is how it ends.
        self.release(in_flight=sys.exc_info()[1])


def hold(
    run_id: str,
    write_epoch: int | None,
    *,
    rank: int,
    client: Any = None,
    client_factory: Callable[[], Any] | None = None,
) -> RankLease | None:
    """Beat a ``rank`` lease on ``run_id`` from this process until it exits.

    ``client``: the caller's own (``client=``), used and never closed; else
    one from ``client_factory`` (default ``Client()``), closed with the lease.
    Returns the lease, or None when there is none to hold: the server takes no
    leases, or this process already writes the run under a lease of its own
    (its ``probe.init()`` joined it through ``PROBE_RUN_ID``). A lease this
    process holds on ANOTHER run is released first: rank 0 opened a new run
    for a new Trainer (a sweep loop) and closed that one. Raises when the
    run cannot be joined; the caller decides whether that is fatal."""
    active = fluent.active_run()
    if active is not None and str(active.id) == str(run_id):
        return None
    with _LEASES_LOCK:
        held = _LEASES.get(str(run_id))
        if held is not None and held._pid == os.getpid() and not held.released:
            return held
        previous = [
            lease for lease in _LEASES.values() if lease._pid == os.getpid() and lease.run_id != str(run_id)
        ]
    for lease in previous:
        lease.release()
    owns = client is None
    if owns:
        if client_factory is None:
            from probe.sdk.client import Client

            client_factory = Client
        client = client_factory()
    try:
        handle = _attach(client, str(run_id), write_epoch, rank)
    except BaseException:
        if owns:
            client.close()
        raise
    if handle is None:
        if owns:
            client.close()
        return None
    lease = RankLease(handle, client, owns_client=owns)
    with _LEASES_LOCK:
        _LEASES[lease.run_id] = lease
    # How this process ends (an uncaught exception, sys.exit, Ctrl-C) is what
    # its release says: the same hooks probe.init() installs on rank 0.
    fluent._install_exit_hooks()
    _at_exit(lease._release_at_exit)
    if multiprocessing.parent_process() is not None:
        from multiprocessing import util

        util.Finalize(None, lease._release_at_worker_exit, exitpriority=100)
    return lease


def _at_exit(callback: Callable[[], None]) -> None:
    """``atexit.register``, by a name tests can point elsewhere."""
    atexit.register(callback)


def _attach(client: Any, run_id: str, write_epoch: int | None, rank: int) -> Any:
    """The lease-only handle, or None when the server takes no leases."""
    if not client.supports_feature(LEASES_FEATURE):
        log.debug("probe: rank %s: the server takes no writer leases; this rank holds none", rank)
        return None
    from probe.sdk.client import _writer_lease

    session_id = str(uuid.uuid4())
    # Rank fields from the launcher's environment, as rank 0's own lease reads
    # them, so the two count rank slots the same way. A launcher that sets no
    # RANK (Lightning's own, `ddp_spawn`) leaves both without: this rank then
    # names its rank but no world size, since a declared size would make the
    # server wait for a slot 0 that rank 0's lease never names.
    writer = _writer_lease("rank", session_id)
    writer.setdefault("rank", int(rank))
    handle = client.attach_run(
        run_id,
        heartbeat=True,
        attached=True,
        write_epoch=write_epoch,
        session_id=session_id,
        writer=writer,
    )
    # One rank's ending is not the run's: on a run that is not on leases (an
    # older client opened it, or it fell back to legacy) the close must still
    # never write a status, only release.
    handle._sends_terminal_status = False
    return handle


def _process_ending(in_flight: BaseException | None) -> str | None:
    """How this process is ending, as far as anything recorded it: fluent's
    exit hooks (the last word: an uncaught exception, ``sys.exit``), else the
    exception a worker is exiting on."""
    if fluent._in_hooks_process() and fluent._exit_recorded:
        return fluent._exit_status
    if in_flight is None:
        return None
    if isinstance(in_flight, KeyboardInterrupt):
        return "canceled"
    if isinstance(in_flight, SystemExit):
        if any(cls.__name__ == "SIGTERMException" for cls in type(in_flight).__mro__):
            # Lightning's SIGTERM: a code-less exit that is not a success.
            return "failed"
        from probe.sdk.run import _status_for_system_exit

        return _status_for_system_exit(in_flight.code, in_flight.__context__)[0]
    return "failed" if isinstance(in_flight, Exception) else None
