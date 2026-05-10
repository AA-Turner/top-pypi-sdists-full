"""Task descriptor and handle types for @cpsl.task()."""

from __future__ import annotations

import asyncio
import functools
import inspect
import json
import re
from datetime import timedelta
from typing import Any, Callable, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from .runner import Runner
    from .session import Session

_TASK_ATTR = "_cpsl_task"


def _runner_rpc_executor(runner: Any) -> Any:
    ensure = getattr(runner, "_ensure_rpc_executor", None)
    if callable(ensure):
        return ensure()
    return getattr(runner, "_rpc_executor", None)


def _task_scope(runner: Any) -> dict[str, str]:
    return {
        "version_id": runner._version_id,
        "user_id": runner._user_id,
    }


def _find_session_param(fn: Callable, functional: bool) -> str:
    """Return the task handler's session parameter name, if any."""
    try:
        params = list(inspect.signature(fn).parameters.values())
    except (TypeError, ValueError):
        return ""

    if not functional and params and params[0].name in ("self", "cls"):
        params = params[1:]
    for param in params:
        if param.kind not in (
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        ):
            continue
        if param.name == "session":
            return param.name
        hint = param.annotation
        if hint is inspect.Parameter.empty:
            continue
        if (isinstance(hint, str) and "Session" in hint) or "Session" in str(hint):
            return param.name
    return ""


class TaskHandle:
    """Handle to a submitted or discovered background task.

    Example::

        handle = await my_task.submit(session=session)
        status = await handle.status()  # "pending", "running", "completed", ...
        await handle.refresh()          # extend the timeout deadline
        await handle.cancel()           # cancel scheduled/running work

    Attributes:
        task_id: Unique identifier for the submitted task.
    """

    __slots__ = ("task_id", "_runner", "_record")

    def __init__(self, task_id: str, runner: Runner, record: dict[str, Any] | None = None) -> None:
        self.task_id = task_id
        self._runner = runner
        self._record: dict[str, Any] = record or {}

    @property
    def task_name(self) -> str:
        return self._record.get("task_name", "")

    @property
    def display_name(self) -> str:
        return self._record.get("display_name", "")

    @property
    def session_id(self) -> str:
        return self._record.get("session_id", "")

    @property
    def kwargs(self) -> dict:
        return self._record.get("kwargs", {})

    @property
    def created_at(self) -> str:
        return self._record.get("created_at", "")

    @property
    def started_at(self) -> str:
        return self._record.get("started_at", "")

    @property
    def completed_at(self) -> str:
        return self._record.get("completed_at", "")

    def __repr__(self) -> str:
        return f"TaskHandle({self.task_id!r})"

    async def status(self) -> str:
        """Return the current task status.

        Returns one of ``"pending"``, ``"claimed"``, ``"running"``,
        ``"completed"``, ``"failed"``, ``"retry"``, ``"cancelled"``,
        ``"scheduled"``, or ``"timeout"``.
        """
        from .clients.capsule import GetTaskRequest

        resp = await asyncio.get_running_loop().run_in_executor(
            _runner_rpc_executor(self._runner),
            self._runner._task_stub.get_task,
            GetTaskRequest(
                task_id=self.task_id,
                **_task_scope(self._runner),
            ),
        )
        return _proto_status_to_str(resp.task.status)

    async def refresh(self) -> None:
        """Reset the task's timeout clock.

        Extends the deadline by the original timeout duration from now.
        Only affects running tasks.
        """
        from .clients.capsule import RefreshTaskTimeoutRequest

        await asyncio.get_running_loop().run_in_executor(
            _runner_rpc_executor(self._runner),
            self._runner._task_stub.refresh_task_timeout,
            RefreshTaskTimeoutRequest(task_id=self.task_id, version_id=self._runner._version_id),
        )

    async def cancel(self) -> bool:
        """Cancel this task.

        Scheduled and queued tasks are cancelled before they run. Running tasks
        are cancelled cooperatively; the runner notices the cancellation on its
        heartbeat and interrupts the task handler.
        """
        from .clients.capsule import CancelTasksRequest

        resp = await asyncio.get_running_loop().run_in_executor(
            _runner_rpc_executor(self._runner),
            self._runner._task_stub.cancel_tasks,
            CancelTasksRequest(
                app_id=self._runner._app_id,
                task_id=self.task_id,
                **_task_scope(self._runner),
            ),
        )
        return resp.cancelled > 0


