"""Job runs — one execution of a job, and what became of it."""

from __future__ import annotations

# Python internals
from dataclasses import dataclass
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterable,
    Awaitable,
    Iterable,
    Mapping,
    Sequence,
    overload,
)
from uuid import UUID

# Current package
from dlthub_sdk._glue.base import Collection, Entity
from dlthub_sdk._glue.context import Async, Listing, M, Sync, _Ctx
from dlthub_sdk._glue.enums import EntityKind, StrEnum
from dlthub_sdk.domain import _narrow
from dlthub_sdk.domain.logs import LogLine

if TYPE_CHECKING:
    # Typing only: domain never imports _gen at runtime.
    # Current package
    from dlthub_sdk._gen.api.models import (
        CancelJobRunsResponse,
        DetailedJobRunResponse,
        PipelineRunSummaryResponse,
    )
    from dlthub_sdk._gen.telemetry.models import (
        JobResultResponse,
        JobResultTraceResponse,
    )


class JobRunStatus(StrEnum):
    """Where a run has got to."""

    PENDING = "pending"
    """Accepted, not yet started."""
    STARTING = "starting"
    """Being placed on a compute backend."""
    RUNNING = "running"
    """Executing."""
    CANCELLING = "cancelling"
    """Cancellation asked for, not yet effective."""
    COMPLETED = "completed"
    """Finished successfully."""
    FAILED = "failed"
    """Finished unsuccessfully."""
    CANCELLED = "cancelled"
    """Stopped on request, or because it exceeded its maximum run time."""
    SKIPPED = "skipped"
    """Recorded without running. A start the platform declines is normally reported
    through :class:`TriggerStatus` and creates no run.
    """
    UNKNOWN = "unknown"
    """A status this SDK version does not know."""


#: The statuses a run never leaves. Anything else may still change.
TERMINAL_STATUSES = frozenset(
    {
        JobRunStatus.COMPLETED,
        JobRunStatus.FAILED,
        JobRunStatus.CANCELLED,
        JobRunStatus.SKIPPED,
    }
)

#: The terminal statuses that did not succeed. SKIPPED is terminal but not a
#: failure: nothing was attempted.
FAILED_STATUSES = frozenset({JobRunStatus.FAILED, JobRunStatus.CANCELLED})


@dataclass(frozen=True)
class PipelineRunSummary:
    """One dlt pipeline a run executed, as telemetry reported it.

    A run executes whatever pipelines its job calls, so a job that loads two
    sources reports two. A run carries one entry per dlt pipeline name it
    reported; a pipeline that ran more than once shows its latest report.
    Telemetry fills this in after the pipeline reports, so a run that has just
    started carries none, and a run whose job never reached a pipeline carries
    none for good.
    """

    pipeline_name: str
    """Name of the dlt pipeline."""
    pipeline_run_id: str | None
    """Telemetry ID of the pipeline run."""
    transaction_id: str | None
    """Transaction ID of the pipeline run."""
    destination_name: str | None
    """Name of the destination the pipeline wrote to."""
    dataset_name: str | None
    """Name of the dataset the pipeline wrote to."""
    # doc: sdk
    status: str | None
    """What the pipeline run ended as. Free-form: it is dlt's own wording, not
    :class:`JobRunStatus`.
    """
    total_rows: int | None
    """Total number of rows loaded by the pipeline."""
    duration_ms: int | None
    """Duration of the pipeline run in milliseconds."""
    started_at: datetime | None
    """When the pipeline run started."""
    finished_at: datetime | None
    """When the pipeline run finished."""

    @staticmethod
    def _from_payload(payload: PipelineRunSummaryResponse) -> PipelineRunSummary:
        return PipelineRunSummary(
            pipeline_name=payload.pipeline_name,
            pipeline_run_id=(
                str(payload.pipeline_run_id)
                if isinstance(payload.pipeline_run_id, UUID)
                else None
            ),
            transaction_id=_narrow.text(payload.transaction_id),
            destination_name=_narrow.text(payload.destination_name),
            dataset_name=_narrow.text(payload.dataset_name),
            status=_narrow.text(payload.status),
            total_rows=_narrow.whole(payload.total_rows),
            duration_ms=_narrow.whole(payload.duration_ms),
            started_at=_narrow.moment(payload.started_at),
            finished_at=_narrow.moment(payload.finished_at),
        )


