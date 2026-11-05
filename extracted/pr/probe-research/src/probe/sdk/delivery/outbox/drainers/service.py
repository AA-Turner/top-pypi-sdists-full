"""ServiceDrainer (Drainer): the Probe service drains this client's queue (plan D8, task 19). A write
wakes one thread that asks the service (`maybe_spawn`), starting it where none runs; the training loop
never waits on the socket, and with no service the journal waits on disk for the next ask."""

from __future__ import annotations

import atexit
import os
import threading
import time

from probe.sdk.delivery.outbox.drainer import Drainer, DrainerKind, _with_credential
from probe.sdk.delivery.outbox.lease import _lease_is_free

#: After an ask no service took, the next waits this long, doubling to the cap.
RETRY_START_S = 1.0
RETRY_CAP_S = 60.0
#: What an exiting process gives a wake not yet asked (its last writes' ask), at most.
EXIT_ASK_S = 5.0


class ServiceDrainer(Drainer):
    """Each write probes the drain lease with ONE non-blocking flock; only when nobody holds it
    is the asker woken. While the lease is held, the side queues that drain may not serve are
    kicked at most every `SIDE_KICK_SECONDS`. A forced kick (a finish, a hand-off) asks at once,
    on the caller's thread."""

    kind = DrainerKind.WORKER

    def __init__(self, directory, *, credential_env: dict | None = None) -> None:
        super().__init__(directory, can_fork=True, credential_env=credential_env)
        self._lease = os.path.join(self.directory, ".worker.lock")
        self._waiting = os.path.join(self.directory, "waiting")
        self._wake = threading.Event()
        self._stop = threading.Event()
        self._asker: threading.Thread | None = None
        self._asker_pid = 0
        self._lock = threading.Lock()
        self.side_kicked_at = float("-inf")
        #: A write woke the asker and it has not asked since (a close's wake is not one).
        self._is_pending = False
        self.asked = 0
        self._is_exit_armed = False

    def wake(self) -> None:
        """After an enqueue (per `log()`): O(1) on the caller's thread."""
        try:
            if self._drain_delivers():
                if time.monotonic() - self.side_kicked_at >= _get_side_kick_s():
                    self.side_kicked_at = time.monotonic()
                    self._ask_soon()
                return
            self._ask_soon()
        except Exception:  # noqa: BLE001 -- best-effort; the finish is the barrier
            pass

    def kick(self, *, force: bool = False) -> None:
        if force:
            super().kick(force=True)
        else:
            self.wake()

    def close(self, timeout: float | None = None) -> bool:
        """Stop the asker, after one last ask for a write not yet asked for."""
        self._stop.set()
        self._wake.set()
        asker = self._asker
        if asker is not None and asker.is_alive():
            asker.join(EXIT_ASK_S if timeout is None else max(0.0, timeout))
        return False

    # -- the asker -------------------------------------------------------------

    def _ask_soon(self) -> None:
        self._start_asker()
        self._is_pending = True
        self._wake.set()

    def _start_asker(self) -> None:
        with self._lock:
            if self._asker is not None and self._asker.is_alive() and self._asker_pid == os.getpid():
                return
            self._asker_pid = os.getpid()
            self._asker = threading.Thread(target=self._ask_loop, name="probe-outbox-ask", daemon=True)
            self._asker.start()
            if not self._is_exit_armed:
                self._is_exit_armed = True
                atexit.register(self._ask_at_exit)

    def _ask_loop(self) -> None:
        from probe.foundation.service_api import handoff

        handoff.hold_open()
        pause = RETRY_START_S
        while True:
            self._wake.wait()
            self._wake.clear()
            if not self._is_pending:
                if self._stop.is_set():
                    return
                continue
            self._is_pending = False
            if self._ask():
                pause = RETRY_START_S
            elif not self._drain_delivers():
                # Nobody took it and nobody drains: ask again later (the journal keeps it).
                if self._stop.wait(pause):
                    return
                pause = min(pause * 2, RETRY_CAP_S)
                self._is_pending = True
                self._wake.set()
            if self._stop.is_set() and not self._is_pending:
                return

    def _ask(self) -> bool:
        """One ask; True when a drain runs or there was nothing to drain."""
        from . import detached

        self.asked += 1
        try:
            detached.maybe_spawn(self.directory, **_with_credential(self.credential_env))
        except Exception:  # noqa: BLE001 -- the journal waits on disk
            return False
        return self._drain_delivers() or not self._has_work()

    def _ask_at_exit(self) -> None:
        """A write the asker has not asked for yet (this process's last ones): asked now, bounded."""
        if self._is_pending and self._asker is not None and self._asker.is_alive():
            self._stop.set()
            self._wake.set()
            self._asker.join(EXIT_ASK_S)

    # -- what is on disk -------------------------------------------------------

    def _drain_delivers(self) -> bool:
        """A drain holds the lease and no upload waits for a promoter (an older drain may not
        promote, `maybe_spawn`): one flock, plus one listing only while the lease is held."""
        if _lease_is_free(None, self._lease):
            return False
        try:
            return not any(name.endswith(".json") for name in os.listdir(self._waiting))
        except OSError:
            return True

    def _has_work(self) -> bool:
        from ...journal.journal import Journal
        from ...status_fields import StatusField

        status = Journal.read_status(self.directory, include_receipts=False) or {}
        return bool(int(status.get(StatusField.PENDING) or 0) or int(status.get(StatusField.WAITING) or 0))


def _get_side_kick_s() -> float:
    from .detached import SIDE_KICK_SECONDS

    return SIDE_KICK_SECONDS
