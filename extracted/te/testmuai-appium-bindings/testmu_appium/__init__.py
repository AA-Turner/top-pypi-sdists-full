"""testmu_appium — Appium runtime bindings for generated mobile tests.

Public API (consumed by codegen-emitted test.py):

    configure(**kwargs)          — set test config at module top
    @testmu_appium.test          — decorator for the test function
    testmu_appium.run(fn)        — session lifecycle (local Appium / LT mobile hub)
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

try:
    __version__ = _pkg_version("testmuai-appium-bindings")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

# Lifecycle
from testmu_appium._configure import configure
from testmu_appium._test_config import test_config_overrides
from testmu_appium._decorator import test
from testmu_appium._session import run
from testmu_appium._step import step
from testmu_appium._vars import var, set_var, get_variable_value, resolve_variable
from testmu_appium._route_failure import route_failure
from testmu_appium._helpers.driver import get_driver
from testmu_appium._timing import capture_action_timings
from testmu_appium.perception import (
    ELEMENT_CONTRACT,
    find_by_fingerprint,
    format_for_prompt,
    parse_tree,
    position_hint,
)

# Element verbs — find + heal + act
from testmu_appium._action_click import click
from testmu_appium._action_type import type as _type, search, clear
from testmu_appium._action_select import select
from testmu_appium._action_scroll import scroll
from testmu_appium._action_scroll_until import scroll_until
from testmu_appium._action_drag import drag

# Driver verbs — act on the session
from testmu_appium._helpers.navigate import navigate
from testmu_appium._helpers.keyevent import keyevent
from testmu_appium._helpers.app_lifecycle import app_lifecycle
from testmu_appium._helpers.device_control import device_control, device_control_query
from testmu_appium._helpers.geolocation import set_geolocation
from testmu_appium._helpers.wait import wait
from testmu_appium._helpers.smartui import smartui_screenshot
from testmu_appium._helpers.cookies import set_cookies, delete_cookies, clear_cookies
from testmu_appium._helpers.local_storage import (
    set_local_storage, delete_local_storage, clear_local_storage,
)
from testmu_appium._helpers.clipboard import (
    set_clipboard, paste_clipboard, clear_clipboard,
)
from testmu_appium._helpers.navigation_history import go_back, go_forward
from testmu_appium._helpers.refresh import refresh
from testmu_appium._helpers.accessibility import accessibility_scan
from testmu_appium._helpers.tabs import get_tabs, new_tab, switch_tab, close_tab
from testmu_appium._helpers.media_injection import inject_media
from testmu_appium._helpers.network_throttle import network_throttle
from testmu_appium._helpers.network_mock import network_mock

# Value / query verbs
from testmu_appium._helpers.assertion import assertion, evaluate_branch
from testmu_appium._helpers.math import math
from testmu_appium._helpers.verify_assertion import verify_assertion
from testmu_appium._helpers.evaluate_math import evaluate_math
from testmu_appium._helpers.condition import check_until_condition
from testmu_appium._helpers.kane_cli import execute_kane_cli
from testmu_appium._helpers.textual_query import textual_query
from testmu_appium._helpers.vision_query import vision_query
from testmu_appium._helpers.execute_api import execute_api
from testmu_appium._helpers.execute_js import execute_js
from testmu_appium._helpers.execute_db import execute_db
from testmu_appium._helpers.textual_analyzer import (
    textual_analyzer,
    textual_analyzer_authoring,
)
from testmu_appium._helpers.network_query import (
    network_query,
    network_capture_query,
    network_capture_capabilities,
    evaluate_network_assertion,
    NetworkCaptureError,
    NetworkCaptureUnavailable,
    NetworkCaptureTimeout,
    NetworkCaptureNotFound,
    NetworkCaptureContractError,
    NetworkAssertionError,
)

# Heal outcomes — exported so a host runtime can introspect a heal result
from testmu_appium._heal import (
    HealDisabled, HealHit, HealNoMatch, HealProtocolError, HealUnavailable,
)

from testmu_appium._errors import (
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
)

# Bound at module level so codegen can emit `testmu_appium.type(...)`. This only
# shadows the builtin for `from testmu_appium import type`, which codegen never does.
type = _type  # noqa: A001


__all__ = [
    # Lifecycle
    "configure", "test_config_overrides", "test", "run", "step",
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
    "verify_assertion", "evaluate_math", "assertion", "evaluate_branch", "math",
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
