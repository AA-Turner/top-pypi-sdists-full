"""gRPC Runner service: graph load + astream for the Go queue worker.

Bind address from LANGGRAPH_RUNNER_BIND:
  unix:///path/to.sock  (local process worker)
  host:port             (sandbox / TCP)
"""

from __future__ import annotations

import asyncio
import logging
import logging.config
import os
import sys
from contextlib import suppress
from typing import TYPE_CHECKING, Any

os.environ.setdefault("DISABLE_TRUSTSTORE", "true")

import grpc.aio as grpc_aio
from grpc_health.v1 import health, health_pb2, health_pb2_grpc
from langgraph_grpc_common.proto import runner_pb2, runner_pb2_grpc

from langgraph_api.asyncio import ValueEvent
from langgraph_api.errors import UserInterrupt, UserRollback
from langgraph_api.graph import collect_graphs_from_env
from langgraph_api.grpc.ops.runs import proto_to_run
from langgraph_api.serde import json_dumpb
from langgraph_api.worker_runtime import (
    ALL_RETRIABLE_EXCEPTIONS,
    RunCheckpointTracker,
    checkpoint_to_status_dict,
    cleanup_custom_checkpointer_for_run,
    fetch_missing_checkpoint,
    stream_run,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from langgraph_api.schema import Run

logger = logging.getLogger("langgraph_api.runner")

ACTION_INTERRUPT = "interrupt"
ACTION_ROLLBACK = "rollback"

STATUS_SUCCESS = "success"
STATUS_ERROR = "error"
STATUS_RETRY = "retry"


def _exception_dict(exc: BaseException) -> dict[str, Any]:
    return {"error": type(exc).__name__, "message": str(exc)}


def _unwrap_cancel(exc: BaseException) -> BaseException:
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
) -> runner_pb2.ExecuteServerMessage:
    return runner_pb2.ExecuteServerMessage(
        done=runner_pb2.Done(
            status=status,
            message=message,
            checkpoint_json=json_dumpb(checkpoint) if checkpoint is not None else b"",
            exception_json=json_dumpb(exception) if exception is not None else b"",
        )
    )


async def _run_graph(
    run: Run,
    attempt: int,
    cancel: ValueEvent,
) -> AsyncIterator[runner_pb2.ExecuteServerMessage]:
    tracker = RunCheckpointTracker()
    temporary = run["kwargs"].get("temporary", False)
    try:
        async for mode, payload in stream_run(run, attempt, cancel, tracker=tracker):
            packet = await asyncio.to_thread(json_dumpb, payload)
            yield runner_pb2.ExecuteServerMessage(
                chunk=runner_pb2.Chunk(mode=mode, packet=packet)
            )
        checkpoint = await fetch_missing_checkpoint(
            run, tracker.checkpoint, temporary=temporary
        )
        yield _done_msg(
            status=STATUS_SUCCESS,
            checkpoint=checkpoint_to_status_dict(checkpoint),
        )
    except Exception as exc:
        exc = _unwrap_cancel(exc)
        checkpoint = checkpoint_to_status_dict(tracker.checkpoint)
        if isinstance(exc, UserInterrupt):
            yield _done_msg(
                status=STATUS_ERROR,
                message=str(exc),
                checkpoint=checkpoint,
            )
            return
        if isinstance(exc, UserRollback):
            await cleanup_custom_checkpointer_for_run(str(run["run_id"]))
            yield _done_msg(status=STATUS_ERROR, message=str(exc))
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
            checkpoint=checkpoint,
        )


class RunnerServicer(runner_pb2_grpc.RunnerServicer):
    def __init__(self) -> None:
        self._busy = False
        self._lock = asyncio.Lock()

    async def Execute(
        self,
        request_iterator: AsyncIterator[runner_pb2.ExecuteClientMessage],
        context: grpc_aio.ServicerContext,
    ) -> AsyncIterator[runner_pb2.ExecuteServerMessage]:
        async with self._lock:
            if self._busy:
                yield _done_msg(status=STATUS_ERROR, message="runner is busy")
                return
            self._busy = True

        cancel = ValueEvent()
        try:
            first = await anext(request_iterator, None)
            if first is None or not first.HasField("execute"):
                yield _done_msg(
                    status=STATUS_ERROR,
                    message="expected ExecuteRequest as first message",
                )
                return

            execute = first.execute
            if not execute.HasField("run"):
                yield _done_msg(
                    status=STATUS_ERROR,
                    message="expected Run on ExecuteRequest",
                )
                return

            run = proto_to_run(execute.run)
            attempt = int(execute.attempt or 1)

            async def _watch_cancel() -> None:
                async for msg in request_iterator:
                    if msg.HasField("cancel"):
                        action = msg.cancel.action or ACTION_INTERRUPT
                        if action == ACTION_ROLLBACK:
                            cancel.set(UserRollback())
                        else:
                            cancel.set(UserInterrupt())

            watch = asyncio.create_task(_watch_cancel())
            try:
                async for out in _run_graph(run, attempt, cancel):
                    yield out
            finally:
                watch.cancel()
                with suppress(asyncio.CancelledError):
                    await watch
        finally:
            async with self._lock:
                self._busy = False


async def _bootstrap() -> None:
    from langgraph_api import _checkpointer as api_checkpointer  # noqa: PLC0415
    from langgraph_api import store as api_store  # noqa: PLC0415
    from langgraph_runtime import database  # noqa: PLC0415

    await database.start_pool()
    await api_store.collect_store_from_env()
    await api_checkpointer.start_checkpointer()
    await collect_graphs_from_env(register=True, allow_js=False)


def _parse_bind(bind: str) -> str:
    """Return a grpc aio add_insecure_port target string."""
    if bind.startswith("unix://"):
        return bind
    if bind.startswith("unix:"):
        return "unix://" + bind[len("unix:") :]
    # host:port
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
    bind = os.environ.get("LANGGRAPH_RUNNER_BIND", "").strip()
    if not bind:
        logger.error("LANGGRAPH_RUNNER_BIND is required (unix:///path or host:port)")
        sys.exit(1)

    max_msg = int(os.environ.get("MAX_STREAM_CHUNK_SIZE_BYTES", 128 * 1024 * 1024))
    max_msg = max_msg + 1024 * 1024  # envelope headroom

    await _bootstrap()

    server = grpc_aio.server(
        options=[
            ("grpc.max_send_message_length", max_msg),
            ("grpc.max_receive_message_length", max_msg),
            ("grpc.keepalive_permit_without_calls", 1),
        ]
    )
    runner_pb2_grpc.add_RunnerServicer_to_server(RunnerServicer(), server)
    health_servicer = health.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    health_servicer.set("", health_pb2.HealthCheckResponse.SERVING)
    health_servicer.set("runner.Runner", health_pb2.HealthCheckResponse.SERVING)

    target = _parse_bind(bind)
    if target.startswith("unix://"):
        path = target[len("unix://") :]
        with suppress(FileNotFoundError):
            os.unlink(path)

    port = server.add_insecure_port(target)
    await server.start()
    logger.info("Runner gRPC server listening on %s (port=%s)", bind, port)
    await server.wait_for_termination()


def main() -> None:
    asyncio.run(amain())


if __name__ == "__main__":
    main()
