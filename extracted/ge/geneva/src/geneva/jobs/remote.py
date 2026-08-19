# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Remote job handle for async Geneva jobs dispatched via phalanx."""

from __future__ import annotations

import logging
import time
from datetime import datetime
from typing import TYPE_CHECKING, Any

import attrs

from geneva.jobs.jobs import (
    JobRecord,
    JobStatus,
)

if TYPE_CHECKING:
    from geneva.db import Connection

_LOG = logging.getLogger(__name__)

# Metric names to display in remote progress bars. Sources:
#   Planning: _plan_read / _plan_copy emit plan_fragments (sub-step desc + n/M).
#   Backfill: run_ray_add_column / _run_column_adding_pipeline emit
#     workers, rows_checkpointed, rows_ready_for_commit, writer_fragments.
#   UDTF refresh: _refresh_udtf_matview emits partitions, rows_produced.
#   Chunker refresh: _append_expanded_fragments emits batches, rows_produced.
_VISIBLE_METRICS = frozenset(
    {
        "plan_fragments",
        "workers",
        "rows_checkpointed",
        "rows_ready_for_commit",
        "writer_fragments",
        "partitions",
        "rows_produced",
        "batches",
    }
)


class _RemoteProgressBars:
    """Stateful tqdm renderer for a remote job's progress.

    Renders a status line, an always-latest events line (surfacing the
    Cluster provisioning -> Job planning -> Executing ... phases), and one bar
    per visible metric. Call :meth:`tick` / :meth:`render_pending` repeatedly —
    from the blocking poll loop *or* from a sync driver's per-iteration
    ``status()`` calls — and :meth:`close` at the end. Holding the bars as
    instance state lets one renderer be shared across both drivers so progress
    is never drawn twice.
    """

    def __init__(self) -> None:
        self._pbars: dict = {}
        self._status_bar = None
        self._events_bar = None
        # Fixed line slots so the status/events lines never collide with the
        # metric bars: position 0 = status, 1 = events, 2+ = metrics in the
        # order they first appear. Without explicit positions tqdm's dynamic
        # stacking desyncs once bars are created at different ticks (and once
        # any raw write lands mid-stack), which is what causes the overlap.
        self._next_metric_pos = 2
        self._closed = False

    def _new_bar(
        self, position: int, *, bar_format: str | None = None, total: int = 0
    ) -> Any:
        from geneva.tqdm import tqdm

        kwargs: dict = {"total": total, "position": position, "leave": True}
        if bar_format is not None:
            kwargs["bar_format"] = bar_format
        return tqdm(**kwargs)

    def render_pending(self, job_id: str) -> None:
        """Render the placeholder line while the job record does not yet exist."""
        from geneva.tqdm import Colors, fmt

        if self._status_bar is None:
            self._status_bar = self._new_bar(0, bar_format="{desc} [{elapsed}]")
        self._status_bar.desc = fmt(
            f"Job {job_id[:8]}... PENDING", Colors.BRIGHT_YELLOW, bold=True
        )
        self._status_bar.refresh()

    def tick(self, record: JobRecord) -> None:
        """Render one live frame from the current job record.

        Deliberately does not log here: raw log lines written while multiple
        tqdm bars are live desync tqdm's cursor and make the status/events lines
        overlap the metric bars. The live status is already on the status line;
        durable status/phase transitions live in the job record's events.
        """
        from geneva.tqdm import Colors, fmt

        status = _status_str(record.status)
        table_col = (
            f"{record.table_name} - {record.column_name}"
            if record.column_name
            else record.table_name
        )

        if self._status_bar is None:
            self._status_bar = self._new_bar(0, bar_format="{desc} [{elapsed}]")
        self._status_bar.desc = fmt(
            f"[{table_col}] {status}",
            Colors.BRIGHT_GREEN if status == "RUNNING" else Colors.BRIGHT_YELLOW,
            bold=True,
        )
        self._status_bar.refresh()

        # Latest lifecycle event as its own always-updating line.
        events = record.events or []
        if events:
            if self._events_bar is None:
                self._events_bar = self._new_bar(1, bar_format="{desc}")
            self._events_bar.desc = fmt(
                f"[{table_col}] {events[-1]}", Colors.BRIGHT_MAGENTA, bold=True
            )
            self._events_bar.refresh()

        # Metric bars (only the allow-listed key metrics). Each keeps a fixed
        # line slot for its whole lifetime and is closed once, in close(), so
        # its position never shifts mid-run (a mid-run close() would renumber
        # the remaining bars and overlap the status/events lines).
        if record.metrics:
            for m in record.metrics:
                if not hasattr(m, "name") or m.name not in _VISIBLE_METRICS:
                    continue
                bar = self._pbars.get(m.name)
                if bar is None:
                    bar = self._new_bar(self._next_metric_pos, total=m.total or 0)
                    self._next_metric_pos += 1
                    self._pbars[m.name] = bar
                # Refresh desc every tick so a metric whose sub-step label
                # changes (e.g. plan_fragments: scanning -> building) advances.
                bar.desc = fmt(f"[{table_col}] {m.desc}", Colors.CYAN, bold=True)
                bar.total = m.total
                bar.n = m.n
                bar.refresh()

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        if self._status_bar is not None:
            self._status_bar.close()
        if self._events_bar is not None:
            self._events_bar.close()
        for bar in self._pbars.values():
            bar.close()


class _ServerJobError(RuntimeError):
    """The remote job reached a terminal FAILED/CANCELLED state server-side.

    Distinguished from client-side polling failures (lost connection, timeout,
    interrupt) so ``RemoteJob.result`` prints resume instructions only for the
    latter -- a server-failed job has nothing left to resume. Subclasses
    ``RuntimeError`` so existing ``except RuntimeError`` callers are unaffected.
    """


