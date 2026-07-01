"""Helper stubs.

Stubs are split into:
- Always-available: work regardless of smart mode (execute_js, execute_api, etc.)
- Smart-gated: only work when TESTMU_SMART=1 (vision, heal, SmartUI, etc.)
"""
import logging
from testmu import _config

_log = logging.getLogger("testmu")


def _stub(name):
    """Create an async stub that always returns None (not smart-gated)."""
    async def stub(*args, **kwargs):
        _log.debug(f"testmu.{name}() stub called — not yet ported")
        return None
    stub.__name__ = name
    stub.__qualname__ = name
    return stub


def _smart_stub(name):
    """Create an async stub that returns None; logs warning only when smart is ON."""
    async def stub(*args, **kwargs):
        if _config.smart:
            _log.warning(f"testmu.{name}() called but not yet ported (stub)")
        return None
    stub.__name__ = name
    stub.__qualname__ = name
    return stub


def _sync_stub(name):
    """Create a sync stub that returns None."""
    def stub(*args, **kwargs):
        _log.debug(f"testmu.{name}() stub called — not yet ported")
        return None
    stub.__name__ = name
    stub.__qualname__ = name
    return stub


# Always available (not smart-gated) — these work with any browser, local or cloud
from testmu._helpers.execute_js import execute_js
from testmu._helpers.execute_api import execute_api, get_api_call_log, clear_api_call_log
from testmu._helpers.execute_db import execute_db
from testmu._helpers.tabs import new_tab, switch_tab, close_tab, ensure_active_page
from testmu._helpers.drag import click_drag, drag_drop, element_drag
from testmu._helpers.gesture import multi_click, long_press
from testmu._helpers.assertion import verify_assertion, evaluate_branch

# Smart-gated — require LT sidecar/AI infrastructure
from testmu._helpers.vision import (
    vision_query,
    textual_query,
    vision_wait,
    vision_action,
    get_vision_coordinates,
)
from testmu._helpers.smartui import smartui_snapshot
from testmu._helpers.textual_analyzer import textual_analyzer

# Smart-gated — real implementations
from testmu._helpers.network import evaluate_network_assertion, network_query
from testmu._helpers.wait import check_until_condition
from testmu._helpers.kane_cli import execute_kane_cli

# Sync deterministic helpers (no I/O, no smart gate)
from testmu._helpers.math import evaluate_math
from testmu._helpers.cookies import get_cookies

# Vision-agent verb (no selector) — smart-gated at call time
from testmu._helpers.scroll_until import scroll_until_element

# Driver-scoped JS-dialog handling (V3) — persistent accept/dismiss policy
from testmu._helpers.dialog import prime_dialog
