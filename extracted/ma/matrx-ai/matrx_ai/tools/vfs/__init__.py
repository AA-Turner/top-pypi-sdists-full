from __future__ import annotations

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.cache import CachingBackend
from matrx_ai.tools.vfs.commands import (
    Command,
    CommandContext,
    VfsCommandRunner,
    encode,
    fail,
    load_all,
    ok,
    register,
    resolve_cwd,
)
from matrx_ai.tools.vfs.core import AbstractBackend, MatrxAsyncFS
from matrx_ai.tools.vfs.errors import (
    raise_eexist,
    raise_einval,
    raise_eisdir,
    raise_enoent,
    raise_enotdir,
    raise_enotempty,
    raise_exdev,
)
from matrx_ai.tools.vfs.paths import (
    Inode,
    InodeType,
    basename,
    dirname,
    is_absolute,
    join,
    normalize,
    split_components,
)
from matrx_ai.tools.vfs.shell import (
    CommandResult,
    CommandRunner,
    ShellEnv,
    ShellExpansionError,
    ShellParseError,
    ShellSyntaxError,
    execute,
    parse,
    tokenize,
)
from matrx_ai.tools.vfs.workspace import (
    WorkspaceContext,
    WorkspaceIdentityMissingError,
    clear_workspace_cache,
    get_backend,
    get_workspace_fs,
    get_workspace_fs_by_id,
    workspace_id_for,
)


async def make_vfs(workspace_id: str = "default") -> MatrxAsyncFS:
    backend = get_backend()
    await backend.ensure_workspace_root(workspace_id)
    return MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)


__all__ = [
    "AbstractBackend",
    "CachingBackend",
    "Command",
    "CommandContext",
    "CommandResult",
    "CommandRunner",
    "Inode",
    "InodeType",
    "MatrxAsyncFS",
    "MemoryBackend",
    "ShellEnv",
    "ShellExpansionError",
    "ShellParseError",
    "ShellSyntaxError",
    "VfsCommandRunner",
    "WorkspaceContext",
    "WorkspaceIdentityMissingError",
    "basename",
    "clear_workspace_cache",
    "dirname",
    "encode",
    "execute",
    "fail",
    "get_backend",
    "get_workspace_fs",
    "get_workspace_fs_by_id",
    "is_absolute",
    "join",
    "load_all",
    "make_vfs",
    "normalize",
    "ok",
    "parse",
    "raise_eexist",
    "raise_einval",
    "raise_eisdir",
    "raise_enoent",
    "raise_enotdir",
    "raise_enotempty",
    "raise_exdev",
    "register",
    "resolve_cwd",
    "split_components",
    "tokenize",
    "workspace_id_for",
]
