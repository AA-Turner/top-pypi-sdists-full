from importlib.metadata import version
import os
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

_TRUTHY_VALUES = {"true", "1", "yes"}

_LIGHT_IMPORT = (
    os.getenv("TOOLUNIVERSE_LIGHT_IMPORT", "false").lower() in _TRUTHY_VALUES
)

# Version information - read from package metadata or pyproject.toml
__version__ = version("tooluniverse")

# Check if lazy loading is enabled
LAZY_LOADING_ENABLED = (
    os.getenv("TOOLUNIVERSE_LAZY_LOADING", "true").lower() in _TRUTHY_VALUES
)

# Import MCP functionality (but don't patch yet to avoid circular imports)
if not _LIGHT_IMPORT:
    try:
        from .mcp_integration import _patch_tooluniverse

        _MCP_PATCH_AVAILABLE = True
    except ImportError:
        # MCP functionality not available
        _MCP_PATCH_AVAILABLE = False
        _patch_tooluniverse = None


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


# Import HTTP Client with graceful fallback for minimal installation
try:
    from .http_client import ToolUniverseClient

    _HTTP_CLIENT_AVAILABLE = True
except ImportError:
    _HTTP_CLIENT_AVAILABLE = False

    class ToolUniverseClient:  # type: ignore[no-redef]
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise ImportError(
                "HTTP Client requires requests and pydantic. "
                "Install with: pip install tooluniverse[client]"
            )


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
    global_names = set(globals().keys())
    tool_names = set(auto_discover_tools(lazy=True).keys())
    return sorted(global_names | tool_names)


# If lazy loading is disabled, eagerly import all tool modules so they
# are immediately available via the registry.
if not _LIGHT_IMPORT and not LAZY_LOADING_ENABLED:
    auto_discover_tools(lazy=False)


__all__ = [
    "__version__",
    "ToolUniverse",
    "BaseTool",
    "register_tool",
    "get_tool_registry",
    "SMCP",
    "create_smcp_server",
    "ToolUniverseClient",
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

# Apply MCP patches after all imports are complete to avoid circular imports
if not _LIGHT_IMPORT and _MCP_PATCH_AVAILABLE and _patch_tooluniverse is not None:
    _patch_tooluniverse(ToolUniverse)
