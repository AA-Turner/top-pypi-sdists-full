"""In-process outbox exporter: fork-free delivery beside the training loop.

Parity F2 (docs/2026-08-04-outbox-miles-parity.md): the detached worker is
the default delivery path; this thread serves environments where forking is
hostile (Ray actors) or where delivery must ride THIS client's transport
(custom transports, tests) -- the two things a detached process can never do.

Coordination: the thread holds the same ``.worker.lock`` lease the worker
does, for its whole life. One journal, one drainer: ``maybe_spawn`` sees the
live lease and never forks beside a running exporter, and an exporter that
starts while a detached worker is draining stays passive until the worker
exits, then takes over at the next wake.

Stops: ``close()``, and auth-block -- never retry rejected credentials
(worker exit-3 parity); ops stay queued, and re-login + ``probe outbox
retry`` resumes delivery. A paused journal only idles the loop (``drain``
returns untouched) without killing the thread.
"""

from __future__ import annotations

import threading

from .._shared import oscompat
from . import durable
from .journal import LaneBackoff, drain
from .outbox_worker import _BACKOFF_CAP_SECONDS, _drop_caps, _lease_path, _write_caps

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
        """Take (or confirm) the worker lease, non-blocking. False while a
        detached worker owns the journal -- delivery is already happening."""
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
        # Say what this sender delivers, as a detached worker does: without a
        # caps file a producer reads the lease holder as a release before 1.11
        # and asks it (in vain: only a detached worker reads the request) to
        # step aside for every new kind.
        _write_caps(self.journal)
        return True

    def _loop(self) -> None:
        # Plan 2.7: the token the API refused, while this client waits for a
        # new login of the same account. A sign-in revokes the old token
        # BEFORE it writes the new one, so a pass in that gap finds nothing new
        # yet; dying there (what this did) stranded every later write of the
        # process. Waiting costs a config read at most every 30 s, no network.
        awaiting: str | None = None
        # A pass that stops on a transient failure backs off through the ONE
        # helper every durable loop uses (plan 0.6), honouring the server's
        # Retry-After. It used to re-drain on every tick and every wake -- a
        # training loop wakes it per `log()` -- which hammered a sick server
        # and, while failures were counted in attempts, dead-lettered a run's
        # writes in ~7 s of outage.
        delays = durable.backoff_delays(None)
        # Per-run waits (plan 1.6): a run whose head op keeps failing is
        # skipped until its own backoff ends; the other runs keep draining.
        lanes = LaneBackoff(ceiling=_BACKOFF_CAP_SECONDS)
        try:
            while not self._stop.is_set():
                self._wake.wait(self.interval)
                self._wake.clear()
                if self._stop.is_set():
                    # One LAST pass before exiting. The stop check used to
                    # return here, so everything enqueued since the previous
                    # tick -- up to a whole interval of a training loop's
                    # metrics -- was left on disk by a clean `close()`, with no
                    # detached worker to inherit it because a drain_interval
                    # client never kicks one.
                    self._final_drain()
                    return
                if awaiting is not None:
                    # Waiting WITHOUT the outbox lease: other processes' writes
                    # keep delivering through the detached worker meanwhile.
                    if not self.client.refresh_credentials(refused=awaiting):
                        continue  # no new login yet; never re-send a refused token
                    awaiting = None
                if not self._try_lease():
                    continue
                refused = getattr(self.client.settings, "token", None)
                try:
                    report = drain(
                        self.journal,
                        client_factory=self.client._outbox_client_factory(),
                        skip_runs=lanes.skip(),
                        # Like the root's worker: other credentials' queues
                        # have their own (#2041 round 3).
                        credential_queues=False,
                    )
                except Exception:  # noqa: BLE001 -- keep the loop alive; drain
                    continue  # itself records last_error in status.json
                if report.auth_blocked:
                    if not self.client._own_credential_refusal(report):
                        if not report.auth_stopped:
                            # Another credential's writes, set aside by the
                            # drain (#2041 review); ours still flow. Carry on.
                            continue
                        # A scope refusal, or another context's key: nothing a
                        # re-login of ours can fix. Stop, as before: never retry
                        # rejected credentials forever.
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
                    # The whole pass stopped (the server is unreachable):
                    # back off everything. Wakes do not cut this short; only
                    # close() does, and it still makes its final pass.
                    if self._stop.wait(
                        durable.honor_retry_after(
                            next(delays), report.retry_after, ceiling=_BACKOFF_CAP_SECONDS
                        )
                    ):
                        self._final_drain()
                        return
                elif not (report.delivered or report.dead_lettered) and lanes.skip():
                    # Nothing moved and what is left waits on runs backing off.
                    # The next tick or `log()` wake runs a pass that skips them
                    # and delivers anything new of this client's own (review of
                    # #2051: waiting here on the stop event held a new write up
                    # to 300 s behind another run's backoff).
                    continue
                else:
                    delays = durable.backoff_delays(None)
        finally:
            self._release_lease()

    def _can_wait_for_a_login(self) -> bool:
        """Only a token from the stored login can be replaced by a new
        login, and only once the account it belongs to is known. An environment
        token (a Kubernetes secret) or one passed in code never changes under
        a running process: stop, as before, rather than wait forever."""
        client = self.client
        if getattr(client, "_credential_source", None) != "config":
            return False
        ready = getattr(client, "_credential_identity_ready", None)
        if ready is not None:
            ready.wait(timeout=5.0)  # the lookup may still be in flight
        return getattr(client, "_credential_identity", None) is not None

    def _final_drain(self) -> None:
        """Best-effort delivery of whatever arrived since the last tick.

        Bounded by nothing here on purpose -- `close()` already joins with a
        timeout, so a drain that outlives it is abandoned rather than hung on,
        and the ops stay durable on disk for the next process either way.
        """
        try:
            if not self._try_lease():
                return
            # `long_ops=False`: a multipart upload's slice (plan (g)) would
            # hold the close for up to its budget; it stays queued for the
            # next worker instead.
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
