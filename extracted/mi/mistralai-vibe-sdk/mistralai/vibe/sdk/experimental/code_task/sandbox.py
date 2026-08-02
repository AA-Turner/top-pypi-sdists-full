"""Sandbox execution — run LLM-generated Python with tool replay/pause.

Mirrors runToolCode() from typescript-sandbox/run-tool-code.ts.

Uses exec() with restricted globals (dev mode). Production would use
Pyodide on Deno for true WASM isolation.

The deadlock detection approach:
- Tool functions return asyncio.Future objects
- Replayed calls: future resolved immediately (no suspension)
- New calls: future left pending (coroutine suspends)
- A detector coroutine uses sleep(0) to observe when all tasks are blocked
- When every coroutine is suspended on unresolved tool futures: deadlock
- Collect all pending tools, return partial_evaluation
"""

import asyncio
import builtins
import random as _real_random
import time as _real_time
from contextlib import suppress
from typing import Any

from .handler import ToolCallHandler
from .types import (
    CodeResult,
    PartialEvaluation,
    RunCodeResult,
    ToolDefinition,
)
from .utils import to_snake_case


def _make_tool_fn(handler: ToolCallHandler, tool_name: str):
    """Create an async tool function for the sandbox."""

    async def tool_fn(**kwargs: Any) -> Any:
        return await handler.call_tool(tool_name, kwargs)

    tool_fn.__name__ = to_snake_case(tool_name)
    tool_fn.__qualname__ = tool_fn.__name__
    return tool_fn


_SAFE_BUILTINS = {
    k: getattr(builtins, k)
    for k in [
        "True",
        "False",
        "None",
        "int",
        "float",
        "str",
        "bool",
        "list",
        "dict",
        "tuple",
        "set",
        "frozenset",
        "len",
        "range",
        "enumerate",
        "zip",
        "map",
        "filter",
        "sorted",
        "reversed",
        "min",
        "max",
        "sum",
        "abs",
        "round",
        "isinstance",
        "issubclass",
        "hasattr",
        "getattr",
        "setattr",
        "type",
        "repr",
        "any",
        "all",
        "object",
        "super",
        "property",
        "staticmethod",
        "classmethod",
        "Exception",
        "ValueError",
        "TypeError",
        "KeyError",
        "IndexError",
        "AttributeError",
        "RuntimeError",
        "StopIteration",
    ]
}


class _TimeShim:
    """Deterministic time.time() via internal replay."""

    def __init__(self, handler: ToolCallHandler):
        self._handler = handler

    def time(self) -> float:
        return self._handler.call_internal("__internal__.time.time", _real_time.time)


class _RandomShim:
    """Deterministic random.random() via internal replay."""

    def __init__(self, handler: ToolCallHandler):
        self._handler = handler

    def random(self) -> float:
        return self._handler.call_internal("__internal__.random.random", _real_random.random)


class _SandboxTaskTracker:
    """Track tasks spawned inside the sandbox asyncio namespace."""

    def __init__(self) -> None:
        self.tasks: set[asyncio.Task[Any]] = set()
        self.task_group_tasks: set[asyncio.Task[Any]] = set()

    def _track_task(
        self, task: asyncio.Task[Any], *, in_task_group: bool = False
    ) -> asyncio.Task[Any]:
        self.tasks.add(task)
        if in_task_group:
            self.task_group_tasks.add(task)
        return task

    def _ensure_future(self, aw: Any) -> asyncio.Future[Any]:
        future = asyncio.ensure_future(aw)
        if isinstance(future, asyncio.Task):
            self._track_task(future)
        return future

    def create_task(
        self,
        coro: Any,
        *,
        name: str | None = None,
        context: Any = None,
        loop: Any = None,
    ) -> asyncio.Task[Any]:
        if loop is not None and loop is not asyncio.get_running_loop():
            raise RuntimeError("Custom asyncio task loops are not allowed in sandbox")

        kwargs: dict[str, Any] = {}
        if name is not None:
            kwargs["name"] = name
        if context is not None:
            kwargs["context"] = context

        task = asyncio.create_task(coro, **kwargs)
        return self._track_task(task)

    def task(
        self,
        coro: Any,
        *,
        loop: Any = None,
        name: str | None = None,
        context: Any = None,
    ) -> asyncio.Task[Any]:
        return self.create_task(coro, loop=loop, name=name, context=context)

    def gather(self, *aws: Any, return_exceptions: bool = False) -> asyncio.Future[Any]:
        return asyncio.gather(
            *(self._ensure_future(aw) for aw in aws),
            return_exceptions=return_exceptions,
        )

    def active_tasks(self) -> set[asyncio.Task[Any]]:
        return {task for task in self.tasks if not task.done()}


