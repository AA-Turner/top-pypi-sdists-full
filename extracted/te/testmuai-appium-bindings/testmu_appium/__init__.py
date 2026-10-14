"""testmu_appium — Appium runtime bindings for generated mobile tests.

Public API (consumed by codegen-emitted test.py):

    configure(**kwargs)          — set test config at module top
    @testmu_appium.test          — decorator for the test function
    testmu_appium.run(fn)        — session lifecycle (local Appium / LT mobile hub)
    open_session(entry, ...), close_session(status) — the same session, owned by a host process
    testmu_appium.step(...)      — step context manager
    var(template), set_var(name, value) — variable store + template substitution

    Element verbs (settle → find → act → heal):
        click, type, search, clear, select, scroll, scroll_until
    Driver verbs (no find, no heal, no selectors):
        navigate, keyevent, app_lifecycle, device_control, device_control_query, set_geolocation, wait, drag,
        smartui_screenshot, set_cookies, delete_cookies, clear_cookies,
        set_local_storage, delete_local_storage, clear_local_storage,
        set_clipboard, paste_clipboard, clear_clipboard, go_back, go_forward,
        refresh, new_tab, switch_tab, close_tab, accessibility_scan,
        inject_media, network_throttle, network_mock
    Value / query verbs:
        verify_assertion, evaluate_math, textual_analyzer, textual_analyzer_authoring,
        vision_query, execute_api, execute_js, execute_db, network_query,
        network_capture_query, network_capture_capabilities,
        evaluate_network_assertion, check_until_condition
        (deprecated: textual_query — superseded by textual_analyzer; kept only for
        tapes that already record it)

    `network_capture_query` is the versioned network.capture.v1 entry point;
    `network_query` remains its legacy flat-argument compatibility wrapper.
    `verify_assertion` / `evaluate_math` take the RECORDED tree the generator
    emits; `assertion` / `math` are the flat-argument forms behind them.

Sync API. Single driver per test. Appium-only. Platform mechanics — strategy
compilation, keycode maps, picker machinery, session options — are runtime data
tables keyed off the configured platform, so the generated test.py stays portable
across Android and iOS.

The binding does NOT load a .env or mutate os.environ on import; the host runtime
injects env vars itself.
"""
from importlib.metadata import PackageNotFoundError, version as _pkg_version

# Old module paths (testmu_appium._vars, testmu_appium.perception, …) alias the
# v4 modules. Installed first so every import below, and any made by the host,
# resolves them.
from testmu_appium import _aliases

_aliases.install()

try:
    __version__ = _pkg_version("testmuai-appium-bindings")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

# Lifecycle
from testmu_appium._configure import configure
from typing import TYPE_CHECKING

# --- shared: one of each, whatever the mode ---------------------------------------
from testmu_appium._step import step

# --- per mode: served by testmu_appium._v4 (and a future _v3) on each call ------------
# They're forwarders (see testmu_appium._router), so names imported before
# configure() runs still follow the mode.
from testmu_appium import _router

_router.load_impls()
globals().update(_router.build_public_namespace())

if TYPE_CHECKING:  # the real objects, for type checkers and IDEs
    from testmu_appium._v4 import *  # noqa: F401,F403

from testmu_appium._errors import (  # shared: `except` needs the real classes
    TestmuConfigError,
    UnsupportedOnPlatform,
    UnknownStrategy,
    UnknownKeyEvent,
    ElementNotFound,
    ElementBlocked,
    CoordinateFallbackUnavailable,
    SmartUINotAvailable,
    PickerModeNotSupported,
    NetworkQueryUnavailable,
    NetworkMockUnavailable,
    ScreenshotUnavailable,
    WebSurfaceUnavailable,
    ViewportCaptureError,
    DegenerateViewportCaptureError,
    UnsupportedTreeContract,
    ViewportSelectionDriftError,
    ViewportResultMissError,
    ViewportScriptCompileError,
    ViewportScriptPolicyError,
    ViewportScriptTimeoutError,
    ViewportScriptRuntimeError,
    ViewportResultTypeError,
    NetworkCaptureError,
    NetworkCaptureUnavailable,
    NetworkCaptureTimeout,
    NetworkCaptureNotFound,
    NetworkCaptureContractError,
    NetworkAssertionError,
)

# `type` is routed like every other verb (see ROUTED_NAMES), so codegen's
# `testmu_appium.type(...)` works; it only shadows the builtin for
# `from testmu_appium import type`, which codegen never does.




def __getattr__(name):
    """``testmu_appium._vars`` etc. as attributes: see testmu_appium._aliases."""
    return _aliases.package_getattr(name)


__all__ = [
    # Lifecycle
    "configure", "test_config_overrides", "test", "run", "step",
    "open_session", "close_session",
    "var", "set_var", "get_variable_value", "resolve_variable",
    "route_failure", "get_driver",
    # Perception
    "parse_tree", "format_for_prompt", "find_by_fingerprint", "position_hint",
    "ELEMENT_CONTRACT",
    # Element verbs
    "click", "type", "search", "clear", "select", "scroll", "scroll_until",
    # Driver verbs
    "navigate", "keyevent", "app_lifecycle", "device_control", "device_control_query", "set_geolocation", "wait", "drag",
    "smartui_screenshot",
    "set_cookies", "delete_cookies", "clear_cookies",
    "set_local_storage", "delete_local_storage", "clear_local_storage",
    "set_clipboard", "paste_clipboard", "clear_clipboard",
    "go_back", "go_forward", "refresh", "accessibility_scan",
    "get_tabs", "new_tab", "switch_tab", "close_tab",
    "inject_media", "network_throttle", "network_mock",
    # Value / query verbs
    "verify_assertion", "verify_schema_assertion", "evaluate_math", "assertion", "evaluate_branch", "math",
    "textual_query", "vision_query", "check_until_condition", "execute_kane_cli",
    "execute_api", "execute_js", "execute_db", "network_query", "network_capture_query",
    "network_capture_capabilities", "evaluate_network_assertion",
    "textual_analyzer", "textual_analyzer_authoring",
    # Heal outcomes
    "HealHit", "HealNoMatch", "HealUnavailable", "HealDisabled", "HealProtocolError",
    # Exceptions
    "TestmuConfigError", "UnsupportedOnPlatform", "UnknownStrategy", "UnknownKeyEvent",
    "ElementNotFound", "ElementBlocked", "CoordinateFallbackUnavailable",
    "SmartUINotAvailable", "PickerModeNotSupported", "NetworkQueryUnavailable",
    "NetworkMockUnavailable",
    "ScreenshotUnavailable",
    "WebSurfaceUnavailable",
    "ViewportCaptureError", "DegenerateViewportCaptureError", "UnsupportedTreeContract",
    "ViewportSelectionDriftError", "ViewportResultMissError", "ViewportScriptCompileError",
    "ViewportScriptPolicyError", "ViewportScriptTimeoutError",
    "ViewportScriptRuntimeError", "ViewportResultTypeError",
    "NetworkCaptureError", "NetworkCaptureUnavailable", "NetworkCaptureTimeout",
    "NetworkCaptureNotFound", "NetworkCaptureContractError", "NetworkAssertionError",
]
