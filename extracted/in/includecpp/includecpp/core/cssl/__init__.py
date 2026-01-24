"""
CSSL - C-Style Scripting Language
Bundled with IncludeCPP for integrated scripting support.

Features:
- BruteForce Injection System: <==, ==>, +<==, -<==, <<==, ==>>
- Dynamic typing with 'dynamic' keyword
- Function modifiers: undefined, open, meta, super, closed, private, virtual
- Advanced data types: datastruct, shuffled, iterator, combo, dataspace
- Injection helpers: string::where, json::key, array::index, etc.
- Global references: @Name, r@Name, s@Name

Performance:
- C++ acceleration via bundled cssl_core module (375x+ speedup)
- Pre-built binaries bundled in PyPI package for instant use
- Auto-rebuilds if bundled module doesn't match platform (once)
- Use is_cpp_available() to check if C++ module is loaded
"""

import os
import sys
import importlib.util
from pathlib import Path
from typing import Optional

# C++ acceleration state
_CPP_AVAILABLE = False
_cpp_module = None
_CPP_LOAD_SOURCE = None  # 'bundled', 'rebuilt', None
_CPP_MODULE_PATH = None


def _load_module_from_path(path: Path) -> Optional[object]:
    """
    Load a Python extension module from file path.

    IncludeCPP builds modules with 'api' as the export name, containing
    submodules for each plugin. We load the 'api' module and return the
    'cssl_core' submodule.

    Args:
        path: Path to .pyd/.so module file

    Returns:
        Loaded cssl_core submodule, or None if loading failed
    """
    dll_handle = None
    try:
        # On Windows, add DLL directory to search path (for MinGW runtime DLLs)
        if sys.platform == 'win32' and hasattr(os, 'add_dll_directory'):
            dll_dir = path.parent
            if dll_dir.exists():
                dll_handle = os.add_dll_directory(str(dll_dir))

        # IncludeCPP exports as 'api', with plugins as submodules
        spec = importlib.util.spec_from_file_location('api', str(path))
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # Return the cssl_core submodule
            if hasattr(module, 'cssl_core'):
                return module.cssl_core
            return module
    except Exception:
        pass
    finally:
        # Clean up DLL directory handle
        if dll_handle is not None:
            try:
                dll_handle.close()
            except Exception:
                pass
    return None


def _try_load_bundled() -> bool:
    """
    Try to load bundled module from PyPI package directory.

    CSSL bundles pre-built modules in includecpp/core/cssl/cpp/build/
    so users get instant C++ acceleration without compiling.

    Returns:
        True if module loaded successfully
    """
    global _CPP_AVAILABLE, _cpp_module, _CPP_LOAD_SOURCE, _CPP_MODULE_PATH

    try:
        from .cssl_compiler import CSSLCompilerConfig, get_cssl_bundled_dir

        config = CSSLCompilerConfig()
        config.setup_first_run()

        suffixes = config.get_all_possible_suffixes()
        build_dir = get_cssl_bundled_dir()

        if not build_dir.exists():
            return False

        # Check for cssl_core.{suffix}
        for suffix in suffixes:
            module_path = build_dir / f'cssl_core{suffix}'
            if module_path.exists():
                module = _load_module_from_path(module_path)
                if module:
                    _cpp_module = module
                    _CPP_AVAILABLE = True
                    _CPP_LOAD_SOURCE = 'bundled'
                    _CPP_MODULE_PATH = str(module_path)
                    return True

        # Check for api.pyd (IncludeCPP format)
        api_path = build_dir / 'api.pyd'
        if not api_path.exists():
            api_path = build_dir / 'api.so'
        if api_path.exists():
            module = _load_module_from_path(api_path)
            if module:
                _cpp_module = module
                _CPP_AVAILABLE = True
                _CPP_LOAD_SOURCE = 'bundled'
                _CPP_MODULE_PATH = str(api_path)
                return True

    except ImportError:
        pass

    return False


def _try_auto_rebuild() -> bool:
    """
    Auto-rebuild module if bundled version not available.

    CSSL is special: if no bundled module matches the user's platform,
    it automatically rebuilds ONCE to the bundled folder.

    Returns:
        True if rebuild succeeded and module loaded
    """
    global _CPP_AVAILABLE, _cpp_module, _CPP_LOAD_SOURCE, _CPP_MODULE_PATH

    try:
        from .cssl_compiler import compile_cssl_core, CSSLCompilerConfig

        config = CSSLCompilerConfig()
        if not config.can_compile():
            return False

        # Rebuild to bundled folder
        module_path = compile_cssl_core(force=True)
        if module_path and module_path.exists():
            module = _load_module_from_path(module_path)
            if module:
                _cpp_module = module
                _CPP_AVAILABLE = True
                _CPP_LOAD_SOURCE = 'rebuilt'
                _CPP_MODULE_PATH = str(module_path)
                return True

    except ImportError:
        pass

    return False


def _initialize_cpp_module():
    """
    Initialize C++ module for CSSL.

    CSSL special handling:
    1. Try bundled module from PyPI package (instant use)
    2. If not found, auto-rebuild to bundled folder (once)
    """
    # Try bundled first (most users)
    if _try_load_bundled():
        return

    # No bundled module - try auto-rebuild
    _try_auto_rebuild()


# Initialize on import
_initialize_cpp_module()


# =============================================================================
# Public API
# =============================================================================

def is_cpp_available() -> bool:
    """Check if C++ acceleration is available."""
    return _CPP_AVAILABLE


