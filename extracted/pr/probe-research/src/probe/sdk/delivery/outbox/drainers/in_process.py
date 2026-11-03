"""In-process outbox exporter: a thread draining beside the training loop where forking is hostile
(Ray actors) or delivery must ride this client's transport. Holds the worker lease (DESIGN.md)."""

from __future__ import annotations

import threading
import weakref

from .....foundation.os_backend import os_backend as oscompat
from .....foundation.durable import durable
from ...transport.deadlines import without_patience
from ..drain.lanes import LaneBackoff
from ..drain.drain import drain
from ..drain.window import CollectWindow
from ..drainer import Drainer, DrainerKind
from ..outbox import _BACKOFF_CAP_SECONDS, _queued_names
from ..lease import _drop_caps, _lease_path, _write_caps

#: Same floor as the Miles exporter honored for PROBE_EXPORT_INTERVAL_SEC.
MIN_INTERVAL_SECONDS = 0.05


class OutboxExporter:
    def __init__(self, client, interval: float):
        self.client = client
        self.journal = client.journal
        self.interval = max(float(interval), MIN_INTERVAL_SECONDS)
        self._stop = threading.Event()
        self._wake = threading.Event()
        self._lease_handle = None
        self._thread = threading.Thread(
            target=self._loop,
            name=f"probe-outbox-export-{self.journal.dir.name}",
            daemon=True,
        )
        self._thread.start()

    @property
    def alive(self) -> bool:
        return self._thread.is_alive()

    def wake(self) -> None:
        self._wake.set()

    # -- loop ----------------------------------------------------------------
    def _try_lease(self) -> bool:
        """Take (or confirm) the worker lease, non-blocking. False while a detached worker
        owns the journal: delivery is already happening."""
        if self._lease_handle is not None:
            return True
        self.journal._ensure()
        handle = open(_lease_path(self.journal), "a+")
        try:
            oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        except (BlockingIOError, OSError):
            handle.close()
            return False
        self._lease_handle = handle
        # Say what this sender delivers, as a detached worker does: without a caps file a
        # producer reads the lease holder as a pre-1.11 release and asks it (in vain: only a
        # detached worker reads the request) to step aside for every new kind.
        # No features: the exporter publishes no progress record, so a waiter asks it in vain.
        _write_caps(self.journal, features=frozenset())
        return True

    def _loop(self) -> None:
        # Plan 2.7: the token the API refused, while this client waits for a new login of the
        # same account. A sign-in revokes the old token BEFORE writing the new one, so a pass
        # in that gap finds nothing new; dying there stranded every later write of the
        # process. Waiting costs a config read at most every 30 s, no network.
        awaiting: str | None = None
        # A pass stopping on a transient failure backs off through the ONE helper every
        # durable loop uses (plan 0.6), honouring Retry-After. It re-drained on every tick and
        # wake (a training loop wakes it per `log()`), hammering a sick server and, with
        # failures counted in attempts, dead-lettering a run's writes in ~7 s of outage.
        delays = durable.backoff_delays(None)
        # Per-run waits (plan 1.6): a run whose head op keeps failing is
        # skipped until its own backoff ends; the other runs keep draining.
        lanes = LaneBackoff(ceiling=_BACKOFF_CAP_SECONDS)
        # Each writer's collect window (plan T2); after a pass, the thread sleeps until the
        # soonest window or run backoff ends and a write wakes it only when it must go now.
        window = CollectWindow()
        pass_now = False
        try:
            while not self._stop.is_set():
                if not pass_now:
                    self._wake.wait(self.interval)
                    self._wake.clear()
                pass_now = False
                if self._stop.is_set():
                    # One LAST pass before exiting. The stop check returned here, so
                    # everything enqueued since the previous tick (up to an interval of a
                    # training loop's metrics) stayed on disk after a clean `close()`, with no
                    # detached worker to inherit it (a drain_interval client never kicks one).
                    self._final_drain()
                    return
                if awaiting is not None:
                    # Waiting WITHOUT the outbox lease: other processes' writes keep delivering
                    # through the detached worker meanwhile.
                    if not self.client.refresh_credentials(refused=awaiting):
                        continue  # no new login yet; never re-send a refused token
                    awaiting = None
                if not self._try_lease():
                    continue
                refused = getattr(self.client.settings, "token", None)
                before = _queued_names(self.journal)
                try:
                    report = drain(
                        self.journal,
                        client_factory=self.client._outbox_client_factory(),
                        skip_runs=lanes.skip(),
                        # Like the root's worker: other credentials' queues
                        # have their own (#2041 round 3).
                        credential_queues=False,
                        window=window,
                    )
                except Exception:  # noqa: BLE001 -- keep the loop alive; drain
                    continue  # itself records last_error in status.json
                if report.auth_blocked:
                    if not self.client._own_credential_refusal(report):
                        if not report.auth_stopped:
                            # Another credential's writes, set aside by the drain (#2041
                            # review); ours still flow. Carry on.
                            continue
                        # A scope refusal or another context's key: no re-login of ours fixes
                        # it. Stop, as before: never retry rejected credentials forever.
                        return
                    if self.client.refresh_credentials(refused=refused):
                        continue
                    if not self._can_wait_for_a_login():
                        return
                    awaiting = refused
                    self._release_lease()
                    continue
                lanes.record(report)
                if report.stopped_transient and not report.stalled_runs:
                    # The whole pass stopped (server unreachable): back off everything. Wakes
                    # do not cut this short; only close() does, and it still makes its final pass.
                    if self._stop.wait(
                        durable.honor_retry_after(
                            next(delays), report.retry_after, ceiling=_BACKOFF_CAP_SECONDS
                        )
                    ):
                        self._final_drain()
                        return
                    continue
                if report.delivered or report.dead_lettered or not lanes.skip():
                    delays = durable.backoff_delays(None)
                waits = [w for w in (report.send_in, lanes.next_wake()) if w is not None]
                if waits and (report.deferred or not (report.delivered or report.dead_lettered)):
                    # What is left waits for its window or its run's backoff (R4: a `log()`
                    # per wake re-drained a stalled run's queue on every write, burning CPU
                    # through a 503 outage). A write of a run NOT waiting still goes within
                    # `LOOK_SECONDS` (review of #2051: never behind another run's backoff).
                    window.wait(
                        self.journal,
                        seconds=max(min(waits), 0.05),
                        seen=before,
                        skip=lanes.skip(),
                        loads=report.deferred_loads,
                        stop=self._stop,
                        woken=self._wake,
                    )
                    if self._stop.is_set():
                        self._final_drain()
                        return
                    pass_now = True
        finally:
            self._release_lease()

    def _can_wait_for_a_login(self) -> bool:
        """Only a token from the stored login can be replaced by a new login, and only once
        its account is known. An environment token (a Kubernetes secret) or one passed in code
        never changes under a running process: stop, as before, rather than wait forever."""
        client = self.client
        if getattr(client, "_credential_source", None) != "config":
            return False
        ready = getattr(client, "_credential_identity_ready", None)
        if ready is not None:
            ready.wait(timeout=5.0)  # the lookup may still be in flight
        return getattr(client, "_credential_identity", None) is not None

    def _final_drain(self) -> None:
        """Best-effort delivery of whatever arrived since the last tick. Unbounded here on
        purpose: `close()` joins with a timeout, so a drain outliving it is abandoned and the
        ops stay durable on disk for the next process.
        """
        try:
            if not self._try_lease():
                return
            # `long_ops=False`: a multipart upload's slice (plan (g)) would hold the close up to
            # its budget; it stays queued for the next worker.
            drain(
                self.journal,
                client_factory=self.client._outbox_client_factory(),
                credential_queues=False,
                long_ops=False,
            )
        except Exception:  # noqa: BLE001 -- a close may never raise
            pass

    def _release_lease(self) -> None:
        if self._lease_handle is None:
            return
        _drop_caps(self.journal)
        try:
            oscompat.flock(self._lease_handle.fileno(), oscompat.LOCK_UN)
        except OSError:
            pass
        self._lease_handle.close()
        self._lease_handle = None

    def close(self, timeout: float = 5.0) -> None:
        self._stop.set()
        self._wake.set()
        self._thread.join(timeout=timeout)


