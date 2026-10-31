"""Shared graph execution setup for single-process worker and multi-process runner."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import structlog

import langgraph_api.logging as lg_logging
from langgraph_api import _checkpointer as api_checkpointer
from langgraph_api.auth.custom import SimpleUser, normalize_user
from langgraph_api.config import (
    BG_JOB_MAX_RETRIES,
    RESUME_DRAINED_RUNS,
    USE_CUSTOM_CHECKPOINTER,
)
from langgraph_api.drain import GraphDrained, ServerRunControl, new_run_control
from langgraph_api.event_streaming.constants import EVENT_STREAMING_V2_CONFIG_KEY
from langgraph_api.feature_flags import (
    IS_POSTGRES_OR_GRPC_BACKEND,
    PREFER_GRPC_CHECKPOINTER,
)
from langgraph_api.graph import restore_dd_trace_context
from langgraph_api.otel_context import restore_otel_trace_context
from langgraph_api.state import patch_interrupt, state_snapshot_to_thread_state
from langgraph_api.stream import astream_state
from langgraph_api.utils import with_user
from langgraph_runtime.database import connect
from langgraph_runtime.retry import RETRIABLE_EXCEPTIONS

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, AsyncIterator

    from langgraph.pregel.debug import CheckpointPayload, TaskResultPayload

    from langgraph_api.asyncio import ValueEvent
    from langgraph_api.schema import Run

logger = structlog.stdlib.get_logger(__name__)

if IS_POSTGRES_OR_GRPC_BACKEND:
    from langgraph_api.grpc.ops.runs import GrpcRetryableException

    GRPC_RETRIABLE_EXCEPTIONS: tuple[type[BaseException], ...] = (
        GrpcRetryableException,
    )
else:
    GRPC_RETRIABLE_EXCEPTIONS = ()

ALL_RETRIABLE_EXCEPTIONS = (
    asyncio.CancelledError,
    *RETRIABLE_EXCEPTIONS,
    *GRPC_RETRIABLE_EXCEPTIONS,
)

# Exceptions after which the run goes back to the queue when drained runs are
# resumed (ResumeDrainedRuns). GraphDrained stays out of
# ALL_RETRIABLE_EXCEPTIONS because a drain isn't a failure.
REQUEUE_EXCEPTIONS = (
    *ALL_RETRIABLE_EXCEPTIONS,
    GraphDrained,
)


@asynccontextmanager
async def set_auth_ctx_for_run(
    run_kwargs: dict, user_id: str | None = None
) -> AsyncGenerator[None, None]:
    try:
        permissions = (
            run_kwargs["config"]["configurable"].get("langgraph_auth_permissions") or []
        )
        user = run_kwargs["config"]["configurable"].get("langgraph_auth_user")
        if not user:
            user = SimpleUser(user_id) if user_id is not None else None
        else:
            user = normalize_user(user)
        run_kwargs["config"]["configurable"]["langgraph_auth_user"] = user
    except Exception:
        logger.warning("Failed to extract user from run kwargs", exc_info=True)
        user = SimpleUser(user_id) if user_id is not None else None
        permissions = None
    if user is not None:
        async with with_user(user, permissions):
            yield None
    else:
        yield None


@dataclass
class RunCheckpointTracker:
    checkpoint: CheckpointPayload | None = None

    def on_checkpoint(self, checkpoint_arg: CheckpointPayload | None) -> None:
        if checkpoint_arg is None:
            logger.warning("Null checkpoint received")
            return
        self.checkpoint = checkpoint_arg

    def on_task_result(self, task_result: TaskResultPayload) -> None:
        if self.checkpoint is None:
            return
        for task in self.checkpoint["tasks"]:
            if task["id"] == task_result["id"]:
                task.update(task_result)
                break


def set_run_logging_context(run: Run, attempt: int) -> None:
    run_id = run["run_id"]
    thread_id = str(run.get("thread_id"))
    lg_logging.set_logging_context(
        {
            "run_id": str(run_id),
            "run_attempt": attempt,
            "thread_id": thread_id,
            "assistant_id": str(run.get("assistant_id")),
            "graph_id": str(_get_graph_id(run)),
            "request_id": str(_get_request_id(run)),
        }
    )


def checkpoint_to_status_dict(
    checkpoint: CheckpointPayload | None,
) -> dict[str, Any] | None:
    """Build the status checkpoint shape Go expects on Done.checkpoint_json."""
    if checkpoint is None:
        return None
    interrupts = {
        t["id"]: [patch_interrupt(i) for i in t["interrupts"]]
        for t in checkpoint.get("tasks", [])
        if t.get("interrupts")
    }
    out: dict[str, Any] = {
        "values": checkpoint.get("values"),
        "next": checkpoint.get("next") or [],
    }
    if interrupts:
        out["interrupts"] = interrupts
    return out


async def fetch_missing_checkpoint(
    run: Run,
    checkpoint: CheckpointPayload | None,
    *,
    temporary: bool,
) -> CheckpointPayload | None:
    if checkpoint is not None or temporary:
        return checkpoint
    if IS_POSTGRES_OR_GRPC_BACKEND:
        from langgraph_api.grpc.ops import Threads  # noqa: PLC0415
    else:
        from langgraph_runtime.ops import Threads  # noqa: PLC0415

    # A forked run's config still pins the checkpoint it started from. Drop the
    # pin so the read returns the state the run left behind; ``checkpoint_ns``
    # stays, since the run writes its checkpoints under it.
    config = run["kwargs"]["config"]
    configurable = dict(config["configurable"])
    configurable.pop("checkpoint_id", None)
    configurable.pop("checkpoint_map", None)
    try:
        async with connect(supports_core_api=PREFER_GRPC_CHECKPOINTER) as conn:
            state_snapshot = await Threads.State.get(
                conn, {**config, "configurable": configurable}, subgraphs=False
            )
            return state_snapshot_to_thread_state(state_snapshot)
    except Exception:
        await logger.aerror(
            "Failed to fetch missing checkpoint",
            exc_info=True,
            run_id=str(run["run_id"]),
        )
        return checkpoint


async def run_resumes_from_checkpoint(run: Run) -> bool:
    """Whether this claim of the run continues from a checkpoint.

    The run continues from the thread's latest checkpoint if it wrote that
    checkpoint itself: an earlier claim of the run got that far, then drained
    or crashed. Postgres records this durably, unlike the Redis attempt and
    drain counters, which can be lost.
    """
    if run["kwargs"].get("temporary", False):
        # Temporary runs have no checkpointer: nothing to resume from.
        return False
    # We don't swallow read errors: the run's input could be re-sent.
    checkpointer = await api_checkpointer.get_checkpointer()
    latest = await checkpointer.aget_tuple(
        {"configurable": {"thread_id": str(run["thread_id"]), "checkpoint_ns": ""}}
    )
    if latest is None:
        return False
    # Another run wrote it when this run hasn't checkpointed yet (e.g. its
    # first claim): the claim sends its input as usual.
    return str(latest.metadata.get("run_id")) == str(run["run_id"])


class DrainPolicy:
    """How the worker treats drained runs: as on main, a drain is an error."""

    requeue_exceptions: tuple[type[BaseException], ...] = ALL_RETRIABLE_EXCEPTIONS

    def is_drain(self, exc: BaseException) -> bool:
        return False

    def counted_drains(self, drains: int) -> int:
        """The drains counted against the retry and drain limits."""
        # The counters can carry drains from when drained runs were resumed:
        # the retry limit counts raw attempts.
        return 0

    async def resumes_from_checkpoint(self, run: Run) -> bool:
        return False

    def new_control(self) -> ServerRunControl | None:
        return None


class ResumeDrainedRuns(DrainPolicy):
    """A drained run goes back to the queue and continues from its checkpoint."""

    requeue_exceptions = REQUEUE_EXCEPTIONS

    def is_drain(self, exc: BaseException) -> bool:
        return isinstance(exc, GraphDrained)

    def counted_drains(self, drains: int) -> int:
        return drains

    async def resumes_from_checkpoint(self, run: Run) -> bool:
        return await run_resumes_from_checkpoint(run)

    def new_control(self) -> ServerRunControl | None:
        return new_run_control()


DRAIN_POLICY: DrainPolicy = (
    ResumeDrainedRuns() if RESUME_DRAINED_RUNS else DrainPolicy()
)


async def fetch_checkpoint_after_failure(
    run: Run,
    failed_attempts: int,
    checkpoint: CheckpointPayload | None,
    *,
    temporary: bool,
) -> CheckpointPayload | None:
    """Return the state a failed, timed-out or cancelled run left behind.

    The tracker only sees checkpoints from ``debug`` events, which Python
    graphs under Protocol v2 don't emit, so a v2 run reaches finalization with
    no checkpoint even if it raised interrupts, and the thread row that
    ``input.respond`` validates against only learns them from this read. Other
    runs keep the tracker's checkpoint. A run over its retry limit never
    started, so there is nothing new to read, and reading could repeat
    whatever crashed it. Drains don't count toward that limit, so callers pass
    the claim's failed attempts rather than its attempt number.
    """
    configurable = run["kwargs"]["config"]["configurable"]
    if failed_attempts > BG_JOB_MAX_RETRIES or not configurable.get(
        EVENT_STREAMING_V2_CONFIG_KEY
    ):
        return checkpoint
    return await fetch_missing_checkpoint(run, checkpoint, temporary=temporary)


async def cleanup_custom_checkpointer_for_run(run_id: str) -> None:
    if not USE_CUSTOM_CHECKPOINTER:
        return
    try:
        from langgraph_api import _checkpointer as api_checkpointer  # noqa: PLC0415

        checkpointer = await api_checkpointer.get_checkpointer()
        await checkpointer.adelete_for_runs([run_id])
    except Exception:
        await logger.aerror(
            "Failed to clean up custom checkpointer data for rolled-back run",
            exc_info=True,
            run_id=run_id,
        )


async def stream_run(
    run: Run,
    attempt: int,
    cancel: ValueEvent,
    tracker: RunCheckpointTracker,
    *,
    control: Any | None = None,
    resume_from_checkpoint: bool = False,
) -> AsyncIterator[tuple[str, Any]]:
    """Yield stream events with worker-parity ambient setup."""
    temporary = run["kwargs"].get("temporary", False)
    set_run_logging_context(run, attempt)
    configurable = run["kwargs"].get("config", {}).get("configurable", {})
    run_id = str(run["run_id"])
    thread_id = str(run["thread_id"])
    async with set_auth_ctx_for_run(run["kwargs"]):
        with (
            restore_otel_trace_context(
                configurable, run_id=run_id, thread_id=thread_id
            ),
            restore_dd_trace_context(configurable, run_id=run_id, thread_id=thread_id),
        ):
            if temporary:
                stream = astream_state(run, attempt, cancel, control=control)
            else:
                stream = astream_state(
                    run,
                    attempt,
                    cancel,
                    on_checkpoint=tracker.on_checkpoint,
                    on_task_result=tracker.on_task_result,
                    control=control,
                    resume_from_checkpoint=resume_from_checkpoint,
                )
            async for mode, payload in stream:
                yield mode, payload


def _get_request_id(run: Run) -> str | None:
    try:
        return run["kwargs"]["config"]["configurable"]["langgraph_request_id"]
    except Exception:
        return None


def _get_graph_id(run: Run) -> str | None:
    try:
        return run["kwargs"]["config"]["configurable"]["graph_id"]
    except Exception:
        logger.info("Failed to get graph_id from run", run_id=str(run["run_id"]))
        return "Unknown"
