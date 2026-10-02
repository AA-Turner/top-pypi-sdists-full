from __future__ import annotations

import functools
import warnings
from collections.abc import Callable, Generator, Iterable
from contextlib import AbstractContextManager, contextmanager
from typing import Any

from django.db import connections, transaction

from django_pg_utils.set._identifier import validate_guc_name


@contextmanager
def _pg_set_context(
    settings: list[tuple[str, str]], using: str
) -> Generator[None, None, None]:
    """Core context manager: SET each GUC, yield, then RESET each."""
    conn = connections[using]
    conn.ensure_connection()

    applied: list[str] = []
    try:
        with conn.cursor() as cursor:
            for name, value in settings:
                cursor.execute(f"SET {name} = %s", [value])
                applied.append(name)
        yield
    finally:
        with conn.cursor() as cursor:
            for name in reversed(applied):
                try:
                    cursor.execute(f"RESET {name}")
                except Exception as exc:
                    warnings.warn(
                        f"pg_set: failed to RESET {name}: {exc}",
                        RuntimeWarning,
                        stacklevel=2,
                    )


def _normalize_settings(args: tuple[Any, ...]) -> list[tuple[str, str]]:
    """Normalize the flexible call signatures into a list of (name, value) tuples.

    Accepts:
        ("name", "value")           -> single GUC
        (iterable_of_tuples,)       -> multiple GUCs
    """
    if len(args) == 2 and isinstance(args[0], str):
        return [(validate_guc_name(args[0]), args[1])]

    if len(args) == 1:
        items = list(args[0])
        if not items:
            return []
        result: list[tuple[str, str]] = []
        for item in items:
            if not (isinstance(item, (tuple, list)) and len(item) == 2):
                raise TypeError(
                    "pg_set multi form expects an iterable of (name, value) "
                    f"pairs; got item {item!r}. Did you mean pg_set(name, value)?"
                )
            name, value = item
            result.append((validate_guc_name(name), value))
        return result

    raise TypeError(
        "pg_set expects either (name, value) or (iterable_of_tuples,). "
        f"Got {len(args)} arguments."
    )


class _ScopedSet:
    """Decorator / context manager that runs a GUC-setting context factory.

    `pg_set` and `atomic_set` differ only in which context manager wraps the
    scope (`_pg_set_context` vs `_atomic_set_context`), so both share this one
    class — the factory is passed in at construction.
    """

    def __init__(
        self,
        context_factory: Callable[
            [list[tuple[str, str]], str], AbstractContextManager[None]
        ],
        *args: str | Iterable[tuple[str, str]],
        using: str = "default",
    ) -> None:
        self._factory = context_factory
        self._settings = _normalize_settings(args)
        self._using = using

    def __enter__(self) -> None:
        self._cm = self._factory(self._settings, self._using)
        return self._cm.__enter__()

    def __exit__(self, *exc_info: object) -> bool | None:
        return self._cm.__exit__(*exc_info)  # type: ignore[arg-type]

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with self._factory(self._settings, self._using):
                return func(*args, **kwargs)

        return wrapper


def pg_set(
    *args: str | Iterable[tuple[str, str]], using: str = "default"
) -> _ScopedSet:
    """Temporarily SET PostgreSQL GUCs within a scope.

    Usage:
        # Single GUC, as context manager:
        with pg_set("work_mem", "256MB"):
            ...

        # Multiple GUCs:
        with pg_set([("work_mem", "256MB"), ("statement_timeout", "30s")]):
            ...

        # Specify database connection:
        with pg_set("work_mem", "256MB", using="other_db"):
            ...

        # As a decorator:
        @pg_set("work_mem", "256MB")
        def my_view(request):
            ...
    """
    return _ScopedSet(_pg_set_context, *args, using=using)


@contextmanager
def _atomic_set_context(
    settings: list[tuple[str, str]], using: str
) -> Generator[None, None, None]:
    """Core context manager: atomic() + SET LOCAL each GUC."""
    conn = connections[using]
    with transaction.atomic(using=using):
        conn.ensure_connection()
        with conn.cursor() as cursor:
            for name, value in settings:
                cursor.execute(f"SET LOCAL {name} = %s", [value])
        yield


def atomic_set(
    *args: str | Iterable[tuple[str, str]], using: str = "default"
) -> _ScopedSet:
    """Wrap a scope in atomic() with SET LOCAL for PostgreSQL GUCs.

    The GUCs are automatically reverted when the transaction ends —
    no RESET is needed.

    Usage:
        # Single GUC, as context manager:
        with atomic_set("work_mem", "256MB"):
            ...

        # Multiple GUCs:
        with atomic_set([("work_mem", "256MB"), ("statement_timeout", "30s")]):
            ...

        # Specify database connection:
        with atomic_set("work_mem", "256MB", using="other_db"):
            ...

        # As a decorator:
        @atomic_set("work_mem", "256MB")
        def my_view(request):
            ...
    """
    return _ScopedSet(_atomic_set_context, *args, using=using)
