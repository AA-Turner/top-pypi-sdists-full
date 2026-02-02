from importlib.metadata import version
import os
import warnings
from typing import Any, Optional, List

from .execute_function import ToolUniverse
from .base_tool import BaseTool
from .default_config import default_tool_files

from .tool_registry import (
    register_tool,
    get_tool_registry,
    get_tool_class_lazy,
    auto_discover_tools,
)

_LIGHT_IMPORT = os.getenv("TOOLUNIVERSE_LIGHT_IMPORT", "false").lower() in (
    "true",
    "1",
    "yes",
)

# Version information - read from package metadata or pyproject.toml
__version__ = version("tooluniverse")

# Check if lazy loading is enabled
LAZY_LOADING_ENABLED = os.getenv("TOOLUNIVERSE_LAZY_LOADING", "true").lower() in (
    "true",
    "1",
    "yes",
)

# Import MCP functionality
if not _LIGHT_IMPORT:
    try:
        from .mcp_integration import _patch_tooluniverse

        # Automatically patch ToolUniverse with MCP methods
        _patch_tooluniverse()

    except ImportError:
        # MCP functionality not available
        pass

# Import SMCP with graceful fallback and consistent signatures for type checking
try:
    from .smcp import SMCP, create_smcp_server

    _SMCP_AVAILABLE = True
except ImportError:
    _SMCP_AVAILABLE = False

    class SMCP:  # type: ignore[no-redef]
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise ImportError(
                "SMCP requires FastMCP. Install with: pip install fastmcp"
            )

    def create_smcp_server(
        name: str = "SMCP Server",
        tool_categories: Optional[List[str]] = None,
        search_enabled: bool = True,
        **kwargs: Any,
    ) -> SMCP:
        raise ImportError("SMCP requires FastMCP. Install with: pip install fastmcp")


def __getattr__(name: str) -> Any:
    """
    Dynamic dispatch for tool classes.
    This replaces the manual _LazyImportProxy list.
    """
    # 1. Try to get it from the tool registry (lazy or eager)
    # The registry knows about all tools via AST discovery or manual registration
    tool_class = get_tool_class_lazy(name)
    if tool_class:
        return tool_class

    # 2. If not found, raise AttributeError standard behavior
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> List[str]:
    """
    Dynamic directory listing.
    Includes standard globals plus all available tools.
    """
    # Standard globals
    global_names = list(globals().keys())

    # Available tools (triggers discovery if not already done)
    # auto_discover_tools(lazy=True) ensures we have the mapping
    tool_registry = auto_discover_tools(lazy=True)
    tool_names = list(tool_registry.keys())

    return sorted(list(set(global_names + tool_names)))


# If lazy loading is disabled, we should eagerly load everything now
# just to be safe and replicate old behavior, although __getattr__ works fine too.
# But for compatibility with `from tooluniverse import *` or inspection tools that
# don't use __dir__, eager loading might be desired if LAZY_LOADING_ENABLED is False.
if not _LIGHT_IMPORT and not LAZY_LOADING_ENABLED:
    # Trigger full discovery (imports all modules)
    auto_discover_tools(lazy=False)
    # Note: We don't inject them into globals() here because __getattr__ handles access.
    # But if users expect them to be in globals() for some reason, they might be disappointed.
    # However, PEP 562 __getattr__ handles instance access perfectly.
    # 'from tooluniverse import ToolName' works.
    pass


__all__ = [
    "__version__",
    "ToolUniverse",
    "BaseTool",
    "register_tool",
    "get_tool_registry",
    "SMCP",
    "create_smcp_server",
    "default_tool_files",
]


# Add tools to __all__ so `from tooluniverse import *` works
# This requires discovering tools first
if not _LIGHT_IMPORT:
    try:
        # Just get the names without importing modules if possible (lazy)
        _registry = auto_discover_tools(lazy=True)
        __all__.extend(list(_registry.keys()))
    except Exception:
        pass
