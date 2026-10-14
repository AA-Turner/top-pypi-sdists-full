"""The v4 implementation (mobile export is v4-only today).

``testmu_appium._router`` serves every per-mode public name from here. The
router also reaches ``_vars`` (configure's stores) and ``_reporter`` (step
begin/end).

v4-only: nothing here may import ``testmu_appium._v3``; shared modules
(``_configure``, ``_config``, ``_errors``, ``_step``, ``_test_state``) are
imported from ``testmu_appium``.
"""
from testmu_appium._v4._test_config import test_config_overrides
from testmu_appium._v4._decorator import test
from testmu_appium._v4._session import run, open_session, close_session
from testmu_appium._v4._vars import var, set_var, get_variable_value, resolve_variable
from testmu_appium._v4._route_failure import route_failure
from testmu_appium._v4._helpers.driver import get_driver
from testmu_appium._v4._timing import capture_action_timings
from testmu_appium._v4.perception import (
    ELEMENT_CONTRACT,
    find_by_fingerprint,
    format_for_prompt,
    parse_tree,
    position_hint,
)

# Element verbs — find + heal + act
from testmu_appium._v4._action_click import click
from testmu_appium._v4._action_type import type, search, clear  # noqa: A004
from testmu_appium._v4._action_select import select
from testmu_appium._v4._action_scroll import scroll
from testmu_appium._v4._action_scroll_until import scroll_until
from testmu_appium._v4._action_drag import drag

# Driver verbs — act on the session
from testmu_appium._v4._helpers.navigate import navigate
from testmu_appium._v4._helpers.keyevent import keyevent
from testmu_appium._v4._helpers.app_lifecycle import app_lifecycle
from testmu_appium._v4._helpers.device_control import device_control, device_control_query
from testmu_appium._v4._helpers.geolocation import set_geolocation
from testmu_appium._v4._helpers.wait import wait
from testmu_appium._v4._helpers.smartui import smartui_screenshot
from testmu_appium._v4._helpers.cookies import set_cookies, delete_cookies, clear_cookies
from testmu_appium._v4._helpers.local_storage import (
    set_local_storage, delete_local_storage, clear_local_storage,
)
from testmu_appium._v4._helpers.clipboard import (
    set_clipboard, paste_clipboard, clear_clipboard,
)
from testmu_appium._v4._helpers.navigation_history import go_back, go_forward
from testmu_appium._v4._helpers.refresh import refresh
from testmu_appium._v4._helpers.accessibility import accessibility_scan
from testmu_appium._v4._helpers.tabs import get_tabs, new_tab, switch_tab, close_tab
from testmu_appium._v4._helpers.media_injection import inject_media
from testmu_appium._v4._helpers.network_throttle import network_throttle
from testmu_appium._v4._helpers.network_mock import network_mock

# Value / query verbs
from testmu_appium._v4._helpers.assertion import assertion, evaluate_branch
from testmu_appium._v4._helpers.math import math
from testmu_appium._v4._helpers.verify_assertion import verify_assertion
from testmu_appium._v4._helpers.schema_assertion import verify_schema_assertion
from testmu_appium._v4._helpers.evaluate_math import evaluate_math
from testmu_appium._v4._helpers.condition import check_until_condition
from testmu_appium._v4._helpers.kane_cli import execute_kane_cli
from testmu_appium._v4._helpers.textual_query import textual_query
from testmu_appium._v4._helpers.vision_query import vision_query
from testmu_appium._v4._helpers.execute_api import execute_api
from testmu_appium._v4._helpers.execute_js import execute_js
from testmu_appium._v4._helpers.execute_db import execute_db
from testmu_appium._v4._helpers.textual_analyzer import (
    textual_analyzer,
    textual_analyzer_authoring,
)
from testmu_appium._v4._helpers.network_query import (
    network_query,
    network_capture_query,
    network_capture_capabilities,
    evaluate_network_assertion,
)

# Heal outcomes — exported so a host runtime can introspect a heal result
from testmu_appium._v4._heal import (
    HealDisabled, HealHit, HealNoMatch, HealProtocolError, HealUnavailable,
)


# Modules the router reaches into.
from testmu_appium._v4 import _vars, _reporter  # noqa: E402,F401
