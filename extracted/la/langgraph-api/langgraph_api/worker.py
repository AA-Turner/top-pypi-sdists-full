import asyncio
import time
import uuid
from contextlib import suppress
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Literal

import structlog
from langgraph.errors import GraphRecursionError
from langgraph.pregel.debug import CheckpointPayload
from starlette.exceptions import HTTPException
from typing_extensions import TypedDict

from langgraph_api.config import (
    BG_JOB_MAX_DRAINS,
    BG_JOB_MAX_RETRIES,
    BG_JOB_TIMEOUT_SECS,
    RESUME_DRAINED_RUNS,
)
from langgraph_api.encryption.context import set_encryption_context
from langgraph_api.errors import UserInterrupt, UserRollback, UserTimeout
from langgraph_api.feature_flags import IS_POSTGRES_OR_GRPC_BACKEND
from langgraph_api.js.errors import RemoteException
from langgraph_api.metadata import incr_runs
from langgraph_api.metrics_otlp import (
    COUNTER_GRAPH_RECURSION_LIMIT_ERROR,
    COUNTER_RUN_ATTEMPT_STARTED,
    COUNTER_RUN_CANCELED_BY_REQUEST,
    COUNTER_RUN_DRAINED,
    COUNTER_RUN_EXCEED_MAX_ATTEMPTS_AT_START,
    COUNTER_RUN_EXCEED_MAX_DRAINS_AT_START,
    COUNTER_RUN_FAILED_AFTER_RETRY,
    COUNTER_RUN_FAILED_RETRIABLE,
    COUNTER_RUN_SET_STATUS_ERROR,
    COUNTER_RUN_SUCCESS,
    LATENCY_RUN_EXECUTION,
    get_otlp_metrics_reporter,
)
from langgraph_api.schema import Run, StreamMode
from langgraph_api.serde import json_dumpb
from langgraph_api.stream import AnyStream, consume
from langgraph_api.worker_runtime import (
    ALL_RETRIABLE_EXCEPTIONS,
    DRAIN_POLICY,
    RunCheckpointTracker,
    cleanup_custom_checkpointer_for_run,
    fetch_checkpoint_after_failure,
    fetch_missing_checkpoint,
    set_run_logging_context,
    stream_run,
)
from langgraph_runtime.database import connect

if IS_POSTGRES_OR_GRPC_BACKEND:
    from langgraph_api.grpc.ops import Runs, Threads
else:
    from langgraph_runtime.ops import Runs, Threads

logger = structlog.stdlib.get_logger(__name__)


class WorkerResult(TypedDict):
    checkpoint: CheckpointPayload | None
    status: str | None
    exception: Exception | None
    run: Run
    webhook: str | None
    run_started_at: str
    run_ended_at: str | None


