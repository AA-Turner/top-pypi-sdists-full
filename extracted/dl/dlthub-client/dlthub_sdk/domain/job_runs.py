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
        BulkCancelResponse,
        DetailedRunResponse,
        PipelineRunSummaryResponse,
    )


class JobRunStatus(StrEnum):
    """Where a run has got to.

    Attributes:
        PENDING: Accepted, not yet started.
        STARTING: Being placed on a compute backend.
        RUNNING: Executing.
        CANCELLING: Cancellation asked for, not yet effective.
        COMPLETED: Finished successfully.
        FAILED: Finished unsuccessfully.
        CANCELLED: Stopped on request.
        SKIPPED: Never ran, because a gate declined it.
        UNKNOWN: A status this SDK version does not know.
    """

    PENDING = "pending"
    STARTING = "starting"
    RUNNING = "running"
    CANCELLING = "cancelling"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"
    UNKNOWN = "unknown"


#: The statuses a run never leaves. Anything else may still change.
TERMINAL_STATUSES = frozenset(
    {
        JobRunStatus.COMPLETED,
        JobRunStatus.FAILED,
        JobRunStatus.CANCELLED,
        JobRunStatus.SKIPPED,
    }
)


@dataclass(frozen=True)
class PipelineRunSummary:
    """One dlt pipeline a run executed, as telemetry reported it.

    A run executes whatever pipelines its script calls, so a job that loads two
    sources reports two. Telemetry fills this in after the pipeline reports, so
    a run that has just started carries none, and a run whose script never
    reached a pipeline carries none for good.

    Attributes:
        pipeline_name: The dlt pipeline's name.
        transaction_id: Identifies this pipeline run in telemetry.
        destination: Where it wrote, when telemetry reported one.
        dataset: The dataset it wrote to, when telemetry reported one.
        status: What the pipeline run ended as. Free-form: it is dlt's own
            wording, not :class:`JobRunStatus`.
        total_rows: Rows loaded, across every table.
        duration_seconds: How long the pipeline ran.
        started_at: When the pipeline began.
        ended_at: When the pipeline finished.
    """

    pipeline_name: str
    transaction_id: str | None
    destination: str | None
    dataset: str | None
    status: str | None
    total_rows: int | None
    duration_seconds: float | None
    started_at: datetime | None
    ended_at: datetime | None

    @staticmethod
    def _from_payload(payload: PipelineRunSummaryResponse) -> PipelineRunSummary:
        return PipelineRunSummary(
            pipeline_name=payload.pipeline_name,
            transaction_id=_narrow.text(payload.transaction_id),
            destination=_narrow.text(payload.destination_name),
            dataset=_narrow.text(payload.dataset_name),
            status=_narrow.text(payload.status),
            total_rows=_narrow.whole(payload.total_rows),
            duration_seconds=_narrow.seconds(payload.duration_ms),
            started_at=_narrow.moment(payload.started_at),
            ended_at=_narrow.moment(payload.finished_at),
        )


@dataclass(frozen=True)
class CancelledRun:
    """One run a bulk cancel stopped.

    Attributes:
        job_ref: The job it belonged to.
        run_id: The run's uuid.
        run_number: Its number within the workspace.
        previous_status: What it was doing when the cancel landed.
    """

    job_ref: str
    run_id: str
    run_number: int
    previous_status: JobRunStatus


@dataclass(frozen=True)
class CancelReport:
    """What a bulk cancel did.

    Attributes:
        cancelled: The runs that were stopped.
        not_running: Job refs that had nothing to stop, which is not an error.
    """

    cancelled: tuple[CancelledRun, ...]
    not_running: tuple[str, ...]

    @staticmethod
    def _from_payload(_ctx: _Ctx[Any], payload: BulkCancelResponse) -> CancelReport:
        return CancelReport(
            cancelled=tuple(
                CancelledRun(
                    job_ref=item.job_ref,
                    run_id=str(item.run_id),
                    run_number=item.run_number,
                    previous_status=JobRunStatus(str(item.previous_status)),
                )
                for item in payload.cancelled
            ),
            not_running=tuple(payload.not_running),
        )


