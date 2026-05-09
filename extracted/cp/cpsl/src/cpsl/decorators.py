"""Lifecycle and handler decorators for Capsule apps.

    @cpsl.boot()       — runs once when the runtime starts
    @cpsl.shutdown()    — runs on SIGTERM before going cold
    @cpsl.enter()       — runs when a new session is created
    @cpsl.exit()        — runs when a session is closed
    @cpsl.message()     — handles every inbound message
    @cpsl.task()        — background work unit with submit/schedule
    @cpsl.schedule()    — periodic execution on cron
    @cpsl.endpoint()    — simple HTTP endpoint
    @cpsl.asgi()        — mount a full ASGI app (FastAPI etc.)
"""

from __future__ import annotations

from typing import Callable, TYPE_CHECKING, Type, TypeVar

if TYPE_CHECKING:
    from .task_types import TaskDescriptor

F = TypeVar("F", bound=Callable)

_BOOT_ATTR = "_cpsl_boot"
_SHUTDOWN_ATTR = "_cpsl_shutdown"
_ENTER_ATTR = "_cpsl_enter"
_EXIT_ATTR = "_cpsl_exit"
_MESSAGE_ATTR = "_cpsl_message"
_MESSAGE_NAME_ATTR = "_cpsl_message_name"
_MESSAGE_LABEL_ATTR = "_cpsl_message_label"
_ACTION_ATTR = "_cpsl_action"
_ACTION_NAME_ATTR = "_cpsl_action_name"
_SCHEDULE_ATTR = "_cpsl_schedule"
_ENDPOINT_ATTR = "_cpsl_endpoint"
_ASGI_ATTR = "_cpsl_asgi"


def _hook(attr: str, doc: str) -> Callable[[F], F]:
    def decorator(fn: F) -> F:
        setattr(fn, attr, True)
        return fn
    decorator.__doc__ = doc
    return decorator


def boot() -> Callable[[F], F]:
    return _hook(_BOOT_ATTR, "Runs once when the runtime starts.")


def shutdown() -> Callable[[F], F]:
    return _hook(_SHUTDOWN_ATTR, "Runs on SIGTERM before the runtime goes cold.")


def enter() -> Callable[[F], F]:
    return _hook(_ENTER_ATTR, "Runs when a new session is created. Receives ``session``.")


def exit() -> Callable[[F], F]:
    return _hook(_EXIT_ATTR, "Runs when a session is closed.")


def message(name: str | None = None, *, label: str | None = None) -> Callable[[F], F]:
    """Register a chat message handler.

    ``@cpsl.message()`` handles the default chat. ``@cpsl.message("name")``
    handles a named chat selected by custom React pages via ``useChat("name")``.
    """
    def decorator(fn: F) -> F:
        setattr(fn, _MESSAGE_ATTR, True)
        setattr(fn, _MESSAGE_NAME_ATTR, name or "")
        setattr(fn, _MESSAGE_LABEL_ATTR, label or name or "")
        return fn
    return decorator


def action(name: str | None = None) -> Callable[[F], F]:
    """Handle a structured UI component event."""
    def decorator(fn: F) -> F:
        setattr(fn, _ACTION_ATTR, True)
        setattr(fn, _ACTION_NAME_ATTR, name or fn.__name__)
        return fn
    return decorator


def task(
    retries: int = 0,
    timeout: int = 0,
    lock: str | None = None,
    retry_for: list[Type[Exception]] | None = None,
    callback_url: str | None = None,
    process: bool = False,
) -> Callable[..., TaskDescriptor]:
    """Background work unit. Returns a TaskDescriptor with .submit()/.schedule().

    Args:
        retries: Max retry attempts on failure.
        timeout: Seconds before the task is killed (0 = no timeout).
        lock: Lock template string (e.g. "user:{user_id}") for distributed locking.
        retry_for: Exception types that trigger a retry instead of permanent failure.
        callback_url: URL to POST task result on completion/failure.
        process: Run in a separate OS process for CPU parallelism and
            crash isolation.
    """
    from .task_types import TaskDescriptor as _TD, _TASK_ATTR

    def decorator(fn: Callable) -> TaskDescriptor:
        desc = _TD(
            fn, retries=retries, timeout=timeout, lock=lock,
            retry_for=retry_for, callback_url=callback_url,
            process=process,
        )
        setattr(desc, _TASK_ATTR, True)
        return desc
    return decorator


def schedule(cron: str) -> Callable[[F], F]:
    """Periodic execution on cron schedule."""
    def decorator(fn: F) -> F:
        setattr(fn, _SCHEDULE_ATTR, cron)
        return fn
    return decorator


def endpoint(method: str = "GET", path: str = "/", authorized: bool = True) -> Callable[[F], F]:
    """Simple HTTP endpoint handler."""
    def decorator(fn: F) -> F:
        setattr(fn, _ENDPOINT_ATTR, {"method": method, "path": path, "authorized": authorized})
        return fn
    return decorator


def asgi(path: str = "/app") -> Callable[[F], F]:
    """Mount a full ASGI application (FastAPI, Starlette, etc.)."""
    def decorator(fn: F) -> F:
        setattr(fn, _ASGI_ATTR, {"path": path})
        return fn
    return decorator