def get_cpp_version() -> Optional[str]:
    """Get C++ module version, or None if not available."""
    if _CPP_AVAILABLE and _cpp_module and hasattr(_cpp_module, 'version'):
        try:
            return _cpp_module.version()
        except Exception:
            pass
    return None


def get_cpp_platform() -> Optional[str]:
    """Get the platform the C++ module was loaded for."""
    return sys.platform if _CPP_AVAILABLE else None


def get_cpp_info() -> dict:
    """
    Get detailed C++ acceleration info.

    Returns:
        dict with keys:
        - available: bool - whether C++ is available
        - source: str - where module was loaded from ('bundled', 'rebuilt')
        - version: str - module version
        - module_path: str - path to loaded module
        - platform: dict - platform info
        - can_compile: bool - whether compilation is possible
    """
    result = {
        'available': _CPP_AVAILABLE,
        'source': _CPP_LOAD_SOURCE,
        'version': get_cpp_version(),
        'module_path': _CPP_MODULE_PATH,
    }

    try:
        from .cssl_compiler import CSSLCompilerConfig
        config = CSSLCompilerConfig()
        result['platform'] = config.get_platform_info()
        result['compiler'] = config.get_compiler()
        result['can_compile'] = config.can_compile()
    except ImportError:
        result['platform'] = {'platform': sys.platform}
        result['compiler'] = None
        result['can_compile'] = False

    return result


def compile_cpp_module(force: bool = False) -> bool:
    """
    Manually trigger C++ module compilation.

    Compiles to the bundled folder so it's available for future imports.

    Args:
        force: If True, recompile even if module exists

    Returns:
        True if compilation succeeded
    """
    global _CPP_AVAILABLE, _cpp_module, _CPP_LOAD_SOURCE, _CPP_MODULE_PATH

    try:
        from .cssl_compiler import compile_cssl_core

        module_path = compile_cssl_core(force=force)
        if module_path and module_path.exists():
            module = _load_module_from_path(module_path)
            if module:
                _cpp_module = module
                _CPP_AVAILABLE = True
                _CPP_LOAD_SOURCE = 'rebuilt'
                _CPP_MODULE_PATH = str(module_path)
                return True
    except ImportError:
        pass

    return False


# =============================================================================
# Import CSSL modules
# =============================================================================

from .cssl_parser import (
    parse_cssl, parse_cssl_program, tokenize_cssl,
    CSSLSyntaxError, CSSLLexer, CSSLParser, ASTNode,
    KEYWORDS, TYPE_GENERICS, TYPE_PARAM_FUNCTIONS, INJECTION_HELPERS
)
from .cssl_runtime import (
    CSSLRuntime, CSSLRuntimeError, CSSLServiceRunner, run_cssl, run_cssl_file,
    register_filter, unregister_filter, get_custom_filters
)
from .cssl_types import (
    DataStruct, Shuffled, Iterator, Combo, DataSpace, OpenQuote,
    OpenFind, Parameter, Stack, Vector, Array,
    create_datastruct, create_shuffled, create_iterator,
    create_combo, create_dataspace, create_openquote, create_parameter,
    create_stack, create_vector, create_array
)


# =============================================================================
# Fast tokenize with C++ acceleration
# =============================================================================

def fast_tokenize(source: str):
    """
    Tokenize CSSL source code.

    Uses C++ Lexer if available (10-20x faster), otherwise Python.

    Args:
        source: CSSL source code string

    Returns:
        List of tokens
    """
    if _CPP_AVAILABLE and _cpp_module and hasattr(_cpp_module, 'Lexer'):
        try:
            lexer = _cpp_module.Lexer(source)
            return lexer.tokenize()
        except Exception:
            pass
    return tokenize_cssl(source)


# =============================================================================
# Optimizer - Smart Performance System
# =============================================================================

from .cssl_optimizer import (
    run_optimized, get_optimizer_stats, configure_optimizer, clear_cache,
    get_optimized_ops, precompile, PrecompiledPattern,
    OptimizedOperations, OptimizedRuntime, ASTCache,
    ExecutionContext, PerformanceThresholds, THRESHOLDS, OPS
)


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    # C++ Acceleration
    'is_cpp_available', 'get_cpp_version', 'get_cpp_platform', 'get_cpp_info',
    'fast_tokenize', 'compile_cpp_module',
    # Optimizer (NEW)
    'run_optimized', 'get_optimizer_stats', 'configure_optimizer', 'clear_cache',
    'get_optimized_ops', 'precompile', 'PrecompiledPattern',
    'OptimizedOperations', 'OptimizedRuntime', 'ASTCache',
    'ExecutionContext', 'PerformanceThresholds', 'THRESHOLDS', 'OPS',
    # Parser
    'parse_cssl', 'parse_cssl_program', 'tokenize_cssl',
    'CSSLSyntaxError', 'CSSLLexer', 'CSSLParser', 'ASTNode',
    'KEYWORDS', 'TYPE_GENERICS', 'TYPE_PARAM_FUNCTIONS', 'INJECTION_HELPERS',
    # Runtime
    'CSSLRuntime', 'CSSLRuntimeError', 'CSSLServiceRunner',
    'run_cssl', 'run_cssl_file',
    # Filter Registration
    'register_filter', 'unregister_filter', 'get_custom_filters',
    # Data Types
    'DataStruct', 'Shuffled', 'Iterator', 'Combo', 'DataSpace', 'OpenQuote',
    'OpenFind', 'Parameter', 'Stack', 'Vector', 'Array',
    'create_datastruct', 'create_shuffled', 'create_iterator',
    'create_combo', 'create_dataspace', 'create_openquote', 'create_parameter',
    'create_stack', 'create_vector', 'create_array'
]