@attrs.define
class RemoteJob:
    """Handle for an asynchronous remote job dispatched via phalanx.

    Implements the same interface as ``NativeJob`` so callers don't need
    to know which mode they're in.  Reads job status from the
    ``_geneva_jobs`` system table through the phalanx connection.
    """

    job_id: str
    table_name: str
    _conn: Connection = attrs.field(repr=False, alias="conn")
    column_name: str | None = None
    job_type: str = "backfill"
    launched_at: datetime = attrs.Factory(lambda: datetime.now(tz=None))

    @classmethod
    def from_job(cls, conn: Connection, job_id: str) -> RemoteJob:
        """Reattach to an already-dispatched job by its ID.

        Job state is durable in the ``_geneva_jobs`` system table, so a handle
        rebuilt here resumes polling exactly where a previous client left off --
        useful after the original process exited or the client failed::

            job = RemoteJob.from_job(conn, job_id)
            job.result()

        Parameters
        ----------
        conn
            Connection to read job state from (e.g. from ``geneva.connect(...)``).
        job_id
            ID of a previously launched job.

        Raises
        ------
        ValueError
            If no job with ``job_id`` exists on the connection.
        """
        record = conn.get_job(job_id)  # raises ValueError if the id is unknown
        return cls(
            job_id=job_id,
            table_name=record.table_name,
            column_name=record.column_name,
            job_type=record.job_type,
            conn=conn,
        )

    @property
    def status(self) -> str:
        """Current job status: PENDING, RUNNING, DONE, FAILED."""
        record = self._read_job_record()
        return _status_str(record.status)

    @property
    def metrics(self) -> list:
        """Current progress metrics."""
        record = self._read_job_record()
        return record.metrics or []

    # Statuses that indicate a job has reached a terminal state
    _TERMINAL_STATUSES = frozenset(
        {
            JobStatus.DONE.value,
            JobStatus.FAILED.value,
            JobStatus.CANCELLED.value,
        }
    )

    def done(self) -> bool:
        """True if job has reached a terminal state (DONE, FAILED, or CANCELLED)."""
        return self.status in self._TERMINAL_STATUSES

    def result(
        self,
        timeout: float | None = None,
        *,
        bars: _RemoteProgressBars | None = None,
    ) -> JobRecord:
        """Block until the job completes and return the final record.

        Parameters
        ----------
        timeout
            Maximum seconds to wait.  ``None`` means wait indefinitely.
        bars
            Optional shared renderer (see :meth:`_poll_until_done`) so a sync
            driver that already rendered live via ``status()`` ticks doesn't
            draw a second set of bars here.

        Raises
        ------
        RuntimeError
            If the job fails or is cancelled.
        TimeoutError
            If *timeout* is exceeded.
        """
        _LOG.info("Polling remote job: %s", self.job_id)
        try:
            return self._poll_until_done(timeout=timeout, bars=bars)
        except _ServerJobError:
            # The job failed/was cancelled server-side; nothing to resume.
            raise
        except BaseException:
            # Client-side failure (lost connection, timeout, Ctrl-C): the server
            # job may still be running, so surface how to reattach and resume
            # polling. BaseException so KeyboardInterrupt is covered too.
            _LOG.warning(
                "Client stopped polling job %s; the job may still be running "
                "server-side. To resume, reconnect and run:\n"
                '    RemoteJob.from_job(conn, "%s").result()',
                self.job_id,
                self.job_id,
            )
            raise

    def _poll_until_done(
        self,
        *,
        timeout: float | None = None,
        refresh_secs: float = 2.0,
        bars: _RemoteProgressBars | None = None,
    ) -> JobRecord:
        """Poll ``_geneva_jobs`` until terminal state, rendering tqdm bars.

        ``bars`` lets a caller share one renderer across drivers — e.g. a sync
        ``Table.backfill`` loop that already rendered live via ``status()``
        ticks and then blocks here — so progress is never drawn twice; the
        caller then owns closing it. When omitted, a private renderer is
        created and closed here.
        """
        own_bars = bars is None
        bars = bars if bars is not None else _RemoteProgressBars()
        start = time.monotonic()
        try:
            while True:
                if timeout is not None and (time.monotonic() - start) >= timeout:
                    raise TimeoutError(
                        f"Job {self.job_id} did not complete within {timeout}s"
                    )

                try:
                    record = self._read_job_record()
                except ValueError:
                    # Job record not yet created — wait for geneva_driver.
                    bars.render_pending(self.job_id)
                    time.sleep(refresh_secs)
                    continue

                bars.tick(record)

                status = _status_str(record.status)
                if status in self._TERMINAL_STATUSES:
                    if status == JobStatus.DONE.value:
                        _LOG.info("Job %s completed", self.job_id)
                        return record
                    events = record.events or []
                    detail = events[-1] if events else "no details available"
                    raise _ServerJobError(
                        f"Job {self.job_id} {status.lower()}: {detail}"
                    )

                time.sleep(refresh_secs)
        finally:
            if own_bars:
                bars.close()

    def _read_job_record(self) -> JobRecord:
        """Read job record from ``_geneva_jobs`` system table.

        Delegates to ``Connection.get_job()`` which uses
        ``JobStateManager`` — works for both native and remote connections.
        """
        return self._conn.get_job(self.job_id)


def _status_str(status: JobStatus | str) -> str:
    """Normalize status to string."""
    return status.value if isinstance(status, JobStatus) else str(status)