@dataclass(frozen=True, repr=False)
class JobRun(Entity[M]):
    """One execution of a job.

    Attributes:
        number: Its number within the workspace, which is how humans refer to it.
        id: The run's uuid.
        job_ref: The job this ran.
        status: Where it has got to.
        trigger: The trigger that started it.
        profile: The profile it ran under.
        started_at: When it began, or ``None`` if it has not.
        ended_at: When it finished, or ``None`` if it has not.
        duration_seconds: How long it ran, once it has finished.
        timeout_seconds: How long the job's version is allowed to run before the
            platform stops it. What an in-flight run's elapsed time is measured
            against.
        interval_start: Start of the data window this run covers, when the job
            declares one.
        interval_end: End of that window.
        pipelines: The dlt pipelines this run executed, in the order telemetry
            reported them. Empty until telemetry has heard from them, so it
            says nothing about a run still in flight.
        prev_run_id: The run that triggered this one, when a job event did.
            ``None`` for a schedule, a manual trigger, or the first run of a
            chain — so it is how a chain is walked backwards.
        created_at: When the run was created.
    """

    number: int
    id: str
    job_ref: str
    status: JobRunStatus
    trigger: str
    profile: str
    started_at: datetime | None
    ended_at: datetime | None
    duration_seconds: float | None
    timeout_seconds: int | None
    interval_start: datetime | None
    interval_end: datetime | None
    pipelines: tuple[PipelineRunSummary, ...]
    prev_run_id: str | None
    created_at: datetime

    _identity = ("number", "id")
    _kind = EntityKind.JOB_RUN

    @property
    def finished(self) -> bool:
        """Whether the status can still change.

        Returns:
            True once the run has reached a terminal status.
        """
        return self.status in TERMINAL_STATUSES

    @overload
    def cancel(self: JobRun[Sync]) -> JobRun[Sync]: ...

    @overload
    def cancel(self: JobRun[Async]) -> Awaitable[JobRun[Async]]: ...

    def cancel(self) -> JobRun[Any] | Awaitable[JobRun[Any]]:
        """Ask the platform to stop this run.

        Returns:
            A fresh snapshot, usually ``CANCELLING`` rather than ``CANCELLED``;
            awaitable in async mode.

        Raises:
            Conflict: The run has already finished.
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
        platform waits a short while for a backend that has not started
        reporting yet.

        Args:
            follow: Keep reading until the run ends. False replays what the
                backend has already reported and stops, which the platform
                marks only by going quiet — so a slow producer can end it early.

        Returns:
            An iterable of log lines; async-iterable in async mode.

        Raises:
            ApiError: The platform could not follow this run — its backend does
                not support live logs, or the stream failed part-way. It reports
                both on an otherwise successful response, so this can be raised
                after some lines have already been yielded.
            NotFound: No such run in this workspace.
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

    @staticmethod
    def _from_payload(ctx: _Ctx[Any], payload: DetailedRunResponse) -> JobRun[Any]:
        return JobRun._bind(
            ctx,
            JobRun(
                number=payload.number,
                id=str(payload.id),
                job_ref=payload.script.job_ref,
                status=JobRunStatus(str(payload.status)),
                trigger=payload.trigger,
                profile=payload.profile,
                started_at=payload.time_started,
                ended_at=payload.time_ended,
                duration_seconds=payload.duration,
                timeout_seconds=getattr(
                    payload.script_version, "max_run_time_seconds", None
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
                pipelines=tuple(
                    PipelineRunSummary._from_payload(summary)
                    for summary in payload.pipeline_run_summaries
                )
                if isinstance(payload.pipeline_run_summaries, list)
                else (),
                prev_run_id=(
                    str(payload.prev_run_id)
                    if isinstance(payload.prev_run_id, UUID)
                    else None
                ),
                created_at=payload.date_added,
            ),
        )


class JobRuns(Collection[M]):
    """The runs of one workspace, or of one job within it."""

    _entity = JobRun

    def _job(self, job_id: str | None) -> str | None:
        return self._ctx.job_id if job_id is None else job_id

    def _listing(self, job_id: str | None) -> Listing[DetailedRunResponse]:
        workspace_id = self._ctx.require_workspace()
        wanted = self._job(job_id)
        return lambda t, limit, offset: t.list_runs(
            workspace_id=workspace_id, job_id=wanted, limit=limit, offset=offset
        )

    @overload
    def get(self: JobRuns[Sync], *, id: str) -> JobRun[Sync]: ...

    @overload
    def get(self: JobRuns[Async], *, id: str) -> Awaitable[JobRun[Async]]: ...

    def get(self, *, id: str) -> JobRun[Any] | Awaitable[JobRun[Any]]:
        """Return one run by id.

        Job runs are addressed by uuid, not by number; the platform offers no
        lookup by number.

        Args:
            id: The run's uuid.

        Returns:
            The run; awaitable in async mode.

        Raises:
            BadRequest: ``id`` is not a uuid.
            NotFound: No such run in this workspace.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        return self._ctx.run(
            lambda t: t.get_run(workspace_id=workspace_id, run_id=id),
            JobRun._from_payload,
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
                the whole workspace when there is none.

        Returns:
            The newest run; awaitable in async mode.

        Raises:
            BadRequest: ``job_id`` is not a uuid.
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
                the whole workspace when there is none.

        Returns:
            The count; awaitable in async mode. Saturates at 10,001.

        Raises:
            BadRequest: ``job_id`` is not a uuid.
            ScopeMissing: Reached without a workspace in scope.
        """
        return self._ctx.count(self._listing(job_id))

    @overload
    def list(
        self: JobRuns[Sync],
        *,
        job_id: str | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> Iterable[JobRun[Sync]]: ...

    @overload
    def list(
        self: JobRuns[Async],
        *,
        job_id: str | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> AsyncIterable[JobRun[Async]]: ...

    def list(
        self,
        *,
        job_id: str | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> Iterable[JobRun[Any]] | AsyncIterable[JobRun[Any]]:
        """Yield runs newest first, paging lazily.

        Args:
            job_id: Narrow to one job's runs. Omit to use the job in scope, or
                the whole workspace when there is none.
            limit: Return at most this many. ``None`` walks to the end.
            offset: Skip this many, server-side.

        Returns:
            An iterable of runs; async-iterable in async mode.

        Raises:
            BadRequest: ``job_id`` is not a uuid.
            ScopeMissing: Reached without a workspace in scope.
            ValueError: A negative ``limit`` or ``offset``.
        """
        return self._ctx.page(
            self._listing(job_id), JobRun._from_payload, limit=limit, offset=offset
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

        Addressed by job, not by run: the platform cancels each job's active
        run, and reports the jobs that had nothing to stop.

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
            CancelReport._from_payload,
        )