class TaskDescriptor:
    """A background task registered with ``@app.task()`` or ``@cpsl.task()``.

    Call ``.submit()`` to run immediately or ``.schedule()`` to run after
    a delay.  Use ``.find()``, ``.count()``, and ``.cancel()`` to query
    and manage submitted tasks.

    When ``process=True``, the task runs in a **separate OS process**,
    giving true CPU parallelism (bypasses the GIL) and crash isolation
    (OOM / segfault in the task won't kill the runner).  The child gets
    a fully re-hydrated ``Session`` — it can ``reply()``,
    ``stream_reply()``, ``show()``, and access ``session.db`` just like
    an in-process task.

    Example::

        @app.task(retries=2, timeout=60)
        async def send_email(session: cpsl.Session, to: str, body: str):
            ...

        @app.task(process=True, timeout=300)
        async def heavy_compute(session: cpsl.Session, data: dict):
            # runs on its own core
            ...

        handle = await send_email.submit(session=session, to="a@b.c", body="Hi")
        status = await handle.status()
    """

    def __init__(
        self,
        fn: Callable,
        retries: int = 0,
        timeout: int = 0,
        lock: str | None = None,
        retry_for: list[Type[Exception]] | None = None,
        callback_url: str | None = None,
        functional: bool = False,
        process: bool = False,
    ) -> None:
        self._fn = fn
        self._name = fn.__name__
        self._is_async = asyncio.iscoroutinefunction(fn)
        self._retries = retries
        self._timeout = timeout
        self._lock_template = lock
        self._retry_for = retry_for or []
        self._callback_url = callback_url
        self._functional = functional
        self._process = process
        self._session_param_name = _find_session_param(fn, functional)
        self._wants_session = bool(self._session_param_name)
        self._instance: Any = None
        self._runner: Runner | None = None

    def _bind(self, instance: Any, runner: Runner) -> None:
        self._instance = instance
        self._runner = runner

    def _resolve_lock(self, kwargs: dict) -> str:
        if not self._lock_template:
            return ""
        return re.sub(
            r"\{(\w+)\}",
            lambda m: str(kwargs.get(m.group(1), "")),
            self._lock_template,
        )

    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if self._functional:
            if self._is_async:
                return await self._fn(*args, **kwargs)
            return await asyncio.get_running_loop().run_in_executor(
                None,
                functools.partial(self._fn, *args, **kwargs),
            )
        if self._is_async:
            return await self._fn(self._instance, *args, **kwargs)
        return await asyncio.get_running_loop().run_in_executor(
            None,
            functools.partial(self._fn, self._instance, *args, **kwargs),
        )

    def _build_request(
        self,
        session: Any,
        kwargs: dict,
        scheduled_at: str = "",
        recurrence_seconds: int = 0,
        display_name: str = "",
    ) -> Any:
        from .clients.capsule import SubmitTaskRequest

        runner = self._require_runner()
        # user_id/version_id come from the runtime env so tasks submitted
        # from inside the app dispatch to the correct owner's inbox rather
        # than the coarse serve channel.
        return SubmitTaskRequest(
            app_id=runner._app_id,
            user_id=runner._user_id,
            version_id=runner._version_id,
            task_name=self._name,
            display_name=display_name,
            session_id=session.id if session else "",
            kwargs_json=json.dumps(kwargs).encode(),
            max_retries=self._retries,
            lock_key=self._resolve_lock(kwargs),
            scheduled_at=scheduled_at,
            timeout=self._timeout,
            recurrence_seconds=recurrence_seconds,
        )

    async def submit(
        self, session: Session | None = None, display_name: str = "", **kwargs: Any
    ) -> TaskHandle:
        """Submit the task for immediate background execution.

        Args:
            session: Bind the task to a chat session so the handler
                receives a hydrated ``Session`` as its first argument.
            **kwargs: Forwarded to the task handler as keyword arguments.

        Returns:
            A :class:`TaskHandle` for polling status or cancelling.

        Example::

            handle = await my_task.submit(session=session, label="job-1")
            await session.show_task(handle, message="Working...")
        """
        runner = self._require_runner()
        req = self._build_request(session, kwargs, display_name=display_name)
        resp = await asyncio.get_running_loop().run_in_executor(
            _runner_rpc_executor(runner),
            runner._task_stub.submit_task,
            req,
        )
        return TaskHandle(resp.task_id, runner)

    async def schedule(
        self,
        when: str | timedelta | Any | None = None,
        *,
        session: Session | None = None,
        delay: str | timedelta | None = None,
        display_name: str = "",
        **kwargs: Any,
    ) -> TaskHandle:
        """Schedule the task to run later, optionally recurring.

        Args:
            when: ``timedelta`` / shorthand delay, or recurrence text like
                ``"every 5m"``. For backward compatibility, a Session passed
                positionally is treated as ``session``.
            session: Bind the task to a chat session.
            delay: ``timedelta`` or shorthand string -- ``"5s"``,
                ``"30m"``, ``"1h"``, ``"3d"``.
            **kwargs: Forwarded to the task handler as keyword arguments.

        Example::

            handle = await my_task.schedule(session=session, delay="30m")
            handle = await my_task.schedule("every 5m", session=session)
        """
        from datetime import datetime, timezone

        runner = self._require_runner()
        if when is not None and not isinstance(when, (str, timedelta)):
            if session is not None:
                raise TypeError("session was provided twice")
            session = when
            when = None
        if when is not None and delay is not None:
            raise ValueError("provide either when or delay, not both")

        schedule_value = when if when is not None else delay
        scheduled_at = ""
        recurrence_seconds = 0
        if schedule_value is not None:
            delay_value, recurrence_seconds = _parse_schedule_value(schedule_value)
            scheduled_at = (datetime.now(timezone.utc) + delay_value).isoformat()

        req = self._build_request(session, kwargs, scheduled_at, recurrence_seconds, display_name)
        resp = await asyncio.get_running_loop().run_in_executor(
            _runner_rpc_executor(runner),
            runner._task_stub.submit_task,
            req,
        )
        return TaskHandle(resp.task_id, runner)

    async def find(
        self,
        status: str | None = None,
        session_id: str | None = None,
        limit: int = 100,
        offset: int = 0,
        **kwargs: Any,
    ) -> list[TaskHandle]:
        from .clients.capsule import FindTasksRequest

        runner = self._require_runner()
        resp = await asyncio.get_running_loop().run_in_executor(
            _runner_rpc_executor(runner),
            runner._task_stub.find_tasks,
            FindTasksRequest(
                app_id=runner._app_id,
                task_name=self._name,
                status=_str_to_proto_status(status) if status else 0,
                session_id=session_id or "",
                kwargs_filter_json=json.dumps(kwargs).encode() if kwargs else b"{}",
                limit=limit,
                offset=offset,
                **_task_scope(runner),
            ),
        )
        return [TaskHandle(t.task_id, runner, _task_record_to_dict(t)) for t in resp.tasks]

    async def count(self, status: str | None = None, **kwargs: Any) -> int:
        from .clients.capsule import CountTasksRequest

        runner = self._require_runner()
        resp = await asyncio.get_running_loop().run_in_executor(
            _runner_rpc_executor(runner),
            runner._task_stub.count_tasks,
            CountTasksRequest(
                app_id=runner._app_id,
                task_name=self._name,
                status=_str_to_proto_status(status) if status else 0,
                kwargs_filter_json=json.dumps(kwargs).encode() if kwargs else b"{}",
                **_task_scope(runner),
            ),
        )
        return resp.count

    async def cancel(self, status: str | None = None, **kwargs: Any) -> int:
        from .clients.capsule import CancelTasksRequest

        runner = self._require_runner()
        resp = await asyncio.get_running_loop().run_in_executor(
            _runner_rpc_executor(runner),
            runner._task_stub.cancel_tasks,
            CancelTasksRequest(
                app_id=runner._app_id,
                task_name=self._name,
                status=_str_to_proto_status(status) if status else 0,
                kwargs_filter_json=json.dumps(kwargs).encode() if kwargs else b"{}",
                **_task_scope(runner),
            ),
        )
        return resp.cancelled

    def _require_runner(self) -> Runner:
        if self._runner is None:
            raise RuntimeError("task not bound to a runner — is the app booted?")
        return self._runner


