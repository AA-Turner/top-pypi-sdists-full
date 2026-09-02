"""Manager instance for ``tool.executor`` rows.

Replaces the legacy ``tl_executor_kind_db`` module. ``tool_executor`` is
the executor registry — each row is a runtime that can dispatch a tool
(e.g. ``matrx-ai-core``, ``aidream``, ``matrx-local``, ``chrome-extension``,
``matrx-user``, ``mcp.<slug>``). Columns: ``name`` (PK text),
``description``, ``parent_executor_name`` (self-FK for inheritance, max
depth 3), ``mcp_server_id`` (FK, non-null iff this IS an MCP runtime),
``config`` (jsonb), ``is_active``, ``metadata``.

Naming convention: regex ``^[a-z][a-z0-9-]*(\\.[a-z0-9][a-z0-9-]*)*$``.
Sub-executors use dot-notation (e.g. ``matrx-user.chat``).
MCP executors are ``mcp.<server_slug>``.

The host (aidream/package_integration.py) injects ``ToolExecutorBase``.
Like ``tool_def_db``, the base is resolved LAZILY (PEP 562 ``__getattr__`` +
memoized builder) so importing this module never requires
``matrx_ai.configure()`` — config errors surface at access time, never at
import time — and the manager rebinds if the host swaps the registered base.
"""

from __future__ import annotations

from typing import Any

from matrx_ai.db._registry import get_base


def _build_manager(base: type) -> Any:
    class _ToolExecutorManager(base):  # type: ignore[misc,valid-type]
        pass

    _ToolExecutorManager.__name__ = "ToolExecutorManager"
    _ToolExecutorManager.__qualname__ = "ToolExecutorManager"
    return _ToolExecutorManager()


_manager: Any = None
_manager_base: type | None = None


def get_tool_executor_manager() -> Any:
    """Return the ``tool_executor`` manager bound to the *currently configured*
    base. Rebuilds when the host swaps the registered ``ToolExecutorBase``
    (identity change), otherwise returns the cached instance."""
    global _manager, _manager_base
    base = get_base("ToolExecutorBase")
    if _manager is None or _manager_base is not base:
        _manager = _build_manager(base)
        _manager_base = base
    return _manager


def __getattr__(name: str) -> Any:
    # PEP 562 lazy module attributes — preserves the historical import surface
    # (``from matrx_ai.tools.tool_executor_db import tool_executor_manager_instance``
    # / ``ToolExecutorManager``) while deferring base resolution to first access.
    if name == "tool_executor_manager_instance":
        return get_tool_executor_manager()
    if name == "ToolExecutorManager":
        return type(get_tool_executor_manager())
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
