"""Type stubs for cpp_api module - VSCode IntelliSense support.

This stub file provides proper type hints for the CppAPI.include() method
so VSCode can show autocomplete suggestions when using C++ modules.
"""

from typing import Any, Dict, Optional, Union, overload, Literal
from pathlib import Path

# Import the generated module wrapper protocols
try:
    from .cpp_api_extensions import *
except ImportError:
    pass  # Not yet generated

class ModuleWrapper:
    """Wrapper for C++ modules with dynamic attribute exposure."""

    def __init__(self, module: Any, info: Dict[str, Any]) -> None: ...
    def getInfo(self) -> Dict[str, Any]: ...
    def __getattr__(self, name: str) -> Any: ...
    def __dir__(self) -> list[str]: ...

class CppApi:
    """Main API class for including C++ modules."""

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
    def Inbuilds(self) -> list[str]: ...

    def exists(self, module_name: str) -> bool: ...

    # Overloaded include() signatures for each inbuilt module using Literal types
    # This allows VSCode to show module-specific autocomplete based on the string literal
    @overload
    def include(self, module_name: Literal["crypto"], auto_update: Optional[bool] = None) -> CryptoModuleWrapper: ...
    @overload
    def include(self, module_name: Literal["filesystem"], auto_update: Optional[bool] = None) -> FilesystemModuleWrapper: ...
    @overload
    def include(self, module_name: Literal["json"], auto_update: Optional[bool] = None) -> JsonModuleWrapper: ...
    @overload
    def include(self, module_name: Literal["string_utils"], auto_update: Optional[bool] = None) -> String_utilsModuleWrapper: ...
    @overload
    def include(self, module_name: Literal["networking"], auto_update: Optional[bool] = None) -> NetworkingModuleWrapper: ...
    @overload
    def include(self, module_name: Literal["data_structures"], auto_update: Optional[bool] = None) -> Data_structuresModuleWrapper: ...
    @overload
    def include(self, module_name: Literal["threading"], auto_update: Optional[bool] = None) -> ThreadingModuleWrapper: ...
    @overload
    def include(self, module_name: Literal["standard_menus"], auto_update: Optional[bool] = None) -> Standard_menusModuleWrapper: ...

    # Fallback for user-defined modules - returns generic ModuleWrapper
    def include(
        self,
        module_name: str,
        auto_update: Optional[bool] = None
    ) -> ModuleWrapper:
        """Include a C++ module.

        The returned ModuleWrapper will have attributes matching the module's
        classes, functions, and structs. VSCode autocomplete will show these
        based on the generated type stubs.

        Args:
            module_name: Name of the module to include
            auto_update: Whether to auto-rebuild if module is outdated

        Returns:
            ModuleWrapper with module-specific attributes for autocomplete
        """
        ...

    def rebuild(
        self,
        verbose: bool = False,
        clean: bool = False
    ) -> None: ...

    def list_modules(self) -> list[str]: ...