class GlobalTaskQuery:
    """Cross-cutting task query: self.tasks.find(), self.tasks.count(), etc."""

    def __init__(self, runner: Runner) -> None:
        self._runner = runner

    async def find(
        self, status: str | None = None, limit: int = 100, offset: int = 0, **kwargs: Any
    ) -> list[TaskHandle]:
        from .clients.capsule import FindTasksRequest

        resp = await asyncio.get_running_loop().run_in_executor(
            _runner_rpc_executor(self._runner),
            self._runner._task_stub.find_tasks,
            FindTasksRequest(
                app_id=self._runner._app_id,
                status=_str_to_proto_status(status) if status else 0,
                kwargs_filter_json=json.dumps(kwargs).encode() if kwargs else b"{}",
                limit=limit,
                offset=offset,
                **_task_scope(self._runner),
            ),
        )
        return [TaskHandle(t.task_id, self._runner, _task_record_to_dict(t)) for t in resp.tasks]

    async def count(self, status: str | None = None, **kwargs: Any) -> int:
        from .clients.capsule import CountTasksRequest

        resp = await asyncio.get_running_loop().run_in_executor(
            _runner_rpc_executor(self._runner),
            self._runner._task_stub.count_tasks,
            CountTasksRequest(
                app_id=self._runner._app_id,
                status=_str_to_proto_status(status) if status else 0,
                kwargs_filter_json=json.dumps(kwargs).encode() if kwargs else b"{}",
                **_task_scope(self._runner),
            ),
        )
        return resp.count

    async def cancel(self, status: str | None = None, **kwargs: Any) -> int:
        from .clients.capsule import CancelTasksRequest

        resp = await asyncio.get_running_loop().run_in_executor(
            _runner_rpc_executor(self._runner),
            self._runner._task_stub.cancel_tasks,
            CancelTasksRequest(
                app_id=self._runner._app_id,
                status=_str_to_proto_status(status) if status else 0,
                kwargs_filter_json=json.dumps(kwargs).encode() if kwargs else b"{}",
                **_task_scope(self._runner),
            ),
        )
        return resp.cancelled

    async def get(self, task_id: str) -> TaskHandle | None:
        from .clients.capsule import GetTaskRequest

        try:
            resp = await asyncio.get_running_loop().run_in_executor(
                _runner_rpc_executor(self._runner),
                self._runner._task_stub.get_task,
                GetTaskRequest(
                    task_id=task_id,
                    **_task_scope(self._runner),
                ),
            )
            return TaskHandle(resp.task.task_id, self._runner, _task_record_to_dict(resp.task))
        except Exception:
            return None


