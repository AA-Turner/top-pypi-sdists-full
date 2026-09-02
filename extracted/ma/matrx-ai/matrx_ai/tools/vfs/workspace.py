from __future__ import annotations

from typing import Protocol, runtime_checkable

from matrx_ai.tools.vfs.backends.memory import MemoryBackend
from matrx_ai.tools.vfs.cache import CachingBackend
from matrx_ai.tools.vfs.core import AbstractBackend, MatrxAsyncFS


@runtime_checkable
class WorkspaceContext(Protocol):
    @property
    def user_id(self) -> str | None: ...
    @property
    def conversation_id(self) -> str | None: ...


_BACKEND: AbstractBackend | None = None
_FS_CACHE: dict[str, MatrxAsyncFS] = {}
# True once a host installs a DURABLE backend (e.g. code_files). Durable mode is per-USER
# (files persist across a user's conversations), so the workspace id drops the conversation
# suffix; the in-memory default stays per-conversation (ephemeral) as before.
_DURABLE_INSTALLED: bool = False


class WorkspaceIdentityMissingError(RuntimeError):
    """Raised when a requested workspace has no exact owner identity."""


# VFS storage backend — "memory" | "postgres". A code-reviewed constant, not
# an env var. (Was MATRX_VFS_BACKEND.) Tracked in /docs/ENV_FLAG_ERADICATION.md.
VFS_BACKEND: str = "memory"


def get_backend() -> AbstractBackend:
    global _BACKEND
    if _BACKEND is None:
        inner: AbstractBackend
        if VFS_BACKEND == "postgres":
            from matrx_ai.tools.vfs.backends.postgres import PostgresBackend

            inner = PostgresBackend()
        else:
            inner = MemoryBackend()
        _BACKEND = CachingBackend(inner)
    return _BACKEND


def set_backend(backend: AbstractBackend | None) -> None:
    """Install a host-provided durable backend (e.g. a code_files-backed store),
    or None to reset to the built-in default.

    This is the seam that gives the VFS a real, per-user filesystem in normal
    (non-sandbox) chat. It is a PLAIN setter: this package imports nothing from
    the rest of ``matrx_ai`` (it must stay liftable), so the wiring that CALLS
    this — reading the host-injected backend from ``matrx_ai.configure`` — lives
    outside ``vfs/``. The host backend is used DIRECTLY (not wrapped in the
    process-global ``CachingBackend``): a durable, per-user, RLS-scoped store
    must read fresh, exactly like ``agent_data``'s ``use_cache=False`` rule, so a
    cross-user cache hit can never serve one user another's row."""
    global _BACKEND, _DURABLE_INSTALLED
    _FS_CACHE.clear()
    _BACKEND = backend
    _DURABLE_INSTALLED = backend is not None


def has_durable_backend() -> bool:
    """True when a host has installed a durable VFS backend (e.g. aidream's code_files
    store). The fs/shell tools consult this to route a no-sandbox call to the durable VFS
    instead of the ephemeral real-disk fallback. False in standalone matrx-ai."""
    return _DURABLE_INSTALLED


def workspace_id_for(ctx: WorkspaceContext) -> str:
    """Resolve exact identity; never substitute a shared anonymous workspace.

    The old resolver mapped missing identities to ``anonymous``/``default``.
    Those shared filesystems are not equivalents of the requested owner, so
    there is no correct silent degradation. Supply authenticated context or
    intentionally use ``get_workspace_fs_by_id`` with an explicit owned id.
    """
    user_id = (ctx.user_id or "").strip()
    if not user_id:
        raise WorkspaceIdentityMissingError(
            "A user-scoped VFS workspace was requested, but WorkspaceContext.user_id "
            "is missing. Pass the authenticated AppContext user_id, or intentionally "
            "call get_workspace_fs_by_id with an explicitly owned workspace id; the "
            "shared 'anonymous' workspace substitute is refused."
        )
    # Durable backend → PER-USER (one filesystem across all the user's conversations).
    # In-memory default → per-conversation (ephemeral), unchanged.
    if _DURABLE_INSTALLED:
        return user_id
    conversation_id = (ctx.conversation_id or "").strip()
    if not conversation_id:
        raise WorkspaceIdentityMissingError(
            "An ephemeral conversation VFS workspace was requested, but "
            "WorkspaceContext.conversation_id is missing. Pass the active conversation "
            "id, install the durable per-user backend, or intentionally call "
            "get_workspace_fs_by_id with an explicitly owned id; the shared 'default' "
            "conversation substitute is refused."
        )
    return f"{user_id}:{conversation_id}"


async def get_workspace_fs(ctx: WorkspaceContext) -> MatrxAsyncFS:
    # 🚨 Do not restore anonymous/default fallbacks; workspace_id_for owns the
    # fail-loud identity boundary.
    workspace_id = workspace_id_for(ctx)
    fs = _FS_CACHE.get(workspace_id)
    if fs is None:
        backend = get_backend()
        await backend.ensure_workspace_root(workspace_id)
        fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
        _FS_CACHE[workspace_id] = fs
    return fs


async def get_workspace_fs_by_id(workspace_id: str) -> MatrxAsyncFS:
    fs = _FS_CACHE.get(workspace_id)
    if fs is None:
        backend = get_backend()
        await backend.ensure_workspace_root(workspace_id)
        fs = MatrxAsyncFS(backend=backend, workspace_id=workspace_id, asynchronous=True)
        _FS_CACHE[workspace_id] = fs
    return fs


def clear_workspace_cache() -> None:
    global _BACKEND
    _FS_CACHE.clear()
    _BACKEND = None
