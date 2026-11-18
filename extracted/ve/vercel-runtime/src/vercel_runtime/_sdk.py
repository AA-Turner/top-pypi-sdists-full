from __future__ import annotations

import functools
import importlib
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from types import ModuleType


class CacheContext(Protocol):
    @property
    def wait_until(self) -> Callable[[Awaitable[object]], None] | None: ...


class CacheContextModule(Protocol):
    def get_context(self) -> CacheContext: ...

    def set_context(
        self,
        *,
        wait_until: Callable[[Awaitable[object]], None] | None = None,
        cache: object | None = None,
        async_cache: object | None = None,
    ) -> None: ...


def import_cached_module(name: str) -> ModuleType | None:
    try:
        return _import_unless_absent(name)
    except ImportError:
        # Raised errors are not cached, so a broken dependency is retried.
        return None


# Resolve after bootstrap; installed dependencies stay fixed per process.
@functools.cache
def _import_unless_absent(name: str) -> ModuleType | None:
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as exc:
        if exc.name and (name == exc.name or name.startswith(exc.name + ".")):
            return None
        raise
