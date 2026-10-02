from __future__ import annotations

import contextlib
import functools
import inspect
import threading
from collections.abc import Callable, Generator
from contextlib import contextmanager
from types import TracebackType
from typing import Any

from django.db import DEFAULT_DB_ALIAS, connections
from django.db.backends.base.base import BaseDatabaseWrapper

from django_pg_utils.set._django import restore_django_logging, suppress_django_logging
from django_pg_utils.set._pg import PgRestoreState, restore_pg, suppress_pg
from django_pg_utils.set._result import HushResult, HushStatus, SettingResult
from django_pg_utils.set._settings import (
    HushSetting,
    get_effective_registry,
    get_hush_default,
)


class HushError(Exception):
    """Raised when strict=True and full suppression is not achieved."""

    def __init__(self, result: HushResult):
        self.result = result
        failed = [r.name for r in result.details if not r.suppressed]
        super().__init__(
            f"pg_hush: full suppression not achieved. "
            f"Failed settings: {', '.join(failed)}"
        )


_UNSET = object()


def _get_caller_location() -> str:
    """Return the first stack frame outside this module as ``file:line``.

    Walks outward and skips this module's own frames, so the location is the
    user's ``with hush(...)`` / ``with hush:`` line regardless of how many
    internal frames (factory, ``_Hush``, contextmanager) sit in between — a
    fixed offset is wrong for the no-parens form, which has an extra frame.
    ``inspect.stack(0)`` (context=0) avoids reading source files per frame.
    """
    for frame_info in inspect.stack(0):
        module = frame_info.frame.f_globals.get("__name__", "")
        if module != __name__:
            return f"{frame_info.filename}:{frame_info.lineno}"
    return "<unknown>"


def _target_aliases(database: str | None, all_aliases: list[str]) -> list[str]:
    """Resolve which connection aliases a hush scope targets.

    ``None`` -> the default connection only (the common case, and cheap — it
    avoids dialing every configured database, e.g. replicas/analytics, as a side
    effect). ``"*"`` -> every configured connection (the old default; kept as an
    explicit opt-in because suppressing everywhere is occasionally what a
    security-sensitive caller wants). Any other value -> that single alias.
    """
    if database is None:
        return [DEFAULT_DB_ALIAS]
    if database == "*":
        return list(all_aliases)
    return [database]


def _compute_status(details: list[SettingResult]) -> HushStatus:
    """Compute overall status from individual results."""
    if not details:
        return HushStatus.NONE
    suppressed = [r for r in details if r.suppressed]
    if len(suppressed) == len(details):
        return HushStatus.FULL
    elif len(suppressed) == 0:
        return HushStatus.NONE
    else:
        return HushStatus.PARTIAL


@contextmanager
def _hush_context(
    database: str | None = None,
    settings: list[str] | None = None,
    caller_location: str = "",
    registry: tuple[HushSetting, ...] | None = None,
) -> Generator[HushResult, None, None]:
    """Core context manager implementation."""
    all_details: list[SettingResult] = []
    pg_states: list[tuple[BaseDatabaseWrapper, PgRestoreState]] = []
    saved_logger_level: int | None = None

    # Determine target connections (None -> default only; "*" -> all).
    aliases = _target_aliases(database, list(connections))

    # Suppress PG settings on each connection
    for alias in aliases:
        conn = connections[alias]
        try:
            conn.ensure_connection()
            results, state = suppress_pg(
                conn,
                alias,
                settings,
                caller_location,
                registry=registry,
            )
            all_details.extend(results)
            pg_states.append((conn, state))
        except Exception as exc:
            all_details.append(
                SettingResult(
                    name="*",
                    connection=alias,
                    suppressed=False,
                    original_value=None,
                    error=f"connection error: {exc}",
                )
            )

    # Suppress Django logger
    django_result, saved_logger_level = suppress_django_logging()
    all_details.append(django_result)

    status = _compute_status(all_details)
    result = HushResult(status=status, details=all_details)

    try:
        yield result
    finally:
        # Restore Django logger (ref-counted; arg-free by design).
        if saved_logger_level is not None:
            restore_django_logging()

        # Restore PG settings
        for conn, state in pg_states:
            with contextlib.suppress(Exception):
                restore_pg(conn, state, caller_location)


def _resolve_param(value: Any, setting_name: str, fallback: Any) -> Any:
    """Resolve a parameter: explicit value wins, then Django setting, then fallback."""
    if value is not _UNSET:
        return value
    return get_hush_default(setting_name, fallback)