async def worker(
    run: Run,
    attempt: int,
    main_loop: asyncio.AbstractEventLoop,
    *,
    encryption_context: dict[str, Any] | None = None,
    drains: int = 0,
    control: Any | None = None,
) -> WorkerResult:
    reporter = get_otlp_metrics_reporter()
    run_id = run["run_id"]
    if attempt == 1:
        incr_runs()

    if encryption_context:
        set_encryption_context(encryption_context)

    # Set context before early logs and max-attempt failures.
    set_run_logging_context(run, attempt)

    checkpoint: CheckpointPayload | None = None
    exception: Exception | asyncio.CancelledError | None = None
    status: str | None = None
    webhook = run["kwargs"].get("webhook", None)
    request_created_at: int | None = run["kwargs"]["config"]["configurable"].get(
        "__request_start_time_ms__"
    )
    after_seconds = run["kwargs"]["config"]["configurable"].get("__after_seconds__", 0)
    run_started_at_dt = datetime.now(UTC)
    run_started_at = run_started_at_dt.isoformat()
    run_ended_at_dt: datetime | None = None
    run_ended_at: str | None = None

    # Note that "created_at" is inclusive of the `after_seconds`
    run_creation_ms = (
        int(
            ((run["created_at"].timestamp() - after_seconds) * 1_000)
            - request_created_at
        )
        if request_created_at is not None
        else None
    )
    temporary = run["kwargs"].get("temporary", False)
    resumable = run["kwargs"].get("resumable", False)
    run_created_at_dt = run["created_at"]
    run_created_at = run["created_at"].isoformat()
    thread_id = str(run.get("thread_id"))
    reporter.inc_counter(
        COUNTER_RUN_ATTEMPT_STARTED,
    )
    run_stream_started_at_dt = datetime.now(UTC)
    await logger.ainfo(
        "Starting background run",
        run_started_at=run_started_at,
        run_creation_ms=run_creation_ms,
        run_queue_ms=ms(run_started_at_dt, run["created_at"]),
        run_stream_start_ms=ms(run_stream_started_at_dt, run_started_at_dt),
        temporary=temporary,
        resumable=resumable,
    )

    # Wrap the graph execution to separate user errors from server errors
    async def wrap_user_errors(
        stream: AnyStream,
        run_id: str | uuid.UUID,
        resumable: bool,
        stream_modes: set[StreamMode],
    ):
        try:
            await consume(
                stream, run_id, resumable, stream_modes, thread_id=run["thread_id"]
            )
        except Exception as e:
            if not isinstance(
                e, UserRollback | UserInterrupt
            ) and not DRAIN_POLICY.is_drain(e):
                logger.exception(
                    f"Run encountered an error in graph: {type(e)}({e})",
                    run_id=str(run_id),
                    thread_id=thread_id,
                )
            if isinstance(e, TimeoutError):
                raise UserTimeout(e) from e
            raise

    tracker = RunCheckpointTracker()
    async with Runs.enter(run_id, run["thread_id"], main_loop, resumable) as done:
        claim = RunClaim.from_counters(attempt, DRAIN_POLICY.counted_drains(drains))
        # attempt the run
        try:
            exceeded = claim.exceeded_limit()
            if exceeded == "retries":
                reporter.inc_counter(COUNTER_RUN_EXCEED_MAX_ATTEMPTS_AT_START)
                await logger.aerror(
                    "Run exceeded max attempts",
                    run_id=str(run["run_id"]),
                    run_completed_in_ms=(
                        int((time.time() * 1_000) - request_created_at)
                        if request_created_at is not None
                        else None
                    ),
                )

                error_message = (
                    f"Run {run['run_id']} exceeded max attempts ({BG_JOB_MAX_RETRIES}).\n\n"
                    "This usually means the pod processing the run became unhealthy and the run was re-queued repeatedly. "
                    "Check for OOM kills, pod restarts, liveness/readiness probe failures, or other signs of pod instability "
                    "in your deployment's logs and metrics."
                    + (
                        " For temporary (threadless) runs, drains count as "
                        "attempts too.\n\n"
                        if RESUME_DRAINED_RUNS
                        else "\n\n"
                    )
                )

                raise RuntimeError(error_message)
            if exceeded == "drains":
                reporter.inc_counter(COUNTER_RUN_EXCEED_MAX_DRAINS_AT_START)
                await logger.aerror(
                    "Run exceeded max drains",
                    run_id=str(run["run_id"]),
                    drains=claim.drains,
                )

                raise RuntimeError(
                    f"Run {run['run_id']} was drained {claim.drains} times without finishing, "
                    f"more than BG_JOB_MAX_DRAINS ({BG_JOB_MAX_DRAINS}) allows. "
                    "This means the graph keeps requesting drains instead of completing; "
                    "check what is calling request_drain() in the graph or how often pods "
                    "are being stopped mid-run."
                )
            # Whether this claim continues an earlier one of the same run is
            # read from Postgres, not from the counters: Redis holds only
            # ephemeral data and can lose them between claims.
            resume = await DRAIN_POLICY.resumes_from_checkpoint(run)
            stream_modes: set[StreamMode] = set(run["kwargs"].get("stream_mode", []))
            await asyncio.wait_for(
                wrap_user_errors(
                    stream_run(
                        run,
                        attempt,
                        done,
                        tracker=tracker,
                        control=control,
                        # Continue from the run's own latest checkpoint
                        # instead of re-sending its original input or command.
                        resume_from_checkpoint=resume,
                    ),
                    run_id,
                    resumable,
                    stream_modes,
                ),
                BG_JOB_TIMEOUT_SECS,
            )
        except (Exception, asyncio.CancelledError) as ee:
            exception = ee
        except BaseException as eee:
            await logger.aerror(
                "Bubbling failed background run",
                run_id=str(run_id),
                exception_type=str(type(eee)),
                exception=str(eee),
            )
            raise
        finally:
            # Tracker is mutated during streaming. Copy after wait_for so
            # error/timeout paths still have the last checkpoint for webhooks.
            checkpoint = tracker.checkpoint
            run_ended_at_dt = datetime.now(UTC)
            run_ended_at = run_ended_at_dt.isoformat()

        # handle exceptions and set status
        async with connect() as conn:
            graph_id = run["kwargs"]["config"]["configurable"]["graph_id"]
            log_info = {
                "run_id": str(run_id),
                "run_attempt": attempt,
                "run_created_at": run_created_at,
                "run_started_at": run_started_at,
                "run_ended_at": run_ended_at,
                "run_exec_ms": ms(run_ended_at_dt, run_started_at_dt),
                "run_completed_in_ms": (
                    int((run_ended_at_dt.timestamp() * 1_000) - request_created_at)
                    if request_created_at is not None
                    else None
                ),
                "run_wait_time_ms": ms(run_started_at_dt, run_created_at_dt),
            }

            if exception is None:
                status = "success"
                reporter.inc_counter(COUNTER_RUN_SUCCESS)

                await logger.ainfo(
                    "Background run succeeded",
                    **log_info,
                )
                # Python graphs under Protocol v2 never feed the tracker, nor does a
                # retry that resumed right at the end
                if checkpoint is None and not temporary:
                    await logger.ainfo(
                        "Fetching missing checkpoint for webhook",
                        run_id=str(run_id),
                        run_attempt=attempt,
                    )
                    checkpoint = await fetch_missing_checkpoint(
                        run, checkpoint, temporary=temporary
                    )
                if not temporary:
                    await Threads.set_joint_status(
                        conn,
                        run["thread_id"],
                        run_id,
                        status,
                        graph_id=graph_id,
                        checkpoint=checkpoint,
                    )
            elif isinstance(exception, TimeoutError):
                status = "timeout"
                reporter.inc_counter(
                    COUNTER_RUN_FAILED_AFTER_RETRY,
                    attributes={"status": status},
                )
                await logger.awarning(
                    "Background run timed out. To increase the timeout, set the BG_JOB_TIMEOUT_SECS environment variable (integer, defaults to 86400).",
                    **log_info,
                )
                if not temporary:
                    await Threads.set_joint_status(
                        conn,
                        run["thread_id"],
                        run_id,
                        status,
                        graph_id=graph_id,
                        checkpoint=await fetch_checkpoint_after_failure(
                            run, claim.failed_attempts, checkpoint, temporary=temporary
                        ),
                        exception=exception,
                    )
            elif isinstance(exception, UserRollback):
                status = "rollback"
                reporter.inc_counter(
                    COUNTER_RUN_CANCELED_BY_REQUEST,
                    attributes={"status": status},
                )
                if not temporary:
                    try:
                        await Threads.set_joint_status(
                            conn,
                            run["thread_id"],
                            run_id,
                            status,
                            graph_id=graph_id,
                            checkpoint=None,
                            exception=exception,
                        )
                        await logger.ainfo(
                            "Background run rolled back",
                            reason=str(exception),
                            **log_info,
                        )
                    except HTTPException as e:
                        if e.status_code == 404:
                            await logger.ainfo(
                                "Ignoring rollback error for missing run",
                                **log_info,
                            )
                        else:
                            raise

                    # Clean up the custom checkpointer's data for this run.
                    await cleanup_custom_checkpointer_for_run(str(run_id))

                    checkpoint = None  # reset the checkpoint
            elif isinstance(exception, UserInterrupt):
                status = "interrupted"
                reporter.inc_counter(
                    COUNTER_RUN_CANCELED_BY_REQUEST,
                    attributes={"status": status},
                )
                await logger.ainfo(
                    "Background run interrupted",
                    reason=str(exception),
                    **log_info,
                )
                if not temporary:
                    await Threads.set_joint_status(
                        conn,
                        run["thread_id"],
                        run_id,
                        status,
                        graph_id,
                        await fetch_checkpoint_after_failure(
                            run, claim.failed_attempts, checkpoint, temporary=temporary
                        ),
                        exception,
                    )
            elif DRAIN_POLICY.is_drain(exception):
                status = "retry"
                # A drained run isn't finished; it notifies on completion.
                webhook = None
                reporter.inc_counter(
                    COUNTER_RUN_DRAINED, attributes={"temporary": temporary}
                )
                # Don't update thread status: the run continues on the next
                # worker that claims it.
                try:
                    if temporary:
                        # No checkpointer, so nothing to resume from: the run
                        # restarts from its input, which is a retry, and counts
                        # against the retry limit like one.
                        await logger.awarning(
                            "Temporary run drained; it has no checkpoint, so it "
                            "restarts from its input and counts as a failed attempt",
                            reason=exception.reason,
                            **log_info,
                        )
                        await Runs.set_status(conn, run_id, "pending")
                    else:
                        await logger.ainfo(
                            "Run drained at a superstep boundary; re-queued to resume",
                            reason=exception.reason,
                            **log_info,
                        )
                        # Requeue counts the drain before making the run
                        # claimable, so the drain doesn't use up a retry.
                        await Runs.requeue(conn, run_id, exception.reason or "")
                except Exception:
                    reporter.inc_counter(COUNTER_RUN_SET_STATUS_ERROR)
                    raise
            elif isinstance(exception, ALL_RETRIABLE_EXCEPTIONS):
                status = "retry"
                reporter.inc_counter(COUNTER_RUN_FAILED_RETRIABLE)
                await logger.awarning(
                    f"Background run failed, will retry. Exception: {type(exception)}({exception})",
                    **log_info,
                )
                # Don't update thread status yet.
                # Apply this even for temporary runs, so we retry
                try:
                    await Runs.set_status(conn, run_id, "pending")
                except Exception:
                    reporter.inc_counter(COUNTER_RUN_SET_STATUS_ERROR)
                    raise
            else:
                status = "error"
                reporter.inc_counter(
                    COUNTER_RUN_FAILED_AFTER_RETRY,
                    attributes={"status": status},
                )
                if isinstance(exception, GraphRecursionError):
                    reporter.inc_counter(COUNTER_GRAPH_RECURSION_LIMIT_ERROR)

                # Convert UserTimeout to TimeoutError for customers
                if isinstance(exception, UserTimeout):
                    exception = exception.timeout_error

                # Sole emitter of the terminal `error` stream event: consume()
                # re-raises without emitting, so a retriable attempt stays silent
                # until the run actually fails. Emit before the status write so raw
                # SSE clients (no status fallback) see it even if that write fails.
                # Resumable runs cache it so `Last-Event-ID` replays end with it too.
                with suppress(Exception):
                    await Runs.Stream.publish(
                        run_id,
                        "error",
                        json_dumpb(exception),
                        thread_id=run["thread_id"],
                        resumable=resumable,
                    )

                # We're outside the original `except` block, so build exc_info manually.
                # This preserves traceback logging for non-remote exceptions.
                exc_info = None
                if not isinstance(exception, RemoteException):
                    exc_info = (
                        type(exception),
                        exception,
                        exception.__traceback__,
                    )

                await logger.aerror(
                    f"Background run failed. Exception: {type(exception)}({exception})",
                    exc_info=exc_info,
                    **log_info,
                )
                if not temporary:
                    await Threads.set_joint_status(
                        conn,
                        run["thread_id"],
                        run_id,
                        status,
                        graph_id,
                        await fetch_checkpoint_after_failure(
                            run, claim.failed_attempts, checkpoint, temporary=temporary
                        ),
                        exception,
                    )

            # delete thread if it's temporary and we don't want to retry
            if temporary and not isinstance(exception, DRAIN_POLICY.requeue_exceptions):
                await Threads.delete(conn, run["thread_id"])

            reporter.record_latency(
                LATENCY_RUN_EXECUTION,
                float(ms(run_ended_at_dt, run_started_at_dt)) / 1000.0,
                attributes={"status": status or "unknown"},
            )

        if isinstance(exception, DRAIN_POLICY.requeue_exceptions):
            if DRAIN_POLICY.is_drain(exception):
                await logger.ainfo("Run drained; will resume when re-claimed")
            else:
                await logger.awarning("RETRYING", exc_info=exception)
            # re-raise so Runs.enter knows not to mark as done
            # Runs.enter will catch the exception, but what triggers the retry
            # is setting the status to "pending"
            raise exception

    return WorkerResult(
        checkpoint=checkpoint,
        status=status,
        exception=exception,
        run=run,
        webhook=webhook,
        run_started_at=run_started_at,
        run_ended_at=run_ended_at,
    )


