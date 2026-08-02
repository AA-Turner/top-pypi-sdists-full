# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Public job result and handle types returned by ``Table.backfill``,
``Table.refresh``, and their ``_async`` counterparts.

These wrap the lower-level ``JobFuture`` (defined in ``geneva.table``) and
expose a stable user-facing surface across native and remote connections.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

import attrs

if TYPE_CHECKING:
    from datetime import datetime

    from geneva.table import JobFuture


# Status strings surfaced through Job / JobResult. The set of allowed
# values is open-ended for forward compatibility; today's executors emit
# the canonical PENDING / RUNNING / DONE / FAILED / CANCELLED set.
PENDING = "PENDING"
RUNNING = "RUNNING"
DONE = "DONE"
FAILED = "FAILED"
CANCELLED = "CANCELLED"


@attrs.define(kw_only=True)
class JobResult:
    """Completed-job metadata. Base type for operation-specific results.

    ``*_source`` fields record the origin of the resolved value:
    ``"explicit"`` (caller-supplied), ``"@udf"`` (snapshot from
    ``@udf(manifest=...)``), ``"deployment-default"`` (phalanx ConfigMap),
    ``"context"`` (legacy ``conn.context(...)``), or ``None`` if unset.
    """

    job_id: str
    status: str
    table_name: str
    launched_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    cluster_name: Optional[str] = None
    cluster_source: Optional[str] = None
    manifest_id: Optional[str] = None
    manifest_source: Optional[str] = None


@attrs.define
class UdfResult:
    udf_name: Optional[str] = None
    udf_version: Optional[str] = None
    rows_processed: int = 0
    rows_skipped: int = 0
    input_columns: Optional[list[str]] = None


@attrs.define(kw_only=True)
class BackfillJobResult(JobResult):
    """Result of a ``Table.backfill`` invocation. Per-column UDF
    identity and counters live in
    [`columns`][geneva.jobs.types.BackfillJobResult.columns], keyed by column
    name. Single-column backfills produce a one-entry map."""

    columns: dict[str, UdfResult] = attrs.field(factory=dict)


@attrs.define(kw_only=True)
class RefreshJobResult(JobResult):
    """Result of a ``Table.refresh`` invocation."""

    new_source_fragments: int = 0
    rows_refreshed: int = 0


class Job:
    """In-progress job handle returned by ``backfill_async`` /
    ``refresh_async``. Wraps a [`JobFuture`][geneva.table.JobFuture] and
    builds a typed [`JobResult`][geneva.jobs.types.JobResult] on completion.
    Reach the wrapped future via [`future`][geneva.jobs.types.Job.future] for
    executor-specific state."""

    def __init__(
        self,
        future: JobFuture,
        *,
        table_name: str,
        column_names: Optional[list[str]] = None,
        result_cls: type = BackfillJobResult,
        extra: Optional[dict] = None,
    ) -> None:
        self._future = future
        self._table_name = table_name
        self._column_names = list(column_names) if column_names else []
        self._result_cls = result_cls
        self._extra = dict(extra) if extra else {}

    @property
    def future(self) -> JobFuture:
        """The underlying executor-specific future."""
        return self._future

    @property
    def table_name(self) -> str:
        return self._table_name

    @property
    def column_names(self) -> list[str]:
        return list(self._column_names)

    @property
    def job_id(self) -> str:
        return self._future.job_id

    def done(self, timeout: float | None = None) -> bool:
        return self._future.done(timeout=timeout)

    @property
    def status(self) -> str:
        # The lower-level future.status() is a side-effecting log
        # printer in current code. Derive a typed status from done() +
        # whether result() raises.
        if not self._future.done():
            return RUNNING
        try:
            self._future.result(timeout=0)
            return DONE
        except Exception:
            return FAILED

    def result(self, timeout: float | None = None) -> JobResult:
        """Block until completion and return the typed result.

        Raises
        ------
            RuntimeError
                if the job failed or was cancelled.
            TimeoutError
                if ``timeout`` elapsed before completion.
        """
        try:
            payload: Any = self._future.result(timeout=timeout)
        except TimeoutError:
            raise
        except Exception as e:
            raise RuntimeError(f"job {self.job_id} failed: {e}") from e

        return self._build_result(payload)

    def _build_result(self, payload: Any) -> JobResult:
        # If the inner future already produced a typed result, prefer
        # it but rewrite job_id so callers' obvious correlation invariant
        # ``job.job_id == job.result().job_id`` holds (the inner future
        # may have generated its own uuid — e.g. RefreshJobResult does).
        if isinstance(payload, JobResult):
            if payload.job_id != self.job_id:
                return attrs.evolve(payload, job_id=self.job_id)
            return payload

        kwargs: dict[str, Any] = {
            "job_id": self.job_id,
            "status": DONE,
            "table_name": self._table_name,
        }
        if isinstance(payload, dict):
            allowed = {f.name for f in attrs.fields(self._result_cls)}
            kwargs.update({k: v for k, v in payload.items() if k in allowed})

        result_columns = self._column_names
        if (
            self._result_cls is BackfillJobResult
            and not result_columns
            and isinstance(payload, dict)
            and payload.get("output_columns")
        ):
            result_columns = list(payload["output_columns"])

        if self._result_cls is BackfillJobResult and result_columns:
            udf = (
                UdfResult(
                    udf_name=payload.get("udf_name"),
                    udf_version=payload.get("udf_version"),
                    input_columns=payload.get("input_columns"),
                    rows_processed=int(payload.get("rows_processed") or 0),
                    rows_skipped=int(payload.get("rows_skipped") or 0),
                )
                if isinstance(payload, dict)
                else UdfResult()
            )
            kwargs["columns"] = dict.fromkeys(result_columns, udf)
        kwargs.update(self._extra)
        return self._result_cls(**kwargs)
