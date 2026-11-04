"""Telemetry — what the platform observed of the pipelines a run executed."""

from __future__ import annotations

# Python internals
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterable,
    Awaitable,
    Iterable,
    Mapping,
    overload,
)

# Current package
from dlthub_sdk._glue.base import Collection, Entity, Namespace
from dlthub_sdk._glue.context import Async, M, Sync, _Ctx
from dlthub_sdk._glue.enums import EntityKind, StrEnum
from dlthub_sdk.domain import _narrow

if TYPE_CHECKING:
    # Typing only: domain never imports _gen at runtime.
    # Current package
    from dlthub_sdk._gen.telemetry.models import (
        DatasetStatsResponse,
        DetailedPipelineRunResponse,
        LoadPackageResponse,
        PipelineRunResponse,
        PipelineRunTableResponse,
        PipelineRunTraceResponse,
        PipelineStatsResponse,
        TelemetryWatermarkResponse,
    )

    #: list returns the row, get the detailed shape.
    PipelineRunPayload = PipelineRunResponse | DetailedPipelineRunResponse

#: The window a listing covers when the caller names none.
DEFAULT_WINDOW = timedelta(days=7)


def _refuse_unfilterable(status: PipelineRunStatus | None) -> None:
    """Refuse a status the platform ignores rather than let it match nothing.

    Args:
        status: What the caller asked to filter on.

    Raises:
        ValueError: The platform cannot filter on it.
    """
    if status is None or status in FILTERABLE_STATUSES:
        return
    filterable = ", ".join(sorted(s.value for s in FILTERABLE_STATUSES))
    raise ValueError(f"the platform filters on {filterable} only, not {status.value!r}")


def _wire_moment(moment: datetime) -> datetime:
    """Convert a timestamp to UTC and drop the zone, as these reads require.

    The endpoints refuse an offset outright. A naive value is refused rather
    than assumed to be UTC: ``datetime.now()`` is local, and reading it as UTC
    would shift the window by the caller's offset and still look plausible.

    Args:
        moment: The timestamp to send. Must carry a zone.

    Returns:
        The same instant, expressed as UTC, without a zone.

    Raises:
        ValueError: ``moment`` carries no zone, so it names no instant.
    """
    if moment.tzinfo is None:
        raise ValueError(
            f"pass an aware datetime, got the naive {moment!r} — a naive value "
            "names no instant. Use datetime.now(timezone.utc), or attach the "
            "zone it was meant in with .replace(tzinfo=...)"
        )
    return moment.astimezone(timezone.utc).replace(tzinfo=None)


def _window(
    since: datetime | None, until: datetime | None
) -> tuple[datetime, datetime]:
    """The window a read covers, defaulted and made ready for the wire.

    Args:
        since: Start of the window, or ``None`` for `DEFAULT_WINDOW` before the end.
        until: End of the window, or ``None`` for now.

    Returns:
        The start and end, both zoneless.
    """
    end = until or datetime.now(timezone.utc)
    start = since or end - DEFAULT_WINDOW
    return _wire_moment(start), _wire_moment(end)


@dataclass(frozen=True)
class TelemetryStatus:
    """How current the platform's telemetry is for one workspace."""

    updated_at: datetime | None
    """When a pipeline run in the workspace was last recorded or updated; `None` when
    there are none. If it is older than the time range you read, empty results may
    mean telemetry is behind rather than that nothing ran.
    """

    @staticmethod
    def _from_payload(
        _ctx: _Ctx[Any], payload: TelemetryWatermarkResponse
    ) -> TelemetryStatus:
        return TelemetryStatus(
            updated_at=(
                payload.updated_at if isinstance(payload.updated_at, datetime) else None
            )
        )


