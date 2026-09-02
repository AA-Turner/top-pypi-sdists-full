# Copyright (C) 2018-present Jesus Lara
#
"""Qworker job executor — dispatches tasks through the qw worker queue."""
from __future__ import annotations
import asyncio
import time
import uuid
from typing import Any, Optional
from flowtask.executors.base import AbstractJobExecutor
from flowtask.executors.models import (
    ExecutorConfig,
    ExecutorType,
    ExecutionHandle,
    TaskResult,
)
from flowtask.executors.events import ExecutorLifecyclePublisher
from flowtask.executors.exceptions import ExecutorError, ExecutorConnectionError
from flowtask.executors.registry import register_executor

DEFAULT_DISPATCH_TIMEOUT = 60
DEFAULT_RETRY_DELAY = 10
DEFAULT_MAX_RETRY_ELAPSED = 60

_TRANSIENT_ERRORS = (
    asyncio.TimeoutError,
    ConnectionError,
    ConnectionRefusedError,
    ConnectionResetError,
    OSError,
)


@register_executor("qworker")
class QworkerJobExecutor(AbstractJobExecutor):
    """Dispatches tasks to the qw worker queue via QClient.

    This is the replacement for the ``queued=True`` / ``no_worker=False``
    code path that existed in all 4 dispatch sites.

    Priority routing:
    - ``"pub"`` → ``QClient.publish()``
    - ``"high"`` → ``QClient(worker_list=WORKER_HIGH_LIST).queue()``
    - ``"low"``/``"default"`` → ``QClient(worker_list=WORKER_LIST).queue()``
    - any key in ``WORKERS_LIST`` → ``QClient(worker_list=WORKERS_LIST[key]).queue()``
    - ``"direct"`` → ``QClient.run()`` (waits for result)

    QClient and TaskWrapper are lazy-imported to avoid loading heavy
    transitive dependencies (aiogram, etc.) at module import time.

    Args:
        config: ExecutorConfig with ``type=QWORKER`` and optional ``priority``.
        **kwargs: Passed through to the base constructor.
    """

    def __init__(self, config: ExecutorConfig, **kwargs) -> None:
        super().__init__(config, **kwargs)
        self._publisher = ExecutorLifecyclePublisher()

    @classmethod
    def name(cls) -> str:
        """Return registry name.

        Returns:
            ``"qworker"``
        """
        return "qworker"

    def _sanitize_kwargs(self, program: str, task: str, kwargs: dict) -> dict:
        """Drop kwargs that cannot be cloudpickled before queue dispatch.

        The TaskWrapper is serialized with ``cloudpickle`` when handed to the
        worker. Any kwarg holding a non-serializable object (e.g. a live uvloop
        event loop, a DB/Redis pool, or the navconfig ``config`` singleton)
        raises ``TypeError: no default __reduce__ due to non-trivial __cinit__``
        and kills the whole dispatch. This guards the boundary: each kwarg is
        probed individually, and any that fails is logged by name and removed so
        the remaining payload still serializes.

        Args:
            program: Program slug (for log context).
            task: Task identifier (for log context).
            kwargs: Raw kwargs destined for the TaskWrapper constructor.

        Returns:
            A new dict containing only the serializable kwargs.
        """
        import cloudpickle  # lazy import

        clean: dict = {}
        for key, value in kwargs.items():
            try:
                cloudpickle.dumps(value)
            except Exception as exc:  # noqa: BLE001 — probe, not control flow
                self.logger.warning(
                    "Dropping non-serializable kwarg '%s' (%s) from %s.%s "
                    "dispatch — would break cloudpickle: %s",
                    key,
                    type(value).__name__,
                    program,
                    task,
                    exc,
                )
                continue
            clean[key] = value
        return clean

    def _make_wrapper(
        self,
        program: str,
        task: str,
        execution_id: str,
        queued: bool = True,
        **kwargs,
    ):
        """Create a TaskWrapper for queue dispatch.

        Args:
            program: Program slug.
            task: Task identifier.
            execution_id: UUID used as the task identity inside the wrapper.
            queued: Whether this is a queued (fire-and-forget) dispatch.
            **kwargs: Forwarded to the TaskWrapper constructor.

        Returns:
            A TaskWrapper instance ready for dispatch.
        """
        from qw.wrappers import TaskWrapper  # lazy import
        kwargs = self._sanitize_kwargs(program, task, kwargs)
        wrapper = TaskWrapper(
            program=program,
            task=task,
            task_id=execution_id,
            ignore_results=True,
            **kwargs,
        )
        wrapper.queued = queued
        return wrapper

    def _get_client(self, priority: Optional[str] = None):
        """Return a QClient for the given priority.

        Args:
            priority: Queue priority key or ``None`` for default.

        Returns:
            A configured QClient instance.
        """
        from qw.client import QClient  # lazy import
        from flowtask.conf import WORKER_LIST, WORKER_HIGH_LIST, WORKERS_LIST

        if priority == "high":
            return QClient(worker_list=WORKER_HIGH_LIST)
        if priority == "low" or priority is None or priority == "default":
            return QClient(worker_list=WORKER_LIST)
        # Named worker in WORKERS_LIST dict
        if priority in WORKERS_LIST:
            worker_list = WORKERS_LIST[priority]
            return QClient(worker_list=worker_list)
        # Unknown key — fall back to default
        self.logger.warning(
            "Unknown priority '%s'; falling back to default worker list", priority
        )
        return QClient(worker_list=WORKER_LIST)

    def _parse_result(self, raw: Any, execution_id: str) -> TaskResult:
        """Normalise a raw QClient result into a TaskResult.

        Args:
            raw: The value returned by QClient.run/queue/publish.
            execution_id: The execution UUID.

        Returns:
            A TaskResult with status and result.
        """
        if isinstance(raw, BaseException):
            return TaskResult(
                status="failed",
                error=str(raw),
                execution_id=execution_id,
            )
        if isinstance(raw, dict):
            if "exception" in raw:
                return TaskResult(
                    status="failed",
                    error=str(raw.get("error", raw["exception"])),
                    execution_id=execution_id,
                )
            # Decode message bytes if present
            try:
                raw["message"] = raw["message"].decode("utf-8")
            except (TypeError, KeyError, AttributeError):
                pass
        return TaskResult(
            status="success",
            result=raw,
            execution_id=execution_id,
        )

    def _load_retry_config(self) -> tuple[int, int, int]:
        """Load timeout and retry settings from project config.

        Returns:
            Tuple of (timeout, retry_delay, max_retry_elapsed) in seconds.
        """
        try:
            from flowtask.conf import (
                SCHEDULER_WORKER_TIMEOUT,
                SCHEDULER_RETRY_ENQUEUE,
                SCHEDULER_MAX_RETRY_ENQUEUE,
            )
            timeout = self._config.timeout or SCHEDULER_WORKER_TIMEOUT
            retry_delay = SCHEDULER_RETRY_ENQUEUE
            max_elapsed = SCHEDULER_MAX_RETRY_ENQUEUE
        except ImportError:
            timeout = self._config.timeout or DEFAULT_DISPATCH_TIMEOUT
            retry_delay = DEFAULT_RETRY_DELAY
            max_elapsed = DEFAULT_MAX_RETRY_ELAPSED
        return timeout, retry_delay, max_elapsed

    @staticmethod
    def _classify_dispatch_error(exc: Exception) -> str:
        """Return a human-readable reason for a dispatch failure."""
        if isinstance(exc, asyncio.TimeoutError):
            return "timed out waiting for worker queue — workers may be unreachable or overloaded"
        if isinstance(exc, ConnectionRefusedError):
            return "connection refused by worker queue broker (Redis/RabbitMQ may be down)"
        if isinstance(exc, ConnectionResetError):
            return "connection to worker queue broker was reset unexpectedly"
        if isinstance(exc, (ConnectionError, OSError)):
            return f"network/OS error connecting to worker queue broker: {exc}"
        if isinstance(exc, asyncio.QueueFull):
            return "worker queue is full — task discarded (non-retryable)"
        exc_name = type(exc).__name__
        exc_msg = str(exc)
        if "pickle" in exc_msg.lower() or "serialize" in exc_msg.lower():
            return f"task payload serialization failed (non-retryable): {exc_msg}"
        return f"unexpected error ({exc_name}): {exc_msg}"

    async def dispatch(
        self,
        program: str,
        task: str,
        task_id: str,
        **kwargs,
    ) -> ExecutionHandle:
        """Queue the task (fire-and-forget) and return immediately.

        Uses ``QClient.queue()`` by default, or ``QClient.publish()`` when
        ``priority == "pub"``.  Retries on transient errors (timeout,
        connection refused/reset) up to ``SCHEDULER_MAX_RETRY_ENQUEUE``
        seconds of wall-clock time.

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Unique execution UUID.
            **kwargs: Forwarded to TaskWrapper (userid, ENV, etc.).

        Returns:
            An ExecutionHandle with the queue message result.
        """
        execution_id = str(task_id) if task_id else str(uuid.uuid4())
        priority: Optional[str] = kwargs.pop(
            "priority", self._config.priority
        )
        channel = f"FLOWTASK:EXEC:{execution_id}"

        await self._publisher.publish(
            "dispatched", program, task, execution_id
        )

        wrapper = self._make_wrapper(program, task, execution_id, queued=True, **kwargs)

        timeout, retry_delay, max_elapsed = self._load_retry_config()
        start_time = time.monotonic()
        attempt = 0
        last_exc: Exception | None = None

        while True:
            attempt += 1
            try:
                if priority == "pub":
                    client = self._get_client(priority=None)
                    result = await asyncio.wait_for(
                        client.publish(wrapper), timeout=timeout
                    )
                else:
                    client = self._get_client(priority=priority)
                    result = await asyncio.wait_for(
                        client.queue(wrapper), timeout=timeout
                    )
                if attempt > 1:
                    self.logger.info(
                        "QClient dispatch for %s.%s succeeded on attempt %d",
                        program, task, attempt,
                    )
                return ExecutionHandle(
                    executor_type=ExecutorType.QWORKER,
                    execution_id=execution_id,
                    task_program=program,
                    task_name=task,
                    channel=channel,
                )
            except _TRANSIENT_ERRORS as exc:
                last_exc = exc
                elapsed = time.monotonic() - start_time
                reason = self._classify_dispatch_error(exc)
                if elapsed >= max_elapsed:
                    msg = (
                        f"QClient dispatch failed for {program}.{task} "
                        f"after {attempt} attempt(s) over {elapsed:.0f}s — "
                        f"reason: {reason}"
                    )
                    self.logger.error(msg)
                    await self._publisher.publish(
                        "failed", program, task, execution_id, error=msg
                    )
                    is_conn = isinstance(exc, (ConnectionError, OSError)) and not isinstance(exc, TimeoutError)
                    if is_conn:
                        raise ExecutorConnectionError(msg) from exc
                    raise ExecutorError(msg) from exc
                self.logger.warning(
                    "QClient dispatch attempt %d for %s.%s failed (%s). "
                    "Retrying in %ds (%.0f/%.0fs elapsed).",
                    attempt, program, task, reason,
                    retry_delay, elapsed, max_elapsed,
                )
                await asyncio.sleep(retry_delay)
            except asyncio.QueueFull as exc:
                reason = self._classify_dispatch_error(exc)
                msg = (
                    f"QClient dispatch failed for {program}.{task} — "
                    f"reason: {reason}"
                )
                self.logger.error(msg)
                await self._publisher.publish(
                    "failed", program, task, execution_id, error=msg
                )
                raise ExecutorError(msg) from exc
            except Exception as exc:
                reason = self._classify_dispatch_error(exc)
                msg = (
                    f"QClient dispatch failed for {program}.{task} — "
                    f"reason: {reason}"
                )
                self.logger.error(msg)
                await self._publisher.publish(
                    "failed", program, task, execution_id, error=msg
                )
                raise ExecutorError(msg) from exc

    async def run(
        self,
        program: str,
        task: str,
        task_id: str,
        **kwargs,
    ) -> TaskResult:
        """Run the task via QClient and wait for the result.

        Uses ``QClient.run()`` (or ``QClient.publish()`` for priority=pub).
        Retries on transient connection errors up to
        ``SCHEDULER_MAX_RETRY_ENQUEUE`` seconds of wall-clock time.

        Args:
            program: Program slug.
            task: Task identifier.
            task_id: Unique execution UUID.
            **kwargs: Forwarded to TaskWrapper (userid, ENV, etc.).

        Returns:
            TaskResult with the worker's return value.
        """
        execution_id = str(task_id) if task_id else str(uuid.uuid4())
        priority: Optional[str] = kwargs.pop(
            "priority", self._config.priority
        )

        await self._publisher.publish("started", program, task, execution_id)

        wrapper = self._make_wrapper(
            program, task, execution_id, queued=False, **kwargs
        )

        _, retry_delay, max_elapsed = self._load_retry_config()
        start_time = time.monotonic()
        attempt = 0

        while True:
            attempt += 1
            try:
                if priority == "pub":
                    client = self._get_client(priority=None)
                    raw = await client.publish(wrapper)
                elif priority == "direct":
                    client = self._get_client(priority="default")
                    raw = await client.run(wrapper)
                else:
                    client = self._get_client(priority=priority)
                    raw = await client.run(wrapper)

                task_result = self._parse_result(raw, execution_id)

                if attempt > 1:
                    self.logger.info(
                        "QClient run for %s.%s succeeded on attempt %d",
                        program, task, attempt,
                    )

                if task_result.status == "success":
                    await self._publisher.publish(
                        "completed", program, task, execution_id
                    )
                else:
                    await self._publisher.publish(
                        "failed", program, task, execution_id, error=task_result.error
                    )

                return task_result

            except _TRANSIENT_ERRORS as exc:
                elapsed = time.monotonic() - start_time
                reason = self._classify_dispatch_error(exc)
                if elapsed >= max_elapsed:
                    msg = (
                        f"QClient run failed for {program}.{task} "
                        f"after {attempt} attempt(s) over {elapsed:.0f}s — "
                        f"reason: {reason}"
                    )
                    self.logger.error(msg)
                    await self._publisher.publish(
                        "failed", program, task, execution_id, error=msg
                    )
                    return TaskResult(
                        status="failed",
                        error=msg,
                        execution_id=execution_id,
                    )
                self.logger.warning(
                    "QClient run attempt %d for %s.%s failed (%s). "
                    "Retrying in %ds (%.0f/%.0fs elapsed).",
                    attempt, program, task, reason,
                    retry_delay, elapsed, max_elapsed,
                )
                await asyncio.sleep(retry_delay)
            except Exception as exc:
                reason = self._classify_dispatch_error(exc)
                msg = (
                    f"QClient run failed for {program}.{task} — "
                    f"reason: {reason}"
                )
                self.logger.error(msg)
                await self._publisher.publish(
                    "failed", program, task, execution_id, error=str(exc)
                )
                return TaskResult(
                    status="failed",
                    error=msg,
                    execution_id=execution_id,
                )

    async def close(self) -> None:
        """Close the lifecycle publisher.

        Args: none.
        """
        await self._publisher.close()
