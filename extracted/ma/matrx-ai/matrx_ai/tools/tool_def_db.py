"""Manager instance for ``tool.definition`` rows.

Replaces the legacy ``tl_def_db`` module. Pulls a host-injected base via the
matrx-ai DB registry so the package can read tool definitions without
importing from aidream. The host (aidream/package_integration.py) injects
``ToolDefinitionBase``.

Why this resolves the base *lazily* instead of at import time
-------------------------------------------------------------
The earlier version did ``ToolDefBase = get_base("ToolDefBase")`` and built the
singleton ``tool_def_manager_instance = ToolDefManager()`` at module-import time.
That permanently baked the manager against whatever happened to be configured
the first time this module was imported. In a process where a stub DB config is
installed first (e.g. matrx-ai's own unit-test conftest) and the real host
config is registered later, the singleton stayed bound to the stub — so
``await tools_manager.filter_items(...)`` raised ``object _Stub can't be used in
'await' expression`` and the registry silently loaded zero tools.

Resolving the base on access (and rebuilding when the registered base object
changes identity) makes the tool layer robust to import order and to a config
being swapped after import — the registry always reads through the *live*
host-injected base. ``BaseManager.__init__`` has no global side effects, so
rebuilding is cheap and safe.
"""

from __future__ import annotations

from typing import Any

from matrx_ai.db._registry import get_base


def _build_manager(base: type) -> Any:
    class _ToolDefManager(base):  # type: ignore[misc,valid-type]
        async def load_all_tools(self) -> Any:
            return await self.load_items()

        async def get_tool_with_all_related(self, id: str) -> Any:
            return await self.get_item_with_all_related(id)

        async def _initialize_runtime_data(self, item: Any) -> None:
            pass

    _ToolDefManager.__name__ = "ToolDefManager"
    _ToolDefManager.__qualname__ = "ToolDefManager"
    return _ToolDefManager()


_manager: Any = None
_manager_base: type | None = None


def get_tool_def_manager() -> Any:
    """Return the ``tool_def`` manager bound to the *currently configured* base.

    Rebuilds when the host swaps the registered ``ToolDefBase`` (identity
    change), otherwise returns the cached instance.
    """
    global _manager, _manager_base
    base = get_base("ToolDefBase")
    if _manager is None or _manager_base is not base:
        _manager = _build_manager(base)
        _manager_base = base
    return _manager


def __getattr__(name: str) -> Any:
    # PEP 562 lazy module attributes — preserves the historical import surface
    # (``from matrx_ai.tools.tool_def_db import tool_def_manager_instance`` /
    # ``ToolDefManager``) while deferring base resolution until first access.
    if name == "tool_def_manager_instance":
        return get_tool_def_manager()
    if name == "ToolDefManager":
        return type(get_tool_def_manager())
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