@dataclass(frozen=True)
class CancelledRun:
    """One run a bulk cancel stopped."""

    job_ref: str
    """Job reference of the cancelled run."""
    job_run_id: str
    """ID of the cancelled run."""
    job_run_number: int
    """Number of the run within its job; numbers repeat across jobs."""
    previous_status: JobRunStatus
    """Status of the run when the cancel request arrived."""


@dataclass(frozen=True)
class CancelReport:
    """What a bulk cancel did."""

    cancelled: tuple[CancelledRun, ...]
    """The runs asked to stop (now cancelling), or that would be in a dry run."""
    not_running: tuple[str, ...]
    """Job refs that had nothing to stop, which is not an error."""

    @staticmethod
    def _from_payload(
        _ctx: _Ctx[Any], payload: CancelJobRunsResponse, job_refs: Sequence[str]
    ) -> CancelReport:
        cancelled = tuple(
            CancelledRun(
                job_ref=item.job_ref,
                job_run_id=str(item.job_run_id),
                job_run_number=item.job_run_number,
                previous_status=JobRunStatus(str(item.previous_status)),
            )
            for item in payload.succeeded
        )
        stopped = {run.job_ref for run in cancelled}
        return CancelReport(
            cancelled=cancelled,
            not_running=tuple(ref for ref in job_refs if ref not in stopped),
        )


@dataclass(frozen=True)
class JobResultTrace:
    """The whole job result a run delivered, as the job sent it.

    :class:`JobResult` carries the summary fields; this carries the whole result
    as the job delivered it, which is where an agent's per-turn tool calls live.
    """

    job_run_id: str
    """The run that declared it."""
    result: Mapping[str, Any]
    """The result exactly as delivered — the declared output and, for an agent, its
    trace: turns and the tools each called, token counts, stop reason. Left opaque:
    the platform stores and returns it verbatim and declares no shape for it.
    """


@dataclass(frozen=True)
class JobResult:
    """The structured result a run declared.

    A run yields at most one, and most do not: a plain pipeline job declares
    none, where an agent job reports its own outcome here. The agent fields are
    ``None`` for any other kind of result.
    """

    job_run_id: str
    """Job run that declared the result."""
    job_ref: str
    """The job that declared the result."""
    result_type: str
    """`job.{category}.{name}`, for example `job.background_agent.{name}`."""
    engine_version: int
    """Result format version; 1 when not declared."""
    result: Any
    """The job's declared output. Shape is job-defined."""
    agent_status: str | None
    """The agent's self-report, which may legitimately disagree with the run's own
    status: a failed agent inside a succeeded run is normal.
    """
    summary: str | None
    """Model-authored markdown, unbounded. Untrusted — render as user content."""
    model: str | None
    """Model the agent ran with. `None` when the result carries no agent trace, as for
    non-agent jobs.
    """
    loop_type: str | None
    """Agent loop that ran. `None` when the result carries no agent trace, as for
    non-agent jobs.
    """
    input_tokens: int | None
    """Input tokens the agent used. `None` when the result carries no agent trace, as
    for non-agent jobs.
    """
    output_tokens: int | None
    """Output tokens the agent used. `None` when the result carries no agent trace, as
    for non-agent jobs.
    """
    total_tokens: int | None
    """Total tokens the agent used. `None` when the result carries no agent trace, as
    for non-agent jobs.
    """
    cost_usd: str | None
    """Cost in USD the agent reported, as a decimal string. `None` when the result
    carries no agent trace, as for non-agent jobs.
    """
    turn_count: int | None
    """Number of turns the agent took. `None` when the result carries no agent trace, as
    for non-agent jobs.
    """
    stop_reason: str | None
    """Why the agent stopped. `None` when the result carries no agent trace, as for
    non-agent jobs.
    """
    created_at: datetime
    """When the result was first stored, UTC."""
    updated_at: datetime
    """When the result was last stored, UTC."""

    @staticmethod
    def _from_payload(_ctx: _Ctx[Any], payload: JobResultResponse) -> JobResult:
        return JobResult(
            job_run_id=str(payload.job_run_id),
            job_ref=payload.job_ref,
            result_type=payload.result_type,
            engine_version=payload.engine_version,
            result=_narrow.data(payload.result),
            agent_status=_narrow.text(payload.agent_status),
            summary=_narrow.text(payload.summary),
            model=_narrow.text(payload.model),
            loop_type=_narrow.text(payload.loop_type),
            input_tokens=_narrow.whole(payload.input_tokens),
            output_tokens=_narrow.whole(payload.output_tokens),
            total_tokens=_narrow.whole(payload.total_tokens),
            cost_usd=_narrow.text(payload.cost_usd),
            turn_count=_narrow.whole(payload.turn_count),
            stop_reason=_narrow.text(payload.stop_reason),
            created_at=payload.created_at,
            updated_at=payload.updated_at,
        )


