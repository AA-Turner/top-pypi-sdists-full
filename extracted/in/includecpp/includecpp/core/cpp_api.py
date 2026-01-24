import os
import sys
import json
import hashlib
import warnings
import platform
from pathlib import Path
from typing import Optional, Any, Dict, TYPE_CHECKING

from .exceptions import (
    CppApiError,
    CppBuildError,
    CppModuleNotFoundError,
    CppModuleOutdatedError,
    CppReloadWarning,
    CppValidationError
)
from ..cli.config_parser import CppProjectConfig

# Import type stubs for VSCode IntelliSense (only used for type checking, not at runtime)
if TYPE_CHECKING:
    try:
        from .cpp_api_extensions import *  # type: ignore
    except ImportError:
        pass  # Stubs not generated yet

class ModuleWrapper:
    """Wrapper for C++ modules to provide getInfo() method and VSCode IntelliSense support."""

    def __init__(self, module, info: Dict[str, Any]):
        # Use object.__setattr__ to bypass our custom __setattr__ during init
        object.__setattr__(self, '_module', module)
        object.__setattr__(self, '_info', info)

        # Dynamically expose all C++ types for VSCode IntelliSense
        # This makes autocomplete work: Engine.SomeClass instead of just Engine.getInfo()
        self._expose_cpp_types()

    def _expose_cpp_types(self):
        """Dynamically expose all C++ classes, functions, and structs as attributes."""
        # Expose all attributes from the actual C++ module
        module = object.__getattribute__(self, '_module')
        if module:
            for attr_name in dir(module):
                if not attr_name.startswith('_'):
                    try:
                        attr_value = getattr(module, attr_name)
                        # Set as instance attribute so VSCode can see it
                        object.__setattr__(self, attr_name, attr_value)
                    except Exception:
                        pass  # Skip attributes that can't be accessed

    def getInfo(self) -> Dict[str, Any]:
        """Get complete module metadata including function signatures (v2.3.5+).

        Returns dictionary with structure:
        {
            "sources": List[str],
            "functions": [
                {
                    "name": str,
                    "return_type": str,
                    "parameters": [
                        {
                            "name": str,
                            "type": str,
                            "default": Optional[str],
                            "const": Optional[bool],
                            "reference": Optional[bool],
                            "pointer": Optional[bool]
                        },
                        ...
                    ],
                    "doc": Optional[str],
                    "static": Optional[bool],
                    "const": Optional[bool],
                    "inline": Optional[bool]
                },
                ...
            ],
            "classes": [
                {
                    "name": str,
                    "doc": Optional[str],
                    "methods": [
                        {"name": str, "doc": Optional[str]},
                        ...
                    ]
                },
                ...
            ],
            "structs": [...],
            "dependencies": [...]
        }

        Returns:
            Complete module metadata dictionary
        """
        return object.__getattribute__(self, '_info')

    def __getattr__(self, name):
        """Delegate attribute access to wrapped module (fallback for dynamic attributes)."""
        if name.startswith('_'):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        module = object.__getattribute__(self, '_module')
        return getattr(module, name)

    def __dir__(self):
        """Return list of attributes for autocomplete."""
        # Combine wrapper attributes with C++ module attributes
        module = object.__getattribute__(self, '_module')
        wrapper_attrs = ['getInfo']
        if module:
            module_attrs = [attr for attr in dir(module) if not attr.startswith('__')]
            return sorted(set(wrapper_attrs + module_attrs))
        return wrapper_attrs