def _build_sandbox_globals(
    handler: ToolCallHandler,
    tools: list[ToolDefinition],
    stdout_lines: list[str],
    stderr_lines: list[str],
    task_tracker: _SandboxTaskTracker,
) -> dict[str, Any]:
    """Build restricted globals for exec()."""
    _real_sleep = asyncio.sleep

    async def _blocked_sleep(seconds: float) -> None:
        if seconds > 0:
            raise RuntimeError(
                "asyncio.sleep() with non-zero delay is not allowed in sandbox. "
                "It introduces non-deterministic timing."
            )
        await _real_sleep(0)

    class _SandboxTaskGroup(asyncio.TaskGroup):
        def create_task(
            self,
            coro: Any,
            *,
            name: str | None = None,
            context: Any = None,
            **kwargs: Any,
        ) -> asyncio.Task[Any]:
            task_kwargs = dict(kwargs)
            if name is not None:
                task_kwargs["name"] = name
            if context is not None:
                task_kwargs["context"] = context

            task = super().create_task(coro, **task_kwargs)
            return task_tracker._track_task(task, in_task_group=True)

    # Expose a sandbox-safe asyncio namespace
    class _SandboxAsyncio:
        gather = staticmethod(task_tracker.gather)
        create_task = staticmethod(task_tracker.create_task)
        sleep = staticmethod(_blocked_sleep)
        wait = staticmethod(asyncio.wait)
        wait_for = staticmethod(asyncio.wait_for)
        Future = asyncio.Future
        Task = staticmethod(task_tracker.task)
        TaskGroup = _SandboxTaskGroup
        CancelledError = asyncio.CancelledError
        TimeoutError = asyncio.TimeoutError

    globals_dict: dict[str, Any] = {
        "__builtins__": dict(_SAFE_BUILTINS),
        "asyncio": _SandboxAsyncio,
        "print": lambda *args: stdout_lines.append(" ".join(str(a) for a in args)),
        "time": _TimeShim(handler),
        "random": _RandomShim(handler),
    }

    for tool in tools:
        fn_name = to_snake_case(tool.function.name)
        globals_dict[fn_name] = _make_tool_fn(handler, tool.function.name)

    return globals_dict


async def _cancel_tasks(tasks: set[asyncio.Task[Any]]) -> None:
    for task in tasks:
        if not task.done():
            task.cancel()

    for task in tasks:
        with suppress(asyncio.CancelledError, Exception):
            await task


def _format_error(error: BaseException) -> str:
    if isinstance(error, ExceptionGroup) and len(error.exceptions) == 1:
        return _format_error(error.exceptions[0])

    return f"{type(error).__name__}: {error}"


def _unretrieved_task_error(task: asyncio.Task[Any]) -> BaseException | None:
    # Avoid task.exception(): it marks the exception as retrieved before sandbox
    # code has had a chance to await the task and catch it.
    if getattr(task, "_log_traceback", True) is False:
        return None

    error = getattr(task, "_exception", None)
    if isinstance(error, BaseException):
        return error

    return None


def _tracked_task_error(
    task_tracker: _SandboxTaskTracker,
) -> tuple[asyncio.Task[Any], str] | None:
    for task in task_tracker.tasks:
        if task in task_tracker.task_group_tasks:
            continue
        if not task.done():
            continue
        if task.cancelled():
            continue

        error = _unretrieved_task_error(task)
        if error is not None:
            return task, _format_error(error)

    return None


def _consume_task_exception(task: asyncio.Task[Any]) -> None:
    with suppress(BaseException):
        task.exception()


def _task_group_error_pending(task_tracker: _SandboxTaskTracker) -> bool:
    for task in task_tracker.task_group_tasks:
        if not task.done() or task.cancelled():
            continue

        if isinstance(getattr(task, "_exception", None), BaseException):
            return True

    return False


def _main_task_failed(main_task: asyncio.Task[Any]) -> bool:
    return main_task.done() and not main_task.cancelled() and main_task.exception() is not None


async def _tracked_task_error_after_user_handlers(
    main_task: asyncio.Task[Any], task_tracker: _SandboxTaskTracker
) -> str | None:
    tracked_task_error = _tracked_task_error(task_tracker)
    if tracked_task_error is None:
        return None

    await asyncio.sleep(0)
    if _main_task_failed(main_task):
        return None

    tracked_task_error = _tracked_task_error(task_tracker)
    if tracked_task_error is None:
        return None

    task, error = tracked_task_error
    _consume_task_exception(task)
    return error


