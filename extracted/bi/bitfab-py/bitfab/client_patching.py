from __future__ import annotations

import contextlib
import contextvars
import importlib.abc
import importlib.machinery
import sys
import threading
from collections.abc import Callable, Iterator
from typing import Any

NODE_RECORDS_CALL = "record"
NODE_OMITS_CALL = "omit"

_node_owns_next_call: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "bitfab_node_owns_next_call", default=None
)
_lock = threading.Lock()


@contextlib.contextmanager
def node_owns_next_call(*, record: bool = True) -> Iterator[None]:
    token = _node_owns_next_call.set(NODE_RECORDS_CALL if record else NODE_OMITS_CALL)
    try:
        yield
    finally:
        _node_owns_next_call.reset(token)


def take_node_ownership() -> str | None:
    ownership = _node_owns_next_call.get()
    if ownership is not None:
        _node_owns_next_call.set(None)
    return ownership


def renamed(function: Any, name: str, marker: str) -> Any:
    with contextlib.suppress(AttributeError, TypeError, ValueError):
        function.__code__ = function.__code__.replace(co_name=name)
    setattr(function, marker, True)
    return function


class _PatchingLoader(importlib.abc.Loader):
    def __init__(self, loader: Any, patch: Callable[[Any], None]) -> None:
        self._loader = loader
        self._patch = patch

    def create_module(self, spec: importlib.machinery.ModuleSpec) -> Any:
        return self._loader.create_module(spec)

    def exec_module(self, module: Any) -> None:
        self._loader.exec_module(module)
        with contextlib.suppress(Exception):
            self._patch(module)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._loader, name)


class PatchingFinder(importlib.abc.MetaPathFinder):
    def __init__(
        self, matches: Callable[[str], bool], patch: Callable[[Any], None]
    ) -> None:
        self._matches = matches
        self._patch = patch
        self._resolving = threading.local()

    def find_spec(
        self, fullname: str, path: Any, target: Any = None
    ) -> importlib.machinery.ModuleSpec | None:
        if not self._matches(fullname):
            return None
        if getattr(self._resolving, "active", False):
            return None
        self._resolving.active = True
        try:
            spec = self._spec_from_other_finders(fullname, path, target)
        finally:
            self._resolving.active = False
        if spec is None or spec.loader is None:
            return None
        spec.loader = _PatchingLoader(spec.loader, self._patch)
        return spec

    def _spec_from_other_finders(
        self, fullname: str, path: Any, target: Any
    ) -> importlib.machinery.ModuleSpec | None:
        for finder in list(sys.meta_path):
            if finder is self:
                continue
            find_spec = getattr(finder, "find_spec", None)
            if find_spec is None:
                continue
            spec = find_spec(fullname, path, target)
            if spec is not None:
                return spec
        return None

    def install(self) -> None:
        if self in sys.meta_path:
            return
        with _lock:
            if self not in sys.meta_path:
                sys.meta_path.insert(0, self)
