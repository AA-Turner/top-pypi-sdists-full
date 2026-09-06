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

from testmu._configure import configure
from testmu._decorator import test
from testmu._step import step
from testmu._session import run
from testmu._vars import var, set_var, get_variable_value
from testmu._matchers import expect
from testmu._errors import TestmuConfigError, AutohealExhausted
from testmu._route_failure import route_failure
from testmu._helpers.condition import (
    Condition,
    ResolvedCondition,
    PossibleCondition,
    ConcatenationOperator,
)
from testmu._downloads_path import downloads_path
from testmu._helpers.devtools_types import NetworkEntry, RequestTiming, ConsoleEntry, CookieEntry
from testmu._helpers.devtools_network import devtools_network_query, DevtoolsQueryResult, NetworkQueryResult
from testmu._helpers.devtools_console import devtools_console_query
from testmu._helpers.devtools_cookies import devtools_cookies_query
from testmu._helpers.devtools_storage import devtools_storage_query
from testmu._helpers.devtools_types import ApiCallEntry
from testmu._helpers.api_calls import api_calls_query
from testmu._helpers.clipboard import ClipboardStore, devtools_clipboard_query, install_clipboard
# Text coercion for fill/type values — public because generated tests wrap
# their fill/type argument in it (the value may be a type-preserved var()
# lookup or a raw execute_js result). TS twin: asText, exported from index.ts.
from testmu._action_specs import as_text
from testmu._devtools_capture import (
    devtoolsNetworkQuery,
    devtoolsConsoleQuery,
    devtoolsCookiesQuery,
    devtoolsStorageQuery,
    clipboardWrite,
    clipboardPaste,
    clipboardClear,
    devtoolsClipboardQuery,
    devtoolsPerformanceQuery,
    snapshotPerformanceTrace,
)

# Helpers — vision functions and remaining helpers
from testmu._helpers import (
    execute_js,
    execute_api,
    get_api_call_log,
    clear_api_call_log,
    execute_db,
    vision_query,
    textual_query,
    vision_wait,
    vision_action,
    verify_assertion,
    evaluate_branch,
    network_query,
    evaluate_network_assertion,
    evaluate_math,
    smartui_snapshot,
    new_tab,
    switch_tab,
    close_tab,
    ensure_active_page,
    click_drag,
    drag_drop,
    element_drag,
    multi_click,
    long_press,
    execute_kane_cli,
    check_until_condition,
    get_vision_coordinates,
    scroll_until_element,
    textual_analyzer,
    derive,
    condition_compute,
    get_cookies,
    prime_dialog,
)

# Install PW-specific heal patch
import testmu.playwright_async  # noqa: F401 — triggers _install_heal()

# Empty-selector entry point — emit
#   `await testmu.locator(page, description='X').<verb>(...)`
# Imported after the heal patch install to avoid an import-time cycle.
from testmu._vision_locator import locator

# Ranked multi-selector resolution — emit
#   `await testmu.resolve_ranked_locator(page, [page.locator(...), ...], description='X')`
# Owns the wrong-element heal wrapper so the generated body stays thin
# (imported, not inlined into every test). Depends on `locator` above.
from testmu._ranked_locator import resolve_ranked_locator

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
    "evaluate_branch",
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
