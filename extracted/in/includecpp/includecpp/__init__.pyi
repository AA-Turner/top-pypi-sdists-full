"""Type stubs for includecpp package - VSCode IntelliSense support."""

from typing import Any, Dict, Optional, List, Literal, overload, Callable
from pathlib import Path
from types import ModuleType
import threading

# Import generated module wrappers for VSCode autocomplete
# These are created by 'includecpp rebuild' and provide module-specific type hints
try:
    from .core.cpp_api_extensions import *
except ImportError:
    pass  # Generated during rebuild


# ========== CSSL Module ==========
class _CSSLModule:
    """CSSL callable module created via CSSL.module()"""
    def __call__(self, *args: Any) -> Any:
        """Execute the module code with arguments."""
        ...

class _CSSLFunctionModule:
    """CSSL function module created via CSSL.makemodule()"""
    def __getattr__(self, name: str) -> Callable[..., Any]:
        """Get a function from the module."""
        ...

class _CsslLang:
    """CSSL Language interface."""

    def exec(self, path_or_code: str, *args: Any) -> Any:
        """Execute CSSL code or file.

        Args:
            path_or_code: Path to .cssl file or CSSL code string
            *args: Arguments accessible via parameter.get(index)

        Returns:
            Execution result
        """
        ...

    def T_exec(
        self,
        path_or_code: str,
        *args: Any,
        callback: Optional[Callable[[Any], None]] = None
    ) -> threading.Thread:
        """Execute CSSL code asynchronously in a thread."""
        ...

    def wait_all(self, timeout: Optional[float] = None) -> None:
        """Wait for all async executions to complete."""
        ...

    def get_output(self) -> List[str]:
        """Get output buffer from last execution."""
        ...

    def clear_output(self) -> None:
        """Clear output buffer."""
        ...

    def set_global(self, name: str, value: Any) -> None:
        """Set a global variable in CSSL runtime."""
        ...

    def get_global(self, name: str) -> Any:
        """Get a global variable from CSSL runtime."""
        ...

    def module(self, code: str) -> _CSSLModule:
        """Create a callable CSSL module from code."""
        ...

    def makemodule(self, code: str) -> _CSSLFunctionModule:
        """Create a CSSL module with accessible functions."""
        ...


class _CSSLBridge:
    """CSSL Bridge module - access to CSSL language from Python."""

    CsslLang: type[_CsslLang]

    def exec(self, path_or_code: str, *args: Any) -> Any:
        """Execute CSSL code or file."""
        ...

    def _exec(self, code: str, *args: Any) -> Any:
        """Execute CSSL code (alias for exec)."""
        ...

    def T_exec(
        self,
        path_or_code: str,
        *args: Any,
        callback: Optional[Callable[[Any], None]] = None
    ) -> threading.Thread:
        """Execute CSSL code asynchronously."""
        ...

    def _T_exec(
        self,
        code: str,
        *args: Any,
        callback: Optional[Callable[[Any], None]] = None
    ) -> threading.Thread:
        """Execute CSSL code asynchronously (alias)."""
        ...

    def set_global(self, name: str, value: Any) -> None:
        """Set a global variable."""
        ...

    def get_global(self, name: str) -> Any:
        """Get a global variable."""
        ...

    def get_output(self) -> List[str]:
        """Get output buffer."""
        ...

    def clear_output(self) -> None:
        """Clear output buffer."""
        ...

    def module(self, code: str) -> _CSSLModule:
        """Create a callable CSSL module."""
        ...

    def makemodule(self, code: str) -> _CSSLFunctionModule:
        """Create a CSSL function module."""
        ...

    def get_cssl(self) -> _CsslLang:
        """Get default CSSL instance."""
        ...


# CSSL module instance
CSSL: _CSSLBridge

__version__: str

# Dynamic module access via: from includecpp import <module_name>
# Auto-generated module declarations
# These allow: from includecpp import <module_name>
cssl_runner: Cssl_runnerModuleWrapper
mycpp: MycppModuleWrapper

def __dir__() -> List[str]:
    """List available modules including dynamically loaded C++ modules."""
    ...

class ModuleWrapper:
    """Wrapper for C++ modules with getInfo() and dynamic attributes."""

    def getInfo(self) -> Dict[str, Any]:
        """Get module metadata including classes, functions, and structs."""
        ...

    def __getattr__(self, name: str) -> Any: ...
    def __dir__(self) -> List[str]: ...

class CppApi:
    """Main API class for including C++ modules with type hints."""

    # Inbuilt module constants
    FileSystem: str
    Crypto: str
    JSON: str
    StringUtils: str
    Networking: str
    DataStructures: str
    Threading: str
    StandardMenus: str

    def __init__(
        self,
        verbose: bool = False,
        auto_update: bool = False,
        config_path: Optional[Path] = None
    ) -> None: ...

    @property
    def Inbuilds(self) -> List[str]:
        """List of available inbuilt modules."""
        ...

    def exists(self, module_name: str) -> bool:
        """Check if a module exists."""
        ...

    # The include() method returns ModuleWrapper with dynamic attributes
    # VSCode will show getInfo() and other attributes set at runtime
    def include(
        self,
        module_name: str,
        auto_update: Optional[bool] = None
    ) -> ModuleWrapper:
        """Include a C++ module.

        Returns a ModuleWrapper instance with:
        - getInfo() method for module metadata
        - Dynamic attributes for classes, functions, and structs

        Example:
            crypto = api.include("crypto")
            crypto.getInfo()  # Get module info
            crypto.Crypto()   # Access Crypto class
            crypto.md5(...)   # Call md5 function

        Args:
            module_name: Name of the module to include
            auto_update: Whether to auto-rebuild if outdated (default: False)

        Returns:
            ModuleWrapper with module-specific attributes
        """
        ...

    def need_update(self, module_name: str) -> bool:
        """Check if module needs rebuild based on source file changes.

        Args:
            module_name: Name of module to check

        Returns:
            True if source files are newer than build
        """
        ...

    def update(self, module_name: str, verbose: Optional[bool] = None) -> None:
        """Rebuild a single module.

        Args:
            module_name: Name of module to rebuild
            verbose: Enable verbose output (default: use instance setting)
        """
        ...

    def rebuild(
        self,
        verbose: bool = False,
        clean: bool = False
    ) -> None:
        """Rebuild C++ modules."""
        ...

    def list_modules(self) -> List[str]:
        """List all available modules."""
        ...

__all__: List[str]  # Includes: CppApi, CSSL, __version__