async def _run_with_deadlock_detection(
    main_coro: Any,
    handler: ToolCallHandler,
    task_tracker: _SandboxTaskTracker,
    timeout: float = 5.0,
) -> dict[str, Any]:
    """Run a coroutine until completion or deadlock.

    Deadlock = all coroutines blocked on unresolved tool futures.
    Detected via sleep(0): after yielding, if main_task is not done
    and pending_count > 0, every schedulable step has completed.
    Double-check with a second sleep(0) for safety.
    """
    main_task = asyncio.create_task(main_coro)

    try:
        async with asyncio.timeout(timeout):
            while not main_task.done() or task_tracker.active_tasks():
                await asyncio.sleep(0)

                if _main_task_failed(main_task):
                    await _cancel_tasks(task_tracker.active_tasks())
                    break

                tracked_task_error = await _tracked_task_error_after_user_handlers(
                    main_task, task_tracker
                )
                if tracked_task_error is not None:
                    await _cancel_tasks({main_task, *task_tracker.active_tasks()})
                    return {
                        "type": "error",
                        "error": tracked_task_error,
                    }

                if handler.pending_count > 0 and (
                    not main_task.done() or task_tracker.active_tasks()
                ):
                    await asyncio.sleep(0)
                    if _main_task_failed(main_task):
                        await _cancel_tasks(task_tracker.active_tasks())
                        break

                    tracked_task_error = await _tracked_task_error_after_user_handlers(
                        main_task, task_tracker
                    )
                    if tracked_task_error is not None:
                        await _cancel_tasks({main_task, *task_tracker.active_tasks()})
                        return {
                            "type": "error",
                            "error": tracked_task_error,
                        }
                    if _task_group_error_pending(task_tracker):
                        await asyncio.sleep(0)
                        continue
                    if handler.pending_count > 0 and (
                        not main_task.done() or task_tracker.active_tasks()
                    ):
                        await _cancel_tasks({main_task, *task_tracker.active_tasks()})
                        return {"type": "deadlock"}
    except TimeoutError:
        await _cancel_tasks({main_task, *task_tracker.active_tasks()})
        return {
            "type": "error",
            "error": f"Execution timed out ({timeout}s)",
        }

    try:
        value = main_task.result()
    except Exception as e:
        return {
            "type": "error",
            "error": _format_error(e),
        }

    tracked_task_error = _tracked_task_error(task_tracker)
    if tracked_task_error is not None:
        task, error = tracked_task_error
        _consume_task_exception(task)
        return {
            "type": "error",
            "error": error,
        }

    return {"type": "success", "value": value}


async def run_python_code(
    partial: PartialEvaluation,
    tools: list[ToolDefinition],
    *,
    timeout: float = 5.0,
) -> RunCodeResult:
    """Execute Python code with tool replay/pause.

    The code must define an ``async def main()`` function.

    Returns:
        - code_result: execution completed (success or error)
        - partial_evaluation: new tool calls need resolution
        - error: compilation or structural error
    """
    loop = asyncio.get_running_loop()
    handler = ToolCallHandler(tools, partial.tool_state, loop)

    stdout_lines: list[str] = []
    stderr_lines: list[str] = []
    task_tracker = _SandboxTaskTracker()
    sandbox_globals = _build_sandbox_globals(
        handler, tools, stdout_lines, stderr_lines, task_tracker
    )

    # Compile and exec user code (defines main)
    try:
        code_obj = compile(partial.code, "<sandbox>", "exec")
        exec(code_obj, sandbox_globals)  # noqa: S102
    except SyntaxError as e:
        return RunCodeResult(type="error", error=str(e))
    except Exception as e:
        return RunCodeResult(type="error", error=f"{type(e).__name__}: {e}")

    main_fn = sandbox_globals.get("main")
    if main_fn is None:
        return RunCodeResult(type="error", error="No main() function defined")
    if not asyncio.iscoroutinefunction(main_fn):
        return RunCodeResult(type="error", error="main() must be async")

    # Run with deadlock detection
    main_coro = main_fn(**partial.input) if partial.input else main_fn()
    result = await _run_with_deadlock_detection(main_coro, handler, task_tracker, timeout)

    stdout = "\n".join(stdout_lines) or None
    stderr = "\n".join(stderr_lines) or None

    if result["type"] == "deadlock":
        return RunCodeResult(
            type="partial_evaluation",
            partial_evaluation=PartialEvaluation(
                code=partial.code,
                tool_state=handler.output,
                input=partial.input,
            ),
        )

    if result["type"] == "error":
        return RunCodeResult(
            type="code_result",
            result=CodeResult(type="error", error=result["error"]),
            stdout=stdout,
            stderr=stderr,
        )

    return RunCodeResult(
        type="code_result",
        result=CodeResult(type="success", value=result["value"]),
        stdout=stdout,
        stderr=stderr,
    )
