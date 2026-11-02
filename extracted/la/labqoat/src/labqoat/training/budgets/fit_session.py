"""Maintain short fit grants while an independent process owns physical expiry."""

import time
from collections.abc import Iterator
from contextlib import contextmanager
from threading import Event, Lock, Thread
from uuid import uuid4

from labqoat.training.budgets.fit_budget_client import FitBudgetClient
from labqoat.training.budgets.fit_grant import FitGrant
from labqoat.training.budgets.fit_interval import FitInterval
from labqoat.training.budgets.fit_supervisor import FitSupervisor
from labqoat.worker.worker_api_error import WorkerApiError


class FitSession:
    """Keep at most a current and future interval; transport failure can never disarm physical expiry."""

    def __init__(self, client: FitBudgetClient, supervisor: FitSupervisor) -> None:
        """Construct inert state; only maintained entry acquires authority."""
        self.client, self.supervisor = client, supervisor
        self._stopped, self._lock = Event(), Lock()
        self._intervals: list[FitInterval] = []
        self._failure: Exception | None = None
        self._first: FitGrant | None = None
        self._started = 0.0
        self._ended: float | None = None
        self._exhausted = False

    @contextmanager
    def maintained(self) -> Iterator["FitSession"]:
        """Acknowledge independent supervision before fit; disarm only after the fit body returns."""
        if self._first is not None or self._stopped.is_set():
            raise RuntimeError("Fit sessions cannot be reused")
        thread = None
        try:
            self._begin()
            thread = Thread(target=self._run, name="labqoat-fit-grants", daemon=True)
            thread.start()
            yield self
            self.check()
        finally:
            self._end(thread)

    def _begin(self) -> None:
        """The session's first grant establishes a common elapsed-time anchor for every successor."""
        self._first = self.client.grant(str(uuid4()))
        self.supervisor.arm(self._first)
        self._started = time.monotonic()
        self._intervals.append(FitInterval(self._first, self._started))

    def check(self) -> None:
        """Let framework update boundaries stop gracefully after a failed grant or usage exchange."""
        if self._failure is not None:
            raise self._failure
        if self.remaining_seconds <= 0:
            raise RuntimeError("Fit execution authority has expired")

    @property
    def remaining_seconds(self) -> float:
        """Expose currently enforced authority, never the original allowance or unconfirmed future time."""
        with self._lock:
            if not self._intervals or self._stopped.is_set():
                return 0.0
            return max(0.0, self._intervals[-1].grant.deadline - time.monotonic())

    def _run(self) -> None:
        """Renewal I/O runs independently; the helper still kills fit if this thread blocks or dies."""
        try:
            while not self._stopped.wait(5.0):
                self._tick()
        except Exception as error:
            self._failure = error

    def _tick(self) -> None:
        """Report live intervals, retire expired reservations and reserve only one future interval."""
        now = time.monotonic() if self._ended is None else self._ended
        self._intervals = [item for item in self._intervals if item.grant.deadline > now]
        for item in self._intervals:
            if now >= item.started_at:
                self._report(item, now, stopped=False)
        if not self._intervals:
            raise RuntimeError("Fit authority expired before renewal")
        if now >= self._intervals[-1].grant.not_before and not self._stopped.is_set() and not self._exhausted:
            self._renew()

    def _renew(self) -> None:
        """Exhaustion stops future reservations while preserving already granted fit time."""
        try:
            self._accept(self.client.grant(str(uuid4())))
        except WorkerApiError as error:
            if error.code != "fit_budget_exhausted":
                raise
            self._exhausted = True

    def _accept(self, grant: FitGrant) -> None:
        """Serialize grant arrival with stopping so delayed renewal cannot restart a completed fit."""
        first = self._first
        if first is None:
            raise RuntimeError("Fit session has no initial authority")
        start = self._started + (grant.starts_at - first.starts_at).total_seconds()
        with self._lock:
            self._intervals.append(FitInterval(grant, start))
            if not self._stopped.is_set():
                self.supervisor.arm(grant)

    def _report(self, item: FitInterval, now: float, *, stopped: bool) -> None:
        """An already expired reservation remains conservatively charged if its receipt is closed."""
        report = item.report(now, stopped=stopped)
        try:
            self.client.report(item.grant, report)
        except WorkerApiError as error:
            if error.code != "fit_grant_closed" or time.monotonic() < item.grant.deadline:
                raise

    def _stop(self) -> None:
        """Stop actual fit before disarming; a renewal in flight sees the captured terminal boundary."""
        with self._lock:
            self._ended = time.monotonic()
            self._stopped.set()
            self.supervisor.stopped()

    def _finish_reports(self) -> None:
        """Report after joining renewal so future reservations acquired during stopping are released too."""
        ended = self._ended
        if ended is not None:
            for item in self._intervals:
                self._report(item, ended, stopped=True)

    def _end(self, thread: Thread | None) -> None:
        """Reap renewal even if the helper's shutdown channel has already failed."""
        try:
            self._stop()
        finally:
            if thread is not None:
                thread.join()
            self._finish_reports()
