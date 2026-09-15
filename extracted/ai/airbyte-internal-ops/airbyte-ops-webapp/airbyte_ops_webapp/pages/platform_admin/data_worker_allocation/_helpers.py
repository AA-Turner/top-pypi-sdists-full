"""Shared helpers for Data Worker Allocation."""

from __future__ import annotations

from typing import Any

from prefab_ui.actions import SetState
from prefab_ui.rx import ERROR, RESULT, STATE

from airbyte_ops_webapp.pages.customer_billing._helpers import (
    auth_available,
    fail_tool_call,
    finish_tool_call,
    resolved_bearer_token,
    resolved_config_api_root,
    start_tool_call,
)


def lookup_success_actions() -> list[SetState]:
    """State updates after a successful allocation lookup."""
    return [
        *finish_tool_call(),
        SetState("org_info", RESULT.org_info),
        SetState("allocations", RESULT.allocations),
        SetState("resolved_org_label", RESULT.resolved_org_label),
        SetState("org_loaded", RESULT.org_loaded),
        SetState("lookup_error", RESULT.lookup_error),
        SetState("allocations_stale", False),
    ]


def lookup_fail_actions() -> list[Any]:
    """State updates after a failed allocation lookup."""
    return [
        *fail_tool_call(ERROR),
        SetState("org_loaded", False),
        SetState("lookup_error", ERROR),
    ]


def apply_success_actions() -> list[Any]:
    """State updates after a capacity change tool call returns.

    A failed or stale result (no `allocations_view`) leaves the overview as-is.
    The replacement view is built by the tool because the renderer does not
    evaluate Rx expressions nested inside a dict literal.
    """
    return [
        *finish_tool_call(),
        SetState("apply_result", RESULT),
        SetState(
            "allocations",
            RESULT.allocations_view.then(RESULT.allocations_view, STATE.allocations),
        ),
        # Only a real success may clear an existing stale warning.
        SetState(
            "allocations_stale",
            RESULT.success.then(RESULT.stale, STATE.allocations_stale),
        ),
        SetState("result_modal_open", True),
    ]


def refresh_fail_actions() -> list[Any]:
    """State updates when the post-change refresh fails."""
    return [
        *fail_tool_call(
            "Refreshing the allocation view failed. The values shown "
            "may be stale - look up the organization again."
        ),
        SetState("allocations_stale", True),
    ]


def apply_fail_actions() -> list[Any]:
    """State updates after capacity addition fails."""
    return [
        *fail_tool_call(ERROR),
        SetState("apply_result", {"success": False, "message": ERROR}),
        SetState("result_modal_open", True),
    ]


__all__ = [
    "apply_fail_actions",
    "apply_success_actions",
    "auth_available",
    "fail_tool_call",
    "finish_tool_call",
    "lookup_fail_actions",
    "lookup_success_actions",
    "refresh_fail_actions",
    "resolved_bearer_token",
    "resolved_config_api_root",
    "start_tool_call",
]
