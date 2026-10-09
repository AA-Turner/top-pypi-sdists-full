"""The v3 implementation (``configure(kane_version="v3")``).

``testmu._router`` serves every per-mode public name from here when the run is
v3. The router also reaches ``_vars`` (configure's stores), ``_reporter``
(step begin/end), ``_heal_patch`` / ``playwright_async`` (heal wrapper) and
``_helpers.gesture`` (``Locator.long_press``).

v3-only: nothing here may import ``testmu._v4`` or an old private path
(``testmu._vars`` etc. alias the v4 modules); shared modules
(``testmu._configure``, ``_config``, ``_errors``, ``_step``, ``_heal_cache``,
``_test_state``) are imported from ``testmu``.
"""
from testmu._v3._decorator import test
from testmu._v3._session import run
from testmu._v3._vars import var, set_var, get_variable_value
from testmu._v3._matchers import expect
from testmu._v3._route_failure import route_failure
from testmu._v3._helpers.condition import (
    Condition,
    ResolvedCondition,
    PossibleCondition,
    ConcatenationOperator,
)
from testmu._v3._downloads_path import downloads_path
from testmu._v3._helpers.devtools_types import (
    ApiCallEntry,
    ConsoleEntry,
    CookieEntry,
    NetworkEntry,
    RequestTiming,
)
from testmu._v3._helpers.devtools_network import (
    devtools_network_query,
    DevtoolsQueryResult,
    NetworkQueryResult,
)
from testmu._v3._helpers.devtools_console import devtools_console_query
from testmu._v3._helpers.devtools_cookies import devtools_cookies_query
from testmu._v3._helpers.devtools_storage import devtools_storage_query
from testmu._v3._helpers.api_calls import api_calls_query
from testmu._v3._helpers.clipboard import ClipboardStore, devtools_clipboard_query, install_clipboard
from testmu._v3._action_specs import as_text
from testmu._v3._devtools_capture import (
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
from testmu._v3._helpers import (
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
    verify_schema_assertion,
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
from testmu._v3 import playwright_async
from testmu._v3._vision_locator import locator
from testmu._v3._ranked_locator import resolve_ranked_locator

# Modules the router reaches into.
from testmu._v3 import _vars, _heal_patch, _helpers, _reporter
import testmu._v3._helpers.gesture  # noqa: F401 — makes _helpers.gesture an attribute