class CppApi:
    # Inbuilt module constants
    FileSystem = "filesystem"
    Crypto = "crypto"
    JSON = "json"
    StringUtils = "string_utils"
    Networking = "networking"
    DataStructures = "data_structures"
    Threading = "threading"
    StandardMenus = "standard_menus"

    def __init__(self, verbose: bool = False, auto_update: bool = False, config_path: Optional[Path] = None):
        """Initialize C++ API.

        Args:
            verbose: Enable detailed logging
            auto_update: Auto-rebuild outdated modules on include()
            config_path: Path to cpp.proj (defaults to cwd/cpp.proj)
        """
        self.project_root = Path.cwd()
        self.config = CppProjectConfig(config_path or (self.project_root / "cpp.proj"))
        self.base_dir = self.config.base_dir
        self.registry_file = self.base_dir / ".module_registry.json"
        self.bindings_dir = self.base_dir / "bindings"

        self.verbose = verbose
        self.auto_update = auto_update
        self.silent = False

        if str(self.bindings_dir) not in sys.path:
            sys.path.insert(0, str(self.bindings_dir))

        self.registry = self._load_registry()
        self.loaded_modules = {}
        self.api_module = None
        self._import_api()

    def _load_registry(self):
        """Load module registry (v1.6 or v2.0 format)."""
        if not self.registry_file.exists():
            if self.verbose:
                print(f"[WARNING] Registry file not found: {self.registry_file}")
                print(f"[INFO] Run 'python -m includecpp rebuild' in project directory")
            return {}

        try:
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if "schema_version" in data and data["schema_version"] == "2.0":
                return data.get("modules", {})
            else:
                return data

        except Exception as e:
            if self.verbose:
                print(f"[WARNING] Failed to load registry: {e}")
            return {}

    def _save_registry(self):
        try:
            with open(self.registry_file, 'w', encoding='utf-8') as f:
                json.dump(self.registry, f, indent=2)
        except Exception:
            pass

    def _import_api(self):
        try:
            if 'api' in sys.modules:
                self.api_module = sys.modules['api']
            else:
                import api
                self.api_module = api
        except ImportError:
            if self.verbose:
                print(f"[WARNING] api module not found in {self.bindings_dir}")
                print(f"[INFO] Run 'python -m includecpp rebuild' to build C++ modules")
            self.api_module = None

    def _compute_hash(self, filepath):
        if not os.path.exists(filepath):
            return "0"

        try:
            with open(filepath, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return "0"

    def exists(self, module_name):
        if module_name not in self.registry:
            return False

        if self.api_module is None:
            return False

        try:
            return hasattr(self.api_module, module_name)
        except Exception:
            return False

    def include(self, module_name: str, auto_update: Optional[bool] = None):
        """Load a C++ module (v2.0 per-module .pyd support).

        Tries to load:
        1. Per-module .pyd: api_modulename.pyd (v2.0)
        2. Fallback to monolithic: api.modulename (v1.6 backward compatibility)

        Args:
            module_name: Name of module to load
            auto_update: Override instance auto_update setting (None = use instance setting)

        Returns:
            ModuleWrapper object with getInfo() support

        Raises:
            CppModuleNotFoundError: If module not found or not built
        """
        # Check cache first
        if module_name in self.loaded_modules:
            return self.loaded_modules[module_name]

        # Check if module is registered
        if module_name not in self.registry:
            raise CppModuleNotFoundError(
                f"Module '{module_name}' not registered.\n"
                f"Available modules: {list(self.registry.keys())}\n"
                f"Run 'python -m includecpp rebuild' to build modules."
            )

        should_auto_update = auto_update if auto_update is not None else self.auto_update
        if self.need_update(module_name):
            if not self.silent:
                print(f"[WARNING] Module '{module_name}' source is newer than build")
            if should_auto_update:
                if not self.silent:
                    print(f"[INFO] Auto-updating module '{module_name}'...")
                self.update(module_name)
            elif not self.silent:
                print(f"[INFO] Run api.update('{module_name}') to rebuild")

        module_info = self.registry.get(module_name, {})

        # Try v2.0 per-module .pyd first: api_modulename
        pyd_name = f"api_{module_name}"
        pyd_suffix = ".pyd" if platform.system() == "Windows" else ".so"
        pyd_path = self.bindings_dir / f"{pyd_name}{pyd_suffix}"

        try:
            if pyd_path.exists():
                if self.verbose:
                    print(f"[INFO] Loading per-module .pyd: {pyd_name}")

                imported = __import__(pyd_name)
                wrapped = ModuleWrapper(imported, module_info)
                self.loaded_modules[module_name] = wrapped
                return wrapped

        except ImportError as e:
            if self.verbose:
                print(f"[WARNING] Failed to import {pyd_name}: {e}")
                print(f"[INFO] Falling back to monolithic api module")

        # Fallback to v1.6 monolithic api module
        if self.api_module is None:
            raise CppModuleNotFoundError(
                f"Module '{module_name}' not built.\n"
                f"Expected: {pyd_path} or api{pyd_suffix}\n"
                f"Run 'python -m includecpp rebuild' to build."
            )

        try:
            # v1.6: Access from monolithic api module
            module = getattr(self.api_module, module_name)
            wrapped = ModuleWrapper(module, module_info)
            self.loaded_modules[module_name] = wrapped
            return wrapped

        except AttributeError:
            raise CppModuleNotFoundError(
                f"Module '{module_name}' not found.\n"
                f"Neither {pyd_name}{pyd_suffix} nor api.{module_name} exists.\n"
                f"Run 'python -m includecpp rebuild' to build."
            )

    def noFeedback(self):
        """Disable all warnings and feedback messages."""
        self.silent = True

    def need_update(self, module_name: str) -> bool:
        """Check if module needs rebuild by comparing source file hashes.

        Supports both v2.3.5 (source_hashes) and v1.6 (hashes) registry formats.
        """
        if module_name not in self.registry:
            return True

        module_info = self.registry[module_name]
        sources = module_info.get('sources', [])

        # Try v2.3.5 format first, fall back to v1.6 format
        stored_hashes = module_info.get('source_hashes', module_info.get('hashes', {}))

        # If no hashes stored at all, rebuild needed
        if not stored_hashes:
            return True

        for source in sources:
            source_path = self.project_root / source
            current_hash = self._compute_hash(str(source_path))

            # Try exact source path first, then just filename (v1.6 compatibility)
            stored_hash = stored_hashes.get(source, stored_hashes.get(Path(source).name, None))

            # If no hash found for this source, rebuild needed
            if stored_hash is None:
                return True

            # Handle hash length mismatch (v1.6 = 16 chars, v2.3.5 = 64 chars)
            if len(stored_hash) == 16 and len(current_hash) == 64:
                # Compare first 16 chars for backwards compatibility
                if current_hash[:16] != stored_hash:
                    return True
            elif current_hash != stored_hash:
                return True

        return False

    def update(self, module_name: str, verbose: Optional[bool] = None):
        from .build_manager import BuildManager
        if verbose is None:
            verbose = self.verbose
        if module_name not in self.registry:
            raise CppModuleNotFoundError(f"Module '{module_name}' not found in registry")
        builder = BuildManager(self.project_root, self.base_dir, self.config)
        success = builder.rebuild(
            modules=[module_name],
            incremental=True,
            parallel=False,
            clean=False,
            verbose=verbose
        )
        if success:
            self.registry = self._load_registry()
            if module_name in self.loaded_modules:
                del self.loaded_modules[module_name]
            if not self.silent and verbose:
                print(f"[INFO] Module '{module_name}' rebuilt successfully")
        else:
            raise CppBuildError(f"Failed to rebuild module '{module_name}'")

    def list_modules(self):
        return list(self.registry.keys())

    def get_module_info(self, module_name):
        if module_name not in self.registry:
            return None

        return self.registry[module_name]