class Telemetry(Namespace[M]):
    """One workspace's telemetry, read from the data plane."""

    @overload
    def status(self: Telemetry[Sync]) -> TelemetryStatus: ...

    @overload
    def status(self: Telemetry[Async]) -> Awaitable[TelemetryStatus]: ...

    def status(self) -> TelemetryStatus | Awaitable[TelemetryStatus]:
        """Return when a pipeline run in this workspace was last recorded or updated.

        If that is older than the window you read, empty results may mean
        telemetry is behind rather than that nothing ran.

        Returns:
            The status; awaitable in async mode.

        Raises:
            DataplaneTokenRejected: The data plane rejected the token the
                platform issued for it.
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()
        return self._ctx.run(
            lambda t: t.get_workspace_watermark(
                workspace_id=workspace_id, dataplane_url=dataplane_url
            ),
            TelemetryStatus._from_payload,
        )

    @property
    def pipeline_runs(self) -> PipelineRuns[M]:
        """The dlt pipeline runs telemetry recorded here.

        Returns:
            This workspace's pipeline runs.
        """
        return PipelineRuns(self._ctx)

    @overload
    def pipelines(
        self: Telemetry[Sync],
        *,
        pipeline_name: str | None = None,
        latest_status: PipelineRunStatus | None = None,
        destination: str | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> Iterable[PipelineActivity]: ...

    @overload
    def pipelines(
        self: Telemetry[Async],
        *,
        pipeline_name: str | None = None,
        latest_status: PipelineRunStatus | None = None,
        destination: str | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> AsyncIterable[PipelineActivity]: ...

    def pipelines(
        self,
        *,
        pipeline_name: str | None = None,
        latest_status: PipelineRunStatus | None = None,
        destination: str | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> Iterable[PipelineActivity] | AsyncIterable[PipelineActivity]:
        """Yield one row per pipeline that ran in the window.

        The window holds the pipeline runs whose start falls in ``[since, until)``.

        Args:
            pipeline_name: Narrow to one pipeline.
            latest_status: Narrow to pipelines whose most recent run ended this
                way. Only ``SUCCEEDED`` and ``FAILED`` are filterable.
            destination: Narrow to pipelines most recently writing here.
            since: Start of the window, zone-aware. Defaults to seven days
                before ``until``.
            until: End of the window, zone-aware. Defaults to now.
            limit: Return at most this many. ``None`` walks to the end, or
                to row 10,100, past which the platform does not page.
            offset: Skip this many, server-side.

        Returns:
            An iterable of per-pipeline activity; async-iterable in async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            DataplaneTokenRejected: The data plane rejected the token the
                platform issued for it.
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            ScopeMissing: Reached without a workspace in scope.
            ValueError: A status the platform cannot filter on, a naive
                ``since`` or ``until``, or a negative ``limit`` or ``offset``.
        """
        _refuse_unfilterable(latest_status)
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()
        start, end = _window(since, until)

        def listing(t: Any, page: int, skip: int) -> Any:
            return t.list_pipeline_stats(
                workspace_id=workspace_id,
                dataplane_url=dataplane_url,
                start=start,
                end=end,
                pipeline_name=pipeline_name,
                latest_status=latest_status.value if latest_status else None,
                latest_destination_name=destination,
                limit=page,
                offset=skip,
            )

        return self._ctx.page(
            listing, PipelineActivity._from_payload, limit=limit, offset=offset
        )

    @overload
    def datasets(
        self: Telemetry[Sync],
        *,
        dataset_name: str | None = None,
        latest_status: PipelineRunStatus | None = None,
        destination: str | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> Iterable[DatasetActivity]: ...

    @overload
    def datasets(
        self: Telemetry[Async],
        *,
        dataset_name: str | None = None,
        latest_status: PipelineRunStatus | None = None,
        destination: str | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> AsyncIterable[DatasetActivity]: ...

    def datasets(
        self,
        *,
        dataset_name: str | None = None,
        latest_status: PipelineRunStatus | None = None,
        destination: str | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> Iterable[DatasetActivity] | AsyncIterable[DatasetActivity]:
        """Yield one row per dataset written to in the window.

        The window holds the pipeline runs whose start falls in ``[since, until)``.

        Args:
            dataset_name: Narrow to one dataset.
            latest_status: Narrow to datasets whose most recent run ended this
                way. Only ``SUCCEEDED`` and ``FAILED`` are filterable.
            destination: Narrow to datasets most recently written here.
            since: Start of the window, zone-aware. Defaults to seven days
                before ``until``.
            until: End of the window, zone-aware. Defaults to now.
            limit: Return at most this many. ``None`` walks to the end, or
                to row 10,100, past which the platform does not page.
            offset: Skip this many, server-side.

        Returns:
            An iterable of per-dataset activity; async-iterable in async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            DataplaneTokenRejected: The data plane rejected the token the
                platform issued for it.
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            ScopeMissing: Reached without a workspace in scope.
            ValueError: A status the platform cannot filter on, a naive
                ``since`` or ``until``, or a negative ``limit`` or ``offset``.
        """
        _refuse_unfilterable(latest_status)
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()
        start, end = _window(since, until)

        def listing(t: Any, page: int, skip: int) -> Any:
            return t.list_dataset_stats(
                workspace_id=workspace_id,
                dataplane_url=dataplane_url,
                start=start,
                end=end,
                dataset_name=dataset_name,
                latest_status=latest_status.value if latest_status else None,
                latest_destination_name=destination,
                limit=page,
                offset=skip,
            )

        return self._ctx.page(
            listing, DatasetActivity._from_payload, limit=limit, offset=offset
        )


class PipelineRunStatus(StrEnum):
    """What became of one dlt pipeline run.

    The platform records a run once dlt reports it finished, so only
    ``SUCCEEDED`` and ``FAILED`` occur; ``UNKNOWN`` covers values added later.
    """

    SUCCEEDED = "succeeded"
    """No dlt step raised an exception; some load jobs may still have failed."""
    FAILED = "failed"
    """Stopped on an error. ``error_step`` says where."""
    UNKNOWN = "unknown"
    """A status this SDK version does not know."""


#: The only statuses the platform accepts as a filter.
FILTERABLE_STATUSES = frozenset({PipelineRunStatus.SUCCEEDED, PipelineRunStatus.FAILED})


@dataclass(frozen=True)
class PipelineTable:
    """One table a pipeline run wrote, and what reached it."""

    table_name: str
    """Name of the table."""
    schema_name: str
    """The schema it sits in."""
    rows_extracted: int | None
    """Rows the extract step wrote for this table; `None` when not extracted."""
    rows_loaded: int | None
    """Rows that dlt prepared for loading for this table (normalized rows). dlt does not
    report per-row load counts, so this is set even when loading failed.
    """
    bytes_loaded: int | None
    """Bytes that dlt prepared for loading for this table (size of the normalized
    files). dlt does not report per-row load counts, so this is set even when loading
    failed.
    """
    load_job_state: str | None
    """`completed` or `failed`; `None` when the table was not loaded."""
    write_disposition: str | None
    """From the resource hints; `None` when the extract step reported none."""

    @staticmethod
    def _from_payload(payload: PipelineRunTableResponse) -> PipelineTable:
        return PipelineTable(
            table_name=payload.table_name,
            schema_name=_narrow.text(payload.schema_name) or "",
            rows_extracted=_narrow.whole(payload.rows_extracted),
            rows_loaded=_narrow.whole(payload.rows_loaded),
            bytes_loaded=_narrow.whole(payload.bytes_loaded),
            load_job_state=_narrow.text(payload.load_job_state),
            write_disposition=_narrow.text(payload.write_disposition),
        )


@dataclass(frozen=True)
class LoadPackage:
    """One load package a pipeline run produced.

    A run loads in packages, so a partial failure shows up here as some
    packages complete and others not.
    """

    load_id: str
    """dlt load id of the package."""
    schema_name: str | None
    """dlt schema the package was created with."""
    load_status: str | None
    """State dlt reported for the package; `loaded` means fully loaded."""
    job_count: int
    """Number of jobs in the package."""
    failed_job_count: int
    """Jobs that failed."""
    total_rows_loaded: int
    """Rows that dlt prepared for loading in this package (normalized rows, or extracted
    rows when normalize reported none). dlt does not report per-row load counts, so
    this is set even when loading failed.
    """
    total_bytes_loaded: int
    """Bytes that dlt prepared for loading in this package (size of the normalized
    files, or of the extracted files when normalize reported none). dlt does not
    report per-row load counts, so this is set even when loading failed.
    """
    is_pending: bool
    """Whether it is still waiting to be loaded."""
    has_schema_migration: bool
    """Whether loading it changed the destination's schema."""
    completed_at: datetime | None
    """When dlt completed the package, UTC; `None` while not completed."""

    @staticmethod
    def _from_payload(payload: LoadPackageResponse) -> LoadPackage:
        return LoadPackage(
            load_id=payload.load_id,
            schema_name=_narrow.text(payload.schema_name),
            load_status=_narrow.text(payload.load_status),
            job_count=_count(payload.job_count),
            failed_job_count=_count(payload.failed_job_count),
            total_rows_loaded=_count(payload.total_rows_loaded),
            total_bytes_loaded=_count(payload.total_bytes_loaded),
            is_pending=payload.is_pending is True,
            has_schema_migration=payload.has_schema_migration is True,
            completed_at=_narrow.moment(payload.completed_at),
        )