class ThreadDrainer(Drainer):
    """The in-process kind (parity F2): the client's `OutboxExporter`, started at its first
    write and woken by every later one. A DEAD exporter is not respawned: the only thing
    that kills one is an auth block, and respawning per write would retry rejected
    credentials forever (the zombie-uploader pitfall). Re-login + `probe outbox retry`
    resumes. Holds the client weakly: a dropped client is freed at once."""

    kind = DrainerKind.THREAD

    def __init__(self, client) -> None:
        super().__init__(client.journal.dir, can_fork=client._default_transport)
        self._client = weakref.ref(client)

    def wake(self) -> None:
        client = self._client()
        if client is None:
            return
        exporter = client._exporter
        if exporter is None:
            with client._exporter_lock:
                exporter = client._exporter
                if exporter is None:
                    # Its thread outlives any patience scope a write here happens inside
                    # (init); see `_wrap_run`.
                    with without_patience():
                        exporter = OutboxExporter(client, client._drain_interval)
                        client._learn_identity()
                    client._exporter = exporter
        exporter.wake()

    def close(self, timeout: float | None = None) -> bool:
        """Join the exporter (its own stop path makes a final pass), within ``timeout`` capped
        at its own 5 s; one still running is abandoned with its ops on disk. A DEAD exporter
        stays in place: it died of an auth block, and clearing it would let the next write
        rebuild one against the same rejected credential (the zombie-uploader pitfall)."""
        client = self._client()
        exporter = client._exporter if client is not None else None
        if exporter is None:
            return False
        was_alive = getattr(exporter, "alive", True)
        if timeout is None:
            exporter.close()
        else:
            exporter.close(timeout=max(0.0, min(5.0, timeout)))
        if was_alive:
            client._exporter = None
        return True
