"""testmu_selenium — Selenium runtime bindings for generated tests.

Public API (consumed by codegen-emitted test.py):
    configure(**kwargs)           — set test config at module top
    @testmu_selenium.test         — decorator for test function
    testmu_selenium.run(fn)       — single-driver session lifecycle
    testmu_selenium.step(...)     — step context manager
    var(template), set_var(name, value) — variable store + template substitution
    findElement, clickElement, input_value, executeJS, visionQuery — runtime helpers
    _heal_cascade(...) → HealResult  — autoheal cascade dispatcher
    Public exception classes: TestmuConfigError, AutohealExhausted, ClickAllMethodsFailed

Sync API. Single driver per test. Selenium-only.
"""
from importlib.metadata import PackageNotFoundError, version as _pkg_version

try:
    __version__ = _pkg_version("testmuai-selenium-bindings")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

# NOTE: the binding intentionally does NOT load a .env / mutate os.environ on
# import. The host runtime (HyperExecute) injects env vars itself; for
# local standalone runs, export the vars or load your .env before invoking the
# test. Resolution reads env vars but never writes them.

from testmu_selenium._configure import configure
from testmu_selenium._decorator import test
from testmu_selenium._session import run
from testmu_selenium._step import step
from testmu_selenium._vars import var, set_var, get_variable_value, resolve_variable
from testmu_selenium._heal_cascade import _heal_cascade, HealResult
from testmu_selenium._route_failure import route_failure
from testmu_selenium._test_config import load_test_config
from testmu_selenium._errors import (
    TestmuConfigError, AutohealExhausted, HealTierMiss, HealAuthError, ClickAllMethodsFailed,
)

# Helpers re-exported at top level (codegen emits these as bare names)
from testmu_selenium._helpers.click import clickElement, add_clickElement_to_webelement
from testmu_selenium._helpers.find_element import findElement
from testmu_selenium._helpers.driver import get_driver
from testmu_selenium._helpers.input_value import input_value
from testmu_selenium._helpers.execute_js import executeJS
from testmu_selenium._helpers.vision_query import visionQuery
from testmu_selenium._helpers.textual_query import textualQuery
from testmu_selenium._helpers.smartui import smartui_snapshot

# Auto-monkey-patch WebElement on package import — generated test.py expects el.clickElement(...)
add_clickElement_to_webelement()

# Additional monkey-patches if available
try:
    from testmu_selenium._helpers.input_value import add_input_value_to_webelement
    add_input_value_to_webelement()
except ImportError:
    pass

try:
    from testmu_selenium._helpers.clear_element import add_clear_element_to_webelement
    add_clear_element_to_webelement()
except ImportError:
    pass

# High-level action wrappers — single-call replacements for the codegen-emitted
# retry+heal loops. Imported AFTER the WebElement monkey-patches so the runners
# can rely on el.clickElement / el.input_value being present.
from testmu_selenium._action_click import click
from testmu_selenium._action_type import type as _type
from testmu_selenium._action_textual_query import textual_query
from testmu_selenium._action_search import search
from testmu_selenium._action_hover import hover
from testmu_selenium._action_clear import clear
from testmu_selenium._action_set_input_files import set_input_files
from testmu_selenium._action_press_key import press_key
from testmu_selenium._action_scroll_into_view import scroll_into_view
from testmu_selenium._action_scroll_until_element import scroll_until_element
from testmu_selenium._action_drag_drop import drag_drop
from testmu_selenium._action_element_drag import element_drag
from testmu_selenium._helpers.drag_at_coordinate import drag_at_coordinate
from testmu_selenium._helpers.clear_at_coordinate import clear_at_coordinate
from testmu_selenium._helpers.navigate import navigate
from testmu_selenium._helpers.wait import wait, wait_until, wait_for_load, check_until_condition

# Codegen emits the bare camelCase name in test.py — alias matches V4 convention.
checkUntilCondition = check_until_condition
from testmu_selenium._helpers.tabs import new_tab, switch_tab, close_tab
from testmu_selenium._helpers.scroll import scroll
from testmu_selenium._helpers.navigation import refresh, go_back, go_forward
from testmu_selenium._helpers.dialog import handle_alert
from testmu_selenium._helpers.url import get_url, get_title
from testmu_selenium._helpers.math import evaluate_math
from testmu_selenium._helpers.network import evaluate_network_assertion, network_query
from testmu_selenium._helpers.execute_api import execute_api
from testmu_selenium._helpers.execute_db import execute_db
from testmu_selenium._helpers.cookies import get_cookies
getCookies = get_cookies
# Bind to the public name `type` at module level — note that this shadows the
# builtin only when accessed via `from testmu_selenium import type`. Codegen
# uses `testmu_selenium.type(...)` so no shadowing concern there.
type = _type  # noqa: A001


__all__ = [
    # Lifecycle
    "configure", "test", "run", "step",
    # Failure routing
    "route_failure",
    # HyperExecute per-run test config (data-driven test_params)
    "load_test_config",
    # Variable store
    "var", "set_var", "get_variable_value", "resolve_variable",
    # Runtime helpers
    "findElement", "get_driver", "clickElement", "input_value", "executeJS", "visionQuery", "textualQuery", "smartui_snapshot",
    # High-level action wrappers — element-level (find + heal + act)
    "click", "type", "search", "hover", "clear", "set_input_files", "press_key", "scroll_into_view",
    "drag_drop", "element_drag", "drag_at_coordinate", "clear_at_coordinate", "textual_query",
    # High-level action wrappers — driver-level (no find, no heal)
    "navigate", "wait", "wait_until", "wait_for_load", "check_until_condition", "checkUntilCondition",
    "new_tab", "switch_tab", "close_tab",
    "scroll", "scroll_until_element", "refresh", "go_back", "go_forward",
    "handle_alert",
    "get_url", "get_title",
    # Driver-agnostic helpers
    "evaluate_math", "evaluate_network_assertion", "network_query",
    "execute_api", "execute_db",
    # Heal
    "_heal_cascade", "HealResult",
    # Exceptions
    "TestmuConfigError", "AutohealExhausted", "ClickAllMethodsFailed",
]