@dataclass(frozen=True)
class PipelineRunTrace:
    """The dlt trace one pipeline run produced."""

    pipeline_run_id: str
    """The pipeline run it belongs to."""
    trace: Mapping[str, Any]
    """The trace exactly as dlt wrote it — per-step timings, the resolved config, and
    the exception when a step raised. Left opaque: the platform stores and returns it
    verbatim and declares no shape for it, as with the definitions
    ``Jobs.deploy_manifest`` accepts.
    """


@dataclass(frozen=True, repr=False)
class PipelineRun(Entity[M]):
    """One dlt pipeline run, as telemetry recorded it.

    A job run executes whatever pipelines its job calls, so one run can
    produce several of these. Addressed by its own uuid, which is *not* a job
    run id. Get one from :meth:`PipelineRuns.list` or
    :attr:`PipelineRunSummary.pipeline_run_id`.
    """

    id: str
    """ID of the pipeline run; not a job run ID."""
    pipeline_name: str
    """Name of the dlt pipeline."""
    status: PipelineRunStatus
    """`failed` when any step raised, otherwise `succeeded`."""
    dataset_name: str | None
    """Dataset the run loaded into, from its load step; `None` when the run did not
    reach load.
    """
    destination_name: str | None
    """Destination the run loaded to, from its load step; `None` when the run did not
    reach load.
    """
    started_at: datetime | None
    """Start of the run from the dlt trace, UTC."""
    finished_at: datetime | None
    """End of the run from the dlt trace, UTC."""
    duration_ms: int | None
    """`finished_at` − `started_at` in milliseconds."""
    total_rows_extracted: int
    """Rows written by the extract step."""
    total_rows_loaded: int
    """Rows that dlt prepared for loading in this run (normalized rows). dlt does not
    report per-row load counts, so this is set even when loading failed.
    """
    total_bytes_loaded: int
    """Bytes that dlt prepared for loading in this run (size of the normalized files).
    dlt does not report per-row load counts, so this is set even when loading failed.
    """
    error_step: str | None
    """First step that raised, for example `extract`, `normalize` or `load`."""
    error_message: str | None
    """Exception message of that step."""
    has_schema_migration: bool | None
    """True when the load step created or changed user tables (`_dlt_*` tables are
    ignored).
    """
    dlt_version: str | None
    """dlt version that ran the pipeline, from the trace's execution context."""
    tables: tuple[PipelineTable, ...]
    """The tables it wrote, with rows per table. Empty on a listed row — only
    :meth:`PipelineRuns.get` reads them.
    """
    load_packages: tuple[LoadPackage, ...]
    """The packages it produced. Empty on a listed row, for the same reason."""

    _identity = ("pipeline_name", "id")
    _kind = EntityKind.PIPELINE_RUN

    @overload
    def trace(self: PipelineRun[Sync]) -> PipelineRunTrace: ...

    @overload
    def trace(self: PipelineRun[Async]) -> Awaitable[PipelineRunTrace]: ...

    def trace(self) -> PipelineRunTrace | Awaitable[PipelineRunTrace]:
        """Read the dlt trace this pipeline run produced.

        Returns:
            The trace; awaitable in async mode.

        Raises:
            NotFound: No trace was stored. A pipeline run the platform never
                linked to a job run has none.
            ScopeMissing: Reached without a workspace in scope.
        """
        return PipelineRuns(self._ctx).trace(id=self.id)

    @property
    def failed(self) -> bool:
        """Whether this pipeline run ended on an error.

        Returns:
            True for :attr:`PipelineRunStatus.FAILED`.
        """
        return self.status is PipelineRunStatus.FAILED

    @staticmethod
    def _from_payload(ctx: _Ctx[Any], payload: PipelineRunPayload) -> PipelineRun[Any]:
        return PipelineRun._bind(
            ctx,
            PipelineRun(
                id=str(payload.id),
                pipeline_name=payload.pipeline_name,
                status=PipelineRunStatus(str(payload.status)),
                dataset_name=_narrow.text(payload.dataset_name),
                destination_name=_narrow.text(payload.destination_name),
                started_at=_narrow.moment(payload.started_at),
                finished_at=_narrow.moment(payload.finished_at),
                duration_ms=_narrow.whole(getattr(payload, "duration_ms", None)),
                total_rows_extracted=_count(payload.total_rows_extracted),
                total_rows_loaded=_count(payload.total_rows_loaded),
                total_bytes_loaded=_count(payload.total_bytes_loaded),
                error_step=_narrow.text(payload.error_step),
                error_message=_narrow.text(payload.error_message),
                has_schema_migration=(
                    payload.has_schema_migration
                    if isinstance(payload.has_schema_migration, bool)
                    else None
                ),
                dlt_version=_narrow.text(payload.dlt_version),
                tables=tuple(
                    PipelineTable._from_payload(row)
                    for row in getattr(payload, "tables", None) or ()
                ),
                load_packages=tuple(
                    LoadPackage._from_payload(row)
                    for row in getattr(payload, "load_packages", None) or ()
                ),
            ),
        )


