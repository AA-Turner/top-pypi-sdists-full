from .core.cpp_api import CppApi
from .core import cssl_bridge as CSSL
from .core.cssl_bridge import (
    # Core classes
    CsslLang,
    CSSLModule,
    CSSLScript,
    CSSLFunctionModule,
    get_cssl,

    # v4.6.5: CsslWatcher
    CsslWatcher,
    watcher_get,
    watcher_set,
    get_watcher,
    list_watchers,

    # v4.9.12: Extended API
    CSSLDevConsole,
    async_console,
    async_console_sync,
    async_run,
    start_async,
    await_result,
    is_async_done,
    cancel_async,
    watch,
    unwatch,
    unwatch_all,
    breakpoint_add,
    breakpoint_remove,
    breakpoint_clear,
    step,
    continue_debug,
    get_stack,
    is_paused,
    profile,
    ProfileResult,
    validate,
    ValidationResult,
    transpile,
    serialize,
    deserialize,
    save_state,
    load_state,
    hot_reload,
    enable_hot_reload,
    disable_hot_reload,
    on,
    once,
    emit,
    off,
    off_all,
    pipe,
    CSSLPipeline,
    sandbox,
    SecurityError,
    run_with_timeout,
    memory_stats,
    MemoryStats,
    export_symbols,
    hook,
    unhook,
    unhook_all,
    inject,
    format_code,
    cssl_format,
    benchmark,
    BenchmarkResult,
    context,
    CSSLContext,

    # Sharing
    share,
    unshare,
    shared,
    get_shared,
    cleanup_shared,
)
import warnings
import os
import sys
from pathlib import Path

__version__ = "4.9.12"
__all__ = [
    "CppApi",
    "CSSL",
    # Core
    "CsslLang",
    "CSSLModule",
    "CSSLScript",
    "CSSLFunctionModule",
    "get_cssl",
    # Watcher
    "CsslWatcher",
    "watcher_get",
    "watcher_set",
    "get_watcher",
    "list_watchers",
    # v4.9.12 Extended API
    "CSSLDevConsole",
    "async_console",
    "async_console_sync",
    "async_run",
    "start_async",
    "await_result",
    "is_async_done",
    "cancel_async",
    "watch",
    "unwatch",
    "unwatch_all",
    "breakpoint_add",
    "breakpoint_remove",
    "breakpoint_clear",
    "step",
    "continue_debug",
    "get_stack",
    "is_paused",
    "profile",
    "ProfileResult",
    "validate",
    "ValidationResult",
    "transpile",
    "serialize",
    "deserialize",
    "save_state",
    "load_state",
    "hot_reload",
    "enable_hot_reload",
    "disable_hot_reload",
    "on",
    "once",
    "emit",
    "off",
    "off_all",
    "pipe",
    "CSSLPipeline",
    "sandbox",
    "SecurityError",
    "run_with_timeout",
    "memory_stats",
    "MemoryStats",
    "export_symbols",
    "hook",
    "unhook",
    "unhook_all",
    "inject",
    "format_code",
    "cssl_format",
    "benchmark",
    "BenchmarkResult",
    "context",
    "CSSLContext",
    # Sharing
    "share",
    "unshare",
    "shared",
    "get_shared",
    "cleanup_shared",
]

# Module-level cache for C++ modules
_api_instance = None
_loaded_modules = {}
_frozen_api = None  # Cached API module for frozen (PyInstaller) mode

def _is_frozen():
    """Check if running in a frozen PyInstaller bundle."""
    return getattr(sys, 'frozen', False)

def _get_frozen_api():
    """Get the bundled API module when running frozen."""
    global _frozen_api
    if _frozen_api is None:
        try:
            import importlib.util
            import importlib.machinery
            ext = '.pyd' if sys.platform == 'win32' else '.so'

            # Look for includecpp.dll in the same directory as the executable
            exe_dir = Path(sys.executable).parent
            dll_path = exe_dir / 'includecpp.dll'

            if dll_path.exists():
                # Use ExtensionFileLoader - module name must be 'api' to match PyInit_api
                loader = importlib.machinery.ExtensionFileLoader('api', str(dll_path))
                spec = importlib.util.spec_from_loader('api', loader, origin=str(dll_path))
                if spec:
                    api_module = importlib.util.module_from_spec(spec)
                    sys.modules['api'] = api_module
                    loader.exec_module(api_module)
                    _frozen_api = api_module
                    return _frozen_api

            # Fallback: try api.pyd in _MEIPASS (legacy/bundled mode)
            if hasattr(sys, '_MEIPASS'):
                meipass = sys._MEIPASS
                if meipass not in sys.path:
                    sys.path.insert(0, meipass)

                api_path = os.path.join(meipass, f'api{ext}')

                if os.path.exists(api_path):
                    loader = importlib.machinery.ExtensionFileLoader('api', api_path)
                    spec = importlib.util.spec_from_loader('api', loader, origin=api_path)
                    if spec:
                        api_module = importlib.util.module_from_spec(spec)
                        sys.modules['api'] = api_module
                        loader.exec_module(api_module)
                        _frozen_api = api_module
                        return _frozen_api

            # Fallback to regular import
            import api
            _frozen_api = api
        except Exception as e:
            # Store error for debugging
            _frozen_api = False
            print(f"[IncludeCPP] Failed to load frozen API: {e}", file=sys.stderr)
    return _frozen_api if _frozen_api else None

def _get_api():
    """Get or create singleton CppApi instance.

    Checks INCLUDECPP_PROJECT env var for project path when running
    from a different directory (e.g., via 'includecpp server run').
    """
    global _api_instance
    if _api_instance is None:
        # Check for project path from environment (set by 'server run -p')
        project_path = os.environ.get('INCLUDECPP_PROJECT')
        if project_path:
            config_path = Path(project_path) / 'cpp.proj'
            if config_path.exists():
                _api_instance = CppApi(config_path=config_path)
            else:
                _api_instance = CppApi()
        else:
            _api_instance = CppApi()
    return _api_instance

def __getattr__(name: str):
    """Enable: from includecpp import fast_list

    This hook is called when Python cannot find an attribute in this module.
    It allows dynamic C++ module loading via the import system.
    """
    if name.startswith('_'):
        raise AttributeError(f"module 'includecpp' has no attribute '{name}'")

    if name in _loaded_modules:
        return _loaded_modules[name]

    # In frozen mode (PyInstaller), try to get module from bundled api
    if _is_frozen():
        frozen_api = _get_frozen_api()
        if frozen_api and hasattr(frozen_api, name):
            module = getattr(frozen_api, name)
            _loaded_modules[name] = module
            return module
        # If not found in frozen api, raise helpful error
        raise AttributeError(
            f"Module '{name}' not found in bundled executable. "
            f"Ensure it was included during build with 'includecpp --make-exe'."
        )

    # Normal mode: use CppApi
    api = _get_api()

    if name not in api.registry:
        available = list(api.registry.keys())
        raise AttributeError(
            f"Module '{name}' not found. "
            f"Available: {available}. "
            f"Run 'includecpp rebuild' first."
        )

    if api.need_update(name):
        warnings.warn(
            f"Module '{name}' source files changed. "
            f"Run 'includecpp rebuild' to update.",
            UserWarning
        )

    module = api.include(name)
    _loaded_modules[name] = module
    return module

def __dir__():
    """List available attributes including C++ modules."""
    base = ['CppApi', 'CSSL', '__version__']
    try:
        api = _get_api()
        return sorted(set(base + list(api.registry.keys())))
    except Exception:
        return base
