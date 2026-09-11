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
        DatasetOverviewResponse,
        GetPipelineRunTraceResponse200,
        LoadPackageResponse,
        PipelineOverviewResponse,
        PipelineRunDetailResponse,
        PipelineRunResponse,
        PipelineRunTableResponse,
        TelemetryWatermarkResponse,
    )

    #: list returns the row, get the detailed shape.
    PipelineRunPayload = PipelineRunResponse | PipelineRunDetailResponse

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
    """How current the platform's telemetry is for one workspace.

    Attributes:
        updated_at: When telemetry last recorded anything, or ``None`` when it
            never has. What separates "nothing ran" from a reading that stopped
            being updated: a zero elsewhere means nothing while this is stale.
    """

    updated_at: datetime | None

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
        """Return when telemetry last recorded anything for this workspace.

        Returns:
            The watermark; awaitable in async mode.

        Raises:
            NotAuthorized: The caller may not read this workspace's telemetry.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()
        return self._ctx.run(
            lambda t: t.get_telemetry_watermark(
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

        Args:
            pipeline_name: Narrow to one pipeline.
            latest_status: Narrow to pipelines whose most recent run ended this
                way. Only ``SUCCEEDED`` and ``FAILED`` are filterable.
            destination: Narrow to pipelines most recently writing here.
            since: Start of the window, zone-aware. Defaults to seven days
                before ``until``.
            until: End of the window, zone-aware. Defaults to now.
            limit: Return at most this many. ``None`` walks to the end.
            offset: Skip this many, server-side.

        Returns:
            An iterable of per-pipeline activity; async-iterable in async mode.

        Raises:
            ScopeMissing: Reached without a workspace in scope.
            ValueError: A status the platform cannot filter on, a naive
                ``since`` or ``until``, or a negative ``limit`` or ``offset``.
        """
        _refuse_unfilterable(latest_status)
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()
        start, end = _window(since, until)

        def listing(t: Any, page: int, skip: int) -> Any:
            return t.list_pipeline_overview(
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

        Args:
            dataset_name: Narrow to one dataset.
            latest_status: Narrow to datasets whose most recent run ended this
                way. Only ``SUCCEEDED`` and ``FAILED`` are filterable.
            destination: Narrow to datasets most recently written here.
            since: Start of the window, zone-aware. Defaults to seven days
                before ``until``.
            until: End of the window, zone-aware. Defaults to now.
            limit: Return at most this many. ``None`` walks to the end.
            offset: Skip this many, server-side.

        Returns:
            An iterable of per-dataset activity; async-iterable in async mode.

        Raises:
            ScopeMissing: Reached without a workspace in scope.
            ValueError: A status the platform cannot filter on, a naive
                ``since`` or ``until``, or a negative ``limit`` or ``offset``.
        """
        _refuse_unfilterable(latest_status)
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()
        start, end = _window(since, until)

        def listing(t: Any, page: int, skip: int) -> Any:
            return t.list_dataset_overview(
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

    The platform sends this as an open string and only ever filters on
    ``SUCCEEDED`` and ``FAILED``, so a run still going reports something this
    does not know rather than a member of its own.

    Attributes:
        SUCCEEDED: Finished, having loaded what it extracted.
        FAILED: Stopped on an error. ``error_step`` says where.
        UNKNOWN: A status this SDK version does not know.
    """

    SUCCEEDED = "succeeded"
    FAILED = "failed"
    UNKNOWN = "unknown"


#: The only statuses the platform accepts as a filter.
FILTERABLE_STATUSES = frozenset({PipelineRunStatus.SUCCEEDED, PipelineRunStatus.FAILED})


@dataclass(frozen=True)
class PipelineTable:
    """One table a pipeline run wrote, and what reached it.

    Attributes:
        table_name: The table's name.
        schema_name: The schema it sits in.
        rows_extracted: Rows read for this table.
        rows_loaded: Rows written to it. Lower than ``rows_extracted`` when its
            load job failed part-way.
        bytes_loaded: Bytes written.
        load_state: What its load job ended as.
        write_disposition: How it was written — append, replace or merge.
    """

    table_name: str
    schema_name: str
    rows_extracted: int | None
    rows_loaded: int | None
    bytes_loaded: int | None
    load_state: str | None
    write_disposition: str | None

    @staticmethod
    def _from_payload(payload: PipelineRunTableResponse) -> PipelineTable:
        return PipelineTable(
            table_name=payload.table_name,
            schema_name=_narrow.text(payload.schema_name) or "",
            rows_extracted=_narrow.whole(payload.rows_extracted),
            rows_loaded=_narrow.whole(payload.rows_loaded),
            bytes_loaded=_narrow.whole(payload.bytes_loaded),
            load_state=_narrow.text(payload.load_job_state),
            write_disposition=_narrow.text(payload.write_disposition),
        )


@dataclass(frozen=True)
class LoadPackage:
    """One load package a pipeline run produced.

    A run loads in packages, so a partial failure shows up here as some
    packages complete and others not.

    Attributes:
        load_id: dlt's load id, which is how a package is identified in logs.
        schema_name: The schema it carried.
        status: What the load ended as.
        jobs: How many load jobs it held.
        failed_jobs: How many of them failed.
        rows_loaded: Rows it wrote.
        bytes_loaded: Bytes it wrote.
        pending: Whether it is still waiting to be loaded.
        schema_migrated: Whether loading it changed the destination's schema.
        completed_at: When it finished.
    """

    load_id: str
    schema_name: str | None
    status: str | None
    jobs: int
    failed_jobs: int
    rows_loaded: int
    bytes_loaded: int
    pending: bool
    schema_migrated: bool
    completed_at: datetime | None

    @staticmethod
    def _from_payload(payload: LoadPackageResponse) -> LoadPackage:
        return LoadPackage(
            load_id=payload.load_id,
            schema_name=_narrow.text(payload.schema_name),
            status=_narrow.text(payload.load_status),
            jobs=_count(payload.job_count),
            failed_jobs=_count(payload.failed_job_count),
            rows_loaded=_count(payload.total_rows_loaded),
            bytes_loaded=_count(payload.total_bytes_loaded),
            pending=payload.is_pending is True,
            schema_migrated=payload.has_schema_migration is True,
            completed_at=_narrow.moment(payload.completed_at),
        )


@dataclass(frozen=True)
class PipelineRunTrace:
    """The dlt trace one pipeline run produced.

    Attributes:
        pipeline_run_id: The pipeline run it belongs to.
        trace: The trace exactly as dlt wrote it — per-step timings, the
            resolved config, and the exception when a step raised. Left opaque:
            the platform stores and returns it verbatim and declares no shape
            for it, as with the definitions ``Jobs.deploy_manifest`` accepts.
    """

    pipeline_run_id: str
    trace: Mapping[str, Any]


@dataclass(frozen=True, repr=False)
class PipelineRun(Entity[M]):
    """One dlt pipeline run, as telemetry recorded it.

    A job run executes whatever pipelines its script calls, so one run can
    produce several of these. Addressed by its own uuid, which is *not* a job
    run id — only :meth:`PipelineRuns.list` hands one out.

    Attributes:
        id: This pipeline run's uuid.
        pipeline_name: The dlt pipeline's name.
        status: What became of it.
        dataset: The dataset it wrote to, when it reported one.
        destination: Where it wrote.
        started_at: When it began.
        ended_at: When it finished.
        duration_seconds: How long it ran.
        rows_extracted: Rows read from the source.
        rows_loaded: Rows written to the destination. Lower than
            ``rows_extracted`` when a load failed part-way.
        bytes_loaded: Bytes written.
        error_step: Which dlt step failed, when one did.
        error_message: What it said.
        schema_migrated: Whether the load changed the destination's schema.
        dlt_version: The dlt that ran it.
        tables: The tables it wrote, with rows per table. Empty on a listed row
            — only :meth:`PipelineRuns.get` reads them.
        load_packages: The packages it produced. Empty on a listed row, for the
            same reason.
    """

    id: str
    pipeline_name: str
    status: PipelineRunStatus
    dataset: str | None
    destination: str | None
    started_at: datetime | None
    ended_at: datetime | None
    duration_seconds: float | None
    rows_extracted: int
    rows_loaded: int
    bytes_loaded: int
    error_step: str | None
    error_message: str | None
    schema_migrated: bool | None
    dlt_version: str | None
    tables: tuple[PipelineTable, ...]
    load_packages: tuple[LoadPackage, ...]

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
        duration_ms = getattr(payload, "duration_ms", None)
        return PipelineRun._bind(
            ctx,
            PipelineRun(
                id=str(payload.id),
                pipeline_name=payload.pipeline_name,
                status=PipelineRunStatus(str(payload.status)),
                dataset=_narrow.text(payload.dataset_name),
                destination=_narrow.text(payload.destination_name),
                started_at=_narrow.moment(payload.started_at),
                ended_at=_narrow.moment(payload.finished_at),
                duration_seconds=(
                    duration_ms / 1000
                    if isinstance(duration_ms, (int, float))
                    else None
                ),
                rows_extracted=_count(payload.total_rows_extracted),
                rows_loaded=_count(payload.total_rows_loaded),
                bytes_loaded=_count(payload.total_bytes_loaded),
                error_step=_narrow.text(payload.error_step),
                error_message=_narrow.text(payload.error_message),
                schema_migrated=(
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
    """How one pipeline has been doing over a window.

    Attributes:
        pipeline_name: The dlt pipeline's name.
        runs: How many times it ran.
        succeeded: How many of those succeeded.
        failed: How many did not. Derived, since the platform reports the
            successes and the total.
        success_rate: The platform's own figure, between 0 and 1.
        rows_extracted: Rows read across every run.
        rows_loaded: Rows written across every run.
        bytes_loaded: Bytes written across every run.
        average_duration_seconds: Mean run length, or ``None`` when nothing
            finished.
        total_duration_seconds: Time spent running, across the window.
        latest_status: What its most recent run ended as.
        latest_run_at: When that run happened.
        latest_dataset: The dataset it most recently wrote to.
        latest_destination: The destination it most recently wrote to.
        latest_sources: The sources its most recent run read.
    """

    pipeline_name: str
    runs: int
    succeeded: int
    failed: int
    success_rate: float
    rows_extracted: int
    rows_loaded: int
    bytes_loaded: int
    average_duration_seconds: float | None
    total_duration_seconds: float
    latest_status: str | None
    latest_run_at: datetime | None
    latest_dataset: str | None
    latest_destination: str | None
    latest_sources: tuple[str, ...]

    @staticmethod
    def _from_payload(
        _ctx: _Ctx[Any], payload: PipelineOverviewResponse
    ) -> PipelineActivity:
        runs = _count(payload.total_runs)
        succeeded = _count(payload.succeeded_runs)
        sources = payload.latest_source_names
        return PipelineActivity(
            pipeline_name=payload.pipeline_name,
            runs=runs,
            succeeded=succeeded,
            failed=max(0, runs - succeeded),
            success_rate=float(payload.success_rate),
            rows_extracted=_count(payload.total_rows_extracted),
            rows_loaded=_count(payload.total_rows_loaded),
            bytes_loaded=_count(payload.total_bytes_loaded),
            average_duration_seconds=_narrow.seconds(payload.avg_duration_ms),
            total_duration_seconds=_narrow.seconds(payload.total_duration_ms) or 0.0,
            latest_status=_narrow.text(payload.latest_status),
            latest_run_at=_narrow.moment(payload.latest_run_at),
            latest_dataset=_narrow.text(payload.latest_dataset_name),
            latest_destination=_narrow.text(payload.latest_destination_name),
            latest_sources=tuple(sources) if isinstance(sources, list) else (),
        )


@dataclass(frozen=True)
class DatasetActivity:
    """What landed in one dataset over a window.

    Attributes:
        dataset_name: The dataset's name.
        pipelines: How many distinct pipelines wrote here. More than one means
            they share it, which is worth knowing before blaming any of them.
        runs: How many runs wrote here.
        succeeded: How many of those succeeded.
        failed: How many did not. Derived, as for a pipeline.
        success_rate: The platform's own figure, between 0 and 1.
        rows_loaded: Rows written across every run.
        bytes_loaded: Bytes written across every run.
        schema_migrations: How many loads changed the schema here.
        average_duration_seconds: Mean run length, or ``None`` when nothing
            finished.
        latest_status: What the most recent run ended as.
        latest_run_at: When that run happened.
        latest_pipeline: Which pipeline wrote most recently.
        latest_destination: Where it wrote.
    """

    dataset_name: str
    pipelines: int
    runs: int
    succeeded: int
    failed: int
    success_rate: float
    rows_loaded: int
    bytes_loaded: int
    schema_migrations: int
    average_duration_seconds: float | None
    latest_status: str | None
    latest_run_at: datetime | None
    latest_pipeline: str | None
    latest_destination: str | None

    @staticmethod
    def _from_payload(
        _ctx: _Ctx[Any], payload: DatasetOverviewResponse
    ) -> DatasetActivity:
        runs = _count(payload.total_runs)
        succeeded = _count(payload.succeeded_runs)
        return DatasetActivity(
            dataset_name=payload.dataset_name,
            pipelines=_count(payload.distinct_pipeline_count),
            runs=runs,
            succeeded=succeeded,
            failed=max(0, runs - succeeded),
            success_rate=float(payload.success_rate),
            rows_loaded=_count(payload.total_rows_loaded),
            bytes_loaded=_count(payload.total_bytes_loaded),
            schema_migrations=_count(payload.schema_migration_count),
            average_duration_seconds=_narrow.seconds(payload.avg_duration_ms),
            latest_status=_narrow.text(payload.latest_status),
            latest_run_at=_narrow.moment(payload.latest_run_at),
            latest_pipeline=_narrow.text(payload.latest_pipeline_name),
            latest_destination=_narrow.text(payload.latest_destination_name),
        )


class PipelineRuns(Collection[M]):
    """The dlt pipeline runs telemetry recorded for one workspace.

    Every read covers a time window, because the platform requires one. Alone
    among the collections there is no ``count()``: the platform offers no total
    for a window, so counting means walking :meth:`list`.
    """

    _entity = PipelineRun

    @overload
    def get(self: PipelineRuns[Sync], *, id: str) -> PipelineRun[Sync]: ...

    @overload
    def get(self: PipelineRuns[Async], *, id: str) -> Awaitable[PipelineRun[Async]]: ...

    def get(self, *, id: str) -> PipelineRun[Any] | Awaitable[PipelineRun[Any]]:
        """Return one pipeline run by id, in full.

        Args:
            id: The pipeline run's uuid, from :meth:`list`. A job run id will
                not do — they are different things.

        Returns:
            The pipeline run; awaitable in async mode.

        Raises:
            BadRequest: ``id`` is not a uuid.
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
            BadRequest: ``id`` is not a uuid.
            NotFound: No such pipeline run, or it has no stored trace. One the
                platform never linked to a job run has none.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()

        def parse(
            _ctx: _Ctx[Any], payload: GetPipelineRunTraceResponse200
        ) -> PipelineRunTrace:
            # The platform returns the trace verbatim, so the generated model
            # declares no fields and everything lands in additional_properties.
            return PipelineRunTrace(
                pipeline_run_id=id, trace=dict(payload.additional_properties)
            )

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

        This is the only place a pipeline run id comes from.

        Args:
            job_run_id: Narrow to the pipelines one job run executed.
            pipeline_name: Narrow to one pipeline.
            status: Narrow to one outcome. Only ``SUCCEEDED`` and ``FAILED`` are
                filterable.
            dataset: Narrow to runs that wrote to one dataset.
            destination: Narrow to runs that wrote to one destination.
            empty_only: True for runs that loaded nothing, False for those that
                loaded something, ``None`` for both.
            since: Start of the window, zone-aware. Defaults to seven days
                before ``until``.
            until: End of the window, zone-aware. Defaults to now.
            limit: Return at most this many. ``None`` walks to the end.
            offset: Skip this many, server-side.

        Returns:
            An iterable of pipeline runs; async-iterable in async mode.

        Raises:
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