def _count(value: Any) -> int:
    """Narrow a counter the generated model may leave unset.

    Args:
        value: What the payload carries.

    Returns:
        The integer, or 0 for anything else.
    """
    return value if isinstance(value, int) else 0


@dataclass(frozen=True)
class PipelineActivity:
    """How one pipeline has been doing over a window."""

    pipeline_name: str
    """Name of the dlt pipeline."""
    total_pipeline_run_count: int
    """Pipeline runs in the range."""
    succeeded_pipeline_run_count: int
    """Pipeline runs in the range with status `succeeded`."""
    failed_pipeline_run_count: int
    """How many did not. Derived, since the platform reports the successes and the
    total.
    """
    success_ratio: float
    """Succeeded ÷ total, from 0 to 1."""
    total_rows_extracted: int
    """Sum of extracted rows over all runs in the range."""
    total_rows_loaded: int
    """Sum of normalized rows over succeeded runs in the time range."""
    total_bytes_loaded: int
    """Sum of normalized bytes (size of the normalized files) over succeeded runs in the
    time range.
    """
    average_duration_ms: int | None
    """Mean `duration_ms` in the range, rounded; `None` when no run has a duration."""
    total_duration_ms: int
    """Sum of `duration_ms` over the runs in the range."""
    latest_status: str | None
    """Status of the most recent pipeline run in the time range."""
    latest_pipeline_run_at: datetime | None
    """When the most recent pipeline run in the time range started."""
    latest_dataset_name: str | None
    """Dataset of the most recent pipeline run in the time range."""
    latest_destination_name: str | None
    """Destination of the most recent pipeline run in the time range."""
    latest_source_names: tuple[str, ...]
    """Sources read by the most recent pipeline run in the time range."""

    @staticmethod
    def _from_payload(
        _ctx: _Ctx[Any], payload: PipelineStatsResponse
    ) -> PipelineActivity:
        runs = _count(payload.total_pipeline_run_count)
        succeeded = _count(payload.succeeded_pipeline_run_count)
        sources = payload.latest_source_names
        return PipelineActivity(
            pipeline_name=payload.pipeline_name,
            total_pipeline_run_count=runs,
            succeeded_pipeline_run_count=succeeded,
            failed_pipeline_run_count=max(0, runs - succeeded),
            success_ratio=float(payload.success_ratio),
            total_rows_extracted=_count(payload.total_rows_extracted),
            total_rows_loaded=_count(payload.total_rows_loaded),
            total_bytes_loaded=_count(payload.total_bytes_loaded),
            average_duration_ms=_narrow.whole(payload.average_duration_ms),
            total_duration_ms=_count(payload.total_duration_ms),
            latest_status=_narrow.text(payload.latest_status),
            latest_pipeline_run_at=_narrow.moment(payload.latest_pipeline_run_at),
            latest_dataset_name=_narrow.text(payload.latest_dataset_name),
            latest_destination_name=_narrow.text(payload.latest_destination_name),
            latest_source_names=tuple(sources) if isinstance(sources, list) else (),
        )