def _parse_delay(s: str) -> timedelta:
    m = re.match(
        r"^(\d+)\s*(d|day|days|h|hr|hour|hours|m|min|mins|minute|minutes|s|sec|secs|second|seconds)$",
        s.strip().lower(),
    )
    if not m:
        raise ValueError(f"invalid delay: {s!r} (expected '3d', '1h', '30m', '5s')")
    n, unit = int(m.group(1)), m.group(2)
    if unit in {"d", "day", "days"}:
        return timedelta(days=n)
    if unit in {"h", "hr", "hour", "hours"}:
        return timedelta(hours=n)
    if unit in {"m", "min", "mins", "minute", "minutes"}:
        return timedelta(minutes=n)
    return timedelta(seconds=n)


def _parse_schedule_value(value: str | timedelta) -> tuple[timedelta, int]:
    if isinstance(value, timedelta):
        return value, 0
    raw = value.strip().lower()
    recurring = False
    for prefix in ("every ", "repeat every "):
        if raw.startswith(prefix):
            raw = raw[len(prefix) :].strip()
            recurring = True
            break
    delay = _parse_delay(raw)
    return delay, int(delay.total_seconds()) if recurring else 0


def _task_record_to_dict(t: Any) -> dict:
    return {
        "task_id": t.task_id,
        "app_id": t.app_id,
        "task_name": t.task_name,
        "display_name": getattr(t, "display_name", ""),
        "session_id": t.session_id,
        "kwargs": json.loads(t.kwargs_json) if t.kwargs_json else {},
        "status": _proto_status_to_str(t.status),
        "attempt": t.attempt,
        "max_retries": t.max_retries,
        "timeout": t.timeout,
        "error": t.error,
        "created_at": t.created_at,
        "started_at": t.started_at,
        "completed_at": t.completed_at,
        "scheduled_at": t.scheduled_at,
        "recurrence_seconds": getattr(t, "recurrence_seconds", 0),
    }


_STATUS_TO_STR = {}
_STR_TO_STATUS = {}


def _init_status_maps():
    from .clients.capsule import TaskStatus

    global _STATUS_TO_STR, _STR_TO_STATUS
    pairs = [
        (TaskStatus.PENDING, "pending"),
        (TaskStatus.CLAIMED, "claimed"),
        (TaskStatus.RUNNING, "running"),
        (TaskStatus.COMPLETED, "completed"),
        (TaskStatus.FAILED, "failed"),
        (TaskStatus.RETRY, "retry"),
        (TaskStatus.CANCELLED, "cancelled"),
        (TaskStatus.SCHEDULED, "scheduled"),
        (TaskStatus.TIMEOUT, "timeout"),
    ]
    _STATUS_TO_STR = {k: v for k, v in pairs}
    _STR_TO_STATUS = {v: k for k, v in pairs}


def _proto_status_to_str(s: int) -> str:
    if not _STATUS_TO_STR:
        _init_status_maps()
    return _STATUS_TO_STR.get(s, "unknown")


def _str_to_proto_status(s: str | None) -> int:
    if s is None:
        return 0
    if not _STR_TO_STATUS:
        _init_status_maps()
    return _STR_TO_STATUS.get(s, 0)
