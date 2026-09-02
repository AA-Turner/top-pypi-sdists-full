"""Manager instance for ``tool.binding`` rows.

Replaces the legacy ``tl_executor_db`` module. ``tool_binding`` is the
pure M2M join between ``tool_def`` and ``tool_executor`` — its only
columns are ``tool_id``, ``executor_name``, ``is_active``, ``created_at``,
``updated_at``. Routing decisions (server vs client vs MCP) live in
Python code now, NOT on the row.

The host (aidream/package_integration.py) injects ``ToolBindingBase``.
Like ``tool_def_db``, the base is resolved LAZILY (PEP 562 ``__getattr__`` +
memoized builder) so importing this module never requires
``matrx_ai.configure()`` — config errors surface at access time, never at
import time — and the manager rebinds if the host swaps the registered base.
"""

from __future__ import annotations

from typing import Any

from matrx_ai.db._registry import get_base


def _build_manager(base: type) -> Any:
    class _ToolBindingManager(base):  # type: ignore[misc,valid-type]
        async def load_all(self) -> Any:
            return await self.load_items()

        async def load_for_tool(self, tool_id: str) -> Any:
            return await self.filter_items(tool_id=tool_id)

    _ToolBindingManager.__name__ = "ToolBindingManager"
    _ToolBindingManager.__qualname__ = "ToolBindingManager"
    return _ToolBindingManager()


_manager: Any = None
_manager_base: type | None = None


def get_tool_binding_manager() -> Any:
    """Return the ``tool_binding`` manager bound to the *currently configured*
    base. Rebuilds when the host swaps the registered ``ToolBindingBase``
    (identity change), otherwise returns the cached instance."""
    global _manager, _manager_base
    base = get_base("ToolBindingBase")
    if _manager is None or _manager_base is not base:
        _manager = _build_manager(base)
        _manager_base = base
    return _manager


def __getattr__(name: str) -> Any:
    # PEP 562 lazy module attributes — preserves the historical import surface
    # (``from matrx_ai.tools.tool_binding_db import tool_binding_manager_instance``
    # / ``ToolBindingManager``) while deferring base resolution to first access.
    if name == "tool_binding_manager_instance":
        return get_tool_binding_manager()
    if name == "ToolBindingManager":
        return type(get_tool_binding_manager())
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
