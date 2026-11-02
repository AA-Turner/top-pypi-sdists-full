"""Renew finite worker ownership independently of authored computation and child waits."""

import os
import signal
import sys
import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from threading import Event, Thread
from typing import ClassVar

from labqoat.worker.scoped_api import ScopedApi
from labqoat.worker.worker_api_error import WorkerApiError


@dataclass
class WorkerLease:
    """Keep live work leased and stop the process when assignment authority is lost."""

    api: ScopedApi
    interval_seconds: ClassVar[float] = 60.0
    recovery_seconds: ClassVar[float] = 600.0
    _stopped: Event = field(default_factory=Event, init=False)

    @contextmanager
    def maintained(self, *, confirmed: bool = False) -> Iterator[None]:
        """Confirm ownership before executing code; stop and join renewal on every exit."""
        thread = None
        try:
            if not confirmed:
                self._renew()
            thread = Thread(target=self._run, name="labqoat-worker-lease", daemon=True)
            thread.start()
            yield
        finally:
            self.stop()
            if thread is not None:
                thread.join()
            self.api.close()

    def stop(self) -> None:
        """Stop renewing before terminal acknowledgement can revoke this input inside a reusable worker."""
        self._stopped.set()

    def _renew(self) -> None:
        """Require an acknowledgement from the existing fenced heartbeat endpoint."""
        try:
            response = self.api.json("POST", "/api/v1/worker/assignments/heartbeat", {})
        except (ValueError, TypeError) as error:
            raise WorkerApiError("Worker lease acknowledgement is invalid", 502) from error
        if response != {"status": "ok"}:
            raise WorkerApiError("Worker lease acknowledgement is invalid", 502)

    def _run(self) -> None:
        """Retry transient failures within a margin shorter than the server's 15-minute lease."""
        renewed_at = time.monotonic()
        while not self._stopped.wait(self.interval_seconds):
            try:
                self._renew()
                renewed_at = time.monotonic()
            except WorkerApiError as error:
                if self._stopped.is_set():
                    return
                if not self._recoverable(error, renewed_at):
                    print("Worker lease lost; terminating execution", file=sys.stderr, flush=True)
                    os.kill(os.getpid(), signal.SIGTERM)
                    return
                print("Worker lease renewal interrupted; retrying", file=sys.stderr, flush=True)

    def _recoverable(self, error: WorkerApiError, renewed_at: float) -> bool:
        """Stale credentials and permanent HTTP failures cannot retain a running worker."""
        transient = error.status is None or error.status >= 500 or error.status in {408, 429}
        return transient and time.monotonic() - renewed_at < self.recovery_seconds
