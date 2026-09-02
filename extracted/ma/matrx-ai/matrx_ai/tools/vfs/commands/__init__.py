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
    import importlib

    modules = [
        "awk", "cat", "cd", "chmod", "chown", "cp", "cut", "df", "diff", "du",
        "echo", "env", "file", "find", "grep", "gzip", "head", "ln", "ls",
        "mkdir", "mv", "patch", "printf", "ps", "pwd", "read_cmd", "readlink",
        "realpath", "rm", "rmdir", "sed", "set_cmd", "sort", "stat", "stubs",
        "tail", "tar", "test_cmd", "touch", "tr", "tree", "type", "uniq",
        "unzip", "wc", "which", "xargs",
    ]
    for mod in modules:
        try:
            importlib.import_module(f"matrx_ai.tools.vfs.commands.{mod}")
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
