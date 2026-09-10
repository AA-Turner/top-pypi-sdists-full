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
    import sys

    from matrx_ai.tools.vfs.commands import registry

    rebuild = registry.take_cleared()

    # fmt: off
    modules = [
        "awk", "cat", "cd", "chmod", "chown", "cp", "cut", "df", "diff", "du",
        "echo", "env", "file", "find", "grep", "gzip", "head", "ln", "ls",
        "mkdir", "mv", "patch", "printf", "ps", "pwd", "read_cmd", "readlink",
        "realpath", "rm", "rmdir", "sed", "set_cmd", "sort", "stat", "stubs",
        "tail", "tar", "test_cmd", "touch", "tr", "tree", "type", "uniq",
        "unzip", "wc", "which", "xargs",
    ]
    # fmt: on
    for mod in modules:
        name = f"matrx_ai.tools.vfs.commands.{mod}"
        try:
            already_imported = sys.modules.get(name)
            if rebuild and already_imported is not None:
                importlib.reload(already_imported)
            else:
                importlib.import_module(name)
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