@dataclass(frozen=True, repr=False)
class JobRun(Entity[M]):
    """One execution of a job."""

    number: int
    """Number of the run within its job, counting up from 1; numbers repeat across jobs.
    """
    id: str
    """Unique ID (a UUID)."""
    job_ref: str
    """Canonical job reference, unique per workspace."""
    status: JobRunStatus
    """The status of the run."""
    trigger: str
    """The trigger the run fired with, e.g. `schedule:0 8 * * *`, `manual:jobs.my_job`,
    `job.success:jobs.upstream`.
    """
    profile: str
    """The name of the profile that was used for the run."""
    started_at: datetime | None
    """When the run started; `None` until it has."""
    finished_at: datetime | None
    """When the run finished; `None` until it has."""
    duration_seconds: float | None
    """Duration of the run in seconds, possibly fractional; `None` until it has
    finished.
    """
    max_run_time_seconds: int | None
    """Maximum allowed run duration in seconds for this job version."""
    interval_start: datetime | None
    """Start of the interval the run processes; `None` for a job without intervals."""
    interval_end: datetime | None
    """End of the interval the run processes; `None` for a job without intervals."""
    pipeline_run_summaries: tuple[PipelineRunSummary, ...]
    """One entry per dlt pipeline name the run reported; a pipeline that ran more than
    once shows its latest report. In no particular order, and empty until telemetry
    has received the reports.
    """
    previous_job_run_id: str | None
    """The upstream run whose completion started this one, through a `job.success:` /
    `job.fail:` trigger or a freshness dependency; `None` for a run started manually,
    by its own schedule, or by a trigger request.
    """
    created_at: datetime
    """When it was created."""

    _identity = ("number", "id")
    _kind = EntityKind.JOB_RUN

    @property
    def finished(self) -> bool:
        """Whether the status can still change.

        Returns:
            True once the run has reached a terminal status.
        """
        return self.status in TERMINAL_STATUSES

    @property
    def failed(self) -> bool:
        """Whether the run finished without succeeding.

        A SKIPPED run is finished but not failed: nothing was attempted.

        Returns:
            True once the run has reached a terminal status other than
            COMPLETED or SKIPPED.
        """
        return self.status in FAILED_STATUSES

    @overload
    def cancel(self: JobRun[Sync]) -> JobRun[Sync]: ...

    @overload
    def cancel(self: JobRun[Async]) -> Awaitable[JobRun[Async]]: ...

    def cancel(self) -> JobRun[Any] | Awaitable[JobRun[Any]]:
        """Ask the platform to stop this run.

        The run moves to ``CANCELLING`` first, and to ``CANCELLED`` once it has
        stopped.

        Returns:
            A fresh snapshot, usually ``CANCELLING`` rather than ``CANCELLED``;
            awaitable in async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            Conflict: The current state does not allow the call, e.g. the workspace is
                archived; `code` and `message` say why.
            NotFound: The run no longer exists.
        """
        workspace_id = self._ctx.require_workspace()
        run_id = self.id
        return self._ctx.run(
            lambda t: t.cancel_run(workspace_id=workspace_id, run_id=run_id),
            JobRun._from_payload,
        )

    @overload
    def logs(self: JobRun[Sync]) -> Iterable[LogLine]: ...

    @overload
    def logs(self: JobRun[Async]) -> AsyncIterable[LogLine]: ...

    def logs(self) -> Iterable[LogLine] | AsyncIterable[LogLine]:
        """Read the run's stored log, oldest line first.

        Lines arrive as the body does, so a long log is never held whole. The
        platform consolidates a run's log after it ends, so this raises until
        that has happened — :meth:`stream_logs` is what follows a live run.
        Platform errors are raised when iteration begins, not by this call.

        Returns:
            An iterable of log lines; async-iterable in async mode.

        Raises:
            NotFound: The run has no stored log, either because it does not
                exist or because it has not been consolidated yet.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()
        run_id = self.id
        return self._ctx.stream(
            lambda t: t.read_logs(
                workspace_id=workspace_id,
                dataplane_url=dataplane_url,
                run_id=run_id,
            ),
            LogLine._from_payload,
        )

    @overload
    def stream_logs(
        self: JobRun[Sync], *, follow: bool = True
    ) -> Iterable[LogLine]: ...

    @overload
    def stream_logs(
        self: JobRun[Async], *, follow: bool = True
    ) -> AsyncIterable[LogLine]: ...

    def stream_logs(
        self, *, follow: bool = True
    ) -> Iterable[LogLine] | AsyncIterable[LogLine]:
        """Follow the run's log live, until the run reaches a terminal status.

        Read from the compute backend rather than from storage, so it works
        while a run is going and stops on its own when the run ends. The
        platform waits up to about a minute for a backend that has not started
        reporting yet. Platform errors are raised when iteration begins, not by
        this call.

        Args:
            follow: Keep reading until the run ends. False replays what the
                backend has already reported and stops, which the platform
                marks only by going quiet — so a slow producer can end it early.

        Returns:
            An iterable of log lines; async-iterable in async mode.

        Raises:
            ApiError: The platform could not follow this run — it is unknown or
                its backend never reported, the backend does not support live
                logs, or the stream failed part-way. It reports these on an
                otherwise successful response, so this can be raised after some
                lines have already been yielded.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()
        run_id = self.id
        return self._ctx.stream(
            lambda t: t.stream_logs(
                workspace_id=workspace_id,
                dataplane_url=dataplane_url,
                run_id=run_id,
                follow=follow,
            ),
            LogLine._from_payload,
        )

    @overload
    def wait(self: JobRun[Sync], *, timeout: float | None = None) -> JobRun[Sync]: ...

    @overload
    def wait(
        self: JobRun[Async], *, timeout: float | None = None
    ) -> Awaitable[JobRun[Async]]: ...

    def wait(
        self, *, timeout: float | None = None
    ) -> JobRun[Any] | Awaitable[JobRun[Any]]:
        """Poll until the run stops changing, and return what it ended as.

        Settles on any terminal status, so a failed or cancelled run returns
        rather than raises — read :attr:`status` to find out which. Checks
        roughly every second at first and backs off to every ten, so a short run
        is noticed almost at once and a long one is not polled thousands of
        times.

        Args:
            timeout: Give up after this many seconds. ``None``, the default,
                waits as long as the run takes.

        Returns:
            A snapshot in a terminal status; awaitable in async mode.

        Raises:
            NotFound: The run no longer exists.
            ScopeMissing: Reached without a workspace in scope.
            ValueError: A negative ``timeout``.
            WaitTimeout: The run was still going when the deadline passed. It is
                unaffected — nothing cancels it — so this can be retried.
        """
        workspace_id = self._ctx.require_workspace()
        run_id = self.id
        return self._ctx.poll(
            lambda t: t.get_run(workspace_id=workspace_id, run_id=run_id),
            JobRun._from_payload,
            lambda run: run.finished,
            timeout=timeout,
            subject=f"run {self.number} had not finished",
        )

    @overload
    def result(self: JobRun[Sync]) -> JobResult: ...

    @overload
    def result(self: JobRun[Async]) -> Awaitable[JobResult]: ...

    def result(self) -> JobResult | Awaitable[JobResult]:
        """Read the structured result this run declared.

        Returns:
            The result; awaitable in async mode.

        Raises:
            NotFound: The run declared none, which is the normal case for a job
                that reports no result — not a sign the run is missing.
            ScopeMissing: Reached without a workspace in scope.
        """
        return JobRuns(self._ctx).result(id=self.id)

    @overload
    def trace(self: JobRun[Sync]) -> JobResultTrace: ...

    @overload
    def trace(self: JobRun[Async]) -> Awaitable[JobResultTrace]: ...

    def trace(self) -> JobResultTrace | Awaitable[JobResultTrace]:
        """Read the whole result this run delivered, trace included.

        Returns:
            The whole result; awaitable in async mode.

        Raises:
            ApiError: The result is too large to serve (``code``
                ``job_result_trace_too_large``); :meth:`result` still reads the
                summary fields.
            NotFound: The run declared no result, which is the normal case for a
                job that reports none — not a sign the run is missing.
            ScopeMissing: Reached without a workspace in scope.
        """
        return JobRuns(self._ctx).trace(id=self.id)

    @staticmethod
    def _from_payload(ctx: _Ctx[Any], payload: DetailedJobRunResponse) -> JobRun[Any]:
        return JobRun._bind(
            ctx,
            JobRun(
                number=payload.number,
                id=str(payload.id),
                job_ref=payload.job.job_ref,
                status=JobRunStatus(str(payload.status)),
                trigger=payload.trigger,
                profile=payload.profile,
                started_at=payload.started_at,
                finished_at=payload.finished_at,
                duration_seconds=payload.duration_seconds,
                max_run_time_seconds=getattr(
                    payload.job_version, "max_run_time_seconds", None
                ),
                interval_start=(
                    payload.interval_start
                    if isinstance(payload.interval_start, datetime)
                    else None
                ),
                interval_end=(
                    payload.interval_end
                    if isinstance(payload.interval_end, datetime)
                    else None
                ),
                pipeline_run_summaries=tuple(
                    PipelineRunSummary._from_payload(summary)
                    for summary in payload.pipeline_run_summaries
                )
                if isinstance(payload.pipeline_run_summaries, list)
                else (),
                previous_job_run_id=(
                    str(payload.previous_job_run_id)
                    if isinstance(payload.previous_job_run_id, UUID)
                    else None
                ),
                created_at=payload.created_at,
            ),
        )


