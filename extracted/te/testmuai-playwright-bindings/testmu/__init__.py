"""TestMu binding for Playwright Python.

Public API:
    testmu.test          — decorator for test functions
    testmu.step(...)     — step context manager
    testmu.run(fn)       — session lifecycle runner
    var(template)        — variable/template resolver
    set_var(name, value) — store variable
    expect               — PW expect with custom matchers
    testmu.<helper>(...)  — helper functions (execute_js, vision_query, etc.)
"""

from importlib.metadata import PackageNotFoundError, version as _pkg_version

# Old private paths (testmu._vars, testmu._helpers.x, …) alias the v4 modules.
# Installed first so every import below, and any made by the host, resolves them.
from testmu import _aliases

_aliases.install()

try:
    __version__ = _pkg_version("testmuai-playwright-bindings")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

# Load .env BEFORE any submodule import so module-level os.getenv() reads
# (in _config, _helpers/vision, etc.) see values from a developer's local
# .env file. On HyperExecute env vars are injected by the platform, so
# python-dotenv is absent there and this is a no-op.
#
# Use find_dotenv(usecwd=True) — walks up from the user's cwd to find a .env.
# The default load_dotenv() walks up from this file's location instead, which
# lives in site-packages and never reaches the user's project root.
try:
    from dotenv import load_dotenv as _load_dotenv, find_dotenv as _find_dotenv
    _load_dotenv(_find_dotenv(usecwd=True))
except ImportError:
    pass

from typing import TYPE_CHECKING

# --- shared: one of each, whatever the mode -------------------------------------
from testmu._configure import configure
from testmu._step import step
from testmu._errors import TestmuConfigError, AutohealExhausted, LoopExhausted
# Classes identical in every mode: the real class, not routed.
from testmu._condition_enums import ConcatenationOperator, PossibleCondition
from testmu._devtools_types import (
    ApiCallEntry, ConsoleEntry, CookieEntry, DevtoolsQueryResult, NetworkEntry,
    NetworkQueryResult, RequestTiming,
)
from testmu._clipboard_store import ClipboardStore

# --- per mode: served by testmu._v4 / testmu._v3 on each call ---------------------
# configure(kane_version="v3") switches every name below to the v3 implementation.
# They're forwarders (see testmu._router), so names imported before configure()
# runs (``from testmu import var``) still follow the mode.
from testmu import _router

_router.load_impls()
globals().update(_router.build_public_namespace())
_router.install_heal()

if TYPE_CHECKING:  # the real objects, for type checkers and IDEs
    from testmu._v4 import *  # noqa: F401,F403
    from testmu._v4 import (  # noqa: F401
        api_calls_query, clear_api_call_log,
        devtoolsConsoleQuery, devtoolsCookiesQuery, devtoolsNetworkQuery,
        devtoolsPerformanceQuery, devtoolsStorageQuery, devtools_clipboard_query,
        get_api_call_log, install_clipboard, snapshotPerformanceTrace, textual_analyzer,
    )



def __getattr__(name):
    """``testmu._vars`` etc. as attributes: see testmu._aliases."""
    return _aliases.package_getattr(name)


__all__ = [
    "__version__",
    "configure",
    "test",
    "step",
    "run",
    "var",
    "set_var",
    "expect",
    "execute_js",
    "execute_api",
    "execute_db",
    "vision_query",
    "textual_query",
    "vision_wait",
    "vision_action",
    "verify_assertion",
    "verify_schema_assertion",
    "evaluate_branch",
    "LoopExhausted",
    "network_query",
    "evaluate_network_assertion",
    "evaluate_math",
    "smartui_snapshot",
    "switch_tab",
    "click_drag",
    "new_tab",
    "close_tab",
    "ensure_active_page",
    "drag_drop",
    "element_drag",
    "multi_click",
    "long_press",
    "downloads_path",
    "execute_kane_cli",
    "check_until_condition",
    "get_vision_coordinates",
    "TestmuConfigError",
    "NetworkEntry",
    "RequestTiming",
    "ConsoleEntry",
    "CookieEntry",
    "devtools_network_query",
    "DevtoolsQueryResult",
    "NetworkQueryResult",
    "devtools_console_query",
    "devtools_cookies_query",
    "devtools_storage_query",
    "clipboardWrite",
    "clipboardPaste",
    "clipboardClear",
    "devtoolsClipboardQuery",
    "as_text",
    # Version-gated public API (additive — only active when kane_version == "v3")
    "scroll_until_element",
    "locator",
    "resolve_ranked_locator",
    "route_failure",
    "get_variable_value",
    "Condition",
    "ResolvedCondition",
    "PossibleCondition",
    "ConcatenationOperator",
    "get_cookies",
    "prime_dialog",
    "AutohealExhausted",
    # Derivation recompute helpers (recorded code_js re-evaluation)
    "derive",
    "condition_compute",
]
