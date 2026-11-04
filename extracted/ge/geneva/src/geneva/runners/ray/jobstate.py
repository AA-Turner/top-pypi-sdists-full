# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Submitter-side state for one Ray driver attempt, independent of its tracker."""

from __future__ import annotations

import base64
import logging
import threading
import time
from concurrent.futures import Future, wait
from typing import TYPE_CHECKING

import ray.exceptions

from geneva.jobs.compaction_pause import open_latest_dataset, resume_after_driver_loss

if TYPE_CHECKING:
    from geneva.jobs.jobs import JobRecord, JobStateManager
    from geneva.table import TableReference

_LOG = logging.getLogger(__name__)
JOB_STATE_TIMEOUT_S = 5.0


class RayJobState:
    def __init__(
        self,
        history: JobStateManager,
        job_id: str,
        table_ref: TableReference | None = None,
    ) -> None:
        self.history = history
        self.job_id = job_id
        self.table_ref = table_ref
        self.object_ref: bytes | None = None
        self._lock = threading.Lock()
        self._failure_started = False
        self._failure_done = threading.Event()
        self._failure_wait_warned = False
        self._saved_lookup: Future[JobRecord | None] | None = None
        self._saved_at = 0.0
        self._saved_warned = False

    def record_failure(self, error: BaseException | None) -> None:
        if (
            self.object_ref is None
            or not isinstance(error, ray.exceptions.RayError)
            or isinstance(error, ray.exceptions.RayTaskError)
        ):
            # Application exceptions already use the driver's finalization.
            return
        with self._lock:
            if self._failure_started:
                return
            self._failure_started = True

        def persist() -> None:
            try:
                self.history.set_failed(
                    self.job_id,
                    f"{type(error).__name__}: {error}",
                    object_ref=self.object_ref,
                )
            except Exception:
                _LOG.exception("Failed to record driver loss for job %s", self.job_id)
                return
            finally:
                self._failure_done.set()
            self._resume_compaction()

        # Ray callbacks run on an RPC thread. Keep writes off it, without
        # making a dead database hold interpreter shutdown open.
        threading.Thread(
            target=persist, name=f"driver-failure-{self.job_id}", daemon=True
        ).start()

    def _resume_compaction(self) -> None:
        """A lost driver never resumes the compaction it paused (GEN-994)."""
        table_ref = self.table_ref
        if table_ref is None:
            return
        resume_after_driver_loss(
            table_name=table_ref.table_name,
            open_dataset=lambda: open_latest_dataset(table_ref, use_worker_props=False),
            history=self.history,
        )

    def finish_failure(
        self,
        error: BaseException,
        timeout: float = JOB_STATE_TIMEOUT_S,
    ) -> None:
        # ray.get may expose the failure before its completion callback runs.
        # Starting here too is idempotent and closes that race for normal waits.
        self.record_failure(error)
        if (
            self._failure_started
            and not self._failure_done.wait(timeout)
            and not self._failure_wait_warned
        ):
            _LOG.warning("Driver failure write still pending for job %s", self.job_id)
            self._failure_wait_warned = True

    def saved_record(
        self, timeout: float = JOB_STATE_TIMEOUT_S, *, refresh: bool = False
    ) -> JobRecord | None:
        """Read matching saved state with a bounded, single-flight wait.

        Reopen through TableReference so enterprise system namespaces and
        refreshed credentials follow the same path as ordinary job history.
        Slow synchronous namespace/storage calls remain on one daemon thread;
        repeated progress polls cannot accumulate blocked lookups.
        Displays can use the previous read during refresh; finalization uses
        ``refresh=True`` to wait for a fresh record instead.
        """
        if self.table_ref is None or self.object_ref is None:
            return None
        deadline = time.monotonic() + timeout
        if refresh:
            with self._lock:
                previous = self._saved_lookup
            if previous is not None and not previous.done():
                # A progress read may have captured RUNNING before the driver
                # finalized. Drain it without trusting its result, then start
                # (or join) a read requested after this refresh. Both waits
                # share one budget and still allow only one lookup in flight.
                done, _ = wait(
                    [previous], timeout=max(0.0, deadline - time.monotonic())
                )
                if not done or time.monotonic() >= deadline:
                    return None
        expected = base64.b64encode(self.object_ref).decode("utf-8")
        with self._lock:
            # Display polls may use the last completed read while refreshing.
            # Otherwise a lookup slower than the display timeout could finish
            # between ticks and be discarded before its metrics are shown.
            cached = (
                self._saved_lookup
                if not refresh
                and self._saved_lookup is not None
                and self._saved_lookup.done()
                else None
            )
            if self._saved_lookup is None or (
                self._saved_lookup.done()
                and (refresh or time.monotonic() - self._saved_at >= 1.0)
            ):
                lookup: Future[JobRecord | None] = Future()
                self._saved_lookup = lookup
                self._saved_at = time.monotonic()

                def read() -> None:
                    try:
                        assert self.table_ref is not None
                        rows = self.table_ref.open_db()._history.get(self.job_id)
                        job = rows[0] if rows else None
                        lookup.set_result(
                            job if job and job.object_ref == expected else None
                        )
                    except Exception as exc:
                        lookup.set_exception(exc)

                threading.Thread(
                    target=read, name=f"saved-job-{self.job_id}", daemon=True
                ).start()
            pending = self._saved_lookup
        try:
            return (cached or pending).result(
                timeout=max(0.0, deadline - time.monotonic())
            )
        except TimeoutError:
            return None
        except Exception:
            if not self._saved_warned:
                _LOG.warning(
                    "Cannot read saved state for job %s", self.job_id, exc_info=True
                )
                self._saved_warned = True
            return None
