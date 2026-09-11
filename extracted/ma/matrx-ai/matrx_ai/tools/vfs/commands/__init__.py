from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import (
    Command,
    CommandContext,
    encode,
    fail,
    ok,
    resolve_cwd,
)
from matrx_ai.tools.vfs.commands.registry import (
    all_names,
    clear,
    get,
    is_registered,
    register,
)
from matrx_ai.tools.vfs.commands.runner import VfsCommandRunner


def load_all() -> None:
    """Register every virtual command — idempotent, and valid after ``clear()``.

    ``register`` runs at module import, so a plain ``import_module`` after a
    ``clear()`` does nothing (Python has cached the module) and the caller is
    left with an empty registry and no error. Reload in that case, so
    ``load_all()`` always means what it says.
    """
    import importlib
    import pkgutil
    import sys

    import matrx_ai.tools.vfs.commands as command_modules
    from matrx_ai.tools.vfs.commands import registry

    rebuild = registry.take_cleared()

    # This is a bounded census of our own package, not an arbitrary plugin
    # import. New command modules register themselves without requiring a
    # second hand-maintained list, while support modules remain inert.
    for module_info in pkgutil.iter_modules(command_modules.__path__):
        if module_info.name in {"base", "registry", "runner"}:
            continue
        name = f"matrx_ai.tools.vfs.commands.{module_info.name}"
        try:
            already_imported = sys.modules.get(name)
            if rebuild and already_imported is not None:
                importlib.reload(already_imported)
            else:
                importlib.import_module(f"matrx_ai.tools.vfs.commands.{module_info.name}")
        except ImportError:
            pass


__all__ = [
    "Command",
    "CommandContext",
    "VfsCommandRunner",
    "all_names",
    "clear",
    "encode",
    "fail",
    "get",
    "is_registered",
    "load_all",
    "ok",
    "register",
    "resolve_cwd",
]
