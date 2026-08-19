# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Remote (``db://``) job-future adapter for namespace-based backfill/refresh."""

from __future__ import annotations

import contextlib
import logging
import time
from typing import Any

from geneva.jobs.remote import RemoteJob  # noqa: TC001 — used at runtime
from geneva.table import JobFuture

_LOG = logging.getLogger(__name__)


class RemoteJobFuture(JobFuture):
    """Adapter bridging [`RemoteJob`][RemoteJob] to the
    [`JobFuture`][JobFuture] interface.

    Bridges the polling-based ``RemoteJob`` to the executor-agnostic
    ``done() / result() / status()`` surface used by ``Job``.
    """

    def __init__(self, remote_job: RemoteJob) -> None:
        super().__init__(job_id=remote_job.job_id)
        self._remote_job = remote_job
        # Log the id here, at dispatch, so it is surfaced when the job starts.
        # The sync backfill/load-columns drivers poll done()/status() and only
        # call result() once the job is already terminal, so a start log inside
        # result() would fire too late to reattach to a still-running job.
        _LOG.info("Started remote job %s", remote_job.job_id)
        # Lazily-created progress renderer, shared between status() live ticks
        # (driven by a sync backfill/refresh loop) and the blocking result()
        # poll, so the bars are never drawn twice.
        self._bars: Any = None

    def _progress_bars(self) -> Any:
        if self._bars is None:
            from geneva.jobs.remote import _RemoteProgressBars

            self._bars = _RemoteProgressBars()
        return self._bars

    @property
    def remote_job(self) -> RemoteJob:
        return self._remote_job

    def done(self, timeout: float | None = None) -> bool:
        if timeout is None or timeout <= 0:
            return self._remote_job.done()

        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self._remote_job.done():
                return True
            time.sleep(min(0.5, max(0.05, deadline - time.monotonic())))
        return self._remote_job.done()

    def result(self, timeout: float | None = None) -> Any:
        if timeout is not None and timeout <= 0:
            record = self._remote_job._read_job_record()
            if not self._remote_job.done():
                raise TimeoutError(
                    f"Job {self.job_id} not yet done (non-blocking probe)"
                )
            status_str = (
                record.status.value
                if hasattr(record.status, "value")
                else str(record.status)
            )
            if status_str != "DONE":
                events = record.events or []
                detail = events[-1] if events else "no details available"
                raise RuntimeError(f"Job {self.job_id} {status_str.lower()}: {detail}")
        else:
            # Reuse the renderer that status() has been ticking (if the caller
            # is a sync driver loop) so the final poll doesn't draw a second set
            # of bars; close it once the job resolves.
            bars = self._progress_bars()
            try:
                record = self._remote_job.result(timeout=timeout, bars=bars)
            except TimeoutError:
                raise
            except BaseException:
                bars.close()
                raise
            else:
                bars.close()
        payload: dict[str, Any] = {
            "job_id": record.job_id,
            "status": record.status.value
            if hasattr(record.status, "value")
            else str(record.status),
            "table_name": record.table_name,
            "launched_at": record.launched_at,
            "completed_at": record.completed_at,
            "manifest_id": record.manifest_id,
            "cluster_name": record.cluster_name,
        }
        if record.column_name:
            payload["column_name"] = record.column_name
        if record.input_columns:
            payload["input_columns"] = list(record.input_columns)
        if record.output_columns:
            payload["output_columns"] = list(record.output_columns)
        for m in record.metrics or []:
            if not hasattr(m, "name"):
                continue
            if m.name == "rows_checkpointed":
                payload["rows_processed"] = m.n
            elif m.name == "rows_skipped":
                payload["rows_skipped"] = m.n
            elif m.name == "rows_refreshed":
                payload["rows_refreshed"] = m.n
            elif m.name == "writer_fragments":
                payload["new_source_fragments"] = m.n
        return payload

    def status(self, timeout: float | None = None) -> None:
        """Render one live progress frame.

        Sync drivers (``Table.backfill`` and the load-columns loop) poll
        ``done()`` then call ``status()`` every tick; rendering here — rather
        than only in the terminal ``result()`` — is what makes db:// progress
        live instead of a single final frame. Best-effort: a render or read
        hiccup must never break the driver loop.
        """
        try:
            record = self._remote_job._read_job_record()
        except ValueError:
            with contextlib.suppress(Exception):
                self._progress_bars().render_pending(self.job_id)
            return None
        except Exception:
            return None
        with contextlib.suppress(Exception):
            self._progress_bars().tick(record)
        return None