class JobRuns(Collection[M]):
    """The runs of one workspace, or of one job within it."""

    _entity = JobRun

    def _job(self, job_id: str | None) -> str | None:
        return self._ctx.job_id if job_id is None else job_id

    def _listing(
        self, job_id: str | None, number: int | None = None
    ) -> Listing[DetailedJobRunResponse]:
        workspace_id = self._ctx.require_workspace()
        wanted = self._job(job_id)
        return lambda t, limit, offset: t.list_runs(
            workspace_id=workspace_id,
            job_id=wanted,
            number=number,
            limit=limit,
            offset=offset,
        )

    @overload
    def get(self: JobRuns[Sync], *, id: str) -> JobRun[Sync]: ...

    @overload
    def get(self: JobRuns[Async], *, id: str) -> Awaitable[JobRun[Async]]: ...

    def get(self, *, id: str) -> JobRun[Any] | Awaitable[JobRun[Any]]:
        """Return one run by id.

        Job runs are addressed by uuid; to find one by number, filter
        :meth:`list` with ``number``.

        Args:
            id: The run's uuid.

        Returns:
            The run; awaitable in async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            NotFound: No such run in this workspace.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        return self._ctx.run(
            lambda t: t.get_run(workspace_id=workspace_id, run_id=id),
            JobRun._from_payload,
        )

    @overload
    def result(self: JobRuns[Sync], *, id: str) -> JobResult: ...

    @overload
    def result(self: JobRuns[Async], *, id: str) -> Awaitable[JobResult]: ...

    def result(self, *, id: str) -> JobResult | Awaitable[JobResult]:
        """Read one run's declared result, without reading the run itself.

        Args:
            id: The run's uuid.

        Returns:
            The result; awaitable in async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            NotFound: No such run, or it declared no result — the platform
                answers the same either way.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()
        return self._ctx.run(
            lambda t: t.get_job_run_result(
                workspace_id=workspace_id,
                dataplane_url=dataplane_url,
                run_id=id,
            ),
            JobResult._from_payload,
        )

    @overload
    def trace(self: JobRuns[Sync], *, id: str) -> JobResultTrace: ...

    @overload
    def trace(self: JobRuns[Async], *, id: str) -> Awaitable[JobResultTrace]: ...

    def trace(self, *, id: str) -> JobResultTrace | Awaitable[JobResultTrace]:
        """Read one run's whole result, without reading the run itself.

        Args:
            id: The run's uuid.

        Returns:
            The whole result; awaitable in async mode.

        Raises:
            ApiError: The result is too large to serve (``code``
                ``job_result_trace_too_large``); :meth:`result` still reads the
                summary fields.
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            NotFound: No such run, or it declared no result — the platform
                answers the same either way.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        dataplane_url = self._ctx.require_dataplane()

        def parse(_ctx: _Ctx[Any], payload: JobResultTraceResponse) -> JobResultTrace:
            return JobResultTrace(job_run_id=id, result=payload.to_dict())

        return self._ctx.run(
            lambda t: t.get_job_run_result_trace(
                workspace_id=workspace_id,
                dataplane_url=dataplane_url,
                run_id=id,
            ),
            parse,
        )

    @overload
    def latest(self: JobRuns[Sync], *, job_id: str | None = None) -> JobRun[Sync]: ...

    @overload
    def latest(
        self: JobRuns[Async], *, job_id: str | None = None
    ) -> Awaitable[JobRun[Async]]: ...

    def latest(
        self, *, job_id: str | None = None
    ) -> JobRun[Any] | Awaitable[JobRun[Any]]:
        """Return the most recent run.

        Args:
            job_id: Narrow to one job's runs. Omit to use the job in scope, or
                the whole workspace when there is none, which leaves out system
                jobs such as the dashboard.

        Returns:
            The newest run; awaitable in async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            NotFound: Nothing has run yet.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        wanted = self._job(job_id)
        return self._ctx.run(
            lambda t: t.get_latest_run(workspace_id=workspace_id, job_id=wanted),
            JobRun._from_payload,
        )

    @overload
    def count(self: JobRuns[Sync], *, job_id: str | None = None) -> int: ...

    @overload
    def count(self: JobRuns[Async], *, job_id: str | None = None) -> Awaitable[int]: ...

    def count(self, *, job_id: str | None = None) -> int | Awaitable[int]:
        """Return how many runs there have been, without fetching them.

        Args:
            job_id: Narrow to one job's runs. Omit to use the job in scope, or
                the whole workspace when there is none, which leaves out system
                jobs such as the dashboard.

        Returns:
            The count; awaitable in async mode. Saturates at 10,001.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            ScopeMissing: Reached without a workspace in scope.
        """
        return self._ctx.count(self._listing(job_id))

    @overload
    def list(
        self: JobRuns[Sync],
        *,
        job_id: str | None = None,
        number: int | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> Iterable[JobRun[Sync]]: ...

    @overload
    def list(
        self: JobRuns[Async],
        *,
        job_id: str | None = None,
        number: int | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> AsyncIterable[JobRun[Async]]: ...

    def list(
        self,
        *,
        job_id: str | None = None,
        number: int | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> Iterable[JobRun[Any]] | AsyncIterable[JobRun[Any]]:
        """Yield runs newest first, paging lazily.

        Platform errors are raised when iteration begins, not by this call.

        Args:
            job_id: Narrow to one job's runs. Omit to use the job in scope, or
                the whole workspace when there is none, which leaves out system
                jobs such as the dashboard.
            number: Keep only the run with this per-job number. Numbers repeat
                across jobs, so pair it with a job.
            limit: Return at most this many. ``None`` walks to the end, or
                to row 10,100, past which the platform does not page.
            offset: Skip this many, server-side.

        Returns:
            An iterable of runs; async-iterable in async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            ScopeMissing: Reached without a workspace in scope.
            ValueError: A negative ``limit`` or ``offset``.
        """
        return self._ctx.page(
            self._listing(job_id, number),
            JobRun._from_payload,
            limit=limit,
            offset=offset,
        )

    @overload
    def cancel_all(
        self: JobRuns[Sync], *, job_refs: Sequence[str], dry_run: bool = False
    ) -> CancelReport: ...

    @overload
    def cancel_all(
        self: JobRuns[Async], *, job_refs: Sequence[str], dry_run: bool = False
    ) -> Awaitable[CancelReport]: ...

    def cancel_all(
        self, *, job_refs: Sequence[str], dry_run: bool = False
    ) -> CancelReport | Awaitable[CancelReport]:
        """Stop whatever is running for the named jobs.

        Addressed by job, not by run: cancels every pending, starting or
        running run of the named jobs. A ref that names no job, or has nothing
        running, is reported in ``not_running``.

        Args:
            job_refs: The jobs whose runs to stop.
            dry_run: Report what would be cancelled without stopping anything.

        Returns:
            What was cancelled and what was not running; awaitable in async mode.

        Raises:
            ValueError: No job refs were given.
            ScopeMissing: Reached without a workspace in scope.
        """
        if not job_refs:
            raise ValueError("pass at least one job ref to cancel")
        workspace_id = self._ctx.require_workspace()
        refs = list(job_refs)
        return self._ctx.run(
            lambda t: t.cancel_runs(
                workspace_id=workspace_id, job_refs=refs, dry_run=dry_run
            ),
            lambda ctx, payload: CancelReport._from_payload(ctx, payload, refs),
        )