@dataclass(frozen=True)
class DatasetActivity:
    """What landed in one dataset over a window."""

    dataset_name: str
    """Name of the dataset, across destinations."""
    distinct_pipeline_count: int
    """Number of distinct pipelines that ran into this dataset in the range."""
    total_pipeline_run_count: int
    """Pipeline runs in the range."""
    succeeded_pipeline_run_count: int
    """Pipeline runs in the range with status `succeeded`."""
    failed_pipeline_run_count: int
    """How many did not. Derived, as for a pipeline."""
    success_ratio: float
    """Succeeded ÷ total, from 0 to 1."""
    total_rows_loaded: int
    """Sum of normalized rows over succeeded runs in the time range."""
    total_bytes_loaded: int
    """Sum of normalized bytes (size of the normalized files) over succeeded runs in the
    time range.
    """
    schema_migration_count: int
    """Runs in the range with `has_schema_migration`."""
    average_duration_ms: int | None
    """Mean `duration_ms` in the range, rounded; `None` when no run has a duration."""
    latest_status: str | None
    """Status of the most recent pipeline run in the time range."""
    latest_pipeline_run_at: datetime | None
    """When the most recent pipeline run in the time range started."""
    latest_pipeline_name: str | None
    """Pipeline of the most recent pipeline run in the time range."""
    latest_destination_name: str | None
    """Destination of the most recent pipeline run in the time range."""

    @staticmethod
    def _from_payload(
        _ctx: _Ctx[Any], payload: DatasetStatsResponse
    ) -> DatasetActivity:
        runs = _count(payload.total_pipeline_run_count)
        succeeded = _count(payload.succeeded_pipeline_run_count)
        return DatasetActivity(
            dataset_name=payload.dataset_name,
            distinct_pipeline_count=_count(payload.distinct_pipeline_count),
            total_pipeline_run_count=runs,
            succeeded_pipeline_run_count=succeeded,
            failed_pipeline_run_count=max(0, runs - succeeded),
            success_ratio=float(payload.success_ratio),
            total_rows_loaded=_count(payload.total_rows_loaded),
            total_bytes_loaded=_count(payload.total_bytes_loaded),
            schema_migration_count=_count(payload.schema_migration_count),
            average_duration_ms=_narrow.whole(payload.average_duration_ms),
            latest_status=_narrow.text(payload.latest_status),
            latest_pipeline_run_at=_narrow.moment(payload.latest_pipeline_run_at),
            latest_pipeline_name=_narrow.text(payload.latest_pipeline_name),
            latest_destination_name=_narrow.text(payload.latest_destination_name),
        )