class _Hush:
    """Callable that works as both a bare decorator, parameterized decorator,
    and context manager."""

    def __init__(
        self,
        database: Any = _UNSET,
        settings: Any = _UNSET,
        strict: Any = _UNSET,
    ) -> None:
        # Store raw args and resolve against Django settings lazily (at enter /
        # call time), not here. Decorators are applied at import time, so eager
        # resolution would (a) require settings to be configured at import and
        # (b) freeze HUSH_* / the registry, making a module-level @hush(...) deaf
        # to override_settings and to any runtime configuration change.
        self._raw_database = database
        self._raw_settings = settings
        self._raw_strict = strict

    def _resolve(
        self,
    ) -> tuple[str | None, list[str] | None, bool, tuple[HushSetting, ...]]:
        database: str | None = _resolve_param(self._raw_database, "DATABASE", None)
        settings: list[str] | None = _resolve_param(
            self._raw_settings, "SETTINGS", None
        )
        strict: bool = _resolve_param(self._raw_strict, "STRICT", False)
        return database, settings, strict, get_effective_registry()

    def __enter__(self) -> HushResult:
        database, settings, self._strict, registry = self._resolve()
        self._caller_location = _get_caller_location()
        self._cm = _hush_context(
            database=database,
            settings=settings,
            caller_location=self._caller_location,
            registry=registry,
        )
        self._result = self._cm.__enter__()
        return self._result

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        suppressed = self._cm.__exit__(exc_type, exc_val, exc_tb)
        # Only raise HushError when the body exited normally; never mask an
        # in-flight exception from the user's code with a strict-mode failure.
        if exc_type is None and self._strict and not self._result:
            raise HushError(self._result)
        return suppressed

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        # Resolve the wrapped function's source location once, at decoration
        # time, directly from the code object. Using `inspect.getsourcelines`
        # would re-read the source file on every call and raise OSError if the
        # file is unreachable (renamed checkout, stale .pyc, exec/REPL, etc.);
        # `co_firstlineno` gives the same line number with no file I/O.
        code = getattr(func, "__code__", None)
        if code is not None:
            caller_location = f"{code.co_filename}:{code.co_firstlineno}"
        else:
            caller_location = f"<{getattr(func, '__qualname__', repr(func))}>"

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Resolve per call so HUSH_* settings are read when the function
            # runs, not when it was decorated.
            database, settings, strict, registry = self._resolve()
            with _hush_context(
                database=database,
                settings=settings,
                caller_location=caller_location,
                registry=registry,
            ) as result:
                retval = func(*args, **kwargs)
            if strict and not result:
                raise HushError(result)
            return retval

        return wrapper


class _HushFactory:
    """Makes `hush` work as bare decorator, parameterized decorator, and
    context manager factory.

    - @hush          -> bare decorator (func passed directly)
    - @hush(...)     -> parameterized decorator (returns _Hush)
    - with hush():   -> context manager (returns _Hush)
    - with hush:     -> context manager (no parens; handled here)
    """

    def __init__(self) -> None:
        # Per-thread stack of active bare `with hush:` scopes. This must be a
        # stack, not a single attribute: the bare form runs through this one
        # shared singleton, so nesting/concurrency would clobber a single slot.
        # Critically, dropping the reference to an active scope's _Hush would let
        # its suspended context-manager generator be garbage-collected mid-scope
        # — running restoration at an arbitrary GC time. The stack keeps each
        # scope alive until its matching __exit__, and threading.local isolates
        # concurrent requests.
        self._local = threading.local()

    def _stack(self) -> list[_Hush]:
        stack: list[_Hush] | None = getattr(self._local, "stack", None)
        if stack is None:
            stack = []
            self._local.stack = stack
        return stack

    def __call__(
        self, func: Callable[..., Any] | None = None, /, **kwargs: Any
    ) -> _Hush | Callable[..., Any]:
        if func is not None and not callable(func):
            # Guard against hush("default") etc. — a non-callable positional was
            # silently dropped before, returning a default-configured _Hush.
            raise TypeError(
                "hush() takes keyword arguments only (database=, settings=, "
                "strict=); got a non-callable positional argument"
            )
        if func is not None and not kwargs:
            # Bare decorator: @hush
            return _Hush()(func)
        # Parameterized: @hush(...) or with hush(...)
        return _Hush(**kwargs)

    def __enter__(self) -> HushResult:
        # with hush as result: (no parens) — treat as hush()
        scope = _Hush()
        self._stack().append(scope)
        return scope.__enter__()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        scope = self._stack().pop()
        return scope.__exit__(exc_type, exc_val, exc_tb)


hush = _HushFactory()
