"""Python executor client for the Go Orchestrator service."""

from __future__ import annotations

import asyncio
import logging
import logging.config
import os
import sys
from contextlib import aclosing, suppress
from typing import TYPE_CHECKING, Any

os.environ.setdefault("DISABLE_TRUSTSTORE", "true")

import grpc.aio as grpc_aio
from langgraph_grpc_common.proto import orchestrator_pb2, orchestrator_pb2_grpc

from langgraph_api.asyncio import ValueEvent
from langgraph_api.encryption.context import set_encryption_context
from langgraph_api.errors import UserInterrupt, UserRollback
from langgraph_api.graph import collect_graphs_from_env
from langgraph_api.grpc.ops import encryption_context_from_proto
from langgraph_api.grpc.ops.runs import proto_to_run
from langgraph_api.serde import json_dumpb
from langgraph_api.worker_runtime import (
    ALL_RETRIABLE_EXCEPTIONS,
    RunCheckpointTracker,
    checkpoint_to_status_dict,
    cleanup_custom_checkpointer_for_run,
    fetch_checkpoint_after_failure,
    fetch_missing_checkpoint,
    stream_run,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from langgraph_api.schema import Run

logger = logging.getLogger("langgraph_api.executor")

ACTION_INTERRUPT = "interrupt"
ACTION_ROLLBACK = "rollback"

STATUS_SUCCESS = "success"
STATUS_ERROR = "error"
STATUS_RETRY = "retry"

# Cap consecutive soft failures so a dead orchestrator doesn't spin forever.
_MAX_DISPATCH_FAILURES = 20
_BACKOFF_INITIAL_SECS = 0.05
_BACKOFF_MAX_SECS = 5.0
# Matches the Go processExecutor connect wait so a dead address fails closed.
_CHANNEL_READY_TIMEOUT_SECS = 60.0


def _exception_dict(exc: BaseException) -> dict[str, Any]:
    return {"error": type(exc).__name__, "message": str(exc)}


def _unwrap_cancel(exc: BaseException) -> BaseException:
    # Match stream consume / asyncio.wait_if_not_done: TaskGroup failures land
    # as ExceptionGroup; classify the first child, not the group.
    if isinstance(exc, ExceptionGroup):
        exc = exc.exceptions[0]
    if isinstance(exc, asyncio.CancelledError) and exc.args:
        inner = exc.args[0]
        if isinstance(inner, BaseException):
            return inner
    return exc


def _done_msg(
    *,
    status: str,
    message: str = "",
    checkpoint: dict[str, Any] | None = None,
    exception: dict[str, Any] | None = None,
) -> orchestrator_pb2.ExecutorMessage:
    return orchestrator_pb2.ExecutorMessage(
        done=orchestrator_pb2.Done(
            status=status,
            message=message,
            checkpoint_json=json_dumpb(checkpoint) if checkpoint is not None else b"",
            exception_json=json_dumpb(exception) if exception is not None else b"",
        )
    )


async def _try_write(call: Any, msg: orchestrator_pb2.ExecutorMessage) -> bool:
    """Write one message. Returns False if the stream is gone."""
    try:
        await call.write(msg)
        return True
    except grpc_aio.AioRpcError:
        logger.warning("Dispatch write failed", exc_info=True)
        return False


async def _failure_checkpoint(
    run: Run,
    failed_attempts: int,
    tracker: RunCheckpointTracker,
    temporary: bool,
) -> dict[str, Any] | None:
    checkpoint = await fetch_checkpoint_after_failure(
        run, failed_attempts, tracker.checkpoint, temporary=temporary
    )
    return checkpoint_to_status_dict(checkpoint)


async def _run_graph(
    run: Run,
    attempt: int,
    failed_attempts: int,
    cancel: ValueEvent,
    encryption_context: dict[str, Any] | None = None,
) -> AsyncIterator[orchestrator_pb2.ExecutorMessage]:
    # Claimed run context for custom encryption key derivation. Always set:
    # this task is reused across dispatches, unlike worker.py. Do not log;
    # metadata is tenant/user key material.
    set_encryption_context(encryption_context or {})
    tracker = RunCheckpointTracker()
    temporary = run["kwargs"].get("temporary", False)
    try:
        async for mode, payload in stream_run(run, attempt, cancel, tracker=tracker):
            packet = await asyncio.to_thread(json_dumpb, payload)
            yield orchestrator_pb2.ExecutorMessage(
                chunk=orchestrator_pb2.Chunk(mode=mode, packet=packet)
            )
        checkpoint = await fetch_missing_checkpoint(
            run, tracker.checkpoint, temporary=temporary
        )
        yield _done_msg(
            status=STATUS_SUCCESS,
            checkpoint=checkpoint_to_status_dict(checkpoint),
        )
    except (Exception, asyncio.CancelledError) as exc:
        exc = _unwrap_cancel(exc)
        # UserRollback subclasses UserInterrupt; check rollback first so
        # cleanup runs and we do not treat a rollback as an interrupt.
        if isinstance(exc, UserRollback):
            await cleanup_custom_checkpointer_for_run(str(run["run_id"]))
            yield _done_msg(status=STATUS_ERROR, message=str(exc))
            return
        if isinstance(exc, UserInterrupt):
            yield _done_msg(
                status=STATUS_ERROR,
                message=str(exc),
                checkpoint=await _failure_checkpoint(
                    run, failed_attempts, tracker, temporary
                ),
            )
            return
        if isinstance(exc, ALL_RETRIABLE_EXCEPTIONS):
            yield _done_msg(
                status=STATUS_RETRY,
                message=str(exc),
                exception=_exception_dict(exc),
            )
            return
        yield _done_msg(
            status=STATUS_ERROR,
            message=str(exc),
            exception=_exception_dict(exc),
            checkpoint=await _failure_checkpoint(
                run, failed_attempts, tracker, temporary
            ),
        )


async def _watch_cancel(call: Any, cancel: ValueEvent) -> None:
    """Read orchestrator cancel messages until the send-side half-closes.

    Clean EOF means the orchestrator is done sending (normal after ExecuteRequest);
    it is not a cancellation. Transport errors still interrupt the graph.
    """
    try:
        while (msg := await call.read()) is not grpc_aio.EOF:
            if msg.HasField("cancel"):
                action = msg.cancel.action or ACTION_INTERRUPT
                if action == ACTION_ROLLBACK:
                    cancel.set(UserRollback())
                else:
                    cancel.set(UserInterrupt())
    except asyncio.CancelledError:
        raise
    except Exception:
        logger.warning("Dispatch cancel watch failed", exc_info=True)
        cancel.set(UserInterrupt())


async def _dispatch_once(stub: orchestrator_pb2_grpc.OrchestratorStub) -> bool:
    """Offer one capacity slot.

    Returns True when the slot was used successfully (run finished, error Done
    delivered, or Release) so the caller can immediately re-offer capacity.
    Returns False for soft failures (empty EOF, open/read errors, mid-run write
    failures) so the caller can back off.
    """
    try:
        call = stub.Dispatch()
        first = await call.read()
    except grpc_aio.AioRpcError:
        logger.warning("Failed to open Dispatch stream", exc_info=True)
        return False

    if first is grpc_aio.EOF:
        logger.info("Dispatch closed without assignment")
        return False

    if first.HasField("release"):
        with suppress(grpc_aio.AioRpcError):
            await call.done_writing()
        return True

    if not first.HasField("execute") or not first.execute.HasField("run"):
        await _try_write(
            call, _done_msg(status=STATUS_ERROR, message="expected ExecuteRequest")
        )
        with suppress(grpc_aio.AioRpcError):
            await call.done_writing()
        return True

    execute = first.execute
    cancel = ValueEvent()
    watch = asyncio.create_task(_watch_cancel(call, cancel))
    write_failed = False
    try:
        try:
            run = proto_to_run(execute.run)
        except Exception as exc:
            logger.exception("Failed to map ExecuteRequest run")
            await _try_write(
                call,
                _done_msg(
                    status=STATUS_ERROR,
                    message=str(exc),
                    exception=_exception_dict(exc),
                ),
            )
            return True

        async with aclosing(
            _run_graph(
                run,
                execute.attempt,
                execute.failed_attempts,
                cancel,
                encryption_context=encryption_context_from_proto(
                    execute.encryption_context
                )
                or None,
            )
        ) as results:
            async for result in results:
                if not await _try_write(call, result):
                    cancel.set(UserInterrupt())
                    write_failed = True
                    break
    finally:
        if not cancel.is_set():
            cancel.set(UserInterrupt())
        # Half-close first so the cancel watcher sees clean EOF; do not
        # cancel the watch task (that cancels the whole Dispatch RPC in grpc.aio).
        with suppress(grpc_aio.AioRpcError):
            await call.done_writing()
        with suppress(asyncio.CancelledError, grpc_aio.AioRpcError):
            await watch
    return not write_failed


async def _bootstrap() -> None:
    from langgraph_api import _checkpointer as api_checkpointer  # noqa: PLC0415
    from langgraph_api import store as api_store  # noqa: PLC0415
    from langgraph_api.asyncio import set_event_loop  # noqa: PLC0415

    # ASGITransport hops loopback onto _MAIN_LOOP (same as runtime lifespan).
    # The executor does not enter API lifespan, so set the pointer here on
    # the loop that starts the pools and later runs stream_run.
    # get_client() with no URL imports langgraph_api.server itself.
    set_event_loop(asyncio.get_running_loop())

    from langgraph_runtime import database  # noqa: PLC0415

    await database.start_pool()
    await api_store.collect_store_from_env()
    await api_checkpointer.start_checkpointer()
    await collect_graphs_from_env(register=True, allow_js=False)


def _parse_bind(bind: str) -> str:
    if bind.startswith("unix:") and not bind.startswith("unix://"):
        return "unix://" + bind[len("unix:") :]
    return bind


def _configure_logging() -> None:
    # Same shape as api/logging.json (structlog Formatter → stdout).
    logging.config.dictConfig(
        {
            "version": 1,
            "incremental": False,
            "disable_existing_loggers": False,
            "formatters": {
                "simple": {"class": "langgraph_api.logging.Formatter"},
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "simple",
                    "stream": "ext://sys.stdout",
                }
            },
            "root": {"handlers": ["console"]},
        }
    )