class PipelineRuns(Collection[M]):
    """The dlt pipeline runs telemetry recorded for one workspace.

    Every read covers a time window, which defaults to the last seven days.
    There is no ``count()``; walk :meth:`list`.
    """

    _entity = PipelineRun

    @overload
    def get(self: PipelineRuns[Sync], *, id: str) -> PipelineRun[Sync]: ...

    @overload
    def get(self: PipelineRuns[Async], *, id: str) -> Awaitable[PipelineRun[Async]]: ...

    def get(self, *, id: str) -> PipelineRun[Any] | Awaitable[PipelineRun[Any]]:
        """Return one pipeline run by id, in full.

        Args:
            id: The pipeline run's uuid, from :meth:`PipelineRuns.list` or
                :attr:`PipelineRunSummary.pipeline_run_id`. A job run id will
                not do — they are different things.

        Returns:
            The pipeline run; awaitable in async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            DataplaneTokenRejected: The data plane rejected the token the
                platform issued for it.
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            NotFound: No such pipeline run in this workspace.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()
        return self._ctx.run(
            lambda t: t.get_pipeline_run(
                workspace_id=workspace_id,
                dataplane_url=dataplane_url,
                pipeline_run_id=id,
            ),
            PipelineRun._from_payload,
        )

    @overload
    def trace(self: PipelineRuns[Sync], *, id: str) -> PipelineRunTrace: ...

    @overload
    def trace(self: PipelineRuns[Async], *, id: str) -> Awaitable[PipelineRunTrace]: ...

    def trace(self, *, id: str) -> PipelineRunTrace | Awaitable[PipelineRunTrace]:
        """Read one pipeline run's dlt trace, without reading the run itself.

        Args:
            id: The pipeline run's uuid.

        Returns:
            The trace; awaitable in async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            NotFound: No such pipeline run, or it has no stored trace. One the
                platform never linked to a job run has none.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()

        def parse(
            _ctx: _Ctx[Any], payload: PipelineRunTraceResponse
        ) -> PipelineRunTrace:
            return PipelineRunTrace(pipeline_run_id=id, trace=payload.to_dict())

        return self._ctx.run(
            lambda t: t.get_pipeline_run_trace(
                workspace_id=workspace_id,
                dataplane_url=dataplane_url,
                pipeline_run_id=id,
            ),
            parse,
        )

    @overload
    def list(
        self: PipelineRuns[Sync],
        *,
        job_run_id: str | None = None,
        pipeline_name: str | None = None,
        status: PipelineRunStatus | None = None,
        dataset: str | None = None,
        destination: str | None = None,
        empty_only: bool | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> Iterable[PipelineRun[Sync]]: ...

    @overload
    def list(
        self: PipelineRuns[Async],
        *,
        job_run_id: str | None = None,
        pipeline_name: str | None = None,
        status: PipelineRunStatus | None = None,
        dataset: str | None = None,
        destination: str | None = None,
        empty_only: bool | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> AsyncIterable[PipelineRun[Async]]: ...

    def list(
        self,
        *,
        job_run_id: str | None = None,
        pipeline_name: str | None = None,
        status: PipelineRunStatus | None = None,
        dataset: str | None = None,
        destination: str | None = None,
        empty_only: bool | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> Iterable[PipelineRun[Any]] | AsyncIterable[PipelineRun[Any]]:
        """Yield pipeline runs in the window, newest first.

        The window holds the pipeline runs whose start falls in ``[since, until)``.

        Args:
            job_run_id: Narrow to the pipelines one job run executed.
            pipeline_name: Narrow to one pipeline.
            status: Narrow to one outcome. Only ``SUCCEEDED`` and ``FAILED`` are
                filterable.
            dataset: Narrow to runs that wrote to one dataset.
            destination: Narrow to runs that wrote to one destination.
            empty_only: True for succeeded runs that extracted nothing to load.
                False for every other run, failed ones included. ``None`` for
                both.
            since: Start of the window, zone-aware. Defaults to seven days
                before ``until``.
            until: End of the window, zone-aware. Defaults to now.
            limit: Return at most this many. ``None`` walks to the end, or
                to row 10,100, past which the platform does not page.
            offset: Skip this many, server-side.

        Returns:
            An iterable of pipeline runs; async-iterable in async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            DataplaneTokenRejected: The data plane rejected the token the
                platform issued for it.
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            ScopeMissing: Reached without a workspace in scope.
            ValueError: A status the platform cannot filter on, a naive
                ``since`` or ``until``, or a negative ``limit`` or ``offset``.
        """
        _refuse_unfilterable(status)
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()
        start, end = _window(since, until)

        def listing(t: Any, page: int, skip: int) -> Any:
            return t.list_pipeline_runs(
                workspace_id=workspace_id,
                dataplane_url=dataplane_url,
                start=start,
                end=end,
                job_run_id=job_run_id,
                pipeline_name=pipeline_name,
                status=status.value if status else None,
                dataset_name=dataset,
                destination_name=destination,
                is_empty_run=empty_only,
                limit=page,
                offset=skip,
            )

        return self._ctx.page(
            listing, PipelineRun._from_payload, limit=limit, offset=offset
        )
