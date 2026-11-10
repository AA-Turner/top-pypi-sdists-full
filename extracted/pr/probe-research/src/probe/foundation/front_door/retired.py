"""Old import paths a front door no longer serves (taken out after their one release): importing one fails at once and
names what to use instead, never a bare "No module named" or an AttributeError a caller's fallback swallows."""

from __future__ import annotations

import sys
import threading
from collections.abc import Callable, Mapping
from typing import Any, NoReturn

_LOCK = threading.Lock()


class RetiredModules:
    """A `sys.meta_path` finder (duck-typed: `importlib.abc` costs ~13 ms at import) answering each retired module path
    (old dotted name -> what to use instead) with `ModuleNotFoundError`, the error a missing module raises, so a
    caller's `except ImportError` behaves as before and the message says where to go."""

    def __init__(self) -> None:
        self.paths: dict[str, str] = {}

    def find_spec(self, fullname: str, path: Any = None, target: Any = None) -> None:
        instead = self.paths.get(fullname)
        if instead is not None:
            raise ModuleNotFoundError(f"{fullname} was retired: {instead}", name=fullname)
        return None


def retire_modules(paths: Mapping[str, str]) -> None:
    """Importing each old module path in ``paths`` fails with what to use instead. One finder per process, last on
    `sys.meta_path`, so it is asked only once every real finder found nothing."""
    with _LOCK:
        finder = next((found for found in sys.meta_path if isinstance(found, RetiredModules)), None)
        if finder is None:
            finder = RetiredModules()
            sys.meta_path.append(finder)
        finder.paths.update(paths)


def make_retired_getattr(module: str, names: Mapping[str, str]) -> Callable[[str], Any]:
    """A package's `__getattr__` for the names it no longer serves (``names``: old name -> what to use instead):
    `ImportError` with that advice, which `from package import name` shows as it is (a retired submodule's name
    included: the import system swallows the finder's error on that path). Any other missing name stays an
    `AttributeError`."""

    def get_retired(name: str) -> NoReturn:
        instead = names.get(name)
        if instead is not None:
            raise ImportError(f"{module}.{name} was retired: {instead}", name=f"{module}.{name}")
        raise AttributeError(f"module {module!r} has no attribute {name!r}")

    return get_retired