@dataclass(frozen=True)
class RunClaim:
    """A run's claim counters, as of one claim.

    Built via `from_counters` so the clamping of the drain count to the
    claims before this one lives in one place.
    """

    attempt: int
    drains: int

    @classmethod
    def from_counters(cls, attempt: int, drains: int) -> "RunClaim":
        """Clamp the drain count to the claims before this one.

        The attempt and drain counters are stored separately, so a stale
        drain value can't be allowed to exceed the claims that came before
        this one.
        """
        return cls(
            attempt=attempt,
            drains=max(0, min(drains, attempt - 1)),
        )

    @property
    def failed_attempts(self) -> int:
        """Claims that were not cooperative handoffs."""
        return self.attempt - self.drains

    def exceeded_limit(self) -> Literal["retries", "drains"] | None:
        """Return which limit this claim exceeds, if any.

        Drains are handoffs, not failures: only failed attempts (claims that
        were not drains) count against the retry limit. A run fails once it
        has drained more than BG_JOB_MAX_DRAINS times.
        """
        if self.failed_attempts > BG_JOB_MAX_RETRIES:
            return "retries"
        # A claim that never drained can't exceed the drain limit (also keeps
        # a nonsensical negative limit from failing flag-off claims, which
        # carry no drains at all).
        if self.drains > 0 and self.drains > BG_JOB_MAX_DRAINS:
            return "drains"
        return None


def ms(after: datetime, before: datetime) -> int:
    return int((after - before).total_seconds() * 1000)