async def amain() -> None:
    _configure_logging()
    from langgraph_api import config  # noqa: PLC0415

    # Role flag before bootstrap so graph registration / other shared code
    # can skip API-only work (mirrors queue_entrypoint + IS_QUEUE_ENTRYPOINT).
    config.IS_EXECUTOR_ENTRYPOINT = True

    address = _parse_bind(os.environ.get("LANGGRAPH_ORCHESTRATOR_ADDRESS", "").strip())
    if not address:
        logger.error("LANGGRAPH_ORCHESTRATOR_ADDRESS is required")
        sys.exit(1)

    max_msg = int(os.environ.get("MAX_STREAM_CHUNK_SIZE_BYTES", 128 * 1024 * 1024))
    max_msg = max_msg + 1024 * 1024  # envelope headroom

    await _bootstrap()

    channel = grpc_aio.insecure_channel(
        address,
        options=[
            ("grpc.max_send_message_length", max_msg),
            ("grpc.max_receive_message_length", max_msg),
            ("grpc.keepalive_permit_without_calls", 1),
        ],
    )
    try:
        async with asyncio.timeout(_CHANNEL_READY_TIMEOUT_SECS):
            await channel.channel_ready()
    except TimeoutError:
        logger.exception(
            "Timed out waiting for Orchestrator channel at %s after %.0fs",
            address,
            _CHANNEL_READY_TIMEOUT_SECS,
        )
        await channel.close()
        sys.exit(1)

    logger.info("Executor connected to Orchestrator at %s", address)
    stub = orchestrator_pb2_grpc.OrchestratorStub(channel)
    failures = 0
    exhausted = False
    try:
        while failures < _MAX_DISPATCH_FAILURES:
            try:
                used = await _dispatch_once(stub)
            except Exception:
                logger.exception("Unexpected dispatch error")
                used = False
            if used:
                failures = 0
                continue
            failures += 1
            delay = min(
                _BACKOFF_INITIAL_SECS * (2 ** (failures - 1)),
                _BACKOFF_MAX_SECS,
            )
            await asyncio.sleep(delay)
        exhausted = True
        logger.error(
            "Exceeded %d consecutive dispatch failures; exiting",
            _MAX_DISPATCH_FAILURES,
        )
    finally:
        await channel.close()
    if exhausted:
        sys.exit(1)


def main() -> None:
    with suppress(KeyboardInterrupt):
        asyncio.run(amain())


if __name__ == "__main__":
    main()
